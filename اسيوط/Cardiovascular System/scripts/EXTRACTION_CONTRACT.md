# CVS (Assiut) — Stage-1 extraction contract

Every question source in `Raw_PDF_Questions/1- Cardiovascular system/` becomes
**exactly one** markdown file in `Markdown_Questions/<NN>_<Name>.md`. No grouping,
no merging, no splitting. A source that genuinely cannot be extracted still gets a
file whose header says `EXCLUDED — <reason>`.

`Markdown_Questions/01_All_Quizzes_CVS.md` is the finished reference example.
`scripts/extract_01_quizzes.py` is the reference extractor.
`scripts/lib_md.py` holds the shared helpers — **use it**, do not re-implement:
`Q`, `write_md`, `clean`, `strip_numbering`, `match_correct`, `has_arabic`.

## Output format (parsed later by the compiler — do not vary it)

```markdown
# Source NN — <Title>

- **Source file:** <relative path>
- **Type:** <format, page count>
- **Tag:** <tag string>
- **tagSuggere:** <Subject or None>
- **Year:** <integer or None>
- **Answer source:** <summary>

---

### Q1: <clean stem>

- **A)** <option>
- **B)** <option>
- **C)** <option>
- **D)** <option>

**Correct Answer:** C
**Answer Source:** key
**Image:** Images/NN_Q1.png
**EXP:** <explanation or model answer>

---
```

- Written/essay questions: no option lines, `**Correct Answer:** -`, the full model
  answer in `**EXP:**`.
- `**Answer Source:**` is one of `key` (printed key or grid), `marked`
  (bolded/highlighted/ticked **as correct** in the source), `online` (the source's own
  online quiz), `derived` (no key anywhere — answered from medical knowledge).
- **A student's own selected answer is not a key.** A Moodle/phone screenshot that only
  shows "Answer saved" with a filled radio records what the student picked; unless the
  page separately marks the option *correct*, the answer is `derived`, not `marked`.
- Options run `A`, `B`, `C`, … with no gaps. `**Correct Answer:**` must be a letter that
  actually exists among the emitted options.
- One script per source: `scripts/extract_<NN>_<slug>.py`, runnable as
  `python3 scripts/extract_<NN>_<slug>.py` from the module root, printing its counts.

## Hard rules

1. **Never invent an answer silently.** Every `derived` answer is counted and printed by
   the script at the end of its run.
2. **Never trust `pdftotext -layout` on a multi-column PDF.** Probe the layout first
   (`pdfinfo`, render a page with `pdftoppm -png -r 150` and actually look at it). Use
   PyMuPDF `page.get_text("blocks")` with coordinates, or
   `/home/omar/MBset/.agents/skills/mbset-module-curator/legacy/extract_pdf_columns.py`.
3. **Never skip a source.** Three counters must agree: highest question number in the
   source, option-`A` blocks in the extracted text, `### Q` headings in the markdown.
   Print all three. If they disagree, fix the extractor — do not explain it away.
4. **Zero Arabic characters** (`[؀-ۿ]`) in any stem, option or explanation.
   Arabic in a *filename* is fine and is not translated.
5. **Statistical bias gate.** For any file with >= 15 MCQs print the answer-letter
   distribution. Max single-letter share > 45% means the extraction is wrong — re-extract,
   do not patch. A real exam sits near 20-30% per letter.
6. **Figure-dependent questions** (stem mentions figure/diagram/shown/arrow/labelled/
   photomicrograph/this image) must carry an `**Image:**` line pointing at a real cropped
   PNG in `Images/<NN>_Q<n>.png`. Crop with `pdftoppm -png -r 200 -f N -l N -x X -y Y -W W -H H`
   or `fitz` clip rects, then open the PNG and confirm it is not blank or half-cut. A
   figure question shipped without its image is a defect; if the figure is unrecoverable,
   drop that question and log it.
7. **Repair notation, never delete it**: `Ca**`→`Ca²⁺`, `Na*`→`Na⁺`, `B1`→`β1`,
   `um`→`µm`, `->`→`→`. `lib_md.clean()` already does the common ones.
8. Strip leading numbering (`1.`, `25-`, `Q1:`), Moodle chrome (`Home » My courses`,
   `Select one:`, `Flag question`, `Clear my choice`, `Your answer is …`, `Quick Links`,
   `About Us`, `Terms of use`, `FAQ`, `Support`, `Contact`, `Lorem Ipsum …`), phone status
   bars, and trailing answer-key grids once they have been consumed.

## Assiut tagging

| Kind | Tag | tagSuggere | Year |
| :-- | :-- | :-- | :-- |
| Midterm exam | `Exams, Midterm <Year>` | None | exam year |
| Final exam | `Exams, Final <Year>` | None | exam year |
| Department question bank | `Department, QBank, <Subject> <Year>` | `<Subject>` | book year or None |
| Department quiz | `Department, Quizzes, Quiz <N>` | None | **None** |
| Department formative | `Department, Formative, Week <N>` | None | **None** |
| Group discussion | `Department, GDs, <Subject> GD <N> <Year>` | `<Subject>` | year or None |
| Other faculty / outside source | `External, <Source> <Year>` | `<Subject>` or None | year or None |

`<Subject>` is one of Anatomy, Physiology, Histology, Biochemistry, Microbiology,
Parasitology, Pathology, Pharmacology. Multidisciplinary sources get `tagSuggere = None`.
Quizzes and formatives carry **no** year unless the year is in the source filename.
`Year` is the year the source states — never the current academic year.

## OCR sources

Many sources are image-only (`pdftotext` returns ~1 char per page). For those:
`pdftoppm -png -r 300`, then `tesseract <png> <out> -l eng --psm 6`, page by page.
Inspect the first two OCR outputs before continuing. Typical damage to repair: `l/1/I`
and `0/O` confusion in option letters, flattened superscripts, option letters swallowed by
a highlight box. Student handwriting that OCRs to gibberish is stripped, never guessed.
A page too degraded to read reliably is logged as `EXCLUDED — unreadable scan` for those
questions only; the rest of the file is still extracted.
