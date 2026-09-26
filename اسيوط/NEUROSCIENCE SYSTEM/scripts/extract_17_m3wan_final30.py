#!/usr/bin/env python3
"""Extract the single, digitally structured M3WAN Final 30 source.

This is intentionally source-specific.  The answer grid is read from its
coordinates on page 23; the question pages are parsed independently and the
printed Arabic social-media footer is removed by the shared cleaner.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, clean, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
SOURCE = MODULE / "Raw_PDF_Questions" / "CNS" / "OTHER EXAMS" / "FINAL - 30 - CNS - M3WAN - ext.pdf"
OUTPUT = MODULE / "Markdown_Questions" / "17_M3WAN_Final_30.md"


QUESTION_RE = re.compile(r"^\s*(\d{1,3})-\s*(.*)$")
OPTION_RE = re.compile(r"^\s*([A-E])-\s*(.*)$")


def source_lines() -> list[str]:
    doc = fitz.open(SOURCE)
    # Pages 1-22 hold questions; page 23 is the answer grid and page 24 is a
    # footer/closing page.  Keep line boundaries for the source's layout.
    lines: list[str] = []
    for page in doc[:22]:
        for raw in page.get_text("text").splitlines():
            line = clean(raw, strip_edges=False)
            if not line or re.fullmatch(r"\d+", line.strip()):
                continue
            if line.strip().lower() in {"final 30", "questions"}:
                continue
            lines.append(line.strip())
    return lines


def parse_questions(lines: list[str]) -> dict[int, tuple[str, list[str]]]:
    starts: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        match = QUESTION_RE.match(line)
        if match:
            starts.append((index, int(match.group(1))))
    if not starts:
        raise RuntimeError("No numbered questions found")

    parsed: dict[int, tuple[str, list[str]]] = {}
    for position, (start, number) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = lines[start:end]
        first = QUESTION_RE.match(body[0])
        assert first
        stem_parts = [first.group(2).strip()] if first.group(2).strip() else []
        options: list[str] = []
        active: int | None = None
        for line in body[1:]:
            option = OPTION_RE.match(line)
            if option:
                options.append(option.group(2).strip())
                active = len(options) - 1
            elif active is None:
                stem_parts.append(line)
            else:
                options[active] = f"{options[active]} {line}".strip()
        # A trailing E- - is a source placeholder, not a populated option.
        while options and options[-1].strip(" .;-—") == "":
            options.pop()
        stem = " ".join(stem_parts)
        if number in parsed:
            raise RuntimeError(f"Duplicate question number {number}")
        parsed[number] = (stem, options)
    return parsed


def answer_key() -> dict[int, str]:
    doc = fitz.open(SOURCE)
    words = doc[22].get_text("words")
    rows: list[list[tuple[float, str]]] = []
    for word in sorted(words, key=lambda item: (item[1], item[0])):
        y, token = float(word[1]), word[4].strip()
        if token == "23" and y > 700:
            continue
        if not rows or abs(rows[-1][0][0] - y) > 4:
            rows.append([(y, token, float(word[0]))])
        else:
            rows[-1].append((y, token, float(word[0])))
    key: dict[int, str] = {}
    for index, row in enumerate(rows):
        number_row = sorted(row, key=lambda item: item[2])
        numbers = [int(item[1]) for item in number_row if item[1].isdigit()]
        # The page header contains the lone number 30.  Real key rows contain
        # ten consecutive question numbers, followed by a row of answers.
        if len(numbers) < 5:
            continue
        if index + 1 >= len(rows):
            raise RuntimeError(f"Answer-grid has no answer row for {numbers}")
        answer_row = sorted(rows[index + 1], key=lambda item: item[2])
        answers = [item[1].upper() for item in answer_row if re.fullmatch(r"[A-E]|ALL|[-–]", item[1], re.I)]
        if len(numbers) != len(answers):
            raise RuntimeError(f"Answer-grid row mismatch: {numbers} vs {answers}")
        key.update(dict(zip(numbers, answers)))
    if len(key) != 150:
        raise RuntimeError(f"Expected 150 answer-grid entries, got {len(key)}")
    return key


def main() -> int:
    parsed = parse_questions(source_lines())
    key = answer_key()
    if sorted(parsed) != list(range(1, 151)):
        missing = sorted(set(range(1, 151)) - set(parsed))
        extra = sorted(set(parsed) - set(range(1, 151)))
        raise RuntimeError(f"Question numbering mismatch; missing={missing}, extra={extra}")

    questions: list[Question] = []
    for number in range(1, 151):
        stem, options = parsed[number]
        source_answer = key[number]
        if source_answer in {"A", "B", "C", "D", "E"}:
            correct, provenance, exp = source_answer, "key", None
        elif number == 27 and source_answer == "ALL":
            # The printed key literally says ALL, but Q27 is a single-best-
            # answer EXCEPT item.  D is the defensible derived answer; retain
            # the key conflict in the explanation for audit follow-up.
            correct, provenance = "D", "derived"
            exp = "Source answer grid prints ALL; the item is single-best-answer and D is the defensible derived exception. Verify against the original teaching key before upload."
        else:
            raise RuntimeError(f"Unsupported answer key at Q{number}: {source_answer}")
        questions.append(
            Question(
                stem=stem,
                options=options,
                correct=correct,
                source=provenance,
                exp=exp,
                tag="External, M3WAN",
            )
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    count = write_markdown(
        OUTPUT,
        "Source 17 — M3WAN Final 30",
        {
            "Source file": "Raw_PDF_Questions/CNS/OTHER EXAMS/FINAL - 30 - CNS - M3WAN - ext.pdf",
            "Type": "External digitally structured MCQ bank",
            "Pages": 24,
            "Tag": "External, M3WAN",
            "Year": "None (30 is the source/form identifier, not an inferred year)",
            "Answer source": "key:149; derived:1 (Q27 conflicts with printed ALL)",
            "Note": "Arabic social-media/footer text removed; Q27 requires key verification before final Excel gate",
        },
        questions,
    )
    print(f"wrote {count} questions to {OUTPUT}")
    print("provenance", {name: sum(1 for q in questions if q.source == name) for name in {q.source for q in questions}})
    print("option_counts", {n: sum(1 for q in questions if len(q.options) == n) for n in sorted({len(q.options) for q in questions})})
    print("arabic", sum(1 for q in questions if any(re.search(r"[\u0600-\u06ff]", value) for value in [q.stem, *q.options, q.exp or ""])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
