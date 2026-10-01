"""`mbset.py worklist` — a closed list of exactly what a reviewer still has to do, with the crops ready.

Everything mechanical (OCR choice, profile, parse, drops caused by bad OCR) is done by the
coordinator first; the reviewer gets only the items that need eyes:

- **text**: MCQs whose text is not clean or complete — OCR symbols, fewer than 3 options, letters out of
  sequence, glued stems/options, more than 6 options, a written item that may be an MCQ;
- **answer**: MCQs without an answer;
- **model**: written questions without a model answer.

Crops for text + answer items are rendered in advance (`.mbset/reports/work_NN_k.png`). A big file is
split into question ranges (`--max-items`), one part per reviewer, so several reviewers work on it in
parallel. Reviewers only write JSON (`.mbset/packets/worklist/out/<NN[_pK]>/*.json`) — never `fix` — so
nobody edits the same markdown at once; `worklist --apply` merges and applies everything. No OCR or
profile experiments are part of a worklist; a file that is broken as a whole goes back to the
coordinator (usually to `transcribe`).
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
        if written and not re.search(r"^\*\*(?:EXP|Model Answer):\*\*", body, re.M):
            out["model"].append((n, ""))
    return out


def build(module: Module, state: dict[str, Any], selector: str | None) -> list[dict[str, Any]]:
    from .common import load_json

    result = []
    for src in module.sources(state, selector):
        if src.get("status") in ("excluded", "missing"):
            continue
        md = module.md_path(src)
        if not md.exists() or not module.parsed_path(src).exists():
            continue
        it = items(md)
        gaps = [g for g in (load_json(module.parsed_path(src)) or {}).get("gaps", []) if "missing" in g]
        entry = {"nn": src["nn"], "file": Path(src["rel"]).name, "md": str(md),
                 "text": it["text"], "answer": [n for n, _ in it["answer"]], "model": [n for n, _ in it["model"]],
                 "gaps": gaps}
        if it["text"] or it["answer"] or it["model"] or gaps:
            result.append(entry)
    return result


def cost(w: dict[str, Any]) -> int:
    """Text items cost the most (a look + a re-read), then model answers, then answers."""
    return 3 * len(w["text"]) + len(w["answer"]) + 2 * len(w["model"])


def split(w: dict[str, Any], max_cost: int) -> list[dict[str, Any]]:
    """A big file is cut into question ranges of at most `max_cost`, one part per reviewer, so no single
    worker holds a long session (long sessions die of timeouts and lose hours)."""
    if cost(w) <= max_cost:
        return [dict(w, part=None, q_range=None)]
    weight: dict[int, int] = {}
    for n, _ in w["text"]:
        weight[n] = weight.get(n, 0) + 3
    for n in w["answer"]:
        weight[n] = weight.get(n, 0) + 1
    for n in w["model"]:
        weight[n] = weight.get(n, 0) + 2
    cuts: list[list[int]] = [[]]
    load = 0
    for n in sorted(weight):
        if load + weight[n] > max_cost and cuts[-1]:
            cuts.append([])
            load = 0
        cuts[-1].append(n)
        load += weight[n]
    parts = []
    for k, qs in enumerate(cuts, 1):
        lo, hi = qs[0], qs[-1]
        parts.append(dict(w, part=k, q_range=(lo, hi),
                          text=[(n, why) for n, why in w["text"] if lo <= n <= hi],
                          answer=[n for n in w["answer"] if lo <= n <= hi],
                          model=[n for n in w["model"] if lo <= n <= hi],
                          gaps=w["gaps"] if k == 1 else []))
    return parts


def sheets_for(module: Module, state: dict[str, Any], unit: dict[str, Any], per: int) -> list[str]:
    from .spotcheck import answer_sheets

    look = sorted({n for n, _ in unit["text"]} | set(unit["answer"]))
    if not look:
        return []
    src = module.sources(state, unit["nn"])[0]
    outs, _ = answer_sheets(module, src, look, per=per)
    tag = f"{unit['nn']}_p{unit['part']}" if unit["part"] else unit["nn"]
    named = []
    for k, o in enumerate(outs, 1):
        dst = o.with_name(f"work_{tag}_{k}.png")
        o.replace(dst)
        named.append(str(dst))
    return named


def out_dir(module: Module, unit: dict[str, Any]) -> Path:
    tag = f"{unit['nn']}_p{unit['part']}" if unit["part"] else unit["nn"]
    return module.meta / "packets" / "worklist" / "out" / tag


def brief(module: Module, work: list[dict[str, Any]], owner: str) -> str:
    lines = [
        f"# MBset worklist — {module.name} — {owner}",
        "",
        "You finish a closed list of items in a medical question bank. This brief is all you get. The",
        "questions were extracted by a deterministic parser; OCR and parser settings are FINAL. Do not run any",
        "mbset.py command, do not edit markdown, profiles or state, do not commit: you only write the JSON",
        "files named below (other reviewers work on other parts of the same files at the same time). The",
        "coordinator applies them all with `mbset.py worklist --apply`.",
        "",
        "## How to work",
        "1. Read the file's markdown for context (question numbers below are its `### Q<n>` numbers — they do",
        "   not change while you work). Open every sheet PNG listed (image tool): each crop is labelled with",
        "   its markdown question number. For a wider view of a page:",
        '   `pdftoppm -r 110 -f P -l P -png "<source pdf>" /tmp/<owner>_pP`.',
        "2. Write, in your output folder, only the files you need (valid UTF-8 JSON; save as you go):",
        '   text.json    {"7": {"stem": "exact printed stem", "options": {"C": "…"}, "note": "why"}}',
        "                only the parts that change; null removes an option; a written case wrongly split into",
        "                options → every option null and the full printed prompt as stem.",
        '   answers.json {"3": "B:marked", "9": "A:key", "12": "D:derived"}',
        "                key = printed key/table; marked = one option visibly marked; derived = only when the",
        "                file has no key and no mark for that question (from medical knowledge, carefully).",
        '   model.json   {"5": {"text": "full model answer", "source": "key"}}   (key = printed, else derived)',
        '   drop.json    {"14": "UNREADABLE p6: …"}   (a question you cannot read, or not a question)',
        '   add.json     [{"after": 24, "stem": "…", "options": {"A": "…"}, "page": 5, "answer": "B:marked",',
        '                 "note": "source Q27"}]   (a question the parser LOST; after = markdown Q it follows)',
        "3. VERBATIM: copy the printed words exactly — never paraphrase, shorten, reword or complete from",
        "   knowledge. Keep medical notation (Ca²⁺, β1, →). Zero Arabic characters unless the file keeps Arabic.",
        "",
        "## Your items",
    ]
    for w in work:
        rng = f" — questions Q{w['q_range'][0]}–Q{w['q_range'][1]} only (part {w['part']})" if w["part"] else ""
        lines.append(f"### NN {w['nn']} — {w['file']}{rng}  (markdown: {w['md']})")
        lines.append(f"output folder: {out_dir(module, w)}")
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
        "Per file/part: text fixes, answers (marked / key / derived counts, derived Q list), model answers",
        "(key / derived), drops with reasons, additions, and items left unresolved with the reason.",
    ]
    return "\n".join(lines) + "\n"


def cmd_worklist(args) -> int:
    if args.apply:
        return apply(args)
    module = Module(args.module)
    state = module.load()
    work = build(module, state, args.only)
    out = module.meta / "packets" / "worklist"
    out.mkdir(parents=True, exist_ok=True)
    units = [u for w in work for u in split(w, args.max_items)]
    n = args.n or min(8, len(units)) or 1
    bins: list[list[dict[str, Any]]] = [[] for _ in range(max(1, n))]
    for u in sorted(units, key=cost, reverse=True):
        min(bins, key=lambda b: sum(cost(x) for x in b)).append(u)
    briefs: list[str] = []
    for k, b in enumerate([b for b in bins if b], 1):
        for u in b:
            u["sheets"] = sheets_for(module, state, u, args.per)
            out_dir(module, u).mkdir(parents=True, exist_ok=True)
        path = out / f"worklist_{k}.txt"
        path.write_text(brief(module, sorted(b, key=lambda w: (w["nn"], w["part"] or 0)), f"work_{k}"),
                        encoding="utf-8")
        names = ", ".join(u["nn"] + (f"/p{u['part']}" if u["part"] else "") for u in b)
        print(f"[+] {path}  ({names}; items {sum(cost(x) for x in b)})")
        briefs.append(str(path))
    (out / "worklist.json").write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = {k: sum(len(w[k]) for w in work) for k in ("text", "answer", "model")}
    parts = sum(1 for u in units if u["part"])
    print(f"[=] {len(work)} file(s) with work ({parts} part(s) from big files): {tot['text']} text, "
          f"{tot['answer']} answers, {tot['model']} model answers")
    from .catalog import repo_root
    from .common import dispatch_lines
    print("[=] dispatch one worker per worklist in parallel:")
    print("\n".join(dispatch_lines(briefs, repo_root(module.root), "high (max for parts with MODEL items)",
                                    args.dispatch)))
    print('[=] then: mbset.py worklist "$M" --apply')
    return 0


# ------------------------------------------------------------------------------------------- apply
def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def apply(args) -> int:
    """Merge every worker's JSON per file and apply it with `fix`, in an order that keeps the workers'
    question numbers valid: text fixes → answers + model answers + drops (one call, numbers resolved before
    the drop renumbers) → additions (anchors translated through the stems)."""
    import argparse
    import tempfile

    from .cli import cmd_fix
    from .writer import md_numbers_by_stem

    module = Module(args.module)
    state = module.load()
    root = module.meta / "packets" / "worklist" / "out"
    by_nn: dict[str, list[Path]] = {}
    for d in sorted(root.glob("*")) if root.exists() else []:
        if d.is_dir() and any(d.glob("*.json")):
            by_nn.setdefault(d.name.split("_p")[0], []).append(d)
    if args.only:
        wanted = {s["nn"] for s in module.sources(state, args.only)}
        by_nn = {k: v for k, v in by_nn.items() if k in wanted}
    if not by_nn:
        print("[=] no worker output to apply")
        return 0
    base = dict(answer=None, answers=None, source=None, exp_file=None, exp_source="derived", image=None,
                drop=None, reason=None, text_file=None, add_file=None, clear_drops=None)
    tmp = Path(tempfile.mkdtemp(prefix="mbset_apply_"))

    def fix(nn: str, **kw: Any) -> None:
        cmd_fix(argparse.Namespace(module=args.module, nn=nn, **{**base, **kw}))

    for nn, dirs in sorted(by_nn.items()):
        texts: dict[str, Any] = {}
        answers: dict[str, str] = {}
        models: dict[str, dict[str, Any]] = {}
        drops: dict[str, str] = {}
        adds: list[dict[str, Any]] = []
        for d in dirs:
            texts.update(_read(d / "text.json") or {})
            answers.update(_read(d / "answers.json") or {})
            models.update(_read(d / "model.json") or {})
            drops.update(_read(d / "drop.json") or {})
            adds += _read(d / "add.json") or []
        print(f"[*] {nn}: {len(texts)} text, {len(answers)} answers, {len(models)} model, {len(drops)} drops, "
              f"{len(adds)} additions from {len(dirs)} part(s)")
        if texts:
            f = tmp / f"{nn}_text.json"
            f.write_text(json.dumps(texts, ensure_ascii=False), encoding="utf-8")
            fix(nn, text_file=str(f))
        src = module.sources(module.load(), nn)[0]
        md = module.md_path(src)
        snapshot = {n: stem for stem, n in md_numbers_by_stem(md).items()}   # numbering the workers saw
        items = [f"{n}={v.split(':')[0].strip().upper()}:{(v.split(':') + ['marked'])[1].strip().lower()}"
                 for n, v in answers.items() if v]
        reasons = sorted(set(drops.values()))
        # one drop reason per call (the reason is logged per call); answers go with the first call
        first = True
        for model_src in sorted({(m.get("source") or "derived") for m in models.values()}) or [None]:
            kw: dict[str, Any] = {}
            if model_src:
                f = tmp / f"{nn}_model_{model_src}.json"
                f.write_text(json.dumps({n: m["text"] for n, m in models.items()
                                         if (m.get("source") or "derived") == model_src}, ensure_ascii=False),
                             encoding="utf-8")
                kw.update(exp_file=str(f), exp_source=model_src)
            if first and items:
                kw["answers"] = " ".join(items)
            first = False
            if kw:
                fix(nn, **kw)
        for reason in reasons:
            nums = sorted(int(n) for n, r in drops.items() if r == reason)
            # numbers shift after each drop call: resolve them through the stems the workers saw
            now_n = md_numbers_by_stem(md)
            cur = [now_n[snapshot[n]] for n in nums if snapshot.get(n) in now_n]
            if cur:
                fix(nn, drop=",".join(map(str, cur)), reason=reason)
        if adds:
            now_n = md_numbers_by_stem(md)
            fixed = []
            for a in adds:
                after = int(a.get("after") or 0)
                while after and snapshot.get(after) not in now_n:
                    after -= 1                         # the anchor was dropped: follow the previous question
                fixed.append(dict(a, after=now_n[snapshot[after]] if after else 0))
            f = tmp / f"{nn}_add.json"
            f.write_text(json.dumps(fixed, ensure_ascii=False), encoding="utf-8")
            fix(nn, add_file=str(f))
            ans = []
            now_n = md_numbers_by_stem(md)
            for a in fixed:
                if a.get("answer") and a["stem"].strip() in now_n:
                    v = a["answer"]
                    ans.append(f"{now_n[a['stem'].strip()]}={v.split(':')[0].strip().upper()}:"
                               f"{(v.split(':') + ['marked'])[1].strip().lower()}")
            if ans:
                fix(nn, answers=" ".join(ans))
    print('[=] applied — now `mbset.py check "$M"`')
    return 0


def register(sub) -> None:
    p = sub.add_parser("worklist", help="closed per-file lists of text fixes / answers / model answers, crops ready")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--n", type=int, help="number of worklists (parallel reviewers; default one per file/part, max 8)")
    p.add_argument("--per", type=int, default=8, help="questions per sheet")
    p.add_argument("--max-items", type=int, default=60,
                   help="a file costing more is split into question ranges, one part per reviewer")
    p.add_argument("--apply", action="store_true", help="apply every worker's JSON output with `fix`")
    p.add_argument("--dispatch", help="worker command chosen by the user, with {brief} {repo} {effort} "
                                      "(default: env MBSET_DISPATCH; none → briefs are only listed)")
    p.set_defaults(fn=cmd_worklist)
