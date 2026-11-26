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
Slide 3 — Filename: 03-slide-why-replicas.png — Type: Content

NARRATIVE GOAL:
解释为什么必须多副本:单机两条死穴,多副本是唯一出路。

KEY CONTENT:
Headline: 单机的两条死穴
Sub-headline: 一台机器扛不住,也靠不住
Body:
- 写不动:磁盘与网络带宽有物理上限,热点 key 在单节点上串行排队
- 一挂全没:单点故障 = 全服榜单瞬间消失,而宕机不是意外,是必然
- 出路:加机器,数据存多份 —— 但新的难题随之而来

VISUAL:
Left half: blueprint cross-section of a single server rack with a red Amber "X" mark and two dimension annotations pointing to the disk and network ports, labeled with failure notes in Chinese. Right half: the same drawing replicated into three smaller racks connected by orthogonal lines, drawn in Engineering Blue, labeled "×3 副本". An arrow from left to right labeled "唯一的出路".

// LAYOUT
Layout: split-compare
Left panel (single, warning tones) vs right panel (triple, blue tones), headline across the top.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 单机的两条死穴
- 一台机器扛不住,也靠不住
- 写不动:磁盘与网络带宽有物理上限,热点 key 在单节点上串行排队
- 一挂全没:单点故障 = 全服榜单瞬间消失,而宕机不是意外,是必然
- 出路:加机器,数据存多份 —— 但新的难题随之而来


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
