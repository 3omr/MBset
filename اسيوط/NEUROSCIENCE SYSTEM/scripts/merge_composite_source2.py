#!/usr/bin/env python3
"""Merge the disjoint local extractions of composite source #2.

The composite PDF contains several exams and repeated page copies.  Each
worker writes a staging Markdown file for a disjoint page range; this script
combines those ranges into the one source-to-one-Markdown deliverable while
keeping each source block intact.  Final normalized-stem deduplication is
performed by export_question_payload.py.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "Markdown_Questions"
OUT = MD / "02_All_CNS_midterm_final_Assuit.md"
STAGE = ROOT.parents[1] / "scratch" / "neuroscience_source2_staging"
BLOCK_RE = re.compile(r"^###\s*Q(?P<num>\d+)\s*:\s*.*?(?=^###\s*Q\d+\s*:|\Z)", re.S | re.M)


def blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(0).strip() for match in BLOCK_RE.finditer(text)]


def staged(name: str) -> Path:
    path = MD / name
    return path if path.is_file() else STAGE / name


def section_blocks(path: Path, fragment: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    for section in re.split(r"^##\s+", text, flags=re.M):
        lines = section.splitlines()
        if lines and fragment in lines[0]:
            return [match.group(0).strip() for match in BLOCK_RE.finditer(section)]
    return []


def renumber(block: str, number: int) -> str:
    return re.sub(r"^###\s*Q\d+\s*:", f"### Q{number}:", block, count=1, flags=re.M)


def main() -> None:
    required = [
        staged("02A_CNS_composite_p12_18.md"),
        staged("02C_CNS_composite_p98_116.md"),
        staged("02D_CNS_composite_p117_125.md"),
        staged("02E_CNS_composite_p19_63.md"),
    ]
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise SystemExit("missing staging files: " + ", ".join(missing))

    # The existing handoff's first 68 blocks are the verified p2-11 copy of
    # source #5.  Its next 44 blocks are the verified p64-73 written copy of
    # source #6.  Its final 55 blocks were incorrectly mapped to p98-116 and
    # are deliberately not reused; the dedicated 02C extraction replaces it.
    old = blocks(MD / "02_All_CNS_midterm_final_Assuit.md")
    p64_written = section_blocks(MD / "02_All_CNS_midterm_final_Assuit.md", "PDF pages 64–73")
    if not p64_written:
        if len(old) < 112:
            raise SystemExit(f"existing handoff has {len(old)} blocks; expected at least 112")
        p64_written = old[68:112]

    sections: list[tuple[str, list[str]]] = [
        ("PDF pages 2–11 (same exam as source #5; retained for composite coverage)", blocks(MD / "05_Mid_exam_2020.md")),
        ("PDF pages 12–18 (Final Exam Form A, 30/12/2020)", blocks(staged("02A_CNS_composite_p12_18.md"))),
        ("PDF pages 19–63 (Top Team CNS bank and Final Exam 18/4/2021; local extraction)", blocks(staged("02E_CNS_composite_p19_63.md"))),
        ("PDF pages 64–73 (verified written copy retained from the prior handoff)", p64_written),
        ("PDF pages 98–116 (Final Reset/Summer 15/5/2022 and Final 18/12/2022)", blocks(staged("02C_CNS_composite_p98_116.md"))),
        ("PDF pages 117–125 (Final 18/12/2022 MCQ first copy)", blocks(staged("02D_CNS_composite_p117_125.md"))),
    ]

    total = sum(len(items) for _, items in sections)
    output: list[str] = [
        "# Source 2 — All CNS midterm and final exams Assiut (complete composite reconciliation)",
        "",
        "- **Source file:** Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/All CNS midterm and final exams Assuit.pdf",
        "- **PDF pages:** 136",
        "- **Extraction policy:** Local PDF text extraction and OCR/visual checks only; no transcriber, NotebookLM, or audio transcription.",
        "- **Processed ranges:** 2–11, 12–18, 19–63, 64–73, 74–97, 98–116, and 117–125.",
        "- **Explicit duplicate exclusion:** pages 74–97 repeat the readable Final 2020/2021 MCQ set covered by the local pages 21–34 extraction; pages 126–136 repeat the MCQ set beginning on pages 117–125. Neither repeated range is emitted twice.",
        "- **Deduplication:** source-range records are retained for provenance; final normalized-stem deduplication is measured by `export_question_payload.py`.",
        f"- **Merged Markdown records:** {total}",
        "- **Note:** Some worker ranges intentionally exclude exact duplicates already represented by another source file; those exclusions are documented in each staging header and do not remove coverage from the final normalized master bank.",
        "",
    ]

    number = 1
    for label, items in sections:
        output.extend([f"## {label}", ""])
        for item in items:
            output.append(f"<!-- {label} -->")
            output.append(renumber(item, number))
            output.extend(["", "---", ""])
            number += 1
    output.extend([
        "## Composite coverage audit",
        "",
        f"- **Sections merged:** {len(sections)}",
        f"- **Records before final normalized-stem deduplication:** {total}",
        "- **Excluded pages:** 126–136 (duplicate MCQ copy); partial/illegible fragments are recorded in the relevant staging headers.",
        "",
    ])
    OUT.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {total} blocks")


if __name__ == "__main__":
    main()
