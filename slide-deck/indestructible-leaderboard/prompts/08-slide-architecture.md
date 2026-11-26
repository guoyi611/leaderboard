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
Slide 8 — Filename: 08-slide-architecture.png — Type: Content

NARRATIVE GOAL:
给出系统总蓝图:三副本 + 可控网络代理 + 实时演示台。

KEY CONTENT:
Headline: 系统蓝图:三副本 + 可控网络
Sub-headline: 所有流量经过代理 —— 那是我们安插的"故障开关"
Body:
- 三个存储节点:各存一份完整数据,先写日志再确认
- 每秒互相推送数据(gossip),自动追平差异
- 网络代理:可按指令注入延迟、乱序、重复、分区、吞响应
- 可视化演示台:浏览器实时看到数据流动与故障效果

VISUAL:
Full engineering blueprint of the system in isometric projection: three server boxes (node1/2/3) arranged in triangle, each box drawn as transparent schematic showing a tiny stack of event cards inside; a central rectangular proxy box labeled "net-proxy 故障注入"; all inter-node lines routed through the proxy with strict 90-degree angles, each line labeled (延迟/重复/分区). A laptop icon on the far left connected to proxy labeled "演示台 :9000/ui". Dimension annotations: "副本 ×3", "全量推送 1s".

// LAYOUT
Layout: full-diagram
Headline top-left, large isometric blueprint center-right, legend column on left edge.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 系统蓝图:三副本 + 可控网络
- 所有流量经过代理 —— 那是我们安插的"故障开关"
- 三个存储节点:各存一份完整数据,先写日志再确认
- 每秒互相推送数据(gossip),自动追平差异
- 网络代理:可按指令注入延迟、乱序、重复、分区、吞响应
- 可视化演示台:浏览器实时看到数据流动与故障效果


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
