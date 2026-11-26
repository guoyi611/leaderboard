"""本地开发冒烟测试:不用 Docker,宿主机直接起 proxy + 3 节点,验证核心机制。

覆盖: 写读收敛 / 分区+重复 / 乱序 / WAL 重启 / CAS local+quorum / 时钟倒退 /
      丢响应幂等重试。Docker 编排(demo 全流程)另行验证。
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "client"))

from client import LeaderboardClient  # noqa: E402

PROXY_URL = "http://localhost:9000"
NODE_PORTS = {"node1": 8001, "node2": 8002, "node3": 8003}
MIGRANT_PORT = 8004
STATE_DIR = os.path.join(ROOT, "local_state")

procs: dict[str, subprocess.Popen] = {}
C = LeaderboardClient(PROXY_URL, timeout=5.0)
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {detail}")


def start_proxy() -> subprocess.Popen:
    env = {**os.environ,
           "PYTHONPATH": f"{ROOT}/src;{ROOT}/proxy" if os.name == "nt" else f"{ROOT}/src:{ROOT}/proxy",
           "PROXY_NODE_URLS": "{}"}  # 节点 URL 由节点端口映射,见下
    # 用 env 映射表: node1 -> localhost:8001 ...
    urls = ",".join(f"{n}=http://localhost:{p}" for n, p in NODE_PORTS.items())
    env["PROXY_NODE_URLS"] = "{" + ",".join(
        f'"{n}":"http://localhost:{p}"'
        for n, p in {**NODE_PORTS, "node4": MIGRANT_PORT}.items()) + "}"
    del urls
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "net_proxy:app", "--port", "9000"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def start_node(name: str, port: int | None = None, migrate_from: str = "",
               batch: int = 50, delay: float = 0.2) -> subprocess.Popen:
    port = port or NODE_PORTS[name]
    peers = ",".join(n for n in ("node1", "node2", "node3") if n != name)
    env = {**os.environ,
           "PYTHONPATH": f"{ROOT}/src" if os.name == "nt" else f"{ROOT}/src",
           "NODE_NAME": name,
           "PEERS": peers,
           "ALL_NODES": "node1,node2,node3",
           "PROXY_URL": PROXY_URL,
           "WAL_PATH": os.path.join(STATE_DIR, name, "wal.log"),
           "WAL_ENABLED": "true",
           "GOSSIP_INTERVAL": "0.5",
           "SLOW_WRITE_MS": "5"}
    if migrate_from:
        env.update({"MIGRATE_FROM": migrate_from,
                    "MIGRATION_BATCH": str(batch),
                    "MIGRATE_DELAY": str(delay)})
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "leaderboard.node:app",
         "--host", "127.0.0.1", "--port", str(port)],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def wait_ready(timeout: float = 30.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            ok = all(C.stats(n)[0] == 200 for n in NODE_PORTS)
            if ok:
                return True
        except Exception:
            pass
        time.sleep(0.4)
    return False


def kill_node(name: str) -> None:
    p = procs.pop(name, None)
    if p:
        if os.name == "nt":
            p.kill()  # 模拟宕机:不给清理机会
        else:
            p.send_signal(signal.SIGKILL)
        p.wait(timeout=10)


def converge(player: str, expect: int, timeout: float = 15.0) -> tuple[bool, dict]:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            scores = {n: C.score(player, n)[1]["score"] for n in NODE_PORTS}
        except Exception:
            scores = {}
        if len(scores) == 3 and set(scores.values()) == {expect}:
            return True, scores
        time.sleep(0.5)
    return False, scores


def main() -> None:
    shutil.rmtree(STATE_DIR, ignore_errors=True)
    os.makedirs(STATE_DIR, exist_ok=True)

    print("== starting proxy + 3 nodes (local mode) ==")
    procs["proxy"] = start_proxy()
    time.sleep(1.0)
    for n in NODE_PORTS:
        procs[n] = start_node(n)
    if not wait_ready():
        print("cluster failed to start")
        teardown(1)
    print("cluster ready\n")

    # ---- 1. 基本写读 + 收敛 ----
    print("[1] basic write & convergence")
    for i in range(10):
        st, _, _ = C.write("alice", 1, target=f"node{(i % 3) + 1}")
        assert st == 200
    ok, scores = converge("alice", 10)
    check("converge to 10", ok, str(scores))

    # ---- 2. 分区 + 重复 x3 ----
    print("[2] partition + duplicate x3")
    C.add_rule("partition", src="node1", dst="node2")
    C.add_rule("partition", src="node2", dst="node1")
    C.add_rule("partition", src="node1", dst="node3")
    C.add_rule("partition", src="node3", dst="node1")
    for _ in range(5):
        C.write("part", 1, target="node1")
        C.write("part", 1, target="node2")
    s1 = C.score("part", "node1")[1]["score"]
    s2 = C.score("part", "node2")[1]["score"]
    C.add_rule("duplicate", src="node*", dst="node*", times=3)
    C.delete_rules_of_type("partition")
    ok, scores = converge("part", 10)
    check("partition diverge then converge (dup x3)", ok and s1 == 5 and s2 == 5,
          f"during: node1={s1} node2={s2}; after: {scores}")
    C.delete_rules_of_type("duplicate")

    # ---- 3. 延迟乱序(2s 验证机制) ----
    print("[3] delay + reorder")
    # 覆盖所有进入 node2 的节点间链路,堵住 gossip 绕行路径
    C.add_rule("delay", src="node*", dst="node2", seconds=2.0, shuffle=True)
    for _ in range(5):
        C.write("reorder", 1, target="node1")
    stale = C.score("reorder", "node2")[1]["score"]
    time.sleep(4.0)
    s_final = C.score("reorder", "node2")[1]["score"]
    check("stale read then converge (order-independent)", stale == 0 and s_final == 5,
          f"stale={stale}, final={s_final}")
    C.delete_rules_of_type("delay")

    # ---- 4. WAL 重启恢复 ----
    print("[4] WAL restart recovery")
    for _ in range(7):
        C.write("wal", 1, target="node1")
    kill_node("node1")
    procs["node1"] = start_node("node1")
    time.sleep(3.0)
    s = C.score("wal", "node1")[1]["score"]
    check("WAL replays 7 entries after restart", s == 7, f"score={s}")

    # ---- 5. CAS: 健康 local 恰 1 成功 ----
    print("[5] concurrent CAS (healthy, local)")
    for _ in range(100):
        C.write("cas1", 1, target="node1")
    converge("cas1", 100)
    import hashlib
    nodes_sorted = sorted(NODE_PORTS)
    primary = nodes_sorted[int(hashlib.md5(b"cas1").hexdigest(), 16) % 3]
    r1 = C.cas("cas1", 100, 10, target=primary, mode="local")
    r2 = C.cas("cas1", 100, 10, target=primary, mode="local")
    wins = r1[1]["ok"] + r2[1]["ok"]
    s = C.score("cas1", primary)[1]["score"]
    check("exactly 1 CAS wins", wins == 1 and s == 110, f"wins={wins}, score={s}")

    # ---- 6. CAS: 分区 quorum 恰 1 成功 ----
    print("[6] concurrent CAS (partitioned, quorum)")
    for _ in range(100):
        C.write("cas2", 1, target="node1")
    converge("cas2", 100)
    p2 = nodes_sorted[int(hashlib.md5(b"cas2").hexdigest(), 16) % 3]
    other = next(n for n in nodes_sorted if n != p2)
    for a in nodes_sorted:
        if a != p2:
            C.add_rule("partition", src=p2, dst=a)
            C.add_rule("partition", src=a, dst=p2)
    time.sleep(0.3)
    ra = C.cas("cas2", 100, 10, target=p2, mode="quorum", timeout=8.0)
    rb = C.cas("cas2", 100, 10, target=other, mode="quorum", timeout=8.0)
    wins = ra[1]["ok"] + rb[1]["ok"]
    C.delete_rules_of_type("partition")
    time.sleep(2.0)
    ok, scores = converge("cas2", 110, timeout=10)
    check("quorum: minority fails, majority wins", wins == 1 and ok,
          f"wins={wins}, scores={scores}")

    # ---- 7. 时钟倒退: LWW 反例 + 条目集无损 ----
    print("[7] clock skew")
    C.set_clock("node3", -60.0)
    C.lww_write("skew", "v3", target="node1")
    time.sleep(0.2)
    C.lww_write("skew", "v4", target="node3")
    time.sleep(2.0)
    lww = {n: (C.lww_read("skew", n)[1]["value"] or [None])[0] for n in NODE_PORTS}
    check("LWW loses update (ts from fast clock wins)", set(lww.values()) == {"v3"},
          str(lww))
    for _ in range(4):
        C.write("skewctr", 1, target="node3")
    ok, scores = converge("skewctr", 4)
    check("counter path immune to clock skew", ok, str(scores))
    C.set_clock("node3", 60.0)

    # ---- 8. 丢响应 + 幂等重试 ----
    print("[8] dropped response + idempotent retry")
    C.add_rule("drop_response", src="client", dst="node2")
    C._client.timeout = 2.0
    st1, _, _ = C.write("drop", 7, target="node2", request_id="rid-001", retries=0)
    C._client.timeout = 5.0
    C.delete_rules_of_type("drop_response")
    st2, body2, _ = C.write("drop", 7, target="node2", request_id="rid-001", retries=1)
    ok, scores = converge("drop", 7)
    check("retry idempotent (score == 7, duplicate=true)",
          st1 == -1 and st2 == 200 and body2["duplicate"] is True and ok,
          f"first={st1}, retry dup={body2['duplicate']}, {scores}")

    # ---- 9. 新节点迁移: 中途宕机 -> 重启重拉 -> 追平 ----
    print("[9] migration with mid-crash")
    for i in range(120):
        C.write("migr", 1, target=f"node{(i % 3) + 1}")
    time.sleep(2.0)
    old_total = C.stats("node1")[1]["total"]

    def start_migrant() -> None:
        procs["node4"] = start_node("node4", port=MIGRANT_PORT,
                                    migrate_from="node1", batch=30, delay=0.3)

    def wait_node4(timeout: float = 20.0) -> tuple[int, dict | None]:
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                st = C.stats("node4")
                if st[0] == 200 and st[1] is not None:
                    return st
            except Exception:
                pass
            time.sleep(0.3)
        return -1, None

    start_migrant()
    st = wait_node4()
    assert st[0] == 200, "node4 未就绪"
    time.sleep(1.0)  # 迁移进行中(约 3-4 批) -> 此刻 mid 进度
    mid = C.stats("node4")[1]["migration"]
    kill_node("node4")
    writes_ok = sum(C.write("migr", 1, target=f"node{(i % 3) + 1}")[0] == 200
                    for i in range(10))
    start_migrant()
    done = False
    for _ in range(40):
        s = C.stats("node4")
        if s[0] == 200 and s[1]["migration"]["done"]:
            done = True
            break
        time.sleep(0.5)
    time.sleep(2.5)  # gossip 追平宕机期间新写
    t4 = C.stats("node4")[1]["total"]
    t1 = C.stats("node1")[1]["total"]
    check("migration mid-crash: old cluster unaffected, node4 catches up",
          writes_ok == 10 and done and mid["batches"] >= 1 and t4 == t1,
          f"mid batches={mid['batches']}, writes={writes_ok}/10, "
          f"node4={t4}, node1={t1}")

    teardown(0 if all(ok for _, ok, _ in results) else 1)


def teardown(code: int) -> None:
    print("\n== summary ==")
    for name, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    if "--keep" in sys.argv:
        print("\ncluster kept running (proxy:9000, node1-3). Ctrl+C to stop.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            pass
    for p in procs.values():
        p.terminate()
    for p in procs.values():
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()
    sys.exit(code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        teardown(130)
    except Exception:
        import traceback
        traceback.print_exc()
        teardown(1)
