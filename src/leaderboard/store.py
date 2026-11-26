"""CRDT 存储核心:不可变条目集 + 并集合并。

核心思想(整个系统正确性的基石):
- 每次加分写是一条不可变条目 (request_id, player, delta, ts, node)
- score(player) = 该玩家全部条目 delta 之和
- merge = 按 request_id 求并集

由此免费获得四个性质:
1. 幂等:同一条目重复投递/重试,并集不变(topic 2 消息重复、topic 9 客户端重试)
2. 交换律+结合律:乱序到达、任意顺序合并,结果相同(topic 3 延迟乱序)
3. 崩溃安全:WAL 只需追加条目,重放即恢复(topic 4 重启丢内存)
4. 分区收敛:两侧各自追加不同条目,愈合后并集 = 两侧之和(topic 2 双向分区)
"""
from __future__ import annotations

import random
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Entry:
    request_id: str
    player: str
    delta: int
    ts: float
    node: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Entry":
        return Entry(
            request_id=d["request_id"],
            player=d["player"],
            delta=int(d["delta"]),
            ts=float(d["ts"]),
            node=d["node"],
        )


@dataclass(frozen=True)
class LwwValue:
    """LWW 寄存器:按时间戳取最大者。仅用于 topic 8 的反例演示。

    主路径(条目集)完全不依赖时间戳排序,这正是
    "为什么不能只用物理时钟解决冲突"的答案。
    """

    ts: float
    value: str


class Store:
    def __init__(self) -> None:
        # player -> {request_id: Entry}
        self._entries: dict[str, dict[str, Entry]] = {}
        # player -> LwwValue
        self._lww: dict[str, LwwValue] = {}

    # ---------- 条目集 ----------

    def apply(self, entry: Entry) -> bool:
        """插入单条条目。返回 True 表示新条目,False 表示重复(已存在)。"""
        bucket = self._entries.setdefault(entry.player, {})
        if entry.request_id in bucket:
            return False
        bucket[entry.request_id] = entry
        return True

    def merge(self, entries: list[Entry]) -> int:
        """并集合并一批条目,返回新增条数。幂等、与顺序无关。"""
        added = 0
        for e in entries:
            if self.apply(e):
                added += 1
        return added

    def score(self, player: str) -> int:
        return sum(e.delta for e in self._entries.get(player, {}).values())

    def total(self) -> int:
        return sum(self.score(p) for p in self._entries)

    def top(self, n: int) -> list[tuple[str, int]]:
        """本地视图的 Top-N。可能读到旧值(最终一致性,场景允许)。"""
        scores = [(p, self.score(p)) for p in self._entries]
        scores.sort(key=lambda x: (-x[1], x[0]))
        return scores[:n]

    def snapshot(self, after: str = "", limit: int = 1000) -> tuple[list[Entry], str]:
        """按 request_id 字典序分页导出条目(数据迁移用)。

        after 为空串表示从头开始。返回 (条目列表, 下一页游标)。
        游标为空串表示没有更多数据。
        """
        flat: list[Entry] = []
        for bucket in self._entries.values():
            flat.extend(bucket.values())
        flat.sort(key=lambda e: e.request_id)
        result = [e for e in flat if e.request_id > after][:limit]
        cursor = result[-1].request_id if len(result) == limit else ""
        return result, cursor

    def entries_of(self, player: str) -> list[Entry]:
        return list(self._entries.get(player, {}).values())

    def entry_count(self) -> int:
        return sum(len(b) for b in self._entries.values())

    # ---------- LWW 寄存器(topic 8 反例用) ----------

    def lww_write(self, player: str, value: str, ts: float) -> bool:
        """ts 大者胜。返回是否接受本次写入。"""
        cur = self._lww.get(player)
        if cur is None or ts > cur.ts:
            self._lww[player] = LwwValue(ts=ts, value=value)
            return True
        return False

    def lww_merge(self, player: str, value: str, ts: float) -> None:
        self.lww_write(player, value, ts)

    def lww_read(self, player: str) -> tuple[str, float] | None:
        v = self._lww.get(player)
        return (v.value, v.ts) if v else None

    def lww_all(self) -> dict[str, tuple[str, float]]:
        return {p: (v.value, v.ts) for p, v in self._lww.items()}


def random_merge_converges(trials: int = 200) -> None:
    """自测:随机乱序 + 随机重复合并,验证收敛性(演示断言的理论依据)。"""
    rng = random.Random(42)
    for _ in range(trials):
        entries = [
            Entry(f"r{i}", f"p{i % 5}", rng.randint(1, 10), rng.random(), "n1")
            for i in range(50)
        ]
        a, b, c = Store(), Store(), Store()
        for store in (a, b, c):
            shuffled = entries[:]
            rng.shuffle(shuffled)
            # 每条消息重复 3 次
            tripled = [e for e in shuffled for _ in range(3)]
            rng.shuffle(tripled)
            store.merge(tripled)
        merged = Store()
        merged.merge(a.snapshot("", 10_000)[0])
        merged.merge(b.snapshot("", 10_000)[0])
        merged.merge(c.snapshot("", 10_000)[0])
        assert a.total() == b.total() == c.total() == merged.total(), "收敛性被破坏"
    print(f"random_merge_converges: {trials} trials OK")


if __name__ == "__main__":
    random_merge_converges()
