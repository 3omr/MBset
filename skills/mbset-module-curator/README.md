# MBset Medical Module Curator Skill Package

Standard Operating Procedure (SOP) and automated toolkit for curating, extracting, verifying and building **MBset** medical question banks and lecture curricula.

**Version 2** — adds source-inventory reconciliation, format-aware extraction (column detection, OCR repair, figure cropping), answer-key provenance with a statistical bias gate, and a forensic bank auditor. PaddleOCR is a fallback for pages with low Tesseract confidence (see `legacy/`). See `SKILL.md` and `references/pipeline-v2.md`.

---

## 📦 Package Contents

```text
mbset-module-curator/
├── SKILL.md                              # agent skill definition & complete SOP
├── README.md                             # installation and usage
├── references/
│   ├── setup-guide.md                    # install + connect your own Telegram (EN / AR)
│   ├── extraction-playbook.md            # format triage, columns, OCR, Moodle, figures
│   ├── answer-key-verification.md        # provenance labels + statistical bias gate
│   ├── schema-31-columns.md              # canonical schema + legacy migration map
│   ├── noise-removal-and-curation.md     # noise regex catalog + notation repair
│   ├── tagging-and-naming.md             # Damietta & Assiut tagging taxonomies
│   └── subcategories-and-lectures.md     # lecture PDF merging & renaming guide
├── legacy/                               # one-off tools, not part of the pipeline
│   ├── extract_pdf_columns.py            # column-aware PDF text extraction (inspection)
│   ├── ocr_paddle_pages.py               # PaddleOCR fallback for low-confidence pages
│   └── smart-ocr-workflow.md             # how to run and reconcile the PaddleOCR fallback
└── scripts/
    ├── mbset.py + mbset/                 # the pipeline CLI (telegram → inventory → ocr → route → parse/transcribe → check → build)
    ├── clean_markdown_noise.py           # deep noise removal
    ├── install.sh                        # optional ahead-of-time setup (the skill also self-installs)
    ├── requirements.txt / requirements-telegram.txt
    ├── build_module_template.py          # markdown -> canonical 32-column Excel
    ├── validate_questions_excel.py       # schema gate
    └── audit_question_bank.py            # forensic gate (keys, dups, noise, images)
```

---

## 🚀 Installation (anyone)

1. Copy this folder to `~/.claude/skills/mbset-module-curator/` (Claude Code), `<project>/.agents/skills/`
   (Codex and other agents) or `~/.gemini/antigravity/skills/` (Antigravity).
2. That's it — the skill sets itself up: the first `mbset.py doctor --fix` (the agent runs it) installs the
   Python packages into `<skill>/.venv` and the OCR/PDF tools (apt / brew / dnf; Windows: WSL). To do it
   ahead of time: `bash scripts/install.sh [--telegram]`.
3. Optional — Telegram: run `python3 scripts/mbset.py telegram setup` **yourself** once, with your own
   account (API id/hash from my.telegram.org).

Full guide in English and Arabic: [`references/setup-guide.md`](references/setup-guide.md).

---

## 🛠️ Pipeline in commands

```bash
# Stages 0-1 — inventory, OCR and parse every source (the parser writes the markdown)
S=<skill>/scripts/mbset.py
python $S inventory "$M" && python $S ocr "$M" && python $S parse "$M"
python $S check "$M"          # the gate; see SKILL.md for the review loop
# PaddleOCR fallback for low-confidence pages only: legacy/smart-ocr-workflow.md

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
