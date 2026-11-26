#!/usr/bin/env bash
# 重置演示环境:销毁集群(含 WAL 卷)并重新拉起,用于重复演示
set -e
cd "$(dirname "$0")"
docker compose -p leaderboard down -v --remove-orphans
docker compose -p leaderboard up -d --build
echo "waiting for nodes..."
for i in $(seq 1 60); do
  if curl -sf http://localhost:9000/stats -H "X-Target-Node: node1" >/dev/null 2>&1; then
    echo "cluster ready"
    exit 0
  fi
  sleep 1
done
echo "cluster not ready in 60s" >&2
exit 1
