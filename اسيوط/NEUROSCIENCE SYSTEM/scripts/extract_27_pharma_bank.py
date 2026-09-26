#!/usr/bin/env python3
"""Source 27: Pharmacology question bank.

The PDF contains two MCQ sections with highlighted answers and two printed
short-answer sections.  MCQ keys are recovered from the source's yellow drawing
rectangles, not guessed from medical knowledge.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lib_md import Question, clean, clean_option, clean_stem, write_markdown  # noqa: E402


MODULE = HERE.parent
SOURCE = MODULE / "Raw_PDF_Questions/CNS/pharma Qs bank.pdf"
OUTPUT = MODULE / "Markdown_Questions/27_Pharmacology_Qs_bank.md"
TAG = "Department, QBank, Pharmacology"


@dataclass
class Line:
    text: str
    page: int
    bbox: fitz.Rect


@dataclass
class ParsedMCQ:
    source_number: int
    stem_lines: list[str] = field(default_factory=list)
    options: list[str] = field(default_factory=list)
    option_bboxes: list[list[tuple[int, fitz.Rect]]] = field(default_factory=list)


QSTART = re.compile(r"^\s*(\d+)\s*[.)-]\s*(.*)$")
OPTSTART = re.compile(r"^\s*([A-Fa-f])\s*[.)-]\s*(.*)$")


def visual_lines(page: fitz.Page, page_number: int) -> list[Line]:
    groups: dict[tuple[int, int], list[tuple]] = {}
    for word in page.get_text("words"):
        groups.setdefault((word[5], word[6]), []).append(word)
    result: list[Line] = []
    for words in groups.values():
        words = sorted(words, key=lambda word: word[0])
        text = " ".join(word[4] for word in words).strip()
        if not text:
            continue
        result.append(
            Line(
                text=text,
                page=page_number,
                bbox=fitz.Rect(
                    min(word[0] for word in words),
                    min(word[1] for word in words),
                    max(word[2] for word in words),
                    max(word[3] for word in words),
                ),
            )
        )
    return sorted(result, key=lambda line: (line.bbox.y0, line.bbox.x0))


def yellow_rects(page: fitz.Page) -> list[fitz.Rect]:
    result = []
    for drawing in page.get_drawings():
        fill = drawing.get("fill")
        if fill and fill[0] > 0.9 and fill[1] > 0.75 and fill[2] < 0.65:
            result.append(fitz.Rect(drawing["rect"]))
    return result


def _split_inline_options(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split a rare question line that starts its first option on the same line."""
    matches = list(re.finditer(r"\s+([A-Fa-f])\s*[.)]\s+", text))
    if not matches or matches[0].start() < 18:
        return text, []
    stem = text[: matches[0].start()].strip()
    pairs = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pairs.append((match.group(1).upper(), text[match.end() : end].strip()))
    return stem, pairs


def _placeholder(option: str) -> bool:
    return bool(re.fullmatch(r"[-–—.]+", (option or "").strip()))


def parse_mcq_pages(document: fitz.Document, page_numbers: range) -> list[ParsedMCQ]:
    questions: list[ParsedMCQ] = []
    current: ParsedMCQ | None = None
    expected_label = "A"

    def flush() -> None:
        nonlocal current
        if current and current.stem_lines and current.options:
            questions.append(current)
        current = None

    stop = False
    for page_number in page_numbers:
        page = document[page_number - 1]
        lines = visual_lines(page, page_number)
        yellows = yellow_rects(page)
        for line in lines:
            text = line.text
            if text.lower().startswith("answer the following short essay"):
                stop = True
                break
            if text in {"Questions", "Select the best answer:", "Select the correct answer:"}:
                continue
            if re.fullmatch(r"\d{1,3}", text):
                continue
            qmatch = QSTART.match(text)
            if qmatch:
                flush()
                current = ParsedMCQ(int(qmatch.group(1)))
                expected_label = "A"
                stem, inline = _split_inline_options(qmatch.group(2))
                current.stem_lines.append(stem)
                for label, option in inline:
                    if not _placeholder(option):
                        current.options.append(option)
                        current.option_bboxes.append([(page_number, line.bbox)])
                        expected_label = chr(ord(expected_label) + 1)
                continue

            omatch = OPTSTART.match(text)
            if omatch and current is not None:
                label, option = omatch.group(1).upper(), omatch.group(2).strip()
                # One source line around Q19 was exported with duplicated labels:
                # "A. B. Scopolamine", "B. C. Dexmedetomidine", etc.  The inner
                # label identifies the real option, so remove the outer duplicate.
                inner = re.match(r"^([A-Fa-f])\s*[.)-]\s+(.+)$", option)
                if label != expected_label and inner and inner.group(1).upper() == expected_label:
                    option = inner.group(2)
                    label = expected_label
                if _placeholder(option):
                    expected_label = chr(ord(expected_label) + 1)
                    continue
                current.options.append(option)
                current.option_bboxes.append([(page_number, line.bbox)])
                expected_label = chr(ord(expected_label) + 1)
                continue

            if current is None:
                continue
            if current.options:
                current.options[-1] += " " + text
                current.option_bboxes[-1].append((page_number, line.bbox))
            else:
                current.stem_lines.append(text)
        if stop:
            break

    flush()

    for question in questions:
        question.options = [clean_option(option) or "" for option in question.options]
        # The repeated-label repair above handles the only known malformed run;
        # retain the source order and let the Markdown renderer repack labels.
        question.stem_lines = [clean_stem(" ".join(question.stem_lines)) or ""]
    return questions


def marked_answers(document: fitz.Document, questions: list[ParsedMCQ]) -> list[str]:
    answers = []
    for question in questions:
        hits = []
        for index, boxes in enumerate(question.option_bboxes):
            for page_number, bbox in boxes:
                rects = yellow_rects(document[page_number - 1])
                expanded = fitz.Rect(bbox.x0 - 1, bbox.y0 - 1, bbox.x1 + 1, bbox.y1 + 1)
                if any(rect.intersects(expanded) for rect in rects):
                    hits.append(index)
                    break
        if len(set(hits)) != 1:
            raise RuntimeError(f"MCQ {question.source_number}: highlighted options={hits}")
        answers.append(chr(65 + hits[0]))
    return answers


def _plain_lines(document: fitz.Document, first: int, last: int) -> list[str]:
    lines: list[str] = []
    for page_number in range(first, last + 1):
        for line in document[page_number - 1].get_text("text").splitlines():
            text = line.strip()
            if text and not re.fullmatch(r"\d{1,3}", text):
                lines.append(text)
    return lines


def parse_first_written(document: fitz.Document) -> list[tuple[str, str]]:
    rows = _plain_lines(document, 15, 17)
    items: list[tuple[str, list[str]]] = []
    current: tuple[str, list[str]] | None = None
    heading = re.compile(r"^(\d+)\s*-\s*(.+)$")
    for line in rows:
        if line.startswith("Answer the following"):
            continue
        match = heading.match(line)
        if match:
            if current:
                items.append(current)
            current = (match.group(2), [])
        elif current:
            current[1].append(line)
    if current:
        items.append(current)
    return [(stem, " ".join(answer)) for stem, answer in items]


def parse_second_written(document: fitz.Document) -> list[tuple[str, str]]:
    rows = _plain_lines(document, 23, 25)
    expected = list(range(1, 14)) + list(range(15, 38))
    next_index = 0
    items: list[tuple[str, list[str]]] = []
    current: tuple[str, list[str]] | None = None
    heading = re.compile(r"^(\d{1,2})\s*[-.)]\s*(.+)$")
    for line in rows:
        if line.startswith("Answer the following"):
            continue
        match = heading.match(line)
        number = int(match.group(1)) if match else None
        if match and next_index < len(expected) and number == expected[next_index]:
            if current:
                items.append(current)
            current = (match.group(2), [])
            next_index += 1
        elif current:
            current[1].append(line)
    if current:
        items.append(current)
    return [(stem, " ".join(answer)) for stem, answer in items]


def fallback_model_answer(stem: str) -> str:
    """Keep a printed answer embedded in a statement when no answer line follows."""
    match = re.search(r"\b(?:is|are)\s+(.+)$", stem, flags=re.I)
    return (match.group(1).strip() if match else stem.strip()) or stem.strip()


def main() -> None:
    document = fitz.open(SOURCE)
    first_mcq = parse_mcq_pages(document, range(1, 15))
    second_mcq = parse_mcq_pages(document, range(18, 24))
    mcqs = first_mcq + second_mcq
    first_answers = marked_answers(document, first_mcq)
    second_answers = marked_answers(document, second_mcq)
    answers = first_answers + second_answers

    if len(first_mcq) != 64 or len(second_mcq) != 27:
        raise RuntimeError(f"unexpected MCQ counts: first={len(first_mcq)}, second={len(second_mcq)}")
    if len(answers) != len(mcqs):
        raise RuntimeError("answer count does not match MCQ count")

    questions: list[Question] = []
    for parsed, correct in zip(mcqs, answers):
        questions.append(
            Question(
                " ".join(parsed.stem_lines),
                parsed.options,
                correct=correct,
                source="marked",
                tag=TAG,
            )
        )

    written = parse_first_written(document) + parse_second_written(document)
    if len(written) != 47:
        raise RuntimeError(f"unexpected written count: {len(written)}")
    for stem, answer in written:
        answer = answer.strip() or fallback_model_answer(stem)
        questions.append(
            Question(stem, options=None, correct="-", source="key", exp=answer, tag=TAG)
        )

    metadata = {
        "Source file": "Raw_PDF_Questions/CNS/pharma Qs bank.pdf",
        "Type": "Marked digital MCQ bank plus two printed short-essay sections, 25 pages",
        "Tag": TAG,
        "tagSuggere": "Pharmacology",
        "Year": "None",
        "Answer source": f"marked: {len(mcqs)} MCQs; key: {len(written)} written model answers",
        "Note": "MCQ numbering restarts at 1 for the second bank; written source omits item 14 in its second section",
    }
    count = write_markdown(OUTPUT, "Source 27 — Pharmacology question bank", metadata, questions)
    print(f"source 27: {count} questions ({len(mcqs)} MCQ / {len(written)} written)")
    print(f"  counters: MCQ blocks in source = {len(mcqs)}, written headings = {len(written)}, ### Q = {count}")
    print(f"  answer sources: marked={len(mcqs)}, key={len(written)}, derived=0")
    print("  answer distribution:", {letter: answers.count(letter) for letter in "ABCDEF" if letter in answers})
    print("  source section numbering: MCQ 1..64 + MCQ 1..27; written 1..11 + 1..13,15..37")
    print("  missing source written item: 14 (preserved as a source gap, not invented)")


if __name__ == "__main__":
    main()
