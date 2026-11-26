"""Topic 8: 系统时间突然倒退一分钟。

两条路径对照:
  A. LWW 寄存器(按物理时间戳决胜): node3 时钟倒退 60s 后写入 v4,
     其 ts 比之前 node1 写的 v3 小 60s -> v4 被"来自未来的旧值"压制,更新丢失!
  B. 条目集主路径(不看时间戳排序): node3 倒退后照常加分,无任何丢失。
预测:A 演示丢更新反例;B 完好。
解释:这就是"为什么不能只用物理时钟解决冲突"——
     我们的正确性来自 request_id 并集 + 因果收敛,与时钟无关。
"""
import time

from common import C, NODES, banner, explain, inject, observe, predict, verdict, \
    wait_converge

LWW_PLAYER = "lww-ivan"
CTR_PLAYER = "ctr-jack"


def main() -> None:
    banner("Topic 8: 系统时间突然倒退一分钟")

    predict(
        "A) LWW 寄存器: node1 写 v3 后, node3 时钟倒退 60s 再写 v4 ->\n"
        "     v4 的 ts 比 v3 早 60s, 合并后 v3 胜 -> v4 更新丢失(反例)\n"
        "B) 条目集主路径: node3 倒退后加分, 分数无损"
    )

    # ---- A: LWW 反例 ----
    inject("node3 时钟偏移 -=60s (系统时间倒退一分钟)")
    C.set_clock("node3", -60.0)
    clock = C.get_clock("node3")[1]
    observe(f"node3 逻辑时钟 now = {clock['now']:.1f} "
            f"(offset {clock['clock_offset']:.0f}s, 比真实时间慢 60s)")

    # node1(正常时钟)先写 v3,node3(倒退时钟)再写 v4 —— 更新的写是 v4
    C.lww_write(LWW_PLAYER, "v3", target="node1")
    time.sleep(0.3)
    accepted = C.lww_write(LWW_PLAYER, "v4", target="node3")[1]
    observe(f"node1 写 v3 (ts=正常); node3 写 v4 -> {accepted} "
            f"(node3 本地接受, 但 ts 倒退了 60s)")

    time.sleep(3.5)  # 等 gossip 合并
    lww_final = {}
    for n in NODES:
        v = C.lww_read(LWW_PLAYER, n)[1]["value"]
        lww_final[n] = v[0] if v else None
    observe(f"gossip 合并后各节点 LWW({LWW_PLAYER}): {lww_final}")

    # ---- B: 条目集对照 ----
    for _ in range(6):
        C.write(CTR_PLAYER, 1, target="node1")
    inject("node3 时钟仍倒退, 向 node3 加分 4 次(条目集主路径)")
    for _ in range(4):
        status, _, _ = C.write(CTR_PLAYER, 1, target="node3")
        assert status == 200
    ok, ctr_scores = wait_converge(CTR_PLAYER, expect=10, timeout=20)
    observe(f"条目集路径收敛: {ctr_scores}")

    C.set_clock("node3", +60.0)  # 恢复时钟

    explain(
        "LWW 用『物理时间戳大者胜』:时钟倒退让新写 v4 带上了 60s 前的旧时间戳,\n"
        "     合并时被时间戳更大的旧值 v3 压制 —— 更新无声丢失,且无法检测。\n"
        "     NTP 校时、闰秒、VM 挂起都会触发同类问题。\n"
        "     我们的排行榜主路径不依赖时间戳决胜:条目按 request_id 求并集,\n"
        "     每次写都必然生效(倒退时钟下 4 分照样收敛),时钟只作展示元数据。\n"
        "     这正是『为什么不能只用物理时钟解决冲突』的标准答案。"
    )
    verdict(lww_final == {"node1": "v3", "node2": "v3", "node3": "v3"}
            and ok and all(v == 10 for v in ctr_scores.values()),
            f"LWW 丢更新反例成立(v4 丢失, 终值 v3); 条目集无损收敛 10: {ctr_scores}")


if __name__ == "__main__":
    main()
