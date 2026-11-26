# Slide Deck Outline

**Topic**: 弄不坏的排行榜 —— 高写入场景下的最终一致性分布式 KV(游戏排行榜)
**Style**: blueprint
**Dimensions**: grid + cool + technical + balanced
**Audience**: general(大学课堂,非分布式背景可听懂)
**Language**: zh (中文正文,关键术语中英对照)
**Slide Count**: 17 slides
**Generated**: 2026-11-26 23:30

---

<STYLE_INSTRUCTIONS>
Design Aesthetic: Precise technical blueprint style. Clean, structured visual metaphors using engineering blueprints, schematics and diagrams. Technical grid overlay with engineering precision, cool analytical blues and grays, information presented in grid-based layouts with drafting-table exactness.

Background:
  Texture: Subtle engineering grid overlay on light paper
  Base Color: Blueprint Paper (#FAF8F5) with Light Gray grid lines (#E5E5E5)

Typography:
  Headlines: Bold, precise geometric sans-serif with consistent letter spacing, authoritative technical presence, Deep Slate color
  Body: Elegant readable serif with comfortable proportions, smaller sizes, editorial quality

Color Palette:
  Primary Text: Deep Slate (#334155) - headlines and body
  Background: Blueprint Paper (#FAF8F5) - primary background
  Accent 1: Engineering Blue (#2563EB) - key elements, highlights, dimension arrows
  Accent 2: Navy Blue (#1E3A5F) - supporting elements, secondary lines
  Fill: Light Blue (#BFDBFE) - diagram fills, section backgrounds
  Warning: Amber (#F59E0B) - fault/warning emphasis only

Visual Elements:
  - Technical schematics with thin consistent line weights
  - Connection lines: straight lines or 90-degree angles ONLY
  - Dimension lines with measurement indicators (arrows + ticks)
  - Isometric/orthographic projections of server racks and network boxes
  - Cross-section style diagrams showing internal data structures
  - Clean minimal charts (bar/line) with grid alignment
  - Stamped title blocks like real engineering drawings (bottom-right corner block with project name fields)

Density Guidelines:
  - Content per slide: one core idea + 3-4 supporting points maximum
  - Whitespace: generous, breathing room between zones
  - Element count: 4-8 elements per slide, strictly grid-aligned

Style Rules:
  Do: Maintain consistent line weights; use grid alignment for all elements; keep palette restrained; create hierarchy through scale; use geometric precision
  Don't: No hand-drawn or organic shapes; no decorative flourishes; no curved connection lines; no photographic elements; no slide numbers, footers, or logos
</STYLE_INSTRUCTIONS>

---

## Slide 1 of 17

**Type**: Cover
**Filename**: 01-slide-cover.png

// NARRATIVE GOAL
用工程蓝图的仪式感开启:这不是一份普通作业,而是一张经过验证的系统设计图纸。

// KEY CONTENT
Headline: 弄不坏的排行榜
Sub-headline: 高写入场景下的最终一致性分布式 KV · 并行计算期末作业(场景三:游戏排行榜)

// VISUAL
A large engineering blueprint cover sheet. Center: bold Chinese title "弄不坏的排行榜" in Deep Slate. Above it a thin dimension line with arrows measuring the title width. Background: subtle grid on paper white. Around the title, faint blueprint annotations: three small isometric server boxes connected by 90-degree orthogonal lines to a central network box, drawn in thin Engineering Blue linework. Bottom-right: a stamped engineering title block (表格框) with fields: 项目=分布式KV / 副本=3 / 故障测试=9/9 通过. Amber stamp mark "PASSED" rotated slightly, like an inspector's stamp.

// LAYOUT
Layout: title-hero
Title dominant in upper-center, schematic drawing occupying lower two-thirds, title block bottom-right.

---

## Slide 2 of 17

**Type**: Content
**Filename**: 02-slide-scene.png

// NARRATIVE GOAL
建立问题意识:游戏排行榜是存储系统里最难伺候的场景之一,三个特征同时出现。

// KEY CONTENT
Headline: 游戏排行榜:三重压力同时到来
Sub-headline: 看似简单的分数榜,实则是最苛刻的存储场景
Body:
- 写入量巨大:每次击杀、拾取都是一次加分,写入频率比订单类业务高一到两个数量级
- 允许读旧值:榜单晚几秒更新玩家无感知 —— 业务给了设计宽容度
- 热点集中:头部主播的单个账号可占全站 50% 的请求

// VISUAL
Three blueprint gauge panels side by side (triptych), each in a thin-bordered frame like instrument panels on a schematic: left panel shows a pressure gauge needle near maximum labeled "写入 QPS"; middle panel shows a clock with tolerance arc labeled "可容忍旧值"; right panel shows a pie chart 50/50 split with the hot half highlighted in Amber, labeled "热点 key 50%". All connected upward to one header line with 90-degree connectors.

// LAYOUT
Layout: triptych-cards
Headline top-left, three equal panels in a row across the middle, generous margins.

---

## Slide 3 of 17

**Type**: Content
**Filename**: 03-slide-why-replicas.png

// NARRATIVE GOAL
解释为什么必须多副本:单机两条死穴,多副本是唯一出路。

// KEY CONTENT
Headline: 单机的两条死穴
Sub-headline: 一台机器扛不住,也靠不住
Body:
- 写不动:磁盘与网络带宽有物理上限,热点 key 在单节点上串行排队
- 一挂全没:单点故障 = 全服榜单瞬间消失,而宕机不是意外,是必然
- 出路:加机器,数据存多份 —— 但新的难题随之而来

// VISUAL
Left half: blueprint cross-section of a single server rack with a red Amber "X" mark and two dimension annotations pointing to the disk and network ports, labeled with failure notes in Chinese. Right half: the same drawing replicated into three smaller racks connected by orthogonal lines, drawn in Engineering Blue, labeled "×3 副本". An arrow from left to right labeled "唯一的出路".

// LAYOUT
Layout: split-compare
Left panel (single, warning tones) vs right panel (triple, blue tones), headline across the top.

---

## Slide 4 of 17

**Type**: Content
**Filename**: 04-slide-three-laws.png

// NARRATIVE GOAL
引出分布式系统的三条物理定律,这是全部难题的来源。

// KEY CONTENT
Headline: 副本世界的三条物理定律
Sub-headline: 数据存到多台机器上,三件事必然发生
Body:
- 机器会挂:三台机器,一年内宕机几乎是必然事件
- 网络会坏:不只是断 —— 还会延迟、乱序、重复投递、丢失响应
- 时钟不可信:校时会让时间倒退,两台机器没有真正的"同一时刻"

// VISUAL
Three horizontal blueprint schematic rows, each a mini-diagram: row 1 shows a server icon with dashed outline and "宕机" label plus a small crack symbol; row 2 shows two servers connected by a signal line that splits into delayed/duplicated/crossed paths, each deviation marked with tiny Amber warning triangles; row 3 shows two clock faces showing different times with a curved(仅时钟指针可圆)backward arrow labeled "-60s". Rows separated by thin dimension lines.

// LAYOUT
Layout: stacked-rows
Headline top, three equal schematic rows below, left-side row labels in navy.

---

## Slide 5 of 17

**Type**: Content
**Filename**: 05-slide-cap-bet.png

// NARRATIVE GOAL
讲清 CAP 取舍:分区时必须在一致性和可用性之间二选一,我们的业务允许选可用性。

// KEY CONTENT
Headline: 我们的赌注:要可用,还是要一致?
Sub-headline: 分区发生时,鱼与熊掌不可兼得(CAP 定理)
Body:
- 选一致性(CP):分区期间拒绝部分写入 —— 银行余额的正确选择,但排行榜用它太奢侈
- 选可用性(AP)← 我们:分区期间两侧继续写入,代价是暂时不一致
- 业务已授权"可短暂读旧值",所以我们敢赌:分区愈合后自动收敛

// VISUAL
Blueprint balance-scale drawn in precise orthogonal linework at center: left pan holds a locked box labeled "C 一致性", right pan (lower, chosen, highlighted Engineering Blue fill) holds a lightning bolt labeled "A 可用性". Fulcrum labeled "分区". A handwritten-style(仅此一处手写感)check mark next to right pan. Dimension annotation under the scale: "只能压一头".

// LAYOUT
Layout: center-diagram
Headline top, central scale diagram, two annotation columns left/right.

---

## Slide 6 of 17

**Type**: Content
**Filename**: 06-slide-one-idea.png

// NARRATIVE GOAL
全场核心思想,必须一图听懂:不存"当前分数"这个数,存"加分事件的集合"。

// KEY CONTENT
Headline: 核心设计:不存分数,存事件
Sub-headline: 一个决定,化解九种故障
Body:
- 每次加分是一条不可变的记录:(唯一编号, 玩家, 加多少)
- 分数 = 把该玩家的所有记录加总
- 合并两台机器的数据 = 求并集(按唯一编号去重)
- 类比:不存文件的最新版本,存完整的 Git 提交历史

// VISUAL
Center: large blueprint cross-section diagram of a ledger vault: a rectangular box labeled "排行榜存储", its cutaway interior shows a stack of small identical cards (事件条目), each card with a tiny ID number; three cards highlighted in Light Blue fill. Below the vault, two dimension lines: "score = Σ 条目" and "merge = A ∪ B", drawn as measurement annotations with arrows. Two arrows from left and right replicas (small server icons) pointing into the vault, labeled "并集".

// LAYOUT
Layout: center-diagram
Big headline top, vault cross-section center, formula dimension lines bottom.

---

## Slide 7 of 17

**Type**: Content
**Filename**: 07-slide-nine-faults.png

// NARRATIVE GOAL
证明核心设计的威力:一张表格把九种故障全部"变无害"。

// KEY CONTENT
Headline: 一个数据结构,九个故障变无害
Sub-headline: 收敛性是数学性质,不是测试运气
Body (table, 9 rows):
- 副本宕机 → 落盘日志重放 + 自动补课
- 分区+重复投递 → 并集去重,投多少次都只算一次
- 延迟乱序 → 并集与顺序无关
- 重启丢内存 → 先写日志再确认
- 迁移一半宕机 → 记录不可变,迁移可重入
- 热点 key → 任意副本都能收写
- 并发 CAS → 已知会双成功,quorum 模式可修复
- 时钟倒退 → 合并根本不读时间戳
- 响应丢失 → 同编号重试,不会双计

// VISUAL
A clean blueprint inspection checklist table drawn like an engineering QA sign-off sheet: thin orthogonal grid lines, 9 rows, columns [故障现象 | 为什么无害 | 状态]. Status column shows 9 small green-blue check marks stamped in rows. Header row in Navy fill with white text. One row (并发 CAS) marked with a small Amber triangle instead of check, with footnote "已知的取舍". Title block in bottom-right corner as on real drawings.

// LAYOUT
Layout: table-full
Headline top-left, large checklist table filling the slide, generous row height.

---

## Slide 8 of 17

**Type**: Content
**Filename**: 08-slide-architecture.png

// NARRATIVE GOAL
给出系统总蓝图:三副本 + 可控网络代理 + 实时演示台。

// KEY CONTENT
Headline: 系统蓝图:三副本 + 可控网络
Sub-headline: 所有流量经过代理 —— 那是我们安插的"故障开关"
Body:
- 三个存储节点:各存一份完整数据,先写日志再确认
- 每秒互相推送数据(gossip),自动追平差异
- 网络代理:可按指令注入延迟、乱序、重复、分区、吞响应
- 可视化演示台:浏览器实时看到数据流动与故障效果

// VISUAL
Full engineering blueprint of the system in isometric projection: three server boxes (node1/2/3) arranged in triangle, each box drawn as transparent schematic showing a tiny stack of event cards inside; a central rectangular proxy box labeled "net-proxy 故障注入"; all inter-node lines routed through the proxy with strict 90-degree angles, each line labeled (延迟/重复/分区). A laptop icon on the far left connected to proxy labeled "演示台 :9000/ui". Dimension annotations: "副本 ×3", "全量推送 1s".

// LAYOUT
Layout: full-diagram
Headline top-left, large isometric blueprint center-right, legend column on left edge.

---

## Slide 9 of 17

**Type**: Content
**Filename**: 09-slide-protocol.png

// NARRATIVE GOAL
说明演示方法论:每个故障都走同一套四步流程,这是可复现的科学方法。

// KEY CONTENT
Headline: 每个故障,同一套四步审判
Sub-headline: 先预测,再动手,然后对照解释
Body:
- ① 预测:动手前先写下预期行为
- ② 注入:一键注入故障(或直接断电一台机器)
- ③ 观察:指着屏幕看真实结果
- ④ 解释:违反了哪条保证?还是仍然正确?为什么

// VISUAL
Blueprint flow diagram: four square stations connected left-to-right by arrows with 90-degree routing, each station a framed panel with a large Chinese numeral (①②③④) and a small schematic icon (crystal ball=预测, lightning bolt=注入, magnifier=观察, balance=解释). The fourth station framed with thicker Engineering Blue border + Amber corner accent, annotated "全场重点". Below the flow, a thin timeline line with tick marks like a measurement scale.

// LAYOUT
Layout: horizontal-flow
Headline top, four equal stations in one row, footnote annotation bottom.

---

## Slide 10 of 17

**Type**: Content
**Filename**: 10-slide-partition-demo.png

// NARRATIVE GOAL
第一个演示高光:分区期间两侧分歧,愈合后自动收敛,重复投递不多算。

// KEY CONTENT
Headline: 演示一:剪断网线,再自动愈合
Sub-headline: 预测 → 注入 → 观察 → 解释
Body:
- 注入:剪断 node1—node2 之间的一切消息(双向分区),并把每条消息复制三份投递
- 观察:分区期间两侧各写 10 分,互相看不见;愈合后三台机器自动一致 = 20
- 解释:重复投递零效果 —— 按唯一编号并集,投多少次都只算一次
- 断言输出:PASS · 三副本 score 全部 == 20

// VISUAL
Left: terminal window mock drawn in blueprint style (rectangular frame, monospace-style text lines rendered as clean glyphs) showing the demo run output with final line "[RESULT] PASS 三副本 score 全部 == 20" highlighted in Engineering Blue fill bar. Right: three-node triangle schematic with the node1—node2 edge drawn as severed (double slash break marks, Amber), small "×3" stamps on message packets; a small green check badge "自愈" near healed edge annotation.

// LAYOUT
Layout: split-code-diagram
Headline top, terminal mock on left 55%, schematic on right 45%.

---

## Slide 11 of 17

**Type**: Content
**Filename**: 11-slide-hotkey-demo.png

// NARRATIVE GOAL
第二个演示高光:热点 key 写入散到三台机器,延迟差整三倍,分数依然准确。

// KEY CONTENT
Headline: 演示二:热点玩家,三台机器一起记账
Sub-headline: 单点串行 142ms vs 三机并行 47ms
Body:
- 对照组:同一个玩家的所有写入都压到一台机器(锁+落盘串行)
- 实验组:同一批写入随机分散到三台 —— 因为任何副本都能收写
- 结果:热点写中位延迟 142.0ms vs 46.8ms,差 3.0 倍 = 副本数
- 两组最终分数完全一致(600 / 600),正确性不受影响

// VISUAL
Clean blueprint bar chart: two horizontal bars with dimension-line styling — top bar (Amber outline) length 3× of bottom bar (Engineering Blue fill), each ending with value labels 142.0ms / 46.8ms in measurement callouts. A dimension bracket between bar ends annotated "3.0× = 副本数并行度". Below: three small server icons with a single player icon fanning out arrows to all three (isometric), labeled "任意副本可写". Chart grid faintly behind.

// LAYOUT
Layout: chart-focus
Headline top, bar chart center occupying 50%, fan-out schematic bottom.

---

## Slide 12 of 17

**Type**: Content
**Filename**: 12-slide-cas-demo.png

// NARRATIVE GOAL
第三个演示高光(全场最有讲头):并发 CAS 在三种条件下三种结局,CAP 的现场交易。

// KEY CONTENT
Headline: 演示三:并发 CAS 的三次审判
Sub-headline: "分数等于 100 才加 10",两个客户端同时执行
Body:
- 健康 + 都发主节点:恰好一个成功 → 110(单点串行,看起来线性)
- 分区 + 本地模式:两个都成功 → 120 ≠ 110(违反线性一致 —— 我们主动演示!)
- 分区 + quorum 模式:恰好一个成功 → 110(要凑 2 票,少数侧自动拒绝)
- 结论:线性性可以买回来,代价是分区期间少数侧不可用 —— 这就是 CAP

// VISUAL
Blueprint tribunal triptych: three framed verdict panels left-to-right; panel 1 shows one green check + one gray cross under "健康 · local", verdict "110 ✓"; panel 2 shows two green checks under "分区 · local" with Amber warning border, verdict "120 ≠ 110"; panel 3 (thicker frame, navy fill header) shows one check + one rejected stamp under "分区 · quorum", verdict "110 ✓". Each panel bottom carries a small scale icon showing what was traded. Connective header line labeled "同一操作,三种条件".

// LAYOUT
Layout: triptych-cards
Headline top, three verdict panels in a row, conclusion strip along bottom in Light Blue fill.

---

## Slide 13 of 17

**Type**: Content
**Filename**: 13-slide-quorum.png

// NARRATIVE GOAL
理论第一讲:quorum 的鸽笼原理,数字不是调参而是推导。

// KEY CONTENT
Headline: quorum:鸽笼原理买到的保证
Sub-headline: N=3, 写 W=2, 读 R=2
Body:
- W + R = 4 > 3:任意"写够 2 台"与"读够 2 台"必有交集 —— 读至少碰到一台见过新数据的机器
- 我们的 quorum 读没做读修复,所以是"大幅降低旧值概率",不是绝对不读旧
- 把 W 从 2 改成 1:交集不再保证,"写成功了却读不到"变成合法行为

// VISUAL
Blueprint pigeonhole diagram: three server boxes in a row; a blue bracket spanning servers 1-2 labeled "写多数派 W=2" (one small card inserted into both 1 and 2); a navy bracket spanning servers 2-3 labeled "读多数派 R=2" (a magnifier over both); the overlap server 2 highlighted with Light Blue fill and a callout "必有交集". Equation annotation at top drawn as stamped characters: "W+R=4 > 3". A crossed-out variant below: W=1 bracket only over server 1, with Amber warning "无交集保证".

// LAYOUT
Layout: diagram-with-counterexample
Headline top, main pigeonhole diagram center, small counterexample strip bottom.

---

## Slide 14 of 17

**Type**: Content
**Filename**: 14-slide-concurrent-paths.png

// NARRATIVE GOAL
理论第二讲:面对并发写,系统只有三条路,我们的选择有数学依据。

// KEY CONTENT
Headline: 面对并发,只有三条路
Sub-headline: 两个操作互相看不见 = 并发(谁先谁后无法判定)
Body:
- 报错:共识协议拒绝其中一个 —— 分区期间少数侧不可写,对排行榜太奢侈
- 仲裁:比时间戳,新者胜 —— 会丢更新,而且时钟不可靠
- 都要:并集合并 ← 我们 —— 并发加分本来就都该保留,语义天然正确
- CAS 是"检查再写入",并发下没有安全的自动合并,所以它才需要 quorum

// VISUAL
Blueprint fork-in-road diagram: one incoming arrow labeled "两个并发写" splits via orthogonal junction into three framed paths; path 1 "报错" with a stop-sign symbol; path 2 "仲裁" with a balance icon where one card falls into a trash bin (丢更新, Amber mark); path 3 "都要" drawn with Engineering Blue emphasis, thicker border, showing two cards merging into a larger stack labeled "并集", stamped "我们的选择". Bottom footnote strip: 数据结构选型 = 提前写好并发的答案.

// LAYOUT
Layout: branching-diagram
Headline top, three-way fork center, footnote strip bottom.

---

## Slide 15 of 17

**Type**: Content
**Filename**: 15-slide-clock-limits.png

// NARRATIVE GOAL
理论第三讲 + 诚实的局限清单:时钟为什么不能当裁判,系统还有哪些没做好。

// KEY CONTENT
Headline: 时钟不能当裁判 · 局限如实交代
Sub-headline: 现场反例 + 改进方向
Body:
- 反例:把 node3 的时钟拨慢一分钟,再写入新值 —— 它的时间戳像"来自过去",会被旧值覆盖,更新无声丢失
- 对策:合并根本不读时间戳;因果交给逻辑时钟;物理钟只用于人看的日志
- 局限→改进:全量推送→差量检测;无读修复→读时补新;存储×3→冷热分层;简化两阶段→生产用共识协议;无认证→签名
- 前两项只影响收敛速度,不影响正确性

// VISUAL
Left half: blueprint clock diagram — two clock faces, left one normal, right one with hands rotated backward labeled "-60s", below them a mini timeline where a newer event card (v4) is overridden by older card (v3), the override marked with Amber "丢失" stamp. Right half: a to-improve checklist table in thin linework, rows [局限 | 改进] with small right-arrows between cells, footer note strip in Light Blue.

// LAYOUT
Layout: split-two-topics
Headline spanning top, clock diagram left 50%, checklist right 50%, footnote bottom.

---

## Slide 16 of 17

**Type**: Content
**Filename**: 16-slide-summary.png

// NARRATIVE GOAL
总结升华:把"当前值"换成"事件集合",九种故障变成同一条数学性质的九次复读。

// KEY CONTENT
Headline: 把"当前值"换成"事件集合"
Sub-headline: 九种故障,变成同一个数学性质的九次复读
Body:
- 机器会挂 → 落盘日志 + 自动补课,恢复不需要人
- 网络会坏 → 不可变记录 + 并集合并,延迟/乱序/重复全部失效
- 时钟不可信 → 正确性路径上没有物理时钟
- 设计阶段的一次正确性投资,在每个故障场景被反复兑现

// VISUAL
Blueprint master-key diagram: one large key (drawn in precise orthogonal linework, Engineering Blue) labeled "事件集合" turning in a central lock; from the lock, nine thin orthogonal lines fan out (3×3 grid routing) to nine small fault icons (server crash, broken link, delayed envelope ×3, restarted box, half-loaded truck, spotlight, crossed arrows, backward clock, lost reply) — each fault icon stamped with a small green check overlay. Equation strip at bottom: 幂等 + 交换 + 结合 ⇒ 收敛.

// LAYOUT
Layout: center-key-radial
Headline top, key-and-lock center, 3×3 fault grid around right side, formula strip bottom.

---

## Slide 17 of 17

**Type**: Back Cover
**Filename**: 17-slide-back-cover.png

// NARRATIVE GOAL
收尾不是"谢谢",而是把系统当作一张通过验收的图纸归档,邀请提问。

// KEY CONTENT
Headline: 图纸归档 · 恭候审查
Body:
- 全部代码与九个可复现演示:GitHub · docker compose up 一键启动
- 可视化演示台:localhost:9000/ui
- 汇报人:A(背景与架构) · B(故障演示) · C(理论与总结)

// VISUAL
Closing blueprint sheet mirroring the cover: the same title block now fully stamped — a large Amber inspection stamp "9/9 FAULTS PASSED" rotated slightly over the corner, the three-server schematic now showing all nodes with green status dots and flowing packet marks on orthogonal lines. Center headline in Deep Slate. Bottom-right title block fields filled in completely like a signed-off engineering drawing, with three signature lines labeled 汇报人 A / B / C.

// LAYOUT
Layout: closing-stamp
Centered headline, stamped schematic below, signature title block bottom-right.
