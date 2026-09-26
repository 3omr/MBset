#!/usr/bin/env python3
"""Extract the four visible MCQs from the supplied Final 2024 page image."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "04_Final_2024_page1.md"

ITEMS = [
    (
        "A 14-year-old boy is brought to the emergency room following an accident in which he hit his head against a concrete wall. He was initially unconscious but then regained alertness and minutes later became comatose. A radiograph reveals a linear skull fracture of the left temporal-parietal region. Which condition is most likely to develop?",
        ["Subdural hematoma", "Epidural hematoma", "Ruptured berry aneurysm", "Contusion of frontal lobes", "Sagittal sinus thrombosis"],
        "B",
    ),
    (
        "A 32-year-old woman presents with a 2-day history of headache, vomiting, and fever. Examination reveals neck rigidity. Lumbar puncture demonstrates abundant neutrophils and decreased glucose. Which is the most common route of spread of infection to the brain?",
        ["Via venous route", "Via arterial route", "Via lymphatics", "Along nerves", "Via skin"],
        "B",
    ),
    (
        "Given the preceding clinical scenario, which of the following is not a complication of that condition?",
        ["Communicated hydrocephalus", "Noncommunicating hydrocephalus", "Brain abscess", "Thrombophlebitis", "Compression of nerves"],
        "B",
    ),
    (
        "A 30-year-old woman presents to the emergency room complaining of the worst headache of her life. Imaging studies reveal subarachnoid hemorrhage, and an angiogram shows a saccular aneurysm. Which best describes the pathogenesis of aneurysm formation?",
        ["Atherosclerosis", "Bacterial infection", "Congenital weakness", "Diabetes mellitus", "Systemic hypertension"],
        "C",
    ),
]


def main() -> int:
    questions = [
        Question(
            stem=stem,
            options=options,
            correct=answer,
            source="marked",
            exp="Answer transcribed from the handwritten circle on the supplied exam image.",
            tag="Exams, Final 2024",
            year=2024,
        )
        for stem, options, answer in ITEMS
    ]
    count = write_markdown(
        OUTPUT,
        "Source 04 — Final 2024 page 1",
        {
            "Source file": "Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/Final 2024.jpg",
            "Type": "Assiut end-of-block exam page image, marked MCQs",
            "Pages": 1,
            "Total questions": len(questions),
            "Answer source": f"marked:{count if False else len(questions)} (handwritten circles)",
            "Tag": "Exams, Final 2024",
            "Year": 2024,
            "Note": "The fifth option of Q4 continues at the top of the paired source image final 2024(1).jpg and was restored here to preserve the complete source item.",
        },
        questions,
    )
    print(f"wrote {count}; marked={count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
