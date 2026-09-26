#!/usr/bin/env python3
"""Extract the visible questions from the supplied Final 2024 page 2 image."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "07_Final_2024_page2.md"

ITEMS = [
    (
        "An adult man has long-standing pyrexia of unknown origin, weight loss, and night sweats, followed by manifestations of meningitis that did not respond to treatment and lasted a long time. When examining CSF, what is the most likely cause of meningitis?",
        ["Epidemic cerebrospinal meningitis", "Fungal meningitis", "H. influenzae meningitis", "Tuberculous meningitis", "Viral meningitis"],
        "D",
    ),
    (
        "A 45-year-old woman has recurrent labial vesicular eruptions. She developed manifestations of meningitis just after an attack of fever and vesicular eruption. What is the most likely cause of meningitis?",
        ["Fungal infection", "Herpes viral infection", "Pneumococci", "Staph. aureus", "Tuberculosis"],
        "B",
    ),
    (
        "Which of the following cellular changes accompanies stimulation of alpha-2 adrenoceptors?",
        ["Decreased concentration of cAMP", "Decreased concentration of IP3", "Increased concentration of cGMP", "Increased concentration of cAMP", "Increased concentration of IP3"],
        "A",
    ),
    (
        "Which of the following statements is true about G-protein-coupled receptors?",
        ["Glycine receptors are G-protein-coupled receptors", "Muscarinic receptors are not metabotropic receptors", "It contains five transmembrane hydrophobic sections", "The N-terminal chain is extracellular and the C-terminal chain is intracellular", "Their action is mediated by biochemical processes that produce a fast effect"],
        "D",
    ),
    (
        "A healthy young adult woman presents with meningoencephalitis after swimming and skiing in a freshwater lake six days earlier. Which parasite is most commonly associated with her symptoms?",
        ["Acanthamoeba", "Naegleria fowleri", "Plasmodium falciparum", "Toxoplasma gondii", "Trypanosoma gambiense"],
        "B",
    ),
    (
        "Diagnosis of granulomatous amoebic encephalitis can be made by which of the following techniques?",
        ["Blood culture on NNN media", "Biopsy of skin sores may detect bradyzoite cysts", "Culture of CSF in nutrient agar plates to detect cyst stages", "Stained CSF specimens can reveal trophozoites with acanthopodia", "Thin blood smears show pleomorphic flagellates"],
        "D",
    ),
    (
        "An HIV-infected patient develops symptoms suggestive of encephalitis. Lumbar puncture and CSF analysis are performed. Which parasitic stages are most likely to be detected?",
        None,
        "-",
    ),
]


def main() -> int:
    questions = []
    for stem, options, answer in ITEMS:
        if options is None:
            questions.append(
                Question(
                    stem=stem,
                    options=None,
                    correct="-",
                    source="derived",
                    exp="The supplied page ends after option C, so the option set and any answer mark are incomplete; no safe answer is assigned without inventing the missing source content.",
                    tag="Exams, Final 2024",
                    year=2024,
                )
            )
        else:
            questions.append(
                Question(
                    stem=stem,
                    options=options,
                    correct=answer,
                    source="marked",
                    exp="Answer transcribed from the handwritten circle on the supplied exam image.",
                    tag="Exams, Final 2024",
                    year=2024,
                )
            )
    count = write_markdown(
        OUTPUT,
        "Source 07 — Final 2024 page 2",
        {
            "Source file": "Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/final 2024(1).jpg",
            "Type": "Assiut end-of-block exam page image, marked MCQs",
            "Pages": 1,
            "Total questions": len(questions),
            "Answer source": "marked:6; derived:1 unresolved incomplete source item",
            "Tag": "Exams, Final 2024",
            "Year": 2024,
            "Note": "Q11 is retained as a written conversion because the single supplied page cuts off its option list after C.",
        },
        questions,
    )
    print(f"wrote {count}; marked=6; derived=1; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
