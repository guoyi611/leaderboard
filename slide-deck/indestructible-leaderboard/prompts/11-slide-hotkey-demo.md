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
Slide 11 — Filename: 11-slide-hotkey-demo.png — Type: Content

NARRATIVE GOAL:
第二个演示高光:热点 key 写入散到三台机器,延迟差整三倍,分数依然准确。

KEY CONTENT:
Headline: 演示二:热点玩家,三台机器一起记账
Sub-headline: 单点串行 142ms vs 三机并行 47ms
Body:
- 对照组:同一个玩家的所有写入都压到一台机器(锁+落盘串行)
- 实验组:同一批写入随机分散到三台 —— 因为任何副本都能收写
- 结果:热点写中位延迟 142.0ms vs 46.8ms,差 3.0 倍 = 副本数
- 两组最终分数完全一致(600 / 600),正确性不受影响

VISUAL:
Clean blueprint bar chart: two horizontal bars with dimension-line styling — top bar (Amber outline) length 3× of bottom bar (Engineering Blue fill), each ending with value labels 142.0ms / 46.8ms in measurement callouts. A dimension bracket between bar ends annotated "3.0× = 副本数并行度". Below: three small server icons with a single player icon fanning out arrows to all three (isometric), labeled "任意副本可写". Chart grid faintly behind.

// LAYOUT
Layout: chart-focus
Headline top, bar chart center occupying 50%, fan-out schematic bottom.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 演示二:热点玩家,三台机器一起记账
- 单点串行 142ms vs 三机并行 47ms
- 对照组:同一个玩家的所有写入都压到一台机器(锁+落盘串行)
- 实验组:同一批写入随机分散到三台 —— 因为任何副本都能收写
- 结果:热点写中位延迟 142.0ms vs 46.8ms,差 3.0 倍 = 副本数
- 两组最终分数完全一致(600 / 600),正确性不受影响


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
