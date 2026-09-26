"""Stages 2+3 gate — one command, problems only.

Hard failures (exit 1) block the Excel; review items are listed for the agent.
Per source: markdown present, three counters agree (source numbering, option-A
lines, `### Q` headings, declared total), bias gate, Arabic/noise/notation, option
sequence, answer letter valid and labelled, figures linked and present, spot
check recorded. Module: every source reconciled (markdown or documented
exclusion), NN unique, no orphan markdown, tags confirmed.
"""

from __future__ import annotations

import importlib.util
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .common import ARABIC, LETTERS, Module, load_json, now

SCRIPTS = Path(__file__).resolve().parents[1]
VALID_SOURCES = {"key", "marked", "online", "derived"}
BIAS_INVESTIGATE, BIAS_FAIL = 0.45, 0.60


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


BUILD = _load("build_module_template")
AUDIT = _load("audit_question_bank")
NOISE = {k: re.compile(v, re.M) for k, v in AUDIT.NOISE.items() if k not in ("markdown markers", "leading numbering")}


def check_source(module: Module, src: dict[str, Any]) -> dict[str, Any]:
    hard: list[str] = []
    review: list[str] = []
    info: dict[str, Any] = {}
    path = module.md_path(src)
    if src.get("status") == "excluded":
        if not src.get("exclusion"):
            hard.append("excluded without a reason")
        return {"hard": hard, "review": review, "info": {"excluded": src.get("exclusion")}}
    if not path.exists():
        return {"hard": [f"no markdown ({src['md']})"], "review": [], "info": {}}
    text = path.read_text(encoding="utf-8")
    qs = BUILD.parse_markdown(str(path))
    raw_blocks = re.split(r"^### Q\d+", text, flags=re.M)[1:]
    nums = [int(n) for n in re.findall(r"^###\s*Q(\d+)", text, re.M)]
    mcq = [q for q in qs if q["Type"] == "QCS"]
    info.update(questions=len(qs), mcq=len(mcq), written=len(qs) - len(mcq))

    if nums != list(range(1, len(nums) + 1)):
        hard.append("numbering is not continuous Q1..QN")
    # ---- three counters
    parsed = load_json(module.parsed_path(src))
    note = src.get("count_note")
    dropped = len(src.get("stages", {}).get("review", {}).get("dropped", []))
    if parsed:
        dropped += len((parsed.get("overrides") or {}).get("dropped", []))
        c = parsed["counters"]
        skipped = len(parsed.get("skipped_questions", []))
        expected = c["source_numbering"] + sum(1 for r in parsed["questions"] if r["number"] is None) - skipped
        info["counters"] = {"source_numbering": c["source_numbering"], "option_a_lines": c["option_a_lines"],
                            "headings": len(qs), "dropped": dropped, "declared": c.get("declared_total")}
        if expected and expected - dropped != len(qs) and not note:
            hard.append(f"counters disagree: source numbering {expected} − dropped {dropped} ≠ {len(qs)} headings")
        if c["option_a_lines"] and abs(c["option_a_lines"] - dropped - len(mcq)) > max(1, len(mcq) // 50) and not note:
            review.append(f"option-A lines {c['option_a_lines']} vs {len(mcq)} MCQs (± dropped {dropped})")
        if c.get("declared_total") and c["declared_total"] != len(qs) + dropped and not note:
            hard.append(f"declared total {c['declared_total']} ≠ {len(qs)} questions (+{dropped} dropped)")
        for g in parsed.get("gaps", []):
            if not note:
                hard.append(f"numbering gap in source: {g}")
        flagged = [(r["i"], r["flags"]) for r in parsed["questions"] if r["flags"]]
        stems = {BUILD.scrub(r["stem"]) for r in parsed["questions"]}
        stale = (parsed.get("overrides") or {}).get("stale")
        if stale:
            review.append(f"{len(stale)} reviewed decisions no longer match any stem — re-review them")
        for i, flags in flagged:
            soft = [f for f in flags if f not in ("figure_dependent", "no_answer")]
            if soft:
                review.append(f"Q{i}: {', '.join(soft)}")
        if not {q["Text"] for q in qs} & stems and qs:
            review.append("markdown no longer matches the parser output (hand-edited?)")
    else:
        review.append("no parser evidence (.mbset/parsed) — counters cannot be verified")
    if note:
        info["count_note"] = note

    # ---- per question
    letters = Counter()
    for n, (q, block) in enumerate(zip(qs, raw_blocks), 1):
        text_all = " ".join(str(q.get(k) or "") for k in ("Text", "EXP", *LETTERS))
        if ARABIC.search(text_all):
            hard.append(f"Q{n}: Arabic characters")
        for label, rx in NOISE.items():
            if rx.search(text_all):
                hard.append(f"Q{n}: noise ({label})")
                break
        if AUDIT.MANGLED.search(text_all):
            review.append(f"Q{n}: mangled notation")
        if q["Type"] == "QCS":
            filled = [L for L in LETTERS if q.get(L)]
            if filled != list(LETTERS[:len(filled)]):
                hard.append(f"Q{n}: options not sequential {filled}")
            if q["Correct"] in (None, "", "?"):
                hard.append(f"Q{n}: unanswered — `mbset.py answersheet`, then `fix --answers`")
            elif q["Correct"] not in filled:
                hard.append(f"Q{n}: Correct {q['Correct']} not among options")
            else:
                letters[q["Correct"]] += 1
                if q.get("source") not in VALID_SOURCES:
                    hard.append(f"Q{n}: Answer Source {q.get('source') or 'missing'}")
            if any(len(str(q[L]).strip()) < 2 for L in filled) and not re.search(r"^\s*-\s*\*\*[A-F]\)\*\*\s*\w\s*$", block, re.M):
                review.append(f"Q{n}: option shorter than 2 chars")
        else:
            if q["Correct"] != "-":
                hard.append(f"Q{n}: written question must have Correct '-'")
            if not q.get("EXP"):
                hard.append(f"Q{n}: written question without model answer (EXP) — `fix --exp-file`")
        if AUDIT.FIGURE.search(q["Text"] or "") and not q.get("Image"):
            hard.append(f"Q{n}: figure-dependent stem without Image")
        if q.get("Image") and not (module.root / q["Image"]).exists():
            hard.append(f"Q{n}: Image file missing {q['Image']}")
    total = sum(letters.values())
    info["distribution"] = {k: round(v / total, 2) for k, v in sorted(letters.items())} if total else {}
    info["sources"] = dict(Counter(q.get("source") or "none" for q in mcq))
    if total >= 15:
        L, c = letters.most_common(1)[0]
        share = c / total
        if share > BIAS_FAIL:
            hard.append(f"bias gate FAIL: {L}={share:.0%} of {total}")
        elif share > BIAS_INVESTIGATE:
            review.append(f"bias gate: {L}={share:.0%} of {total} — sample 10 answers against the source")
    if info["sources"].get("derived"):
        review.append(f"{info['sources']['derived']} derived answers — report to the user")
    spot = src.get("stages", {}).get("review", {}).get("spot_check")
    if not spot:
        hard.append("no spot-check recorded (`mbset.py spotcheck`, then `mbset.py review --spot`)")
    else:
        info["spot_check"] = spot
    return {"hard": hard, "review": review, "info": info}


def check_module(module: Module, state: dict[str, Any], selector: str | None = None) -> dict[str, Any]:
    hard: list[str] = []
    review: list[str] = []
    per: dict[str, Any] = {}
    sources = module.sources(state, selector)
    for src in sources:
        res = check_source(module, src)
        per[src["nn"]] = res
        hard += [f"{src['nn']} {src['md']}: {h}" for h in res["hard"]]
        review += [f"{src['nn']} {src['md']}: {r}" for r in res["review"]]
        if src.get("status") != "excluded" and not src.get("tags", {}).get("confirmed"):
            hard.append(f"{src['nn']}: tag not confirmed ({src.get('tags', {}).get('tag')}) — `mbset.py set`")
    if not selector:
        if state.get("duplicate_nn"):
            hard.append(f"NN used by more than one source: {state['duplicate_nn']} — `mbset.py renumber`")
        owned = {s["md"] for s in state["sources"]}
        for p in sorted(module.markdown.glob("*.md")) if module.markdown.exists() else []:
            if not p.name.startswith("00_") and p.name not in owned:
                review.append(f"orphan markdown (no source in state): {p.name}")
        missing = [s["nn"] for s in state["sources"] if s.get("status") == "missing"]
        if missing:
            hard.append(f"sources in state but not on disk: {missing}")
        live = [s for s in state["sources"] if s.get("status") != "excluded"]
        info = {"sources": len(state["sources"]), "excluded": len(state["sources"]) - len(live),
                "questions": sum(per[s["nn"]]["info"].get("questions", 0) for s in live if s["nn"] in per)}
    else:
        info = {}
    return {"hard": hard, "review": review, "per_source": per, "summary": info, "at": now()}


def write_report(module: Module, result: dict[str, Any]) -> Path:
    out = module.meta / "reports" / f"check_{result['at'][:10]}.md"
    lines = [f"# Check report — {module.name}", "", f"Generated {result['at']}", ""]
    if result["summary"]:
        lines += [f"- {k}: {v}" for k, v in result["summary"].items()] + [""]
    lines += ["| NN | Q | MCQ | sources | distribution | counters | status |", "|---|---:|---:|---|---|---|---|"]
    for nn, res in result["per_source"].items():
        i = res["info"]
        status = "EXCLUDED" if i.get("excluded") else ("FAIL" if res["hard"] else ("review" if res["review"] else "OK"))
        lines.append(f"| {nn} | {i.get('questions', '')} | {i.get('mcq', '')} | {i.get('sources', '')} | "
                     f"{i.get('distribution', '')} | {i.get('counters', '')} | {status} |")
    lines += ["", f"## Hard failures ({len(result['hard'])})", ""] + [f"- {h}" for h in result["hard"]]
    lines += ["", f"## Review items ({len(result['review'])})", ""] + [f"- {r}" for r in result["review"]]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
