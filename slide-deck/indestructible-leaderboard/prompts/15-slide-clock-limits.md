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
Slide 15 — Filename: 15-slide-clock-limits.png — Type: Content

NARRATIVE GOAL:
理论第三讲 + 诚实的局限清单:时钟为什么不能当裁判,系统还有哪些没做好。

KEY CONTENT:
Headline: 时钟不能当裁判 · 局限如实交代
Sub-headline: 现场反例 + 改进方向
Body:
- 反例:把 node3 的时钟拨慢一分钟,再写入新值 —— 它的时间戳像"来自过去",会被旧值覆盖,更新无声丢失
- 对策:合并根本不读时间戳;因果交给逻辑时钟;物理钟只用于人看的日志
- 局限→改进:全量推送→差量检测;无读修复→读时补新;存储×3→冷热分层;简化两阶段→生产用共识协议;无认证→签名
- 前两项只影响收敛速度,不影响正确性

VISUAL:
Left half: blueprint clock diagram — two clock faces, left one normal, right one with hands rotated backward labeled "-60s", below them a mini timeline where a newer event card (v4) is overridden by older card (v3), the override marked with Amber "丢失" stamp. Right half: a to-improve checklist table in thin linework, rows [局限 | 改进] with small right-arrows between cells, footer note strip in Light Blue.

// LAYOUT
Layout: split-two-topics
Headline spanning top, clock diagram left 50%, checklist right 50%, footnote bottom.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 时钟不能当裁判 · 局限如实交代
- 现场反例 + 改进方向
- 反例:把 node3 的时钟拨慢一分钟,再写入新值 —— 它的时间戳像"来自过去",会被旧值覆盖,更新无声丢失
- 对策:合并根本不读时间戳;因果交给逻辑时钟;物理钟只用于人看的日志
- 局限→改进:全量推送→差量检测;无读修复→读时补新;存储×3→冷热分层;简化两阶段→生产用共识协议;无认证→签名
- 前两项只影响收敛速度,不影响正确性


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
