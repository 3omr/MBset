#!/usr/bin/env python3
"""Compare pipeline markdown against a reviewed ("golden") markdown file or folder.

For every golden question, find the best-matching new question by normalized stem
(rapidfuzz) and compare the *text* of the correct option, so repacked letters do
not count as differences. Reports: recall (golden questions found), extra
questions, stem fidelity, answer agreement, and the disagreements to inspect.

    python tests/compare_markdown.py GOLDEN.md NEW.md
    python tests/compare_markdown.py --dirs GOLDEN_DIR NEW_DIR --map map.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "build", ROOT / ".agents/skills/mbset-module-curator/scripts/build_module_template.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load(path: Path) -> list[dict]:
    return [build.repack(q) for q in build.parse_markdown(str(path))]


def answer_text(q: dict) -> str | None:
    if q["Type"] != "QCS" or q.get("Correct") not in "ABCDEF" or not q.get("Correct"):
        return None
    return q.get(q["Correct"])


def compare(golden: Path, new: Path, threshold: int = 80) -> dict:
    g, n = load(golden), load(new)
    pool = [(norm(q["Text"]), i) for i, q in enumerate(n)]
    used: set[int] = set()
    found, stem_scores, agree, disagree, missing = 0, [], 0, [], []
    for q in g:
        key = norm(q["Text"])
        best = max(((fuzz.ratio(key, k), i) for k, i in pool if i not in used), default=(0, None))
        if best[0] < threshold:
            missing.append(q["Text"][:90])
            continue
        used.add(best[1])
        found += 1
        stem_scores.append(best[0])
        other = n[best[1]]
        ga, na = answer_text(q), answer_text(other)
        if ga is None or na is None:
            if q["Type"] == "QCS" and other["Type"] == "QCS" and (ga is None) != (na is None):
                disagree.append((q["Text"][:70], ga, na))
            continue
        if fuzz.ratio(norm(ga), norm(na)) >= 85:
            agree += 1
        else:
            disagree.append((q["Text"][:70], ga, na))
    extra = [n[i]["Text"][:90] for _, i in pool if i not in used]
    comparable = agree + len(disagree)
    return {
        "golden": len(g), "new": len(n), "found": found,
        "recall": round(found / len(g), 3) if g else None,
        "stem_fidelity": round(sum(stem_scores) / len(stem_scores), 1) if stem_scores else None,
        "answers_compared": comparable, "answers_agree": agree,
        "answer_agreement": round(agree / comparable, 3) if comparable else None,
        "disagreements": disagree, "missing": missing, "extra": extra,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("golden")
    ap.add_argument("new")
    ap.add_argument("--dirs", action="store_true", help="golden/new are folders; pair files via --map")
    ap.add_argument("--map", help='JSON {"golden.md": "new.md"}')
    ap.add_argument("--json")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    pairs = []
    if args.dirs:
        mapping = json.loads(Path(args.map).read_text(encoding="utf-8"))
        pairs = [(Path(args.golden) / a, Path(args.new) / b) for a, b in mapping.items()]
    else:
        pairs = [(Path(args.golden), Path(args.new))]
    results = {}
    tot = {"golden": 0, "found": 0, "compared": 0, "agree": 0, "new": 0}
    for gp, np_ in pairs:
        if not np_.exists():
            print(f"{gp.name:45} NEW MISSING ({np_.name})")
            continue
        r = compare(gp, np_)
        results[gp.name] = r
        tot["golden"] += r["golden"]; tot["found"] += r["found"]; tot["new"] += r["new"]
        tot["compared"] += r["answers_compared"]; tot["agree"] += r["answers_agree"]
        print(f"{gp.name[:45]:45} golden={r['golden']:4} new={r['new']:4} recall={r['recall']} "
              f"stem={r['stem_fidelity']} answers={r['answers_agree']}/{r['answers_compared']}")
        if args.verbose:
            for d in r["disagreements"]:
                print(f"    ≠ {d[0]!r}: golden={d[1]!r} new={d[2]!r}")
            for m in r["missing"]:
                print(f"    - missing: {m}")
            for e in r["extra"]:
                print(f"    + extra: {e}")
    if len(pairs) > 1:
        print(f"\nTOTAL golden={tot['golden']} new={tot['new']} recall={tot['found'] / max(tot['golden'], 1):.3f} "
              f"answer agreement={tot['agree']}/{tot['compared']} ({tot['agree'] / max(tot['compared'], 1):.3f})")
    if args.json:
        Path(args.json).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
