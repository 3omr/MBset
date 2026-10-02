"""Per-source orchestration: profile → lines → questions → answers → markdown."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from . import answers as answers_mod
from . import overrides
from .common import Module, dump_json, load_json, now, review_flags, text_hash
from .document import load_lines
from .parser import Parser, finish, qnum
from .profiles import effective_profile, write_profile
from .writer import render, write


def raw_counters(lines, profile: dict[str, Any]) -> dict[str, Any]:
    """Counters computed straight from the text, independent of the parser's state machine.

    Source numbering = Σ over sections of (last − first + 1), so an excerpt that starts at
    Q121 counts its own questions only; a restart at 1 opens a new section.
    """
    from .parser import RTL_NUMBER

    q_rx = re.compile(profile["question_start"], re.I)
    a_rx = re.compile(r"^\s*(?:\.\s*)*[(\[]?[aA]\s*(?:[.)\]:]|-(?=\s))\s*\S")
    sections: list[list[int]] = []          # [first, last]
    for ln in lines:
        m = q_rx.match(ln.text)
        if m:
            n = qnum(m)
        else:
            r = RTL_NUMBER.search(ln.text)
            if not r:
                continue
            n = int(r.group(1))
        if not sections:
            sections.append([n, n])
        elif n == sections[-1][1] + 1 or sections[-1][1] < n <= sections[-1][1] + 4:
            sections[-1][1] = n
        elif n == 1 and sections[-1][1] >= 2:
            sections.append([1, 1])
    inline_a = sum(1 for ln in lines if re.search(r"(?:^|\s)[(\[]?a\s*[.)\]]\s+\S.*\s[(\[]?b\s*[.)\]]\s+\S", ln.text))
    return {
        "source_numbering": sum(b - a + 1 for a, b in sections),
        "sections": [f"{a}-{b}" for a, b in sections],
        "option_a_lines": sum(1 for ln in lines if a_rx.match(ln.text)) + inline_a,
    }


def parse_source(module: Module, state: dict[str, Any], src: dict[str, Any], force: bool = False,
                 dry_run: bool = False) -> dict[str, Any]:
    if not module.profile_path(src).exists():
        write_profile(module, src)
    profile = effective_profile(module, src)
    if profile.get("transcribe"):
        # visual route: the questions come from the workers' chunk JSONs (mbset.py transcribe)
        from . import transcribe
        manifest = load_json(transcribe.tdir(module, src) / "manifest.json") or {}
        base = None
        if manifest.get("pages_only"):
            # a mix: the listed pages come from the transcript, every other page from the parser
            lines, _ = load_lines(module, src, profile)
            parsed_recs = finish(Parser(profile, lenient=True).parse(lines), profile)
            answers_mod.attach(module, src, parsed_recs, lines, profile)
            skip = set(manifest["pages_only"]) | set(manifest.get("key_pages") or [])
            base = [r for r in parsed_recs if (r.get("page") or 0) + 1 not in skip]
        t = transcribe.load(module, src, profile, base=base)
        records, info, counters, gaps = t["records"], t["info"], t["counters"], t["gaps"]
        dropped_lines: list[str] = []
        skipped: list[Any] = []
        report: dict[str, Any] = {"method": "transcribe"}
    else:
        lines, info = load_lines(module, src, profile)
        parser = Parser(profile, lenient=info.get("method") == "ocr")
        questions = parser.parse(lines)
        records = finish(questions, profile)
        report = answers_mod.attach(module, src, records, lines, profile)
        counters = raw_counters(lines, profile)
        gaps, dropped_lines, skipped = parser.gaps, parser.dropped, parser.skipped
    applied = overrides.apply(src, records)
    disputed = src.get("disputed") or {}
    for r in records:            # a derived answer the independent second opinion disagreed with (consensus)
        if disputed and r["type"] == "QCS" and r.get("answer_source") == "derived" \
                and overrides.key(r["stem"]) in disputed:
            r["flags"].append("derived_disputed")
    if profile.get("transcribe") and t.get("duplicates"):
        applied.setdefault("dropped", []).extend(t["duplicates"])
    report["answered"] = sum(1 for r in records if r["type"] == "QCS" and r.get("correct"))
    report["mcq"] = sum(1 for r in records if r["type"] == "QCS")
    old = load_json(module.parsed_path(src)) or {}
    old_images = {r["stem"]: r.get("image") for r in old.get("questions", []) if r.get("image")}
    for r in records:
        if r["stem"] in old_images and not r.get("image_removed"):
            r["image"] = old_images[r["stem"]]
    counters["parsed_questions"] = len(records)
    counters["parsed_numbered"] = sum(1 for r in records if r["number"] is not None)
    counters["declared_total"] = profile.get("declared_total")
    parsed = {
        "nn": src["nn"], "source": src["rel"], "sha256": src.get("sha256"), "at": now(),
        "layout": info, "counters": counters, "gaps": gaps, "answers": report,
        "distribution": answers_mod.distribution(records),
        "dropped_lines": dropped_lines[:200], "dropped_count": len(dropped_lines),
        "skipped_questions": skipped, "overrides": applied,
        "questions": records,
    }
    result = {"nn": src["nn"], "questions": len(records), "overrides": applied,
              "mcq": report["mcq"], "answered": report["answered"],
              "flags": sum(1 for r in records if review_flags(r["flags"])), "counters": counters, "gaps": gaps,
              "distribution": parsed["distribution"]}
    if dry_run:
        result["dry_run"] = True
        return result
    dump_json(module.parsed_path(src), parsed)
    text = render(src, records, keep_arabic=bool(profile.get("keep_arabic")))
    if profile.get("markdown") == "keep":
        # a visually reconciled markdown is the deliverable; the parser output is evidence only
        ok, msg = False, f"{src['md']} kept (profile markdown: keep) — parser output stored as evidence only"
    else:
        ok, msg = write(module, src, text, force=force)
    result["written"] = ok
    result["message"] = msg
    stage = src.setdefault("stages", {}).setdefault("parse", {})
    stage.update(at=now(), questions=len(records), mcq=report["mcq"], answered=report["answered"],
                 sources=_source_counts(records), flags=result["flags"])
    if ok:
        stage["md_hash"] = text_hash(text)
        src["status"] = "parsed"
        src.get("stages", {}).pop("review", None)
    module.save(state)
    return result


def _source_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in records:
        if r["type"] == "QCS":
            k = r.get("answer_source") or "none"
            out[k] = out.get(k, 0) + 1
    return out


def refresh_hash(module: Module, state: dict[str, Any], src: dict[str, Any]) -> None:
    """After a tool (not a human) edits the markdown, keep it re-parseable."""
    path = module.md_path(src)
    if path.exists():
        src.setdefault("stages", {}).setdefault("parse", {})["md_hash"] = text_hash(path.read_text(encoding="utf-8"))
        module.save(state)


def describe(result: dict[str, Any]) -> str:
    c = result["counters"]
    dist = " ".join(f"{k}{int(v * 100)}%" for k, v in result.get("distribution", {}).items())
    parts = [f"{result['nn']}: {result['questions']} Q ({result['mcq']} MCQ, {result['answered']} answered)",
             f"counters src#={c['source_numbering']} optA={c['option_a_lines']} parsed={c['parsed_questions']}"]
    if c.get("declared_total"):
        parts.append(f"declared={c['declared_total']}")
    if dist:
        parts.append(dist)
    if result["flags"]:
        parts.append(f"{result['flags']} flagged")
    ov = result.get("overrides") or {}
    if ov.get("applied"):
        parts.append(f"{ov['applied']} reviewed decisions re-applied ({len(ov['dropped'])} drops)")
    if ov.get("stale"):
        parts.append(f"{len(ov['stale'])} stale decisions (stem changed — re-review)")
    if result.get("gaps"):
        parts.append(f"gaps: {'; '.join(result['gaps'])}")
    if result.get("written") is False:
        parts.append(f"NOT WRITTEN — {result['message']}")
    return " | ".join(parts)
