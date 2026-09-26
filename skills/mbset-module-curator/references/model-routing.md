# Model routing — which model for which step

The expensive part used to be a large model reading every page and typing every question. With
`mbset.py` the text never passes through the model; what remains is judgement on flagged items.
Route each step to the cheapest model that does it reliably.

| Step | Needs | Suggested model |
| :--- | :--- | :--- |
| `inventory`, `ocr`, `parse`, `check`, `catalog`, `build` | nothing — deterministic scripts | any model / no model (run the commands) |
| Confirming tags, exclusions, count notes | reading filenames and the summary | small fast model |
| Profile fixes from `show --flags` (columns, pages, patterns) | reading evidence, editing YAML | small or mid model |
| Spot-check sheets (`spotcheck` PNGs) | comparing an image with text | mid model with vision |
| Answer sheets for pen-marked scans (`answersheet` PNGs) | reading handwriting ticks / circles reliably | strong vision model |
| Derived answers and QROC model answers | medical knowledge, must be correct | strongest model; always reported |
| Coordinating packets, final report | overview | the main session model |

## Rules
- Never let any model transcribe question text; if the parser output is wrong, the fix is a
  profile change or a single `fix`, both of which keep the source wording.
- A cheaper model that is unsure about a mark answers `?` (leaves it) rather than guessing; the
  strong model then does a second pass on only those sheets.
- Derived answers are never mixed with read answers: `--source derived`, and the counts go in the
  final report.
- Batch work: one answer sheet holds 6 questions, so a 30-question exam is 5 images and one
  `fix --answers` call — do not process questions one message at a time.
