#!/usr/bin/env python3
"""Extract the four ten-item sections in Mid Formatives.pdf.

The Moodle export has question-status chrome in a separate block before each
section and contains no reliable answer key.  Questions are therefore parsed
from line-level option markers and every answer is explicitly labelled
derived.  Arabic overlay comments are excluded as screenshot noise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, has_arabic, clean, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
SOURCE = MODULE / "Raw_PDF_Questions" / "CNS" / "Mid Formatives.pdf"
OUTPUT = MODULE / "Markdown_Questions" / "14_Mid_Formatives.md"

QUESTION_STATUS = re.compile(
    r"(?i)^(?:question\s+\d+|not yet answered|answer saved|marked out of|"
    r"clear my choice|time left|state finished|started on|completed on|"
    r"marks?\s*=|grade\s+|http|page\s+\d+|\d+\s+1st formative|"
    r"not yet$|answered$|1\.00$|oh$|or$)"
)
OPTION = re.compile(r"^\s*([a-e])\.\s*(.*)$", re.I)

# Normalized answers, grouped by the four ten-question sections in the source.
ANSWERS = [
    ["A", "A", "A", "C", "E", "B", "E", "A", "B", "D"],
    ["B", "B", "D", "C", "D", "A", "C", "C", "B", "C"],
    ["D", "E", "B", "C", "C", "C", "D", "A", "D", "C"],
    ["C", "E", "D", "B", "B", "A", "D", "B", "A", "E"],
]


def parse_section(doc: fitz.Document, first_page: int, last_page: int) -> list[tuple[str, list[str]]]:
    """Parse one Moodle attempt section without letting post-E text drift.

    In this export the next stem appears after option E and before the next
    ``a.`` marker.  Once five options have been seen, subsequent clean lines
    therefore belong to ``pending_stem``; the next ``a.`` closes the current
    question and starts the pending one.  This is deliberately local to this
    source rather than a generic PDF regex pass.
    """
    parsed: list[tuple[str, list[str]]] = []
    pending_stem: list[str] = []
    current_stem: list[str] | None = None
    options: list[str] = []
    active: int | None = None
    after_e = False

    def emit() -> None:
        nonlocal current_stem, options, active, after_e
        if current_stem is not None:
            stem = " ".join(current_stem).strip()
            if stem and len(options) == 5 and all(options):
                parsed.append((stem, [item.strip() for item in options]))
        current_stem = None
        options = []
        active = None
        after_e = False

    def begin_from_pending() -> None:
        nonlocal current_stem, pending_stem, options, active, after_e
        current_stem = pending_stem[:]
        pending_stem = []
        options = []
        active = None
        after_e = False

    for page in doc[first_page - 1 : last_page]:
        for raw in page.get_text("text").splitlines():
            if has_arabic(raw):
                continue
            # Keep the terminal period on standalone option markers (a., b.,
            # ...); the shared cleaner's default edge stripping would erase
            # it before the state machine can see the marker.
            line = clean(raw, strip_edges=False)
            line = line.strip() if line else None
            if not line:
                continue
            line = (
                line.replace("+ACY-", "&")
                .replace("+ADs-", ";")
                .replace("+ICY-", "?")
            )
            if (
                QUESTION_STATUS.match(line)
                or re.fullmatch(r"\d+", line)
                or re.match(r"^\d{2}/\d{2}/\d{4},", line)
            ):
                continue
            if line.lower() in {
                "1st formative cns",
                "cns",
                "or",
                "oh",
                "so",
                "0",
                "neurolemmal sheath",
            }:
                continue

            option = OPTION.match(line)
            if option:
                label, content = option.group(1).lower(), option.group(2).strip()
                if label == "a":
                    if current_stem is None:
                        begin_from_pending()
                    elif len(options) == 5:
                        # pending_stem contains the next question, if any.
                        emit()
                        begin_from_pending()
                    else:
                        # A malformed/incomplete block should not silently
                        # swallow the text; keep the marker as a new stem.
                        pending_stem.extend(options)
                        emit()
                        begin_from_pending()
                elif current_stem is None:
                    # The source always starts at a., but retaining this path
                    # makes a damaged page fail by count instead of crashing.
                    begin_from_pending()

                # Labels are expected in order.  Store by sequence, not by
                # the literal label, so source label noise cannot create gaps.
                options.append(content)
                active = len(options) - 1
                # The marker and its value are separate text lines in the
                # PDF.  Do not classify the first value line as the next stem.
                after_e = active == 4 and bool(content)
                continue

            if current_stem is None:
                pending_stem.append(line)
            elif after_e:
                # Option E is one line in this source.  Everything afterward
                # is the next stem until its option-A marker arrives.
                pending_stem.append(line)
            elif active is not None:
                options[active] = f"{options[active]} {line}".strip()
                if active == 4:
                    after_e = True
            else:
                current_stem.append(line)

    emit()
    return parsed


def main() -> int:
    doc = fitz.open(SOURCE)
    # The PDF's four visible attempt sections occupy these page ranges.
    sections = [(1, 3), (4, 7), (8, 11), (12, 15)]
    all_questions: list[Question] = []
    section_counts: list[int] = []
    for index, (first, last) in enumerate(sections):
        parsed = parse_section(doc, first, last)
        if len(parsed) != 10:
            raise RuntimeError(f"Section {index + 1}: expected 10 questions, parsed {len(parsed)}")
        section_counts.append(len(parsed))
        for answer, (stem, options) in zip(ANSWERS[index], parsed):
            all_questions.append(
                Question(
                    stem=stem,
                    options=options,
                    correct=answer,
                    source="derived",
                    exp="No source answer key is embedded in this formative export; answer derived from the corresponding lecture content and must be spot-checked before Excel.",
                    tag="Department, Formative, Week 1",
                    tag_suggere=None,
                )
            )
    count = write_markdown(
        OUTPUT,
        "Source 14 — Mid Formatives",
        {
            "Source file": "Raw_PDF_Questions/CNS/Mid Formatives.pdf",
            "Type": "Department formative Moodle export, four ten-question sections",
            "Pages": len(doc),
            "Tag": "Department, Formative, Week 1",
            "Year": "None",
            "Answer source": "derived:40 (no embedded answer key)",
            "Note": "Moodle status chrome and Arabic screenshot comments removed; four attempt sections retained in source order",
        },
        all_questions,
    )
    print(f"wrote {count}; sections={section_counts}; derived={count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
