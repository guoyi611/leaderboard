"""Topic 7: 两个客户端同时执行 CAS。

CAS 语义: score(player)==expected 时追加 delta 条目。
三个场景(各用独立 player):
  1. 健康 + 都发 primary:      恰 1 个成功 (primary 单点串行检查)
  2. 分区 + local 模式:         两侧都成功 -> 愈合后 120 != 110, 违反线性一致
  3. 分区 + quorum 模式(W=2):   少数侧凑不齐法定人数 -> 恰 1 个成功
预测见各场景;解释:排行榜加分场景对 CAS 的线性性要求与代价。
"""
import time

from common import C, NODES, banner, explain, inject, observe, predict, verdict, \
    wait_converge


def primary_of(player: str) -> str:
    import hashlib
    nodes = sorted(NODES)
    return nodes[int(hashlib.md5(player.encode()).hexdigest(), 16) % len(nodes)]


def setup(player: str, base: int = 100) -> None:
    for _ in range(base):
        C.write(player, 1, target="node1")
    ok, _ = wait_converge(player, expect=base)
    assert ok, f"{player} 基础分未收敛"


def main() -> None:
    banner("Topic 7: 两个客户端同时执行 CAS")

    # ---- 场景 1: 健康, 都发 primary ----
    p1 = "cas-frank"
    setup(p1)
    primary = primary_of(p1)
    predict(f"[场景1] {p1} primary={primary}: 两个 CAS(expected=100,+10)并发发 primary,\n"
            "     恰 1 个成功 (100->110), 另一个 expected 不匹配失败")
    inject("两个客户端同时向 primary 发 CAS")
    r1a = C.cas(p1, 100, 10, target=primary, mode="local")
    r1b = C.cas(p1, 100, 10, target=primary, mode="local")
    wins = sum(r[1]["ok"] for r in (r1a, r1b))
    observe(f"结果: {r1a[1]['ok']} / {r1b[1]['ok']} (成功数 {wins}), "
            f"score = {C.score(p1, primary)[1]['score']}")
    s1_ok = wins == 1 and C.score(p1, primary)[1]["score"] == 110

    # ---- 场景 2: 分区, local 模式 (双主各自成功) ----
    p2 = "cas-grace"
    setup(p2)
    primary2 = primary_of(p2)
    other = next(n for n in NODES if n != primary2)
    # 分区: primary2 一侧, other+剩余节点一侧
    for a in NODES:
        if a != primary2:
            C.add_rule("partition", src=primary2, dst=a)
            C.add_rule("partition", src=a, dst=primary2)
    time.sleep(0.5)
    predict(f"[场景2] 分区({primary2} ∥ 其余): A 发 {primary2}, B 发 {other}(非 primary):\n"
            "     local 模式两侧各自检查旧值 100 都成功 -> 愈合后 120 != 110, 违反线性一致")
    inject("分区下两侧同时 CAS(local 模式)")
    r2a = C.cas(p2, 100, 10, target=primary2, mode="local", timeout=3.0)
    r2b = C.cas(p2, 100, 10, target=other, mode="local", timeout=3.0)
    wins2 = sum(r[1]["ok"] for r in (r2a, r2b) if r[1])
    observe(f"结果: 双方 ok = {r2a[1]['ok']} / {r2b[1]['ok']}, "
            f"{primary2} score = {C.score(p2, primary2)[1]['score']}, "
            f"{other} score = {C.score(p2, other)[1]['score']}")
    C.delete_rules_of_type("partition")
    time.sleep(3)  # 愈合收敛
    s2_score = {n: C.score(p2, n)[1]["score"] for n in NODES}
    observe(f"愈合后: {s2_score} (两侧 CAS 都生效, 120 != 110)")
    s2_ok = wins2 == 2 and all(v == 120 for v in s2_score.values())

    # ---- 场景 3: 分区, quorum 模式 (W=2) ----
    p3 = "cas-heidi"
    setup(p3)
    primary3 = primary_of(p3)
    other3 = next(n for n in NODES if n != primary3)
    for a in NODES:
        if a != primary3:
            C.add_rule("partition", src=primary3, dst=a)
            C.add_rule("partition", src=a, dst=primary3)
    time.sleep(0.5)
    predict(f"[场景3] 同样分区, quorum 模式(W=2): {primary3} 凑不齐 2 票 -> 失败;\n"
            "     另一侧自己+1 peer = 2 票 -> 成功。恰 1 成功, 终值 110")
    inject("分区下两侧同时 CAS(quorum 模式)")
    r3a = C.cas(p3, 100, 10, target=primary3, mode="quorum", timeout=8.0)
    r3b = C.cas(p3, 100, 10, target=other3, mode="quorum", timeout=8.0)
    wins3 = sum(r[1]["ok"] for r in (r3a, r3b) if r[1])
    C.delete_rules_of_type("partition")
    time.sleep(3)
    s3_score = {n: C.score(p3, n)[1]["score"] for n in NODES}
    observe(f"结果: 成功数 {wins3}, 愈合后 {s3_score}")
    s3_ok = wins3 == 1 and all(v == 110 for v in s3_score.values())

    explain(
        "CAS 的原子性来自『检查+插入』在单节点事件循环里串行执行。\n"
        "     场景1(健康): 两请求都到 primary, 顺序检查, 第二个必然看到 110 != 100。\n"
        "     场景2(分区+local): 失去全局串行点, 两侧都基于旧值 100 判断 -> 双成功。\n"
        "     这违反了单对象线性一致性 —— 换来的是分区期间两侧都可写(可用性)。\n"
        "     排行榜『加 10 分』本身可用条目集无损合并, 只有 CAS 语义受影响。\n"
        "     场景3(quorum): 提交需 W=2 节点确认, 少数侧拒绝提交,\n"
        "     恢复线性一致性的代价是分区期间少数侧 CAS 不可用(CAP 取舍)。"
    )
    verdict(s1_ok and s2_ok and s3_ok,
            f"场景1 恰1成功 {s1_ok}; 场景2 双成功120 {s2_ok}; 场景3 quorum恰1成功110 {s3_ok}")


if __name__ == "__main__":
    main()
