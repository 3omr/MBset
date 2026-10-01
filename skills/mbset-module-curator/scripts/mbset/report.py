"""`report` — the final user report for a module, built from state + Markdown_Questions.

Per source: NN, file, class, questions / MCQ / QROC, answered, answer-source counts
(key / marked / online / derived / none), figures linked, spot-check verdict, tag. Then totals,
every derived answer by file and question number, excluded sources with their reasons and the
letter-distribution flags (one letter above 45 % in a file with ≥ 15 MCQs).

The markdown is parsed with the same parser the Excel build uses (`build_module_template`), so
the counts are the counts that will be uploaded. Without ``.mbset/state.json`` the report degrades
to markdown only: source names come from the catalog, tags from a ``*tag_map*.json`` (module root,
``.mbset/`` or ``.mbset/archive/``), exclusions from the placeholder files.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .common import LETTERS, Module, now

SOURCES = ("key", "marked", "online", "derived", "none")
BIAS_INVESTIGATE, BIAS_FAIL, BIAS_MIN = 0.45, 0.60, 15


def _build():
    from .check import BUILD
    return BUILD


def parse_md(path: Path) -> dict[str, Any]:
    """Counts for one canonical markdown file."""
    build = _build()
    qs = build.parse_markdown(str(path))
    out: dict[str, Any] = {"questions": len(qs), "mcq": 0, "qroc": 0, "answered": 0,
                           "sources": Counter(), "letters": Counter(), "derived": [],
                           "figures": 0, "figures_missing": [], "unanswered": []}
    root = path.parent.parent
    for q in qs:
        src = q.get("source") or "none"
        if src not in SOURCES:
            src = "none"
        out["sources"][src] += 1
        if src == "derived":
            out["derived"].append(q["n"])
        if q["Type"] == "QCS":
            out["mcq"] += 1
            filled = [L for L in LETTERS if q.get(L)]
            if q["Correct"] in filled:
                out["answered"] += 1
                out["letters"][q["Correct"]] += 1
            else:
                out["unanswered"].append(q["n"])
        else:
            out["qroc"] += 1
            if q.get("EXP"):
                out["answered"] += 1
            else:
                out["unanswered"].append(q["n"])
        if q.get("Image"):
            out["figures"] += 1
            if not (root / q["Image"]).exists():
                out["figures_missing"].append(q["n"])
    total = sum(out["letters"].values())
    out["bias"] = None
    if total >= BIAS_MIN:
        letter, c = out["letters"].most_common(1)[0]
        share = c / total
        if share > BIAS_INVESTIGATE:
            out["bias"] = (letter, share, total, "FAIL" if share > BIAS_FAIL else "investigate")
    return out


def _placeholder_reason(path: Path) -> str | None:
    from .tidy import is_placeholder

    if not is_placeholder(path):
        return None
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^\*\*Status:\*\*\s*(.+)$", text, re.M) or re.search(r"\b((?:EXCLUDED|DUPLICATE)\b.*)$", text, re.M)
    return m.group(1).strip() if m else "placeholder"


def _catalog(module: Module) -> dict[str, dict[str, str]]:
    """markdown name → {source, status, note} from 00_CATALOG_OF_ALL_FILES.md."""
    out: dict[str, dict[str, str]] = {}
    cat = module.markdown / "00_CATALOG_OF_ALL_FILES.md"
    if not cat.exists():
        return out
    for line in cat.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        md = next((c.strip("`* ") for c in cells if c.strip("`* ").endswith(".md")), None)
        src = next((c.strip("`* ") for c in cells
                    if re.search(r"\.(pdf|docx?|pptx?|txt|jpe?g|png)$", c.strip("`* "), re.I)), None)
        if md:
            status = next((c for c in cells if re.search(r"EXCLUDED|STAGED|PENDING|DONE", c)), "")
            out[md] = {"source": src or "", "status": status, "note": cells[-1] if cells else ""}
    return out


def _tag_maps(module: Module) -> dict[str, str]:
    found: dict[str, str] = {}
    paths = [*module.root.glob("*tag_map*.json"), module.meta / "tag_map.json",
             *(module.meta / "archive").glob("*tag_map*.json")]
    for p in paths:
        try:
            for md, meta in json.loads(p.read_text(encoding="utf-8")).items():
                tag = meta.get("Tag") if isinstance(meta, dict) else None
                if tag and md not in found:
                    found[md] = tag
        except (OSError, ValueError, AttributeError):
            continue
    return found


def collect(module: Module) -> dict[str, Any]:
    state = module.load() if module.state_path.exists() else {"sources": []}
    by_md = {s.get("md"): s for s in state.get("sources", [])}
    catalog = _catalog(module)
    tags = _tag_maps(module)
    rows: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    stray: list[dict[str, str]] = []      # placeholder markdown that no state source owns
    mds = sorted(p for p in module.markdown.glob("*.md") if not p.name.startswith("00_")) \
        if module.markdown.is_dir() else []
    for p in mds:
        src = by_md.get(p.name)
        nn = src["nn"] if src else (re.match(r"^(\d+)", p.name) or [None, "--"])[1]
        source = Path(src["rel"]).name if src else catalog.get(p.name, {}).get("source", "")
        if src and src.get("status") == "excluded":
            excluded.append({"nn": nn, "md": p.name, "source": source, "reason": src.get("exclusion") or "(no reason)"})
            continue
        reason = _placeholder_reason(p)
        if reason and src:
            excluded.append({"nn": nn, "md": p.name, "source": source,
                             "reason": f"{reason} [state status {src.get('status')!r} — `mbset.py set --exclude`]"})
            continue
        if reason:
            (stray if state.get("sources") else excluded).append(
                {"nn": nn, "md": p.name, "source": source, "reason": reason})
            continue
        counts = parse_md(p)
        rows.append({
            "nn": nn, "md": p.name, "source": source,
            "class": (src or {}).get("triage", {}).get("class") or (Path(source).suffix.lstrip(".").lower() or "-"),
            "spot": (src or {}).get("stages", {}).get("review", {}).get("spot_check") or "-",
            "tag": (src or {}).get("tags", {}).get("tag") or tags.get(p.name) or "-",
            "in_state": bool(src), **counts,
        })
    for s in state.get("sources", []):
        if s.get("status") == "excluded" and not (module.markdown / (s.get("md") or "")).is_file():
            excluded.append({"nn": s["nn"], "md": s.get("md") or "", "source": Path(s["rel"]).name,
                             "reason": s.get("exclusion") or "(no reason)"})
    missing = [s for s in state.get("sources", []) if s.get("status") != "excluded"
               and not (module.markdown / (s.get("md") or "")).is_file()]
    return {"module": module.name, "mode": "state + markdown" if state.get("sources") else "markdown only",
            "rows": rows, "excluded": excluded, "stray_placeholders": stray, "missing": missing, "at": now()}


def render(data: dict[str, Any]) -> str:
    rows = data["rows"]
    L = [f"# Question bank report — {data['module']}", "",
         f"Generated {data['at']} · mode: {data['mode']}", ""]
    tot = Counter()
    for r in rows:
        tot.update({k: r[k] for k in ("questions", "mcq", "qroc", "answered", "figures")})
        tot.update({f"src_{k}": r["sources"].get(k, 0) for k in SOURCES})
    L += ["## Totals", "",
          f"- sources with questions: **{len(rows)}** · excluded: **{len(data['excluded'])}**"
          + (f" · missing markdown: **{len(data['missing'])}**" if data["missing"] else ""),
          f"- questions: **{tot['questions']}** ({tot['mcq']} MCQ / {tot['qroc']} QROC) · answered: **{tot['answered']}**",
          "- answer sources: " + " · ".join(f"{k} {tot['src_' + k]}" for k in SOURCES),
          f"- **derived answers: {tot['src_derived']}** (not taken from a key, a mark or an online review — "
          "reported for the user's decision)",
          f"- figures linked: {tot['figures']}", ""]
    L += ["## Per source", "",
          "| NN | file | class | Q | MCQ | QROC | answered | key | marked | online | derived | none | figures | spot | tag |",
          "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in rows:
        s = r["sources"]
        fig = str(r["figures"]) + (f" ({len(r['figures_missing'])} missing)" if r["figures_missing"] else "")
        name = r["source"] or r["md"]
        L.append(f"| {r['nn']} | {name} | {r['class']} | {r['questions']} | {r['mcq']} | {r['qroc']} | "
                 f"{r['answered']} | {s.get('key', 0)} | {s.get('marked', 0)} | {s.get('online', 0)} | "
                 f"{s.get('derived', 0)} | {s.get('none', 0)} | {fig} | {r['spot']} | {r['tag']} |")
    derived = [r for r in rows if r["derived"]]
    L += ["", f"## Derived answers ({tot['src_derived']})", ""]
    L += [f"- {r['nn']} `{r['md']}` ({len(r['derived'])}): " + ", ".join(f"Q{n}" for n in r["derived"])
          for r in derived] or ["- none"]
    unanswered = [r for r in rows if r["unanswered"]]
    if unanswered:
        L += ["", "## Unanswered", ""]
        L += [f"- {r['nn']} `{r['md']}`: " + ", ".join(f"Q{n}" for n in r["unanswered"]) for r in unanswered]
    L += ["", f"## Excluded sources ({len(data['excluded'])})", ""]
    L += [f"- {e['nn']} {e['source'] or e['md']}: {e['reason']}" for e in data["excluded"]] or ["- none"]
    if data.get("stray_placeholders"):
        L += ["", "## Placeholder markdown not owned by any state source", ""]
        L += [f"- `{e['md']}`: {e['reason']}" for e in data["stray_placeholders"]]
    if data["missing"]:
        L += ["", "## Sources without markdown", ""]
        L += [f"- {s['nn']} {Path(s['rel']).name} (expected {s.get('md')})" for s in data["missing"]]
    flagged = [r for r in rows if r["bias"]]
    L += ["", f"## Letter distribution (files with ≥{BIAS_MIN} answered MCQs, one letter > {BIAS_INVESTIGATE:.0%})", ""]
    L += [f"- {r['nn']} `{r['md']}`: {b[0]} = {b[1]:.0%} of {b[2]} — {b[3]}"
          f" ({', '.join(f'{k} {v}' for k, v in sorted(r['letters'].items()))})"
          for r in flagged for b in [r["bias"]]] or ["- no file above the threshold"]
    orphans = [r for r in rows if not r["in_state"]] if data["mode"] != "markdown only" else []
    if orphans:
        L += ["", "## Markdown not in state", ""] + [f"- {r['md']}" for r in orphans]
    return "\n".join(L) + "\n"


def cmd_report(args) -> int:
    module = Module(args.module)
    data = collect(module)
    text = render(data)
    out = Path(args.out) if args.out else module.meta / "reports" / f"report_{data['at'][:10]}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"[=] report: {out}")
    return 0


def register(sub) -> None:
    p = sub.add_parser("report", help="final user report: counts, answer provenance, derived, exclusions, bias")
    p.add_argument("module", help="module folder, e.g. 'My University/Endocrinology'")
    p.add_argument("--out", help="markdown file (default .mbset/reports/report_<date>.md)")
    p.set_defaults(fn=cmd_report)
