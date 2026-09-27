---
name: mbset-module-curator
description: >-
  Standard operating procedure and toolkit for curating, formatting, and building
  MBset medical modules. Use it to extract questions from exam PDFs, scans, Word files,
  slides and screenshots into markdown and the 32-column question bank Excel: the mbset.py
  pipeline (inventory, OCR, per-source parser profiles, automatic answer keys with provenance,
  visual answer sheets, figures, spot checks, forensic check gate, build, report), tagging rules,
  lecture subcategories and PDF management.
---

# MBset Medical Module Curator Skill

SOP for building MBset modules (Faculty of Medicine, Al-Azhar University, Damietta; Assiut-sourced
material is also supported).

**Prime directive**: a module is finished only when **every question in every source file** is in
the master Excel, **with the answer the source actually gives**. Both are proven by measurement
(`mbset.py check` / `report`), never asserted.

## 1. Hard rules (never relaxed)

1. **Question text comes from the source, never from memory.** The parser writes every stem and
   option; a misread *file* is fixed through its profile (`.mbset/profiles/NN.yaml`) and a re-parse.
   A misread *question* (missing option, OCR symbols like `¢ © |`, words out of order, glued stem and
   option) is corrected by **re-reading the page image** and writing exactly what is printed with
   `fix NN --text-file` — every fix is logged with the original text and reviewed. Never paraphrase,
   shorten, reword, complete or "improve" a question, and never type one from memory or another bank.
2. **Never invent an answer.** Every MCQ carries `**Answer Source:**` `key` / `marked` / `online` /
   `derived`. An unreadable mark stays `?`. `derived` (the agent's knowledge, only when the source
   has no answer) is reported to the user with counts.
3. **Bias gate**: a file with ≥ 15 MCQs and one letter > 45% is investigated, > 60% fails.
4. **Three counters agree** per file — source numbering, option-A blocks, `### Q` headings; a
   declared source total wins. No Excel work until `check` shows 0 hard failures.
5. **32-column canonical header** (31 + `ModelAnswer`), `id` empty, `subcategoryId` / `subcategoryName` empty, zero
   Arabic characters, `QCS` → one existing letter `A`-`F`, `QROC` → `Correct`/`EXP` empty, model answer in `ModelAnswer`,
   figure-dependent stems have `Image`. → [`references/schema-32-columns.md`](./references/schema-32-columns.md)
6. **No silent omissions**: `count(sources) == count(markdown) + EXCLUDED — <reason>`.

## 2. The pipeline — `mbset.py` (parse first, review second)

All state lives in `<Module>/.mbset/` (state.json, profiles, OCR cache, parsed evidence, reports).
Every command is idempotent and resumable. Full reference with flags:
[`references/pipeline-v2.md`](./references/pipeline-v2.md).

```bash
S=.agents/skills/mbset-module-curator/scripts/mbset.py      # M="أزهر دمياط/<Module>"
python $S doctor "$M"               # environment (+ module) health: tools, packages, stale locks
python $S tidy "$M"                 # dry-run plan to standardize the folder layout (--apply moves to _trash/)
python $S inventory "$M"            # Stage 0: expand archives, hash-dedupe, triage, suggest tags
python $S ocr "$M"                  # Tesseract for every scanned source, parallel, cached per page
python $S parse "$M"                # Stage 1+2: profile → markdown, answers with provenance, flags, counters
python $S check "$M"                # Stages 2+3 gate: problems only, grouped per file
# … review loop (below) until check prints 0 hard failures …
python $S catalog "$M"              # 00_CATALOG_OF_ALL_FILES.md + tag map, generated from state
python $S build "$M"                # check → build_module_template → validate → audit (all must pass)
python $S report "$M"               # final per-file counts, answer sources, derived list → give it to the user
```

| Command | One line |
| :--- | :--- |
| `inventory` / `ocr` / `parse` | sources → triage → OCR cache → markdown with answers and flags |
| `show NN --flags` / `--dropped` | only the flagged questions with evidence / lines discarded as noise |
| `profile --only NN --print` | the effective profile; edit the YAML, then `parse --only NN` |
| `answersheet --only NN` | crops of unanswered MCQs, 6 per PNG, for a visual pass over pen marks |
| `fix NN --answers "2=B 3=C" --source marked` | batch answers; also `--exp-file`, `--image`, `--drop … --reason` |
| `figures --only NN` | crop figures for figure-dependent stems → `Images/NN_Qi.png`, linked |
| `spotcheck --only NN` / `review NN --spot "7/7 OK"` | max(5, 10%) source-vs-markdown sheets / record the verdict |
| `set NN --tag … --year … --confirm` | confirm tags; `--exclude REASON`, `--count-note` |
| `renumber` | resolve duplicate NN (markdown, evidence and `Images/<NN>_*` move together) |
| `check [--only NN]` | the gate; exit 1 on hard failures |
| `catalog` / `build` / `report` | catalog + tag map / gated Excel / final user report |
| `packets --n 4` / `lock NN --owner X` | parallel work packets with self-contained Codex briefs / claim sources |
| `status` / `run` | one line per source / inventory → ocr → parse → check in one go |
| `doctor [module]` | environment and module health check (OK / WARN / FAIL) |
| `tidy` | standardize the module folder to the deliverables layout (dry run; `--apply`, `--restore`) |
| `crossdup <roots…>` | report sources byte-identical across modules (nothing is moved) |
| `lectures plan` / `match` / `apply` / `check` | the two-phase lecture / subcategory workflow (§4) |

### The review loop for one source
1. `parse --only NN` → counters equal? answered = MCQ? distribution sane?
2. `show NN --flags` → profile problem (fix YAML, re-parse) or single question (`fix`). Every field
   and recipe: [`references/profiles.md`](./references/profiles.md). A hand-edited markdown is never
   overwritten without `--force` (backup kept).
3. `show NN --dropped` once per file — the noise filter must not have eaten a question.
4. Unanswered MCQs → `answersheet`, read the marks, `fix --answers … --source marked`. No visible mark
   → leave `?`; only when the source truly has no answer, `--source derived` and report the count.
5. `figures --only NN` when figure-dependent stems exist; view the contact sheet.
6. `spotcheck --only NN`, view the sheets, `review NN --spot "k/k OK"`.
7. `set NN --confirm` (or `--tag …`), then `check --only NN` → 0 hard failures.

Answer provenance, in priority order: `key` (answer grid / `Ans:` lines, section-aware) → `online`
(DocReader quiz; never defaults when the site has no answer) → `marked` (exactly one option carries
a mark) → `derived`. Disagreeing sources, keys not among the options and multi-letter keys are
flagged. Every `fix` is stored by stem, so a re-parse re-applies it. Never copy an answer from a
similar question in another file. → [`references/answer-key-verification.md`](./references/answer-key-verification.md)

`check` hard-fails on: missing markdown, non-continuous numbering, disagreeing counters, declared
total mismatch, numbering gaps, Arabic, noise signatures, non-sequential options, unanswered MCQs,
invalid Answer Source, written questions without a model answer, figure stems without an image,
bias > 60%, no spot check, unconfirmed tags, tag placeholders (`<…>`), duplicate NN, missing sources.
It warns on unconfirmed tags without a year.

### Parallel work and delegation
`packets "$M" --n 4` splits the sources into balanced packets and writes, per packet,
`.mbset/packets/packet_k.md` and a self-contained Codex brief `packet_k_brief.txt`. The judgement
steps (pen-mark answer sheets, flag triage, spot-check sheets, QROC model answers / derived answers)
run one Codex **gpt-6-luna** worker at effort **max** per packet, in parallel; the orchestrator
re-verifies every packet with `check` / `report` and builds the Excel once.
→ [`references/parallel-workflow.md`](./references/parallel-workflow.md),
[`references/model-routing.md`](./references/model-routing.md)

## 3. Tags, schema and text cleaning (summaries — details in the references)

- **Tags** — Damietta: `Department, <Subject> <Year>` · `Exams, End|Final <Year>` ·
  `Exams, Formative <Year>` (both rounds share one tag) · `Professor, Dr <Name> <Year>` (one spelling
  per professor) · `External, <Source> <Year>`. Assiut adds `Exams, Midterm`, `Department, QBank|Quizzes|Formative|GDs, …`;
  Quizzes and Formatives carry no year unless it is in the filename. Overlaps merge unique tags into
  one string. `tagSuggere` = discipline for department/professor sources, `None` for exams. A year
  that is not in the filename is never guessed: the suggestion has no year and `check` warns.
  → [`references/tagging-and-naming.md`](./references/tagging-and-naming.md)
- **Schema** — the canonical 32-column header, column rules and the legacy
  (`Genetics_Questions.xlsx`, `POD_Questions.xlsx`) migration map →
  [`references/schema-32-columns.md`](./references/schema-32-columns.md). Confirm `categoryId` /
  `categoryName` against the module's platform export; never invent one.
- **Noise** — the parser strips numbering, invisible unicode, Moodle/LMS chrome, phone status bars,
  answer-key grids, bubble artifacts and OCR gibberish, and repairs notation (`Ca**` → `Ca²⁺`,
  `B1` → `β1`, `->` → `→`) instead of deleting it; recurring junk goes in the profile's
  `skip_patterns`. → [`references/noise-removal-and-curation.md`](./references/noise-removal-and-curation.md)
- **Extraction by format** (columns, scans, Moodle, screenshots, figures) →
  [`references/extraction-playbook.md`](./references/extraction-playbook.md). PaddleOCR is a fallback
  for pages with low Tesseract confidence only — see `legacy/`.

## 4. Lectures and subcategories (two phases)

Phase 1: `subcategories_<Module>.xlsx` with `categoryId` and `subcategoryId` **empty**, present the
lecture breakdown, then **STOP & WAIT** for the user to upload it. Phase 2: the platform export
`subcategories_<Module>_<Date>.xlsx` is the single source of truth; every lecture becomes
`Lectures/<subcategoryId>.pdf` (count equals the subcategories). Multi-part lectures of one topic
merge unless the user says otherwise. `mbset.py lectures` runs both phases.
→ [`references/subcategories-and-lectures.md`](./references/subcategories-and-lectures.md)

| Module | `categoryId` |
| :--- | :--- |
| Normal Human Body | `DamiettaFa_NORMAL_HUMAN_BODY` |
| Biomedical | `DamiettaFa_BIOMEDICAL` |
| Blood | `DamiettaFa_BLOOD` |
| Respiratory | `DamiettaFa_RESPIRATORY` |
| CVS | `DamiettaFa_CVS` |
| CNS | `DamiettaFa_CNS` |
| POD | `DamiettaFa_POD` |
| Genetics | `DamiettaFa_GENETICS` |
| Behavioral Science | `DamiettaFa_BEHAVIORAL_SCIENCE` |

## 5. Markdown format (what `build_module_template.py` parses)

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

## 6. Deliverables per module

```
<Module>/
├── subcategories_<Module>_<Date>.xlsx      # official platform export (source of truth)
├── <Module>_Questions.xlsx                 # master 32-column bank (canonical header)
├── Lectures/<subcategoryId>.pdf            # one PDF per subcategory, exact 1:1
├── Raw_PDF_Questions/                      # every source file, archives expanded
├── Markdown_Questions/
│   ├── 00_CATALOG_OF_ALL_FILES.md          # forensic catalog (generated by `catalog`)
│   └── <NN>_<SourceName>.md                # exactly one per source file
└── Images/<NN>_<Qn>.png                    # figures for figure-dependent questions
```

## 7. Scripts and references

* `scripts/mbset.py` — the pipeline CLI (package `scripts/mbset/`)
* `scripts/build_module_template.py` — markdown → canonical 32-column Excel (dedupe on normalized stems)
* `scripts/validate_questions_excel.py` — schema gate · `scripts/audit_question_bank.py` — forensic gate (`--by-tag`)
* `scripts/clean_markdown_noise.py` — noise cleaner for markdown produced outside the parser (dry run by default, never changes an answer)
* `legacy/` — `extract_pdf_columns.py`, `ocr_paddle_pages.py`, `smart-ocr-workflow.md` (one-off inspection / PaddleOCR fallback)
* References: [pipeline-v2](./references/pipeline-v2.md) · [profiles](./references/profiles.md) ·
  [parallel-workflow](./references/parallel-workflow.md) · [model-routing](./references/model-routing.md) ·
  [extraction-playbook](./references/extraction-playbook.md) · [answer-key-verification](./references/answer-key-verification.md) ·
  [schema-32-columns](./references/schema-32-columns.md) · [noise-removal-and-curation](./references/noise-removal-and-curation.md) ·
  [tagging-and-naming](./references/tagging-and-naming.md) · [subcategories-and-lectures](./references/subcategories-and-lectures.md)
