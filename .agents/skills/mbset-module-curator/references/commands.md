# `mbset.py` — command reference

The procedure is in SKILL.md §2; this page lists every command and flag.

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
| `ocr "$M" [--jobs 2 --workers 4] [--force] [--all] [--searchable]` | Tesseract TSV per page for scanned sources, in parallel, cached by hash + settings; `--searchable` also writes an `ocrmypdf --redo-ocr -O 3` copy (`.mbset/ocrpdf/NN.pdf`, parse it with profile `text: ocrpdf`) | `.mbset/ocr/NN.json`; pages with low confidence listed |
| `profile "$M" [--only] [--force] [--print]` | write / show the per-source profile | `.mbset/profiles/NN.yaml` |
| `parse "$M" [--only] [--force] [--dry-run]` | lines → questions → answers → markdown; OCRs first when needed; re-applies `fix` decisions | `Markdown_Questions/NN_*.md`, `.mbset/parsed/NN.json` |
| `route "$M" [--only]` | per source: `parse`, `transcribe` (whole file) or `transcribe pages …` (only the bad pages: OCR < 0.60 or most questions flagged; the rest stays parsed) | terminal + the commands to run |
| `transcribe "$M" --only NN [--pages 4-9,15] [--format png\|pdf] [--pages-per 6] [--key-pages P] [--dispatch …]` | chunk briefs (6 pages each) for the pages to read; `pdf` = chunks of the ocrmypdf copy for PDF-reading workers; `--key-pages` = one key job instead of the key in every chunk; profile `transcribe: true` | `.mbset/transcripts/NN/{chunk_KK.pdf\|pages/,chunk_KK.brief.txt,key.brief.txt,manifest.json}` |
| `transcribe "$M" --status [--only]` | chunks transcribed / left | terminal |
| `consensus "$M" [--only NN]` / `--apply` | text-only second answer for every derived MCQ (brief per source in `.mbset/consensus/`); `--apply` marks disagreements `derived_disputed` → `worklist` | `.mbset/consensus/NN.{brief.txt,json}` |
| `spotcheck "$M" --only NN --worker` / `review "$M" --auto` | a brief for a worker to compare sampled pages (≈10 %, flagged first, every question on them) with the markdown; `review --auto` records `k/k OK`, differences go to `worklist` as text items | `.mbset/spotcheck/NN.{brief.txt,json}` |
| `dispatch "$M" [--only NN] [--dispatch '<cmd {brief}>' --parallel 4]… [--stagger 20] [--retries 2]` — repeat `--dispatch`/`--parallel` for several worker pools on one queue | run every pending chunk / key brief with the worker command saved at `init` (shell workers; Claude subagents use the Agent tool), N at a time, retrying briefs whose JSON is missing | `.mbset/work/dispatch/*.log` |
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
 "printed_count": 9,
 "questions": [{"page": 7, "number": 12, "case": "", "stem": "…", "options": {"A": "…", "B": "…"},
                "answer": "B", "answer_source": "marked", "model_answer": null,
                "model_answer_source": null, "figure": false}],
 "skipped_numbers": [], "notes": ""}
```
`parse --only NN` ingests every chunk in page order: options must run A.. in order, the key must be one of
the options, `answer_source` must be key / marked / online / derived (written questions: `model_answer`
with key / derived). Numbering gaps not listed in `skipped_numbers`, missing chunks and a `printed_count` that differs from the
chunk's questions (hard failures), and stems
absent from the page's OCR / text layer (`transcript_not_in_page_text`) are reported. `fix` decisions are
re-applied on every ingest, exactly as for parsed sources.
