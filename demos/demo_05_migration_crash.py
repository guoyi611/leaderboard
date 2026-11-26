"""Topic 5: 新节点在数据迁移到一半时宕机。

node4 以 migration 模式启动:从 node1 分页拉取全量条目(每批 sleep,
让"迁移到一半"可控)。中途 kill node4:
预测:迁移故障不影响老副本服务(迁移是新节点的故障域);
     node4 重启后从头重拉,幂等合并不多算,最终与老副本一致。
"""
import subprocess
import time

from common import C, PROJECT_ROOT, banner, explain, inject, observe, predict, verdict, \
    kill_node, start_node, wait_up

PLAYER = "migr-eve"


def compose(*args: str) -> None:
    subprocess.run(["docker", "compose", "-p", "leaderboard", *args],
                   cwd=PROJECT_ROOT, check=True, stdout=subprocess.DEVNULL)


def node4_stats() -> dict:
    return C.stats("node4")[1]


def main() -> None:
    banner("Topic 5: 新节点在数据迁移到一半时宕机")

    # 老集群写入足量数据(4 批以上)
    for i in range(400):
        status, _, _ = C.write(PLAYER, 1, target=f"node{(i % 3) + 1}")
        assert status == 200
    time.sleep(2.5)  # 等 gossip 收敛
    old_total = C.stats("node1")[1]["total"]
    observe(f"老集群写入 400 条, node1 total = {old_total}")

    predict(
        "node4 启动迁移(每批 100 条,批间 1s),2.5s 后(约 50%)kill node4:\n"
        "     期间向老节点写入仍 100% 成功;node4 重启后重拉,最终 total 与老副本相等"
    )

    inject("docker compose --profile migration up -d node4 (迁移模式启动)")
    compose("--profile", "migration", "up", "-d", "node4")
    assert wait_up("node4"), "node4 启动超时"

    time.sleep(2.5)  # 迁移进行到约一半
    mid = node4_stats()
    observe(f"迁移中: node4 已拉 {mid['migration']['entries_seen']} 条 "
            f"({mid['migration']['batches']} 批), 老集群 total = "
            f"{C.stats('node1')[1]['total']}")

    inject("迁移到一半: docker compose kill node4, 同时继续向老集群写入")
    kill_node("node4")
    writes_ok = 0
    for i in range(20):
        status, _, _ = C.write(PLAYER, 1, target=f"node{(i % 3) + 1}")
        writes_ok += status == 200
    observe(f"node4 宕机期间老集群写入 {writes_ok}/20 成功")

    inject("docker compose start node4 (重启, 从头重拉)")
    start_node("node4")
    assert wait_up("node4"), "node4 重启超时"

    # 等迁移完成 + gossip 追平
    for _ in range(60):
        st = node4_stats()
        if st["migration"]["done"] and st["total"] == C.stats("node1")[1]["total"]:
            break
        time.sleep(1.0)
    final4 = node4_stats()["total"]
    final1 = C.stats("node1")[1]["total"]
    observe(f"迁移完成: node4 total = {final4}, node1 total = {final1}")

    compose("stop", "node4")
    compose("rm", "-f", "node4")

    explain(
        "迁移 = 新节点从 seed 分页拉条目 + 追日志,是『新节点自己的事』:\n"
        "     它宕机不影响老副本读写(迁移的故障域隔离)。\n"
        "     重启后从头重拉,条目按 request_id 并集,重拉不多算 —— 迁移幂等。\n"
        "     最终 node4 通过 gossip 追上宕机期间的新写入,与老副本一致。"
    )
    verdict(writes_ok == 20 and final4 == final1 and final4 >= old_total + 20,
            f"期间写入 20/20 成功; 迁移后 node4({final4}) == node1({final1})")


if __name__ == "__main__":
    main()
