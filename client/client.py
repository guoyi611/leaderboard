"""排行榜客户端 SDK:所有流量经 proxy,写请求自带 request_id 幂等重试。"""
from __future__ import annotations

import time
import uuid

import httpx


class LeaderboardClient:
    def __init__(self, proxy_url: str = "http://localhost:9000", source: str = "client",
                 timeout: float = 5.0, node_urls: dict[str, str] | None = None):
        """
        proxy_url: 经可控代理访问(默认,支持故障注入)
        node_urls: 直连模式 {"node1": "http://host:port"} —— 绕过 proxy,
                   用于压测(proxy 是单线程实验装置,不应成为吞吐瓶颈)
        """
        self.proxy = proxy_url.rstrip("/") if proxy_url else ""
        self.node_urls = node_urls or {}
        self.source = source
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def _headers(self, target: str) -> dict:
        return {"X-Source-Node": self.source, "X-Target-Node": target}

    def _base(self, target: str) -> str:
        if target in self.node_urls:
            return self.node_urls[target]
        return self.proxy

    def _call(self, method: str, path: str, target: str, json_body: dict | None = None):
        url = f"{self._base(target)}{path}"
        if method == "GET":
            r = self._client.get(url, headers=self._headers(target))
        else:
            r = self._client.post(url, json=json_body, headers=self._headers(target))
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, None

    # ---------------- 数据面 ----------------

    def write(self, player: str, delta: int, target: str, request_id: str | None = None,
              retries: int = 3) -> tuple[int, dict | None, float]:
        """加分写。超时自动用同一 request_id 重试(服务端幂等,至多生效一次)。"""
        rid = request_id or str(uuid.uuid4())
        last_exc_status = None
        for attempt in range(retries + 1):
            t0 = time.perf_counter()
            try:
                status, body = self._call("POST", "/write", target,
                                          {"player": player, "delta": delta, "request_id": rid})
                if status == 200:
                    return status, body, (time.perf_counter() - t0) * 1000
                last_exc_status = status
            except (httpx.TimeoutException, httpx.TransportError):
                last_exc_status = -1
                continue
        return last_exc_status, None, -1.0

    def cas(self, player: str, expected: int, delta: int, target: str,
            request_id: str | None = None, mode: str = "local",
            timeout: float | None = None, retries: int = 0):
        rid = request_id or str(uuid.uuid4())
        old_timeout = self._client.timeout
        if timeout:
            self._client.timeout = timeout
        try:
            status, body = self._call("POST", "/cas", target,
                                      {"player": player, "expected": expected, "delta": delta,
                                       "request_id": rid, "mode": mode})
        finally:
            self._client.timeout = old_timeout
        return status, body

    def score(self, player: str, target: str, mode: str = "local"):
        return self._call("GET", f"/score/{player}?mode={mode}", target)

    def top(self, n: int, target: str):
        return self._call("GET", f"/top/{n}", target)

    def lww_write(self, player: str, value: str, target: str):
        return self._call("POST", f"/lww/{player}", target, {"value": value})

    def lww_read(self, player: str, target: str):
        return self._call("GET", f"/lww/{player}", target)

    def stats(self, target: str):
        return self._call("GET", "/stats", target)

    # ---------------- 演示控制面 ----------------

    def set_clock(self, target: str, offset_delta: float):
        return self._call("POST", "/admin/clock", target, {"offset_delta": offset_delta})

    def get_clock(self, target: str):
        return self._call("GET", "/admin/clock", target)

    def set_wal(self, target: str, enabled: bool):
        return self._call("POST", "/admin/wal", target, {"enabled": enabled})

    def set_slow(self, target: str, enabled: bool, slow_ms: float | None = None):
        body = {"enabled": enabled}
        if slow_ms is not None:
            body["slow_ms"] = slow_ms
        return self._call("POST", "/admin/slow", target, body)

    # ---------------- proxy 规则 ----------------

    def add_rule(self, rule_type: str, src="*", dst="*", **params):
        body = {"type": rule_type, "src": src, "dst": dst, **params}
        r = self._client.post(f"{self.proxy}/rules", json=body)
        return r.json()

    @staticmethod
    def probe_direct(nodes: tuple = ("node1", "node2", "node3"),
                     prefixes: tuple = ("http://localhost:810", "http://localhost:800")) \
            -> dict[str, str]:
        """探测直连地址:docker 端口映射(8101..)或本地 dev 模式(8001..)。"""
        for prefix in prefixes:
            urls = {n: f"{prefix}{i + 1}" for i, n in enumerate(nodes)}
            try:
                r = httpx.get(f"{urls[nodes[0]]}/stats", timeout=2.0,
                              headers={"X-Target-Node": nodes[0]})
                if r.status_code == 200:
                    return urls
            except Exception:
                continue
        return {}

    def list_rules(self) -> list[dict]:
        return self._client.get(f"{self.proxy}/rules").json()["rules"]

    def delete_rule(self, rule_id: int):
        self._client.delete(f"{self.proxy}/rules/{rule_id}")

    def delete_rules_of_type(self, rule_type: str) -> int:
        removed = 0
        for r in self.list_rules():
            if r["type"] == rule_type:
                self.delete_rule(r["id"])
                removed += 1
        return removed

    def clear_rules(self):
        self._client.delete(f"{self.proxy}/rules")
