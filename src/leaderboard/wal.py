"""预写日志(Write-Ahead Log):条目追加 + 重放恢复。

设计:
- 每行一个 JSON:条目 {"t":"e",...} 或 LWW 更新 {"t":"lww",...}
- fsync 可开关(topic 4 对照演示:关 WAL/关 fsync 丢数据)
- 重放 = 逐行 apply 到 Store,天然幂等
"""
from __future__ import annotations

import json
import os
from typing import IO

from .store import Entry, Store


class Wal:
    def __init__(self, path: str, enabled: bool = True, fsync: bool = True) -> None:
        self.path = path
        self.enabled = enabled
        self.fsync = fsync
        self._file: IO | None = None

    def open(self) -> None:
        if self._file is None and self.enabled:
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            self._file = open(self.path, "a", encoding="utf-8")

    def append_entry(self, entry: Entry) -> None:
        self._write({"t": "e", "e": entry.to_dict()})

    def append_lww(self, player: str, value: str, ts: float) -> None:
        self._write({"t": "lww", "p": player, "v": value, "ts": ts})

    def _write(self, record: dict) -> None:
        if not self.enabled:
            return
        self.open()
        assert self._file is not None
        self._file.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._file.flush()
        if self.fsync:
            os.fsync(self._file.fileno())

    def replay(self, store: Store) -> int:
        """把 WAL 重放到 Store,返回恢复的条目数。文件不存在视为空日志。"""
        if not os.path.exists(self.path):
            return 0
        restored = 0
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    # 最后一行写一半崩溃:截断尾部,停止重放(经典 WAL 语义)
                    break
                if record.get("t") == "e":
                    if store.apply(Entry.from_dict(record["e"])):
                        restored += 1
                elif record.get("t") == "lww":
                    store.lww_merge(record["p"], record["v"], record["ts"])
        return restored

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None
