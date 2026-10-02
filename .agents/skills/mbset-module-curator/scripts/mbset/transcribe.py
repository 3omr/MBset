"""`mbset.py route` / `transcribe` — the visual route for pages OCR cannot read well.

Scanned exams, phone screenshots and pen-marked pages are where the parse → fix → re-add loop eats the
time: Tesseract garbles the text, the parser splits or loses questions, and a reviewer re-reads the page
anyway. For such pages the page itself is the input:

1. `route` measures every source and every OCR page and says `parse`, `transcribe` (whole file) or
   `transcribe --pages …` (only the bad pages; the rest stays parsed — the cheapest mix).
2. `transcribe --only NN` cuts the pages to read into chunks of a few pages (big files are always split)
   and writes one self-contained brief per chunk. The worker writes **one JSON** with every question as
   printed, its answer with provenance, the model answer of written questions and the shared case text —
   one pass. `--format png` (default) hands page images with each page's OCR text as a draft to correct;
   `--format pdf` a chunk of the `ocrmypdf --redo-ocr -O 3` copy, for workers whose file tool reads PDFs.
3. An answer key printed apart (`--key-pages`) is read once by its own small job (`key.json`), never sent
   with every chunk.
4. `parse --only NN` builds the markdown from the chunk JSONs (plus the parsed pages in a `--pages` mix) with
   the usual gates: numbering gaps, missing chunks, a chunk whose own count disagrees with its questions,
   keys among the options, bias, stems absent from the page text (`transcript_not_in_page_text`), spot check.

    .mbset/transcripts/NN/manifest.json          chunks, pages, status
    .mbset/transcripts/NN/pages/p007.png         page images (--format png)
    .mbset/transcripts/NN/chunk_02.pdf           chunk PDF (--format pdf)
    .mbset/transcripts/NN/chunk_02.brief.txt     worker brief
    .mbset/transcripts/NN/chunk_02.json          worker output
    .mbset/transcripts/NN/key.brief.txt / key.json   answer-key job
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import IMAGE_SUFFIXES, LETTERS, Module, dump_json, load_json, norm_stem, now, review_flags

VALID_SOURCES = {"key", "marked", "online", "derived"}
PAGES_PER_CHUNK = 6
# route thresholds: below this OCR confidence (file or page), or above this share of questions needing
# review, the page itself is cheaper than repairing the OCR text question by question
ROUTE_CONF, ROUTE_REVIEW_SHARE, PAGE_BAD_CONF = 0.80, 0.30, 0.60
MIX_MAX_SHARE = 0.40          # more bad pages than this → transcribe the whole file


def tdir(module: Module, src: dict[str, Any]) -> Path:
    return module.meta / "transcripts" / src["nn"]


# --------------------------------------------------------------------------------------------- route
def _bad_pages(module: Module, src: dict[str, Any]) -> list[int]:
    """1-based pages whose OCR is poor or whose parsed questions mostly need review."""
    bad: set[int] = set()
    data = load_json(module.ocr_path(src))
    if data:
        bad |= {i + 1 for i, p in enumerate(data["pages"]) if (p.get("mean_conf") or 0) < PAGE_BAD_CONF
                and p.get("lines")}
    parsed = load_json(module.parsed_path(src))
    if parsed:
        per: dict[int, list[bool]] = {}
        for r in parsed["questions"]:
            if r.get("page") is not None and "transcribed" not in r.get("flags", []):
                per.setdefault(r["page"] + 1, []).append(bool(review_flags(r["flags"])))
        bad |= {p for p, v in per.items() if len(v) >= 2 and sum(v) / len(v) > 0.5}
    return sorted(bad)


def route(module: Module, src: dict[str, Any]) -> tuple[str, str, list[int]]:
    """('parse' | 'transcribe', why, pages) — pages non-empty: transcribe only those, parse the rest."""
    path = module.source_path(src)
    t = src.get("triage", {})
    total = t.get("pages") or src.get("pages") or 1
    if path.suffix.lower() in (".docx", ".pptx", ".txt", ".md"):
        return "parse", "text document", []
    if path.suffix.lower() in IMAGE_SUFFIXES or t.get("class") in ("screenshot", "phone_screenshots"):
        return "transcribe", "screenshots / photos", []
    parsed = load_json(module.parsed_path(src))
    share = (sum(1 for r in parsed["questions"] if review_flags(r["flags"])) / len(parsed["questions"])
             if parsed and parsed["questions"] else 0.0)
    conf = (src.get("stages", {}).get("ocr") or {}).get("mean_conf")
    if not t.get("has_text") and conf is None:
        return "transcribe", "scanned, no OCR yet (run `ocr` to measure, or transcribe directly)", []
    bad = _bad_pages(module, src)
    whole = (conf is not None and conf < ROUTE_CONF) or share > ROUTE_REVIEW_SHARE
    if whole and (len(bad) > MIX_MAX_SHARE * total or not bad):
        why = (f"OCR confidence {conf:.2f}" if conf is not None and conf < ROUTE_CONF
               else f"{share:.0%} of parsed questions need review")
        return "transcribe", why, []
    if bad:
        return "transcribe", f"{len(bad)}/{total} page(s) need reading; the rest parses well", bad
    return "parse", ("text layer" if t.get("has_text") else f"scanned, OCR confidence {conf:.2f}"), []


# ---------------------------------------------------------------------------------------- prepare
def _page_count(module: Module, src: dict[str, Any]) -> int:
    path = module.source_path(src)
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return 1
    import fitz
    with fitz.open(path) as doc:
        return len(doc)


def render_pages(module: Module, src: dict[str, Any], pages: list[int], dpi: int = 150) -> None:
    """Page images (1-based `pages`) for PNG workers, cached; image sources copied as PNG."""
    out_dir = tdir(module, src) / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = module.source_path(src)
    if path.suffix.lower() in IMAGE_SUFFIXES:
        from PIL import Image
        out = out_dir / "p001.png"
        if not out.exists():
            Image.open(path).convert("RGB").save(out)
        return
    import fitz

    from .ocr import searchable_path
    text_src = searchable_path(module, src)
    text_src = text_src if text_src.exists() else (path if src.get("triage", {}).get("has_text") else None)
    ocr = None if text_src else load_json(module.ocr_path(src))
    with fitz.open(path) as doc:
        tdoc = fitz.open(text_src) if text_src else None
        for p in pages:
            out = out_dir / f"p{p:03d}.png"
            if not out.exists():
                doc[p - 1].get_pixmap(dpi=dpi, annots=True).save(out)
            # the page's machine text beside its image: the worker corrects a draft instead of typing
            txt = out.with_suffix(".txt")
            if not txt.exists():
                if tdoc is not None:
                    body = tdoc[p - 1].get_text()
                elif ocr and p - 1 < len(ocr["pages"]):
                    body = "\n".join(ln["text"] for ln in ocr["pages"][p - 1]["lines"])
                else:
                    body = ""
                if body.strip():
                    txt.write_text(body, encoding="utf-8")
        if tdoc is not None:
            tdoc.close()


def _page_tokens(module: Module, src: dict[str, Any]) -> dict[int, str]:
    """1-based page → raw machine text (ocrmypdf layer, text layer or OCR cache)."""
    from .ocr import searchable_path
    out: dict[int, str] = {}
    path = module.source_path(src)
    text_src = searchable_path(module, src)
    text_src = text_src if text_src.exists() else (path if path.suffix.lower() == ".pdf"
                                                    and src.get("triage", {}).get("has_text") else None)
    if text_src:
        import fitz
        with fitz.open(text_src) as doc:
            for i, page in enumerate(doc):
                out[i + 1] = page.get_text()
    else:
        data = load_json(module.ocr_path(src)) or {"pages": []}
        for i, pg in enumerate(data["pages"]):
            out[i + 1] = "\n".join(ln["text"] for ln in pg["lines"])
    return out


def key_pairs(text: str) -> int:
    """How many question→letter pairs a page's text holds: `12-B` / `12) b` pairs, or a table printed as a
    row of consecutive numbers followed by a row of letters (how answer grids come out of PDFs and OCR)."""
    direct = len(re.findall(r"(?<!\d)\d{1,3}\s*[-.:)=]\s*\(?[A-Ea-e]\)?(?![A-Za-z])", text))
    toks = text.split()
    rows, i = 0, 0
    while i < len(toks):
        j = i
        while j + 1 < len(toks) and toks[j].isdigit() and toks[j + 1].isdigit() and int(toks[j + 1]) == int(toks[j]) + 1:
            j += 1
        n = j - i + 1 if toks[i].isdigit() else 0
        if n >= 5:
            letters = 0
            while j + 1 + letters < len(toks) and re.fullmatch(r"[A-Ea-e]\.?", toks[j + 1 + letters]):
                letters += 1
            if letters >= 5:
                rows += min(n, letters)
                i = j + 1 + letters
                continue
        i += 1
    return max(direct, rows)


def detect_key_pages(module: Module, src: dict[str, Any], minimum: int = 10) -> list[int]:
    """Pages that print an answer key (≥ `minimum` pairs) — found from the text, no model involved."""
    return sorted(p for p, t in _page_tokens(module, src).items() if key_pairs(t) >= minimum)


def chunk_pdf(module: Module, src: dict[str, Any], pages: list[int], out: Path) -> None:
    """The chunk's pages (1-based, in order) cut from the `ocrmypdf --redo-ocr -O 3` copy."""
    import fitz

    from .ocr import searchable_pdf
    from .profiles import effective_profile
    base = searchable_pdf(module, src, effective_profile(module, src))
    with fitz.open(base) as doc:
        part = fitz.open()
        for p in pages:
            part.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
        part.save(out, garbage=3, deflate=True)
        part.close()


def page_weights(module: Module, src: dict[str, Any], pages: list[int]) -> dict[int, float]:
    """Relative reading work per page (1.0 = an average page): the amount of machine text, so dense pages of
    questions weigh more than a title page — chunks of equal work finish together."""
    toks = _page_tokens(module, src)
    sizes = {p: len((toks.get(p) or "").split()) for p in pages}
    avg = (sum(sizes.values()) / len(sizes)) if sizes else 0
    conf = {i + 1: pg.get("mean_conf") or 0 for i, pg in enumerate((load_json(module.ocr_path(src)) or {}).get("pages", []))}
    out: dict[int, float] = {}
    for p in pages:
        w = min(2.5, sizes[p] / avg) if avg else 1.0
        if p in conf and conf[p] < 0.80:
            w = max(w, 2.0)          # a photo / weak scan: little machine text, but the slowest page to read (measured)
        elif sizes[p] >= 15:
            w = max(w, 0.8)          # a page with questions is never a light page
        out[p] = max(0.3, w)
    return out


def chunks_by_work(pages: list[int], weights: dict[int, float], per: int) -> list[list[int]]:
    """Consecutive pages grouped so each chunk carries about `per` average pages of work."""
    out: list[list[int]] = []
    load = 0.0
    for p in sorted(set(pages)):
        if out and p == out[-1][-1] + 1 and load + weights.get(p, 1.0) <= per * 1.15:
            out[-1].append(p)
            load += weights.get(p, 1.0)
        else:
            out.append([p])
            load = weights.get(p, 1.0)
    if len(out) > 1 and sum(weights.get(p, 1.0) for p in out[-1]) < per / 3 and out[-1][0] == out[-2][-1] + 1:
        tail = out.pop()
        out[-1] += tail
    return out


def chunks_for(pages: list[int] | int, per: int) -> list[list[int]]:
    """Runs of consecutive 1-based pages cut into chunks of `per`; a tail of one or two pages joins the
    previous chunk of the same run."""
    if isinstance(pages, int):
        pages = list(range(1, pages + 1))
    runs: list[list[int]] = []
    for p in sorted(set(pages)):
        if runs and p == runs[-1][-1] + 1:
            runs[-1].append(p)
        else:
            runs.append([p])
    out: list[list[int]] = []
    for run in runs:
        part = [run[i:i + per] for i in range(0, len(run), per)]
        if len(part) > 1 and len(part[-1]) <= max(1, per // 3):
            tail = part.pop()
            part[-1] = part[-1] + tail
        out += part
    return out


SCHEMA = """{
  "pages": [7, 8, 9, 10, 11, 12],
  "printed_count": 2,
  "questions": [
    {
      "page": 7,
      "number": 12,
      "exam": "Final 2023",
      "case": "",
      "stem": "exactly as printed",
      "options": {"A": "as printed", "B": "...", "C": "...", "D": "..."},
      "answer": "C",
      "answer_source": "marked",
      "model_answer": null,
      "model_answer_source": null,
      "figure": false
    },
    {
      "page": 9,
      "number": 13,
      "exam": "Final 2023",
      "case": "",
      "stem": "Define: ketolysis",
      "options": {},
      "answer": null,
      "answer_source": null,
      "model_answer": "the printed answer, or one written from medical knowledge",
      "model_answer_source": "key",
      "figure": false
    }
  ],
  "skipped_numbers": [],
  "notes": ""
}"""


def _what_to_read(module: Module, src: dict[str, Any], fmt: str, pages: list[int], context: int | None,
                  pdf: Path | None) -> str:
    if fmt == "pdf":
        mapping = ", ".join(f"PDF page {i} = source page {p}" for i, p in enumerate(pages, 1))
        extra = f"; PDF page {len(pages) + 1} = source page {context} (context only)" if context else ""
        return (f"Read this PDF (every page; it has a text layer, but the PAGE IMAGE is what counts):\n  {pdf}\n"
                f"  ({mapping}{extra}). Always write SOURCE page numbers in the JSON.")
    pdir = tdir(module, src) / "pages"
    lines = "\n".join(f"  - page {p}: {pdir / f'p{p:03d}.png'}" for p in pages)
    ctx = f"\n  - page {context} (context only): {pdir / f'p{context:03d}.png'}" if context else ""
    # the OCR text goes inside the brief, not in extra files: every file a worker opens is one more slow step
    drafts = []
    for p in pages + ([context] if context else []):
        txt = pdir / f"p{p:03d}.txt"
        if txt.exists():
            body = re.sub(r"\n{3,}", "\n\n", txt.read_text(encoding="utf-8")).strip()[:5000]
            drafts.append(f"----- page {p}: OCR draft (has errors; the image is the truth) -----\n{body}")
    draft = ("\n\nOCR drafts of the same pages — start from them and correct every word against the image:\n"
             + "\n".join(drafts)) if drafts else ""
    return (f"Read these page images (open every one; zoom into small or pen-marked areas):\n{lines}{ctx}"
            f"{draft}")


def brief(module: Module, src: dict[str, Any], k: int, n_chunks: int, pages: list[int], context: int | None,
          out: Path, fmt: str = "png", pdf: Path | None = None, key_job: bool = False) -> str:
    keep_ar = "kept in Arabic exactly as printed (this source is keep_arabic)" if _keep_arabic(module, src) \
        else "never write Arabic characters; an Arabic-only line that is not part of a question is skipped"
    key_rule = ("   The answer key printed elsewhere in this file is read by a separate job: when your pages print no\n"
                "   answer for a question and show no mark, leave answer and answer_source null (do NOT derive).\n"
                if key_job else
                "   - no key and no mark → answer from medical knowledge, answer_source \"derived\".\n")
    return f"""MBset transcription — {module.name} · source {src['nn']} ({Path(src['rel']).name}) · chunk {k}/{n_chunks}

{_what_to_read(module, src, fmt, pages, context, pdf)}
Your pages: {pages[0]}–{pages[-1]}.

Write ONE file, and nothing else: {out}
(write it as you go, every page or two, so a timeout never loses the work).
Open ONLY the files listed above. Do not open, list or search any other file or folder, do not run
programs or convert files, and ignore any skills or project instructions you find: this brief is complete.

JSON format (UTF-8, valid JSON):
{SCHEMA}

Rules:
1. VERBATIM. Every stem and option is copied exactly as printed — same words, same order, same spelling of
   drug names and numbers. Never shorten, summarise, reword, complete, translate or "improve". Medical
   notation is written properly (Ca²⁺, Na⁺, β1, µm, →). Arabic: {keep_ar}.
2. EVERY question that STARTS on your pages, in page order, none skipped. A question running past your last
   page is finished from the context page. Text at the top of your first page that continues a question from
   the previous page belongs to the previous chunk — skip it. Answer-key grids are not questions. Page
   headers, lecture titles, watermarks, phone status bars, LMS buttons ("Flag question", "Time left",
   "Select one:"), page numbers: never part of a stem.
3. `number`: the printed question number (integer), or null when the source prints none. Do not renumber.
   A number the source itself skips → add it to "skipped_numbers".
4. `case`: a clinical scenario / passage / matching instruction printed ONCE for SEVERAL questions goes in
   `case` of each of those questions (identical text), and their `stem` holds only the sub-question. A
   scenario that belongs to one question only stays inside its `stem`; otherwise `case` is "".
5. MCQ options: letters A, B, C… in printed order (a printed "a)" is "A"; options printed as 1/2/3 become A/B/C);
   at most six (A–F). True/False → options {{"A": "True", "B": "False"}}. Matching items → one question per
   item, each with the full printed list as options (the instruction in `case`). "Select all that apply" /
   several correct → a written question with the printed choices kept in the stem ("a. … b. …") and the
   correct set as model_answer.
6. ANSWER, in the same pass:
   - printed key / "Ans:" line / review "The correct answer is" on your pages → answer_source "key";
   - exactly one option visibly marked (tick, circle, highlight, pen, bold) → "marked";
   - several marks, or a student's in-progress selection that is not a key → treat as no mark;
{key_rule}   The letter must be one of the question's own options. Never copy an answer from another question.
7. WRITTEN questions (no options): model_answer = the printed answer verbatim with model_answer_source "key";
   if none is printed, write a complete, exam-standard model answer from medical knowledge with
   model_answer_source "derived" (keep numbered points as "1. … 2. …").
8. `figure`: true when the stem needs a picture, graph or table on the page to be answered.
   `exam`: the title and year of the exam this question belongs to, as printed in that exam's header (e.g.
   "Final 2023", "MED 2019", "Date: 22/5/2023") — a file can hold several exams; null when none is printed.
9. BEFORE FINISHING, count on the pages (not in your JSON) how many questions start on your pages and write it
   as `printed_count`; if it differs from the number of entries in `questions`, find and fix the difference.
10. Do not run any other command, do not edit markdown or state; the coordinator ingests your JSON.
"""


KEY_SCHEMA = """{"sections": [{"1": "B", "2": "D", "3": "A"}], "notes": ""}"""


def key_brief(module: Module, src: dict[str, Any], key_pages: list[int], out: Path, fmt: str,
              pdf: Path | None) -> str:
    return f"""MBset answer key — {module.name} · source {src['nn']} ({Path(src['rel']).name})

{_what_to_read(module, src, fmt, key_pages, None, pdf)}

These pages hold a printed answer key (they may also hold questions — ignore those). Write ONE file, and
nothing else: {out}
Open ONLY the files listed above; do not run programs.
JSON: {KEY_SCHEMA}
- One object per numbering section, in the order the key prints them (a key that restarts at 1 starts a new
  section); keys are the printed question numbers, values the printed letter (A–F, uppercase).
- Only what is printed: an unreadable or missing entry is left out — never guess.
- Do not run any other command.
"""


def _keep_arabic(module: Module, src: dict[str, Any]) -> bool:
    from .profiles import effective_profile
    return bool(effective_profile(module, src).get("keep_arabic"))


def enable(module: Module, src: dict[str, Any]) -> None:
    """Switch the source's profile to the transcript route (`transcribe: true`)."""
    import yaml

    from .profiles import write_profile
    path = write_profile(module, src)
    text = path.read_text(encoding="utf-8")
    own = yaml.safe_load(text) or {}
    if own.get("transcribe") is True:
        return
    if re.search(r"^transcribe:.*$", text, re.M):
        text = re.sub(r"^transcribe:.*$", "transcribe: true", text, flags=re.M)
    else:
        text = text.rstrip() + "\ntranscribe: true   # questions come from .mbset/transcripts (mbset.py transcribe)\n"
    path.write_text(text, encoding="utf-8")


def prepare(module: Module, src: dict[str, Any], per: int = PAGES_PER_CHUNK, dpi: int = 150,
            key_pages: list[int] | None = None, fmt: str = "png", only_pages: list[int] | None = None
            ) -> dict[str, Any]:
    """Split the pages to read into chunks (stable once made), cut their PDFs or render their images and
    write one brief per chunk (+ the key job). `only_pages`: transcribe these, parse the rest."""
    total = _page_count(module, src)
    d = tdir(module, src)
    d.mkdir(parents=True, exist_ok=True)
    old = load_json(d / "manifest.json") or {}
    if key_pages is None:
        key_pages = old.get("key_pages") if "key_pages" in old and old.get("keys_auto") is False \
            else detect_key_pages(module, src)
        auto = True
    else:
        auto = False
    only = sorted(only_pages) if only_pages is not None else old.get("pages_only")
    # key pages stay in the chunks too: a key table often shares its page with questions
    wanted = list(only or range(1, total + 1))
    same = old.get("chunks") and old.get("pages") == total and old.get("pages_only") == only \
        and old.get("format", "png") == fmt
    chunks = [c["pages"] for c in old["chunks"]] if same else \
        chunks_by_work(wanted, page_weights(module, src, wanted), per)
    manifest = {"nn": src["nn"], "source": src["rel"], "pages": total, "created": old.get("created") or now(),
                "format": fmt, "key_pages": key_pages, "keys_auto": auto, "pages_only": only, "chunks": []}
    if fmt == "png":
        need = {p for c in chunks for p in c} | {c[-1] + 1 for c in chunks if c[-1] < total} | set(key_pages)
        render_pages(module, src, sorted(need), dpi=dpi)
    for k, pages in enumerate(chunks, 1):
        out = d / f"chunk_{k:02d}.json"
        context = pages[-1] + 1 if pages[-1] < total else None
        pdf = None
        if fmt == "pdf":
            pdf = d / f"chunk_{k:02d}.pdf"
            if not pdf.exists() or not same:
                chunk_pdf(module, src, pages + ([context] if context else []), pdf)
        b = d / f"chunk_{k:02d}.brief.txt"
        b.write_text(brief(module, src, k, len(chunks), pages, context, out, fmt, pdf, False),
                     encoding="utf-8")
        manifest["chunks"].append({"k": k, "pages": pages, "brief": str(b), "out": str(out)})
    # one small job per run of key pages; each key is applied to the exam printed before it
    manifest["keys"] = []
    for j, group in enumerate(chunks_for(key_pages, 3) if key_pages else [], 1):
        kpdf = None
        if fmt == "pdf":
            kpdf = d / f"key_{j:02d}.pdf"
            chunk_pdf(module, src, group, kpdf)
        kb = d / f"key_{j:02d}.brief.txt"
        kb.write_text(key_brief(module, src, group, d / f"key_{j:02d}.json", fmt, kpdf), encoding="utf-8")
        manifest["keys"].append({"pages": group, "brief": str(kb), "out": str(d / f"key_{j:02d}.json")})
    dump_json(d / "manifest.json", manifest)
    enable(module, src)
    return manifest


# ----------------------------------------------------------------------------------------- ingest
def _page_texts(module: Module, src: dict[str, Any]) -> dict[int, str]:
    """0-based page → normalized OCR / text-layer text, for the verbatim check."""
    out: dict[int, str] = {}
    data = load_json(module.ocr_path(src))
    if data:
        for pno, pg in enumerate(data["pages"]):
            if (pg.get("mean_conf") or 0) >= 0.6:
                out[pno] = norm_stem(" ".join(ln["text"] for ln in pg["lines"]))
    from .ocr import searchable_path
    path = module.source_path(src)
    for f, ok in ((path, path.suffix.lower() == ".pdf" and src.get("triage", {}).get("has_text")),
                  (searchable_path(module, src), searchable_path(module, src).exists())):
        if not ok:
            continue
        import fitz
        with fitz.open(f) as doc:
            for pno, page in enumerate(doc):
                t = norm_stem(page.get_text())
                if len(t) > 80:
                    out[pno] = (out.get(pno, "") + " " + t).strip()
    return out


def _record(q: dict[str, Any], c: dict[str, Any], keep_ar: bool, texts: dict[int, str], fuzz) -> dict[str, Any]:
    from .parser import _clean_text

    flags = ["transcribed"]
    stem = _clean_text(q.get("stem") or "", stem=True, keep_arabic=keep_ar)
    case = _clean_text(q.get("case") or "", keep_arabic=keep_ar)
    page = int(q.get("page") or c["pages"][0])
    if page not in c["pages"]:
        flags.append("page_outside_chunk")
    opts = {str(L).upper(): (t or "").strip() for L, t in (q.get("options") or {}).items() if (t or "").strip()}
    letters = sorted(opts)
    if letters and letters != list(LETTERS[:len(letters)]):
        flags.append("letters_not_sequential")
    options = [{"letter": L, "text": _clean_text(opts[L], keep_arabic=keep_ar), "bold": 0.0, "color": 0.0,
                "marks": [], "page": page - 1, "bbox": None} for L in letters]
    qtype = "QCS" if len(options) >= 2 else "QROC"
    if len(options) == 1:
        flags.append("single_option")
    correct = (q.get("answer") or "").strip().upper() or None
    source = (q.get("answer_source") or "").strip().lower() or None
    if qtype == "QCS":
        if correct and correct not in letters:
            flags.append("key_letter_not_among_options")
            correct = None
        if source not in VALID_SOURCES or not correct:
            source = None
    else:
        correct, source = None, None
    exp = (q.get("model_answer") or "").strip() if qtype == "QROC" else (q.get("explanation") or "").strip()
    exp_source = ((q.get("model_answer_source") or "").strip().lower() or None) if qtype == "QROC" else None
    if exp_source not in (None, "key", "derived"):
        exp_source = "derived"
    if fuzz and texts.get(page - 1) and len(norm_stem(stem)) > 25:
        if fuzz.partial_ratio(norm_stem(stem)[:80], texts[page - 1]) < 70:
            flags.append("transcript_not_in_page_text")
    from .check import AUDIT
    if q.get("figure") or AUDIT.FIGURE.search(stem):     # the gate's own figure test: no stem slips past
        flags.append("figure_dependent")
    num = q.get("number")
    num = int(num) if isinstance(num, (int, str)) and str(num).strip().isdigit() else None
    exam = str(q.get("exam") or "").strip()
    yr = re.findall(r"(?<!\d)((?:19|20)\d{2})(?!\d)", exam)
    return {"i": 0, "number": num, "section": None, "type": qtype, "stem": stem, "case": case,
            "exam": exam or None, "year": int(yr[-1]) if yr else None,
            "after": "", "exp": exp, "exp_source": exp_source if exp else None, "inline_answer": None,
            "options": options, "flags": flags, "cut_prefix": "", "page": page - 1, "bbox": None,
            "pages": [page - 1], "candidates": {}, "correct": correct, "answer_source": source}


def load(module: Module, src: dict[str, Any], profile: dict[str, Any],
         base: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Records + counters + gaps from the chunk JSONs, in the shape `pipeline.parse_source` writes.
    `base`: parser records of the pages that are not transcribed (a `--pages` mix), merged in page order."""
    d = tdir(module, src)
    manifest = load_json(d / "manifest.json")
    if not manifest:
        raise SystemExit(f"[-] {src['nn']}: profile says transcribe but there is no manifest — "
                         f"run `mbset.py transcribe <Module> --only {src['nn']}`")
    keep_ar = bool(profile.get("keep_arabic"))
    texts = _page_texts(module, src)
    try:
        from rapidfuzz import fuzz
    except ImportError:
        fuzz = None
    trecs: list[dict[str, Any]] = []
    missing: list[str] = []
    mismatch: list[str] = []
    skipped: list[int] = []
    for c in manifest["chunks"]:
        out = Path(c["out"])
        if not out.exists():
            missing.append(f"chunk {c['k']} (pages {c['pages'][0]}-{c['pages'][-1]})")
            continue
        try:
            data = json.loads(out.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            missing.append(f"chunk {c['k']}: invalid JSON ({e})")
            continue
        skipped += [int(x) for x in data.get("skipped_numbers") or [] if str(x).isdigit()]
        qs = data.get("questions") or []
        pc = data.get("printed_count")
        if isinstance(pc, int) and pc != len(qs):
            mismatch.append(f"chunk {c['k']} (pages {c['pages'][0]}-{c['pages'][-1]}): worker counted {pc} on the "
                            f"pages but wrote {len(qs)}")
        trecs += [_record(q, c, keep_ar, texts, fuzz) for q in qs]
    keys = list(manifest.get("keys") or []) + ([dict(manifest["key"], pages=manifest.get("key_pages") or [])]
                                               if manifest.get("key") else [])
    for kj in keys:
        if not Path(kj["out"]).exists():
            missing.append(f"answer-key job (pages {','.join(map(str, kj['pages']))})")
    # merge with the parsed pages (stable: parser order within a page, then transcript order)
    records = sorted([(r["page"], 0, i, r) for i, r in enumerate(base or [])]
                     + [(r["page"], 1, i, r) for i, r in enumerate(trecs)], key=lambda x: x[:3])
    records = [x[3] for x in records]
    for i, r in enumerate(records, 1):
        r["i"] = i
    # numbering: sections restart at 1; gaps not declared as skipped by the source are reported
    sections: list[list[int]] = []
    gaps: list[str] = []
    for r in records:
        n = r["number"]
        if n is None:
            r["section"] = len(sections) - 1 if sections else 0
            continue
        # a restart at 1, a jump back, or a jump forward by more than 4 (the next exam of a compilation,
        # "Part II starts at 31") opens a section — like the parser's counters; a question really lost inside
        # a chunk is caught by the chunk's printed_count instead
        if not sections or (n == 1 and sections[-1][1] >= 2) or n <= sections[-1][1] - 5 \
                or n > sections[-1][1] + 5:
            sections.append([n, n])
        else:
            last = sections[-1][1]
            if n > last + 1:
                hole = [x for x in range(last + 1, n) if x not in skipped]
                if hole:
                    gaps.append(f"{last} → {n} (missing {hole[0]}{'–' + str(hole[-1]) if len(hole) > 1 else ''})")
            elif n <= last:
                r["flags"].append(f"number_repeated_{n}")
            sections[-1][1] = max(last, n)
        r["section"] = len(sections) - 1
    _apply_keys(records, [(min(kj["pages"] or [10 ** 6]), json.loads(Path(kj["out"]).read_text(encoding="utf-8")))
                          for kj in keys if Path(kj["out"]).exists()])
    # the same question printed twice in one source (a compilation repeating an exam, a model-answer copy and
    # a student copy): keep the first, drop the rest with a reason — the counters account for them
    seen: dict[str, int] = {}
    dupes: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    for r in records:
        k = norm_stem((r.get("case") or "") + " " + r["stem"] + " " + " ".join(o["text"] for o in r["options"]))
        if k and k in seen and "transcribed" in r["flags"]:
            dupes.append({"stem": r["stem"][:120], "reason": f"printed twice in the source (p{r['page'] + 1}, "
                                                             f"first on p{seen[k] + 1})"})
            continue
        seen.setdefault(k, r["page"])
        kept.append(r)
    records = kept
    for i, r in enumerate(records, 1):
        r["i"] = i

    numbering = sum(b - a + 1 for a, b in sections) - len([x for x in skipped
                                                           if any(a <= x <= b for a, b in sections)])
    counters = {"source_numbering": numbering, "sections": [f"{a}-{b}" for a, b in sections],
                "option_a_lines": 0, "parsed_questions": len(records),
                "parsed_numbered": sum(1 for r in records if r["number"] is not None),
                "declared_total": profile.get("declared_total"), "missing_chunks": missing,
                "chunk_count_mismatch": mismatch}
    if missing:
        gaps = [f"not transcribed yet: {m}" for m in missing] + gaps
    return {"records": records, "counters": counters, "gaps": gaps, "duplicates": dupes,
            "info": {"method": "transcribe" if not base else "transcribe+parse"}}


def _apply_keys(records: list[dict[str, Any]], keys: list[tuple[int, dict[str, Any]]]) -> None:
    """Apply printed keys (each read by its own job) to the exam each belongs to.

    Keys are taken in page order. A key at page K answers the numbering sections that start after the
    previous key page and before K (the exam printed before its key — a section starting on page K itself
    belongs to the next exam). When those hold less than half of the key's numbers (pages scanned out of
    order), the sections after K up to the next key are added. A key with several sections (a key restarting
    at 1) maps them in page order. The key wins over marks and knowledge (key > marked > derived); a
    disagreement with a visible mark is flagged."""
    starts: dict[int, int] = {}
    for r in records:
        if r.get("section") is not None:
            starts[r["section"]] = min(starts.get(r["section"], 10 ** 6), r["page"] + 1)
    keys = sorted(keys, key=lambda k: k[0])
    used: set[int] = set()
    prev = 0
    for n, (page, key) in enumerate(keys):
        nxt = keys[n + 1][0] if n + 1 < len(keys) else 10 ** 6
        secs = key.get("sections") if isinstance(key.get("sections"), list) else [key.get("key") or {}]
        secs = [{int(k): str(v).strip().upper().rstrip(".") for k, v in (sk or {}).items() if str(k).isdigit()}
                for sk in secs]
        secs = [sk for sk in secs if sk]
        if not secs:
            prev = page
            continue
        nums = set().union(*secs)
        before = sorted((st, idx) for idx, st in starts.items() if prev <= st < page and idx not in used)
        have = {r["number"] for r in records if r.get("section") in {i for _, i in before}}
        cand = before
        if len(nums & have) < 0.5 * len(nums):
            cand = before + sorted((st, idx) for idx, st in starts.items() if page < st < nxt and idx not in used)
        # each key number answers ONE section: the closest to the key — the latest before it, else the earliest
        # after it — so an older exam with the same numbers earlier in the file is left alone
        order = [idx for _, idx in sorted(before, reverse=True)] + [idx for st, idx in cand if st > page]
        secnums = {idx: {r["number"] for r in records if r.get("section") == idx} for idx in order}
        flat = {k: v for sk in secs for k, v in sk.items()}       # several key sections → by number, nearest wins
        target_of: dict[int, int] = {}
        for num in flat:
            hit = next((idx for idx in order if num in secnums[idx]), None)
            if hit is not None:
                target_of[num] = hit
        targets = set(target_of.values())
        for r in records:
            if r["type"] != "QCS" or r["number"] is None or target_of.get(r["number"]) != r.get("section"):
                continue
            letter = flat[r["number"]]
            if letter not in {o["letter"] for o in r["options"]}:
                r["flags"].append("key_letter_not_among_options")
                continue
            if r.get("answer_source") == "marked" and r.get("correct") and r["correct"] != letter:
                r["flags"].append("answer_sources_disagree")
            r["correct"], r["answer_source"] = letter, "key"
        used |= set(targets)
        prev = page


def status(module: Module, src: dict[str, Any]) -> str:
    m = load_json(tdir(module, src) / "manifest.json")
    if not m:
        return f"{src['nn']}: no transcript"
    done = [c for c in m["chunks"] if Path(c["out"]).exists()]
    left = [f"{c['k']}(p{c['pages'][0]}-{c['pages'][-1]})" for c in m["chunks"] if not Path(c["out"]).exists()]
    left += [f"key(p{','.join(map(str, k['pages']))})" for k in m.get("keys") or [] if not Path(k["out"]).exists()]
    scope = f"pages {','.join(map(str, m['pages_only']))} of {m['pages']}" if m.get("pages_only") else f"{m['pages']} pages"
    return (f"{src['nn']}: {len(done)}/{len(m['chunks'])} chunks transcribed, {scope}"
            + (f" — left: {' '.join(left)}" if left else " — ready: `parse --only " + src["nn"] + "`"))


# -------------------------------------------------------------------------------------------- CLI
def _spec(pages: list[int]) -> str:
    runs: list[list[int]] = []
    for p in pages:
        if runs and p == runs[-1][-1] + 1:
            runs[-1].append(p)
        else:
            runs.append([p])
    return ",".join(f"{r[0]}-{r[-1]}" if len(r) > 1 else str(r[0]) for r in runs)


def cmd_route(args) -> int:
    module = Module(args.module)
    state = module.load()
    whole, mixed = [], []
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing"):
            continue
        r, why, pages = route(module, src)
        label = r if not pages else "transcribe pages " + _spec(pages)
        print(f"{src['nn']}  {label:<24} {why}  — {Path(src['rel']).name}")
        if r == "transcribe":
            (mixed if pages else whole).append((src["nn"], pages))
    if whole:
        print(f'[=] python3 $S transcribe "$M" --only {",".join(n for n, _ in whole)}')
    for nn, pages in mixed:
        print(f'[=] python3 $S transcribe "$M" --only {nn} --pages {_spec(pages)}')
    return 0


def cmd_transcribe(args) -> int:
    from .catalog import repo_root
    from .common import dispatch_lines, parse_pages
    module = Module(args.module)
    state = module.load()
    srcs = [s for s in module.sources(state, args.only) if s.get("status") not in ("excluded", "missing")]
    if args.status:
        for src in srcs:
            if (tdir(module, src) / "manifest.json").exists() or args.only:
                print(status(module, src))
        return 0
    if not args.only:
        raise SystemExit("[-] name the sources: --only NN[,NN…] (see `mbset.py route`)")
    keys = [p + 1 for p in parse_pages(args.key_pages, 10_000)] if args.key_pages else None
    only = [p + 1 for p in parse_pages(args.pages, 10_000)] if args.pages else None
    if only and len(srcs) > 1:
        raise SystemExit("[-] --pages applies to one source at a time")
    briefs: list[str] = []
    for src in srcs:
        m = prepare(module, src, per=args.pages_per, dpi=args.dpi, key_pages=keys, fmt=args.format,
                    only_pages=only)
        todo = [c["brief"] for c in m["chunks"] if not Path(c["out"]).exists()]
        todo += [k["brief"] for k in m.get("keys") or [] if not Path(k["out"]).exists()]
        scope = f"pages {_spec(m['pages_only'])} of {m['pages']}" if m.get("pages_only") else f"{m['pages']} pages"
        keys = f" + {len(m['keys'])} key job(s) (key pages {_spec(m['key_pages'])})" if m.get("keys") else ""
        print(f"[+] {src['nn']}: {scope} → {len(m['chunks'])} chunk(s){keys}, "
              f"{len(todo)} brief(s) to run ({args.format})")
        briefs += todo
    print(f"[=] {len(briefs)} brief(s) — dispatch them all in parallel, one worker each:")
    print("\n".join(dispatch_lines(briefs, repo_root(module.root), "high", args.dispatch)))
    print('[=] then: transcribe "$M" --status → parse "$M" --only NN → spotcheck → check')
    return 0


def register(sub) -> None:
    p = sub.add_parser("route", help="per source/page: parse, transcribe, or transcribe only the bad pages")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.set_defaults(fn=cmd_route)
    p = sub.add_parser("transcribe", help="visual route: chunk briefs → worker JSON → markdown on parse")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--pages", help='transcribe only these pages (e.g. "4-9,15"); the rest stays parsed')
    p.add_argument("--format", choices=["png", "pdf"], default="png",
                   help="png: page images + OCR text drafts · pdf: chunk of the ocrmypdf copy (PDF-reading workers)")
    p.add_argument("--pages-per", type=int, default=PAGES_PER_CHUNK, help="pages per chunk (one worker each)")
    p.add_argument("--dpi", type=int, default=150)
    p.add_argument("--key-pages", help='pages holding an answer key apart from the questions (read once)')
    p.add_argument("--status", action="store_true", help="chunks transcribed / left")
    p.add_argument("--dispatch", help="worker command chosen by the user, with {brief} {repo} {effort} "
                                      "(default: saved at init / env MBSET_DISPATCH; none → briefs listed)")
    p.set_defaults(fn=cmd_transcribe)
