#!/usr/bin/env python3
"""Source 11: convert the printed CNS definition table into QROC items.

The source is a digital two-column table.  The parser uses word coordinates to
keep wrapped definitions attached to the correct term; it does not rely on the
interleaved plain-text order.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lib_md import Question, clean, write_markdown  # noqa: E402


MODULE = HERE.parent
SOURCE = MODULE / "Raw_PDF_Questions/CNS/CNS definitions.pdf"
OUTPUT = MODULE / "Markdown_Questions/11_CNS_definitions.md"


def _line_words(words: list[tuple]) -> list[list[tuple]]:
    """Group words into visual lines by their y coordinate."""
    lines: list[list[tuple]] = []
    for word in sorted(words, key=lambda item: (item[1], item[0])):
        if not lines or abs(word[1] - lines[-1][0][1]) > 1.2:
            lines.append([word])
        else:
            lines[-1].append(word)
    return lines


def extract_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    document = fitz.open(SOURCE)
    for page_number, page in enumerate(document, 1):
        words = [word for word in page.get_text("words") if word[1] < page.rect.height - 35]
        current_name: str | None = None
        current_definition: list[str] = []
        for line in _line_words(words):
            left = [word for word in line if word[0] < 260]
            right = [word for word in line if word[0] >= 260]
            left_text = " ".join(word[4] for word in left).strip()
            right_text = " ".join(word[4] for word in right).strip()

            # Skip title/byline/table-header material on page 1.
            if page_number == 1 and line[0][1] < 115:
                continue
            if left_text and re.fullmatch(r"\d{1,3}", left_text):
                continue
            if left_text:
                if current_name and current_definition:
                    pairs.append((current_name, " ".join(current_definition)))
                current_name = left_text
                current_definition = []
            if right_text and current_name:
                current_definition.append(right_text)
        if current_name and current_definition:
            pairs.append((current_name, " ".join(current_definition)))

    cleaned: list[tuple[str, str]] = []
    for name, definition in pairs:
        name = clean(name) or ""
        definition = clean(definition) or ""
        name = re.sub(r"\s*-\s*\s*-\s*$", "", name).strip()
        if name and definition and name.lower() not in {"scientific name", "definition"}:
            cleaned.append((name, definition.rstrip(" .")))
    return cleaned


def main() -> None:
    pairs = extract_pairs()
    questions = [
        Question(
            f"Define {name}.",
            options=None,
            correct="-",
            source="key",
            exp=definition,
            tag="Department, QBank, General 2024",
            year=2024,
        )
        for name, definition in pairs
    ]
    metadata = {
        "Source file": "Raw_PDF_Questions/CNS/CNS definitions.pdf",
        "Type": f"Digital two-column definition table, {len(fitz.open(SOURCE))} pages",
        "Tag": "Department, QBank, General 2024",
        "tagSuggere": "None",
        "Year": "2024",
        "Answer source": "key — the model definitions are printed in the source table",
    }
    count = write_markdown(OUTPUT, "Source 11 — CNS definitions", metadata, questions)
    print(f"source 11: {count} questions (0 MCQ / {count} written)")
    print(f"  counters: definition rows in source = {len(pairs)}, ### Q = {count}")
    print("  answer sources: key:", count)
    print("  Arabic characters:", sum(bool(re.search(r"[\u0600-\u06ff]", name + definition)) for name, definition in pairs))
    for i, (name, definition) in enumerate(pairs, 1):
        print(f"  {i:02d}. {name} -> {definition}")


if __name__ == "__main__":
    main()
