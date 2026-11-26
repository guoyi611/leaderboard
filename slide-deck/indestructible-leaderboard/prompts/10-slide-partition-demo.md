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
Slide 10 — Filename: 10-slide-partition-demo.png — Type: Content

NARRATIVE GOAL:
第一个演示高光:分区期间两侧分歧,愈合后自动收敛,重复投递不多算。

KEY CONTENT:
Headline: 演示一:剪断网线,再自动愈合
Sub-headline: 预测 → 注入 → 观察 → 解释
Body:
- 注入:剪断 node1—node2 之间的一切消息(双向分区),并把每条消息复制三份投递
- 观察:分区期间两侧各写 10 分,互相看不见;愈合后三台机器自动一致 = 20
- 解释:重复投递零效果 —— 按唯一编号并集,投多少次都只算一次
- 断言输出:PASS · 三副本 score 全部 == 20

VISUAL:
Left: terminal window mock drawn in blueprint style (rectangular frame, monospace-style text lines rendered as clean glyphs) showing the demo run output with final line "[RESULT] PASS 三副本 score 全部 == 20" highlighted in Engineering Blue fill bar. Right: three-node triangle schematic with the node1—node2 edge drawn as severed (double slash break marks, Amber), small "×3" stamps on message packets; a small green check badge "自愈" near healed edge annotation.

// LAYOUT
Layout: split-code-diagram
Headline top, terminal mock on left 55%, schematic on right 45%.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 演示一:剪断网线,再自动愈合
- 预测 → 注入 → 观察 → 解释
- 注入:剪断 node1—node2 之间的一切消息(双向分区),并把每条消息复制三份投递
- 观察:分区期间两侧各写 10 分,互相看不见;愈合后三台机器自动一致 = 20
- 解释:重复投递零效果 —— 按唯一编号并集,投多少次都只算一次
- 断言输出:PASS · 三副本 score 全部 == 20


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
