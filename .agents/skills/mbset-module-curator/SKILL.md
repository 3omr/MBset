---
name: mbset-module-curator
description: >-
  Standard operating procedure and toolkit for curating, formatting, and building
  MBset medical modules. Use it to extract questions from exam PDFs, scans, Word files,
  slides and screenshots into markdown and the 31-column question bank Excel: the mbset.py
  pipeline (inventory, OCR, per-source parser profiles, automatic answer keys with provenance,
  visual answer sheets, figures, spot checks, forensic check gate, build), tagging rules,
  lecture subcategories and PDF management.
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

## 5. The Question Bank Pipeline — `mbset.py` (parse first, review second)

**The model never types question text.** A deterministic parser extracts every stem, option and
answer from the source into canonical markdown; the agent's job is to (1) make each source's
*profile* right, (2) review only what the tools flag, and (3) read answers off the page where the
source marks them by pen. This is what makes a module take minutes of agent time instead of hours,
and it removes the paraphrasing, skipped questions and invented answers that hand-transcription
produces. Retyping questions from a PDF — or from memory — is forbidden; if the parser gets a file
wrong, fix the profile and re-parse.

All state lives in `<Module>/.mbset/` (state.json, profiles, OCR cache, parsed evidence, reports).
Every command is idempotent and resumable; `status` shows where each source is.

```bash
S=.agents/skills/mbset-module-curator/scripts/mbset.py      # M="أزهر دمياط/<Module>"
python $S inventory "$M"            # Stage 0: expand archives, hash-dedupe, triage every source, suggest tags
python $S ocr "$M"                  # Tesseract for every scanned source, parallel, cached per page
python $S parse "$M"                # profile → markdown for every source (≈1 min per module), flags + counters
python $S check "$M"                # Stages 2+3 gate: problems only, grouped per file
# … review loop below until check prints 0 hard failures …
python $S catalog "$M"              # 00_CATALOG_OF_ALL_FILES.md + tag map, generated from state
python $S build "$M"                # check → build_module_template → validate → audit (all must pass)
```

### Stage 0 — Inventory (`inventory`)
Expands `.zip/.rar/.7z`, lists every source with pages and a SHA-256, auto-excludes byte-identical
duplicates (`EXCLUDED — duplicate of NN`), flags near-duplicates, keeps the NN of an existing
catalog, and triages each file (`digital_single`, `digital_two_column`, `scanned`, `moodle`,
`docreader`, `docx`, `pptx`, `screenshot`, `phone_screenshots`, `text`) with signals such as
declared totals and figure words. Tags are *suggested* (`confirmed: false`); the agent confirms or
corrects them with `set NN --tag … --year … --confirm`. `set NN --exclude "reason"` documents a
source with no questions. `count(sources) == count(markdown) + excluded` is enforced by `check`.

### Stage 1 — Profiles and parsing (`profile`, `parse`, `show`)
Each source gets `.mbset/profiles/NN.yaml`, pre-filled from its triage class
(`references/profiles/*.yaml`). The parser handles, without per-file code: column detection per
page, two-column reading order, option grids (a c / b d), inline `a. … b. …` runs, right-to-left
PDFs, section-restarting numbering, excerpts starting at Q121, chapter numbering `24.3`,
unnumbered questions, OCR number/marker repair, Moodle/DocReader/scanner/phone chrome, and
figure detection. `parse` prints per file: questions, MCQ, answered, the three counters, answer
distribution and flag count. Read **only** the flagged questions:

```bash
python $S show "$M" NN --flags      # flagged questions with evidence (source no., page, marks/style per option)
python $S show "$M" NN --dropped    # lines the parser discarded as noise — make sure no question is in there
python $S profile "$M" --only NN --print   # the effective profile; edit .mbset/profiles/NN.yaml, then parse --only NN
```

Typical profile fixes: `columns: 2`, `pages: "3-40"`, `stop_patterns: ["^Answers"]`,
`answers: {mode: grid, grid_pages: "-1"}`, `numbering: none`, `type: written`,
`declared_total: 60`. Every field is in [`references/profiles.md`](./references/profiles.md).
A markdown file edited after the parser wrote it is never overwritten without `--force`
(a backup is kept).

### Stage 2 — Answers with provenance (automatic first, visual second)
`parse` resolves answers itself, in priority order, and labels each one:

| Label | Found by | Notes |
| :--- | :--- | :--- |
| `key` | answer grid anywhere in the file (`1-C 2-A`, two-row tables, `Ans: B` lines, section-aware) | highest trust |
| `online` | the source's DocReader quiz (`answers.docreader_quiz: <id>`) | never defaults when the site has no answer |
| `marked` | exactly one option carries a mark: tick glyph, highlight/ink/circle/box annotation, coloured fill, pixel tint, bold, colour, underline | a style shared by most options is ignored |
| `derived` | the agent's medical knowledge, only when the source has no answer | **reported to the user with counts** |

Sources disagreeing, a key letter that is not among the options and multi-letter keys are flagged.
Scans with **pen marks** cannot be read reliably by pixels — read them visually, in batches:

```bash
python $S answersheet "$M" --only NN            # crops of every unanswered MCQ, 6 per PNG, labelled with Q numbers
python $S fix "$M" NN --answers "2=B 3=B 4=B 6=C" --source marked
python $S fix "$M" NN --exp-file model_answers.json          # written questions: {"12": "model answer …"} (derived)
python $S fix "$M" NN --image 7=Images/NN_Q7.png --drop 31 --reason "duplicate of Q30 in the source"
```

Every `fix` decision is stored in state (keyed by stem), so a later profile fix + re-parse
re-applies it; stale decisions are reported. **Bias gate:** ≥ 15 MCQs and one letter > 45% →
investigate, > 60% → hard fail. Never copy an answer from a similar question in another file.

### Stage 3 — Review and the gate (`figures`, `spotcheck`, `review`, `check`)
```bash
python $S figures "$M" --only NN                 # crops figures for figure-dependent stems → Images/NN_Qi.png, linked
python $S spotcheck "$M" --only NN [--flagged]   # max(5,10%) source crops beside the markdown, 5 per PNG
python $S review "$M" NN --spot "7/7 OK"         # record the verdict (required by check)
python $S check "$M" [--only NN] [--all]         # 0 hard failures before any Excel work
```
`check` hard-fails on: missing markdown, non-continuous numbering, counters that disagree
(source numbering − documented drops ≠ headings), declared total mismatch, numbering gaps,
Arabic, noise signatures, non-sequential options, unanswered MCQs, invalid Answer Source,
written questions without a model answer, figure stems without an image, bias > 60%, no spot
check, unconfirmed tags, duplicate NN, missing sources. An explained, accepted mismatch is
recorded with `set NN --count-note "…"`. Everything else is a review item.

### Stage 4 — Build (`catalog`, `build`)
`build` refuses to run while `check` has hard failures, then runs
`build_module_template.py` (dedupe on normalized stems, tags merged), `validate_questions_excel.py`
and `audit_question_bank.py --by-tag`; all three must pass. Report the final counts per file,
the answer-source breakdown and every `derived` count to the user.

### Working in parallel and choosing models
`packets "$M" --n 4` splits the sources into balanced work packets (by pages) with the exact
command loop; each agent `lock`s its NNs and touches only their profiles and markdown. The
catalog and the Excel are built once, by the coordinator. See
[`references/parallel-workflow.md`](./references/parallel-workflow.md) and
[`references/model-routing.md`](./references/model-routing.md) (cheap model for the
mechanical loop, strong model only for pen-marked answer sheets and derived answers).

### Legacy tools
`extract_pdf_columns.py`, `ocr_paddle_pages.py` and `clean_markdown_noise.py` (now canonical-format,
dry-run by default, never invents an answer) remain for one-off inspection. The markdown format,
the provenance labels, the counters and the gates are unchanged — `mbset.py` writes and proves them.

**Markdown file format** (what `build_module_template.py` parses):
```markdown
### Q1: <clean stem>

- **A)** <option>
- **B)** <option>

**Correct Answer:** B
**Answer Source:** key            <!-- key | marked | online | derived -->
**Image:** Images/05_Q1.png       <!-- only when figure-dependent -->
**Source Pages:** 3
**EXP:** <explanation / model answer>

---
```
Written questions use `**Correct Answer:** -` with the model answer in `**EXP:**` and no options.

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

* [Pipeline v2 — every mbset.py command](./references/pipeline-v2.md)
* [Parser profiles — every field, with recipes](./references/profiles.md)
* [Parallel workflow (packets, locks)](./references/parallel-workflow.md)
* [Model routing (which model for which step)](./references/model-routing.md)
* [Extraction Playbook (format triage, columns, OCR, figures)](./references/extraction-playbook.md)
* [Smart OCR Workflow (PaddleOCR positions, confidence, review)](./references/smart-ocr-workflow.md)
* [Answer-Key Provenance & Verification](./references/answer-key-verification.md)
* [31-Column Specification & Legacy Migration](./references/schema-31-columns.md)
* [Deep Noise Removal & Curation Guide](./references/noise-removal-and-curation.md)
* [Tagging & Merging Reference](./references/tagging-and-naming.md)
* [Subcategories & Lecture Processing Guide](./references/subcategories-and-lectures.md)
* [mbset.py — the pipeline CLI](./scripts/mbset.py)
* [Column-Aware PDF Extractor](./scripts/extract_pdf_columns.py)
* [Forensic Bank Auditor](./scripts/audit_question_bank.py)
* [Excel Schema Validator](./scripts/validate_questions_excel.py)
* [Deep Noise Removal CLI](./scripts/clean_markdown_noise.py)
* [PaddleOCR page extractor](./scripts/ocr_paddle_pages.py)
* [Master Build Script Template](./scripts/build_module_template.py)
