# Extraction Playbook — Format Triage, Columns, OCR & Figures

Stage 1 of the pipeline. The rule this file exists to enforce: **look at the file before you extract it**, and pick the recipe that matches its format.

> **With `mbset.py` (the default since v2)** triage is automatic (`inventory`) and each recipe below
> is a *profile* (`references/profiles/*.yaml`, fields in [`profiles.md`](./profiles.md)) executed by one
> parser — not a script per file, and never questions typed by the model. Use this playbook to
> understand a format and to choose profile settings when `show --flags` shows the parser misread a
> file. The manual commands below remain valid for inspecting a source by hand.

---

## 0. Triage in 60 seconds

```bash
pdfinfo "src.pdf" | egrep -i 'Pages|Page size'
pdftotext -layout -f 1 -l 2 "src.pdf" - | head -60      # is there a text layer at all?
pdftoppm -png -r 110 -f 1 -l 1 "src.pdf" page           # render page 1 and LOOK at it
```

| Signal from the probe | Class | Recipe |
| :--- | :--- | :--- |
| Clean text, one question per line block | Digital single-column | §1 |
| Text is interleaved: `1.What is…  C) Klinefelter` on one line | Digital multi-column | §2 |
| `pdftotext` returns almost nothing | Scanned / image-only | §3 |
| `Home » My courses »`, `Select one:`, `Flag question` | Moodle web export | §4 |
| Phone clock, battery, `Clear my choice` | Phone screenshot set | §4 |
| `DocReader Guide`, `Solve it online at: https://doc-reader-guide.com/...` | DocReader export | §5 |
| `.pptx` / slide-shaped pages | Slide deck | §6 |

Always render at least one page as PNG and actually view it. The text layer lies about layout; the image does not.

---

## 1. Digital single-column

```bash
pdftotext -layout "src.pdf" out.txt
```
Then parse question blocks by the numbering pattern actually used in that file (`1.`, `1)`, `Q1:`, `1-`). Confirm the pattern by eye first — mixing `a.`/`A)` option styles within one file is normal and both must be accepted.

---

## 2. Digital multi-column (the highest-risk class)

`pdftotext -layout` merges the columns horizontally and produces chimera stems. Extract each column with a crop box instead:

```bash
pdfinfo src.pdf | grep 'Page size'        # e.g. 595 x 854 pts
# left half, then right half, page by page
pdftotext -layout -f $p -l $p -x 0   -y 0 -W 300 -H 854 src.pdf -
pdftotext -layout -f $p -l $p -x 300 -y 0 -W 295 -H 854 src.pdf -
```

`mbset.py parse` detects the split per page and reads each column in order (profile `columns: auto|1|2`).
For one-off inspection only, the old helper is in `legacy/extract_pdf_columns.py` (`--probe` shows the detected split).

**Verification after column extraction** — all three must hold:
1. no line contains two different question numbers;
2. every question has a contiguous option run (`A`→`D`) with nothing from another question inside it;
3. the highest question number per section matches the count of `### Q` blocks for that section.

Watch for **section restarts**: department books restart at `1.` for each chapter. Record the boundaries; renumber continuously in the markdown.

---

## 3. Scanned / OCR pages

1. Render at high DPI before OCR: `pdftoppm -png -r 300 src.pdf pg`.
2. `mbset.py ocr` runs Tesseract per page (cached) and lists pages with low confidence. PaddleOCR is a fallback
   for those pages only — see [`legacy/smart-ocr-workflow.md`](../legacy/smart-ocr-workflow.md). Its output is a
   draft to check against the rendered page, never text to paste into the markdown.
3. OCR page by page, never the whole file blind; inspect the first two outputs before continuing.
4. Typical damage to repair:
   - superscripts/subscripts flattened: `Ca**` → `Ca²⁺`, `Na*` → `Na⁺`, `B1` → `β1`, `um` → `µm`;
   - `l`/`1`/`I` and `0`/`O` confusion inside option letters;
   - option letters swallowed by a highlight rectangle → see [answer-key-verification.md](./answer-key-verification.md) §3;
   - Arabic student handwriting rendered as pseudo-Latin gibberish → strip entirely.
5. If a page is too degraded to read reliably, mark those questions `EXCLUDED — unreadable scan` in the catalog. Never guess a stem.

---

## 4. Moodle exports & phone screenshot sets

1. Strip web chrome and status bars first (regex catalog in `noise-removal-and-curation.md` §A/§B).
2. Convert inline `Select one: a. … b. … c. …` runs into structured options.
3. **Decouple the preceding explanation**: in review pages the previous question's answer is printed immediately above the next stem — strip it before parsing.
4. Screenshot sets are usually **one question per image and out of order**: sort by filename/timestamp, then verify that the question numbers visible in the images form a continuous run. Missing screenshots are missing questions — list them in the catalog.
5. Moodle review pages mark the chosen and the correct option differently (`Your answer is correct`, a green tick). The **correct** marker is the key; the student's choice is not.

---

## 5. DocReader exports

Header looks like:
```
DocReader Guide
Department book 2026
Solve it online at: https://doc-reader-guide.com/mcq-quizzes/2116
Questions
1. The innermost layer of the heart wall is called:
```
These files are clean, single-column and **contain no answer key**. The key lives in the online quiz at the printed URL. Fetch it and label the answers `online`; if the URL is unreachable, the answers are `derived` and must be reported as such. Strip the header block, the URL line and the `Questions` divider from the extracted text.

---

## 6. Slide decks (.pptx) and .docx sources

Read the file's own XML/text rather than converting to PDF first — conversion loses the bold/highlight that marks correct answers. Keep the per-slide/per-paragraph order, and treat a slide's "Answer:" line as `key` provenance.

---

## 7. Figure-dependent questions

A stem matching `figure|fig\.|diagram|shown|this slide|arrow|labell?ed|photomicrograph|following image|picture` needs its picture.

1. Locate the question's page: `pdftotext -f N -l N` until the stem appears.
2. Render and crop:
   ```bash
   pdftoppm -png -r 200 -f N -l N src.pdf pg          # full page
   pdftoppm -png -r 200 -f N -l N -x X -y Y -W W -H H src.pdf crop   # region, in pixels at that DPI
   ```
   Or pull embedded raster images directly: `pdfimages -png -f N -l N src.pdf img`.
3. Save as `<Module>/Images/<Index>_<Qn>.png`, reference it in the markdown as `**Image:** Images/<Index>_<Qn>.png`, and carry it into the Excel `Image` column.
4. Verify the crop by viewing it — a blank or half-cropped figure is as broken as no figure.
5. If the figure genuinely cannot be recovered, the question is excluded and logged; it is never shipped text-only.

---

## 8. Post-extraction checklist (per file, before Stage 2)

- [ ] Question count agrees across all three counters (source numbering, option-A blocks, `### Q` headings).
- [ ] No chimera stems (text from two questions merged).
- [ ] Options start at `A`, sequential, no gaps, no duplicates, none under 2 characters.
- [ ] Zero Arabic characters; zero web/phone/OCR noise signatures.
- [ ] Medical notation repaired (`Ca²⁺`, `β1`, `µm`, `→`).
- [ ] Every figure-dependent question has an `**Image:**` line.
- [ ] Every MCQ has `**Correct Answer:**` and `**Answer Source:**`.
