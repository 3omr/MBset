# MBset Medical Module Curator Skill Package

Standard Operating Procedure (SOP) and automated toolkit for curating, extracting, verifying and building **MBset** medical question banks and lecture curricula.

**Version 2** — adds source-inventory reconciliation, format-aware extraction (column detection, OCR repair, figure cropping), answer-key provenance with a statistical bias gate, and a forensic bank auditor. Scanned sources can also use the optional confidence-aware PaddleOCR pass. See `SKILL.md` §5 and `references/smart-ocr-workflow.md`.

---

## 📦 Package Contents

```text
mbset-module-curator/
├── SKILL.md                              # agent skill definition & complete SOP
├── README.md                             # installation and usage
├── references/
│   ├── extraction-playbook.md            # format triage, columns, OCR, Moodle, figures
│   ├── smart-ocr-workflow.md             # PaddleOCR confidence, positions, review
│   ├── answer-key-verification.md        # provenance labels + statistical bias gate
│   ├── schema-31-columns.md              # canonical schema + legacy migration map
│   ├── noise-removal-and-curation.md     # noise regex catalog + notation repair
│   ├── tagging-and-naming.md             # Damietta & Assiut tagging taxonomies
│   └── subcategories-and-lectures.md     # lecture PDF merging & renaming guide
└── scripts/
    ├── extract_pdf_columns.py            # column-aware PDF text extraction
    ├── clean_markdown_noise.py           # deep noise removal
    ├── ocr_paddle_pages.py               # optional confidence-aware OCR drafts
    ├── build_module_template.py          # markdown -> canonical 31-column Excel
    ├── validate_questions_excel.py       # schema gate
    └── audit_question_bank.py            # forensic gate (keys, dups, noise, images)
```

---

## 🚀 Installation

* **Claude Code / Cowork workspace**: `<repo_root>/.agents/skills/mbset-module-curator/` (also mirrored at `<repo_root>/skills/`).
* **Antigravity / Gemini**: `~/.gemini/antigravity/skills/mbset-module-curator/`.
* **Cursor / custom rules**: keep the folder in the repo and reference `SKILL.md`.

### Dependencies
```bash
pip install openpyxl
sudo apt-get install poppler-utils      # pdftotext, pdfinfo, pdftoppm, pdfimages
pip install pymupdf                     # optional: lecture PDF merging
```

For the optional PaddleOCR pass, use the isolated `.venv-smart-ocr/` environment documented in `references/smart-ocr-workflow.md`. The base MBset requirements do not include PaddleOCR.

---

## 🛠️ Pipeline in commands

```bash
# Stage 1 — extract one markdown per source
# Optional Smart OCR pass for image-only or weakly recognized scans
.venv-smart-ocr/bin/python .agents/skills/mbset-module-curator/scripts/ocr_paddle_pages.py "Raw_PDF_Questions/Scan.pdf" --output-dir /tmp/mbset-smart-ocr
# Inspect the page images and confidence flags before turning OCR text into questions.

python scripts/extract_pdf_columns.py "Raw_PDF_Questions/End 2023.PDF" --probe
python scripts/extract_pdf_columns.py "Raw_PDF_Questions/End 2023.PDF" -o /tmp/end2023.txt
#   ... inspect, parse into Markdown_Questions/06_End_2023.md, then:
python scripts/clean_markdown_noise.py --file Markdown_Questions/06_End_2023.md

# Stage 2+3 — provenance, bias and completeness gates (before any Excel)
python scripts/audit_question_bank.py --markdown Markdown_Questions

# Stage 4 — compile and gate the master Excel
python scripts/build_module_template.py \
    --markdown Markdown_Questions --catalog Markdown_Questions/00_CATALOG_OF_ALL_FILES.md \
    --category-id DamiettaFa_CVS --category-name CVS --out CVS_Questions.xlsx
python scripts/validate_questions_excel.py CVS_Questions.xlsx
python scripts/audit_question_bank.py --excel CVS_Questions.xlsx --by-tag
```

Both gates must exit 0 before the file goes to the platform.

---

## ⚠️ The three rules that matter most

1. **Never invent an answer.** Every MCQ carries `**Answer Source:**` (`key` / `marked` / `online` / `derived`), and `derived` is reported to the user with counts.
2. **Never trust `-layout` on a multi-column PDF.** Detect the split and extract per column, or questions silently merge into each other.
3. **Never skip a source.** Every file in `Raw_PDF_Questions/` (archives expanded) appears in the catalog, either extracted or explicitly `EXCLUDED — <reason>`.
