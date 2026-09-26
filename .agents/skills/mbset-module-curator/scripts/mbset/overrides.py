"""Reviewer decisions that survive a re-parse.

`mbset.py fix` records every decision here (keyed by the normalized stem, so it
still applies after renumbering or a re-parse) and edits the markdown in place.
`parse` re-applies them to the fresh parser output, so fixing the profile and
re-parsing never loses reviewed answers, images, model answers or drops.

    src["overrides"][<stem key>] = {
        "answer": "<text of the correct option>", "source": "marked",   # MCQ
        "exp": "<model answer>", "exp_source": "derived",               # written
        "image": "Images/05_Q3.png",
        "drop": "<reason>",
        "at": "...",
    }
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import norm_stem, now

OPT = re.compile(r"^\s*-\s*\*\*([A-F])\)\*\*\s*(.*)$", re.M)
HEAD = re.compile(r"^### Q(\d+):\s*(.*)$", re.M)


def key(stem: str) -> str:
    return norm_stem(stem)[:160]


def md_questions(path: Path) -> dict[int, dict[str, Any]]:
    """Markdown Q number → {stem, options {letter: text}}."""
    text = path.read_text(encoding="utf-8")
    out: dict[int, dict[str, Any]] = {}
    heads = list(HEAD.finditer(text))
    for j, m in enumerate(heads):
        body = text[m.end():heads[j + 1].start() if j + 1 < len(heads) else len(text)]
        out[int(m.group(1))] = {"stem": m.group(2).strip(), "options": {L: t.strip() for L, t in OPT.findall(body)}}
    return out


def record(src: dict[str, Any], stem: str, **fields: Any) -> None:
    entry = src.setdefault("overrides", {}).setdefault(key(stem), {})
    entry.update({k: v for k, v in fields.items() if v is not None}, at=now())


def apply(src: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply stored decisions in place; returns what matched and what no longer matches anything."""
    ov = src.get("overrides") or {}
    if not ov:
        return {"applied": 0, "dropped": [], "stale": []}
    seen: set[str] = set()
    dropped: list[dict[str, Any]] = []
    keep: list[dict[str, Any]] = []
    applied = 0
    for r in records:
        k = key(r["stem"])
        o = ov.get(k)
        if not o:
            keep.append(r)
            continue
        seen.add(k)
        applied += 1
        if o.get("drop"):
            dropped.append({"stem": r["stem"][:120], "reason": o["drop"]})
            continue
        if o.get("answer") and r["type"] == "QCS":
            want = norm_stem(o["answer"])
            hit = [opt["letter"] for opt in r["options"] if norm_stem(opt["text"]) == want]
            if hit:
                r["correct"] = hit[0]
                r["answer_source"] = o.get("source")
                r["flags"] = [f for f in r["flags"] if f not in ("no_answer", "answer_sources_disagree")]
            else:
                r["flags"].append("override_answer_text_not_found")
        if o.get("exp"):
            r["exp"] = o["exp"]
            r["exp_source"] = o.get("exp_source")
            r["flags"] = [f for f in r["flags"] if f != "written_without_model_answer"]
        if o.get("image"):
            r["image"] = o["image"]
        keep.append(r)
    records[:] = keep
    return {"applied": applied, "dropped": dropped, "stale": sorted(set(ov) - seen)}
