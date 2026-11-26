"""Topic 2: 网络双向分区 + 消息重复发送三次。

预测:分区期间两侧各自接受写入,各自视图只见本侧写入(分歧);
     分区是双向的 -> 互相都不可达;愈合后 gossip 恢复,且重复投递
     的消息不会导致多记(条目按 request_id 去重,幂等)。
解释:CRDT 并集合并 + 幂等 => 重复消息(at-least-once 投递)免费容错;
     分歧收敛 = 两侧之和。
"""
from common import C, NODES, banner, explain, inject, observe, predict, verdict, wait_converge

PLAYER = "part-bob"


def partition(node_a: str, node_b: str) -> None:
    """注入 a<->b 双向分区(消息黑洞,调用方超时)。"""
    C.add_rule("partition", src=node_a, dst=node_b)
    C.add_rule("partition", src=node_b, dst=node_a)


def main() -> None:
    banner("Topic 2: 网络双向分区 + 消息重复发送三次")

    predict(
        "分区(node1 ∥ node2,node3)期间两侧各写 10 分,各自读到的都是 10(看不到对方);\n"
        "     愈合时所有 gossip 消息重复投递 3 次,最终三副本 score 全部 == 20"
    )

    inject("双向分区: node1 <-> node2, node1 <-> node3")
    partition("node1", "node2")
    partition("node1", "node3")

    # 两侧各自写
    for i in range(10):
        status, _, _ = C.write(PLAYER, 1, target="node1")
        assert status == 200
    for i in range(10):
        status, _, _ = C.write(PLAYER, 1, target="node2")
        assert status == 200

    s1 = C.score(PLAYER, "node1")[1]["score"]
    s2 = C.score(PLAYER, "node2")[1]["score"]
    observe(f"分区期间: node1 视图 = {s1}, node2 视图 = {s2} (各只见本侧写入,分歧)")

    inject("节点间消息重复投递 3 次 + 愈合分区")
    C.add_rule("duplicate", src="node*", dst="node*", times=3)
    C.delete_rules_of_type("partition")  # 只移除分区,保留重复投递

    ok, scores = wait_converge(PLAYER, expect=20, timeout=30)
    observe(f"愈合后(消息重复×3): {scores}")

    explain(
        "分区期间两侧独立接受写 -> 分歧(各自 10),这是最终一致系统的正常行为。\n"
        "     愈合后 gossip 恢复,条目并集 = 两侧之和 20。\n"
        "     每条消息被重复投递 3 次,但条目以 request_id 为主键做并集,\n"
        "     重复到达不产生任何额外效果 —— 幂等性让 at-least-once 网络变得安全。"
    )
    verdict(ok and all(v == 20 for v in scores.values()),
            f"重复投递×3 下三副本 score 全部 == 20: {scores}")


if __name__ == "__main__":
    main()
