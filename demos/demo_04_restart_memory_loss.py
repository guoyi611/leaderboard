"""Topic 4: 节点重启后丢失内存状态。

对照实验(用分区把 carol 的数据隔离在 node3 单副本上,排除 peer 恢复干扰):
  A. WAL 开: 写 10 -> kill/start -> 启动即恢复 10 (WAL 重放)
  B. WAL 关: 再写 5 (只在内存) -> kill/start -> 恢复到 10, 丢失 5
预测:A 恢复完整;B 丢失关 WAL 之后的写入。
解释:内存态易失,WAL(追加+fsync)把提交点从内存移到磁盘;
     重放幂等(条目 request_id 去重),重复恢复无害。
"""
from common import C, banner, explain, inject, observe, predict, verdict, \
    kill_node, start_node, wait_up

PLAYER = "wal-dave"


def restart_and_read() -> int:
    kill_node("node3")
    start_node("node3")
    assert wait_up("node3"), "node3 启动超时"
    return C.score(PLAYER, "node3")[1]["score"]


def main() -> None:
    banner("Topic 4: 节点重启后丢失内存状态")

    # 隔离 node3: 数据只存在于 node3(排除 gossip 从 peer 恢复的干扰)
    predict(
        "node3 独区持有数据:\n"
        "     A) WAL 开:写 10 -> 重启 -> 恢复 10\n"
        "     B) WAL 关:再写 5 -> 重启 -> 只有 10,丢 5 (内存态丢失)"
    )
    inject("隔离 node3 (node3 <-> node1/node2 分区), 数据单副本化")
    C.add_rule("partition", src="node3", dst="node1")
    C.add_rule("partition", src="node1", dst="node3")
    C.add_rule("partition", src="node3", dst="node2")
    C.add_rule("partition", src="node2", dst="node3")

    # A: WAL 开
    C.set_wal("node3", True)
    for _ in range(10):
        status, _, _ = C.write(PLAYER, 1, target="node3")
        assert status == 200
    observe("A) WAL 开: 写 10 分到 node3 (每条都 fsync 落盘)")
    inject("A) kill node3 -> start node3")
    score_a = restart_and_read()
    observe(f"A) 重启后 node3 score = {score_a} (WAL 重放恢复)")

    # B: WAL 关
    C.set_wal("node3", False)
    for _ in range(5):
        status, _, _ = C.write(PLAYER, 1, target="node3")
        assert status == 200
    observe("B) WAL 关: 再写 5 分到 node3 (只进内存,不落盘)")
    inject("B) kill node3 -> start node3")
    score_b = restart_and_read()
    observe(f"B) 重启后 node3 score = {score_b} (WAL 停在 10, 内存里的 5 丢了)")

    C.set_wal("node3", True)
    C.delete_rules_of_type("partition")
    # node3 缺的 5 分是刻意演示丢失的,不等收敛

    explain(
        "节点重启 = 内存清零。\n"
        "     A) WAL 在每次写前追加条目并 fsync,重启重放 -> 数据完整。\n"
        "     B) 关闭 WAL 后写只在内存,重启即丢 —— 对比展示了持久化边界。\n"
        "     重放利用 request_id 去重,天然幂等;最后一行写一半会因 JSON 解析\n"
        "     失败被截断,这是 WAL 的标准尾部处理。"
    )
    verdict(score_a == 10 and score_b == 10,
            f"A 恢复 {score_a}==10 完整; B 恢复 {score_b}==10 丢了关 WAL 后的 5 分")


if __name__ == "__main__":
    main()
