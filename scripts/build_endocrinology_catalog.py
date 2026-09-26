#!/usr/bin/env python3
"""Build the Stage 0/Stage 3 source catalog for the Endocrinology module.

The catalog is deliberately conservative: staged Markdown counts are reported
as recoverable counts, while every source without a staged, source-specific
Markdown file remains visibly pending.  Once the module audit reports exist,
their hard-findings status is reflected in the catalog gate.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    import fitz
except ImportError as exc:  # pragma: no cover - dependency is part of MBset
    raise SystemExit("PyMuPDF is required to build the source catalog") from exc


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "أزهر دمياط/Endocrinology"
RAW = MODULE / "Raw_PDF_Questions"
MARKDOWN = MODULE / "Markdown_Questions"
CATALOG = MARKDOWN / "00_CATALOG_OF_ALL_FILES.md"
AUDIT_REPORTS = (MODULE / "markdown_audit.json", MODULE / "excel_audit.json")


# These are the first source-specific Markdown outputs already prepared in the
# scratch work.  The remaining raw files stay pending until their own format
# recipe and answer provenance have been checked.
STAGED: dict[str, str] = {
    "Endocrine WRITTEN Qs part.2.pdf": "01_Endocrine_WRITTEN_Qs_part_2.md",
    "Endocrine WRITTEN Qs part.3.pdf": "02_Endocrine_WRITTEN_Qs_part_3.md",
    "Endocrine mcq الحسين.pdf": "03_Endocrine_mcq_Hussein.md",
    "Metabolic syndrome questions.pdf": "04_Metabolic_syndrome_questions.md",
    "adrenal questions منير.pdf": "05_Adrenal_questions.md",
    "introduction questions منير.pdf": "06_Introduction_questions.md",
    "parathyroid questions منير.pdf": "07_Parathyroid_questions.md",
    "pituitary questions منير.pdf": "08_Pituitary_questions.md",
    "thyroid question منير.pdf": "09_Thyroid_questions.md",
    "اسئلة DM منير.pdf": "10_Diabetes_questions.md",
    "Thyroid Mansoura.pdf": "11_Thyroid_Mansoura.md",
    "mcq kumar endocrine pdf.pdf": "12_Kumar_endocrine.md",
    "اسئله الجراحه كتاب القاهره شابتر الاندوكرين...pdf": "13_Cairo_surgery.md",
    "Lippincott_Illustrated Reviews_Pharmacology_7th(2019) export.pdf": "14_Lippincott_pharmacology.md",
    "mcq on diabetic drugs.docx": "15_Diabetic_drugs_docx.md",
    "اسئله الفارما من ملف د. محمد هشام.pdf": "16_Hesham_pharma.md",
    "2024 formative Endo 1,2 محلول.pdf": "17_Formative_2024.md",
    "Endo  formative 20_21.pdf": "18_Endo_formative_20_21.md",
    "Endocrine formative 2025.pdf": "19_Endocrine_formative_2025.md",
    "Endocrinology Final Exam 2023..pdf": "20_Endocrinology_Final_Exam_2023.md",
    "Final 2022.pdf": "21_Final_2022.md",
    "Final 26.pdf": "22_Final_2026.md",
    "1st Endo Formative  (22-23).PDF": "23_1st_Endo_Formative_22_23.md",
    "2nd Endo Formative  (22- 23) ans.pdf": "24_2nd_Endo_Formative_22_23.md",
    "Mcq, endocrine الموجي أطفال.pdf": "25_Mcq_endocrine_Mogy_Pediatrics.md",
    "Endocrine summtive 2025.pdf": "26_Endocrine_summative_2025.md",
    "end Endocrinology  2023..pdf": "27_End_2023.md",
    "end module endocrine  2021-2022.pdf": "28_End_module_2021_2022.md",
    "end 2024.pdf": "01_End_2024.md",
    "End 2026.pdf": "30_End_2026_EXCLUDED.md",
    "endocrine final 2024.pdf": "31_Endocrine_Final_2024.md",
    "Endocrine surgery.pdf": "32_Endocrine_surgery.md",
    "Schwartz MCQ Principles of Surgery  @AUDatabot (1).pdf": "33_Schwartz.md",
    "أسئلة MCQ د. خالد..pdf": "34_Dr_Khaled_MCQ_EXCLUDED.md",
    "Endocrine WRITTEN Qs part.1.pdf": "36_Endocrine_written_part_1_EXCLUDED.md",
    "Endocrine د.خالد ملونة.pdf": "37_Endocrine_Dr_Khaled_notes_EXCLUDED.md",
    "اندوكراين سنه رابعه.pdf": "38_Endocrine_year4_notes_EXCLUDED.md",
    "اهم اسئلة فالثايرويد.pdf": "39_Important_thyroid_notes_EXCLUDED.md",
    "أسئلة endocrine قديمه...pdf": "40_Old_endocrine_notes_DUPLICATE.md",
    "Surgery & Pediatric.pdf": "41_Surgery_pediatric_notes_EXCLUDED.md",
    "endocrine_باطنة_سنه_رابعه_من_مذكرة_الامتحان.pdf": "42_Endocrine_written_topic_outline_EXCLUDED.md",
}


def page_label(path: Path) -> str:
    if path.suffix.casefold() == ".docx":
        return "DOCX"
    try:
        with fitz.open(path) as document:
            return f"{len(document)} PDF pages"
    except Exception as exc:  # keep inventory visible even if a file is bad
        return f"PDF unreadable ({type(exc).__name__})"


def markdown_counts(path: Path) -> tuple[int, int, int, int]:
    if not path.exists():
        return 0, 0, 0, 0
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = re.findall(r"^### Q\d+:.*?(?=^### Q\d+:|\Z)", text, flags=re.M | re.S)
    qroc = sum(bool(re.search(r"^\*\*Correct Answer:\*\*\s*-$", block, flags=re.M)) for block in blocks)
    mcq = sum(bool(re.search(r"^\*\*Correct Answer:\*\*\s*[A-F]", block, flags=re.M)) for block in blocks)
    multi_key = sum(bool(re.search(r"^\*\*Correct Answer:\*\*\s*[A-F](?:/[A-F])+", block, flags=re.M)) for block in blocks)
    return len(blocks), mcq, qroc, multi_key


def table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def audits_passed() -> bool:
    """Return true only when both audit reports contain no hard findings."""
    import json

    for report in AUDIT_REPORTS:
        if not report.exists():
            return False
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        if data.get("hard"):
            return False
    return True


def main() -> int:
    MARKDOWN.mkdir(parents=True, exist_ok=True)
    sources = sorted(
        (path for path in RAW.iterdir() if path.is_file() and path.suffix.casefold() in {".pdf", ".docx"}),
        key=lambda path: path.name.casefold(),
    )
    rows: list[str] = []
    staged_sources = 0
    excluded_sources = 0
    staged_questions = 0
    staged_mcq = 0
    staged_qroc = 0
    multi_key_total = 0
    audit_ok = audits_passed()

    for index, source in enumerate(sources, start=1):
        target_name = STAGED.get(source.name)
        target = MARKDOWN / target_name if target_name else None
        total, mcq, qroc, multi_key = markdown_counts(target) if target else (0, 0, 0, 0)
        is_excluded = bool(target_name and ("EXCLUDED" in target_name or "DUPLICATE" in target_name))
        if target_name and target and target.exists() and is_excluded:
            excluded_sources += 1
            status = "EXCLUDED — documented"
            status_text = target.read_text(encoding="utf-8", errors="replace")
            note_match = re.search(r"\*\*Status:\*\*\s*EXCLUDED\s*[—-]\s*(.+)", status_text)
            note = note_match.group(1).strip() if note_match else "Explicit exclusion record present."
            target_name = target_name
            total = mcq = qroc = multi_key = 0
        elif target_name and target and target.exists():
            staged_sources += 1
            staged_questions += total
            staged_mcq += mcq
            staged_qroc += qroc
            multi_key_total += multi_key
            status = "STAGED — audit passed" if audit_ok else "STAGED — audit pending"
            note = (
                "Recoverable count; completeness, provenance, noise, and bias audits passed."
                if audit_ok
                else "Recoverable count only; completeness and key verification remain open."
            )
            if source.name == "Endocrine mcq الحسين.pdf":
                note = (
                    "Three source multi-answer keys were normalized as QROC notes; audit passed."
                    if audit_ok
                    else f"{multi_key} multi-answer keys need normalization before Excel."
                )
            elif source.name == "Endocrine WRITTEN Qs part.3.pdf" and total == 0:
                note = "No recoverable explicit block; retained as an auditable zero-count output."
            elif qroc:
                note = (
                    "Contains written items; audit passed."
                    if audit_ok
                    else "Contains written items; model-answer audit remains open."
                )
        else:
            status = "PENDING — source-specific extraction"
            note = "No Markdown output yet; do not infer questions from the filename."
            target_name = "—"

        rows.append(
            "| {index} | `{source}` | {pages} | `{target}` | {total} | {mcq} | {qroc} | {status} | {note} |".format(
                index=index,
                source=table_cell(source.name),
                pages=page_label(source),
                target=target_name,
                total=total,
                mcq=mcq,
                qroc=qroc,
                status=status,
                note=table_cell(note),
            )
        )

    pending_sources = len(sources) - staged_sources - excluded_sources
    lines = [
        "# Endocrinology — source inventory and extraction catalog",
        "",
        "> Stage 0 inventory is exhaustive for `Raw_PDF_Questions`. Staged counts are recoverable Markdown counts; the audit reports beside this catalog are the completeness, provenance, noise, and bias gate.",
        "",
        f"- Raw sources inventoried: **{len(sources)}**",
        f"- Markdown files staged with questions: **{staged_sources}**",
        f"- Explicitly excluded sources: **{excluded_sources}**",
        f"- Sources still pending: **{pending_sources}**",
        f"- Staged recoverable questions: **{staged_questions}** ({staged_mcq} MCQ, {staged_qroc} QROC)",
        f"- Multi-answer keys flagged for normalization: **{multi_key_total}**",
        "",
        "| # | Raw source | Pages / type | Markdown output | Recoverable Qs | MCQ | QROC | Status | Audit note |",
        "|---:|---|---:|---|---:|---:|---:|---|---|",
        *rows,
        "",
        "## Gate status",
        "",
        (
            "**NOT READY FOR EXCEL.** Pending sources, source-specific omissions, multi-answer keys, and answer-key spot checks must be resolved before compilation."
            if pending_sources
            else (
                "**SOURCE INVENTORY COMPLETE; AUDIT PASSED.** All sources have a question Markdown file or an explicit exclusion record, and both module audit reports contain no hard findings."
                if audit_ok
                else "**SOURCE INVENTORY COMPLETE; AUDIT PENDING.** All sources have a question Markdown file or an explicit exclusion record; the Excel gate remains closed until the staged files pass the audits."
            )
        ),
        "",
    ]
    CATALOG.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {CATALOG}")
    print(f"sources={len(sources)} staged={staged_sources} pending={pending_sources} questions={staged_questions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
