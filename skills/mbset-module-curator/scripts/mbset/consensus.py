"""`mbset.py consensus` — an independent second answer for every `derived` MCQ, as text only.

A derived answer is one model's knowledge. A second, independent answer costs little when it is text only
(stem + options, no page images): one brief per source lists the derived questions; a worker answers them
blind (it never sees the first answer). Figure questions are left out: they cannot be judged from text. `--apply` compares: agreement stays as it is, a disagreement marks
the question `derived_disputed` — `check` lists it and `worklist` sends it for a careful look (effort max).

    mbset.py consensus "$M" [--only NN]          # write .mbset/consensus/NN.brief.txt
    mbset.py dispatch "$M"                       # runs them with the other pending briefs
    mbset.py consensus "$M" --apply              # compare; disagreements → derived_disputed
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import Module, load_json

HEAD = re.compile(r"^### Q(\d+):\s*(.*)$", re.M)
OPT = re.compile(r"^\s*-\s*\*\*([A-F])\)\*\*\s*(.*)$", re.M)


def cdir(module: Module) -> Path:
    return module.meta / "consensus"


def derived_questions(md: Path) -> list[dict[str, Any]]:
    text = md.read_text(encoding="utf-8")
    heads = list(HEAD.finditer(text))
    out = []
    for j, m in enumerate(heads):
        body = text[m.end():heads[j + 1].start() if j + 1 < len(heads) else len(text)]
        if "**Answer Source:** derived" not in body or "**Image:**" in body:
            continue                 # a figure question cannot be judged from text — its image needs eyes
        opts = OPT.findall(body)
        corr = re.search(r"^\*\*Correct Answer:\*\*\s*([A-F])", body, re.M)
        case = re.search(r"^\*\*Case:\*\*\s*(.*)$", body, re.M)
        if len(opts) >= 2 and corr:
            out.append({"n": int(m.group(1)), "stem": m.group(2).strip(), "case": case.group(1) if case else "",
                        "options": opts, "answer": corr.group(1)})
    return out


def brief(module: Module, src: dict[str, Any], qs: list[dict[str, Any]], out: Path) -> str:
    lines = [f"MBset second opinion — {module.name} · source {src['nn']}", "",
             "Answer each medical MCQ below from your own knowledge: the single best option letter.",
             f"Write ONE file, and nothing else: {out}",
             'JSON: {"answers": {"<question number>": "<letter>"}}  — every question, no explanations.',
             "Do not open any other file and do not run programs.", ""]
    for q in qs:
        if q["case"]:
            lines.append(f"Case: {q['case']}")
        lines.append(f"Q{q['n']}: {q['stem']}")
        lines += [f"  {L}) {t}" for L, t in q["options"]]
        lines.append("")
    return "\n".join(lines)


def cmd_consensus(args) -> int:
    from .overrides import key as stem_key
    module = Module(args.module)
    state = module.load()
    cdir(module).mkdir(parents=True, exist_ok=True)
    made = disputed = agreed = 0
    for src in module.sources(state, args.only):
        md = module.md_path(src)
        if src.get("status") in ("excluded", "missing") or not md.exists():
            continue
        qs = derived_questions(md)
        out = cdir(module) / f"{src['nn']}.json"
        if not args.apply:
            if qs and not out.exists():
                (cdir(module) / f"{src['nn']}.brief.txt").write_text(brief(module, src, qs, out), encoding="utf-8")
                made += 1
            continue
        if not out.exists():
            continue
        second = {str(k): str(v).strip().upper()[:1] for k, v in (json.loads(out.read_text())["answers"]).items()}
        disp = src.setdefault("disputed", {})
        for q in qs:
            other = second.get(str(q["n"]))
            if not other:
                continue
            if other == q["answer"]:
                agreed += 1
                disp.pop(stem_key(q["stem"]), None)
            else:
                disputed += 1
                disp[stem_key(q["stem"])] = f"{q['answer']} vs {other}"
    if args.apply:
        module.save(state)
        print(f"[=] second opinion: {agreed} agree, {disputed} disputed → `parse` then `worklist` sends the disputed")
    else:
        print(f"[+] {made} brief(s) in {cdir(module)} — run them with `mbset.py dispatch` (or Claude subagents), "
              f"then `consensus --apply`")
    return 0


def pending(module: Module) -> list[tuple[str, Path]]:
    d = cdir(module)
    return [(str(b), d / (b.name.replace(".brief.txt", ".json"))) for b in sorted(d.glob("*.brief.txt"))
            if not (d / b.name.replace(".brief.txt", ".json")).exists()] if d.exists() else []


def register(sub) -> None:
    p = sub.add_parser("consensus", help="independent text-only second answer for derived MCQs")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--apply", action="store_true", help="compare the second answers; disagreements → disputed")
    p.set_defaults(fn=cmd_consensus)
