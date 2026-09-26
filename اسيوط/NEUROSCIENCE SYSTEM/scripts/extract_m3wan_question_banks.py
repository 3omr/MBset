#!/usr/bin/env python3
"""Extract the four digitally structured M3WAN banks with per-file bounds.

The files share a visual layout, but each source is handled as an explicit
configuration (question pages, answer-grid page, and expected total).  This
keeps page-specific anomalies visible instead of applying a blind batch regex.
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
RAW = MODULE / "Raw_PDF_Questions" / "CNS" / "OTHER EXAMS"
OUT = MODULE / "Markdown_Questions"

CONFIG = [
    {
        "number": 18,
        "file": "FINAL - CNS - 32 - M3WAN.pdf",
        "output": "18_M3WAN_Final_32.md",
        "key_page": 13,
        "question_end_page": 12,
        "stop_marker": None,
        "stop_occurrence": 1,
        "expected": 75,
        "label": "Final CNS 32",
    },
    {
        "number": 19,
        "file": "MID & FINAL 31 - CNS - M3WAN .pdf",
        "output": "19_M3WAN_Mid_Final_31.md",
        "key_page": 17,
        "question_end_page": 16,
        "stop_marker": "Mid & final 31",
        "stop_occurrence": 1,
        "expected": 100,
        "label": "Mid & Final 31",
    },
    {
        "number": 20,
        "file": "MID 30 - CNS - M3WAN.pdf",
        "output": "20_M3WAN_Mid_30.md",
        "key_page": 13,
        "question_end_page": 13,
        "stop_marker": "MID – 30",
        "stop_occurrence": 2,
        "expected": 75,
        "label": "Mid 30",
    },
    {
        "number": 21,
        "file": "mid 32 CNS - M3WAN.pdf",
        "output": "21_M3WAN_Mid_32.md",
        "key_page": 9,
        "question_end_page": 9,
        "stop_marker": "اخلامتة",
        "stop_occurrence": 1,
        "expected": 37,
        "label": "Mid CNS 32",
    },
]

QUESTION_RE = re.compile(r"^\s*(\d{1,3})-\s*(.*)$")
OPTION_RE = re.compile(r"^\s*([A-E])-(?=\s|$)\s*(.*)$")
SOCIAL_NOISE = re.compile(
    r"(?i)https?://|t\.me|facebook|youtube|جميع الحقوق|M3WAN|معوان|ابدأ مستعيناً"
)
INLINE_OPTION_RE = re.compile(r"(?<!\S)([A-E])-(?=\s|$)")

# Q23 has an ambiguous printed cell ("C - D"); the remaining items have a
# dash in the source grid.  These are defensible single-best answers derived
# from the source stems and the matching lecture content, and are explicitly
# reported as derived rather than silently promoted to key provenance.
DERIVED_ANSWERS = {
    23: "B",
    47: "B",
    53: "D",
    60: "A",
    61: "B",
    62: "B",
    63: "C",
    66: "C",
    70: "D",
}


def question_lines(
    doc: fitz.Document, end_page: int, stop_marker: str | None, stop_occurrence: int
) -> list[str]:
    lines: list[str] = []
    stop_seen = 0
    for page_number, page in enumerate(doc, start=1):
        if page_number > end_page:
            break
        for raw in page.get_text("text").splitlines():
            if stop_marker and stop_marker in raw:
                stop_seen += 1
                if stop_seen >= stop_occurrence:
                    return lines
            value = clean(raw, strip_edges=False)
            if not value or re.fullmatch(r"\d+", value.strip()):
                continue
            if SOCIAL_NOISE.search(value):
                continue
            lines.append(value.strip())
    return lines


def split_inline_options(line: str) -> list[tuple[str, str]]:
    """Split `A- ... B- ...` without mistaking terms such as A-delta."""
    matches = list(INLINE_OPTION_RE.finditer(line))
    if not matches:
        return []
    parts: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
        parts.append((match.group(1), line[match.end() : end].strip()))
    return parts


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
        stem = [first.group(2).strip()] if first.group(2).strip() else []
        options: list[str] = []
        active: int | None = None
        for line in body[1:]:
            inline_options = split_inline_options(line)
            if inline_options:
                for _, content in inline_options:
                    options.append(content)
                    active = len(options) - 1
            else:
                option = OPTION_RE.match(line)
                if option:
                    options.append(option.group(2).strip())
                    active = len(options) - 1
                elif active is None:
                    stem.append(line)
                else:
                    options[active] = f"{options[active]} {line}".strip()
        while options and options[-1].strip(" .;-—") == "":
            options.pop()
        if number in parsed:
            raise RuntimeError(f"Duplicate question number {number}")
        parsed[number] = (" ".join(stem), options)
    return parsed


def answer_key(doc: fitz.Document, page_number: int, expected: int) -> dict[int, str]:
    page = doc[page_number - 1]
    rows: list[list[tuple[float, str, float]]] = []
    for word in sorted(page.get_text("words"), key=lambda item: (item[1], item[0])):
        y, token, x = float(word[1]), word[4].strip(), float(word[0])
        if token == str(page_number) and y > 700:
            continue
        if not rows or abs(rows[-1][0][0] - y) > 4:
            rows.append([(y, token, x)])
        else:
            rows[-1].append((y, token, x))
    key: dict[int, str] = {}
    for index, row in enumerate(rows):
        numbers = [int(item[1]) for item in sorted(row, key=lambda item: item[2]) if item[1].isdigit()]
        if not numbers:
            continue
        if index + 1 >= len(rows):
            continue
        number_cells = sorted(
            [(int(item[1]), item[2]) for item in row if item[1].isdigit()],
            key=lambda item: item[1],
        )
        answer_words = [
            item for item in sorted(rows[index + 1], key=lambda item: item[2])
            if re.fullmatch(r"[A-E]|ALL|[-–]", item[1], re.I)
        ]
        # A malformed source cell such as "C - D" can contain multiple word
        # tokens.  Assign answer tokens to the nearest question-number
        # column, so the ambiguity remains one cell instead of shifting all
        # later answers.
        cells: dict[int, list[str]] = {i: [] for i in range(len(number_cells))}
        for _, token, x in answer_words:
            nearest = min(range(len(number_cells)), key=lambda i: abs(number_cells[i][1] - x))
            cells[nearest].append(token.upper())
        answers = [" ".join(cells[i]) for i in range(len(number_cells))]
        if len(numbers) != len(answers) or any(not value for value in answers):
            continue
        for number, answer in zip(numbers, answers):
            if 1 <= number <= expected:
                key[number] = answer
    if len(key) != expected:
        raise RuntimeError(f"Expected {expected} answer-grid entries, got {len(key)}")
    return key


def extract(config: dict[str, object]) -> None:
    source = RAW / str(config["file"])
    expected = int(config["expected"])
    doc = fitz.open(source)
    parsed = parse_questions(
        question_lines(
            doc,
            int(config["question_end_page"]),
            config.get("stop_marker"),
            int(config.get("stop_occurrence", 1)),
        )
    )
    if sorted(parsed) != list(range(1, expected + 1)):
        missing = sorted(set(range(1, expected + 1)) - set(parsed))
        extra = sorted(set(parsed) - set(range(1, expected + 1)))
        raise RuntimeError(f"{source.name}: numbering mismatch; missing={missing}, extra={extra}")
    key = answer_key(doc, int(config["key_page"]), expected)

    questions: list[Question] = []
    unresolved: list[int] = []
    for number in range(1, expected + 1):
        stem, options = parsed[number]
        answer = key[number]
        if answer in set("ABCDE"):
            correct, provenance, exp = answer, "key", None
        elif number in DERIVED_ANSWERS:
            correct, provenance = DERIVED_ANSWERS[number], "derived"
            exp = f"The source answer grid prints {answer!r}; answer derived from the source stem and the matching lecture content. Verify during final spot-check."
        else:
            correct, provenance = "-", "key"
            unresolved.append(number)
            exp = f"The source answer grid leaves Q{number} without a letter ({answer!r}); resolve before the Excel upload gate."
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

    output = OUT / str(config["output"])
    count = write_markdown(
        output,
        f"Source {config['number']} — M3WAN {config['label']}",
        {
            "Source file": f"Raw_PDF_Questions/CNS/OTHER EXAMS/{config['file']}",
            "Type": "External digitally structured MCQ bank",
            "Pages": len(doc),
            "Tag": "External, M3WAN",
            "Year": "None (M3WAN form number is not inferred as a year)",
            "Answer source": f"key:{expected - len(unresolved) - sum(1 for number in DERIVED_ANSWERS if number in parsed)}; derived:{sum(1 for number in DERIVED_ANSWERS if number in parsed)}; unresolved key blanks:{len(unresolved)}",
            "Note": "Arabic social-media/footer text removed; derived answers and unresolved answer-grid blanks are explicitly retained for final spot-check",
        },
        questions,
    )
    print(f"{output.name}: {count} questions; unresolved={unresolved}")


def main() -> int:
    for config in CONFIG:
        extract(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
