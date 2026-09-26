# Parser profiles

A profile (`<Module>/.mbset/profiles/NN.yaml`) describes the **format** of one source, never its
content. `inventory` triages the file, `parse` writes a profile from the matching template in
`references/profiles/` the first time, and the agent edits it when `parse` / `check` / `show --flags`
show the format was read wrongly. Then `parse --only NN` again — never retype questions.

Merge order: built-in defaults ← `template:` ← the file's own keys. `profile --only NN --print`
shows the effective result. `profile --only NN --force` rewrites it from the triage.

## Fields

| Field | Default | Use it when |
| :--- | :--- | :--- |
| `template` | from triage | switch recipe: `digital_single`, `digital_two_column`, `scanned`, `moodle_review`, `docreader`, `docx`, `pptx`, `screenshots`, `department_book_sections`, `written_only` |
| `text` | `auto` | force the text source: `native` (PDF text layer), `ocr` (cached Tesseract), `docx`, `pptx`, `plain` |
| `columns` | `auto` | `2` when the column probe misses a two-column layout (stems interleaved in `show`), `1` to disable splitting |
| `split` | `null` | force the gutter x in points when auto-detection picks the wrong gutter |
| `pages` | all | `"3-40"` (1-based) — skip covers, indexes, answer pages parsed separately |
| `skip_patterns` | `[]` | regexes for recurring junk lines the noise filter does not know (running headers, watermarks) |
| `stop_patterns` | `[]` | stop parsing at e.g. `"^Answers?\\b"` or `"^Model answers"` |
| `question_start` | `12.` `12)` `12-` `Q12:` `(12)` `24.3 ` | a file numbers questions differently (e.g. `"^\\s*Q\\s*(\\d+)\\b"`); keep one capture group |
| `option_pattern` | `a.` `(a)` `A)` `a-` `[a]` | options use another marker; group 1 is the letter |
| `options_inline` | `auto` | `true` for `a. x  b. y  c. z` on one line, `false` if stems are being split at words like "a." |
| `sections_restart` | `true` | `false` when a `1.` inside a question list is not a new section |
| `numbering` | `auto` | `none` when questions are unnumbered (found from option runs / paragraphs) |
| `declared_total` | `null` | the source states "Total 30 questions" — `check` then requires exactly that |
| `type` | `auto` | `mcq` (flags any question without options) or `written` (all QROC) |
| `answers.mode` | `auto` | `grid`, `inline`, `marked`, `online`, `none` to force one method |
| `answers.grid_pages` | whole file | `"-1"` (last page), `"45-48"` — where the key grid lives |
| `answers.grid_pattern` | `12-C`, `12 C`, `12) c`, `12=C` | unusual key formats |
| `answers.inline_pattern` | `Answer: C`, `Ans - c`, `Key: B` | a per-question answer line in another wording |
| `answers.marked_by` | all mark kinds | restrict to the kinds this file really uses, e.g. `[highlight]` when bold is used for emphasis |
| `answers.tint` | `true` | pixel-colour detection on scans; `false` when the scan is coloured paper |
| `answers.docreader_quiz` | `null` | the id in `doc-reader-guide.com/mcq-quizzes/<id>` printed in the PDF |
| `written.answer_marker` | `Answer:` / `Model answer:` | where a written question's model answer starts |
| `ocr.dpi`, `ocr.psm`, `ocr.rotate` | 300, 3, 0 | re-OCR with `ocr --only NN --force` after changing (psm 4/6 for tables, rotate 90/180) |
| `ocr.tool` | `tesseract` | `paddle` = PaddleOCR (`.venv-smart-ocr`): far better on phone photos, curved or unevenly lit scans and bold headings; try it first when a scanned exam loses questions |
| `ocr.split` | 1 | `2` = two book pages per scan: cut at the gutter and OCR each half (stops lines running across the spread) |
| `ocr.normalize`, `ocr.threshold` | off | Tesseract only: flatten uneven lighting / binarize (0-255) when highlighter or shading hides text |
| `notes` | `""` | free text for the next agent (what was special about this file) |

## Recipes

**Two-column stems interleaved** → `columns: 2` (and `split: 297` if the gutter is off-centre).

**Department book with a key grid after each chapter**
```yaml
template: department_book_sections
answers: {mode: grid, grid_pages: "12,25,40"}
```
Sections are matched to grids in order; counts are checked per section.

**Moodle review export** → `template: moodle_review`; "The correct answer is: …" becomes `key`.

**DocReader PDF with an online quiz** → `answers: {mode: online, docreader_quiz: 1234}`.

**Scanned exam with a pen tick on the letter** → leave `answers.mode: auto`; the unanswered MCQs
go to `answersheet`, and the agent reads the marks visually and fixes them with `fix --answers`.

**Written-only file (short essays)** → `template: written_only`; model answers come from the
source (`written.answer_marker`) or are derived and recorded with `fix --exp-file` (reported).

**Excerpt that starts at Q121** — nothing to do; the first number > 3 opens the section.

**A counter mismatch that is real** (the source skips number 17) →
`mbset.py set "$M" NN --count-note "source skips no. 17"`; never pad or renumber the source.

## Pen-marked scans
A tick or circle often destroys the option marker: `D Incision`, `DIncision`, `By Infected`, a row
with no letter at all between two options, as the first row after the stem, or after the last option.
In OCR mode the parser rebuilds the missing option from the letter sequence and flags it
`option_marker_repaired_<L>_…_possible_mark` — the damaged option is usually the marked answer.
Confirm it on the answer sheet; the flag alone is never an answer.
