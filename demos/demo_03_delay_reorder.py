"""Topic 3: 消息延迟 10 秒后乱序到达。

预测:node1->node2 的复制消息被延迟 0~10s 随机打散(乱序);
     延迟窗口内读 node2 得到旧值(场景允许:最终一致性);
     消息全部到达后 node2 收敛,且终值与到达顺序无关(并集合并的交换律)。
解释:state-based CRDT 的 merge 满足交换律/结合律/幂等,
     乱序不影响收敛结果 —— 这正是选择条目集而不是"增量加法"的原因。
"""
import time

from common import C, banner, explain, inject, observe, predict, verdict, wait_converge

PLAYER = "delay-carol"


def main() -> None:
    banner("Topic 3: 消息延迟 10 秒后乱序到达")

    # 基础:通过 node1 写 5 分并等收敛
    for _ in range(5):
        C.write(PLAYER, 1, target="node1")
    ok, scores = wait_converge(PLAYER, expect=5)
    observe(f"基础分数: {scores}")

    predict(
        "node1->node2 注入随机 0~10s 延迟(乱序)后,node1 再写 10 分:\n"
        "     窗口内 node2 读到旧值 5(允许);10s 后全部到达,node2 == 15,与顺序无关"
    )

    inject("proxy 规则: 所有节点 -> node2 的复制消息延迟 0~10s 随机(乱序)")
    C.add_rule("delay", src="node*", dst="node2", seconds=10.0, shuffle=True)

    t_write = time.time()
    for _ in range(10):
        status, _, _ = C.write(PLAYER, 1, target="node1")
        assert status == 200

    # 延迟窗口内:node2 应仍是旧值
    s2_stale = C.score(PLAYER, "node2")[1]["score"]
    s1 = C.score(PLAYER, "node1")[1]["score"]
    observe(f"写入后立刻读: node1 = {s1}(新值), node2 = {s2_stale}(旧值,消息还在路上)")

    # 等乱序消息全部到达(最长 10s 延迟 + gossip 周期,留裕量)
    time.sleep(max(0.0, 10.0 - (time.time() - t_write)) + 3.0)
    ok, scores = wait_converge(PLAYER, expect=15, timeout=20)
    observe(f"延迟窗口结束后: {scores}")

    C.delete_rules_of_type("delay")

    explain(
        "node2 在延迟窗口内读到旧值 5 —— 短暂读旧值是本场景明确允许的语义。\n"
        "     10 条消息随机延迟 0~10s 到达(乱序),但条目集合并 = 并集,\n"
        "     满足交换律:先到后到结果一样,node2 最终 == 15。\n"
        "     如果用『增量加法』复制,乱序重复都可能导致多加/漏加 —— 我们避免了这一点。"
    )
    verdict(ok and scores.get("node2") == 15,
            f"乱序全部到达后 node2 == 15: {scores}")


if __name__ == "__main__":
    main()
