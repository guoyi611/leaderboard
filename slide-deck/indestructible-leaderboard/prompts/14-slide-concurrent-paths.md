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
Slide 14 — Filename: 14-slide-concurrent-paths.png — Type: Content

NARRATIVE GOAL:
理论第二讲:面对并发写,系统只有三条路,我们的选择有数学依据。

KEY CONTENT:
Headline: 面对并发,只有三条路
Sub-headline: 两个操作互相看不见 = 并发(谁先谁后无法判定)
Body:
- 报错:共识协议拒绝其中一个 —— 分区期间少数侧不可写,对排行榜太奢侈
- 仲裁:比时间戳,新者胜 —— 会丢更新,而且时钟不可靠
- 都要:并集合并 ← 我们 —— 并发加分本来就都该保留,语义天然正确
- CAS 是"检查再写入",并发下没有安全的自动合并,所以它才需要 quorum

VISUAL:
Blueprint fork-in-road diagram: one incoming arrow labeled "两个并发写" splits via orthogonal junction into three framed paths; path 1 "报错" with a stop-sign symbol; path 2 "仲裁" with a balance icon where one card falls into a trash bin (丢更新, Amber mark); path 3 "都要" drawn with Engineering Blue emphasis, thicker border, showing two cards merging into a larger stack labeled "并集", stamped "我们的选择". Bottom footnote strip: 数据结构选型 = 提前写好并发的答案.

// LAYOUT
Layout: branching-diagram
Headline top, three-way fork center, footnote strip bottom.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 面对并发,只有三条路
- 两个操作互相看不见 = 并发(谁先谁后无法判定)
- 报错:共识协议拒绝其中一个 —— 分区期间少数侧不可写,对排行榜太奢侈
- 仲裁:比时间戳,新者胜 —— 会丢更新,而且时钟不可靠
- 都要:并集合并 ← 我们 —— 并发加分本来就都该保留,语义天然正确
- CAS 是"检查再写入",并发下没有安全的自动合并,所以它才需要 quorum


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
