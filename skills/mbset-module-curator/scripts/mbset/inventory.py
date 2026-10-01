"""Stage 0 — source inventory, dedupe, triage and catalog skeleton.

* expands archives into ``Raw_PDF_Questions/<archive stem>/`` (archives are recorded,
  never silently skipped);
* hashes every source: byte-identical copies become ``EXCLUDED — duplicate of NN``;
  near-duplicates (same opening text) are flagged for a human decision;
* keeps an existing module's NN indices (read from its catalog), assigns new ones
  after the highest, and reports any NN used twice;
* triages each source (text layer, columns, marked styling, key grids, Moodle /
  DocReader / screenshot signatures) and suggests Tag / tagSuggere / Year;
* warns about source-like files elsewhere in the module that are not in
  ``Raw_PDF_Questions``.
"""

from __future__ import annotations

import re
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from .common import (ARABIC, ARCHIVE_SUFFIXES, IMAGE_SUFFIXES, SOURCE_SUFFIXES, SUBJECTS, Module, now,
                     safe_name, sha256)

SKIP_DIRS = {".mbset", "Markdown_Questions", "Images", "OCR_PDF", "OCR_Text", "Lectures", "__pycache__"}

MOODLE = re.compile(r"Select one:|Flag question|Home\s*»\s*My courses|Question \d+\s*(?:Correct|Incorrect|Not answered)|"
                    r"Finish review|Mark [\d.]+ out of", re.I)
DOCREADER = re.compile(r"doc-reader-guide\.com/mcq-quizzes/(\d+)", re.I)
PHONE = re.compile(r"Clear my choice|\b\d{1,2}:\d{2}\s*(?:AM|PM)?\s*[■-◿]|\bLTE\b|\b4G\b|\d{1,3}%\s*$", re.M)
GRID_PAIR = re.compile(r"\b(\d{1,3})\s*[-.:)=]?\s*\(?([A-Ea-e])\)?(?=\s|$|,)")
QNUM = re.compile(r"^\s*(?:Q(?:uestion)?\s*)?\(?(?:\d{1,3}\.\d{1,3}\s+(?=[A-Z(])|\d{1,3}\s*(?:[.)](?!\d)|-(?!\w)|:)\s*\S)", re.M)
OPT = re.compile(r"^\s*[(\[]?([a-eA-E])\s*[.)\-\]:]\s+\S", re.M)
DECLARED = re.compile(r"\b(\d{2,3})\s*(?:MCQs?|questions|Qs)\b", re.I)
FIGURE = re.compile(r"(?i)\b(figure|fig\.|diagram|shown below|this slide|arrow|labell?ed|photomicrograph|"
                    r"following image|picture)\b")


# --------------------------------------------------------------------------- archives
def expand_archives(module: Module, state: dict[str, Any]) -> None:
    known = {a["sha256"] for a in state.get("archives", [])}
    for arc in sorted(p for p in module.raw.rglob("*") if p.suffix.lower() in ARCHIVE_SUFFIXES):
        digest = sha256(arc)
        if digest in known:
            continue
        dest = arc.parent / safe_name(arc.name)
        dest.mkdir(exist_ok=True)
        if arc.suffix.lower() == ".zip":
            with zipfile.ZipFile(arc) as zf:
                zf.extractall(dest)
        elif arc.suffix.lower() == ".rar":
            subprocess.run(["unrar", "x", "-o+", str(arc), str(dest) + "/"], check=True, capture_output=True)
        else:
            subprocess.run(["7z", "x", "-y", f"-o{dest}", str(arc)], check=True, capture_output=True)
        files = [p for p in dest.rglob("*") if p.is_file()]
        state.setdefault("archives", []).append({
            "rel": str(arc.relative_to(module.root)), "sha256": digest, "expanded_to": str(dest.relative_to(module.root)),
            "files": len(files), "at": now(),
        })
        print(f"[+] expanded {arc.name} → {dest.relative_to(module.root)} ({len(files)} files)")


# --------------------------------------------------------------------------- triage
def _pdf_triage(path: Path) -> dict[str, Any]:
    import fitz

    from .document import page_mark_rects

    out: dict[str, Any] = {}
    with fitz.open(path) as doc:
        n = len(doc)
        texts = [doc[i].get_text() for i in range(n)]
        chars = [len(t.strip()) for t in texts]
        words = [len(re.findall(r"[A-Za-z]{3,}", t)) for t in texts]
        bold = spans = colored = 0
        marks = 0
        images = 0
        for page in doc:
            images += len(page.get_images())
            marks += len(page_mark_rects(page))
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for s in line["spans"]:
                        if s["text"].strip():
                            spans += 1
                            bold += bool(s["flags"] & 16 or re.search(r"bold|black|heavy", s["font"], re.I))
                            c = s["color"]
                            r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
                            colored += (max(r, g, b) - min(r, g, b)) > 60
        text_pages = sum(1 for c, w in zip(chars, words) if c > 150 and w > 20)
        out.update(pages=n, chars=sum(chars), text_pages=text_pages,
                   has_text=text_pages >= max(1, int(0.6 * n)), images=images, mark_rects=marks,
                   bold_ratio=round(bold / spans, 2) if spans else 0.0,
                   color_ratio=round(colored / spans, 2) if spans else 0.0)
        joined = "\n".join(texts)
        out["columns"] = _probe_columns(doc) if out["has_text"] else None
        out["text_sample"] = joined[:4000]
        out["tail"] = "\n".join(texts[-2:])[-4000:] if n else ""
    return out


def _probe_columns(doc) -> int:
    from .document import Line, detect_split

    votes = 0
    probed = 0
    for page in list(doc)[:6]:
        lines = []
        for block in page.get_text("dict")["blocks"]:
            for raw in block.get("lines", []):
                text = "".join(s["text"] for s in raw["spans"]).strip()
                if text:
                    lines.append(Line(text=text, bbox=tuple(raw["bbox"])))
        if len(lines) < 8:
            continue
        probed += 1
        votes += detect_split(lines, page.rect.width, page.rect.height) is not None
    return 2 if probed and votes >= max(1, probed // 2) else 1


def _docx_triage(path: Path) -> dict[str, Any]:
    from .document import docx_lines

    lines = docx_lines(path)
    text = "\n".join(ln.text for ln in lines)
    return {"pages": 1, "chars": len(text), "has_text": True, "paragraphs": len(lines),
            "bold_ratio": round(sum(ln.bold > 0.5 for ln in lines) / max(len(lines), 1), 2),
            "highlight_lines": sum("highlight" in ln.marks for ln in lines),
            "color_ratio": round(sum(ln.color > 0.5 for ln in lines) / max(len(lines), 1), 2),
            "text_sample": text[:4000], "tail": text[-4000:]}


def _pptx_triage(path: Path) -> dict[str, Any]:
    from .document import pptx_lines

    lines = pptx_lines(path)
    text = "\n".join(ln.text for ln in lines)
    return {"pages": (max((ln.page for ln in lines), default=-1) + 1), "chars": len(text), "has_text": bool(text),
            "bold_ratio": round(sum(ln.bold > 0.5 for ln in lines) / max(len(lines), 1), 2),
            "color_ratio": round(sum(ln.color > 0.5 for ln in lines) / max(len(lines), 1), 2),
            "text_sample": text[:4000], "tail": text[-4000:]}


def triage(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        t = _pdf_triage(path)
    elif suffix == ".docx":
        t = _docx_triage(path)
    elif suffix == ".pptx":
        t = _pptx_triage(path)
    elif suffix in (".txt", ".md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        t = {"pages": 1, "chars": len(text), "has_text": True, "text_sample": text[:4000], "tail": text[-4000:]}
    else:
        t = {"pages": 1, "chars": 0, "has_text": False}
    sample = t.get("text_sample", "")
    tail = t.get("tail", "")
    t["signals"] = {
        "moodle": len(MOODLE.findall(sample)),
        "docreader_quiz": (DOCREADER.search(sample).group(1) if DOCREADER.search(sample) else None),
        "phone": len(PHONE.findall(sample)),
        "question_numbers": len(QNUM.findall(sample)),
        "option_lines": len(OPT.findall(sample)),
        "grid_pairs_tail": len(GRID_PAIR.findall(tail)),
        "declared_total": _declared(sample),
        "figure_words": len(FIGURE.findall(sample)),
    }
    t["class"] = _classify(path, t)
    t.pop("tail", None)
    t["text_sample"] = sample[:1500]
    return t


def _declared(sample: str) -> int | None:
    for m in DECLARED.finditer(sample[:1500]):
        n = int(m.group(1))
        if 10 <= n <= 400:
            return n
    return None


def _classify(path: Path, t: dict[str, Any]) -> str:
    suffix = path.suffix.lower()
    s = t["signals"]
    if suffix in IMAGE_SUFFIXES:
        return "screenshot"
    if suffix == ".docx":
        return "docx"
    if suffix == ".pptx":
        return "pptx"
    if suffix in (".txt", ".md"):
        return "text"
    if s["docreader_quiz"]:
        return "docreader"
    if s["moodle"] >= 2:
        return "moodle"
    if not t.get("has_text"):
        return "scanned"
    if s["phone"] >= 3:
        return "phone_screenshots"
    return "digital_two_column" if t.get("columns") == 2 else "digital_single"


# --------------------------------------------------------------------------- tags
def suggest_tags(module: Module, rel: str) -> dict[str, Any]:
    """Filename/folder heuristics from the module's taxonomy (`taxonomy.py`; chosen at `mbset.py init`).
    The agent confirms with `mbset.py set`. A year that is not in the filename is never guessed: the tag
    comes without it, `needs_year: True`, and `check` reports it until the year is set; year-free families
    (Assiut Quizzes / Formatives) never need one."""
    from .taxonomy import load, suggest
    tax = getattr(module, "taxonomy", None) or load(getattr(module, "university", None))
    return suggest(tax, rel)


# --------------------------------------------------------------------------- catalog import
def existing_indices(module: Module) -> dict[str, str]:
    """source filename → markdown filename, read from an existing catalog."""
    catalog = module.markdown / "00_CATALOG_OF_ALL_FILES.md"
    mapping: dict[str, str] = {}
    if not catalog.exists():
        return mapping
    for line in catalog.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        md = next((c.strip("`* ") for c in cells if c.strip("`* ").endswith(".md")), None)
        src = next((c.strip("`* ") for c in cells
                    if re.search(r"\.(pdf|docx|pptx|txt|jpe?g|png)$", c.strip("`* "), re.I)), None)
        if md and src:
            mapping[Path(src).name] = md
    return mapping


def existing_tags(module: Module) -> dict[str, dict[str, Any]]:
    """Tags a finished module already carries (tag map JSON or catalog)."""
    import json

    found: dict[str, dict[str, Any]] = {}
    for tm in [*module.root.glob("*tag_map*.json"), *(module.meta / "archive").glob("*tag_map*.json"),
               module.meta / "tag_map.json"]:
        if not tm.exists():
            continue
        try:
            for md, meta in json.loads(tm.read_text(encoding="utf-8")).items():
                found[md] = {"tag": meta.get("Tag"), "tagSuggere": meta.get("tagSuggere"), "year": meta.get("Year"),
                             "confidence": "existing", "confirmed": True}
        except Exception:
            pass
    return found


# --------------------------------------------------------------------------- main
def discover(module: Module) -> list[Path]:
    files = []
    for p in sorted(module.raw.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(module.root).parts):
            continue
        if p.suffix.lower() in SOURCE_SUFFIXES:
            files.append(p)
    return files


def stray_sources(module: Module, known_hashes: set[str]) -> list[str]:
    stray = []
    for p in module.root.rglob("*"):
        rel = p.relative_to(module.root)
        if not p.is_file() or rel.parts[0] in ("Raw_PDF_Questions", ".mbset", "Lectures", "Images"):
            continue
        if any(part.startswith("Lecture") or part in SKIP_DIRS for part in rel.parts):
            continue
        if p.suffix.lower() in (".pdf", ".docx", ".pptx") and sha256(p) not in known_hashes:
            stray.append(str(rel))
    return stray


def run(module: Module, near_threshold: float = 0.95) -> dict[str, Any]:
    from rapidfuzz import fuzz

    if not module.raw.is_dir():
        raise SystemExit(f"[-] {module.raw} does not exist — put every source there first")
    state = module.load()
    expand_archives(module, state)
    by_rel = {s["rel"]: s for s in state["sources"]}
    catalog_map = existing_indices(module)
    tags = existing_tags(module)
    used = {s["nn"] for s in state["sources"]}
    for md in catalog_map.values():
        m = re.match(r"(\d+)_", md)
        if m:
            used.add(f"{int(m.group(1)):02d}")
    next_nn = max((int(n) for n in used), default=0) + 1

    files = discover(module)
    seen_hash: dict[str, dict[str, Any]] = {}
    for path in files:
        rel = str(path.relative_to(module.root))
        digest = sha256(path)
        src = by_rel.get(rel)
        if src and src.get("sha256") == digest and src.get("triage"):
            seen_hash.setdefault(digest, src)
            continue
        if src is None:
            md = catalog_map.get(path.name)
            if md:
                nn = f"{int(md.split('_', 1)[0]):02d}"
            else:
                nn = f"{next_nn:02d}"
                next_nn += 1
                md = f"{nn}_{safe_name(path.name)}.md"
            src = {"nn": nn, "rel": rel, "md": md, "status": "pending", "stages": {}, "added": now()}
            state["sources"].append(src)
            by_rel[rel] = src
        suffix = path.suffix.lower()
        src.update(sha256=digest, size=path.stat().st_size,
                   kind="pdf" if suffix == ".pdf" else "image" if suffix in IMAGE_SUFFIXES else suffix.lstrip("."))
        print(f"[*] triage {src['nn']} {path.name}")
        try:
            src["triage"] = triage(path)
        except Exception as exc:
            src["triage"] = {"error": f"{type(exc).__name__}: {exc}", "class": "unreadable", "has_text": False}
        src["pages"] = src["triage"].get("pages")
        if not src.get("tags"):
            src["tags"] = tags.get(src["md"]) or suggest_tags(module, rel)
        if digest in seen_hash and seen_hash[digest] is not src:
            first = seen_hash[digest]
            src["status"] = "excluded"
            src["exclusion"] = f"duplicate of {first['nn']} ({Path(first['rel']).name})"
        seen_hash.setdefault(digest, src)

    present = {str(p.relative_to(module.root)) for p in files}
    for src in state["sources"]:
        if src["rel"] not in present and src.get("status") != "missing":
            src["status"] = "missing"
            print(f"[!] {src['nn']} {src['rel']} is in the state but no longer on disk")

    # near-duplicates: same opening text under different names
    live = [s for s in state["sources"] if s.get("status") != "excluded" and s.get("triage", {}).get("text_sample")]
    near = []
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            ta, tb = a["triage"]["text_sample"][:1200], b["triage"]["text_sample"][:1200]
            if len(ta) > 300 and len(tb) > 300 and fuzz.ratio(ta, tb) / 100 >= near_threshold:
                near.append([a["nn"], b["nn"]])
    state["near_duplicates"] = near

    nn_count: dict[str, int] = {}
    for s in state["sources"]:
        nn_count[s["nn"]] = nn_count.get(s["nn"], 0) + 1
    state["duplicate_nn"] = sorted(n for n, c in nn_count.items() if c > 1)
    md_names = {}
    for p in module.markdown.glob("*.md") if module.markdown.exists() else []:
        m = re.match(r"(\d+)_", p.name)
        if m and not p.name.startswith("00_"):
            md_names.setdefault(f"{int(m.group(1)):02d}", []).append(p.name)
    state["duplicate_md_prefix"] = {k: v for k, v in md_names.items() if len(v) > 1}
    state["stray_sources"] = stray_sources(module, {s["sha256"] for s in state["sources"] if s.get("sha256")})
    state["inventory_at"] = now()
    state["sources"].sort(key=lambda s: s["nn"])
    module.save(state)
    return state


def summary(state: dict[str, Any]) -> str:
    rows = state["sources"]
    by_class: dict[str, int] = {}
    for s in rows:
        by_class[s.get("triage", {}).get("class", "?")] = by_class.get(s.get("triage", {}).get("class", "?"), 0) + 1
    lines = [f"sources: {len(rows)}  " + "  ".join(f"{k}={v}" for k, v in sorted(by_class.items()))]
    dups = [s for s in rows if (s.get("exclusion") or "").startswith("duplicate")]
    if dups:
        lines.append(f"byte-identical duplicates auto-excluded: {len(dups)}")
        lines += [f"  {s['nn']} {Path(s['rel']).name} — {s['exclusion']}" for s in dups]
    if state.get("near_duplicates"):
        lines.append(f"near-duplicates to decide: {state['near_duplicates']}")
    if state.get("duplicate_nn"):
        lines.append(f"[!] NN used by more than one source: {state['duplicate_nn']}")
    if state.get("duplicate_md_prefix"):
        lines.append(f"[!] markdown files sharing an NN prefix: {state['duplicate_md_prefix']}")
    if state.get("stray_sources"):
        lines.append(f"[!] {len(state['stray_sources'])} source-like file(s) outside Raw_PDF_Questions and not in it:")
        lines += [f"  {s}" for s in state["stray_sources"][:20]]
    low = [s for s in rows if s.get("tags", {}).get("confidence") == "low"]
    if low:
        lines.append(f"tags needing a decision (confidence low): {', '.join(s['nn'] for s in low)}")
    no_year = [s for s in rows if s.get("tags", {}).get("needs_year") and not s.get("tags", {}).get("confirmed")]
    if no_year:
        lines.append(f"tags without a year (read it from the source, then `set NN --tag … --year …`): "
                     f"{', '.join(s['nn'] for s in no_year)}")
    return "\n".join(lines)
