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
# optional profile keys (only stored in the cache key when set, so old caches stay valid):
#   ocr.split: 2        two book pages per scan: cut at the gutter (found automatically) and OCR each half
#   ocr.threshold: 190  binarize before OCR (0-255): highlighter / shaded backgrounds hide text from Tesseract
#   ocr.normalize: true divide by the blurred background: phone photos / uneven lighting (Tesseract only)
# `ocr --searchable` also writes an `ocrmypdf --redo-ocr -O 3` PDF per source (.mbset/ocrpdf/NN.pdf); profile
# `text: ocrpdf` parses its text layer, and `transcribe --format pdf` hands it to PDF-reading workers.
#   ocr.tool: paddle    PaddleOCR instead of Tesseract (photos, curved pages, bold headings); needs the
#                       PaddleOCR venv (`.venv-smart-ocr` next to the repo root, or $MBSET_PADDLE_PYTHON)


def _settings(profile: dict[str, Any] | None) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    cfg.update((profile or {}).get("ocr") or {})
    cfg["engine"] = 2          # v2 caches word boxes (margin handwriting is split off later)
    return cfg


def _prepare(png: bytes, cfg: dict[str, Any]) -> list[tuple[bytes, int]]:
    """Page image → [(image, x offset in pixels)], one per strip, after optional binarization."""
    split, thr = int(cfg.get("split") or 1), cfg.get("threshold")
    if split <= 1 and not thr and not cfg.get("normalize"):
        return [(png, 0)]
    from PIL import Image, ImageChops, ImageFilter

    img = Image.open(io.BytesIO(png)).convert("L")
    if cfg.get("normalize"):
        bg = img.filter(ImageFilter.GaussianBlur(40))
        img = ImageChops.divide(img, bg)
    if thr:
        img = img.point(lambda v, t=int(thr): 255 if v >= t else 0)
    cuts = [0]
    if split > 1:
        w, h = img.size
        cols = img.resize((w, max(1, h // 8))).load()
        ink = [sum(255 - cols[x, y] for y in range(max(1, h // 8))) for x in range(w)]
        for k in range(1, split):
            lo, hi = int(w * (k / split - 0.12)), int(w * (k / split + 0.12))
            band = 15                       # the gutter is the whitest ~band-px-wide column near the middle
            best = min(range(lo, hi - band), key=lambda x: sum(ink[x:x + band]))
            cuts.append(best + band // 2)
        cuts.append(w)
    else:
        cuts.append(img.size[0])
    out = []
    for a, b in zip(cuts, cuts[1:]):
        buf = io.BytesIO()
        img.crop((a, 0, b, img.size[1])).save(buf, format="PNG")
        out.append((buf.getvalue(), a))
    return out


def _tesseract_page(png: bytes, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for strip, (img, dx) in enumerate(_prepare(png, cfg)):
        # strips are read left to right; block numbers stay distinct so columns never interleave
        for ln in _tesseract_image(img, cfg, dx):
            ln["block"] += 1000 * strip
            result.append(ln)
    return result


def _tesseract_image(png: bytes, cfg: dict[str, Any], dx: int = 0) -> list[dict[str, Any]]:
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
        x += dx
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


def paddle_python() -> str | None:
    """The Python interpreter that has PaddleOCR installed, if any."""
    env = os.getenv("MBSET_PADDLE_PYTHON")
    if env and Path(env).exists():
        return env
    for parent in Path(__file__).resolve().parents:
        cand = parent / ".venv-smart-ocr" / "bin" / "python"
        if cand.exists():
            return str(cand)
    return None


def _paddle_pages(rendered: list[tuple[bytes, float, float]], cfg: dict[str, Any]) -> list[list[dict[str, Any]]]:
    import json

    py = paddle_python()
    if not py:
        raise RuntimeError("ocr.tool: paddle needs the PaddleOCR venv (.venv-smart-ocr) or $MBSET_PADDLE_PYTHON")
    scale = 72.0 / cfg["dpi"]
    with tempfile.TemporaryDirectory() as tmp:
        jobs = []                                           # (page index, strip, x offset, png path)
        for i, (png, _, _) in enumerate(rendered):
            for strip, (img, dx) in enumerate(_prepare(png, cfg)):
                path = Path(tmp) / f"p{i:04d}_{strip}.png"
                path.write_bytes(img)
                jobs.append((i, strip, dx, str(path)))
        worker = Path(__file__).with_name("paddle_worker.py")
        run = subprocess.run([py, str(worker), *[j[3] for j in jobs]], capture_output=True, text=True, check=False)
        if "@@MBSET_JSON@@" not in run.stdout:
            raise RuntimeError(f"paddle worker failed: {(run.stderr or run.stdout)[-400:]}")
        results = json.loads(run.stdout.split("@@MBSET_JSON@@", 1)[1])
    pages: list[list[dict[str, Any]]] = [[] for _ in rendered]
    for (i, strip, dx, _), lines in zip(jobs, results):
        for n, ln in enumerate(lines):
            x0, y0, x1, y1 = ln["box"]
            x0, x1 = x0 + dx, x1 + dx
            words, step = ln["text"].split(), (x1 - x0) / max(len(ln["text"]), 1)
            pos, boxes = 0, []
            for w in words:                                  # no word boxes: spread words over the line
                at = ln["text"].find(w, pos)
                boxes.append([w, round((x0 + at * step) * scale, 1), round((x0 + (at + len(w)) * step) * scale, 1),
                              round(ln["score"], 2)])
                pos = at + len(w)
            pages[i].append({"text": ln["text"], "bbox": [round(v * scale, 1) for v in (x0, y0, x1, y1)],
                             "conf": round(ln["score"], 3), "block": 1000 * strip + n, "words": boxes})
    return pages


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
    if cfg.get("tool") == "paddle":
        texts = _paddle_pages(rendered, cfg)
    else:
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


def searchable_path(module: Module, src: dict[str, Any]) -> Path:
    return module.meta / "ocrpdf" / f"{src['nn']}.pdf"


def searchable_pdf(module: Module, src: dict[str, Any], profile: dict[str, Any] | None = None,
                   jobs: int = 4, force: bool = False) -> Path:
    """`ocrmypdf --redo-ocr -O 3` copy of the source: a compact PDF whose text layer is fresh Tesseract OCR
    (existing OCR text is replaced, real digital text kept). Workers that read PDFs (e.g. Gemini) get it for
    transcription — page image and text together, smaller files — and the verbatim check reads its text.
    Cached in .mbset/ocrpdf/NN.pdf by source sha256 + languages."""
    import shutil
    import json as _json

    out = searchable_path(module, src)
    lang = ((profile or {}).get("ocr") or {}).get("lang") or "eng"
    stamp = out.with_suffix(".json")
    key = {"sha256": src.get("sha256"), "lang": lang}
    if out.exists() and not force and stamp.exists() and _json.loads(stamp.read_text()) == key:
        return out
    if not shutil.which("ocrmypdf"):
        raise RuntimeError("ocrmypdf is not installed (apt install ocrmypdf / brew install ocrmypdf)")
    out.parent.mkdir(parents=True, exist_ok=True)
    srcpath = module.source_path(src)
    cmd = ["ocrmypdf", "--redo-ocr", "-O", "3", "-l", lang, "--jobs", str(jobs), "--output-type", "pdf",
           "-q", str(srcpath), str(out)]
    if srcpath.suffix.lower() in IMAGE_SUFFIXES:
        cmd[1:2] = ["--image-dpi", "200"]            # a photo has no text to redo; give it a resolution
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode not in (0, 10) or not out.exists():   # 10 = PDF/A conversion warning, output is fine
        raise RuntimeError(f"ocrmypdf failed ({r.returncode}): {(r.stderr or r.stdout).strip()[-300:]}")
    stamp.write_text(_json.dumps(key))
    return out


def needs_ocr(src: dict[str, Any]) -> bool:
    return src.get("kind") == "image" or (src.get("kind") == "pdf" and not src.get("triage", {}).get("has_text"))


def run(module: Module, state: dict[str, Any], selector: str | None, jobs: int, workers: int,
        force: bool, include_text: bool, searchable: bool = False) -> int:
    from .profiles import load_profile

    todo = [s for s in module.sources(state, selector)
            if s.get("status") != "excluded" and (include_text or needs_ocr(s)
                                                   or (load_profile(module, s) or {}).get("text") in ("ocr", "best"))]
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
            if searchable and module.source_path(src).suffix.lower() in (".pdf", *IMAGE_SUFFIXES):
                try:
                    print(f"    searchable PDF: {searchable_pdf(module, src, load_profile(module, src), workers, force)}")
                except RuntimeError as exc:
                    print(f"[-] {src['nn']} searchable PDF: {exc}")
            module.save(state)
    module.save(state)
    return 1 if failed else 0
