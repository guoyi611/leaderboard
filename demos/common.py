"""演示公共设施:输出格式、收敛等待、docker compose 控制。"""
from __future__ import annotations

import os
import subprocess
import sys
import time

# Windows 控制台默认 GBK,强制 UTF-8 输出中文
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "client"))

from client import LeaderboardClient  # noqa: E402

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NODES = ["node1", "node2", "node3"]
PROXY = "http://localhost:9000"

C = LeaderboardClient(PROXY)


def compose(*args: str) -> None:
    """docker compose 控制(固定 project 名,避免中文路径影响)。"""
    subprocess.run(["docker", "compose", "-p", "leaderboard", *args],
                   cwd=PROJECT_ROOT, check=True,
                   stdout=subprocess.DEVNULL)


def kill_node(node: str) -> None:
    compose("kill", node)


def start_node(node: str) -> None:
    compose("start", node)


def wait_up(node: str, timeout: float = 30.0) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            status, _ = C.stats(node)
            if status == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def wait_converge(player: str, nodes: list[str] | None = None, expect: int | None = None,
                  timeout: float = 30.0) -> tuple[bool, dict[str, int]]:
    """轮询直到各节点 score 一致(且等于 expect,若给定)。"""
    nodes = nodes or NODES
    t0 = time.time()
    scores: dict[str, int] = {}
    while time.time() - t0 < timeout:
        scores = {}
        alive = True
        for n in nodes:
            try:
                status, body = C.score(player, n)
                if status == 200:
                    scores[n] = body["score"]
                else:
                    alive = False
            except Exception:
                alive = False
        values = set(scores.values())
        if alive and len(values) == 1 and (expect is None or values == {expect}):
            return True, scores
        time.sleep(1.0)
    return False, scores


def banner(title: str) -> None:
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)


def predict(text: str) -> None:
    print(f"\n[PREDICT 预测] {text}")


def inject(text: str) -> None:
    print(f"[INJECT  注入] {text}")


def observe(text: str) -> None:
    print(f"[OBSERVE 观察] {text}")


def explain(text: str) -> None:
    print(f"[EXPLAIN 解释] {text}")


def verdict(ok: bool, text: str = "") -> None:
    print(f"\n[RESULT  断言] {'PASS' if ok else 'FAIL'} {text}")
    if not ok:
        sys.exit(1)
