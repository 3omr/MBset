---
name: mbset-module-curator
description: >-
  Standard operating procedure and toolkit for curating, formatting, and building
  MBset medical modules: source inventory reconciliation, format-aware 1-to-1 markdown
  extraction with confidence-aware OCR and deep noise removal, answer-key provenance and statistical verification,
  image-question handling, lecture PDF management, and 31-column master question bank Excel.
---

# MBset Medical Module Curator Skill

End-to-end standard operating procedure (SOP) for building, formatting, and curating medical academic modules for the **MBset** educational platform (Faculty of Medicine, Al-Azhar University, Damietta; Assiut-sourced material is also supported).

**Prime directive**: a module is finished only when **every question in every source file** is present in the master Excel, **with the answer the source actually gives**. Completeness and answer correctness outrank speed, and both are proven by measurement, never asserted.

---

## 1. Module Overview & Platform Roles

Each module represents an integrated block of medical disciplines (Anatomy, Histology, Physiology, Biochemistry, Microbiology, Parasitology, Pathology, Pharmacology, Behavioral science, Genetics).

### Established Module Identifiers
| Module Name | `categoryId` | Primary Disciplines |
| :--- | :--- | :--- |
| **Normal Human Body (NHB)** | `DamiettaFa_NORMAL_HUMAN_BODY` | Anatomy, Histology, Physiology, Biochemistry |
| **Biomedical** | `DamiettaFa_BIOMEDICAL` | Microbiology, Parasitology |
| **Blood Module** | `DamiettaFa_BLOOD` | Pathology, Pharmacology, Physiology, Histology |
| **Respiratory Module** | `DamiettaFa_RESPIRATORY` | Anatomy, Physiology, Pathology, Pharma |
| **CVS** | `DamiettaFa_CVS` | Anatomy, Histology, Physiology, Micro, Pharma, Biochem |
| **CNS** | `DamiettaFa_CNS` | Anatomy, Histology, Physiology, Micro, Pharma |
| **POD (Principles of Disease)** | `DamiettaFa_POD` | Pathology, Pharmacology |
| **Genetics** | `DamiettaFa_GENETICS` | Biochemistry, Histology |
| **Behavioral Science** | `DamiettaFa_BEHAVIORAL_SCIENCE` | Psychology, Behavioral science |

> Always confirm a module's real `categoryId` / `categoryName` against the module's own `subcategories_<Module>_<Date>.xlsx` platform export before compiling. Never invent one.

---

## 2. Lecture Subcategories & PDF Formatting

### A. Subcategory Planning & Multi-Part Merging
1. **Multi-Part Merging Rule**: Multi-part lectures of the same cohesive topic are merged into a single lecture/subcategory unless the user says otherwise.
   * *Merge Examples*: `Locomotor Joints (1 & 2)`, `Proteins (1 & 2)`, `Autonomic Neurotransmitters & Receptors (1, 2, 3)`.
   * *Keep Separate Examples*: `Systems of the Body (1 & 2)`, `Epithelium (1, 2, 3)`, `Body Fluids & Homeostasis`.
2. **Subcategory ID Convention**: `<categoryId>_<LECTURE_NAME_UPPER_SNAKE_CASE>`
   * Example: `DamiettaFa_NORMAL_HUMAN_BODY_ACTIVE_TRANSPORT_ACROSS_CELL`

### B. Two-Phase Workflow for New Modules
1. **Phase 1 — Initial Lectures File (`subcategories_<Module>.xlsx`)**
   - Scan the module schedule and build the initial lectures Excel file.
   - **`categoryId` & `subcategoryId` MUST be left completely empty (`None`)**.
   - Present a detailed breakdown of all lecture names, subjects, and topics.
   - **PAUSE & STOP**: the user uploads the file so the platform assigns official IDs.
2. **Phase 2 — Post-Upload PDF Renaming & Question Bank Compilation**
   - Adopt the platform export `subcategories_<Module>_<YYYY-MM-DD>.xlsx` as the single source of truth; delete temporary subcategory files.
   - Rename every lecture PDF to `<Module>/Lectures/<subcategoryId>.pdf`.
   - Build the master question bank via the pipeline in Section 5.

### C. Lecture PDFs Organization
```
<Module>/Lectures/<subcategoryId>.pdf
```
The PDF count in `Lectures/` must equal the subcategories count exactly.

---

## 3. The 31-Column Question Bank Schema (Canonical)

The canonical, platform-accepted header — the one used by CVS, CNS, NHB and Behavioral Science — is exactly:

```
id, Cas, Text, Image, explanationImage, A, B, C, D, E, F,
A_EXP, B_EXP, C_EXP, D_EXP, E_EXP, F_EXP, Correct, Hint, EXP, Note, Type,
categoryId, categoryName, subcategoryId, subcategoryName,
tagSuggere, Year, Tag, ImageMasks, ExplanationImageMasks
```

| Col # | Column | Value | Rule |
| :---: | :--- | :--- | :--- |
| **0** | `id` | **Empty** | **CRITICAL**: blank so the platform assigns IDs. |
| **1** | `Cas` | `None` / String | Case scenario / clinical stem. |
| **2** | `Text` | String | **Clean stem**. Zero Arabic, no leading numbering, no invisible unicode, no markdown markers. |
| **3** | `Image` | `None` / path | Filled for figure-dependent questions (Section 5, Stage 1 §7). |
| **4** | `explanationImage` | `None` | Optional explanation image. |
| **5-10** | `A` … `F` | String / `None` | Option text, no `a.` prefixes, starting at `A`, strictly sequential. |
| **11-16** | `A_EXP` … `F_EXP` | `None` | Per-option explanations (usually empty). |
| **17** | `Correct` | String | `QCS`: single uppercase `A`-`F` that **exists** among the populated options. `QROC`: strict hyphen `-`. |
| **18** | `Hint` | `None` | Optional. |
| **19** | `EXP` | String / `None` | `QCS`: explanation. `QROC`: **complete model answer**. |
| **20** | `Note` | `None` | Empty. |
| **21** | `Type` | String | `QCS` (MCQ) or `QROC` (written/short answer). |
| **22** | `categoryId` | String | Module ID. |
| **23** | `categoryName` | String | Module name. |
| **24** | `subcategoryId` | `None` | Blank for bulk question upload. |
| **25** | `subcategoryName` | `None` | Blank for bulk question upload. |
| **26** | `tagSuggere` | String / `None` | Discipline for department/professor sources; `None` for general exams. |
| **27** | `Year` | Integer | Must match the source header/filename exactly. |
| **28** | `Tag` | String | See Section 4. |
| **29-30** | `ImageMasks`, `ExplanationImageMasks` | `None` | Empty. |

> **Legacy variant warning.** Some older banks (`Genetics_Questions.xlsx`, `POD_Questions.xlsx`) use a different 31-column header (`category`, `title`, `image_A`-`image_E`, `justification`, `difficulty`, `importance`, `repetition`, `verified`). That layout is **legacy** — do not produce it for new work, and migrate it when touching those modules. The mapping is in [`references/schema-31-columns.md`](./references/schema-31-columns.md).

---

## 4. Tagging & Naming Conventions

### A. Damietta tag families
| Family | Pattern | `tagSuggere` | Example |
| :--- | :--- | :--- | :--- |
| Department books | `Department, <Subject> <Year>` | `<Subject>` | `Department, Physiology 2026` |
| Past exams (end-round) | `Exams, End <Year>` | `None` | `Exams, End 2025` |
| Past exams (final) | `Exams, Final <Year>` | `None` | `Exams, Final 2023` |
| Formatives | `Exams, Formative <Year>` | `None` | `Exams, Formative 2025` (Formative 1 and 2 of a year share one tag) |
| Professor / doctor collections | `Professor, Dr <Name> <Year>` | `<Subject>` if single-subject | `Professor, Dr Elmorshdy 2025` |
| External (other faculties, outside banks) | `External, <Source> <Year>` | `<Subject>` or `None` | `External, Psycho 404 2026` |

`<Subject>` is always a capitalized standard discipline: `Anatomy`, `Physiology`, `Histology`, `Biochemistry`, `Microbiology`, `Parasitology`, `Pathology`, `Pharmacology`.

### B. Assiut tag families
`Exams, Midterm|Final <Year>` · `Department, QBank, <Subject> <Year>` · `Department, Quizzes, Week <N>` · `Department, Formative, Week <N>` · `Department, GDs, <Subject> GD <N> <Year>` · `External, <Source> <Year>`.
**Quizzes and Formatives carry NO year** unless the year is explicitly in the source filename.

### C. Overlaps
Merge unique tags into one comma-separated string, department/professor tag first, then exams:
`Department, Histology 2026, Exams, End 2025, End 2021`

Full detail: [`references/tagging-and-naming.md`](./references/tagging-and-naming.md).

---

## 5. The Question Bank Curation Pipeline (Stage 0 → Stage 4)

### Stage 0 — Source Inventory & Reconciliation (before any extraction)
1. Expand every archive in the module folder (`.zip`, `.7z`, `.rar`) into `<Module>/Raw_PDF_Questions/`; archives are sources too and are frequently forgotten.
2. List **every** candidate source: `.pdf`, `.PDF`, `.docx`, `.pptx`, `.txt`, `.md`, image folders (`.jpg`/`.png` screenshot sets).
3. Record each with its page/slide count (`pdfinfo`, `pdftotext`) in the catalog skeleton.
4. **Reconciliation rule**: `count(source files) == count(markdown files)`. A source that is intentionally excluded (duplicate of another file, lecture notes with no questions, unreadable scan) must still appear in the catalog with `EXCLUDED — <reason>`. Silent omissions are the single most common way questions go missing.

### Stage 1 — Format-Aware 1-to-1 Markdown Extraction
Every source file becomes exactly one file at `<Module>/Markdown_Questions/<Index>_<SourceName>.md`. No grouping, no merging, no splitting.

1. **Triage first, extract second.** Before writing any extraction code, classify the file — digital single-column, digital multi-column, scanned/OCR, Moodle web export, phone-screenshot set, DocReader export, or slide deck — and use the matching recipe in [`references/extraction-playbook.md`](./references/extraction-playbook.md). For scanned/image-only sources or weak existing OCR, use the confidence-aware PaddleOCR pass in [`references/smart-ocr-workflow.md`](./references/smart-ocr-workflow.md) as an OCR aid. **Never run a generic regex script across several files**; each source has its own quirks.
2. **Multi-column handling is mandatory, not optional.** `pdftotext -layout` interleaves columns and silently destroys stems. Detect columns (see playbook) and extract each column separately with `scripts/extract_pdf_columns.py`, then concatenate in reading order (page 1 col 1, page 1 col 2, page 2 col 1, …).
3. **Section-restarting numbering.** Department books commonly restart numbering per chapter (`1..54`, then `1..12`, then `1..12`). Renumber continuously `Q1..QN` in the markdown, and note each source section boundary in the catalog. Never treat a restart as the end of the file.
4. **Answer extraction, never answer invention.** Every question records where its answer came from (Stage 2). If a source genuinely has no key anywhere, the answer is derived — and must be labelled as derived.
5. **Strict ban on placeholders & fabrications**: never default `Correct` to `A` or any letter; never invent `True/False` options; never fabricate an option to fill a gap.
6. **Agent-owned deep noise removal on every source.** Clean OCR/text while structuring the Markdown, then run `scripts/clean_markdown_noise.py` and manually inspect and repair its output against the source. Remove Moodle chrome, phone status bars, inline `Select one:` options, trailing answer-key grids, `TABLE n A B` headers, bubble artifacts (`@©`, `®@`), Franco-Arab OCR gibberish, Arabic script, leading numbering, invisible unicode, and preceding-question explanation bleed. The cleaner supplements source-aware work; it does not replace it. Do not hand off routine noise cleanup to the user. Use [`references/noise-removal-and-curation.md`](./references/noise-removal-and-curation.md), and do not proceed with noisy Markdown.
7. **Figure-dependent questions.** When a stem refers to a figure, diagram, slide, arrow, photomicrograph or "the following image", the picture is part of the question:
   - Crop the figure from the source page (see playbook §7) and save it as `<Module>/Images/<Index>_<Qn>.png`.
   - Reference that path in the markdown as `**Image:** <relative path>` and carry it into the `Image` column.
   - A figure-dependent question with no image is unanswerable on the platform: if the figure cannot be recovered, mark the question `EXCLUDED — figure unrecoverable` in the catalog rather than shipping a broken question.
8. **Unicode fidelity.** Preserve medical notation: `Ca²⁺`, `Na⁺`, `K⁺`, `β1`, `α2`, `µm`, `→`. OCR renders these as `Ca**`, `Na*`, `B1`, `um`; repair them, do not ship them.

**Markdown file format** (fixed — the Stage 3 compiler parses it):
```markdown
### Q1: <clean stem>

- **A)** <option>
- **B)** <option>
- **C)** <option>
- **D)** <option>

**Correct Answer:** C
**Answer Source:** key            <!-- key | marked | online | derived -->
**Image:** Images/05_Q1.png       <!-- only when figure-dependent -->
**EXP:** <explanation / model answer>

---
```
Written questions use `**Correct Answer:** -` with the model answer in `**EXP:**` and no options.

### Stage 2 — Answer-Key Provenance & Verification (the accuracy gate)
This stage exists because unverified keys are the largest silent defect in the repository — one module shipped 228 questions keyed 100% `A` and another 560 keyed 97% `A`.

1. **Provenance label on every MCQ** (`**Answer Source:**`):
   | Label | Meaning | Trust |
   | :--- | :--- | :--- |
   | `key` | Printed answer key/grid in the source | Highest |
   | `marked` | Correct option bolded, highlighted, ticked, bulleted or colored in the source | High — verify the letter after any option repacking |
   | `online` | Recovered from the source's own online quiz (e.g. a DocReader `doc-reader-guide.com/mcq-quizzes/<id>` link printed in the PDF) | High |
   | `derived` | No key in the source; answered from medical knowledge | **Must be reported to the user, per file, with counts** |
2. **Statistical bias gate (hard fail).** For every source file with ≥ 15 MCQs, compute the distribution of `Correct`. A real exam sits near 20-30% per letter. **Fail the file** if any single letter exceeds **45%**, and investigate before proceeding; > 80% on one letter is proof of a placeholder default, never a coincidence. Run `scripts/audit_question_bank.py --markdown <dir>` or `--excel <file>` to get the per-source table.
3. **Marked-answer recovery.** Where OCR dropped the letter of a highlighted option, recover it from the layout (bold run, highlight rectangle, bullet glyph, indentation) — and re-check the letter after any option repacking in Stage 3.
4. **Spot-check sampling.** For each file, verify 5 answers (or 10%, whichever is larger) against the source by eye. Record `verified n/N` in the catalog.
5. **Never** resolve a missing key by copying the answer of a similar question from another file.

### Stage 3 — Forensic Completeness Audit (pre-Excel gate)
1. **Catalog** `<Module>/Markdown_Questions/00_CATALOG_OF_ALL_FILES.md` with one row per source: index, group, source filename, type/pages, target markdown, total/MCQ/written counts, tag, `tagSuggere`, `Year`, answer-source breakdown (`key/marked/online/derived`), spot-check result, status.
2. **Three independent counters must agree** (± small, explained margin):
   - the highest question number in the source (per section, summed),
   - the number of option-`A` blocks in the extracted text,
   - the number of `### Q` headings in the markdown.
   Disagreement means questions were lost or duplicated — re-extract, do not "explain away".
3. **Declared totals** stated in the source ("120 questions", "Total marks 80") override every estimate.
4. Continuous numbering `1..N`, no gaps, no duplicates, zero Arabic characters, zero noise signatures.
5. **STOP & VERIFY**: the Excel is not created or modified until every markdown file passes Stages 2 and 3.

### Stage 4 — Master 31-Column Excel Compilation & Validation
1. **Aggregate** all verified markdown into `<Module>_Questions.xlsx` (canonical header, Section 3).
2. **Deduplicate** on the normalized stem `re.sub(r'[^a-z0-9]','',stem.lower())`:
   - MCQ + written sharing a stem → keep `QCS`, enrich `EXP` with the model answer, merge tags.
   - Matching questions ("match structure with effect") keep their matching items inside the stem so distinct items are not collapsed.
   - After compiling, **zero duplicate normalized stems may remain**.
3. **Option repacking**: options must start at `A` and be sequential; when repacking, move `Correct` with them.
4. **Validate, then audit**:
   ```bash
   python scripts/validate_questions_excel.py <Module>/<Module>_Questions.xlsx   # schema gate
   python scripts/audit_question_bank.py --excel <Module>/<Module>_Questions.xlsx # forensic gate
   ```
   Both must exit clean: 0 schema errors, 0 option mismatches, 0 duplicate stems, 0 Arabic, 0 noise signatures, 0 bias-flagged sources, 0 figure-dependent questions without an image.
5. Report the final counts to the user against the catalog totals.

---

## 6. Deliverables per Module

```
<Module>/
├── subcategories_<Module>_<Date>.xlsx      # official platform export (source of truth)
├── <Module>_Questions.xlsx                 # master 31-column bank (canonical header)
├── Lectures/<subcategoryId>.pdf            # one PDF per subcategory, exact 1:1
├── Raw_PDF_Questions/                      # every source file, archives expanded
├── Markdown_Questions/
│   ├── 00_CATALOG_OF_ALL_FILES.md          # mandatory forensic catalog
│   └── <NN>_<SourceName>.md                # exactly one per source file
└── Images/<NN>_<Qn>.png                    # figures for figure-dependent questions
```
*(Optional human-readable reference: `All_Questions_<Module>.md`.)*

---

## 7. Reference Files and Helpers

* [Extraction Playbook (format triage, columns, OCR, figures)](./references/extraction-playbook.md)
* [Smart OCR Workflow (PaddleOCR positions, confidence, review)](./references/smart-ocr-workflow.md)
* [Answer-Key Provenance & Verification](./references/answer-key-verification.md)
* [31-Column Specification & Legacy Migration](./references/schema-31-columns.md)
* [Deep Noise Removal & Curation Guide](./references/noise-removal-and-curation.md)
* [Tagging & Merging Reference](./references/tagging-and-naming.md)
* [Subcategories & Lecture Processing Guide](./references/subcategories-and-lectures.md)
* [Column-Aware PDF Extractor](./scripts/extract_pdf_columns.py)
* [Forensic Bank Auditor](./scripts/audit_question_bank.py)
* [Excel Schema Validator](./scripts/validate_questions_excel.py)
* [Deep Noise Removal CLI](./scripts/clean_markdown_noise.py)
* [PaddleOCR page extractor](./scripts/ocr_paddle_pages.py)
* [Master Build Script Template](./scripts/build_module_template.py)
