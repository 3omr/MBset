# Pipeline v2 — `mbset.py` command reference

```bash
S=<skill>/scripts/mbset.py          # wherever the skill folder is installed
M="My University/Endocrinology"     # any module folder with Raw_PDF_Questions/
```
`--only` accepts NN (`3`, `03`), ranges (`10-14`), comma lists and file names. All state is in
`$M/.mbset/`; deleting that folder resets the pipeline but never touches sources or markdown.

| Command | What it does | Output |
| :--- | :--- | :--- |
| `init [--show\|--list\|--test F…]` / `init --university N [--taxonomy-file f.yaml] [--worker W] [--dispatch D] [--telegram yes\|no] [--language L]` | first-run setup per person: faculty + tag taxonomy, worker, Telegram, language (SKILL.md §0) | `~/.config/mbset/config.yaml`, `taxonomies/` |
| `telegram setup` | once per person, **run by the user** in their own terminal: API id/hash from my.telegram.org + login; saved in `~/.config/mbset/` (mode 600) | — |
| `telegram status` | Telethon installed? credentials saved? session logged in? (no secrets printed) | terminal |
| `telegram download "$M" URL… [--links-file f] [--offset] [--limit] [--dry-run]` | post files → `$M/Raw_PDF_Questions/` (public posts, ranges `…/120-160`, private `t.me/c/…`); resumable, sha-deduplicated | `.mbset/telegram_downloads.json` |
| `inventory "$M" [--university Damietta\|Assiut]` | expand archives, SHA-256 + near-duplicate detection, triage, NN assignment (keeps an existing catalog's NN), tag suggestions | `state.json`, summary table |
| `ocr "$M" [--jobs 2 --workers 4] [--force] [--all]` | Tesseract TSV per page for scanned sources, in parallel, cached by hash + settings | `.mbset/ocr/NN.json`; pages with low confidence listed |
| `profile "$M" [--only] [--force] [--print]` | write / show the per-source profile | `.mbset/profiles/NN.yaml` |
| `parse "$M" [--only] [--force] [--dry-run]` | lines → questions → answers → markdown; OCRs first when needed; re-applies `fix` decisions | `Markdown_Questions/NN_*.md`, `.mbset/parsed/NN.json` |
| `route "$M" [--only]` | per source `parse` or `transcribe` from measurements (text layer, OCR confidence < 0.80, screenshots, > 30 % of parsed questions needing review) | terminal + the transcribe command |
| `transcribe "$M" --only NN [--pages-per 6] [--dpi 150] [--key-pages P]` | render pages, split into chunks, one self-contained worker brief per chunk; profile `transcribe: true` | `.mbset/transcripts/NN/{pages,chunk_KK.brief.txt,manifest.json}` |
| `transcribe "$M" --status [--only]` | chunks transcribed / left | terminal |
| `worklist "$M" [--only] [--n K] [--max-items 60] [--per 8]` | closed review lists (text / answers / model answers) with crops; files costing more than `--max-items` are split into question ranges, one part per reviewer | `.mbset/packets/worklist/worklist_k.txt`, `out/<NN[_pK]>/` |
| `worklist "$M" --apply [--only]` | merge every reviewer's JSON per file and apply it with `fix` (text → answers + model answers → drops → additions, numbers resolved through the stems) | markdown + decisions |
| `show "$M" NN [--flags] [--q 3,7] [--dropped]` | questions with evidence: source number, page, per-option style/marks, answer evidence, flags | terminal |
| `answersheet "$M" [--only] [--q 1,4] [--per 6]` | crops of unanswered MCQs (or `--q`) labelled with markdown Q numbers | `.mbset/reports/answers_NN_k.png` |
| `fix "$M" NN --answers "1=A 2=C" --source marked` | set answers in batch (`--answer 3=B:key` per item also works) | markdown edited, decision stored |
| `fix "$M" NN --model-file f.json [--exp-source derived]` | model answers `{"N": "text"}` for written questions (`--exp-file` is the same flag) | `**Model Answer:**` set, `Answer Source: derived` |
| `fix "$M" NN --text-file t.json` | stem / options re-read from the page image: `{"7": {"stem": "…", "options": {"C": "…"}, "note": "…"}}` (exact wording; `null` removes an option) | text fixed, original logged, survives re-parse |
| `fix "$M" NN --add-file a.json` | a question the parser lost, re-read exactly from the page: `[{"after": 24, "stem": "…", "options": {…}, "page": 5}]` | inserted, logged, survives re-parse |
| `fix "$M" NN --clear-drops ocr` | after a better OCR/profile: remove drops that were made only because the text was garbled | questions return on the next parse |
| `fix "$M" NN --image 5=Images/NN_Q5.png` / `--drop 7,8 --reason "…"` | link an image / remove non-questions with a logged reason | counters account for drops |
| `figures "$M" [--only] [--q]` | crop figures for figure-dependent stems (embedded image or drawing nearest to the stem, else the question region) | `Images/NN_Qi.png`, linked; contact sheet |
| `spotcheck "$M" [--only] [--flagged] [--n]` | max(5, 10%) samples spread over the file: source crop beside markdown | `.mbset/reports/spotcheck_NN_k.png` |
| `review "$M" NN --spot "6/6 OK" [--note]` | record the spot-check verdict | state |
| `set "$M" NN --tag … --subject … --year … --confirm` | confirm / correct tags (`--exclude REASON`, `--include`, `--count-note`) | state |
| `renumber "$M"` | resolve duplicate NN prefixes: renames the markdown, moves its sha-matched parsed/OCR evidence, renames its `Images/<old>_*` crops to `<new>_*` and rewrites those paths in the markdown, parsed JSON and stored `fix --image` decisions (an image linked by both sources is left in place and reported) | files renamed |
| `check "$M" [--only] [--all] [--quiet] [--json f]` | the Stage 2+3 gate; exit 1 on hard failures | `.mbset/reports/check_DATE.md` |
| `catalog "$M"` | `00_CATALOG_OF_ALL_FILES.md` + `tag_map.json` generated from state (old catalog backed up) | markdown |
| `packets "$M" --n 4` | balanced work packets for parallel agents, each with a self-contained worker brief (see `parallel-workflow.md`) | `.mbset/packets/packet_k.md`, `packet_k_brief.txt` |
| `lock "$M" 3,7 --owner A [--release]` | claim sources for one agent | `.mbset/locks/NN.lock` |
| `build "$M" [--category-id --category-name] [--out]` | check → build_module_template → validate → audit | `<Module>_Questions.xlsx` |
| `status "$M"` | one line per source: stage, class, pages, questions, answered | terminal |
| `run "$M"` | inventory → ocr → parse → check in one go | terminal |
| `report "$M"` | final user report: per-file counts, answer-source breakdown, every derived answer, exclusions, bias flags | terminal + report file |
| `doctor ["$M"]` | environment (tools, Python packages) and optional module health; OK / WARN / FAIL | exit 1 on FAIL |
| `tidy "$M" [--apply] [--restore DATE]` | standardize the folder to the deliverables layout; dry run by default, `--apply` moves to `_trash/<date>/` with a manifest | `.mbset/reports/tidy_DATE.md` |
| `crossdup ROOT…` | sources byte-identical across modules (report only, hashes cached) | terminal |
| `lectures "$M" plan/match/apply/check` | two-phase lecture workflow: subcategories file with empty ids → match official rows to lecture sources → `Lectures/<subcategoryId>.pdf` → verify | `.mbset/lectures_manifest.json` |

## The transcribe route
A chunk JSON (written by the worker, see the brief for the full rules):
```json
{"pages": [7, 8, 9, 10, 11, 12],
 "questions": [{"page": 7, "number": 12, "stem": "…", "options": {"A": "…", "B": "…"},
                "answer": "B", "answer_source": "marked", "model_answer": null,
                "model_answer_source": null, "figure": false}],
 "skipped_numbers": [], "notes": ""}
```
`parse --only NN` ingests every chunk in page order: options must run A.. in order, the key must be one of
the options, `answer_source` must be key / marked / online / derived (written questions: `model_answer`
with key / derived). Numbering gaps not listed in `skipped_numbers`, missing chunks (hard failure) and stems
absent from the page's OCR / text layer (`transcript_not_in_page_text`) are reported. `fix` decisions are
re-applied on every ingest, exactly as for parsed sources.

## The review loop for one parsed source
1. `parse --only NN` → read the summary line: counters equal? answered = MCQ? distribution sane?
2. `show NN --flags` → for each flag, decide: profile problem (fix YAML, re-parse) or single
   question (`fix`). Typical flags: `unnumbered`, `numbering_gap_before`, `letters_not_sequential`,
   `option_marker_repaired_*`, `possible_chimera`, `stem_prefix_cut`, `text_after_options`,
   `low_ocr_confidence`, `answer_sources_disagree`, `several_options_with_*`, `figure_dependent`.
3. `show NN --dropped` once per file — the noise filter must not have eaten a question.
4. Unanswered MCQs → `answersheet`, view the PNGs, `fix --answers … --source marked`. If the source
   truly has no answer: answer from knowledge with `--source derived` and report the count.
5. `figures --only NN` when figure-dependent stems exist; view the contact sheet.
6. `spotcheck --only NN`, view the sheets, `review NN --spot "k/k OK"` (or fix and re-check).
7. `set NN --confirm` (or `--tag …`), then `check --only NN` → 0 hard failures. A suggested tag
   never carries a guessed year: when the filename has none, the tag comes without it, `check` warns,
   and the year is read from the source header (`set NN --tag "… 2024" --year 2024`).

## Speed reference (Endocrinology, 41 sources, 1 244 golden questions)
Inventory 7 s · OCR 283 scanned pages 8 min (2×4 workers, cached afterwards) · parse all 54 s ·
check 1 s · build 3 s. Digital sources come out complete with answers; scanned exams need the
visual answer pass (≈ 5 sheets per 30-question exam).
