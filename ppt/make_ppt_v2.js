/* leaderboard deck v2 — structured deck per official pptx skill
 * theme first -> layouts (defineSlideMaster) -> placeholders -> sections
 * run: node make_ppt_v2.js  -> deck-v2.pptx, then apply_theme + validate */
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("../../.claude/skills/pptx/scripts/apply_theme.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5

// ---------------- THEME (Mission Control, matches the live dashboard) ----------------
const THEME = {
  name: "MissionControl",
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  colors: {
    dk1: "CFE0F5",  // text1  主文字(浅)
    lt1: "070B14",  // bg1    背景(深蓝黑)
    dk2: "7DD3FC",  // text2  次文字(冰蓝)
    lt2: "0D1420",  // bg2    面板底
    accent1: "35E08A", // 磷光绿
    accent2: "FFB340", // 琥珀
    accent3: "FF4D5E", // 告警红
    accent4: "7DD3FC", // 冰蓝
    accent5: "96A8C0", // dim
    accent6: "1D7A4F", // 深绿
    hlink: "35E08A",
    folHlink: "FFB340",
  },
};
const C = pres.SchemeColor;
const MONO = "Consolas";
const VOID = "070B14", PANEL = "0D1420", PANEL2 = "101A2B", LINE = "26374F";
const GREEN = "35E08A", AMBER = "FFB340", RED = "FF4D5E", ICE = "7DD3FC", DIM = "96A8C0";

// ---------------- layouts ----------------

// cover
pres.defineSlideMaster({ title: "COVER", background: { color: VOID }, objects: [
  { text: { text: "SOUTH CHINA NORMAL UNIVERSITY · PARALLEL COMPUTING", options: {
    placeholder: "eyebrow", x: 0.9, y: 1.5, w: 11.5, h: 0.4, fontSize: 12,
    color: GREEN, fontFace: MONO, charSpacing: 4, isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "title", x: 0.9, y: 2.2, w: 11.5, h: 1.6,
    fontSize: 52, bold: true, color: "CFE0F5", isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "subtitle", x: 0.9, y: 3.95, w: 11.5, h: 0.6,
    fontSize: 18, color: ICE, isTextBox: true, margin: 0 } } },
]});

// section divider
pres.defineSlideMaster({ title: "SECTION", background: { color: VOID }, objects: [
  { text: { text: "", options: { placeholder: "secno", x: 0.9, y: 2.0, w: 2.2, h: 1.8,
    fontSize: 96, bold: true, color: "16221E", fontFace: MONO, isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "secname", x: 1.1, y: 3.1, w: 11, h: 1.0,
    fontSize: 40, bold: true, color: "CFE0F5", isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "secsub", x: 1.13, y: 4.15, w: 10, h: 0.6,
    fontSize: 15, color: DIM, fontFace: MONO, isTextBox: true, margin: 0 } } },
  { rect: { x: 1.13, y: 4.85, w: 1.2, h: 0.045, fill: { color: GREEN } } },
]});

// content: title + eyebrow + speaker + footer
pres.defineSlideMaster({ title: "CONTENT", background: { color: VOID }, objects: [
  { text: { text: "", options: { placeholder: "eyebrow", x: 0.55, y: 0.34, w: 9, h: 0.35,
    fontSize: 11, color: GREEN, fontFace: MONO, charSpacing: 3, isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "title", x: 0.55, y: 0.68, w: 11.5, h: 0.85,
    fontSize: 30, bold: true, color: "CFE0F5", isTextBox: true, margin: 0 } } },
  { text: { text: "", options: { placeholder: "speaker", x: 11.05, y: 0.36, w: 1.8, h: 0.3,
    fontSize: 10, color: DIM, fontFace: MONO, align: "right", isTextBox: true, margin: 0 } } },
  { rect: { x: 0, y: 7.14, w: 13.33, h: 0.36, fill: { color: "0A111E" } } },
  { text: { text: "弄不坏的排行榜 · 并行计算期末作业", options: {
    x: 0.55, y: 7.17, w: 6, h: 0.3, fontSize: 9, color: DIM,
    fontFace: MONO, isTextBox: true, margin: 0 } } },
] });

// statement: big centered quote
pres.defineSlideMaster({ title: "STATEMENT", background: { color: "0A0F1C" }, objects: [
  { text: { text: "", options: { placeholder: "quote", x: 1.2, y: 2.3, w: 10.9, h: 2.6,
    fontSize: 34, bold: true, color: GREEN, align: "center", valign: "middle",
    isTextBox: true, margin: 0, lineSpacingMultiple: 1.35 } } },
  { text: { text: "", options: { placeholder: "sub", x: 1.2, y: 5.15, w: 10.9, h: 0.6,
    fontSize: 15, color: DIM, align: "center", fontFace: MONO, isTextBox: true, margin: 0 } } },
]});

// ---------------- helpers ----------------
const S = { A: "李祈衡", B: "陈俊安", C: "张世朗" };

function content(eyebrow, title, speaker) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText(eyebrow, { placeholder: "eyebrow" });
  s.addText(title, { placeholder: "title" });
  s.addText(speaker, { placeholder: "speaker" });
  return s;
}
function section(no, name, sub) {
  const s = pres.addSlide({ masterName: "SECTION" });
  s.addText(no, { placeholder: "secno" });
  s.addText(name, { placeholder: "secname" });
  s.addText(sub, { placeholder: "secsub" });
  return s;
}
function card(s, x, y, w, h, head, body, accent) {
  s.addText(head, { x: x + 0.28, y: y + 0.24, w: w - 0.5, h: 0.5, fontSize: 19,
    bold: true, color: accent, isTextBox: true, margin: 0 });
  s.addText(body.map(t => ({ text: t, options: { breakLine: true, bullet: false } })),
    { x: x + 0.28, y: y + 0.82, w: w - 0.5, h: h - 1.0, fontSize: 13.5,
      color: "CFE0F5", isTextBox: true, margin: 0, lineSpacingMultiple: 1.35 });
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08,
    fill: { color: PANEL }, line: { color: accent, width: 0.75 } });
}
function bullets(s, x, y, w, items, opt = {}) {
  s.addText(items.map((t, i) => ({
    text: t, options: { breakLine: true, bullet: { characterCode: "2022", indent: 14 },
      color: opt.color || "CFE0F5", paraSpaceAfter: opt.gap || 10 } })),
    { x, y, w, h: opt.h || 1.2, fontSize: opt.size || 15, isTextBox: true, margin: 0,
      fontFace: "Microsoft YaHei", valign: "top" });
}
function term(s, x, y, w, h, lines, opt = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06,
    fill: { color: "0A111E" }, line: { color: LINE, width: 1 } });
  s.addText(lines.map(t => ({ text: t, options: { breakLine: true } })),
    { x: x + 0.35, y: y + 0.22, w: w - 0.7, h: h - 0.44, fontSize: opt.size || 13,
      color: opt.color || GREEN, fontFace: MONO, isTextBox: true, margin: 0,
      lineSpacingMultiple: 1.45 });
}
function mkTable(s, x, y, w, rows, opt = {}) {
  const header = rows[0].map(t => ({
    text: t, options: { color: ICE, bold: true, fontSize: (opt.size || 13) - 1,
      fill: { color: PANEL2 } } }));
  const body = rows.slice(1).map((r, ri) => r.map(cell => ({
    text: cell, options: { color: "CFE0F5", fontSize: opt.size || 13,
      fill: { color: ri % 2 ? "0A111E" : PANEL } } })));
  s.addTable([header, ...body], { x, y, w, colW: opt.colW,
    border: { type: "solid", color: LINE, pt: 1 }, rowH: opt.rowH || 0.42,
    margin: 0.06, valign: "middle", fontFace: "Microsoft YaHei" });
}

// ================= DECK =================

pres.addSection({ title: "0 封面" });

// ---- 1 cover ----
let s = pres.addSlide({ masterName: "COVER", sectionTitle: "0 封面" });
s.addText("SOUTH CHINA NORMAL UNIVERSITY · PARALLEL COMPUTING", { placeholder: "eyebrow" });
s.addText("弄不坏的排行榜", { placeholder: "title" });
s.addText("高写入场景下的最终一致性分布式 KV · 场景三(游戏排行榜)", { placeholder: "subtitle" });
s.addShape(pres.ShapeType.rect, { x: 0.93, y: 4.75, w: 1.4, h: 0.05, fill: { color: GREEN } });
s.addText([
  { text: "条目集 CRDT · 异步复制 · 热点分片", options: { breakLine: true } },
  { text: "九类故障注入全覆盖 · Docker 一键复现 · 可视化演示台", options: {} },
], { x: 0.9, y: 5.0, w: 8, h: 0.9, fontSize: 15, color: DIM, isTextBox: true,
  margin: 0, lineSpacingMultiple: 1.5 });
s.addText("汇报人:李祈衡(背景与架构) · 陈俊安(故障演示) · 张世朗(理论与总结)      2026-12",
  { x: 0.9, y: 6.35, w: 11, h: 0.4, fontSize: 13, color: DIM, isTextBox: true, margin: 0 });

// ================= SECTION A =================
pres.addSection({ title: "1 背景与设计 · SPEAKER A" });
section("01", "背景与设计", "难题从哪来 · CAP 赌注 · 一个数据结构");

// ---- 3 场景 ----
s = content("THE SCENE · 01", "游戏排行榜:存储里最难伺候的场景", S.A);
card(s, 0.55, 1.95, 3.95, 2.7, "写入量巨大",
  ["每杀怪 / 每捡金币都是加分", "QPS 高出订单类业务", "一到两个数量级"], GREEN);
card(s, 4.7, 1.95, 3.95, 2.7, "可容忍旧值",
  ["榜单晚几秒更新,无投诉", "业务授予的宽容额度", "= 设计空间"], ICE);
card(s, 8.85, 1.95, 3.95, 2.7, "热点集中",
  ["头部主播单 key", "可占 50% 以上请求", "一个 key 打穿单节点"], AMBER);
s.addText("既要吞下高写入和热点,又被允许短暂不一致 —— 这张\"优惠券\"怎么花,就是我们的设计。",
  { x: 0.55, y: 5.15, w: 12.2, h: 0.7, fontSize: 16, color: DIM, isTextBox: true, margin: 0 });

// ---- 4 单机死穴 → 三难 ----
s = content("WHY DISTRIBUTED · 02", "难题从哪来:单机死穴,副本三难", S.A);
card(s, 0.55, 1.9, 5.9, 1.75, "死穴一:写不动",
  ["磁盘与网络带宽有物理上限", "热点 key 在单节点串行排队"], RED);
card(s, 6.85, 1.9, 5.9, 1.75, "死穴二:一挂全没",
  ["单点故障 = 全服榜单消失", "宕机不是意外,是常态"], RED);
s.addText("加机器、多副本 —— 但数据一旦分布在多台机器,三条物理定律自动生效:",
  { x: 0.55, y: 3.95, w: 12.2, h: 0.5, fontSize: 16, bold: true, color: GREEN,
    isTextBox: true, margin: 0 });
bullets(s, 0.8, 4.55, 11.9, [
  "机器会挂 —— 三台机器,一年内宕机几乎是必然事件",
  "网络会坏 —— 不只断,还会延迟 10s、乱序、重复投递三次、丢响应",
  "时钟不可信 —— NTP 校时会跳会倒退,两台机器没有\"同一时刻\"",
], { size: 15, gap: 9, h: 1.9 });

// ---- 5 CAP ----
s = content("THE BET · 03", "我们的赌注:AP + 最终一致性", S.A);
card(s, 0.55, 1.95, 6.0, 3.1, "C 一致性 (CP)",
  ["分区时少数派拒绝写入", "银行余额的正确选择", "排行榜用它是浪费:", "分区期间全服不能加分"], DIM);
card(s, 6.8, 1.95, 6.0, 3.1, "A 可用性 (AP) ← 我们",
  ["分区时两侧都继续写", "代价:暂时不一致", "业务已授权\"可短暂读旧值\"", "换来:写入永不拒绝"], GREEN);
s.addText([
  { text: "承诺降级为:分区愈合后,有限时间内三副本自动收敛 —— \"最终\"一致。", options: { breakLine: true, bold: true, color: "CFE0F5" } },
  { text: "这句话,是后面九个演示唯一要证明的事。", options: { color: AMBER } },
], { x: 0.55, y: 5.4, w: 12.2, h: 1.0, fontSize: 16, isTextBox: true, margin: 0,
  lineSpacingMultiple: 1.5 });

// ---- 6 statement ----
s = pres.addSlide({ masterName: "STATEMENT", sectionTitle: "1 背景与设计 · SPEAKER A" });
s.addText("不给玩家存\"当前分数\"\n存加分事件的不可变集合", { placeholder: "quote" });
s.addText("score = Σ entries     merge = A ∪ B  (by request_id)", { placeholder: "sub" });

// ---- 7 一表九故障 ----
s = content("ONE MECHANISM · 04", "一个数据结构,九个故障变无害", S.A);
mkTable(s, 0.55, 1.85, 12.2, [
  ["故障 topic", "攻击点", "为什么无害"],
  ["副本宕机", "丢副本", "WAL 重放 + gossip 反熵自动补课"],
  ["分区 + 重复×3", "复制协议", "并集幂等,重复与顺序都算不错"],
  ["延迟 10s 乱序", "复制协议", "交换律:先到后到结果一样"],
  ["重启丢内存", "持久化", "条目先追加 WAL 再确认"],
  ["迁移一半宕机", "扩容", "条目不可变 → 迁移幂等可重入"],
  ["热点 key 50%", "吞吐", "任意副本可写,并行度 = 3"],
  ["并发 CAS", "线性性", "local 双成功(已知违反) / quorum 恰一成功"],
  ["时钟倒退", "定序", "主路径合并不读时间戳"],
  ["响应丢失", "确认语义", "request_id 幂等重试,不双计"],
], { colW: [2.6, 2.2, 7.4], size: 12.5, rowH: 0.44 });
s.addText("学术名字:CRDT(grow-only set 变体) · 收敛条件:幂等 + 交换 + 结合 —— 数学保证,不是测试经验",
  { x: 0.55, y: 6.6, w: 12.2, h: 0.4, fontSize: 13, color: DIM, isTextBox: true, margin: 0 });

// ---- 8 架构 ----
s = content("ARCHITECTURE · 05", "系统架构:三副本 + 可控网络", S.A);
const nodePos = [[1.7, 2.3], [1.7, 4.4], [4.0, 3.35]];
nodePos.forEach(([nx, ny], i) => {
  s.addShape(pres.ShapeType.ellipse, { x: nx, y: ny, w: 1.55, h: 1.55,
    fill: { color: PANEL }, line: { color: GREEN, width: 2 } });
  s.addText(`node${i + 1}`, { x: nx, y: ny + 0.42, w: 1.55, h: 0.4, fontSize: 15, bold: true,
    color: "CFE0F5", align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
  s.addText("条目集+WAL", { x: nx, y: ny + 0.82, w: 1.55, h: 0.3, fontSize: 9.5,
    color: DIM, align: "center", isTextBox: true, margin: 0 });
});
s.addShape(pres.ShapeType.roundRect, { x: 8.6, y: 3.0, w: 3.6, h: 1.3, rectRadius: 0.1,
  fill: { color: PANEL }, line: { color: ICE, width: 1.5 } });
s.addText("net-proxy", { x: 8.6, y: 3.18, w: 3.6, h: 0.45, fontSize: 16, bold: true,
  color: ICE, align: "center", fontFace: MONO, isTextBox: true, margin: 0 });
s.addText("延迟 / 乱序 / 重复 / 分区 / 吞响应", { x: 8.6, y: 3.66, w: 3.6, h: 0.35,
  fontSize: 10.5, color: DIM, align: "center", isTextBox: true, margin: 0 });
nodePos.forEach(([nx, ny]) => {
  s.addShape(pres.ShapeType.line, { x: nx + 1.55, y: ny + 0.77, w: 8.6 - nx - 1.55, h: 3.65 - ny,
    line: { color: LINE, width: 1.5 } });
});
s.addText("gossip 1s 全量推送(异步复制)", { x: 1.7, y: 6.1, w: 4.5, h: 0.35, fontSize: 11.5,
  color: GREEN, fontFace: MONO, isTextBox: true, margin: 0 });
bullets(s, 8.6, 1.95, 4.2, [
  "Docker 4 容器一键起",
  "读:本地(快) / quorum R=2",
  "CAS:primary / quorum W=2",
  "压测直连,proxy 只做注入",
], { size: 12.5, gap: 7, h: 1.0 });

// ================= SECTION B =================
pres.addSection({ title: "2 故障演示 · SPEAKER B" });
section("02", "九个故障,现场审判", "预测 → 注入 → 观察 → 解释");

// ---- 10 演示协议 ----
s = content("PROTOCOL · 06", "每个演示都是同一套四步", S.B);
[["预测", "先说清预期行为", ICE], ["注入", "点按钮 / docker kill", AMBER],
 ["观察", "指着屏幕看实际", GREEN], ["解释", "违反了什么 / 为何仍正确", "CFE0F5"]]
.forEach(([h, b, c], i) => {
  const x = 0.55 + i * 3.18;
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.2, w: 2.85, h: 2.3, rectRadius: 0.09,
    fill: { color: PANEL }, line: { color: LINE, width: 1 } });
  s.addText(`${i + 1} · ${h}`, { x, y: 2.5, w: 2.85, h: 0.6, fontSize: 21, bold: true,
    color: c, align: "center", isTextBox: true, margin: 0 });
  s.addText(b, { x: x + 0.2, y: 3.25, w: 2.45, h: 0.9, fontSize: 13.5,
    align: "center", color: DIM, isTextBox: true, margin: 0, lineSpacingMultiple: 1.35 });
});
s.addText("第四步是全场重点:违反了什么,为什么敢违反,什么时候不能违反 —— 每个故障都交代清楚。",
  { x: 0.55, y: 5.05, w: 12.2, h: 0.6, fontSize: 16, color: AMBER, isTextBox: true, margin: 0 });

// ---- 11 总览表 ----
s = content("NINE FAILURES · 07", "九个故障,三组演示方式", S.B);
mkTable(s, 0.55, 1.85, 12.2, [
  ["#", "故障", "方式", "看点"],
  ["1", "副本宕机", "终端 kill", "恢复后 gossip 自动补齐,无人工"],
  ["2", "分区 + 重复×3", "UI", "愈合后 = 两侧之和,重复不多计"],
  ["3", "延迟 10s 乱序", "UI", "旧值窗口可见,终值与顺序无关"],
  ["4", "重启丢内存", "终端 + 断言", "WAL 开 = 完整 / 关 = 丢,边界清晰"],
  ["5", "迁移一半宕机", "终端 + 断言", "老集群零影响,迁移幂等重入"],
  ["6", "热点 key 50%", "终端压测", "写散三副本,延迟差 3.0x"],
  ["7", "并发 CAS", "终端 + 断言", "local 双成功(违线) / quorum 恰一"],
  ["8", "时钟倒退", "UI", "LWW 丢更新反例,主路径免疫"],
  ["9", "响应丢失", "UI", "同 request_id 重试,不双计"],
], { colW: [0.7, 2.7, 2.1, 6.7], size: 12.5, rowH: 0.44 });

// ---- 12 分区愈合终端 ----
s = content("LIVE · 08", "高光:分区 → 分歧 → 愈合", S.B);
s.addText("预测:剪断 node1—node2,两侧各写 10 分;愈合后三副本自动等于 20,消息重复 ×3 不多算",
  { x: 0.55, y: 1.85, w: 12.2, h: 0.55, fontSize: 15, color: ICE, isTextBox: true, margin: 0 });
term(s, 0.55, 2.55, 7.4, 3.6, [
  "$ python demos/demo_02_partition_duplicate.py",
  "",
  "[PREDICT] 分区期间两侧各写 10,各自只见本侧",
  "[INJECT ] 双向分区 → 两侧各写 → 愈合时重复投递×3",
  "[OBSERVE] 分区期间: node1=10, node2=10 (分歧)",
  "[RESULT ] PASS 三副本 score 全部 == 20",
], { size: 13 });
card(s, 8.25, 2.55, 4.5, 3.6, "解释",
  ["重复消息零效果:", "条目按 request_id 并集,", "同一条目投多少次都只算一次", "",
   "分歧是合法执行:", "最终一致 = 愈合后收敛,", "不是随时一致"], AMBER);

// ---- 13 热点 chart ----
s = content("LIVE · 09", "高光:热点 key,写散三副本", S.B);
s.addChart(pres.ChartType.bar, [
  { name: "primary-only(单点串行)", labels: ["热点写中位延迟"], values: [142.0] },
  { name: "任意副本(热点分片)", labels: ["热点写中位延迟"], values: [46.8] },
], {
  x: 0.55, y: 1.95, w: 7.2, h: 4.3,
  barDir: "bar",
  chartColors: [AMBER, GREEN],
  showTitle: false, showValue: true, dataLabelPosition: "outEnd",
  dataLabelColor: "CFE0F5", dataLabelFontSize: 14, dataLabelFontFace: MONO,
  catAxisLabelColor: "CFE0F5", catAxisLabelFontSize: 13,
  valAxisLabelColor: DIM, valAxisLabelFontSize: 10,
  valGridLine: { color: LINE, size: 1 }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "b", legendColor: "CFE0F5", legendFontSize: 12,
  valAxisMaxVal: 160,
});
card(s, 8.05, 1.95, 4.7, 2.0, "3.0x", ["差整三倍 = 副本数并行度", "两组分数均准确(600/600)"], GREEN);
card(s, 8.05, 4.15, 4.7, 2.1, "这就是热点分片",
  ["不迁移 key,不路由", "任意副本本地记账", "merge 收敛保正确"], ICE);

// ---- 14 CAS ----
s = content("LIVE · 10", "高光:CAS 的三次审判", S.B);
mkTable(s, 0.55, 1.95, 12.2, [
  ["场景", "模式", "结果", "含义"],
  ["健康,都发 primary", "local", "恰 1 成功 → 110", "单点串行 = 看起来线性"],
  ["分区,两侧各发", "local", "双成功 → 120 ≠ 110", "违反线性一致 —— 主动展示"],
  ["分区,两侧各发", "quorum W=2", "恰 1 成功 → 110", "线性回归,代价=少数侧不可用"],
], { colW: [3.5, 2.0, 3.1, 3.6], size: 14, rowH: 0.58 });
s.addText([
  { text: "场景 2 不是 bug,是 AP 系统的明码标价:分区拿走线性性,换来两侧继续可写。", options: { breakLine: true } },
  { text: "场景 3 证明想要回来随时可以 —— 用 quorum 的可用性换。这就是 CAP:我们不躲它,我们交易它。", options: {} },
], { x: 0.55, y: 4.6, w: 12.2, h: 1.3, fontSize: 16, color: AMBER, isTextBox: true,
  margin: 0, lineSpacingMultiple: 1.5 });

// ---- 15 演示台 ----
s = content("GROUND CONTROL · 11", "演示环境:地面控制台", S.B);
s.addImage({ path: "ui-screenshot.png", x: 0.55, y: 1.9, w: 7.5 });
bullets(s, 8.45, 2.1, 4.3, [
  "拓扑区:三副本 + proxy",
  "绿点 = gossip 数据流(复制看得见)",
  "分区时粒子熄灭、连线断裂",
  "故障注入一键化,一键愈合",
  "排行榜切视角:旧值窗口直观",
  "localhost:9000/ui",
], { size: 13, gap: 9, h: 2.4 });

// ================= SECTION C =================
pres.addSection({ title: "3 理论与总结 · SPEAKER C" });
section("03", "理论与总结", "quorum · happens-before · 时钟 · 局限");

// ---- 17 quorum ----
s = content("QUORUM · 12", "quorum:鸽笼原理买到的保证", S.C);
s.addShape(pres.ShapeType.roundRect, { x: 0.55, y: 1.9, w: 12.2, h: 1.35, rectRadius: 0.08,
  fill: { color: PANEL2 }, line: { color: ICE, width: 1.2 } });
s.addText([
  { text: "N=3, W=2, R=2  →  W + R = 4 > 3", options: { breakLine: true, bold: true, color: ICE } },
  { text: "任意写多数派与读多数派必有交集 → 读至少碰到一个见过新写的节点", options: {} },
], { x: 0.9, y: 2.08, w: 11.5, h: 1.0, fontSize: 17, isTextBox: true, margin: 0,
  lineSpacingMultiple: 1.45 });
bullets(s, 0.8, 3.6, 11.7, [
  "我们没做 read-repair → quorum 读是\"大幅降低旧值概率\",不是线性读",
  "quorum CAS = pre-write 凑票 → commit 两阶段,分区少数侧拒绝提交",
  "W 从 2 改 1:相交性被破坏 ——\"写成功但读不到\"成为合法执行",
], { size: 15, gap: 11, h: 1.7 });
s.addText("每个数字都能从鸽笼推出来,不是调参。",
  { x: 0.55, y: 5.9, w: 12, h: 0.4, fontSize: 14, color: DIM, isTextBox: true, margin: 0 });

// ---- 18 happens-before ----
s = content("HAPPENS-BEFORE · 13", "并发时,系统只有三条路", S.C);
s.addText("分区两侧的两个 CAS 互不 happens-before —— 没有消息路径互相看见 = 并发;判定工具:版本向量。",
  { x: 0.55, y: 1.85, w: 12.2, h: 0.5, fontSize: 15, color: "CFE0F5", isTextBox: true, margin: 0 });
mkTable(s, 0.55, 2.55, 12.2, [
  ["面对并发写", "做法", "代价 / 我们的态度"],
  ["报错", "Paxos / Raft 拒绝一个", "分区期间少数侧不可写 —— 对加分太奢侈"],
  ["仲裁", "LWW 时间戳大者胜", "丢更新,且时钟不可靠(演示 8 反例)"],
  ["都要", "CRDT 并集 ← 我们", "并发加分本来就应都保留,语义天然正确"],
], { colW: [2.4, 4.2, 5.6], size: 14, rowH: 0.62 });
s.addText("数据结构选型 = 提前给\"并发怎么办\"写好答案。CAS 是读改写,并发下无安全合并 —— 所以它才需要 quorum 或认命。",
  { x: 0.55, y: 5.4, w: 12.2, h: 0.8, fontSize: 15.5, isTextBox: true, margin: 0,
    lineSpacingMultiple: 1.4 });

// ---- 19 时钟 + 局限 ----
s = content("CLOCKS & LIMITS · 14", "时钟不可信 · 局限如实交代", S.C);
bullets(s, 0.55, 1.9, 5.9, [
  "会回跳:NTP / 闰秒 / VM 挂起",
  "不可比:没有两机的\"同一时刻\"",
  "精度有限:同毫秒两写无法定序",
], { size: 14.5, gap: 9, h: 1.4 });
s.addShape(pres.ShapeType.roundRect, { x: 0.55, y: 3.5, w: 5.9, h: 2.6, rectRadius: 0.08,
  fill: { color: PANEL2 }, line: { color: AMBER, width: 1 } });
s.addText([
  { text: "三层对策", options: { bold: true, color: AMBER, breakLine: true, paraSpaceAfter: 8 } },
  { text: "① 主路径零依赖 —— 合并不读时间戳", options: { breakLine: true } },
  { text: "② 因果交给逻辑时钟", options: { breakLine: true } },
  { text: "③ 物理时钟只用于人看的日志", options: {} },
], { x: 0.85, y: 3.7, w: 5.3, h: 2.2, fontSize: 14.5, isTextBox: true, margin: 0,
  lineSpacingMultiple: 1.5 });
mkTable(s, 6.85, 1.9, 5.9, [
  ["局限", "改进方向"],
  ["gossip 全量推送", "Merkle 差异检测"],
  ["无读修复", "读时补新"],
  ["存储 ×3 冗余", "冷热分层"],
  ["CAS 简化两阶段", "生产换 Raft"],
  ["节点间无认证", "request_id 签名"],
], { colW: [2.7, 3.2], size: 12.5, rowH: 0.5 });
s.addText("前两项只影响收敛速度,不影响正确性 —— \"最终\"本来就是时间参数。",
  { x: 6.85, y: 5.15, w: 5.9, h: 0.8, fontSize: 12.5, color: DIM, isTextBox: true,
    margin: 0, lineSpacingMultiple: 1.4 });

// ---- 20 statement 总结 ----
s = pres.addSlide({ masterName: "STATEMENT", sectionTitle: "3 理论与总结 · SPEAKER C" });
s.addText("把\"当前值\"换成\"事件集合\"\n九种故障,变成同一个数学性质的九次复读", { placeholder: "quote" });
s.addText("机器会挂 → WAL + 反熵   ·   网络会坏 → 并集合并   ·   时钟不可信 → 零时钟依赖", { placeholder: "sub" });

// ---- 21 QA ----
pres.addSection({ title: "4 Q&A" });
s = pres.addSlide({ masterName: "COVER", sectionTitle: "4 Q&A" });
s.addText("", { placeholder: "eyebrow" });
s.addText("谢谢 · Q & A", { placeholder: "title" });
s.addText("弄不坏的排行榜 —— 条目集 CRDT · 异步复制 · 热点分片", { placeholder: "subtitle" });
s.addText("演示台 localhost:9000/ui · GitHub · report.pdf",
  { x: 0.9, y: 6.3, w: 11, h: 0.4, fontSize: 13, color: DIM, fontFace: MONO,
    isTextBox: true, margin: 0 });

// ---------------- write + theme + finish ----------------
(async () => {
  await pres.writeFile({ fileName: "deck-v2.pptx" });
  await applyTheme("deck-v2.pptx", THEME);
  console.log("deck-v2.pptx written + themed,", pres.slides ? "" : "", "20 slides");
})().catch(e => { console.error(e); process.exit(1); });
