"""Figure crops for figure-dependent questions + one contact sheet per file.

For each question flagged `figure_dependent` (or listed with --questions):
1. digital pages: the embedded image / vector drawing nearest the question
   (within the question's own vertical band, or just above/below it);
2. scanned pages (the page *is* one image): the question's own region, from its
   first line down to the next question in the same column;
The crop is saved as ``Images/<NN>_Q<n>.png`` at 200 DPI and linked with
``**Image:**`` in the markdown. A contact sheet (reports/figures_NN.png) shows
every crop with its label so the agent verifies all of them in one look.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import Module, dump_json, load_json
from .writer import edit, md_numbers_by_stem


def _question_regions(records: list[dict[str, Any]]) -> dict[int, tuple[int, list[float]]]:
    regions: dict[int, tuple[int, list[float]]] = {}
    for idx, r in enumerate(records):
        if not r.get("bbox"):
            continue
        x0, y0, x1, y1 = r["bbox"]
        nxt = next((n for n in records[idx + 1:] if n.get("bbox") and n["page"] == r["page"]), None)
        bottom = nxt["bbox"][1] - 2 if nxt and nxt["bbox"][1] > y0 else None
        regions[r["i"]] = (r["page"], [x0, y0, x1, bottom if bottom else y1])
    return regions


def crop_for(doc, page_no: int, region: list[float], scanned: bool):
    import fitz

    page = doc[page_no]
    x0, y0, x1, y1 = region
    band = fitz.Rect(0, max(y0 - 260, 0), page.rect.width, min(y1 + 260, page.rect.height))
    if not scanned:
        boxes = [fitz.Rect(info["bbox"]) for info in page.get_image_info()]
        try:
            boxes += [d["rect"] for d in page.get_drawings() if d["rect"].width > 60 and d["rect"].height > 60]
        except Exception:
            pass
        boxes = [b for b in boxes if b.intersects(band) and b.width < page.rect.width * 0.98]
        if boxes:
            qmid = (y0 + y1) / 2
            best = min(boxes, key=lambda b: abs((b.y0 + b.y1) / 2 - qmid))
            return best + (-6, -6, 6, 6)
    col_left = 0 if x0 < page.rect.width / 2 - 20 else page.rect.width / 2
    col_right = page.rect.width if x1 > page.rect.width / 2 + 20 or col_left > 0 else page.rect.width / 2 + 10
    bottom = y1 if y1 > y0 + 30 else min(y0 + 320, page.rect.height)
    return fitz.Rect(col_left, max(y0 - 8, 0), col_right, min(bottom + 8, page.rect.height))


def contact_sheet(items: list[tuple[str, Path]], out: Path, thumb: int = 360) -> Path | None:
    from PIL import Image, ImageDraw

    if not items:
        return None
    cols = 3
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb + 10) + 10, rows * (thumb + 34) + 10), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, path) in enumerate(items):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb, thumb))
        x = 10 + (i % cols) * (thumb + 10)
        y = 10 + (i // cols) * (thumb + 34)
        draw.text((x, y), label, fill="black")
        sheet.paste(img, (x, y + 18))
        draw.rectangle([x - 1, y + 17, x + img.width, y + 18 + img.height], outline="grey")
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def run(module: Module, src: dict[str, Any], questions: list[int] | None = None, link: bool = True) -> dict[str, Any]:
    import fitz

    parsed = load_json(module.parsed_path(src))
    if not parsed:
        raise SystemExit(f"[-] {src['nn']}: parse it first")
    records = parsed["questions"]
    path = module.source_path(src)
    if path.suffix.lower() != ".pdf":
        return {"skipped": "figures are cropped from PDFs only; add images manually"}
    wanted = set(questions or [r["i"] for r in records if "figure_dependent" in r["flags"]])
    if not wanted:
        return {"cropped": 0}
    regions = _question_regions(records)
    scanned = not src.get("triage", {}).get("has_text")
    module.images.mkdir(exist_ok=True)
    items, links = [], {}
    with fitz.open(path) as doc:
        for r in records:
            if r["i"] not in wanted or r["i"] not in regions:
                continue
            page_no, region = regions[r["i"]]
            rect = crop_for(doc, page_no, region, scanned)
            pix = doc[page_no].get_pixmap(dpi=200, clip=rect)
            out = module.images / f"{src['nn']}_Q{r['i']}.png"
            pix.save(out)
            rel = f"Images/{out.name}"
            r["image"] = rel
            links[r["stem"]] = rel
            items.append((f"Q{r['i']} p{page_no + 1}", out))
    sheet = contact_sheet(items, module.meta / "reports" / f"figures_{src['nn']}.png")
    dump_json(module.parsed_path(src), parsed)
    if link and links and module.md_path(src).exists():
        numbers = md_numbers_by_stem(module.md_path(src))
        by_number = {numbers[stem]: img for stem, img in links.items() if stem in numbers}
        missing = [stem[:50] for stem in links if stem not in numbers]
        edit(module.md_path(src), images=by_number)
        if missing:
            print(f"[!] {src['nn']}: {len(missing)} crop(s) not linked (stem edited in markdown): {missing}")
    return {"cropped": len(items), "contact_sheet": str(sheet) if sheet else None}
