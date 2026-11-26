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
Slide 5 — Filename: 05-slide-cap-bet.png — Type: Content

NARRATIVE GOAL:
讲清 CAP 取舍:分区时必须在一致性和可用性之间二选一,我们的业务允许选可用性。

KEY CONTENT:
Headline: 我们的赌注:要可用,还是要一致?
Sub-headline: 分区发生时,鱼与熊掌不可兼得(CAP 定理)
Body:
- 选一致性(CP):分区期间拒绝部分写入 —— 银行余额的正确选择,但排行榜用它太奢侈
- 选可用性(AP)← 我们:分区期间两侧继续写入,代价是暂时不一致
- 业务已授权"可短暂读旧值",所以我们敢赌:分区愈合后自动收敛

VISUAL:
Blueprint balance-scale drawn in precise orthogonal linework at center: left pan holds a locked box labeled "C 一致性", right pan (lower, chosen, highlighted Engineering Blue fill) holds a lightning bolt labeled "A 可用性". Fulcrum labeled "分区". A handwritten-style(仅此一处手写感)check mark next to right pan. Dimension annotation under the scale: "只能压一头".

// LAYOUT
Layout: center-diagram
Headline top, central scale diagram, two annotation columns left/right.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 我们的赌注:要可用,还是要一致?
- 分区发生时,鱼与熊掌不可兼得(CAP 定理)
- 选一致性(CP):分区期间拒绝部分写入 —— 银行余额的正确选择,但排行榜用它太奢侈
- 选可用性(AP)← 我们:分区期间两侧继续写入,代价是暂时不一致
- 业务已授权"可短暂读旧值",所以我们敢赌:分区愈合后自动收敛


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
