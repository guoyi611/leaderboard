"""生成 PPT:游戏排行榜分布式系统(深色 Mission Control 风格)。

用法: python ppt/make_ppt.py  -> 输出 ppt/leaderboard.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

VOID = RGBColor(0x07, 0x0B, 0x14)
PANEL = RGBColor(0x0D, 0x14, 0x20)
PHOSPHOR = RGBColor(0x35, 0xE0, 0x8A)
AMBER = RGBColor(0xFF, 0xB3, 0x40)
ALARM = RGBColor(0xFF, 0x4D, 0x5E)
ICE = RGBColor(0x7D, 0xD3, 0xFC)
TEXT = RGBColor(0xCF, 0xE0, 0xF5)
DIM = RGBColor(0x76, 0x89, 0xA3)
MONO = "Consolas"
YAHEI = "Microsoft YaHei"

SW, SH = Inches(13.333), Inches(7.5)


def slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid(); bg.fill.fore_color.rgb = VOID
    bg.line.fill.background()
    bg.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=PANEL, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    sh.adjustments[0] = 0.06
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line; sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def txt(s, x, y, w, h, text, size=18, color=TEXT, bold=False, font=YAHEI,
        align=PP_ALIGN.LEFT, mono=False, spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run(); r.text = line
        f = r.font
        f.size = Pt(size); f.color.rgb = color; f.bold = bold
        f.name = MONO if mono else font
    return tb


def eyebrow(s, text, color=PHOSPHOR):
    txt(s, Inches(0.55), Inches(0.32), Inches(11), Inches(0.4),
        text, size=12, color=color, mono=True, bold=True)


def title(s, text, color=TEXT):
    txt(s, Inches(0.55), Inches(0.68), Inches(12.3), Inches(0.9),
        text, size=30, color=color, bold=True)


def speaker_tag(s, who):
    txt(s, Inches(11.3), Inches(0.32), Inches(1.6), Inches(0.4),
        who, size=11, color=DIM, mono=True, align=PP_ALIGN.RIGHT)


def bullet_list(s, x, y, w, items, size=16, gap=0.52, color=TEXT, dot=PHOSPHOR):
    for i, it in enumerate(items):
        yy = y + Inches(gap) * i
        c = s.shapes.add_shape(MSO_SHAPE.OVAL, x, yy + Inches(0.13), Inches(0.09), Inches(0.09))
        c.fill.solid(); c.fill.fore_color.rgb = dot; c.line.fill.background()
        c.shadow.inherit = False
        txt(s, x + Inches(0.28), yy, w - Inches(0.3), Inches(0.5), it, size=size, color=color)


def table(s, x, y, w, rows, col_ws=None, header=True, size=13, row_h=0.42):
    n_r, n_c = len(rows), len(rows[0])
    tbl_shape = s.shapes.add_table(n_r, n_c, x, y, w, Inches(row_h * n_r))
    tbl = tbl_shape.table
    if col_ws:
        total = sum(col_ws)
        for i, cw in enumerate(col_ws):
            tbl.columns[i].width = Emu(int(w * cw / total))
    for r_i, row in enumerate(rows):
        tbl.rows[r_i].height = Inches(row_h)
        for c_i, cell_text in enumerate(row):
            cell = tbl.cell(r_i, c_i)
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = PANEL if (r_i % 2 == 0 or not header) else RGBColor(0x0A, 0x11, 0x1E)
            if header and r_i == 0:
                cell.fill.fore_color.rgb = RGBColor(0x10, 0x1A, 0x2B)
            p = cell.text_frame.paragraphs[0]
            r = p.add_run(); r.text = str(cell_text)
            r.font.size = Pt(size if not (header and r_i == 0) else size - 1)
            r.font.name = YAHEI
            if header and r_i == 0:
                r.font.color.rgb = ICE; r.font.bold = True
            else:
                r.font.color.rgb = TEXT


prs = Presentation()
prs.slide_width = SW; prs.slide_height = SH

# ---------------- 1 封面 ----------------
s = slide(prs)
txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(0.5),
    "SOUTH CHINA NORMAL UNIVERSITY · PARALLEL COMPUTING", size=13, color=PHOSPHOR, mono=True)
txt(s, Inches(0.9), Inches(1.8), Inches(11.5), Inches(1.5),
    "弄不坏的排行榜", size=54, bold=True)
txt(s, Inches(0.9), Inches(3.0), Inches(11.5), Inches(0.8),
    "高写入场景下的最终一致性分布式 KV(场景三 · 游戏排行榜)", size=20, color=ICE)
box(s, Inches(0.9), Inches(4.15), Inches(7.2), Inches(2.0), fill=PANEL)
txt(s, Inches(1.2), Inches(4.4), Inches(6.8), Inches(1.6),
    "条目集 CRDT · 异步复制 · 热点分片\n9 类故障注入全覆盖,Docker 一键复现\n演示台 localhost:9000/ui",
    size=15, color=TEXT, spacing=1.5)
txt(s, Inches(0.9), Inches(6.5), Inches(11.5), Inches(0.6),
    "汇报人:A(背景与架构) · B(故障演示) · C(理论与总结)      2026-12", size=14, color=DIM)

# ---------------- 2 场景 ----------------
s = slide(prs); eyebrow(s, "01 · THE SCENE"); speaker_tag(s, "SPEAKER A")
title(s, "游戏排行榜:存储里最难伺候的场景")
cards = [
    ("写入量巨大", "每杀怪/捡金币都是加分\nQPS 高出订单类业务 1-2 个量级", PHOSPHOR),
    ("可容忍旧值", "榜单晚几秒更新,无用户投诉\n业务给的宽容 = 设计空间", ICE),
    ("热点集中", "头部主播一个 key 占 50% 请求\n单 key 打穿单节点", AMBER),
]
for i, (h, b, c) in enumerate(cards):
    x = Inches(0.55 + i * 4.25)
    box(s, x, Inches(2.0), Inches(3.9), Inches(2.6), line=RGBColor(0x1C, 0x2A, 0x40))
    txt(s, x + Inches(0.3), Inches(2.3), Inches(3.4), Inches(0.6), h, size=20, bold=True, color=c)
    txt(s, x + Inches(0.3), Inches(3.0), Inches(3.4), Inches(1.4), b, size=14, color=TEXT, spacing=1.4)
txt(s, Inches(0.55), Inches(5.2), Inches(12), Inches(0.8),
    "一句话:既要吞下高写入和热点,又被允许短暂不一致 —— 这张\"优惠券\"怎么花,就是我们的设计。", size=16, color=DIM)

# ---------------- 3 单机死穴 ----------------
s = slide(prs); eyebrow(s, "02 · WHY DISTRIBUTED"); speaker_tag(s, "SPEAKER A")
title(s, "难题从哪来:单机的两个死穴")
box(s, Inches(0.55), Inches(1.9), Inches(5.9), Inches(2.2), line=RGBColor(0x2A, 0x1F, 0x40))
txt(s, Inches(0.85), Inches(2.1), Inches(5.3), Inches(0.5), "死穴一:写不动", size=19, bold=True, color=ALARM)
txt(s, Inches(0.85), Inches(2.7), Inches(5.3), Inches(1.2),
    "磁盘与网络带宽有物理上限\n热点 key 在单节点上串行排队", size=15, spacing=1.5)
box(s, Inches(6.85), Inches(1.9), Inches(5.9), Inches(2.2), line=RGBColor(0x2A, 0x1F, 0x40))
txt(s, Inches(7.15), Inches(2.1), Inches(5.3), Inches(0.5), "死穴二:一挂全没", size=19, bold=True, color=ALARM)
txt(s, Inches(7.15), Inches(2.7), Inches(5.3), Inches(1.2),
    "单点故障 = 全服榜单消失\n宕机不是意外,是常态", size=15, spacing=1.5)
txt(s, Inches(0.55), Inches(4.5), Inches(12.2), Inches(0.7),
    "答案看起来自然:加机器,多副本 —— 但数据一旦存在多台机器上,三个新难题自动出现 ↓",
    size=17, color=PHOSPHOR, bold=True)

# ---------------- 4 分布式三难 ----------------
s = slide(prs); eyebrow(s, "03 · THE REAL PROBLEM"); speaker_tag(s, "SPEAKER A")
title(s, "真正的难题:副本世界的三条物理定律")
bullet_list(s, Inches(0.8), Inches(2.0), Inches(11.8), [
    "机器会挂 —— 三台机器,一年内宕机几乎是必然事件",
    "网络会坏 —— 不只断,还会延迟 10s、乱序、重复投递三次、丢响应",
    "时钟不可信 —— NTP 校时会跳会倒退,两台机器的\"同一时刻\"不存在",
], size=18, gap=0.75)
box(s, Inches(0.8), Inches(4.6), Inches(11.7), Inches(1.6), fill=RGBColor(0x10, 0x1A, 0x2B))
txt(s, Inches(1.1), Inches(4.85), Inches(11.1), Inches(1.2),
    "所以问题不是\"把数据存三份\",而是:\n在会挂、会乱、会跳的世界里,怎么让三份数据最终变成\"一份\" —— CAP 的取舍开始了",
    size=17, color=ICE, spacing=1.5, bold=True)

# ---------------- 5 CAP 取舍 ----------------
s = slide(prs); eyebrow(s, "04 · THE BET"); speaker_tag(s, "SPEAKER A")
title(s, "我们的赌注:AP + 最终一致性")
box(s, Inches(0.55), Inches(1.9), Inches(6.0), Inches(3.0), line=PHOSPHOR)
txt(s, Inches(0.85), Inches(2.15), Inches(5.4), Inches(0.5), "C 一致性 (CP)", size=18, bold=True, color=DIM)
txt(s, Inches(0.85), Inches(2.75), Inches(5.4), Inches(1.9),
    "分区时少数派拒绝写入\n· 银行余额的正确选择\n· 排行榜用它是浪费:\n  分区期间全服不能加分", size=15, spacing=1.45)
box(s, Inches(6.8), Inches(1.9), Inches(6.0), Inches(3.0), line=PHOSPHOR)
txt(s, Inches(7.1), Inches(2.15), Inches(5.4), Inches(0.5), "A 可用性 (AP) ← 我们", size=18, bold=True, color=PHOSPHOR)
txt(s, Inches(7.1), Inches(2.75), Inches(5.4), Inches(1.9),
    "分区时两侧都继续写\n· 代价:暂时不一致\n· 业务已授权\"可短暂读旧值\"\n· 换来:写入永不拒绝", size=15, spacing=1.45)
txt(s, Inches(0.55), Inches(5.3), Inches(12), Inches(1.0),
    "承诺降级为:分区愈合后,有限时间内三副本自动收敛 —— \"最终\"一致。\n这句话是后面九个演示唯一要证明的事。", size=16, color=TEXT, spacing=1.4)

# ---------------- 6 核心设计 ----------------
s = slide(prs); eyebrow(s, "05 · THE ONE IDEA"); speaker_tag(s, "SPEAKER A")
title(s, "全部设计的基石:存事件,不存当前值")
box(s, Inches(0.55), Inches(1.85), Inches(12.2), Inches(1.35), fill=RGBColor(0x10, 0x1A, 0x2B), line=PHOSPHOR)
txt(s, Inches(0.9), Inches(2.1), Inches(11.6), Inches(0.9),
    '每次加分 = 一条不可变条目 (request_id, player, delta, ts, node)\n分数 = 该玩家全部条目之和        合并 = 按 request_id 求并集',
    size=17, color=PHOSPHOR, mono=False, spacing=1.5, bold=True)
txt(s, Inches(0.55), Inches(3.5), Inches(12), Inches(0.5),
    "类比:不存文件,存 Git 提交历史 —— 历史只会追加,永远不会冲突", size=15, color=ICE)
bullet_list(s, Inches(0.8), Inches(4.3), Inches(11.5), [
    "重复投递 → 同一条目并集只算一次(幂等)",
    "乱序到达 → 并集与顺序无关(交换律)",
    "分区分歧 → 愈合后并集 = 两侧之和(收敛)",
    "任何副本可写 → 写并行度 = 副本数(热点分片)",
], size=16, gap=0.6)

# ---------------- 7 故障→无害 映射 ----------------
s = slide(prs); eyebrow(s, "06 · ONE MECHANISM, NINE FAILURES"); speaker_tag(s, "SPEAKER A")
title(s, "一个数据结构,九个故障变无害")
table(s, Inches(0.55), Inches(1.9), Inches(12.2), [
    ["故障 topic", "攻击点", "为什么无害"],
    ["副本宕机", "丢副本", "WAL 重放 + gossip 反熵自动补课"],
    ["分区 + 重复×3", "复制协议", "并集幂等,重复与顺序都算不错"],
    ["延迟 10s 乱序", "复制协议", "交换律:先到后到结果一样"],
    ["重启丢内存", "持久化", "条目先追加 WAL 再确认"],
    ["迁移一半宕机", "扩容", "条目不可变 → 迁移幂等可重入"],
    ["热点 key 50%", "吞吐", "任意副本可写,并行度=3"],
    ["并发 CAS", "线性性", "local 双成功(已知违反) / quorum 恰一成功"],
    ["时钟倒退", "定序", "主路径不读时间戳"],
    ["响应丢失", "确认语义", "request_id 幂等重试,不双计"],
], col_ws=[2.6, 2.2, 7.4], size=12, row_h=0.42)
txt(s, Inches(0.55), Inches(6.45), Inches(12), Inches(0.5),
    "学术名字:CRDT(grow-only set 变体)· 收敛性的数学条件:幂等 + 交换 + 结合", size=14, color=DIM)

# ---------------- 8 架构 ----------------
s = slide(prs); eyebrow(s, "07 · ARCHITECTURE"); speaker_tag(s, "SPEAKER A")
title(s, "系统架构:三副本 + 可控网络")
node_pos = [(1.7, 2.2), (5.3, 2.2), (3.5, 4.3)]
for i, (nx, ny) in enumerate(node_pos):
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(nx), Inches(ny), Inches(1.9), Inches(1.9))
    c.fill.solid(); c.fill.fore_color.rgb = PANEL; c.line.color.rgb = PHOSPHOR; c.line.width = Pt(2)
    c.shadow.inherit = False
    txt(s, Inches(nx), Inches(ny + 0.55), Inches(1.9), Inches(0.5), f"node{i+1}",
        size=15, bold=True, align=PP_ALIGN.CENTER, mono=True)
    txt(s, Inches(nx), Inches(ny + 0.95), Inches(1.9), Inches(0.4), "副本+WAL",
        size=11, color=DIM, align=PP_ALIGN.CENTER)
px, py, pw, ph = 9.0, 2.9, 3.3, 1.3
pb = box(s, Inches(px), Inches(py), Inches(pw), Inches(ph), line=ICE)
txt(s, Inches(px), Inches(py + 0.18), Inches(pw), Inches(0.5), "net-proxy",
    size=15, bold=True, color=ICE, align=PP_ALIGN.CENTER, mono=True)
txt(s, Inches(px), Inches(py + 0.62), Inches(pw), Inches(0.5), "延迟/乱序/重复/分区/吞响应",
    size=10, color=DIM, align=PP_ALIGN.CENTER)
for nx, ny in node_pos:
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                Inches(nx + 1.9), Inches(ny + 0.95), Inches(px), Inches(py + 0.65))
    cn.line.color.rgb = RGBColor(0x1C, 0x2A, 0x40); cn.line.width = Pt(1.5)
for (x1, y1), (x2, y2) in [(node_pos[0], node_pos[2]), (node_pos[1], node_pos[2]), (node_pos[0], node_pos[1])]:
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                Inches(x1 + 0.95), Inches(y1 + 1.9 if y1 < y2 else 0.0) if False else Inches(x1 + 0.95),
                                Inches(x2 + 0.95), Inches(y2 + (0 if y2 > y1 else 1.9)))
    cn.line.color.rgb = PHOSPHOR; cn.line.width = Pt(2.5)
txt(s, Inches(0.7), Inches(1.75), Inches(4), Inches(0.4), "gossip 1s 全量推送", size=12, color=PHOSPHOR, mono=True)
bullet_list(s, Inches(8.6), Inches(4.6), Inches(4.3), [
    "Docker 4 容器一键起",
    "读:本地(快) / quorum R=2",
    "CAS:primary / quorum W=2",
], size=13, gap=0.5)

# ---------------- 9 演示台 ----------------
s = slide(prs); eyebrow(s, "08 · GROUND CONTROL"); speaker_tag(s, "SPEAKER B")
title(s, "演示环境:地面控制台")
box(s, Inches(0.55), Inches(1.9), Inches(7.6), Inches(4.7), line=RGBColor(0x1C, 0x2A, 0x40))
try:
    import os
    shot = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        "ego", "ui-review-20261126", "shot-01.png")
    if not os.path.exists(shot):
        shot = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "ui-screenshot.png")
    if os.path.exists(shot):
        s.shapes.add_picture(shot, Inches(0.7), Inches(2.0), width=Inches(7.3))
    else:
        txt(s, Inches(0.9), Inches(4.0), Inches(6.9), Inches(0.5),
            "[ 演示台截图:localhost:9000/ui ]", size=16, color=DIM, align=PP_ALIGN.CENTER)
except Exception:
    pass
bullet_list(s, Inches(8.5), Inches(2.1), Inches(4.4), [
    "拓扑区:三副本+proxy,绿点=gossip 数据流(复制看得见)",
    "故障注入一键化:分区/延迟/重复/吞响应/时钟",
    "排行榜切视角:不同副本不同时刻,旧值窗口直观",
    "demo 脚本:断言 PASS/FAIL,可复现可审计",
    "终端+网页双轨演示",
], size=14, gap=0.85)

# ---------------- 10 演示流程 ----------------
s = slide(prs); eyebrow(s, "09 · PROTOCOL"); speaker_tag(s, "SPEAKER B")
title(s, "每个演示都是同一套四步")
steps = [("预测", "先说清楚\n预期行为", ICE), ("注入", "点按钮 /\ndocker kill", AMBER),
         ("观察", "指着屏幕\n看实际结果", PHOSPHOR), ("解释", "违反了哪项保证\n或为何仍正确", TEXT)]
for i, (h, b, c) in enumerate(steps):
    x = Inches(0.55 + i * 3.15)
    box(s, x, Inches(2.2), Inches(2.75), Inches(2.3), line=RGBColor(0x1C, 0x2A, 0x40))
    txt(s, x, Inches(2.5), Inches(2.75), Inches(0.6), f"{i+1} · {h}", size=20, bold=True,
        color=c, align=PP_ALIGN.CENTER)
    txt(s, x + Inches(0.2), Inches(3.25), Inches(2.35), Inches(1.1), b, size=13,
        align=PP_ALIGN.CENTER, spacing=1.4)
txt(s, Inches(0.55), Inches(5.0), Inches(12), Inches(0.9),
    "第四步是全场重点:违反了什么,为什么敢违反,什么时候不能违反 —— 每个故障都交代清楚。",
    size=16, color=AMBER)

# ---------------- 11 9 topic 总览 ----------------
s = slide(prs); eyebrow(s, "10 · NINE FAILURES"); speaker_tag(s, "SPEAKER B")
title(s, "九个故障,三组演示方式")
table(s, Inches(0.55), Inches(1.85), Inches(12.2), [
    ["#", "故障", "方式", "看点"],
    ["1", "副本宕机", "终端 kill", "恢复后 gossip 自动补齐,无人工"],
    ["2", "分区+重复×3", "UI", "愈合后 =两侧之和,重复不多计"],
    ["3", "延迟10s乱序", "UI", "旧值窗口可见,终值与顺序无关"],
    ["4", "重启丢内存", "终端+断言", "WAL 开=完整 / 关=丢,边界清晰"],
    ["5", "迁移一半宕机", "终端+断言", "老集群零影响,迁移幂等重入"],
    ["6", "热点 key 50%", "终端压测", "写散三副本,延迟差 3.0x"],
    ["7", "并发 CAS", "终端+断言", "local 双成功(违线) / quorum 恰一"],
    ["8", "时钟倒退", "UI", "LWW 丢更新反例,主路径免疫"],
    ["9", "响应丢失", "UI", "同 request_id 重试,不双计"],
], col_ws=[0.7, 2.6, 2.0, 6.9], size=13, row_h=0.46)

# ---------------- 12-14 演示高光 ----------------
s = slide(prs); eyebrow(s, "11 · LIVE DEMO"); speaker_tag(s, "SPEAKER B")
title(s, "现场演示:分区 → 分歧 → 愈合")
txt(s, Inches(0.55), Inches(1.9), Inches(12), Inches(0.6),
    "预测:剪断 node1—node2,两侧各写 10 分;愈合后三副本自动等于 20,消息重复×3 不多算",
    size=16, color=ICE)
txt(s, Inches(0.55), Inches(2.7), Inches(12), Inches(0.6),
    "[ 现场 UI 操作 + 此处可贴愈合后截图:三节点 total 全部相同 ]", size=14, color=DIM)
box(s, Inches(0.55), Inches(3.6), Inches(12.2), Inches(2.8), fill=RGBColor(0x0A, 0x11, 0x1E), line=RGBColor(0x1C, 0x2A, 0x40))
txt(s, Inches(0.9), Inches(3.85), Inches(11.5), Inches(2.4),
    "$ python demos/demo_02_partition_duplicate.py\n\n[PREDICT] 分区期间两侧各写 10,各自视图只见本侧\n[INJECT ] 双向分区 → 两侧各写 → 愈合时 gossip 重复投递×3\n[RESULT ] PASS 三副本 score 全部 == 20",
    size=14, color=PHOSPHOR, mono=True, spacing=1.5)

s = slide(prs); eyebrow(s, "12 · LIVE DEMO"); speaker_tag(s, "SPEAKER B")
title(s, "现场演示:热点与迁移")
txt(s, Inches(0.55), Inches(1.9), Inches(12.2), Inches(0.9),
    "热点:同一 key 全部写压 primary(锁+落盘串行) vs 写散三副本 —— 延迟差整三倍\n迁移:node4 拷数据到一半被杀,老集群写入成功率 100%,重启重拷不多算",
    size=15, color=ICE, spacing=1.5)
box(s, Inches(0.55), Inches(3.1), Inches(12.2), Inches(3.2), fill=RGBColor(0x0A, 0x11, 0x1E), line=RGBColor(0x1C, 0x2A, 0x40))
txt(s, Inches(0.9), Inches(3.35), Inches(11.5), Inches(2.8),
    "$ python demos/demo_06_hotkey.py\n  A primary-only: 热点写中位 142.0ms / 普通写 46.8ms\n  B 任意副本   : 热点写中位  46.8ms   →  3.0x\n[RESULT ] PASS  分数 A=600 B=600(准确)\n\n$ python demos/demo_05_migration_crash.py\n  迁移中 kill node4,期间老集群写入 20/20 成功\n[RESULT ] PASS  node4(495) == node1(495)",
    size=14, color=PHOSPHOR, mono=True, spacing=1.4)

s = slide(prs); eyebrow(s, "13 · LIVE DEMO"); speaker_tag(s, "SPEAKER B")
title(s, "现场演示:CAS 的三次审判")
table(s, Inches(0.55), Inches(1.95), Inches(12.2), [
    ["场景", "模式", "结果", "含义"],
    ["健康,都发 primary", "local", "恰 1 成功 → 110", "单点串行 = 看起来线性"],
    ["分区,两侧各写", "local", "双成功 → 120 ≠ 110", "违反线性一致 —— 主动展示"],
    ["分区,两侧各写", "quorum W=2", "恰 1 成功 → 110", "线性性回归,代价=少数侧不可用"],
], col_ws=[3.4, 2.0, 3.2, 3.6], size=14, row_h=0.55)
txt(s, Inches(0.55), Inches(4.6), Inches(12.2), Inches(1.6),
    "场景 2 不是 bug,是 AP 系统的明码标价:分区拿走线性性,换来两侧继续可写。\n场景 3 证明想要回来随时可以 —— 用 quorum 的可用性换。\n这就是 CAP:我们不是躲开它,是把它摆上台面交易。",
    size=16, spacing=1.5, color=AMBER)

# ---------------- 15 quorum ----------------
s = slide(prs); eyebrow(s, "14 · QUORUM"); speaker_tag(s, "SPEAKER C")
title(s, "quorum:鸽笼原理买到的保证")
box(s, Inches(0.55), Inches(1.9), Inches(12.2), Inches(1.3), fill=RGBColor(0x10, 0x1A, 0x2B), line=ICE)
txt(s, Inches(0.9), Inches(2.15), Inches(11.5), Inches(0.9),
    "N=3, W=2, R=2  →  W + R = 4 > 3\n任意写多数派与任意读多数派必有交集 → 读至少碰到一个见过新写的节点",
    size=17, color=ICE, bold=True, spacing=1.5)
bullet_list(s, Inches(0.8), Inches(3.6), Inches(11.5), [
    "我们没做 read-repair → quorum 读是\"大幅降低旧值概率\",不是线性读",
    "quorum CAS = pre-write 凑票(W)→ commit 两阶段,分区少数侧拒绝提交",
    "W 从 2 改 1:1+2>3 不再成立,相交性被破坏 ——\"写成功但读不到\"成为合法执行",
], size=16, gap=0.7)
txt(s, Inches(0.55), Inches(6.2), Inches(12), Inches(0.5),
    "每个数字都能从鸽笼推出来,不是调参。", size=15, color=DIM)

# ---------------- 16 happens-before ----------------
s = slide(prs); eyebrow(s, "15 · HAPPENS-BEFORE"); speaker_tag(s, "SPEAKER C")
title(s, "happens-before:并发时系统只有三条路")
bullet_list(s, Inches(0.8), Inches(1.95), Inches(11.5), [
    "分区两侧的两个 CAS:互不 happens-before —— 没有消息路径互相看见 = 并发",
    "判定工具:版本向量(因果历史),两个向量互不支配 → 并发",
], size=16, gap=0.65)
table(s, Inches(0.55), Inches(3.3), Inches(12.2), [
    ["面对并发写", "做法", "代价 / 我们的态度"],
    ["报错", "Paxos/Raft 拒绝一个", "分区期间少数侧不可写 —— 对加分太奢侈"],
    ["仲裁", "LWW 时间戳大者胜", "丢更新,且时钟不可靠(演示 8 反例)"],
    ["都要", "CRDT 并集 ← 我们", "并发加分本来就应都保留,语义天然正确"],
], col_ws=[2.4, 4.0, 5.8], size=14, row_h=0.55)
txt(s, Inches(0.55), Inches(5.6), Inches(12.2), Inches(1.0),
    "数据结构选型 = 提前给\"并发怎么办\"写好答案。\nCAS 是读改写,并发下无安全合并函数 —— 所以它才需要 quorum 或认命。",
    size=16, spacing=1.4, color=TEXT)

# ---------------- 17 时钟 ----------------
s = slide(prs); eyebrow(s, "16 · CLOCKS"); speaker_tag(s, "SPEAKER C")
title(s, "为什么不能只用物理时钟")
bullet_list(s, Inches(0.8), Inches(1.95), Inches(11.5), [
    "会回跳:NTP 校时 / 闰秒 / VM 挂起 —— 演示 8 现场制造了丢更新",
    "不可比:两台机器没有\"同一时刻\"的总序",
    "精度有限:同一毫秒的两个写无法定序",
], size=17, gap=0.68)
box(s, Inches(0.55), Inches(4.15), Inches(12.2), Inches(1.9), fill=RGBColor(0x10, 0x1A, 0x2B), line=AMBER)
txt(s, Inches(0.9), Inches(4.4), Inches(11.5), Inches(1.5),
    "我们的三层对策:\n① 主路径零依赖 —— 条目合并不读时间戳\n② 因果交给逻辑时钟(happens-before / 版本向量)\n③ 物理时钟只用于人看的日志",
    size=16, spacing=1.5, color=TEXT)
txt(s, Inches(0.55), Inches(6.35), Inches(12), Inches(0.5),
    "Lamport 1978:分布式系统里的先后,由通信定义,不由钟表定义。", size=15, color=ICE)

# ---------------- 18 局限 ----------------
s = slide(prs); eyebrow(s, "17 · LIMITATIONS"); speaker_tag(s, "SPEAKER C")
title(s, "没做好的事,如实交代")
table(s, Inches(0.55), Inches(1.95), Inches(12.2), [
    ["局限", "影响", "改进方向"],
    ["gossip 全量推送", "百万条目级推送代价大", "Merkle 树差异检测,只传差集"],
    ["无读修复", "旧值窗口 ≈ gossip 周期(1s)", "读时补新,窗口指数缩短"],
    ["存储 ×3 全量冗余", "空间成本", "冷热分层,日志重建"],
    ["CAS quorum 是简化两阶段", "无 leader 选举/日志复制", "生产换 Raft"],
    ["节点间无认证", "恶意节点可伪造条目", "request_id 签名 + 节点准入"],
], col_ws=[3.6, 4.0, 4.6], size=14, row_h=0.55)
txt(s, Inches(0.55), Inches(5.6), Inches(12), Inches(0.7),
    "前两项只影响收敛速度,不影响正确性 —— \"最终\"本来就是个时间参数。", size=15, color=DIM)

# ---------------- 19 总结 ----------------
s = slide(prs); eyebrow(s, "18 · SUMMARY"); speaker_tag(s, "SPEAKER C")
title(s, "回到开场的三条物理定律")
table(s, Inches(0.55), Inches(1.95), Inches(12.2), [
    ["定律", "我们的答案"],
    ["机器会挂", "WAL 先落盘再确认 + gossip 反熵,恢复不需要人"],
    ["网络会坏", "不可变条目 + 并集合并,延迟/乱序/重复/分区全部失效"],
    ["时钟不可信", "正确性路径零时钟,因果交给 happens-before"],
], col_ws=[3.0, 9.2], size=16, row_h=0.62)
box(s, Inches(0.55), Inches(4.6), Inches(12.2), Inches(1.5), fill=RGBColor(0x10, 0x1A, 0x2B), line=PHOSPHOR)
txt(s, Inches(0.9), Inches(4.85), Inches(11.5), Inches(1.1),
    "最大的一课:把\"当前值\"换成\"事件集合\",\n九种故障从九个工程难题,变成同一个数学性质的九次复读。",
    size=18, color=PHOSPHOR, bold=True, spacing=1.5)
txt(s, Inches(0.55), Inches(6.4), Inches(12), Inches(0.6),
    "代码 / 九个可复现演示 / 报告:GitHub · docker compose up 一键复现", size=15, color=DIM)

# ---------------- 20 Q&A ----------------
s = slide(prs)
txt(s, Inches(0.9), Inches(2.4), Inches(11.5), Inches(1.2), "谢谢 · Q A",
    size=60, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.9), Inches(4.0), Inches(11.5), Inches(0.8),
    "弄不坏的排行榜 —— 条目集 CRDT · 异步复制 · 热点分片", size=18,
    color=ICE, align=PP_ALIGN.CENTER)
txt(s, Inches(0.9), Inches(5.6), Inches(11.5), Inches(0.6),
    "演示台 localhost:9000/ui · GitHub repo · report.pdf", size=14,
    color=DIM, align=PP_ALIGN.CENTER, mono=True)

out = "leaderboard.pptx"
prs.save(out)
print(f"saved {out} with {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
