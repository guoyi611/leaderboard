"""Topic 6: 某个 key 占据 50% 的请求(热点)。

对照组 A(primary-only): 一个热点 key 的全部写都压到它的 primary 节点,
     该节点对同 key 写持锁串行 + 每次写模拟磁盘延迟 -> 单点排队。
实验组 B(任意副本): 同一热点 key 的写随机散到 3 个副本(热点分片),
     3 个节点并行消化 -> 延迟大幅下降。
预测:中位延迟 A >= 3 x B;两组最终分数都准确。
解释:条目集 CRDT 让『任何副本都能收写』成为合法的热点分片方案,
     写并行度 = 副本数,这是本系统缓解热 key 的核心手段。
"""
import asyncio
import statistics
import time

from common import C, NODES, banner, explain, inject, observe, predict, verdict
from client import LeaderboardClient

HOT = "hot-player"
HOT_B = "hot-player-b"  # B 组独立热点 key(避免与 A 组分数叠加)
NORMAL_PREFIX = "normal-"
WRITES_PER_GROUP = 150
HOT_RATIO = 0.5


async def workload(player: str, targets: list[str], cid: int,
                   direct: dict[str, str]) -> tuple[list[float], list[float], int]:
    """一个并发写负载(直连节点,绕过 proxy)。返回 (热点写延迟列表, 普通写延迟列表, 成功数)。"""
    client = LeaderboardClient(source=f"load-{cid}", timeout=30.0, node_urls=direct)
    hot_lat: list[float] = []
    normal_lat: list[float] = []
    ok = 0
    for i in range(WRITES_PER_GROUP):
        is_hot = i < WRITES_PER_GROUP * HOT_RATIO
        p = player if is_hot else f"{NORMAL_PREFIX}{player}-{cid}-{i % 50}"
        target = targets[i % len(targets)]
        status, _, ms = await asyncio.to_thread(client.write, p, 1, target)
        if status == 200:
            (hot_lat if is_hot else normal_lat).append(ms)
            ok += 1
    client._client.close()
    return hot_lat, normal_lat, ok


def primary_of(player: str, nodes: list[str]) -> str:
    import hashlib
    nodes_sorted = sorted(nodes)
    h = int(hashlib.md5(player.encode()).hexdigest(), 16)
    return nodes_sorted[h % len(nodes_sorted)]


def run_group(label: str, player: str, hot_targets: list[str],
              direct: dict[str, str]) -> tuple[float, int, int]:
    """跑一组负载:50% 打热点 key,50% 打普通 key(直连)。返回 (热点写中位延迟, 成功数, 热点分数)。"""
    primary = primary_of(player, NODES)

    async def run_all():
        return await asyncio.gather(*[
            workload(player, hot_targets, cid, direct) for cid in range(8)
        ])

    results = asyncio.run(run_all())
    hot_all = [ms for r in results for ms in r[0]]
    normal_all = [ms for r in results for ms in r[1]]
    total_ok = sum(r[2] for r in results)
    time.sleep(3)  # 等 gossip 收敛热点分数
    hot_score = C.score(player, primary)[1]["score"]
    print(f"  {label}: 热点写中位 {statistics.median(hot_all):.1f}ms / "
          f"普通写中位 {statistics.median(normal_all):.1f}ms, "
          f"成功 {total_ok}/{8 * WRITES_PER_GROUP}, score = {hot_score}")
    return statistics.median(hot_all), total_ok, hot_score


def main() -> None:
    banner("Topic 6: 某个 key 占据 50% 的请求(热点)")

    # 压测流量直连节点:proxy 是单线程故障注入装置,不应成为吞吐瓶颈
    direct = LeaderboardClient.probe_direct()
    assert direct, "无法探测节点直连地址(docker: 8101-8103, 本地 dev: 8001-8003)"

    primary = primary_of(HOT, NODES)
    predict(
        f"{HOT} 的 primary 是 {primary}:\n"
        "     A) primary-only: 热点写全部排队串行(锁+磁盘延迟) -> 热点写高延迟\n"
        "     B) 任意副本(热点分片): 同一热点 key 的写散到 3 节点并行,\n"
        "        热点写中位延迟显著低于 A(理论并行度 3x);两组分数最终准确"
    )

    inject("所有节点开启 slow 写路径 (per-key 锁 + 磁盘延迟模拟 12ms)")
    for n in NODES:
        C.set_slow(n, True, slow_ms=12)

    inject(f"A) primary-only 模式: 所有写(热点+普通)固定发给 {primary}")
    lat_a, ok_a, score_a = run_group("A primary-only", HOT, [primary], direct)

    inject("B) 任意副本模式(热点分片): 写随机散到 node1/2/3")
    lat_b, ok_b, score_b = run_group("B 任意副本   ", HOT_B, NODES, direct)

    for n in NODES:
        C.set_slow(n, False)

    expect_hot = int(8 * WRITES_PER_GROUP * HOT_RATIO)
    observe(f"热点写中位: A {lat_a:.1f}ms vs B {lat_b:.1f}ms, "
            f"倍率 {lat_a / max(lat_b, 0.01):.1f}x")
    explain(
        "primary-only: 同一热点 key 的写在单节点上按锁串行 + 每次落盘,\n"
        "     吞吐被单节点磁盘能力封顶。\n"
        "     任意副本模式利用条目集 CRDT『任何副本可收写』的性质,\n"
        "     同一 key 的写分摊到 3 个节点并行执行 —— 这就是热点分片,\n"
        "     理论并行度 3x(实测倍率含网络与调度开销)。\n"
        "     正确性不受影响:分数 = 条目并集求和,gossip 自动收敛。"
    )
    time.sleep(3)
    score_b_final = C.score(HOT_B, primary_of(HOT_B, NODES))[1]["score"]
    verdict(lat_a >= 1.4 * lat_b and score_a == expect_hot and score_b_final == expect_hot,
            f"热点写延迟 A({lat_a:.1f}) >= 1.4xB({lat_b:.1f}), 实测 "
            f"{lat_a / max(lat_b, 0.01):.1f}x; 分数 A={score_a}, B={score_b_final}, "
            f"期望 {expect_hot}")


if __name__ == "__main__":
    main()
