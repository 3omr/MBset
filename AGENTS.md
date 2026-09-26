# MBset Project Guidelines & Instructions

This repository manages medical modules, lecture curricula, and question banks for the **MBset** educational platform (tailored to Faculty of Medicine, Al-Azhar University, Damietta; Assiut-sourced material is also supported).

---

## 1. Skill Reference
All standard workflows, scripts, and specifications are packaged in the workspace skill:
* **Skill Name**: `mbset-module-curator`
* **Skill Path**: [.agents/skills/mbset-module-curator/SKILL.md](file:///.agents/skills/mbset-module-curator/SKILL.md)
* Mirrored copy: `skills/mbset-module-curator/` (keep both in sync)

**Prime directive**: a module is finished only when every question in every source file is in the master Excel, with the answer the source actually gives. Both are proven by measurement, never asserted.

---

## 2. Core Constraints & Rules

### A. Question Bank Schema (31 Columns)

The canonical, platform-accepted header is exactly:

```
id, Cas, Text, Image, explanationImage, A, B, C, D, E, F,
A_EXP, B_EXP, C_EXP, D_EXP, E_EXP, F_EXP, Correct, Hint, EXP, Note, Type,
categoryId, categoryName, subcategoryId, subcategoryName,
tagSuggere, Year, Tag, ImageMasks, ExplanationImageMasks
```

1. **`id` (Col 0)**: MUST be empty (`None`). The platform generates IDs on upload.
2. **`subcategoryId` & `subcategoryName` (Cols 24-25)**: MUST be empty (`None`) for question banks.
3. **`Type` (Col 21)**: `QCS` (MCQ) or `QROC` (written/short answer).
4. **`Correct` (Col 17)**: `QCS` → one uppercase `A`-`F` that exists among the populated options. `QROC` → strict hyphen `-`.
5. **`EXP` (Col 19)**: `QCS` → explanation. `QROC` → **full model answer**.
6. **`Image` (Col 3)**: MUST be filled for figure-dependent questions (`Images/<NN>_<Qn>.png`). A stem that refers to a figure with an empty `Image` is a defect, not an acceptable compromise.
7. **`tagSuggere` (Col 26)**: discipline name for department/professor sources; `None` for general exams.
8. **`Year` (Col 27)**: exact integer from the source file/filename.
9. **`Tag` (Col 28)**:
   - **Damietta**: `Department, <Subject> <Year>` · `Exams, End|Final <Year>` · `Exams, Formative <Year>` (Formative 1 and 2 of a year share one tag) · `Professor, Dr <Name> <Year>` · `External, <Source> <Year>`
   - **Assiut**: `Exams, Midterm|Final <Year>` · `Department, QBank, <Subject> <Year>` · `Department, Quizzes, Week <N>` · `Department, Formative, Week <N>` · `Department, GDs, <Subject> GD <N> <Year>` · `External, <Source> <Year>` (Quizzes and Formatives carry **no year** unless it is in the source filename)
   - Overlaps: merged comma-separated string, unique tags only.
   - One canonical spelling per professor across all tags (`Dr elmorshdy` and `Dr Morshdy` in filenames are the same person → `Professor, Dr Elmorshdy <Year>`), and one tag per formative year regardless of round.
10. **Legacy layout**: `Genetics_Questions.xlsx` and `POD_Questions.xlsx` use an older 31-column header (`category`, `title`, `justification`, `difficulty`, `importance`, `repetition`, `verified`). Do not produce it; migrate per `references/schema-31-columns.md` when touching those modules.

### B. Text Cleaning & Deep Noise Removal
- **Zero Arabic characters** (`[؀-ۿ]`) anywhere in stems, options or explanations.
- Strip leading numbering (`1.`, `25-`, `Q1:`, `### Q10:`, `[MCQ]`) and invisible unicode (`​`, `﻿`, `\xa0`).
- Purge Moodle chrome and footers, mobile screenshot status bars and LMS buttons, trailing chapter answer-key grids, `TABLE n A B` headers, bubble artifacts (`@©`, `®@`), and Franco-Arab OCR gibberish.
- Convert inline `Select one: a. … b. …` runs into structured options; decouple the preceding question's explanation from the next stem.
- **Repair medical notation** rather than deleting it: `Ca**` → `Ca²⁺`, `Na*` → `Na⁺`, `B1` → `β1`, `um` → `µm`, `->` → `→`.
- Options must start at `A` and run sequentially with no gaps; when repacking, move `Correct` with them.
- Do **not** strip numbered lists inside a `QROC` model answer, or trailing `...` in fill-in-the-blank stems.

### C. Question Bank Pipeline (Stage 0 → Stage 4)
1. **Stage 0 — Source inventory & reconciliation**: expand every archive; list every source with its page count; `count(sources) == count(markdown files)`; an intentionally skipped source is logged `EXCLUDED — <reason>`. No silent omissions.
2. **Stage 1 — Format-aware 1-to-1 markdown extraction**: run the pipeline `scripts/mbset.py` (`inventory` → `ocr` → `parse`). Triage is automatic and every source gets its own parser profile (`.mbset/profiles/NN.yaml`) matching its format (digital single/multi-column, scanned, Moodle, screenshots, DocReader, slides, docx); the parser, not the model, writes the markdown. **Never type question text from memory or paraphrase it** — when a file is misread, fix its profile and re-parse; when single questions are misread (missing option, OCR symbols, disordered words), re-read the page image and write exactly what is printed with `mbset.py fix NN --text-file` (logged with the original text). Multi-column pages are split per column automatically (`pdftotext -layout` merges columns and destroys stems). Section-restarting numbering, figures (`mbset.py figures`) and inline options are handled by the parser. No placeholder answers, no invented options.
3. **Stage 2 — Answer-key provenance & verification**: keys, marks and online quizzes are read automatically; pen-marked scans are answered visually in batches (`mbset.py answersheet` → `mbset.py fix --answers … --source marked`). Every MCQ carries `**Answer Source:**` (`key` / `marked` / `online` / `derived`); `derived` is reported to the user with counts. **Statistical bias gate**: for any file with ≥15 MCQs, a single answer letter above 45% is investigated and above 60% fails — that is how ~1,100 CNS questions ended up keyed 84-100% `A`. Spot-check `max(5, 10%)` answers per file against the source (`mbset.py spotcheck` → `mbset.py review --spot`).
4. **Stage 3 — Forensic completeness audit (pre-Excel gate)**: maintain `Markdown_Questions/00_CATALOG_OF_ALL_FILES.md`; three independent counters (source numbering, option-A blocks, `### Q` headings) must agree; declared source totals win. **STOP** — no Excel work until every markdown file passes; `mbset.py check` is this gate (0 hard failures).
5. **Stage 4 — Master Excel compilation & validation**: `mbset.py build` runs the chain below and refuses while `check` fails. Compile with `scripts/build_module_template.py`, deduplicate normalized stems (zero may remain), then gate with `scripts/validate_questions_excel.py` **and** `scripts/audit_question_bank.py --by-tag`. Both must exit clean.

### D. Two-Phase Workflow for New Modules
1. **Phase 1 — `subcategories_<Module>.xlsx`**: scan the schedule, build the lectures file with `categoryId` & `subcategoryId` empty, present the lecture breakdown, then **STOP & WAIT** for the user to upload it so the platform generates IDs.
2. **Phase 2 — Renaming & compilation**: adopt the platform export `subcategories_<Module>_<Date>.xlsx` as the single source of truth, delete temporary files, rename lecture PDFs to `Lectures/<subcategoryId>.pdf`, and build the question bank via Stage 0-4.

### E. Deliverables per Module
```
<Module>/
├── subcategories_<Module>_<Date>.xlsx   # official platform export
├── <Module>_Questions.xlsx              # master 31-column bank (canonical header)
├── Lectures/<subcategoryId>.pdf         # one PDF per subcategory
├── Raw_PDF_Questions/                   # every source, archives expanded
├── Markdown_Questions/00_CATALOG_OF_ALL_FILES.md + <NN>_<Source>.md
└── Images/<NN>_<Qn>.png                 # figures for figure-dependent questions
```
