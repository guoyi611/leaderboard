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
Slide 13 — Filename: 13-slide-quorum.png — Type: Content

NARRATIVE GOAL:
理论第一讲:quorum 的鸽笼原理,数字不是调参而是推导。

KEY CONTENT:
Headline: quorum:鸽笼原理买到的保证
Sub-headline: N=3, 写 W=2, 读 R=2
Body:
- W + R = 4 > 3:任意"写够 2 台"与"读够 2 台"必有交集 —— 读至少碰到一台见过新数据的机器
- 我们的 quorum 读没做读修复,所以是"大幅降低旧值概率",不是绝对不读旧
- 把 W 从 2 改成 1:交集不再保证,"写成功了却读不到"变成合法行为

VISUAL:
Blueprint pigeonhole diagram: three server boxes in a row; a blue bracket spanning servers 1-2 labeled "写多数派 W=2" (one small card inserted into both 1 and 2); a navy bracket spanning servers 2-3 labeled "读多数派 R=2" (a magnifier over both); the overlap server 2 highlighted with Light Blue fill and a callout "必有交集". Equation annotation at top drawn as stamped characters: "W+R=4 > 3". A crossed-out variant below: W=1 bracket only over server 1, with Amber warning "无交集保证".

// LAYOUT
Layout: diagram-with-counterexample
Headline top, main pigeonhole diagram center, small counterexample strip bottom.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- quorum:鸽笼原理买到的保证
- N=3, 写 W=2, 读 R=2
- W + R = 4 > 3:任意"写够 2 台"与"读够 2 台"必有交集 —— 读至少碰到一台见过新数据的机器
- 我们的 quorum 读没做读修复,所以是"大幅降低旧值概率",不是绝对不读旧
- 把 W 从 2 改成 1:交集不再保证,"写成功了却读不到"变成合法行为


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
