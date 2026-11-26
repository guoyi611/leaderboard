"""Topic 1: 一个副本突然宕机。

预测:宕机期间写继续成功(其余副本可收写);恢复后通过 anti-entropy gossip
     自动补齐缺失条目,最终三副本收敛到相同值(最终一致性)。
解释:异步复制下副本可能暂时落后,可用性不依赖单个副本;
     恢复靠周期性 state-based merge,无需人工干预。
"""
from common import C, NODES, banner, explain, inject, observe, predict, verdict, \
    kill_node, start_node, wait_converge, wait_up

PLAYER = "crash-alice"


def main() -> None:
    banner("Topic 1: 一个副本突然宕机")

    # 基础写入并收敛
    for i in range(20):
        C.write(PLAYER, 1, target=NODES[i % 2])
    ok, scores = wait_converge(PLAYER, expect=20)
    observe(f"宕机前: {scores} (三副本一致)")

    predict("kill node3 后继续写全部成功;node3 重启后 2 个 gossip 周期内自动补齐")

    inject("docker compose kill node3")
    kill_node("node3")

    total_before = 20
    for i in range(10):
        status, body, _ = C.write(PLAYER, 1, target=NODES[i % 2])
        assert status == 200, f"宕机期间写入失败: {status}"
    observe("宕机期间向 node1/node2 写入 10 次,全部成功 (可用性未受影响)")

    inject("docker compose start node3 (重启恢复)")
    start_node("node3")
    assert wait_up("node3"), "node3 未能在 30s 内启动"

    ok, scores = wait_converge(PLAYER, expect=total_before + 10, timeout=30)
    observe(f"node3 恢复后: {scores}")

    explain(
        "异步复制意味着 node3 宕机时错过 10 条写入(暂时落后),但集群仍可写。\n"
        "     node3 重启后,周期性 gossip 把 node1/node2 的条目集推给它,\n"
        "     条目并集 merge 使它追平到 30 —— 最终一致性,未违反任何承诺:\n"
        "     本场景允许短暂读旧值,收敛前 node3 的读都是旧值。"
    )
    verdict(ok and all(v == 30 for v in scores.values()),
            f"三副本 score 全部 == 30: {scores}")


if __name__ == "__main__":
    main()
