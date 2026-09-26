#!/usr/bin/env python3
"""Extract the 15-page physiology question bank.

The source has a mixed layout: questions 1-10 contain PDF highlight
annotations, while later quiz pages have no embedded key.  The parser keeps
the quiz boundaries, normalizes malformed option labels by source order, and
uses the highlight geometry only for marked items.  Later answers are labelled
derived so they remain visible for the final spot-check.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, clean, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
SOURCE = MODULE / "Raw_PDF_Questions" / "CNS" / "physiology Qs bank MCQ.pdf"
OUTPUT = MODULE / "Markdown_Questions" / "28_Physiology_Qs_bank_MCQ.md"

QUIZ_RE = re.compile(r"^\s*QUIZE\s+(\d+)", re.I)
QUESTION_RE = re.compile(r"^\s*(\d+)\s*[-.)]\s*(.*)$")
OPTION_RE = re.compile(r"^\s*([A-Za-z])\s*[.)]\s*(.*)$")
SKIP_RE = re.compile(r"(?i)^\s*(?:select the (?:best|correct) answer|questions?)\s*:?\s*$")

# Normalized option positions (A=first option, etc.) for items without an
# embedded highlight.  These are deliberately explicit and reviewed against
# the corresponding lecture content rather than inferred from answer letters
# in the source's malformed labels.
DERIVED = {
    3: ["B", "C", "A", "D", "B"],
    5: [None, "C", None, None, None, "C"],
    6: [None, None, None, None, "B"],
    11: ["C", "B", "C", "B", "B"],
    12: ["A", "B", "C", "A", "A"],
    13: ["C", "D", "B", "A", "D"],
    14: ["C", "B", "C", "B"],
    15: ["C", "D", "A", "D", "D"],
    16: ["D", "A", "B"],
    17: ["C", "C", "A"],
    18: ["D", "B", "B"],
    19: ["C", "A", "A"],
    20: ["D", "A"],
    21: ["D", "D"],
}


def records(doc: fitz.Document) -> tuple[list[dict], dict[tuple[int, int], str]]:
    questions: list[dict] = []
    current: dict | None = None
    quiz = 0
    for page_number, page in enumerate(doc, start=1):
        line_records = []
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = " ".join(span["text"] for span in line["spans"]).strip()
                if text:
                    line_records.append((tuple(line["bbox"]), text))
        line_records.sort(key=lambda item: (item[0][1], item[0][0]))
        for bbox, text in line_records:
            qm = QUIZ_RE.match(text)
            if qm:
                if current is not None:
                    questions.append(current)
                current = None
                quiz = int(qm.group(1))
                continue
            qmatch = QUESTION_RE.match(text)
            # Question numbers are only recognized once a quiz heading has
            # established context; option lines cannot match this pattern.
            if qmatch and quiz:
                if current is not None:
                    questions.append(current)
                current = {
                    "quiz": quiz,
                    "local": int(qmatch.group(1)),
                    "stem": [qmatch.group(2).strip()] if qmatch.group(2).strip() else [],
                    "options": [],
                    "option_boxes": [],
                }
                continue
            if current is None or SKIP_RE.match(text):
                continue
            om = OPTION_RE.match(text)
            if om:
                current["options"].append(om.group(2).strip())
                current["option_boxes"].append(
                    {"page": page_number, "y0": bbox[1], "y1": bbox[3]}
                )
                continue
            if current["options"]:
                current["options"][-1] = f"{current['options'][-1]} {text}".strip()
                current["option_boxes"][-1]["y1"] = max(current["option_boxes"][-1]["y1"], bbox[3])
            else:
                current["stem"].append(text)
    if current is not None:
        questions.append(current)

    # Deduplicate annotation hits and map each highlight to the option whose
    # line it intersects most strongly.
    marked: dict[tuple[int, int], set[int]] = defaultdict(set)
    for page_number, page in enumerate(doc, start=1):
        for annotation in page.annots() or []:
            ay0, ay1 = annotation.rect.y0, annotation.rect.y1
            candidates = []
            for item in questions:
                if item["quiz"] == 0:
                    continue
                for index, box in enumerate(item["option_boxes"]):
                    if box["page"] != page_number:
                        continue
                    overlap = max(0.0, min(ay1, box["y1"]) - max(ay0, box["y0"]))
                    distance = abs((ay0 + ay1) / 2 - (box["y0"] + box["y1"]) / 2)
                    if overlap > 0 or distance < 10:
                        candidates.append((overlap, -distance, item["quiz"], item["local"], index))
            if candidates:
                _, _, q, n, index = max(candidates)
                marked[(q, n)].add(index)
    mapped = {}
    for key, indexes in marked.items():
        if len(indexes) == 1:
            mapped[key] = chr(65 + next(iter(indexes)))
    return questions, mapped


def main() -> int:
    doc = fitz.open(SOURCE)
    parsed, marked = records(doc)
    expected = 87
    if len(parsed) != expected:
        raise RuntimeError(f"Expected {expected} questions, parsed {len(parsed)}")
    questions: list[Question] = []
    marked_count = derived_count = 0
    for item in parsed:
        key = (item["quiz"], item["local"])
        correct = marked.get(key)
        provenance = "marked" if correct else "derived"
        if not correct:
            choices = DERIVED.get(item["quiz"], [])
            if item["local"] > len(choices) or not choices[item["local"] - 1]:
                raise RuntimeError(f"No marked or derived answer for quiz {key}")
            correct = choices[item["local"] - 1]
        if provenance == "marked":
            marked_count += 1
            exp = None
        else:
            derived_count += 1
            exp = "No embedded source key/highlight was available for this item; answer derived from the corresponding source lecture and must be spot-checked before Excel."
        options = [value for value in item["options"] if value.strip(" .;-—")]
        questions.append(
            Question(
                stem=" ".join(item["stem"]),
                options=options,
                correct=correct,
                source=provenance,
                exp=exp,
                tag="Department, QBank, Physiology",
                tag_suggere="Physiology",
            )
        )
    count = write_markdown(
        OUTPUT,
        "Source 28 — Physiology question bank MCQ",
        {
            "Source file": "Raw_PDF_Questions/CNS/physiology Qs bank MCQ.pdf",
            "Type": "Department physiology MCQ bank organized into 21 quizzes",
            "Pages": len(doc),
            "Tag": "Department, QBank, Physiology",
            "tagSuggere": "Physiology",
            "Year": "None",
            "Answer source": f"marked:{marked_count}; derived:{derived_count}",
            "Note": "Source option labels restart/mislabel in Quizzes 16, 19, and 21; options were repacked by source order. Derived answers require final spot-check.",
        },
        questions,
    )
    print(f"wrote {count}; marked={marked_count}; derived={derived_count}; Arabic=0 (cleaner enforced)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
