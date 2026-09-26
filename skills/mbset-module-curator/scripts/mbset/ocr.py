"""Stage 0.5 — batch OCR with line-level confidence and coordinates.

Pages are rendered with PyMuPDF (annotations off, so student ink does not pollute
the text) and read by Tesseract in TSV mode, one process per page in parallel.
The result is cached in ``.mbset/ocr/NN.json`` keyed by the source sha256 and the
OCR settings, so a module is OCRed once, in the background, before extraction.

Coordinates are stored in PDF points so the same evidence can be used for
column splitting, marked-answer detection, figure cropping and spot-check sheets.
"""

from __future__ import annotations

import csv
import io
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .common import IMAGE_SUFFIXES, Module, dump_json, load_json, now

DEFAULTS = {"dpi": 300, "psm": 3, "lang": "eng", "rotate": 0}


def _settings(profile: dict[str, Any] | None) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    cfg.update((profile or {}).get("ocr") or {})
    cfg["engine"] = 2          # v2 caches word boxes (margin handwriting is split off later)
    return cfg


def _tesseract_page(png: bytes, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as fh:
        fh.write(png)
        img = fh.name
    try:
        env = dict(os.environ, OMP_THREAD_LIMIT="1")
        out = subprocess.run(
            ["tesseract", img, "stdout", "--psm", str(cfg["psm"]), "-l", cfg["lang"], "tsv"],
            capture_output=True, text=True, env=env, check=False,
        ).stdout
    finally:
        os.unlink(img)
    lines: dict[tuple[int, int, int], dict[str, Any]] = {}
    for row in csv.DictReader(io.StringIO(out), delimiter="\t", quoting=csv.QUOTE_NONE):
        if row.get("level") != "5" or not (row.get("text") or "").strip():
            continue
        key = (int(row["block_num"]), int(row["par_num"]), int(row["line_num"]))
        x, y, w, h = (int(row[k]) for k in ("left", "top", "width", "height"))
        conf = float(row["conf"])
        line = lines.setdefault(key, {"words": [], "bbox": [x, y, x + w, y + h], "confs": [], "boxes": []})
        line["words"].append(row["text"])
        line["boxes"].append([x, x + w, conf])
        b = line["bbox"]
        line["bbox"] = [min(b[0], x), min(b[1], y), max(b[2], x + w), max(b[3], y + h)]
        if conf >= 0:
            line["confs"].append(conf)
    scale = 72.0 / cfg["dpi"]
    result = []
    for key in sorted(lines):
        line = lines[key]
        confs = line["confs"]
        result.append({
            "text": " ".join(line["words"]),
            "bbox": [round(v * scale, 1) for v in line["bbox"]],
            "conf": round(sum(confs) / len(confs) / 100, 3) if confs else 0.0,
            "block": key[0],
            "words": [[t, round(b[0] * scale, 1), round(b[1] * scale, 1), round(b[2] / 100, 2)]
                      for t, b in zip(line["words"], line["boxes"])],
        })
    return result


def _render_pages(path: Path, cfg: dict[str, Any]) -> list[tuple[bytes, float, float]]:
    import fitz

    pages = []
    if path.suffix.lower() in IMAGE_SUFFIXES:
        pix = fitz.Pixmap(str(path))
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        # images are treated as pages at `dpi` so bboxes stay in "points"
        pages.append((pix.tobytes("png"), pix.width * 72 / cfg["dpi"], pix.height * 72 / cfg["dpi"]))
        return pages
    with fitz.open(path) as doc:
        for page in doc:
            if cfg.get("rotate"):
                page.set_rotation((page.rotation + int(cfg["rotate"])) % 360)
            pix = page.get_pixmap(dpi=cfg["dpi"], annots=False, colorspace=fitz.csGRAY)
            pages.append((pix.tobytes("png"), page.rect.width, page.rect.height))
    return pages


def ocr_source(module: Module, src: dict[str, Any], profile: dict[str, Any] | None = None,
               workers: int = 4, force: bool = False) -> dict[str, Any]:
    cfg = _settings(profile)
    out = module.ocr_path(src)
    cached = load_json(out)
    if cached and not force and cached.get("sha256") == src["sha256"] and cached.get("settings") == cfg:
        return cached
    rendered = _render_pages(module.source_path(src), cfg)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        texts = list(pool.map(lambda item: _tesseract_page(item[0], cfg), rendered))
    pages = []
    for (_, width, height), lines in zip(rendered, texts):
        confs = [ln["conf"] for ln in lines if ln["text"].strip()]
        pages.append({
            "width": round(width, 1), "height": round(height, 1), "lines": lines,
            "mean_conf": round(sum(confs) / len(confs), 3) if confs else 0.0,
            "low_lines": sum(1 for c in confs if c < 0.70),
        })
    data = {"sha256": src["sha256"], "settings": cfg, "created": now(), "pages": pages}
    dump_json(out, data)
    return data


def needs_ocr(src: dict[str, Any]) -> bool:
    return src.get("kind") == "image" or (src.get("kind") == "pdf" and not src.get("triage", {}).get("has_text"))


def run(module: Module, state: dict[str, Any], selector: str | None, jobs: int, workers: int,
        force: bool, include_text: bool) -> int:
    from .profiles import load_profile

    todo = [s for s in module.sources(state, selector)
            if s.get("status") != "excluded" and (include_text or needs_ocr(s)
                                                   or (load_profile(module, s) or {}).get("text") == "ocr")]
    if not todo:
        print("[=] nothing needs OCR")
        return 0
    print(f"[*] OCR {len(todo)} source(s): {jobs} file(s) at a time × {workers} page worker(s)")

    def one(src: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None, str | None]:
        try:
            return src, ocr_source(module, src, load_profile(module, src), workers, force), None
        except Exception as exc:  # keep going; failures are recorded, never hidden
            return src, None, f"{type(exc).__name__}: {exc}"

    failed = 0
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for src, data, err in pool.map(one, todo):
            if err:
                failed += 1
                src.setdefault("stages", {})["ocr"] = {"status": "failed", "error": err, "at": now()}
                print(f"[-] {src['nn']} {src['rel']}: {err}")
                continue
            low = [i + 1 for i, p in enumerate(data["pages"]) if p["mean_conf"] < 0.80 or p["low_lines"] >= 5]
            src.setdefault("stages", {})["ocr"] = {
                "status": "done", "at": now(), "pages": len(data["pages"]), "review_pages": low,
                "mean_conf": round(sum(p["mean_conf"] for p in data["pages"]) / max(len(data["pages"]), 1), 3),
            }
            flag = f"  review pages {low}" if low else ""
            print(f"[+] {src['nn']} {Path(src['rel']).name}: {len(data['pages'])} page(s), "
                  f"mean conf {src['stages']['ocr']['mean_conf']}{flag}")
            module.save(state)
    module.save(state)
    return 1 if failed else 0
