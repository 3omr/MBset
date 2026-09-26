"""Stage 2 — attach answers with provenance, automatically where the source allows.

Priority: printed key (grid or inline `Answer: C`) > online (DocReader) > marked
(bold / colour / highlight / ink / tint that distinguishes exactly one option).
Every recovered answer carries its `answer_source` and an evidence string. Two
sources that disagree are flagged, never silently resolved. Nothing defaults to
a letter: a question with no evidence stays unanswered until the agent labels it
`derived` (and reports it) or excludes it.
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Any

from .common import LETTERS, Module, dump_json, load_json, now
from .document import Line

MARK_KINDS = ("tick", "highlight", "fill", "tint", "ink", "circle", "box", "underline")


# --------------------------------------------------------------------------- grid keys
def _grid_pages(spec: Any, total: int) -> list[int]:
    if spec is None:
        return list(range(max(total - 2, 0), total))
    pages = []
    for part in str(spec).split(","):
        part = part.strip()
        if re.fullmatch(r"-\d+", part):
            pages.append(total + int(part))
        elif "-" in part:
            a, b = part.split("-", 1)
            pages.extend(range(int(a) - 1, int(b)))
        elif part:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < total]


def parse_grid(lines: list[Line], profile: dict[str, Any], total_pages: int) -> list[dict[int, str]]:
    """Return one {number: letter} map per key section, in reading order.

    Key lines are lines made only of number→letter pairs (`1 B 31 C/B 61 B`, `1-a 2-c`,
    table rows `1 E 21 C`), anywhere in the file unless `grid_pages` narrows it, plus the
    two-row format (`1 2 3 4 5` above `A C B D A`). `C/B` keeps the first letter and is
    reported in `multi` so the question is flagged.
    """
    from .parser import GRID_LINE, KEY_LABEL, is_grid_line

    cfg = profile["answers"]
    spec = cfg.get("grid_pages")
    pages = set(_grid_pages(spec, total_pages)) if spec else None
    rows = [ln for ln in lines if pages is None or ln.page in pages]
    sections: list[dict[int, str]] = [{}]
    multi: set[tuple[int, int]] = set()

    def add(n: int, letter: str, is_multi: bool = False) -> None:
        cur = sections[-1]
        if n in cur or (cur and n == 1 and max(cur) > 1):
            sections.append({})
            cur = sections[-1]
        cur[n] = letter.upper()
        if is_multi:
            multi.add((len(sections) - 1, n))

    i = 0
    while i < len(rows):
        text = rows[i].text
        nums = re.findall(r"\b\d{1,3}\b", text)
        if len(nums) >= 3 and re.fullmatch(r"[\d\s|.\-]+", text.strip()) and i + 1 < len(rows):
            letters = re.findall(r"\b([A-Fa-f])\b", rows[i + 1].text)
            if len(letters) == len(nums) and re.fullmatch(r"[A-Fa-f\s|.\-]+", rows[i + 1].text.strip()):
                for n, letter in zip(nums, letters):
                    add(int(n), letter)
                i += 2
                continue
        if is_grid_line(text):
            for m in GRID_LINE.finditer(KEY_LABEL.sub("", text)):
                add(int(m.group(1)), m.group(2), "/" in m.group(0))
        i += 1
    out = [s for s in sections if s]
    parse_grid.multi = multi  # type: ignore[attr-defined]
    return out if sum(map(len, out)) >= 5 else []


def apply_grid(records: list[dict[str, Any]], grid: list[dict[int, str]]) -> int:
    """Map key sections onto question sections (same count) or onto one continuous run."""
    if not grid:
        return 0
    q_sections = sorted({r["section"] for r in records})
    hit = 0
    if len(grid) == len(q_sections):
        lookup = {(sec, n): letter for sec, g in zip(q_sections, grid) for n, letter in g.items()}
        key_of = lambda r: (r["section"], r["number"])  # noqa: E731
    else:
        flat: dict[int, str] = {}
        offset = 0
        for g in grid:
            for n, letter in g.items():
                flat[offset + n] = letter
            offset += max(g)
        lookup = {(0, n): letter for n, letter in flat.items()}
        running = {}
        offset = 0
        for sec in q_sections:
            nums = [r["number"] for r in records if r["section"] == sec and r["number"]]
            running[sec] = offset
            offset += max(nums, default=0)
        key_of = lambda r: (0, (r["number"] or 0) + running[r["section"]])  # noqa: E731
    for r in records:
        if r["type"] != "QCS" or r["number"] is None:
            continue
        letter = lookup.get(key_of(r))
        if letter:
            r.setdefault("candidates", []).append({"source": "key", "letter": letter, "evidence": "answer grid"})
            hit += 1
    return hit


# --------------------------------------------------------------------------- marked
def marked_candidate(r: dict[str, Any], kinds: list[str], file_stats: dict[str, float]) -> dict[str, Any] | None:
    opts = r["options"]
    if len(opts) < 2:
        return None
    for kind in kinds:
        if file_stats.get(kind, 0) > 0.6:
            continue  # nearly every option carries it → it is layout, not a key
        if kind == "bold":
            on = [o for o in opts if o["bold"] >= 0.6]
            off = [o for o in opts if o["bold"] < 0.3]
        elif kind == "color":
            on = [o for o in opts if o["color"] >= 0.5]
            off = [o for o in opts if o["color"] < 0.2]
        else:
            on = [o for o in opts if kind in o["marks"]]
            off = [o for o in opts if kind not in o["marks"]]
        if len(on) == 1 and len(off) == len(opts) - 1:
            return {"source": "marked", "letter": on[0]["letter"], "evidence": f"only option with {kind}"}
        if len(on) > 1 and len(on) < len(opts) and kind not in ("bold", "color"):
            r["flags"].append(f"several_options_with_{kind}")
    return None


def file_style_stats(records: list[dict[str, Any]]) -> dict[str, float]:
    opts = [o for r in records if r["type"] == "QCS" for o in r["options"]]
    if not opts:
        return {}
    stats = {"bold": sum(o["bold"] >= 0.6 for o in opts) / len(opts),
             "color": sum(o["color"] >= 0.5 for o in opts) / len(opts)}
    for kind in MARK_KINDS:
        stats[kind] = sum(kind in o["marks"] for o in opts) / len(opts)
    return {k: round(v, 3) for k, v in stats.items()}


# --------------------------------------------------------------------------- DocReader
def fetch_docreader(module: Module, quiz: int) -> list[dict[str, Any]]:
    cache = module.meta / "cache" / f"docreader_{quiz}.json"
    data = load_json(cache)
    if data is not None:
        return data
    url = f"https://doc-reader-guide.com/mcq-quizzes/{quiz}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html)
    text = "".join(chunks).encode("utf-8").decode("unicode_escape")
    start = text.find('"questions":[')
    if start < 0:
        raise RuntimeError(f"no questions array in {url}")
    start += len('"questions":')
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                data = json.loads(text[start:i + 1])
                break
    dump_json(cache, data)
    return data


def apply_online(records: list[dict[str, Any]], online: list[dict[str, Any]]) -> int:
    from rapidfuzz import fuzz

    from .common import norm_stem

    hit = 0
    pool = [(norm_stem(q.get("text")), q) for q in online]
    for r in records:
        if r["type"] != "QCS":
            continue
        key = norm_stem(r["stem"])
        best = max(pool, key=lambda item: fuzz.ratio(key, item[0]), default=None)
        if not best or fuzz.ratio(key, best[0]) < 85:
            continue
        q = best[1]
        idx = q.get("correctOptionIndex")
        opts = q.get("options") or []
        if idx is None or not (0 <= idx < len(opts)):
            continue  # no key online — never default
        target = norm_stem(opts[idx])
        scores = [(fuzz.ratio(target, norm_stem(o["text"])), o["letter"]) for o in r["options"]]
        score, letter = max(scores)
        if score >= 80:
            r.setdefault("candidates", []).append({"source": "online", "letter": letter,
                                                   "evidence": f"docreader option {idx}"})
            if q.get("explanation") and not r.get("exp"):
                r["exp"] = q["explanation"]
            hit += 1
    return hit


# --------------------------------------------------------------------------- resolve
ORDER = {"key": 0, "online": 1, "marked": 2}


def resolve(records: list[dict[str, Any]]) -> None:
    for r in records:
        if r["type"] == "QROC":
            r.update(correct="-", answer_source=None)
            continue
        cands = r.get("candidates", [])
        if r.get("inline_answer"):
            cands.insert(0, {"source": "key", "letter": r["inline_answer"], "evidence": "inline answer line"})
        valid = [c for c in cands if c["letter"] in {o["letter"] for o in r["options"]}]
        if len(valid) < len(cands):
            r["flags"].append("key_letter_not_among_options")
        if not valid:
            r.update(correct=None, answer_source=None)
            r["flags"].append("no_answer")
            continue
        valid.sort(key=lambda c: ORDER[c["source"]])
        best = valid[0]
        if len({c["letter"] for c in valid}) > 1:
            r["flags"].append("answer_sources_disagree:" + ",".join(f"{c['source']}={c['letter']}" for c in valid))
        r.update(correct=best["letter"], answer_source=best["source"], answer_evidence=best["evidence"])


def attach(module: Module, src: dict[str, Any], records: list[dict[str, Any]], lines: list[Line],
           profile: dict[str, Any]) -> dict[str, Any]:
    cfg = profile["answers"]
    mode = cfg.get("mode", "auto")
    report: dict[str, Any] = {"mode": mode}
    for r in records:
        r["candidates"] = []
    if mode in ("grid", "auto"):
        grid = parse_grid(lines, profile, src.get("pages") or 1)
        report["grid_sections"] = [len(g) for g in grid]
        pairs = sum(map(len, grid))
        # a short quiz has a short key: accept it when it covers most of the questions
        enough = pairs >= 10 or (pairs >= 3 and pairs >= 0.8 * sum(1 for r in records if r["type"] == "QCS"))
        report["grid_hits"] = apply_grid(records, grid) if (mode == "grid" or enough) else 0
        multi = getattr(parse_grid, "multi", set())
        if multi:
            q_sections = sorted({r["section"] for r in records})
            for r in records:
                sec_idx = q_sections.index(r["section"]) if len(grid) == len(q_sections) else 0
                if (sec_idx, r["number"]) in multi:
                    r["flags"].append("multi_answer_key")
    if mode in ("online", "auto") and cfg.get("docreader_quiz"):
        try:
            online = fetch_docreader(module, int(cfg["docreader_quiz"]))
            report["online_questions"] = len(online)
            report["online_hits"] = apply_online(records, online)
        except Exception as exc:
            report["online_error"] = f"{type(exc).__name__}: {exc}"
    if mode in ("marked", "auto"):
        stats = file_style_stats(records)
        report["style_stats"] = stats
        kinds = [k for k in cfg.get("marked_by", []) if k]
        hits = 0
        for r in records:
            if r["type"] == "QCS":
                c = marked_candidate(r, kinds, stats)
                if c:
                    r["candidates"].append(c)
                    hits += 1
        report["marked_hits"] = hits
    resolve(records)
    for r in records:
        r["flags"] = list(dict.fromkeys(r["flags"]))
    mcq = [r for r in records if r["type"] == "QCS"]
    report["answered"] = sum(1 for r in mcq if r.get("correct"))
    report["mcq"] = len(mcq)
    report["at"] = now()
    return report


def distribution(records: list[dict[str, Any]]) -> dict[str, float]:
    letters = [r["correct"] for r in records if r["type"] == "QCS" and (r.get("correct") or "?") in LETTERS]
    if not letters:
        return {}
    return {L: round(letters.count(L) / len(letters), 3) for L in LETTERS if letters.count(L)}
