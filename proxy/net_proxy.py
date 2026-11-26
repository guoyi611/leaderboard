"""可控网络代理:所有节点间/客户端->节点流量都经此转发,故障注入点。

工作方式:
- 请求头 X-Target-Node 指定目标节点,转发到 http://{target}:8000{path}
- 请求头 X-Source-Node 标识来源(节点名或 client),用于规则匹配
- 规则引擎(REST 控制):
    delay       延迟 N 秒转发;shuffle=True 时每条消息随机延迟 0~N 秒(乱序)
    duplicate   每条消息重复转发 times 次(topic 2:消息重复发送三次)
    partition   双向黑洞:命中即挂起(topic 2:网络分区)
    drop_response 转发成功但吞掉响应,客户端超时(topic 9:响应在途中丢失)
- src/dst 支持 "*" 通配;规则按添加顺序,第一条命中生效
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import time

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

NODE_PORT = 8000
BLACK_HOLE_SECONDS = 3600  # 分区黑洞:挂到客户端超时为止

# 本地开发模式: PROXY_NODE_URLS='{"node1":"http://localhost:8001",...}'
# docker 模式下为空,直接用 http://{target}:8000
NODE_URLS = json.loads(os.environ.get("PROXY_NODE_URLS", "{}"))


def node_url(target: str) -> str:
    return NODE_URLS.get(target, f"http://{target}:{NODE_PORT}")


# 共享连接池:避免每请求新建 TCP 连接的握手开销(否则 proxy 成为吞吐瓶颈)
shared_client = httpx.AsyncClient(timeout=30.0)

app = FastAPI(title="net-proxy")

rules: list[dict] = []
_next_id = 1


class RuleReq(BaseModel):
    type: str  # delay | duplicate | partition | drop_response
    src: str = "*"  # X-Source-Node 或 "*"
    dst: str = "*"  # X-Target-Node 或 "*"
    seconds: float = 0.0  # delay 用
    shuffle: bool = False  # delay 用:随机 0~seconds
    times: int = 3  # duplicate 用


def _match(value: str, pattern: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith("*"):
        return value.startswith(pattern[:-1])
    return value == pattern


def _matches(rule: dict, src: str, dst: str) -> bool:
    return _match(src, rule["src"]) and _match(dst, rule["dst"])


def _first_match(src: str, dst: str) -> dict | None:
    for rule in rules:
        if _matches(rule, src, dst):
            return rule
    return None


async def _forward(request: Request, target: str):
    body = await request.body()
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in ("host", "content-length")}
    url = f"{node_url(target)}{request.url.path}"
    if request.url.query:
        url += f"?{request.url.query}"
    return await shared_client.request(request.method, url, content=body,
                                       headers=headers)


# ---------------- 控制面(不转发) ----------------

@app.get("/ui")
async def ui():
    """可视化演示面板(纯静态单页,浏览器直接访问 :9000/ui)。"""
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))


@app.post("/rules")
async def add_rule(req: RuleReq):
    global _next_id
    rule = {"id": _next_id, **req.model_dump(), "created": time.time()}
    _next_id += 1
    rules.append(rule)
    return rule


@app.get("/rules")
async def list_rules():
    return {"rules": rules}


@app.delete("/rules")
async def clear_rules():
    rules.clear()
    return {"cleared": True}


@app.delete("/rules/{rule_id}")
async def delete_rule(rule_id: int):
    before = len(rules)
    rules[:] = [r for r in rules if r["id"] != rule_id]
    return {"deleted": len(rules) < before}


@app.get("/health")
async def proxy_health():
    return {"status": "up", "active_rules": len(rules)}


# ---------------- 数据面(转发 + 故障注入) ----------------

async def _proxy(request: Request):
    src = request.headers.get("X-Source-Node", "client")
    target = request.headers.get("X-Target-Node")
    if not target:
        return JSONResponse({"error": "missing X-Target-Node header"}, status_code=400)

    rule = _first_match(src, target)
    if rule is None:
        r = await _forward(request, target)
        return JSONResponse(r.json() if r.content else None, status_code=r.status_code)

    if rule["type"] == "partition":
        # 双向分区:直接黑洞挂起,调用方超时
        await asyncio.sleep(BLACK_HOLE_SECONDS)
        return JSONResponse({"error": "unreachable"}, status_code=504)

    if rule["type"] == "delay":
        if rule["shuffle"]:
            await asyncio.sleep(random.uniform(0, rule["seconds"]))
        else:
            await asyncio.sleep(rule["seconds"])
        r = await _forward(request, target)
        return JSONResponse(r.json() if r.content else None, status_code=r.status_code)

    if rule["type"] == "duplicate":
        times = max(1, rule["times"])
        first = None
        for _ in range(times):
            r = await _forward(request, target)  # 每份都真实送达目标
            if first is None:
                first = r
        return JSONResponse(first.json() if first.content else None, status_code=first.status_code)

    if rule["type"] == "drop_response":
        # 服务端正常处理(写已落盘),但响应被吞,客户端只能超时重试
        asyncio.create_task(_forward_and_drop(request, target))
        await asyncio.sleep(BLACK_HOLE_SECONDS)
        return JSONResponse({"error": "timeout"}, status_code=504)

    r = await _forward(request, target)
    return JSONResponse(r.json() if r.content else None, status_code=r.status_code)


async def _forward_and_drop(request: Request, target: str):
    try:
        await _forward(request, target)
    except Exception:
        pass


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path: str, request: Request):
    return await _proxy(request)
