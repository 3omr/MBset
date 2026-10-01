"""`mbset.py route` / `transcribe` — the visual route for sources OCR cannot read well.

Scanned exams, phone screenshots and pen-marked pages are where the parse → fix → re-add loop eats
the time: Tesseract garbles the text, the parser splits or loses questions, and a reviewer re-reads the
page anyway. For such sources the page image *is* the input:

1. `route` measures every source (text layer, OCR confidence, share of questions needing review) and
   says `parse` or `transcribe` — a measurement, never a trial.
2. `transcribe --only NN` renders the pages and cuts the file into chunks of a few pages (big files are
   always split, so no single worker holds a long session). Each chunk gets a self-contained brief:
   the worker reads its page images and writes **one JSON** with every question exactly as printed,
   its answer with provenance and, for written questions, the model answer — one pass, no follow-up
   rounds for answers or model answers.
3. `parse --only NN` then builds the markdown from the chunk JSONs (profile `transcribe: true`), with the
   same gates as the parser route: numbering gaps, missing chunks, options in sequence, keys among the
   options, bias, spot check. Stems that do not appear in the OCR/text layer of their page are flagged
   (`transcript_not_in_page_text`), which catches paraphrasing. `fix` keeps working on top.

    .mbset/transcripts/NN/manifest.json          chunks, pages, status
    .mbset/transcripts/NN/pages/p007.png         rendered page images
    .mbset/transcripts/NN/chunk_02.brief.txt     worker brief (pages 7-12, context page 13)
    .mbset/transcripts/NN/chunk_02.json          worker output
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import IMAGE_SUFFIXES, LETTERS, Module, dump_json, load_json, norm_stem, now, review_flags

VALID_SOURCES = {"key", "marked", "online", "derived"}
PAGES_PER_CHUNK = 6
# route thresholds: below this OCR confidence, or above this share of questions needing review, the
# page image is cheaper than repairing the OCR text question by question
ROUTE_CONF, ROUTE_REVIEW_SHARE = 0.80, 0.30


def tdir(module: Module, src: dict[str, Any]) -> Path:
    return module.meta / "transcripts" / src["nn"]


# --------------------------------------------------------------------------------------------- route
def route(module: Module, src: dict[str, Any]) -> tuple[str, str]:
    """('parse' | 'transcribe', why) from measurements already in state / parsed evidence."""
    path = module.source_path(src)
    t = src.get("triage", {})
    if path.suffix.lower() in (".docx", ".pptx", ".txt", ".md"):
        return "parse", "text document"
    if path.suffix.lower() in IMAGE_SUFFIXES or t.get("class") in ("screenshot", "phone_screenshots"):
        return "transcribe", "screenshots / photos"
    if t.get("has_text"):
        parsed = load_json(module.parsed_path(src))
        if parsed and parsed["questions"]:
            share = sum(1 for r in parsed["questions"] if review_flags(r["flags"])) / len(parsed["questions"])
            if share > ROUTE_REVIEW_SHARE:
                return "transcribe", f"text layer, but {share:.0%} of parsed questions need review"
        return "parse", "text layer"
    conf = (src.get("stages", {}).get("ocr") or {}).get("mean_conf")
    if conf is None:
        return "transcribe", "scanned, no OCR yet (run `ocr` to measure, or transcribe directly)"
    if conf < ROUTE_CONF:
        return "transcribe", f"scanned, OCR confidence {conf:.2f} < {ROUTE_CONF}"
    parsed = load_json(module.parsed_path(src))
    if parsed and parsed["questions"]:
        share = sum(1 for r in parsed["questions"] if review_flags(r["flags"])) / len(parsed["questions"])
        if share > ROUTE_REVIEW_SHARE:
            return "transcribe", f"scanned, OCR {conf:.2f} but {share:.0%} of parsed questions need review"
    return "parse", f"scanned, OCR confidence {conf:.2f}"


# ---------------------------------------------------------------------------------------- prepare
def _page_count(module: Module, src: dict[str, Any]) -> int:
    path = module.source_path(src)
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return 1
    import fitz
    with fitz.open(path) as doc:
        return len(doc)


def render_pages(module: Module, src: dict[str, Any], dpi: int = 150) -> list[Path]:
    """Page images for the workers (cached; PDFs at `dpi`, image sources copied as PNG)."""
    out_dir = tdir(module, src) / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = module.source_path(src)
    outs: list[Path] = []
    if path.suffix.lower() in IMAGE_SUFFIXES:
        from PIL import Image
        out = out_dir / "p001.png"
        if not out.exists():
            Image.open(path).convert("RGB").save(out)
        return [out]
    import fitz
    with fitz.open(path) as doc:
        for pno, page in enumerate(doc):
            out = out_dir / f"p{pno + 1:03d}.png"
            if not out.exists():
                page.get_pixmap(dpi=dpi, annots=True).save(out)
            outs.append(out)
    return outs


def chunks_for(total: int, per: int) -> list[list[int]]:
    """1-based page lists; the last chunk absorbs a remainder of one or two pages."""
    pages = list(range(1, total + 1))
    out = [pages[i:i + per] for i in range(0, total, per)]
    if len(out) > 1 and len(out[-1]) <= max(1, per // 3):
        tail = out.pop()
        out[-1] = out[-1] + tail
    return out


SCHEMA = """{
  "pages": [7, 8, 9, 10, 11, 12],
  "questions": [
    {
      "page": 7,
      "number": 12,
      "stem": "exactly as printed",
      "options": {"A": "as printed", "B": "...", "C": "...", "D": "..."},
      "answer": "C",
      "answer_source": "key",
      "model_answer": null,
      "model_answer_source": null,
      "figure": false
    },
    {
      "page": 9,
      "number": 13,
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


def brief(module: Module, src: dict[str, Any], k: int, n_chunks: int, pages: list[int], context: int | None,
          out: Path, repo: Path, key_pages: list[int] | None = None) -> str:
    pdir = tdir(module, src) / "pages"
    imgs = "\n".join(f"  - page {p}: {pdir / f'p{p:03d}.png'}" for p in pages)
    ctx = (f"\nContext page (read only to finish a question that starts on page {pages[-1]} and runs over; never "
           f"transcribe a question that STARTS on it): {pdir / f'p{context:03d}.png'}") if context else ""
    keys = [p for p in key_pages or [] if p not in pages]
    if keys:
        ctx += ("\nAnswer-key pages of this file (read only — take the answers of YOUR questions from them, "
                "answer_source \"key\"; mind section restarts):\n"
                + "\n".join(f"  - page {p}: {pdir / f'p{p:03d}.png'}" for p in keys))
    keep_ar = "kept in Arabic exactly as printed (this source is keep_arabic)" if _keep_arabic(module, src) \
        else "never write Arabic characters; an Arabic-only line that is not part of a question is skipped"
    return f"""MBset transcription — {module.name} · source {src['nn']} ({Path(src['rel']).name}) · chunk {k}/{n_chunks}

Read these page images (open every one; zoom into small or pen-marked areas):
{imgs}{ctx}

Write ONE file, and nothing else in the repository: {out}
(write it as you go, every page or two, so a timeout never loses the work).

JSON format (UTF-8, valid JSON):
{SCHEMA}

Rules:
1. VERBATIM. Every stem and option is copied exactly as printed — same words, same order, same spelling of
   drug names and numbers. Never shorten, summarise, reword, complete, translate or "improve". Medical
   notation is written properly (Ca²⁺, Na⁺, β1, µm, →). Arabic: {keep_ar}.
2. EVERY question that STARTS on your pages, in page order, none skipped. A question running onto the next page
   is finished from the context page. Text at the top of your first page that continues a question from the
   previous page belongs to the previous chunk — skip it. Answer-key grids are not questions. Page headers, lecture titles, watermarks, phone status bars, LMS buttons
   ("Flag question", "Time left", "Select one:"), page numbers: never part of a stem.
3. `number`: the printed question number (integer), or null when the source prints none. Do not renumber.
   A number the source itself skips → add it to "skipped_numbers".
4. MCQ options: letters A, B, C… in printed order (a printed "a)" is "A"; options printed as 1/2/3 become A/B/C).
   True/False → options {{"A": "True", "B": "False"}}. Matching items → one question per item, each with the
   full printed list as options. "Select all that apply" / several correct → a written question with the
   printed choices kept in the stem ("a. … b. …") and the correct set as model_answer.
5. ANSWER, in the same pass:
   - printed key / "Ans:" line / review "The correct answer is" → answer_source "key";
   - exactly one option visibly marked (tick, circle, highlight, pen, bold) → "marked";
   - several marks, or a student's in-progress selection that is not a key → treat as no mark;
   - no key and no mark → answer from medical knowledge, answer_source "derived".
   The letter must be one of the question's own options. Never copy an answer from another question.
6. WRITTEN questions (no options): model_answer = the printed answer verbatim with model_answer_source "key";
   if none is printed, write a complete, exam-standard model answer from medical knowledge with
   model_answer_source "derived" (keep numbered points as "1. … 2. …").
7. `figure`: true when the stem needs a picture, graph or table on the page to be answered.
8. Do not run any other command, do not edit markdown or state; the coordinator ingests your JSON.
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


def prepare(module: Module, src: dict[str, Any], repo: Path, per: int = PAGES_PER_CHUNK,
            dpi: int = 150, key_pages: list[int] | None = None) -> dict[str, Any]:
    """Render pages, split into chunks of `per` pages (stable once made) and write one brief per chunk.
    `key_pages` (1-based) hold an answer key printed apart from the questions: every chunk reads them."""
    total = _page_count(module, src)
    render_pages(module, src, dpi=dpi)
    d = tdir(module, src)
    old = load_json(d / "manifest.json") or {}
    if old.get("chunks") and old.get("pages") == total:
        chunks = [c["pages"] for c in old["chunks"]]          # keep the split stable once workers have it
    else:
        chunks = chunks_for(total, per)
    key_pages = key_pages if key_pages is not None else old.get("key_pages") or []
    manifest = {"nn": src["nn"], "source": src["rel"], "pages": total, "created": old.get("created") or now(),
                "key_pages": key_pages, "chunks": []}
    for k, pages in enumerate(chunks, 1):
        out = d / f"chunk_{k:02d}.json"
        context = pages[-1] + 1 if pages[-1] < total else None
        b = d / f"chunk_{k:02d}.brief.txt"
        b.write_text(brief(module, src, k, len(chunks), pages, context, out, repo, key_pages), encoding="utf-8")
        manifest["chunks"].append({"k": k, "pages": pages, "brief": str(b), "out": str(out),
                                   "done": out.exists()})
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
    path = module.source_path(src)
    if path.suffix.lower() == ".pdf" and src.get("triage", {}).get("has_text"):
        import fitz
        with fitz.open(path) as doc:
            for pno, page in enumerate(doc):
                t = norm_stem(page.get_text())
                if len(t) > 80:
                    out[pno] = (out.get(pno, "") + " " + t).strip()
    return out


def load(module: Module, src: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    """Records + counters + gaps from the chunk JSONs, in the shape `pipeline.parse_source` writes."""
    from .parser import _clean_text

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
    records: list[dict[str, Any]] = []
    missing: list[str] = []
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
        for q in data.get("questions") or []:
            flags = ["transcribed"]
            stem = _clean_text(q.get("stem") or "", stem=True, keep_arabic=keep_ar)
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
                if source not in VALID_SOURCES:
                    source = None
                if not correct:
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
            if q.get("figure"):
                flags.append("figure_dependent")
            num = q.get("number")
            num = int(num) if isinstance(num, (int, str)) and str(num).strip().isdigit() else None
            records.append({
                "i": len(records) + 1, "number": num, "section": None, "type": qtype, "stem": stem,
                "after": "", "exp": exp, "exp_source": exp_source if exp else None, "inline_answer": None,
                "options": options, "flags": flags, "cut_prefix": "", "page": page - 1, "bbox": None,
                "pages": [page - 1], "candidates": {}, "correct": correct, "answer_source": source,
            })
    # numbering: sections restart at 1; gaps not declared as skipped by the source are reported
    sections: list[list[int]] = []
    gaps: list[str] = []
    for r in records:
        n = r["number"]
        if n is None:
            continue
        if not sections or (n == 1 and sections[-1][1] >= 2) or n <= sections[-1][1] - 5:
            sections.append([n, n])
            continue
        last = sections[-1][1]
        if n > last + 1:
            hole = [x for x in range(last + 1, n) if x not in skipped]
            if hole:
                gaps.append(f"{last} → {n} (missing {hole[0]}{'–' + str(hole[-1]) if len(hole) > 1 else ''})")
        elif n <= last:
            r["flags"].append(f"number_repeated_{n}")
        sections[-1][1] = max(last, n)
    numbering = sum(b - a + 1 for a, b in sections) - len([x for x in skipped
                                                           if any(a <= x <= b for a, b in sections)])
    counters = {"source_numbering": numbering, "sections": [f"{a}-{b}" for a, b in sections],
                "option_a_lines": 0, "parsed_questions": len(records),
                "parsed_numbered": sum(1 for r in records if r["number"] is not None),
                "declared_total": profile.get("declared_total"), "missing_chunks": missing}
    if missing:
        gaps = [f"not transcribed yet: {m}" for m in missing] + gaps
    return {"records": records, "counters": counters, "gaps": gaps, "info": {"method": "transcribe"}}


def status(module: Module, src: dict[str, Any]) -> str:
    m = load_json(tdir(module, src) / "manifest.json")
    if not m:
        return f"{src['nn']}: no transcript"
    done = [c for c in m["chunks"] if Path(c["out"]).exists()]
    left = [f"{c['k']}(p{c['pages'][0]}-{c['pages'][-1]})" for c in m["chunks"] if not Path(c["out"]).exists()]
    return (f"{src['nn']}: {len(done)}/{len(m['chunks'])} chunks transcribed, {m['pages']} pages"
            + (f" — left: {' '.join(left)}" if left else " — ready: `parse --only " + src["nn"] + "`"))


# -------------------------------------------------------------------------------------------- CLI
def cmd_route(args) -> int:
    module = Module(args.module)
    state = module.load()
    picks = {"parse": [], "transcribe": []}
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing"):
            continue
        r, why = route(module, src)
        picks[r].append(src["nn"])
        print(f"{src['nn']}  {r:<10} {why}  — {Path(src['rel']).name}")
    if picks["transcribe"]:
        print(f'[=] transcribe: python3 $S transcribe "$M" --only {",".join(picks["transcribe"])}')
    return 0


def cmd_transcribe(args) -> int:
    from .catalog import repo_root
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
    repo = repo_root(module.root)
    keys = None
    if args.key_pages:
        from .common import parse_pages
        keys = [p + 1 for p in parse_pages(args.key_pages, 10_000)]
    briefs: list[str] = []
    for src in srcs:
        m = prepare(module, src, repo, per=args.pages_per, dpi=args.dpi, key_pages=keys)
        todo = [c for c in m["chunks"] if not Path(c["out"]).exists()]
        print(f"[+] {src['nn']}: {m['pages']} pages → {len(m['chunks'])} chunk(s), {len(todo)} to transcribe "
              f"(profile now transcribe: true)")
        briefs += [c["brief"] for c in todo]
    from .common import dispatch_lines
    print(f"[=] {len(briefs)} brief(s) — dispatch them all in parallel, one worker each:")
    print("\n".join(dispatch_lines(briefs, repo, "high", args.dispatch)))
    print('[=] then: transcribe "$M" --status → parse "$M" --only NN → spotcheck → check')
    return 0


def register(sub) -> None:
    p = sub.add_parser("route", help="per source: parse (text is good) or transcribe (page images), measured")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.set_defaults(fn=cmd_route)
    p = sub.add_parser("transcribe", help="visual route: page images → chunk briefs → JSON → markdown on parse")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--pages-per", type=int, default=PAGES_PER_CHUNK, help="pages per chunk (one worker each)")
    p.add_argument("--dpi", type=int, default=150)
    p.add_argument("--key-pages", help='pages holding an answer key apart from the questions, e.g. "12" or "11-12"')
    p.add_argument("--status", action="store_true", help="chunks transcribed / left")
    p.add_argument("--dispatch", help="worker command chosen by the user, with {brief} {repo} {effort} "
                                      "(default: env MBSET_DISPATCH; none → briefs are only listed)")
    p.set_defaults(fn=cmd_transcribe)
