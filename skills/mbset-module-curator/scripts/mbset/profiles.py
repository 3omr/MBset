"""Parser profiles: one small YAML per source, suggested from triage, edited by the agent.

A profile describes the *format* of a source, never its content. The parser
executes it; the agent's job is to make it right, not to retype questions.
See ``references/profiles.md`` for every field.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .common import Module

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "references" / "profiles"

DEFAULT: dict[str, Any] = {
    "template": None,
    "text": "auto",            # auto | native | ocr | ocrpdf (ocrmypdf --redo-ocr text layer) | docx | pptx | plain
    "columns": "auto",         # auto | 1 | 2
    "split": None,             # force the gutter x (points)
    "pages": None,             # "1-12" (1-based); None = all
    "skip_patterns": [],       # regexes; matching lines are dropped before parsing
    "stop_patterns": [],       # regex; parsing stops at the first match (e.g. answer-key page)
    # "12.", "12)", "12-", "Q12:", "(12)" and chapter-style "24.3 " (the question is the last number)
    "question_start": r"^\s*(?:Q(?:uestion)?\s*)?\(?(?:\d{1,3}\.(\d{1,3})\s+(?=[A-Z(])|(\d{1,3})\s*(?:[.)](?!\d)|-(?!\w)|:)\s*)",
    # leading dots come from right-to-left PDFs that move the full stop to the front (".A. Neck pain")
    "option_pattern": r"^\s*(?:\.\s*)*[(\[]?([a-fA-F])\s*(?:[.)\]:]|-(?=\s))\s*(?=\S)",
    "options_inline": "auto",  # auto | true | false  ("a. x b. y c. z" on one line)
    "sections_restart": True,  # numbering restarting at 1 opens a new section
    "numbering": "auto",       # auto | none (questions are found from option runs / paragraphs)
    "declared_total": None,
    "type": "auto",            # auto | mcq | written
    "answers": {
        "mode": "auto",        # auto | grid | inline | marked | online | none
        "grid_pages": None,    # pages holding the key grid, e.g. "12" or "-1" (last)
        "grid_pattern": r"(?<!\d)(\d{1,3})\s*[-.:)=]?\s*\(?([A-Fa-f])\)?(?![A-Za-z])",
        "inline_pattern": r"^\s*(?:correct\s+)?(?:answer|ans|key)\s*(?:is)?\s*[:\-=.]?\s*\(?([A-Fa-f])\)?\b",
        "marked_by": ["tick", "highlight", "fill", "tint", "ink", "circle", "box", "bold", "bold_marker", "color", "underline"],
        "tint": True,
        "docreader_quiz": None,
    },
    "written": {
        "answer_marker": r"^\s*(?:model\s+)?(?:answer|ans)\s*[:\-]",
    },
    "ocr": {"dpi": 300, "psm": 3, "lang": "eng", "rotate": 0},
    # questions written in Arabic are kept in Arabic (user decision per module); OCR with ocr.lang: ara+eng
    "keep_arabic": False,
    "markdown": "parser",      # parser | keep (a reconciled markdown is kept; fix edits it in place)
    "transcribe": False,       # true: questions come from page-image transcripts (`mbset.py transcribe`)
    "question_end": None,
    "numeric_options": False,  # options numbered 1) 2) 3) (needs question_end to tell stems apart)      # regex, e.g. '[:؟?]\s*$': such a line after an option run starts a new question
    "notes": "",
}


def _merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def template(name: str | None) -> dict[str, Any]:
    if not name:
        return {}
    path = TEMPLATES_DIR / f"{name}.yaml"
    if not path.exists():
        raise SystemExit(f"[-] unknown profile template {name!r}; see {TEMPLATES_DIR}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_profile(module: Module, src: dict[str, Any]) -> dict[str, Any] | None:
    path = module.profile_path(src)
    if not path.exists():
        return None
    own = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return _merge(_merge(DEFAULT, template(own.get("template"))), own)


def effective_profile(module: Module, src: dict[str, Any]) -> dict[str, Any]:
    return load_profile(module, src) or _merge(DEFAULT, suggest(src))


def suggest(src: dict[str, Any]) -> dict[str, Any]:
    """Suggest the fields that differ from DEFAULT, from the triage facts."""
    t = src.get("triage", {})
    s = t.get("signals", {})
    cls = t.get("class")
    prof: dict[str, Any] = {"source": src["rel"]}
    mapping = {"digital_single": "digital_single", "digital_two_column": "digital_two_column",
               "scanned": "scanned", "moodle": "moodle_review", "docreader": "docreader",
               "docx": "docx", "pptx": "pptx", "screenshot": "screenshots", "phone_screenshots": "moodle_review"}
    prof["template"] = mapping.get(cls)
    if cls == "digital_two_column":
        prof["columns"] = 2
    answers: dict[str, Any] = {}
    if s.get("docreader_quiz"):
        answers.update(mode="online", docreader_quiz=int(s["docreader_quiz"]))
    # otherwise mode stays "auto": grid, inline, marked and online are all tried and ranked
    if answers:
        prof["answers"] = answers
    if t.get("has_text") and s.get("option_lines", 0) <= 1 and s.get("question_numbers", 0) <= 2 and cls != "docx":
        prof["template"] = "written_only"
        prof["numbering"] = "none"
    if s.get("declared_total"):
        prof["declared_total"] = s["declared_total"]
    sample = t.get("text_sample", "")
    inline = re.findall(r"^\s*\(?a\s*[.)]\s+\S.*\s\(?b\s*[.)]\s+\S", sample, re.M | re.I)
    if len(inline) >= 3:
        prof["options_inline"] = True
    return prof


def write_profile(module: Module, src: dict[str, Any], force: bool = False) -> Path:
    path = module.profile_path(src)
    if path.exists() and not force:
        return path
    prof = suggest(src)
    t = src.get("triage", {})
    header = (f"# Parser profile for {src['nn']} — {Path(src['rel']).name}\n"
              f"# class={t.get('class')} pages={t.get('pages')} has_text={t.get('has_text')} "
              f"columns={t.get('columns')} bold_ratio={t.get('bold_ratio')} mark_rects={t.get('mark_rects')}\n"
              f"# signals={t.get('signals')}\n"
              "# Only fields that differ from the template/DEFAULT are needed. Field reference:\n"
              "#   .agents/skills/mbset-module-curator/references/profiles.md\n")
    path.write_text(header + yaml.safe_dump(prof, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path
