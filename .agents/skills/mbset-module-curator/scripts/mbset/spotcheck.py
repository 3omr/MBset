"""Spot-check sheets: source crop beside the extracted question, for max(5, 10%) samples.

The sample is spread across the file (first, last and evenly between), and
always includes flagged questions first when `--flagged` is given. One PNG per
five questions is written to reports/spotcheck_NN_<k>.png; the agent views the
sheets and records the verdict with `mbset.py review NN --spot "6/6 OK"`.
"""

from __future__ import annotations

import math
import re
import textwrap
from pathlib import Path
from typing import Any

from .common import Module, load_json

FONT_CANDIDATES = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                   "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]


def _font(size: int):
    from PIL import ImageFont

    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def sample(records: list[dict[str, Any]], flagged_first: bool = False, n: int | None = None) -> list[dict[str, Any]]:
    if not records:
        return []
    k = n or max(5, math.ceil(len(records) * 0.10))
    k = min(k, len(records))
    picked: list[dict[str, Any]] = []
    if flagged_first:
        picked = [r for r in records if r["flags"]][: k // 2]
    step = (len(records) - 1) / max(k - 1, 1)
    for j in range(k):
        r = records[round(j * step)]
        if r not in picked:
            picked.append(r)
        if len(picked) >= k:
            break
    return sorted(picked, key=lambda r: r["i"])


def _md_blocks(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^### Q(\d+):\s*(.*?)(?=^### Q\d+:|\Z)", text, re.S | re.M):
        body = m.group(0).split("\n---")[0]
        stem = m.group(2).splitlines()[0].strip()
        out[stem] = body
    return out


def _panel_text(block: str) -> list[str]:
    lines = []
    for raw in block.splitlines():
        raw = raw.replace("**", "").strip()
        if not raw or raw.startswith("Source Pages"):
            continue
        raw = re.sub(r"^### ", "", raw)
        lines += textwrap.wrap(raw, 62) or [""]
    return lines[:28]


def render(module: Module, src: dict[str, Any], flagged_first: bool = False, n: int | None = None) -> list[Path]:
    import fitz
    from PIL import Image, ImageDraw

    parsed = load_json(module.parsed_path(src))
    if not parsed:
        raise SystemExit(f"[-] {src['nn']}: parse it first")
    records = parsed["questions"]
    picks = sample(records, flagged_first, n)
    blocks = _md_blocks(module.md_path(src)) if module.md_path(src).exists() else {}
    path = module.source_path(src)
    is_pdf = path.suffix.lower() == ".pdf"
    doc = fitz.open(path) if is_pdf else None
    font = _font(15)
    outs: list[Path] = []
    try:
        for chunk_no in range(0, len(picks), 5):
            chunk = picks[chunk_no:chunk_no + 5]
            rows = []
            for r in chunk:
                left = None
                if doc is not None and r.get("bbox"):
                    page = doc[r["page"]]
                    x0, y0, x1, y1 = r["bbox"]
                    rect = fitz.Rect(max(x0 - 12, 0), max(y0 - 6, 0), min(max(x1, x0 + 250) + 12, page.rect.width),
                                     min(max(y1, y0 + 60) + 10, page.rect.height))
                    pix = page.get_pixmap(dpi=110, clip=rect, annots=True)
                    left = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    if left.width > 620:
                        left = left.resize((620, int(left.height * 620 / left.width)))
                block = blocks.get(r["stem"]) or f"(not found in markdown) Q{r['i']}: {r['stem']}"
                text_lines = [f"[parsed #{r['i']} · source no. {r['number']} · page {r['page'] + 1}"
                              f"{' · ' + ','.join(r['flags']) if r['flags'] else ''}]"] + _panel_text(block)
                h_text = 20 * len(text_lines) + 10
                h = max(left.height if left else 0, h_text) + 16
                row = Image.new("RGB", (1300, h), "white")
                if left:
                    row.paste(left, (8, 8))
                d = ImageDraw.Draw(row)
                for j, t in enumerate(text_lines):
                    d.text((650, 8 + 20 * j), t, fill="darkred" if j == 0 else "black", font=font)
                d.line([(0, h - 1), (1300, h - 1)], fill="grey")
                rows.append(row)
            sheet = Image.new("RGB", (1300, sum(r.height for r in rows)), "white")
            y = 0
            for row in rows:
                sheet.paste(row, (0, y))
                y += row.height
            out = module.meta / "reports" / f"spotcheck_{src['nn']}_{chunk_no // 5 + 1}.png"
            sheet.save(out)
            outs.append(out)
    finally:
        if doc is not None:
            doc.close()
    return outs


def _crop(doc, r: dict[str, Any], dpi: int = 120, width: int = 900):
    """The whole question (stem → last option) from the source page, marks included."""
    import fitz
    from PIL import Image

    page = doc[r["page"]]
    x0, y0, x1, y1 = r["bbox"]
    opts = [o for o in r.get("options", []) if o.get("page") == r["page"] and o.get("bbox")]
    if opts:
        y1 = max(y1, max(o["bbox"][3] for o in opts))
        x1 = max(x1, max(o["bbox"][2] for o in opts))
        x0 = min(x0, min(o["bbox"][0] for o in opts))
    rect = fitz.Rect(max(x0 - 30, 0), max(y0 - 6, 0), min(max(x1, x0 + 300) + 30, page.rect.width),
                     min(max(y1, y0 + 60) + 8, page.rect.height))
    pix = page.get_pixmap(dpi=dpi, clip=rect, annots=True)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if img.width > width:
        img = img.resize((width, int(img.height * width / img.width)))
    return img


def answer_sheets(module: Module, src: dict[str, Any], wanted: list[int] | None = None,
                  per: int = 6) -> tuple[list[Path], list[int]]:
    """One PNG per `per` questions, each crop labelled with its markdown Q number and option letters.

    The agent reads the marks on the sheet and answers in one call:
    `mbset.py fix <module> NN --answers "3=B 4=D …" --source marked`.
    """
    import fitz
    from PIL import Image, ImageDraw

    from .writer import md_numbers_by_stem

    parsed = load_json(module.parsed_path(src))
    path = module.source_path(src)
    if not parsed or path.suffix.lower() != ".pdf":
        return [], []
    md = module.md_path(src)
    by_stem = md_numbers_by_stem(md) if md.exists() else {}
    text = md.read_text(encoding="utf-8") if md.exists() else ""
    unanswered = {int(n) for n in re.findall(r"^### Q(\d+):(?:(?!^### Q).)*?^\*\*Correct Answer:\*\* \?", text, re.S | re.M)}
    picks = []
    for r in parsed["questions"]:
        n = by_stem.get(r["stem"])
        if n is None or r["type"] != "QCS" or not r.get("bbox"):
            continue
        if (wanted and n in wanted) or (not wanted and n in unanswered):
            picks.append((n, r))
    font = _font(18)
    outs: list[Path] = []
    doc = fitz.open(path)
    try:
        for k in range(0, len(picks), per):
            rows = []
            for n, r in picks[k:k + per]:
                img = _crop(doc, r)
                label = f"Q{n}  ({len(r['options'])} options, p{r['page'] + 1})"
                row = Image.new("RGB", (920, img.height + 34), "white")
                ImageDraw.Draw(row).text((8, 6), label, fill="darkred", font=font)
                row.paste(img, (10, 30))
                ImageDraw.Draw(row).line([(0, row.height - 1), (920, row.height - 1)], fill="grey", width=2)
                rows.append(row)
            sheet = Image.new("RGB", (920, sum(x.height for x in rows)), "white")
            y = 0
            for row in rows:
                sheet.paste(row, (0, y))
                y += row.height
            out = module.meta / "reports" / f"answers_{src['nn']}_{k // per + 1}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            sheet.save(out)
            outs.append(out)
    finally:
        doc.close()
    return outs, [n for n, _ in picks]
