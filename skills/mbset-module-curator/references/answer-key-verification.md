# Answer-Key Provenance & Verification

Stage 2 of the pipeline. A question bank with complete stems and wrong keys is worse than no bank at all: students memorize the error. This reference defines how a key earns its place in the Excel.

---

## 1. Why this gate exists

A forensic audit of the existing modules found systematic placeholder keys that every earlier check passed:

| Source group | MCQs | Answer distribution |
| :--- | ---: | :--- |
| CNS · `Department, Physiology 2025` | 228 | **A = 100%** |
| CNS · `Department, Physiology 2026` | 560 | **A = 97%** |
| CNS · `Department, Histology 2026` | 173 | **A = 91%** |
| CNS · `Exams, End 2023` / `End 2025` | 90 / 90 | **A = 84%** each |
| CNS · `Exams, End 2024` | 90 | A = 71% |
| CNS · `Exams, End 2021` | 45 | A = 60% |

Roughly 1,100 CNS questions carry a key that cannot be real. Schema validation reported zero errors on all of them, because each `Correct` letter did match a populated option. Only a distribution check catches this.

---

## 2. Provenance labels

Every MCQ in a markdown file carries `**Answer Source:**` with one of:

| Label | Meaning | Required evidence |
| :--- | :--- | :--- |
| `key` | Printed answer key, answer grid, or "Answer: C" line in the source | Cite the page in the catalog |
| `marked` | Correct option bolded / highlighted / ticked / bulleted / colored in the source | Re-check the letter after any option repacking |
| `online` | Recovered from the source's own online quiz (e.g. the DocReader URL printed in the PDF) | Record the URL in the catalog |
| `derived` | The source has no key anywhere; the answer comes from medical knowledge | **Must be reported to the user with per-file counts before compiling** |

Rules:
- `derived` is a last resort, never a default, and never silent.
- An answer is never copied from a "similar" question in another file.
- If a source has a key for only part of its questions, the rest are `derived` — not inherited.

---

## 3. Recovering `marked` answers OCR destroyed

Highlighting, bullets and bold runs frequently swallow the option letter, producing option lists that start at `B` or skip a letter.

1. Confirm visually: render the page (`pdftoppm -png -r 200`) and look at which option is emphasized.
2. Restore the missing letter and repack so options run `A, B, C, D`.
3. Set `Correct` to the **repacked** letter of the emphasized option.
4. A file where many questions lost the same letter is a formatting pattern, not a coincidence — handle the whole file with one inspected rule, verified on 5 sampled questions.

---

## 4. The statistical bias gate (hard fail)

For every source file with ≥ 15 MCQs:

```bash
python scripts/audit_question_bank.py --markdown <Module>/Markdown_Questions
python scripts/audit_question_bank.py --excel <Module>/<Module>_Questions.xlsx --by-tag
```

| Max single-letter share | Verdict |
| :--- | :--- |
| ≤ 45% | Pass |
| 46-60% | Investigate: sample 10 answers against the source before proceeding |
| > 60% | **Fail** — treat as a placeholder default and re-key the file from the source |
| ≥ 90% | Fabricated key; the file must be re-extracted, not patched |

A genuine exam distributes answers roughly evenly (20-30% per letter across A-D). A real file can lean, but it does not lean to 84%.

---

## 5. Spot-check sampling (every file, no exceptions)

- Sample `max(5, 10% of questions)` per file, spread across the file (not the first five).
- Compare stem, all options, and the key against the rendered source page.
- Record in the catalog: `spot-check 6/6 OK` or `spot-check 5/6 — Q23 key corrected B→C`.
- Any mismatch found means the whole file is re-verified, not just the sampled question.

---

## 6. What goes in the catalog

Per source row:

```
| 05 | End | End 2021.PDF | 10 p | 05_End_2021.md | 50 | 50 MCQ | key 50 / marked 0 / online 0 / derived 0 |
  A28% B22% C26% D24% | spot-check 5/5 OK | Exams, End 2021 | None | 2021 | OK |
```

A module is not ready for upload while any row shows an unexplained `derived` bulk, a failed bias gate, or a missing spot-check.
