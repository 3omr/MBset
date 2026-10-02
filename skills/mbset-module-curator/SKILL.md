---
name: mbset-module-curator
description: >-
  Standard operating procedure and toolkit for curating, formatting, and building
  MBset medical modules. Use it to extract questions from exam PDFs, scans, Word files,
  slides and screenshots into markdown and the 32-column question bank Excel: the mbset.py
  pipeline (Telegram download with the user's own account, inventory, OCR, route, per-source parser profiles or parallel page-image transcription,
  automatic answer keys with provenance, worklists split across parallel reviewers, figures, spot
  checks, forensic check gate, build, report), tagging rules, lecture subcategories and PDF management.
---

# MBset Medical Module Curator Skill

SOP for building MBset modules, usable by anyone who has this folder. Tag taxonomies are included for
Damietta (Al-Azhar, Faculty of Medicine) and Assiut curricula (`inventory --university`).

In every command below `$S` is `<this skill folder>/scripts/mbset.py` and `$M` the module folder (any path).

## 0. First run — set the skill up for this person (always check first)
Run `python3 $S init --show` at the start of every session. If it prints **NOT INITIALIZED**, run this
onboarding before any module work. Its answers are saved in `~/.config/mbset/` and never asked again; the
user can change them later with `init`.

**Step 1 — ask the user** (one AskUserQuestion with up to 4 questions; use their language):
1. **Faculty / university.** Offer the faculties listed by `init --list` (Damietta, Assiut) plus *Other*.
   For *Other*, ask its name.
2. **Who runs the heavy work** (transcription / review briefs): *Claude subagents* (always available), each
   delegate CLI that `doctor` finds (Codex, Antigravity, Cursor, OpenCode…), or *none* (the main agent works
   alone). If they pick a CLI, ask which model.
3. **Telegram:** do their sources come from Telegram channels or groups?
4. **Reply language** (Arabic / English).

**Step 2 — tag system for their faculty.**
- **Built-in faculty:** show `init --list`'s rules for it in plain words and ask if that matches how their
  faculty labels sources.
- **Other (or rules that don't fit):** show the generic families (`init --list`, *Generic*). Ask how their
  faculty names its sources: exam rounds (final / midterm / formative / quiz…), department or subject
  books, professor collections, external banks, and which families carry no year. Write a taxonomy YAML
  (format in `scripts/mbset/taxonomy.py`; examples in `references/taxonomies/`) and preview it on their
  real filenames: `init --test "<file 1>" "<file 2>" … --university <name>`. Adjust until they agree.
  Then save it with `--taxonomy-file`.
- Also ask for their platform `categoryId` prefix, if they know it. Otherwise it comes from the platform
  export later.

**Step 3 — save:**
`python3 $S init --university <name> [--taxonomy-file f.yaml] --worker "<choice>" [--dispatch '<cmd {brief}>'] --telegram yes|no --language ar|en`

**Step 4 — tools:**
- Run `python3 $S doctor --fix` (add `--telegram` if they use Telegram). Missing Python packages go into
  `<skill>/.venv` automatically, and later `mbset.py` calls use it. Missing OCR/PDF tools are installed
  with apt/brew/dnf when that needs no password.
- If it prints `[!] needs administrator rights`, show the user the printed command and ask them to run it
  in their own terminal. Never type a sudo password.
- If they use Telegram and `doctor` says credentials or login are missing, the user connects **their own
  account** once with `mbset.py telegram setup`:
  - if the host lets you start a command in the user's own terminal (e.g. the Terminal panel of the Claude
    desktop app), start `python3 $S telegram setup` there and tell them to type the answers there;
  - otherwise give them the command and [`references/setup-guide.md`](./references/setup-guide.md).
  Never ask for, read back, type or store their api_hash, phone number, login code or password, and do
  not read that terminal while they type.
- Re-run `doctor` until it shows 0 FAIL.

**After setup:**
- Modules use the saved faculty's taxonomy. A module from another faculty (e.g. an Assiut folder for a
  Damietta user) takes `inventory --university <name>`.
- The saved worker is used for every dispatch (`--dispatch` / `MBSET_DISPATCH` override it). If it fails
  or runs out of credits, ask again.

**Prime directive**: a module is finished only when **every question in every source file** is in
the master Excel, **with the answer the source actually gives**. Both are proven by measurement
(`mbset.py check` / `report`), never asserted.

## 1. Hard rules (never relaxed)

1. **Question text comes from the source, never from memory.** Scripts or workers copy every stem and
   option verbatim from the page; never paraphrase, shorten, reword, complete or "improve", never type a
   question from memory or another bank. Corrections are re-reads of the page, logged with the original.
2. **Never invent an answer.** Every MCQ carries `**Answer Source:**` `key` / `marked` / `online` /
   `derived` (priority in that order). `derived` = knowledge, only when the source gives no answer; it is
   reported to the user with counts. Never copy an answer from a similar question in another file.
3. **Bias gate**: a file with ≥ 15 MCQs and one letter > 45 % is investigated, > 60 % fails.
4. **Counters agree** per file (source numbering, questions, a declared total, each chunk's own count).
   No Excel until `check` shows 0 hard failures.
5. **32-column canonical header** (31 + `ModelAnswer`): `id`, `subcategoryId`, `subcategoryName` empty;
   zero Arabic (except sources with `keep_arabic: true`); `QCS` → one existing letter `A`-`F`; `QROC` →
   `Correct`/`EXP` empty, model answer in `ModelAnswer`; a shared scenario in `Cas`; figure-dependent
   stems have `Image`. → [`references/schema-31-columns.md`](./references/schema-31-columns.md)
6. **No silent omissions**: `count(sources) == count(markdown) + EXCLUDED — <reason>`.

## 2. Extracting questions — the one procedure

Principles: **scripts first** (they read most pages for free), **models only for pages scripts cannot
read**, **one pass per question** (text + answer + model answer together), **big files always split**,
**workers write JSON only**, **gates decide**, not re-reading. All state is in `<Module>/.mbset/`; every
command is resumable. Every flag: [`references/commands.md`](./references/commands.md).

```bash
S=<skill>/scripts/mbset.py ; M="<University>/<Module>"   # any folder with Raw_PDF_Questions/
```

**Step 1 — sources.** Put every source in `$M/Raw_PDF_Questions/` (`telegram download "$M" <links>` fetches
them with the user's own account, §0). `python3 $S inventory "$M"` expands archives, drops byte-identical
copies, triages every file and suggests its tag.

**Step 2 — machine reading (no model tokens).**
`python3 $S ocr "$M" --searchable` (Tesseract per page, cached, plus an `ocrmypdf --redo-ocr -O 3` copy of
every scanned PDF) → `python3 $S parse "$M"`. Text-layer and clean-OCR pages come out complete, with
answers from printed keys.

**Step 3 — route.** `python3 $S route "$M"` prints, per source: `parse` (done), `transcribe` (whole file:
screenshots, OCR < 0.80, > 30 % of questions need review) or `transcribe pages …` (only the bad pages; the
rest stays parsed). Run the printed commands. Never repair a transcribe-route file question by question.

**Step 4 — transcription by workers.** `python3 $S transcribe "$M" --only NN [--pages …] [--key-pages P]
[--format pdf]` cuts the pages into chunks of about 6 pages of work (dense or weakly-OCRed pages count more)
with one self-contained brief each: `png` (default) gives page images with each page's OCR draft inside the
brief; `pdf` gives chunks of the ocrmypdf copy, only for workers whose file tool reads PDFs (Antigravity reads
images only — use png). Answer-key pages are **found automatically** (or `--key-pages`) and each is read by a
one-minute key job, applied to the exam printed before it. Dispatch the briefs to the worker the user
chose (§0, [`references/workers.md`](./references/workers.md)), effort high: Claude subagents — one background
`Agent` call per brief, all at once; a delegate CLI — `python3 $S dispatch "$M" --only NN` (3 at a time,
retries briefs whose JSON is missing, starts staggered; shared logins drop at high parallelism). Workers
write verbatim questions, `case` for shared scenarios, the `exam` (→ per-question Year), answers with
provenance, model answers and a `printed_count`. Then `transcribe "$M" --status` → `parse "$M" --only NN`.

**Step 5 — what is left.** `python3 $S consensus "$M"` → `dispatch` → `consensus --apply`: every `derived`
answer gets an independent, text-only second answer (cheap: no images); disagreements become
`derived_disputed`. `python3 $S worklist "$M"` lists only what still needs eyes (unclean text, unanswered or
disputed MCQs, written questions without a model answer) with crops; big files are split into question
ranges. Dispatch all worklists at once (effort high; max for parts with model answers), then
`worklist "$M" --apply`. Figures: `figures "$M" --only NN`.

**Step 6 — gates.** `python3 $S check "$M"` until 0 hard failures. It fails on: missing markdown or chunk,
a chunk count mismatch, disagreeing counters, numbering gaps, Arabic, noise, non-sequential options,
unanswered MCQs, invalid Answer Source, written questions without a model answer, figure stems without an
image, bias > 60 %, no spot check, unconfirmed tags or placeholders, duplicate NN. Review items include
`transcript_not_in_page_text` (a paraphrase warning — compare with the page). Spot check every file:
`spotcheck "$M" --only NN` → view → `review "$M" NN --spot "k/k OK"`; confirm tags with `set NN --confirm`.

**Step 7 — deliver.** `catalog "$M"` → `build "$M"` (check → Excel → validate → audit) → `report "$M"`;
give the user the per-file counts and every `derived` count.

Single fixes at any point: `fix "$M" NN --text-file / --answers "3=B" --source marked / --model-file /
--drop N --reason … / --image N=…` (decisions survive re-parses). A file read wrongly as a whole by the
parser: edit its profile ([`references/profiles.md`](./references/profiles.md)) and `parse --only NN`.

### Choosing the worker
Asked once at first-run setup (§0) and saved (`init --show`); if nothing is saved, ask before the first
dispatch. Options: **Claude subagents** (always available — one background `Agent` call per brief: "Read
<brief> and do exactly what it says"), an installed delegate CLI (`doctor` lists them; pass
`--dispatch '<cmd with {brief} {repo} {effort}>'`), or **none** (the main agent works the briefs itself).
If a worker fails or runs out of credits, ask again. Whatever the worker, its output is re-verified by the
gates. → [`references/workers.md`](./references/workers.md)

## 3. Tags, schema and text cleaning (summaries — details in the references)

- **Tags** — chosen per faculty at first-run setup (`init`; taxonomies in `references/taxonomies/` and
  `~/.config/mbset/taxonomies/`). Damietta: `Department, <Subject> <Year>` · `Exams, End|Final <Year>` ·
  `Exams, Formative <Year>` (both rounds share one tag) · `Professor, Dr <Name> <Year>` (one spelling
  per professor) · `External, <Source> <Year>`. Assiut adds `Exams, Midterm`, `Department, QBank|Quizzes|Formative|GDs, …`;
  Quizzes and Formatives carry no year unless it is in the filename. Overlaps merge unique tags into
  one string. `tagSuggere` = discipline for department/professor sources, `None` for exams. A year
  that is not in the filename is never guessed: the suggestion has no year and `check` warns.
  → [`references/tagging-and-naming.md`](./references/tagging-and-naming.md)
- **Schema** — the canonical 32-column header, column rules and the legacy
  (`Genetics_Questions.xlsx`, `POD_Questions.xlsx`) migration map →
  [`references/schema-31-columns.md`](./references/schema-31-columns.md). Confirm `categoryId` /
  `categoryName` against the module's platform export; never invent one.
- **Noise** — the parser strips numbering, invisible unicode, Moodle/LMS chrome, phone status bars,
  answer-key grids, bubble artifacts and OCR gibberish, and repairs notation (`Ca**` → `Ca²⁺`,
  `B1` → `β1`, `->` → `→`) instead of deleting it; recurring junk goes in the profile's `skip_patterns`.
  Never strip numbered lists inside a model answer or a trailing `...` of a fill-in-the-blank stem.

## 4. Lectures and subcategories (two phases)

Phase 1: `subcategories_<Module>.xlsx` with `categoryId` and `subcategoryId` **empty**, present the
lecture breakdown, then **STOP & WAIT** for the user to upload it. Phase 2: the platform export
`subcategories_<Module>_<Date>.xlsx` is the single source of truth; every lecture becomes
`Lectures/<subcategoryId>.pdf` (count equals the subcategories). Multi-part lectures of one topic
merge unless the user says otherwise. `mbset.py lectures` runs both phases.
→ [`references/subcategories-and-lectures.md`](./references/subcategories-and-lectures.md)

Known Damietta platform IDs (examples — the module's platform export is always the source of truth, and
other universities have their own):

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
**Case:** <shared scenario>       <!-- only when several questions share it → Cas column -->
**Image:** Images/05_Q1.png       <!-- only when figure-dependent -->
**Source Pages:** 3
**EXP:** <explanation>            <!-- MCQ only -->

---

### Q2: <written question>

**Correct Answer:** -
**Answer Source:** key            <!-- key (printed) | derived (written from knowledge) -->
**Source Pages:** 4
**Model Answer:** <full model answer> <!-- → ModelAnswer column; Correct and EXP stay empty -->

---
```
Written questions have no options, `**Correct Answer:** -` and the model answer in `**Model Answer:**`.
Older markdown files carry it as `**EXP:**`; the builder reads both, so they are never rewritten for this —
a re-parse or `fix --model-file` writes the new label.

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

* `scripts/mbset.py` — the CLI (package `scripts/mbset/`): `init` first-run setup · `telegram` · `inventory`
  · `ocr` · `parse` · `route` / `transcribe` · `worklist` · `fix` · `check` · `build` · `report` · `lectures`
* `scripts/install.sh` — optional ahead-of-time setup (same as `doctor --fix`) · `requirements*.txt`
* `scripts/build_module_template.py` (markdown → 32-column Excel) · `validate_questions_excel.py` (schema gate)
  · `audit_question_bank.py` (forensic gate) · `clean_markdown_noise.py` (markdown made outside the pipeline)
* References: [setup-guide](./references/setup-guide.md) · [commands](./references/commands.md) ·
  [workers](./references/workers.md) · [profiles](./references/profiles.md) ·
  [schema-31-columns](./references/schema-31-columns.md) · [tagging-and-naming](./references/tagging-and-naming.md) ·
  [subcategories-and-lectures](./references/subcategories-and-lectures.md) · `references/taxonomies/`
