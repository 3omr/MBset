# Subcategories & Lecture Processing Guide

Lectures follow the two-phase workflow (SKILL.md §3). Every step runs through `mbset.py lectures`;
module-specific hand scripts are no longer needed.

```
mbset.py lectures <Module> plan  --schedule FILE | --from-dir DIR [--category-name N] [--tag T] [--merge-parts]
mbset.py lectures <Module> match --sources [KIND=]DIR ... [--map pins.json] [--priority …] [--threshold 0.6]
mbset.py lectures <Module> apply [--ocr] [--force] [--lectures-dir DIR]
mbset.py lectures <Module> check [--verbose] [--min-chars 200]
```
`--out-dir DIR` (match/apply/check) puts the manifest and reports in DIR instead of `<Module>/.mbset/`
— use it for dry runs against a module you must not touch.

## Phase 1 — `plan` (then STOP)
* `--schedule`: `.xlsx`/`.csv` with `name` (or lecture/title/topic) and optional `tag` (group/subject)
  columns, or `.txt`/`.md` with `# Group` / `Group:` headings and one lecture per line (numbering and
  list markers stripped). `--from-dir`: one row per lecture file, first sub-folder = tag.
* Writes `subcategories_<Module>.xlsx`, sheet `Subcategories`, the 13 platform columns
  `categoryId, categoryName, subcategoryId, name, tag, type, pdf, studyRecommendations, pdfVersion,
  pdfDate, pdfNote, questionsCount, orderIndex` — **`categoryId` and `subcategoryId` empty**,
  `questionsCount` 0, `orderIndex` 10, 20, …; refuses to overwrite without `--force`.
* Multi-part files (`Joints Part 1/2`, `… II`) are listed; merging is the user's call
  (`--merge-parts` collapses them into one row; merge the PDFs with `--map`, below).
* Present the printed breakdown, have the user upload the file, and **wait** for the platform export
  `subcategories_<Module>_<Date>.xlsx`. It is the single source of truth from then on; delete the
  temporary Phase-1 file.

## Phase 2 — `match` → `apply` → `check`
1. **`match`** (dry run) reads the newest export (or `--export`), scans the source folders and fuzzy-matches
   each row (name and id) to one file: typo-tolerant, abbreviations expanded (`htn`, `DM`), Telegram
   `0000000315__` prefixes ignored, and opposite prefixes never confused (hypo/hyper, thyroid/parathyroid,
   micro/macro). Assignment is one file per row per kind; a `deck.pdf`/`deck.pptx` pair counts once
   (PDF preferred). Each row takes the first kind in the priority, default
   **powerpoint (College) → book → docreader → existing → other → missing**. A kind comes from
   `KIND=DIR`, else `.pptx/.ppt/.odp` = powerpoint, else the folder name (PowerPoint/College/slides,
   Book, DocReader/Telegram, Lectures/Upload). Output: `.mbset/lectures_manifest.json` and the table
   `.mbset/reports/lectures_match.md` with score, ambiguous rows (⚠) and unmatched source files.
2. **Review the table.** Fix wrong or missing rows with `--map pins.json` (keys: subcategoryId or exact
   name; file paths relative to the module):
   ```json
   {"Hyperthyroidism": "Book/Endocrine.pdf#19-26",
    "Posterior pituitary disorders (Diabetes Insipidus, SIADH)": ["Slides/DI.pptx", "Slides/SIADH.pptx"],
    "Radiology: Imaging": {"files": ["Slides/slidesaver_x.pdf"], "kind": "powerpoint", "force": true},
    "Dyslipidemia": null}
   ```
   A pin is a candidate of its kind and still obeys the priority; `"force": true` wins outright and
   `null` forces `missing`. Book ranges are never guessed — add one only after checking the section
   boundary in the book. Re-run `match` until the table is right.
3. **`apply`** builds `Lectures/<subcategoryId>.pdf` per matched row: copies a PDF, converts
   pptx/ppt/docx with LibreOffice (`soffice --headless --convert-to pdf`), slices page ranges and merges
   lists. `--ocr` runs `ocrmypdf --skip-text` on outputs with fewer than `--min-chars` text-layer chars.
   Sources are never moved or deleted; an existing different `Lectures/<id>.pdf` is not overwritten
   without `--force`; re-runs are idempotent. Missing rows are listed.
4. **`check`** (gate): every export row has `Lectures/<subcategoryId>.pdf`, no stray files in `Lectures/`,
   every PDF readable; prints page counts and flags PDFs without a text layer. Exit 1 on missing, stray
   or unreadable files; the PDF count must equal the export row count.

Final layout:
```
<Module>/
├── subcategories_<Module>_<Date>.xlsx
└── Lectures/
    ├── DamiettaFa_NORMAL_HUMAN_BODY_ACTION_POTENTIAL.pdf
    └── …                                  # exactly one PDF per export row
```
