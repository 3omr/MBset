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


def stem_or_options(stem: str, options: list[str]) -> str:
    """The text a decision is keyed by: the stem, or — for an item whose stem the parser lost — its
    options (an empty stem would make every such item share one key)."""
    return stem if (stem or "").strip() else "OPTS " + " | ".join(options)


def rkey(r: dict[str, Any]) -> str:
    """Decision key of a parsed record. An empty stem is keyed by its first option, the way the
    markdown reader sees it (`### Q9: ` followed by `- **A)** …`), so fixes to empty-stem questions stick."""
    k = key(r["stem"])
    if not k and r.get("options"):
        k = key("- **%s)** %s" % (r["options"][0]["letter"], r["options"][0]["text"]))
    return k


def md_questions(path: Path) -> dict[int, dict[str, Any]]:
    """Markdown Q number → {stem, options {letter: text}}."""
    text = path.read_text(encoding="utf-8")
    out: dict[int, dict[str, Any]] = {}
    heads = list(HEAD.finditer(text))
    for j, m in enumerate(heads):
        body = text[m.end():heads[j + 1].start() if j + 1 < len(heads) else len(text)]
        opts = {L: t.strip() for L, t in OPT.findall(body)}
        out[int(m.group(1))] = {"stem": stem_or_options(m.group(2).strip(), [opts[L] for L in sorted(opts)]),
                                "options": opts}
    return out


def key_for(src: dict[str, Any], md_stem: str, md_options: dict[str, str] | None = None) -> str:
    """The decision key of a markdown question: the parser's stem, even after a visual text fix changed
    the stem shown in the markdown. Banks repeat questions: when several decisions fit the same shown
    stem, the one whose options match the markdown question's options wins."""
    ov = src.get("overrides") or {}
    k = key(md_stem)
    cands = [k] if k in ov else []
    cands += [pk for pk, o in ov.items() if not o.get("drop") and o.get("stem_fix") and key(o["stem_fix"]) == k and pk != k]
    if not cands:
        return k
    if len(cands) == 1 or not md_options:
        return cands[0]
    want = {norm_stem(t) for t in md_options.values()}

    def overlap(pk: str) -> int:
        o = ov[pk]
        seen = {norm_stem(t) for t in ((o.get("text_before") or {}).get("options") or {}).values()}
        seen |= {norm_stem(t) for t in (o.get("options_fix") or {}).values() if t}
        if o.get("answer"):
            seen.add(norm_stem(o["answer"]))
        return len(want & seen)

    return max(cands, key=overlap)


def record(src: dict[str, Any], stem: str, options: dict[str, str] | None = None, **fields: Any) -> None:
    entry = src.setdefault("overrides", {}).setdefault(key_for(src, stem, options), {})
    entry.update({k: v for k, v in fields.items() if v is not None}, at=now())


def apply_text_fix(o: dict[str, Any], r: dict[str, Any]) -> None:
    """Visual corrections (`fix --text-file`): stem and/or options re-read from the page image."""
    if o.get("stem_fix"):
        r["stem"] = o["stem_fix"]
        r["flags"] = [f for f in r["flags"] if f not in ("empty_stem", "stem_too_short")]
    if o.get("options_fix"):
        opts = {x["letter"]: x for x in r.get("options", [])}
        for letter, text in o["options_fix"].items():
            if text is None:
                opts.pop(letter, None)
            elif letter in opts:
                opts[letter]["text"] = text
            else:
                opts[letter] = {"letter": letter, "text": text, "bold": 0.0, "color": 0.0, "marks": []}
        r["options"] = [opts[L] for L in sorted(opts)]
        if r["options"] and r.get("type") != "QCS":
            r["type"] = "QCS"                       # a written item that really is an MCQ
        elif not r["options"] and r.get("type") == "QCS":
            r["type"] = "QROC"                      # sub-prompts a/b/c taken as options: a written case
        if r.get("correct") not in {o["letter"] for o in r["options"]}:
            r["correct"], r["answer_source"] = None, None
        r["flags"] = [f for f in r["flags"] if not f.startswith(("letters_not_sequential", "options_start_at"))]
    r["flags"].append("text_corrected_visual")


def _fuzzy_pairs(ov: dict[str, Any], records: list[dict[str, Any]], taken: set[int]) -> dict[int, str]:
    """Decisions whose stem changed a little (new OCR, profile fix) → the record they belong to.

    One-to-one, best score first: token-set ratio ≥ 88 on the normalized stem (≥ 95 for drops, so a
    garbled stem can never drop a real question), similar length.
    """
    try:
        from rapidfuzz import fuzz
    except ImportError:
        return {}
    cands = []
    for k, o in ov.items():
        need = 95 if o.get("drop") else 88
        for i, r in enumerate(records):
            if i in taken:
                continue
            rk = rkey(r)
            if not rk or not (0.6 <= len(rk) / max(len(k), 1) <= 1.6):
                continue
            score = fuzz.token_set_ratio(k, rk)
            if score >= need:
                cands.append((score, k, i))
    out: dict[int, str] = {}
    used: set[str] = set()
    for score, k, i in sorted(cands, reverse=True):
        if k in used or i in out:
            continue
        out[i] = k
        used.add(k)
    return out


def _answer_letter(o: dict[str, Any], r: dict[str, Any]) -> str | None:
    want = norm_stem(o["answer"])
    hit = [opt["letter"] for opt in r["options"] if norm_stem(opt["text"]) == want]
    if hit:
        return hit[0]
    # the same option before/after a glyph repair ("e ective" → "effective"): equal letter skeletons
    skel = lambda t: re.sub(r"[^a-z]|[fh]", "", norm_stem(t))
    hit = [opt["letter"] for opt in r["options"] if skel(opt["text"]) and skel(opt["text"]) == skel(o["answer"])]
    if len(hit) == 1:
        return hit[0]
    try:
        from rapidfuzz import fuzz
    except ImportError:
        return None
    scores = sorted(((fuzz.ratio(want, norm_stem(opt["text"])), opt["letter"]) for opt in r["options"]), reverse=True)
    # the option text changed slightly too: take it only when it is clearly the one
    if scores and scores[0][0] >= 85 and (len(scores) == 1 or scores[0][0] - scores[1][0] >= 15):
        return scores[0][1]
    return None


def add_missing(src: dict[str, Any], records: list[dict[str, Any]]) -> int:
    """Questions the parser never produced (swallowed by a neighbour, lost in the scan), re-read from the
    page by a reviewer: `src["additions"]` = [{"after": <stem key or "">, "stem", "options", "page", …}].
    Inserted after the question whose stem key is `after` (at the start when empty)."""
    n = 0
    last: dict[str, dict[str, Any]] = {}             # several additions after one question keep their order
    for add in src.get("additions") or []:
        rec = {"i": None, "number": None, "section": None, "type": "QCS" if add.get("options") else "QROC",
               "stem": add["stem"], "after": "", "exp": "", "inline_answer": None,
               "options": [{"letter": L, "text": t, "bold": 0.0, "color": 0.0, "marks": []}
                           for L, t in sorted((add.get("options") or {}).items())],
               "flags": ["added_from_page_image"], "cut_prefix": "", "page": (add.get("page") or 1) - 1,
               "bbox": None, "pages": [(add.get("page") or 1) - 1], "candidates": {}, "correct": None,
               "answer_source": None}
        if any(rkey(r) == key(rec["stem"]) for r in records):
            continue                                   # the parser finds it now: nothing to add
        at = 0
        anchor = add.get("after") or ""
        if anchor in last and any(r is last[anchor] for r in records):
            at = next(i for i, r in enumerate(records) if r is last[anchor]) + 1
        elif anchor:
            at = next((i + 1 for i, r in enumerate(records) if rkey(r) == anchor
                       or key(ov_stem(src, r)) == anchor), len(records))
        records.insert(at, rec)
        last[anchor] = rec
        n += 1
    return n


def ov_stem(src: dict[str, Any], r: dict[str, Any]) -> str:
    o = (src.get("overrides") or {}).get(rkey(r)) or {}
    return o.get("stem_fix") or r["stem"]


def apply(src: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply stored decisions in place; returns what matched and what no longer matches anything."""
    added = add_missing(src, records)
    ov = src.get("overrides") or {}
    if not ov:
        return {"applied": 0, "dropped": [], "stale": [], "added": added}
    match: dict[int, str] = {}
    for i, r in enumerate(records):
        if rkey(r) in ov:
            match[i] = rkey(r)
    left = {k: o for k, o in ov.items() if k not in set(match.values())}
    fuzzy = _fuzzy_pairs(left, records, set(match)) if left else {}
    match.update(fuzzy)
    dropped: list[dict[str, Any]] = []
    keep: list[dict[str, Any]] = []
    for i, r in enumerate(records):
        k = match.get(i)
        if not k:
            keep.append(r)
            continue
        o = ov[k]
        if i in fuzzy:
            r["flags"].append("decision_matched_fuzzy")
        if o.get("drop"):
            dropped.append({"stem": r["stem"][:120], "reason": o["drop"]})
            continue
        if o.get("stem_fix") or o.get("options_fix"):
            apply_text_fix(o, r)
        if o.get("answer") and r["type"] == "QCS":
            letter = _answer_letter(o, r)
            if letter:
                r["correct"] = letter
                r["answer_source"] = o.get("source")
                r["flags"] = [f for f in r["flags"] if f not in ("no_answer", "answer_sources_disagree")]
            else:
                r["flags"].append("override_answer_text_not_found")
        if o.get("exp_clear"):
            r["exp"], r["exp_source"] = "", None          # a wrong explanation carried over from a neighbour
        elif o.get("exp"):
            r["exp"] = o["exp"]
            r["exp_source"] = o.get("exp_source")
            r["flags"] = [f for f in r["flags"] if f != "written_without_model_answer"]
        if o.get("image") == "none":
            r["image"], r["image_removed"] = None, True    # a false figure link removed by a reviewer
            r["flags"] = [f for f in r["flags"] if f != "figure_dependent"]
        elif o.get("image"):
            r["image"] = o["image"]
        keep.append(r)
    records[:] = keep
    return {"applied": len(match), "dropped": dropped, "stale": sorted(set(ov) - set(match.values())),
            "added": added}
