# Leaderboard: 最终一致性游戏排行榜

华南师范大学并行计算课程期末作业(场景 3:游戏排行榜)。
高写入量、可接受短暂读旧值、热点 key 场景下的多副本 KV/排行榜服务,
通过故障注入演示 9 个分布式故障 topic 下系统的行为与保证。

## 架构

```
                 +------------------+
   demos(client) |  net-proxy :9000 |  故障注入点: 延迟/乱序/重复/分区/吞响应
                 +--------+---------+
                          |  所有流量经 proxy 转发 (X-Target-Node)
        +-----------------+-----------------+
        |                 |                 |
   +----+----+       +----+----+       +----+----+
   | node1   | gossip | node2   | gossip | node3   |   条目集 CRDT + WAL + 静态 primary
   +---------+       +---------+       +---------+
```

**核心设计:写 = 不可变条目 `(request_id, player, delta, ts, node)`,score = Σ delta,
复制 = 周期 gossip 条目并集 merge(state-based CRDT)。**

由此一次性获得:幂等(重复消息/重试安全)、乱序无关(交换律)、
崩溃恢复(WAL 追加重放)、分区收敛(并集 = 两侧之和)、
任意副本可写(热点分片:写并行度 = 副本数)。

**流量路径**:演示与故障注入走 proxy(`:9000`,请求头 `X-Target-Node` 指定目标);
demo_06 的压测流量**直连**节点宿主机端口 `8101-8103`(proxy 是单线程实验装置,
不应成为吞吐瓶颈 —— 这本身是讲解点)。

## 快速开始

```bash
pip install -r requirements.txt   # 宿主机只需 httpx 跑 demo 脚本
./reset.sh                        # 构建+启动集群(重置 WAL 卷)
```

**可视化演示台**:浏览器打开 <http://localhost:9000/ui> ——
集群拓扑实时遥测(gossip 数据流粒子)、排行榜 Top10、故障注入控制台
(分区/延迟乱序/重复×3/吞响应/时钟倒退一键注入与愈合)。

```bash
cd demos
python demo_01_crash.py           # 依次运行 9 个演示(断言 PASS/FAIL)
```

重跑演示前先 `./reset.sh`(演示断言基于全新集群状态)。

## 9 个故障演示

| # | 文件 | topic | 核心断言 |
|---|------|-------|---------|
| 1 | demo_01_crash.py | 副本宕机 | 重启后 gossip 自动补齐,三副本收敛 |
| 2 | demo_02_partition_duplicate.py | 双向分区+消息重复×3 | 愈合后 score = 两侧之和,重复不多计 |
| 3 | demo_03_delay_reorder.py | 延迟 10s 乱序 | 窗口内读旧值(允许),最终与顺序无关 |
| 4 | demo_04_restart_memory_loss.py | 重启丢内存 | WAL 开=完整恢复,关=丢内存写 |
| 5 | demo_05_migration_crash.py | 迁移一半宕机 | 老集群不受影响,迁移幂等重入 |
| 6 | demo_06_hotkey.py | 热 key 占 50% 请求 | 任意副本写(分片)延迟 << primary 单点 |
| 7 | demo_07_concurrent_cas.py | 并发 CAS | 健康恰 1 成功;分区 local 双成功(违反线性一致);quorum 恢复 |
| 8 | demo_08_clock_skew.py | 时钟倒退 1 分钟 | LWW 丢更新(反例);条目集无损 |
| 9 | demo_09_lost_response.py | 磁盘写成功响应丢失 | 同 request_id 重试幂等,不多计 |

每个演示输出统一结构: `PREDICT -> INJECT -> OBSERVE -> EXPLAIN -> 断言`,
断言失败以非零码退出。

## 一致性语义(讲解口径)

- 最终一致性:分区/宕机期间各副本可分歧,愈合后有限时间内收敛
- 读:默认本地读(可短暂旧值);quorum 读(R=2)降低旧值概率,但不提供线性一致
- 写:任意副本,立即本地生效,异步复制
- CAS:primary 单点串行检查;local 模式分区下可能双成功(已知违反),
  quorum 模式(W=2)以分区期间少数侧不可用换回线性一致
- 时钟:正确性不依赖物理时钟(条目并集);LWW 寄存器仅作 topic 8 反例

## 目录结构

```
src/leaderboard/store.py    条目集 CRDT(纯函数核心)
src/leaderboard/node.py     节点: HTTP API + gossip + CAS + 迁移 + 时钟偏移
src/leaderboard/wal.py      预写日志(追加/fsync/重放)
proxy/net_proxy.py          可控网络代理(故障规则引擎)
client/client.py            客户端 SDK(request_id 幂等重试)
demos/                      9 个故障注入演示
```
