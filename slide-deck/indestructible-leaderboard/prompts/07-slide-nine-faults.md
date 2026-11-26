Create a presentation slide image following these guidelines:

## Image Specifications
- Type: Presentation slide
- Aspect Ratio: 16:9 (landscape)
- Style: Professional slide deck

## Core Principles
- Clean, uncluttered layouts with clear visual hierarchy
- Each slide conveys ONE clear message
- NO slide numbers, page numbers, footers, headers, or logos

## CRITICAL TEXT RULES (highest priority)
- All Chinese text MUST be rendered EXACTLY as written below, character by character. Never substitute, translate to English, or distort strokes.
- The slide may ONLY contain the text listed in the "ALLOWED TEXT" section. Do NOT add any other text, labels, captions, watermarks, decorative characters, or pseudo-text anywhere.
- NO small filler text, NO fake table cells with gibberish. Any table-like element may only contain the listed words.
- Keep every text element large and readable.

## STYLE_INSTRUCTIONS
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

## SLIDE CONTENT
Slide 7 — Filename: 07-slide-nine-faults.png — Type: Content

NARRATIVE GOAL:
证明核心设计的威力:一张表格把九种故障全部"变无害"。

KEY CONTENT:
Headline: 一个数据结构,九个故障变无害
Sub-headline: 收敛性是数学性质,不是测试运气
Body:
- 副本宕机 → 落盘日志重放 + 自动补课
- 分区+重复投递 → 并集去重,投多少次都只算一次
- 延迟乱序 → 并集与顺序无关
- 重启丢内存 → 先写日志再确认
- 迁移一半宕机 → 记录不可变,迁移可重入
- 热点 key → 任意副本都能收写
- 并发 CAS → 已知会双成功,quorum 模式可修复
- 时钟倒退 → 合并根本不读时间戳
- 响应丢失 → 同编号重试,不会双计

VISUAL:
A clean blueprint inspection checklist table drawn like an engineering QA sign-off sheet: thin orthogonal grid lines, 9 rows, columns [故障现象 | 为什么无害 | 状态]. Status column shows 9 small green-blue check marks stamped in rows. Header row in Navy fill with white text. One row (并发 CAS) marked with a small Amber triangle instead of check, with footnote "已知的取舍". Title block in bottom-right corner as on real drawings.

// LAYOUT
Layout: table-full
Headline top-left, large checklist table filling the slide, generous row height.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 一个数据结构,九个故障变无害
- 收敛性是数学性质,不是测试运气
- 副本宕机 → 落盘日志重放 + 自动补课
- 分区+重复投递 → 并集去重,投多少次都只算一次
- 延迟乱序 → 并集与顺序无关
- 重启丢内存 → 先写日志再确认
- 迁移一半宕机 → 记录不可变,迁移可重入
- 热点 key → 任意副本都能收写
- 并发 CAS → 已知会双成功,quorum 模式可修复
- 时钟倒退 → 合并根本不读时间戳
- 响应丢失 → 同编号重试,不会双计


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
