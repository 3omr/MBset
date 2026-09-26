#!/usr/bin/env python3
"""
MBset Column-Aware PDF Text Extractor
=====================================

`pdftotext -layout` interleaves multi-column exam booklets and silently produces
chimera question stems. This tool detects the column split from the x-positions of
the words on each page and extracts each column with its own crop box, emitting
text in true reading order (page 1 col 1, page 1 col 2, page 2 col 1, ...).

Detection rule (three conditions, all required):
  * the shallowest bin in the middle 40% of the page holds < 25% of the median
    text density (a real gutter),
  * at least 25% of the text mass sits on each side of it (both columns exist),
  * headers (top 10%) and footers (bottom 7%) are excluded, so a centered chapter
    title cannot hide the gutter.

Requires poppler-utils (`pdftotext`, `pdfinfo`). No Python dependencies.

Usage
-----
    python extract_pdf_columns.py src.pdf -o out.txt          # auto-detect
    python extract_pdf_columns.py src.pdf --columns 2         # force 2 columns
    python extract_pdf_columns.py src.pdf --probe             # report detection only
    python extract_pdf_columns.py src.pdf --pages 3-7 -o x.txt
    python extract_pdf_columns.py src.pdf -o x.txt --markers  # keep PAGE/COL markers
"""

import argparse
import re
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET

BINS = 100
MID_LO, MID_HI = 0.30, 0.70      # search the gutter in the middle 40% of the page
GUTTER_RATIO = 0.25              # gutter density vs median text density
SIDE_MASS = 0.25                 # minimum text mass on each side


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout


def bbox_xml(pdf, first, last):
    return run(["pdftotext", "-bbox", "-f", str(first), "-l", str(last), pdf, "-"])


def page_geometry(pdf):
    """(width, height, pages) — from pdfinfo, falling back to the bbox XML."""
    out = run(["pdfinfo", pdf])
    m = re.search(r"Page size:\s*([\d.]+)\s*x\s*([\d.]+)", out)
    p = re.search(r"Pages:\s*(\d+)", out)
    width = float(m.group(1)) if m else None
    height = float(m.group(2)) if m else None
    pages = int(p.group(1)) if p else None
    if width is None or pages is None:
        xml = bbox_xml(pdf, 1, 1)
        try:
            root = ET.fromstring(xml)
            for el in root.iter():
                if el.tag.endswith("page"):
                    width = width or float(el.attrib.get("width", 612))
                    height = height or float(el.attrib.get("height", 792))
                    break
            pages = pages or sum(1 for el in ET.fromstring(bbox_xml(pdf, 1, 10000)).iter()
                                 if el.tag.endswith("page"))
        except ET.ParseError:
            pass
    if not width:
        sys.exit("Could not determine page geometry (is poppler-utils installed?)")
    return width, height or 792.0, pages or 1


def x_histogram(pdf, width, height, first, last):
    """Word-density histogram across the page width, headers/footers excluded."""
    try:
        root = ET.fromstring(bbox_xml(pdf, first, last))
    except ET.ParseError:
        return [0] * BINS, width / BINS
    step = width / BINS
    hist = [0] * BINS
    for w in root.iter():
        if not w.tag.endswith("word"):
            continue
        try:
            y0 = float(w.attrib["yMin"])
            x0, x1 = float(w.attrib["xMin"]), float(w.attrib["xMax"])
        except (KeyError, ValueError):
            continue
        if y0 < height * 0.10 or y0 > height * 0.93:     # skip header / footer bands
            continue
        for b in range(max(0, int(x0 / step)), min(BINS - 1, int(x1 / step)) + 1):
            hist[b] += 1
    return hist, step


def detect_split(pdf, width, height, first, last):
    """Return (split_x or None, diagnostics dict)."""
    hist, step = x_histogram(pdf, width, height, first, last)
    total = sum(hist)
    diag = {"words_binned": total}
    if total < 100:
        diag["reason"] = "too little text to judge"
        return None, diag
    mx = max(hist) or 1
    body = [h for h in hist if h > 0.05 * mx]
    median = statistics.median(body) if body else 0
    lo, hi = int(BINS * MID_LO), int(BINS * MID_HI)
    window = hist[lo:hi]
    gmin = min(window)
    gidx = lo + window.index(gmin)
    left = sum(hist[:gidx]) / total
    right = sum(hist[gidx:]) / total
    diag.update({"median_density": median, "gutter_density": gmin,
                 "ratio": round(gmin / median, 3) if median else None,
                 "left_mass": round(left, 2), "right_mass": round(right, 2),
                 "split_x": round(gidx * step, 1)})
    if median and gmin < GUTTER_RATIO * median and left > SIDE_MASS and right > SIDE_MASS:
        return gidx * step, diag
    diag["reason"] = "no qualifying gutter — single column"
    return None, diag


def extract_region(pdf, page, x, y, w, h):
    return run(["pdftotext", "-layout", "-f", str(page), "-l", str(page),
                "-x", str(int(x)), "-y", str(int(y)),
                "-W", str(int(w)), "-H", str(int(h)), pdf, "-"])


def main():
    ap = argparse.ArgumentParser(description="Column-aware PDF text extraction for MBset sources")
    ap.add_argument("pdf")
    ap.add_argument("-o", "--output", help="output .txt (default: stdout)")
    ap.add_argument("--columns", type=int, choices=[1, 2], help="force column count")
    ap.add_argument("--split", type=float, help="force the split x-coordinate in points")
    ap.add_argument("--pages", help="page range, e.g. 3-7 (default: all)")
    ap.add_argument("--probe", action="store_true", help="report detection and exit")
    ap.add_argument("--markers", action="store_true",
                    help="emit ----- PAGE n COL m ----- markers")
    args = ap.parse_args()

    width, height, total = page_geometry(args.pdf)
    first, last = 1, total
    if args.pages:
        m = re.match(r"^(\d+)(?:-(\d+))?$", args.pages)
        if not m:
            sys.exit("--pages must look like 5 or 3-7")
        first = int(m.group(1))
        last = min(int(m.group(2) or m.group(1)), total)

    split, diag = detect_split(args.pdf, width, height, first, min(last, first + 2))
    if args.split:
        split = args.split
    if args.columns == 1:
        split = None
    elif args.columns == 2 and split is None:
        split = width / 2

    if args.probe:
        print(f"pages={total}  page size={width:.0f}x{height:.0f} pts")
        print(f"detection: {diag}")
        print(f"verdict: {'2 columns, split x=%.0f' % split if split else 'single column'}")
        return

    chunks = []
    for p in range(first, last + 1):
        if split:
            for idx, (x, w) in enumerate(((0, split), (split, width - split)), start=1):
                if args.markers:
                    chunks.append(f"\n----- PAGE {p} COL {idx} -----\n")
                chunks.append(extract_region(args.pdf, p, x, 0, w, height))
        else:
            if args.markers:
                chunks.append(f"\n----- PAGE {p} -----\n")
            chunks.append(extract_region(args.pdf, p, 0, 0, width, height))

    text = "".join(chunks)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        mode = f"2 columns (split x={split:.0f})" if split else "single column"
        print(f"[+] {args.pdf}: pages {first}-{last}, {mode} -> {args.output} "
              f"({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
