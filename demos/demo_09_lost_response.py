"""Topic 9: 磁盘写成功,但响应在途中丢失。

流程: proxy 吞掉 node2 的写响应(drop_response) -> 客户端超时,
     以为失败;磁盘/WAL 上其实已写入。客户端用同一 request_id 重试:
     服务端识别重复请求,不重复计分,返回 duplicate=true。
预测:重试后客户端拿到确认;分数只加了一次(幂等)。
解释:at-least-once 网络 + 幂等服务端 = effectively-once;
     客户端生成的 request_id 是幂等键。
"""
from common import C, banner, explain, inject, observe, predict, verdict, wait_converge

PLAYER = "lost-kate"
RID = "retry-demo-rid-001"


def main() -> None:
    banner("Topic 9: 磁盘写成功, 但响应在途中丢失")

    predict(
        "proxy 吞掉 node2 的响应 -> 第一次写客户端超时(但 WAL 已落盘);\n"
        "     同一 request_id 重试 -> 服务端幂等去重, 返回 duplicate=true;\n"
        "     最终 score 恰好 +7, 不是 +14"
    )

    inject("proxy 规则: drop_response (client -> node2 响应被吞)")
    C.add_rule("drop_response", src="client", dst="node2")

    # 客户端短超时, 手动控制重试时序
    short = C._client.timeout
    C._client.timeout = 3.0
    status1, body1, _ = C.write(PLAYER, 7, target="node2", request_id=RID, retries=0)
    C._client.timeout = short
    observe(f"第一次写: status={status1} (客户端超时, 不知道服务端已写入)")

    # 服务端视角:数据已在(等 gossip 传播后从 node1 读,绕开被吞的响应路径)
    import time as _t
    _t.sleep(2.5)
    server_score = C.score(PLAYER, "node1")[1]["score"]
    observe(f"从 node1 读 {PLAYER}: score = {server_score} (写实际已生效, WAL 已落盘)")

    inject("清除规则, 客户端用同一 request_id 重试")
    C.delete_rules_of_type("drop_response")
    status2, body2, _ = C.write(PLAYER, 7, target="node2", request_id=RID, retries=1)
    observe(f"重试: status={status2}, duplicate={body2.get('duplicate') if body2 else '?'}, "
            f"score={body2.get('score') if body2 else '?'}")

    ok, scores = wait_converge(PLAYER, expect=7, timeout=15)
    observe(f"最终收敛: {scores}")

    explain(
        "写路径: 追加 WAL + fsync(磁盘成功) -> 返回响应(途中丢失)。\n"
        "     客户端视角这是一次超时,但数据已经持久化。\n"
        "     盲目重试会造成双计;客户端携带同一 request_id 重试,\n"
        "     服务端条目主键就是 request_id -> 并集自动去重,\n"
        "     响应还明确告知 duplicate=true。\n"
        "     at-least-once 传输 + 幂等写入 = effectively-once 语义。"
    )
    verdict(ok and all(v == 7 for v in scores.values())
            and body2 is not None and body2.get("duplicate") is True,
            f"score 恰为 7 (未双计): {scores}; 重试响应 duplicate=true")


if __name__ == "__main__":
    main()
