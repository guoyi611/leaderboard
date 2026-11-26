"""排行榜节点:FastAPI 单 worker 进程。

路由分四组:
- 客户端 API:/write /cas /score /top /lww
- 内部复制 API:/internal/merge /internal/snapshot /internal/pre-write|commit|discard
- 演示控制 API:/admin/clock /admin/wal /admin/slow
- 观测 API:/health /stats

关键机制:
- 写 = 插入不可变条目(request_id 幂等),任意副本可收写(热点分片的本质)
- gossip 后台任务周期性把本地条目集推给随机 peer(异步复制)
- CAS 在"该 key 的静态 primary"上检查+插入;quorum 模式需 W=2 确认
- 时钟 = 系统时间 + clock_offset,可通过 /admin/clock 注入偏移(topic 8)
"""
from __future__ import annotations

import asyncio
import hashlib
import os
import time
from typing import Optional

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

from .store import Entry, Store
from .wal import Wal

NODE_NAME = os.environ.get("NODE_NAME", "node1")
PEERS = [p.strip() for p in os.environ.get("PEERS", "").split(",") if p.strip()]
PROXY_URL = os.environ.get("PROXY_URL", "http://proxy:9000")
WAL_PATH = os.environ.get("WAL_PATH", "/data/wal.log")
WAL_ENABLED = os.environ.get("WAL_ENABLED", "true").lower() == "true"
WAL_FSYNC = os.environ.get("WAL_FSYNC", "true").lower() == "true"
GOSSIP_INTERVAL = float(os.environ.get("GOSSIP_INTERVAL", "1.0"))
ALL_NODES = [p.strip() for p in os.environ.get("ALL_NODES", ",".join([NODE_NAME] + PEERS)).split(",") if p.strip()]
MIGRATE_FROM = os.environ.get("MIGRATE_FROM", "")  # 新节点数据迁移的 seed 节点
MIGRATION_BATCH = int(os.environ.get("MIGRATION_BATCH", "100"))
MIGRATE_DELAY = float(os.environ.get("MIGRATE_DELAY", "0"))

# 演示用可调参数(运行时可通过 /admin/slow 修改)
slow_write_ms = float(os.environ.get("SLOW_WRITE_MS", "5"))  # primary 模式模拟磁盘+锁成本

app = FastAPI(title=f"leaderboard-node-{NODE_NAME}")

store = Store()
wal = Wal(WAL_PATH, enabled=WAL_ENABLED, fsync=WAL_FSYNC)
clock_offset = 0.0
slow_primary_mode = False
write_locks: dict[str, asyncio.Lock] = {}
staging: dict[str, Entry] = {}  # request_id -> Entry(quorum CAS 两阶段用)
cas_results: dict[str, bool] = {}  # request_id -> 成功与否(重试直接回缓存)
migration_progress = {"done": not MIGRATE_FROM, "entries_seen": 0, "batches": 0,
                      "seed": MIGRATE_FROM}
start_time = time.time()


def now() -> float:
    """节点逻辑时钟 = 系统时间 + 可注入偏移。"""
    return time.time() + clock_offset


def primary_of(player: str) -> str:
    """静态一致性哈希:key -> primary 节点。"""
    nodes = sorted(ALL_NODES)
    h = int(hashlib.md5(player.encode()).hexdigest(), 16)
    return nodes[h % len(nodes)]


def _lock_for(player: str) -> asyncio.Lock:
    if player not in write_locks:
        write_locks[player] = asyncio.Lock()
    return write_locks[player]


def _commit_entry(entry: Entry) -> bool:
    """条目落 WAL + 进内存(提交点)。"""
    fresh = store.apply(entry)
    if fresh:
        wal.append_entry(entry)
    return fresh


# 共享连接池(节点间流量都走 proxy,复用连接避免握手开销)
_forward_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _forward_client
    if _forward_client is None:
        _forward_client = httpx.AsyncClient(timeout=5.0)
    return _forward_client


async def _forward(method: str, path: str, target: str, json_body: dict | None = None,
                   timeout: float = 5.0) -> tuple[int, dict | None]:
    """经 proxy 访问其他节点(所有节点间流量都走 proxy,便于注入故障)。"""
    headers = {"X-Source-Node": NODE_NAME, "X-Target-Node": target}
    client = _get_client()
    if method == "GET":
        r = await client.get(f"{PROXY_URL}{path}", headers=headers, timeout=timeout)
    else:
        r = await client.post(f"{PROXY_URL}{path}", json=json_body, headers=headers,
                              timeout=timeout)
    try:
        body = r.json()
    except Exception:
        body = None
    return r.status_code, body


# ---------------- 模型 ----------------

class WriteReq(BaseModel):
    player: str
    delta: int
    request_id: str
    ts: Optional[float] = None  # 缺省用本节点逻辑时钟


class CasReq(BaseModel):
    player: str
    expected: int
    delta: int
    request_id: str
    mode: str = "local"  # local | quorum


class MergeReq(BaseModel):
    entries: list[dict]
    lww: dict[str, list] = {}  # player -> [value, ts]


class PreWriteReq(BaseModel):
    entry: dict


class CommitReq(BaseModel):
    request_id: str


class ClockReq(BaseModel):
    offset_delta: float


class WalReq(BaseModel):
    enabled: bool


class SlowReq(BaseModel):
    enabled: bool
    slow_ms: Optional[float] = None  # 可选:调整锁内模拟磁盘延迟


class LwwWriteReq(BaseModel):
    value: str


# ---------------- 客户端 API ----------------

@app.post("/write")
async def write(req: WriteReq):
    """加分写:本地插条目。任何副本都能收写(写并行度 = 副本数)。"""
    entry = Entry(
        request_id=req.request_id,
        player=req.player,
        delta=req.delta,
        ts=req.ts if req.ts is not None else now(),
        node=NODE_NAME,
    )
    async with _lock_for(req.player):
        if slow_primary_mode:
            # primary 模式:per-key 锁 + 模拟磁盘延迟,热点 key 在单节点上串行化
            await asyncio.sleep(slow_write_ms / 1000)
        fresh = _commit_entry(entry)
    return {
        "ok": True,
        "player": req.player,
        "score": store.score(req.player),
        "duplicate": not fresh,
        "node": NODE_NAME,
    }


@app.post("/cas")
async def cas(req: CasReq):
    """CAS:score(player)==expected 时追加 delta 条目。

    local 模式:本地检查+插入(分区双主下两侧都可能成功 -> 违反线性一致,演示点)
    quorum 模式:需 W=2 个节点 pre-write 确认后才 commit,分区少数侧失败
    """
    if req.request_id in cas_results:  # 重试直接回缓存(幂等)
        return {"ok": cas_results[req.request_id], "player": req.player,
                "score": store.score(req.player), "retried": True, "node": NODE_NAME}

    entry = Entry(req.request_id, req.player, req.delta, now(), NODE_NAME)

    async with _lock_for(req.player):
        current = store.score(req.player)
        if current != req.expected:
            cas_results[req.request_id] = False
            return {"ok": False, "reason": f"expected {req.expected}, got {current}",
                    "player": req.player, "score": current, "node": NODE_NAME}
        if req.mode == "quorum":
            ok = await _quorum_cas(entry)
            cas_results[req.request_id] = ok
            return {"ok": ok, "player": req.player,
                    "score": store.score(req.player), "mode": "quorum", "node": NODE_NAME}
        _commit_entry(entry)
        cas_results[req.request_id] = True
        return {"ok": True, "player": req.player,
                "score": store.score(req.player), "mode": "local", "node": NODE_NAME}


async def _quorum_cas(entry: Entry, w: int = 2) -> bool:
    """两阶段:pre-write 暂存 -> ack>=W 则 commit,否则 discard。

    peer 调用并发 + 短超时,分区黑洞下快速失败而不是串行拖满客户端超时。
    """
    staging[entry.request_id] = entry

    async def pre_write(peer: str) -> bool:
        try:
            status, _ = await _forward("POST", "/internal/pre-write",
                                       target=peer, json_body={"entry": entry.to_dict()},
                                       timeout=1.5)
            return status == 200
        except Exception:
            return False

    results = await asyncio.gather(*[pre_write(p) for p in PEERS])
    acks = 1 + sum(results)
    ok = acks >= w
    action = "/internal/commit" if ok else "/internal/discard"

    async def notify(peer: str):
        try:
            await _forward("POST", action, target=peer,
                           json_body={"request_id": entry.request_id}, timeout=1.5)
        except Exception:
            pass

    await asyncio.gather(*[notify(p) for p in PEERS])
    if ok:
        _commit_entry(entry)
    else:
        staging.pop(entry.request_id, None)
    return ok


@app.get("/score/{player}")
async def score(player: str, mode: str = "local"):
    """读:默认本地视图(可短暂旧值,场景允许);quorum 读 R=2 降低旧值概率。"""
    if mode == "quorum":
        async def read_peer(peer: str):
            try:
                status, body = await _forward("GET", f"/score/{player}",
                                              target=peer, timeout=1.5)
                if status == 200:
                    return body["score"]
            except Exception:
                pass
            return None

        results = await asyncio.gather(*[read_peer(p) for p in PEERS])
        values = [store.score(player)] + [v for v in results if v is not None]
        acks = len(values)
        return {"player": player, "score": max(values), "acks": acks, "mode": "quorum",
                "node": NODE_NAME}
    return {"player": player, "score": store.score(player), "mode": "local", "node": NODE_NAME}


@app.get("/top/{n}")
async def top(n: int):
    return {"top": store.top(n), "node": NODE_NAME, "ts": now()}


@app.post("/lww/{player}")
async def lww_write(player: str, req: LwwWriteReq):
    """LWW 寄存器写(仅 topic 8 反例演示用)。ts 取本节点逻辑时钟。"""
    accepted = store.lww_write(player, req.value, now())
    if accepted:
        wal.append_lww(player, req.value, now())
    return {"accepted": accepted, "node": NODE_NAME,
            "current": store.lww_read(player)}


@app.get("/lww/{player}")
async def lww_read(player: str):
    return {"player": player, "value": store.lww_read(player), "node": NODE_NAME}


# ---------------- 内部复制 API ----------------

@app.post("/internal/merge")
async def internal_merge(req: MergeReq):
    """gossip 合并:条目并集 + LWW 取 max ts。幂等。"""
    entries = [Entry.from_dict(d) for d in req.entries]
    added = store.merge(entries)
    for player, (value, ts) in req.lww.items():
        store.lww_merge(player, value, ts)
    return {"added": added, "node": NODE_NAME}


@app.get("/internal/snapshot")
async def internal_snapshot(after: str = "", limit: int = 100):
    """分页导出条目(新节点数据迁移用)。游标 = 最后一条 request_id。"""
    entries, cursor = store.snapshot(after=after, limit=limit)
    return {"entries": [e.to_dict() for e in entries], "cursor": cursor,
            "lww": {p: list(v) for p, v in store.lww_all().items()},
            "node": NODE_NAME}


@app.post("/internal/pre-write")
async def internal_pre_write(req: PreWriteReq):
    staging[req.entry["request_id"]] = Entry.from_dict(req.entry)
    return {"ok": True}


@app.post("/internal/commit")
async def internal_commit(req: CommitReq):
    entry = staging.pop(req.request_id, None)
    if entry is not None:
        _commit_entry(entry)
    return {"ok": True}


@app.post("/internal/discard")
async def internal_discard(req: CommitReq):
    staging.pop(req.request_id, None)
    return {"ok": True}


# ---------------- 演示控制 API ----------------

@app.post("/admin/clock")
async def admin_clock(req: ClockReq):
    """注入时钟偏移(topic 8:系统时间突然倒退一分钟)。"""
    global clock_offset
    clock_offset += req.offset_delta
    return {"node": NODE_NAME, "clock_offset": clock_offset, "now": now()}


@app.get("/admin/clock")
async def get_clock():
    return {"node": NODE_NAME, "clock_offset": clock_offset, "now": now(),
            "system_time": time.time()}


@app.post("/admin/wal")
async def admin_wal(req: WalReq):
    wal.enabled = req.enabled
    if req.enabled:
        wal.open()
    return {"node": NODE_NAME, "wal_enabled": wal.enabled}


@app.post("/admin/slow")
async def admin_slow(req: SlowReq):
    """topic 6:开启 primary 模式写路径的锁+磁盘延迟。"""
    global slow_primary_mode, slow_write_ms
    slow_primary_mode = req.enabled
    if req.slow_ms is not None:
        slow_write_ms = req.slow_ms
    return {"node": NODE_NAME, "slow_primary_mode": slow_primary_mode,
            "slow_ms": slow_write_ms}


@app.get("/health")
async def health():
    return {"node": NODE_NAME, "status": "up", "uptime": time.time() - start_time}


@app.get("/stats")
async def stats():
    return {
        "node": NODE_NAME,
        "entry_count": store.entry_count(),
        "total": store.total(),
        "player_count": len(store._entries),
        "clock_offset": clock_offset,
        "wal_enabled": wal.enabled,
        "slow_primary_mode": slow_primary_mode,
        "slow_ms": slow_write_ms,
        "peers": PEERS,
        "migration": migration_progress,
        "primary_map": {p: primary_of(p) for p in PRIMARY_PROBE},
    }


PRIMARY_PROBE = [f"p{i}" for i in range(12)]


# ---------------- gossip / 迁移后台任务 ----------------

async def gossip_loop():
    """周期性向所有 peer 推送本地状态(state-based 异步复制)。

    全量 push:3 副本规模下开销可接受,收敛无随机盲区
    (单随机 peer push 会留下『恰好一直没被选中』的传播空洞)。
    """
    while True:
        await asyncio.sleep(GOSSIP_INTERVAL)
        if not PEERS:
            continue
        entries, _ = store.snapshot("", 10_000)
        payload = {
            "entries": [e.to_dict() for e in entries],
            "lww": {p: list(v) for p, v in store.lww_all().items()},
        }
        for peer in PEERS:
            try:
                await _forward("POST", "/internal/merge", target=peer,
                               json_body=payload)
            except Exception:
                pass  # peer 不可达:下个周期再试(最终一致性)


async def migration_loop():
    """新节点从 seed 分页拉取全量条目(数据迁移)。

    - 条目不可变 + 并集 merge => 迁移天然幂等,中途宕机重启重拉不会多算
    - 游标 = 上一批最后一条 request_id(字典序),支持断点续传语义
    """
    cursor = ""
    while True:
        try:
            status, body = await _forward(
                "GET",
                f"/internal/snapshot?after={cursor}&limit={MIGRATION_BATCH}",
                target=MIGRATE_FROM, timeout=10.0,
            )
        except Exception:
            await asyncio.sleep(1.0)
            continue
        if status != 200 or body is None:
            await asyncio.sleep(1.0)
            continue
        entries = [Entry.from_dict(d) for d in body["entries"]]
        store.merge(entries)
        for player, (value, ts) in (body.get("lww") or {}).items():
            store.lww_merge(player, value, ts)
        migration_progress["entries_seen"] += len(entries)
        migration_progress["batches"] += 1
        cursor = body["cursor"]
        if not cursor:
            migration_progress["done"] = True
            break
        await asyncio.sleep(MIGRATE_DELAY)


@app.on_event("startup")
async def startup():
    restored = wal.replay(store)
    if restored:
        print(f"[{NODE_NAME}] WAL 恢复 {restored} 条记录")
    asyncio.create_task(gossip_loop())
    if MIGRATE_FROM:
        print(f"[{NODE_NAME}] 开始从 {MIGRATE_FROM} 迁移数据")
        asyncio.create_task(migration_loop())
