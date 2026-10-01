"""Tag taxonomies as data — one YAML per faculty, chosen once at first-run setup (`mbset.py init`).

Built-in taxonomies live in `references/taxonomies/*.yaml` (Damietta, Assiut, generic); a faculty that is
not built in gets its own file in `~/.config/mbset/taxonomies/<name>.yaml`, written during `init` from the
user's answers. `inventory` suggests each source's tag from the rules below and `check` applies the
taxonomy's year rules.

    name: Damietta
    description: Al-Azhar Faculty of Medicine, Damietta
    multidisciplinary: [Exams]              # tag prefixes whose tagSuggere is None (mixed subjects)
    year_free: []                           # tag prefixes that carry no year unless the filename has one
    rules:                                  # first match wins; tested on "<folder> <filename>" lowercased
      - {match: 'formative', tag: 'Exams, Formative'}
      - {has: professor, tag: 'Professor, Dr {professor}', confidence: low}
      - {has: subject, tag: 'Department, {subject}'}
    default: {tag: 'External, {label}', confidence: low}

Placeholders: {subject} {professor} {week} {gd} {label}. `[ … ]` is an optional segment, dropped when a
placeholder inside it is unknown (`Department, Quizzes[, Week {week}]`); an unknown placeholder outside
one becomes `<Subject>` / `<Name>` / `<N>` so `check` flags it. The year is appended to the tag unless the
rule's family is year-free; a year that is not in the filename is never guessed.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .common import ARABIC, CONFIG_DIR, SUBJECTS, safe_name

BUILTIN = Path(__file__).resolve().parents[2] / "references" / "taxonomies"
USER = CONFIG_DIR / "taxonomies"
PLACEHOLDER = {"subject": "<Subject>", "professor": "<Name>", "week": "<N>", "gd": "<N>", "label": "source"}
# "Dr X" / "د. خالد" / "د/خالد" — the Arabic "د" only as its own token followed by "." or "/"
_PROF = re.compile(r"(?:\bdr\.?\s*|(?<![؀-ۿ])د\s*[./]\s*)([A-Za-z؀-ۿ]+)", re.I)


def available() -> dict[str, Path]:
    """name (lowercase) → file; a user taxonomy overrides a built-in one of the same name."""
    out: dict[str, Path] = {}
    for d in (BUILTIN, USER):
        if d.is_dir():
            for f in sorted(d.glob("*.yaml")):
                out[f.stem.lower()] = f
    return out


def load(name: str | None) -> dict[str, Any]:
    files = available()
    f = files.get((name or "").lower()) or files["generic"]
    tax = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    tax.setdefault("name", f.stem)
    tax.setdefault("multidisciplinary", ["Exams"])
    tax.setdefault("year_free", [])
    tax.setdefault("rules", [])
    tax.setdefault("default", {"tag": "External, {label}", "confidence": "low"})
    return tax


def validate(tax: dict[str, Any]) -> list[str]:
    """Problems in a taxonomy file (empty list = usable)."""
    errs = []
    if not tax.get("name"):
        errs.append("name is missing")
    for i, r in enumerate(tax.get("rules") or [], 1):
        if not r.get("tag"):
            errs.append(f"rule {i}: tag is missing")
        if "match" in r:
            try:
                re.compile(r["match"])
            except re.error as e:
                errs.append(f"rule {i}: bad regex {r['match']!r} ({e})")
        elif r.get("has") not in PLACEHOLDER:
            errs.append(f"rule {i}: needs `match: <regex>` or `has: subject|professor|week|gd`")
        bad = set(re.findall(r"\{(\w+)\}", r.get("tag", ""))) - set(PLACEHOLDER)
        if bad:
            errs.append(f"rule {i}: unknown placeholder(s) {sorted(bad)}")
    if not (tax.get("default") or {}).get("tag"):
        errs.append("default.tag is missing")
    return errs


def _fill(template: str, facts: dict[str, Any]) -> str:
    def opt(m: re.Match) -> str:
        inner = m.group(1)
        return "" if any(not facts.get(k) for k in re.findall(r"\{(\w+)\}", inner)) else inner
    text = re.sub(r"\[([^\]]*)\]", opt, template)
    return re.sub(r"\{(\w+)\}", lambda m: str(facts.get(m.group(1)) or PLACEHOLDER.get(m.group(1), m.group(0))), text)


def facts_for(rel: str) -> dict[str, Any]:
    name = Path(rel).stem
    low = f"{Path(rel).parent} {name}".lower()
    years = re.findall(r"(?<!\d)(20\d{2})(?!\d)", name)
    short = re.search(r"(?<!\d)(\d{2})\s*[-_/ ]\s*(\d{2})(?!\d)", name)
    exam_yy = re.search(r"\b(?:final|end|formative|summ?a?tive|midterm)\s*(\d{2})(?!\d)", name, re.I)
    prof = _PROF.search(name)
    week = re.search(r"week\s*(\d+)", low)
    gd = re.search(r"\bgd\s*[-_ ]?\s*(\d+)", low)
    label = re.sub(r"(?<!\d)(?:20)?\d{2}(?!\d)", "", safe_name(name, 40)).replace("_", " ")
    return {
        "low": low,
        "year4": int(years[-1]) if years else None,
        "year": int(years[-1]) if years else (2000 + int(short.group(2)) if short
                                              else 2000 + int(exam_yy.group(1)) if exam_yy else None),
        "subject": next((s for s in SUBJECTS if s.lower()[:5] in low), None),
        # tags are English only: an Arabic name is left for the agent to transliterate
        "professor": (prof.group(1).title() if not ARABIC.search(prof.group(1)) else None) if prof else None,
        "has_professor": bool(prof),
        "week": week.group(1) if week else None,
        "gd": gd.group(1) if gd else None,
        "label": " ".join(label.split())[:30].strip() or None,
    }


def suggest(tax: dict[str, Any], rel: str) -> dict[str, Any]:
    f = facts_for(rel)
    rule = None
    for r in tax["rules"]:
        if "match" in r and re.search(r["match"], f["low"]):
            rule = r
        elif r.get("has") == "professor" and f["has_professor"]:
            rule = r
        elif r.get("has") in ("subject", "week", "gd") and f.get(r["has"]):
            rule = r
        if rule:
            break
    rule = rule or tax["default"]
    tag = _fill(rule["tag"], f)
    confidence = rule.get("confidence", "medium")
    year_free = tag.startswith(tuple(tax["year_free"])) if tax["year_free"] else False
    year, needs_year = (f["year4"] if year_free else f["year"]), False
    if year_free:
        if year:
            tag = f"{tag} {year}"
    elif year is None:
        confidence, needs_year = "low", True
    else:
        tag = f"{tag} {year}"
    mixed = tag.startswith(tuple(tax["multidisciplinary"]))
    return {"tag": tag, "tagSuggere": None if mixed else f["subject"], "year": year, "confidence": confidence,
            "needs_year": needs_year, "confirmed": False}
