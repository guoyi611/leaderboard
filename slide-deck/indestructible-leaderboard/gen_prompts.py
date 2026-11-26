"""Step 5: 从 outline.md 生成 17 个 prompt 文件(prompts/NN-slide-*.md)。

注入实测经验(wan2.7-image):
- 每页给出"允许出现的全部文字"白名单,页面上不得出现任何其他文字
- 中文文本必须逐字精确渲染
- 禁止装饰性小字/伪文字
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUTLINE = os.path.join(HERE, "outline.md")
PROMPTS = os.path.join(HERE, "prompts")
os.makedirs(PROMPTS, exist_ok=True)

text = open(OUTLINE, encoding="utf-8").read()

style = re.search(r"<STYLE_INSTRUCTIONS>(.*?)</STYLE_INSTRUCTIONS>", text, re.S).group(1).strip()

blocks = re.split(r"\n## Slide (\d+) of 17\n", text)
slides = []
for i in range(1, len(blocks), 2):
    slides.append((int(blocks[i]), blocks[i + 1]))

BASE = """Create a presentation slide image following these guidelines:

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
{style}

## SLIDE CONTENT
{content}

Generate the slide image now with the DashScope image model. Output 16:9 landscape PNG.
"""


def extract(block):
    """提取 slide 块的关键内容,并构建 ALLOWED TEXT 白名单。"""
    lines = block.strip().split("\n")
    fname = next(l for l in lines if l.startswith("**Filename**:")).split(":")[1].strip()
    typ = next(l for l in lines if l.startswith("**Type**:")).split(":")[1].strip()
    goal = ""
    content_start = block.find("// KEY CONTENT")
    vis_start = block.find("// VISUAL")
    key = block[content_start:vis_start].strip()
    vis = block[vis_start:block.find("// LAYOUT")].strip()
    layout = block[block.find("// LAYOUT"):].strip()
    # allowed text: 抓 KEY CONTENT 里所有中文字符串(引号外正文行也含英文混排,取含中文的行)
    allowed = []
    for line in key.split("\n"):
        l = line.strip()
        if re.search(r"[\u4e00-\u9fff]", l) and not l.startswith("//"):
            l = re.sub(r"^-\s*", "", l)
            # 去掉 markdown 标记行名
            if l.startswith("Headline:") or l.startswith("Sub-headline:"):
                l = l.split(":", 1)[1].strip()
            if l.startswith("Body"):
                continue
            allowed.append(l)
    allow_block = "\n".join(f"- {a}" for a in allowed)
    body_lines = re.findall(r"^-\s*(.+)$", key, re.M)
    body_block = "\n".join(f"- {b}" for b in body_lines)
    headline = ""
    sub = ""
    for line in key.split("\n"):
        if line.startswith("Headline:"):
            headline = line.split(":", 1)[1].strip()
        if line.startswith("Sub-headline:"):
            sub = line.split(":", 1)[1].strip()
    content = f"""Slide {num} — Filename: {fname} — Type: {typ}

NARRATIVE GOAL:
{block[block.find('// NARRATIVE GOAL'):content_start].split(chr(10),1)[1].strip()}

KEY CONTENT:
Headline: {headline}
Sub-headline: {sub}
Body:
{body_block}

VISUAL:
{vis.split(chr(10),1)[1].strip()}

{layout}

## ALLOWED TEXT (render exactly; NOTHING else may appear on the slide)
{allow_block}
"""
    return fname, content


for num, block in slides:
    fname, content = extract(block)
    out = BASE.format(style=style, content=content)
    path = os.path.join(PROMPTS, fname.replace(".png", ".md"))
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", os.path.basename(path))

print(f"\n{len(slides)} prompt files generated")
