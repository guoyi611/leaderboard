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
Slide 12 — Filename: 12-slide-cas-demo.png — Type: Content

NARRATIVE GOAL:
第三个演示高光(全场最有讲头):并发 CAS 在三种条件下三种结局,CAP 的现场交易。

KEY CONTENT:
Headline: 演示三:并发 CAS 的三次审判
Sub-headline: "分数等于 100 才加 10",两个客户端同时执行
Body:
- 健康 + 都发主节点:恰好一个成功 → 110(单点串行,看起来线性)
- 分区 + 本地模式:两个都成功 → 120 ≠ 110(违反线性一致 —— 我们主动演示!)
- 分区 + quorum 模式:恰好一个成功 → 110(要凑 2 票,少数侧自动拒绝)
- 结论:线性性可以买回来,代价是分区期间少数侧不可用 —— 这就是 CAP

VISUAL:
Blueprint tribunal triptych: three framed verdict panels left-to-right; panel 1 shows one green check + one gray cross under "健康 · local", verdict "110 ✓"; panel 2 shows two green checks under "分区 · local" with Amber warning border, verdict "120 ≠ 110"; panel 3 (thicker frame, navy fill header) shows one check + one rejected stamp under "分区 · quorum", verdict "110 ✓". Each panel bottom carries a small scale icon showing what was traded. Connective header line labeled "同一操作,三种条件".

// LAYOUT
Layout: triptych-cards
Headline top, three verdict panels in a row, conclusion strip along bottom in Light Blue fill.

---

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
- 演示三:并发 CAS 的三次审判
- "分数等于 100 才加 10",两个客户端同时执行
- 健康 + 都发主节点:恰好一个成功 → 110(单点串行,看起来线性)
- 分区 + 本地模式:两个都成功 → 120 ≠ 110(违反线性一致 —— 我们主动演示!)
- 分区 + quorum 模式:恰好一个成功 → 110(要凑 2 票,少数侧自动拒绝)
- 结论:线性性可以买回来,代价是分区期间少数侧不可用 —— 这就是 CAP


Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
