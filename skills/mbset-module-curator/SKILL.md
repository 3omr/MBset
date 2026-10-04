---
name: mbset-module-curator
description: >-
  Standard operating procedure and toolkit for building MBset medical question banks and lecture sets: exam
  PDFs, scans, Word files, slides and screenshots → verbatim markdown → the 32-column bank Excel. The mbset.py
  pipeline (Telegram download with the user's own account, inventory, OCR, per-page routing, parallel
  transcription by the worker the user chose, printed keys found automatically, second opinions, gates,
  build), faculty tag systems, lecture subcategories.
---

# MBset Module Curator

`$S` = `<this skill folder>/scripts/mbset.py`, `$M` = the module folder (any folder with `Raw_PDF_Questions/`).
Every command is resumable; all state is in `$M/.mbset/`. Flags: [`references/commands.md`](./references/commands.md).

## 0. First run (check every session)
`python3 $S init --show`. If it says **NOT INITIALIZED**, do the onboarding in
[`references/first-run.md`](./references/first-run.md) before anything else: ask the user (one question set)
for their **faculty** (tag system: built-in Damietta / Assiut, or build theirs with them and preview it with
`init --test`), **who runs the briefs** (Claude subagents, an installed delegate CLI, or none), **Telegram**
yes/no and **reply language**; save with `init`; run `doctor --fix` until 0 FAIL. Never handle the user's
Telegram api_hash, phone, login code or any password — the user runs `telegram setup` in their own terminal.

**Prime directive**: a module is finished only when every question of every source is in the Excel with the
answer the source gives — proven by `check` / `report`, never asserted.

## 1. Hard rules
1. **Verbatim.** Stems and options are copied exactly as printed — typos included — never paraphrased,
   shortened, completed, corrected or typed from memory. Corrections are re-reads of the page, logged.
2. **Answer provenance**: `key` > `online` > `marked` > `derived` (knowledge, only when the source gives
   none; reported with counts). Never copy an answer from a similar question elsewhere.
3. **Bias gate**: ≥ 15 MCQs and one letter > 45 % → investigate; > 60 % → fail.
4. **Counters agree** (numbering, questions, declared total, each chunk's own count) — or a written count note.
5. **32-column header**; `id`, `subcategoryId/Name` empty; zero Arabic unless the source is `keep_arabic`;
   `QCS` → one existing letter A–F; `QROC` → `ModelAnswer`, `Correct`/`EXP` empty; shared scenario → `Cas`;
   figure stems have `Image`. → [`references/schema-31-columns.md`](./references/schema-31-columns.md)
6. **No silent omissions**: every source is in the markdown or `EXCLUDED — <reason>`.
7. **Finished modules are not reworked.** New tools are tried on copies; a finished bank changes only when the
   user asks for that specific change.

## 2. Extracting questions — the one procedure
Scripts read what they can for free; workers read only what scripts cannot, in one pass per question; big
files are always split; workers write JSON only; gates decide.

1. **Sources** in `$M/Raw_PDF_Questions/` (`telegram download "$M" <links>`), then `inventory "$M"`
   (archives expanded, byte-identical files dropped, tags suggested from the faculty's taxonomy).
2. **Machine reading**: `ocr "$M" --searchable` (Tesseract per page — weak photo pages retried with the light
   flattened — plus an `ocrmypdf --redo-ocr -O 3` copy) → `parse "$M"`.
3. **Route**: `route "$M"` → per source `parse` (done), `transcribe` (whole file) or `transcribe pages …`.
   Never repair a transcribe-route file question by question.
4. **Transcribe**: `transcribe "$M" --only NN [--pages …]` → chunks of ≈ 6 pages of work, each brief holding
   the page images and their OCR drafts; pages identical to a page already read (this or another source) are
   not read again; answer-key pages are found and read by one-minute key jobs, applied to the exam before
   them. Dispatch: Claude subagents (one background Agent call per brief) or
   `dispatch "$M" [--dispatch '<cmd>' --parallel 4 …]` (several pools allowed, staggered, retried).
   Then `parse "$M" --only NN`. → [`references/workers.md`](./references/workers.md)
5. **Second looks**: `consensus "$M"` (text-only second answer for derived MCQs → disputes);
   `spotcheck "$M" --worker` (a worker compares sampled pages with the markdown); `dispatch`, then
   `consensus --apply` / `review "$M" --auto`. `worklist "$M"` gathers what is left (unclean text, spot-check
   differences, unanswered or disputed MCQs, missing model answers), split for parallel reviewers →
   `worklist --apply`. Figures: `figures "$M"`.
6. **Gates**: `check "$M"` until 0 hard failures; `set NN --confirm` (tags) / `--count-note`; an exam
   header year that differs from the file's year → ask the user → `set NN --question-year file|printed`.
7. **Deliver**: `catalog` → `build` (Excel + validate + audit) → `report`; tell the user the derived counts.

Single fixes: `fix "$M" NN --text-file | --answers "3=B" --source marked | --model-file | --drop N --reason |
--image N=…` (logged, survive re-parses). A file the parser misreads as a whole: fix its profile
([`references/profiles.md`](./references/profiles.md)) and re-parse — or transcribe it.

## 3. Tags, lectures, deliverables
- **Tags** per faculty: `references/taxonomies/*.yaml` (+ the user's own in `~/.config/mbset/taxonomies/`);
  families and rules in [`references/tagging-and-naming.md`](./references/tagging-and-naming.md). A year not
  in the source is never guessed; questions carry the exam year printed in their header.
- **Lectures** (two phases: subcategories file with empty ids → STOP for the user's upload → platform export
  is the truth → `Lectures/<subcategoryId>.pdf`): `lectures plan|match|apply|check` →
  [`references/subcategories-and-lectures.md`](./references/subcategories-and-lectures.md).
- **Deliverables**: `subcategories_<Module>_<Date>.xlsx`, `<Module>_Questions.xlsx`, `Lectures/`,
  `Raw_PDF_Questions/`, `Markdown_Questions/` (catalog + one file per source), `Images/<NN>_<Qn>.png`.

References: [first-run](./references/first-run.md) · [setup-guide](./references/setup-guide.md) ·
[commands](./references/commands.md) · [workers](./references/workers.md) · [profiles](./references/profiles.md)
· [schema + markdown format](./references/schema-31-columns.md) · [tagging](./references/tagging-and-naming.md)
· [lectures](./references/subcategories-and-lectures.md)
