#!/usr/bin/env python3
"""Create explicit one-to-one records for non-question source files."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions"

RECORDS = [
    ("36_Endocrine_written_part_1_EXCLUDED.md", "Endocrine WRITTEN Qs part.1.pdf", "The scan contains lecture notes/diagrams but no recoverable self-contained question block or answer pair."),
    ("37_Endocrine_Dr_Khaled_notes_EXCLUDED.md", "Endocrine د.خالد ملونة.pdf", "The 64-page file is a colored lecture-note/revision handout; OCR inventory found no reliable numbered question blocks with answer choices."),
    ("38_Endocrine_year4_notes_EXCLUDED.md", "اندوكراين سنه رابعه.pdf", "The file is a lecture/revision note collection, not a self-contained question source; no stable question/answer blocks were recoverable."),
    ("39_Important_thyroid_notes_EXCLUDED.md", "اهم اسئلة فالثايرويد.pdf", "The scan is a topic-summary sheet with fragmented prompts and no recoverable answer-key structure."),
    ("40_Old_endocrine_notes_DUPLICATE.md", "أسئلة endocrine قديمه...pdf", "Duplicate of the endocrine written-topic outline source; excluded after OCR text similarity reconciliation."),
    ("41_Surgery_pediatric_notes_EXCLUDED.md", "Surgery & Pediatric.pdf", "The scan contains diagrams/lecture notes and no recoverable question blocks."),
    ("42_Endocrine_written_topic_outline_EXCLUDED.md", "endocrine_باطنة_سنه_رابعه_من_مذكرة_الامتحان.pdf", "Topic-outline prompts without a source answer key or complete model answers; retained as an explicit exclusion rather than inventing answers."),
    ("34_Dr_Khaled_MCQ_EXCLUDED.md", "أسئلة MCQ د. خالد..pdf", "The four-page scan remains unreadable after OCR: no stable stems/options or answer key can be reconstructed without fabrication."),
    ("32_Endocrine_surgery_EXCLUDED.md", "Endocrine surgery.pdf", "The two-column scan interleaves question text, answer explanations and figures; OCR cannot preserve a reliable 1-to-1 option/key pairing, so it is excluded pending a cleaner source."),
    ("30_End_2026_EXCLUDED.md", "End 2026.pdf", "The PDF is a mixed/incomplete compilation: question numbering restarts across different sheets, several blocks are absent or duplicated, and the scan does not preserve a reliable one-to-one answer sequence."),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, source, reason in RECORDS:
        (OUT / filename).write_text(
            "# Excluded source record\n\n"
            f"**Status:** EXCLUDED — {reason}\n\n"
            "No question rows were created from this source.\n",
            encoding="utf-8",
        )
    print(f"Wrote {len(RECORDS)} explicit exclusion records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
