"""`mbset.py worklist` — a closed list of exactly what a reviewer still has to do, with the crops ready.

Everything mechanical (OCR choice, profile, parse, drops caused by bad OCR) is done by the
coordinator first; the reviewer gets only the items that need eyes:

- **text**: MCQs whose text is not clean or complete — OCR symbols, fewer than 3 options, letters out of
  sequence, glued stems/options, more than 6 options, a written item that may be an MCQ;
- **answer**: MCQs without an answer;
- **model**: written questions without a model answer.

Crops for text + answer items are rendered in advance (`.mbset/reports/work_NN_k.png`), so the
reviewer only looks and writes one `fix --text-file` and one `fix --answers` call per file. No OCR or
profile experiments are part of a worklist; a file that is broken as a whole goes back to the
coordinator.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .check import ODD
from .common import Module

HEAD = re.compile(r"^### Q(\d+):\s*(.*)$", re.M)
OPT = re.compile(r"^- \*\*([A-F])\)\*\*\s*(.*)$", re.M)


def items(md: Path) -> dict[str, list[tuple[int, str]]]:
    text = md.read_text(encoding="utf-8")
    heads = list(HEAD.finditer(text))
    out: dict[str, list[tuple[int, str]]] = {"text": [], "answer": [], "model": []}
    for j, m in enumerate(heads):
        n, stem = int(m.group(1)), m.group(2)
        body = text[m.end():heads[j + 1].start() if j + 1 < len(heads) else len(text)]
        opts = OPT.findall(body)
        written = "**Correct Answer:** -" in body
        why = []
        blob = stem + " " + " ".join(t for _, t in opts)
        odd = ODD.findall(blob)
        if odd:
            why.append(f"symbols {''.join(sorted(set(''.join(odd))))[:8]!r}")
        if not written:
            letters = [L for L, _ in opts]
            if letters != list("ABCDEF"[:len(letters)]):
                why.append(f"options {''.join(letters)} not A.. in order")
            if len(opts) < 3:
                why.append(f"only {len(opts)} option(s)")
            if any(len(t.strip()) <= 1 for _, t in opts):
                why.append("empty option")
            if re.search(r"(?:^|\s)[A-E][.)]?\s+[A-Z][a-z]", stem[-80:]) and len(opts) < 5:
                why.append("an option may be glued to the stem")
        if "**Extra Options" in body:
            why.append("more than 6 options (two questions glued?)")
        if written and re.search(r"(?:^|\s)[a-e][.)]\s+\S+.*\s[b-e][.)]\s", stem):
            why.append("written item with a/b/c choices — MCQ or case sub-prompts?")
        if len(stem) < 12:
            why.append("stem too short")
        if why:
            out["text"].append((n, "; ".join(why)))
        if not written and "**Correct Answer:** ?" in body:
            out["answer"].append((n, ""))
        if written and "**EXP:**" not in body:
            out["model"].append((n, ""))
    return out


def build(module: Module, state: dict[str, Any], selector: str | None, per: int = 8) -> list[dict[str, Any]]:
    from .spotcheck import answer_sheets

    result = []
    for src in module.sources(state, selector):
        if src.get("status") in ("excluded", "missing"):
            continue
        md = module.md_path(src)
        if not md.exists() or not module.parsed_path(src).exists():
            continue
        it = items(md)
        look = sorted({n for n, _ in it["text"]} | {n for n, _ in it["answer"]})
        sheets: list[str] = []
        if look:
            outs, _ = answer_sheets(module, src, look, per=per)
            for k, o in enumerate(outs, 1):
                dst = o.with_name(f"work_{src['nn']}_{k}.png")
                o.replace(dst)
                sheets.append(str(dst))
        from .common import load_json
        gaps = [g for g in (load_json(module.parsed_path(src)) or {}).get("gaps", []) if "missing" in g]
        entry = {"nn": src["nn"], "file": Path(src["rel"]).name, "md": str(md), "sheets": sheets,
                 "text": it["text"], "answer": [n for n, _ in it["answer"]], "model": [n for n, _ in it["model"]],
                 "gaps": gaps}
        if it["text"] or it["answer"] or it["model"] or gaps:
            result.append(entry)
    return result


def brief(module: Module, work: list[dict[str, Any]], script: str, owner: str) -> str:
    nns = ",".join(w["nn"] for w in work)
    M, S = str(module.root), script
    lines = [
        f"# MBset worklist — {module.name} — {nns}",
        "",
        "You finish a closed list of items in a medical question bank. This brief is all you get. The",
        "questions were extracted by a deterministic parser; OCR and parser settings are FINAL — do not",
        "run `ocr`, `parse`, `profile` or edit profiles. Do not commit.",
        "",
        f"S={S}",
        f'M="{M}"',
        f'Start: python3 $S lock "$M" {nns} --owner {owner}',
        "",
        "## How to work (one file at a time, batch everything)",
        "0. A previous reviewer may already have done some items: read the file's markdown first and skip",
        "   every item that is already correct there (answered, clean, complete).",
        "1. Open every sheet PNG listed for the file (image tool). Each crop is labelled with its markdown",
        "   question number; the markdown file shows what the parser wrote. For a wider view of a page:",
        '   `pdftoppm -r 110 -f P -l P -png "$M/Raw_PDF_Questions/<file>" /tmp/<owner>_pP`.',
        "2. TEXT items: write ONE json and ONE call:",
        '   python3 $S fix "$M" NN --text-file /tmp/<owner>_NN_text.json',
        '   {"7": {"stem": "exact printed stem", "options": {"A": "…", "B": "…", "C": "…", "D": "…"}, "note": "why"}}',
        "   Give only the parts that change; `null` removes an option; a written case wrongly split into",
        "   options → all options null and the full printed prompt as stem. Copy the printed words exactly —",
        "   never paraphrase, shorten, reword or complete from knowledge. Keep medical notation (Ca²⁺, β1, →).",
        "   A question you cannot read on the page: `fix NN --drop N --reason \"UNREADABLE p<page>: …\"`.",
        "   A question the parser LOST (a MISSING source number, or swallowed into a neighbour): add it,",
        "   exactly as printed, with ONE call per file (do this first — it renumbers the markdown):",
        '   python3 $S fix "$M" NN --add-file /tmp/<owner>_NN_add.json',
        '   [{"after": 24, "stem": "…", "options": {"A": "…", "B": "…"}, "page": 5, "note": "source Q27"}]',
        "   (`after` = the markdown Q number it follows, 0 = first). Then re-open the markdown for numbers.",
        "3. ANSWER items (after the text fixes, same numbering): ONE call per file:",
        '   python3 $S fix "$M" NN --answers "3=B 4=D 9=A" --source marked   (key if printed in a key/table)',
        "   Only letters you SEE marked or printed. Unsure → leave it. The flag `possible_mark` means the",
        "   parser rebuilt an option whose marker a pen stroke destroyed — often the marked one, but confirm.",
        "   If the whole file has no answers at all (no marks, no key): answer from medical knowledge with",
        "   `--source derived` — carefully, and list every one.",
        "4. MODEL items (written questions): one json `{\"N\": \"full model answer in English\"}` and",
        '   python3 $S fix "$M" NN --exp-file /tmp/<owner>_NN_exp.json --exp-source key   (printed answer)',
        "   or `--exp-source derived` (from knowledge). Zero Arabic characters anywhere.",
        f'5. When all files are done: python3 $S check "$M" --only {nns}; then',
        f'   python3 $S lock "$M" {nns} --owner {owner} --release',
        "",
        "## Your items",
    ]
    for w in work:
        lines.append(f"### NN {w['nn']} — {w['file']}  (markdown: {w['md']})")
        if w["sheets"]:
            lines.append("sheets: " + " ".join(w["sheets"]))
        if w["text"]:
            lines.append(f"TEXT ({len(w['text'])}): " + "; ".join(f"Q{n} {why}" for n, why in w["text"]))
        if w["answer"]:
            lines.append(f"ANSWER ({len(w['answer'])}): " + ",".join(f"Q{n}" for n in w["answer"]))
        if w["model"]:
            lines.append(f"MODEL ({len(w['model'])}): " + ",".join(f"Q{n}" for n in w["model"]))
        if w.get("gaps"):
            lines.append("MISSING source numbers (find them on the pages; add the ones really missing): "
                         + "; ".join(w["gaps"][:12]))
        lines.append("")
    lines += [
        "## Final message (nothing else)",
        "Per file: text fixes (count + Q numbers), answers (marked / key / derived counts, derived Q list),",
        "model answers (key / derived), items left unresolved with the reason, drops with reasons, and the",
        "`check --only` summary lines.",
    ]
    return "\n".join(lines) + "\n"


def cmd_worklist(args) -> int:
    module = Module(args.module)
    state = module.load()
    work = build(module, state, args.only, per=args.per)
    out = module.meta / "packets" / "worklist"
    out.mkdir(parents=True, exist_ok=True)
    script = str(Path(__file__).resolve().parents[1] / "mbset.py")
    # balance by item count: text items cost the most (a look + a re-read), then answers, then model
    cost = lambda w: 3 * len(w["text"]) + len(w["answer"]) + 2 * len(w["model"])
    bins: list[list[dict[str, Any]]] = [[] for _ in range(max(1, args.n))]
    for w in sorted(work, key=cost, reverse=True):
        min(bins, key=lambda b: sum(cost(x) for x in b)).append(w)
    for k, b in enumerate([b for b in bins if b], 1):
        path = out / f"worklist_{k}.txt"
        path.write_text(brief(module, sorted(b, key=lambda w: w["nn"]), script, f"work_{k}"), encoding="utf-8")
        print(f"[+] {path}  ({', '.join(w['nn'] for w in b)}; items {sum(cost(x) for x in b)})")
    (out / "worklist.json").write_text(json.dumps(work, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = {k: sum(len(w[k]) for w in work) for k in ("text", "answer", "model")}
    print(f"[=] {len(work)} file(s) with work: {tot['text']} text, {tot['answer']} answers, {tot['model']} model answers")
    return 0


def register(sub) -> None:
    p = sub.add_parser("worklist", help="closed per-file lists of text fixes / answers / model answers, crops ready")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--n", type=int, default=1, help="number of worklists (parallel reviewers)")
    p.add_argument("--per", type=int, default=8, help="questions per sheet")
    p.set_defaults(fn=cmd_worklist)
