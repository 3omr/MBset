# Benchmark — mbset.py v2 on Endocrinology (2026-09-26)

Golden = the existing, hand/LLM-extracted `أزهر دمياط/Endocrinology/Markdown_Questions` (1 244 questions).
New = `mbset.py` run on a copy of the same 41 sources, no manual review yet.
Comparison: `tests/compare_markdown.py --dirs <golden> <new> --map endo_map.json`
(fuzzy stem match ≥ 80; answer agreement compares the *text* of the correct option).

## Time (41 sources, 283 scanned pages)
| Step | Time |
| :--- | ---: |
| inventory (hash, triage, tags) | 7 s |
| OCR, all scanned sources, 3×4 workers (once; cached) | 7 min 11 s |
| parse, all sources | 55 s |
| check | 1 s |
| build (compile + validate + audit) | 3 s |

The previous workflow typed each file by hand through an LLM session (hours per module).

## Quality before review
| | files | questions | MCQ | answered automatically |
| :--- | ---: | ---: | ---: | ---: |
| digital (text layer, docx) | 18 | 846 | 784 | 745 (95 %) |
| scanned | 23 | 903 | 527 | 206 (39 %) — rest via `answersheet` |

Against the golden: recall 0.824 overall, stem fidelity 99–100 on digital files, answer agreement
817/1 001 (0.816). Digital files with keys/marks match the golden on 97–100 % of answers
(Parathyroid 33/33, Thyroid Mansoura 69/69, Introduction 29/29, Diabetes 87/88, Kumar 119/124).

Why the golden numbers understate v2:
- **Golden stems are paraphrased** in several files (End 2023, Lippincott, case questions), so an
  exact extraction does not "match" them — e.g. golden End 2023 Q4 is a one-line summary of a
  6-line clinical stem.
- **Golden answer errors**: `17_Formative_2024` disagrees with the red-marked options in the source
  (e.g. "main treatment for adrenal hypofunction": source marks hormone replacement, golden says
  chemotherapy). 24 of its 58 answers disagree with v2; the sampled ones follow the source's red marks — re-verify this file.
- **Golden omissions**: `09_Thyroid_questions` (thyroid question منير.pdf) has 53 questions in the
  source; the golden has 41 and silently drops all 8 written questions and 4 case questions while
  its catalog says "audit passed".

Remaining weak spots (need the visual review loop, by design): pen-marked scanned exams (End 2021 /
2023 / 2024, Final 2024, Summative 2025, Cairo, Schwartz, Mogy) and scanned books with explanations
between questions (Endocrine surgery). Their answers come from `answersheet` + `fix --answers`;
the 4 End 2023 answers read that way all agreed with the golden.

## Regression tests
`python3 -m unittest discover -s tests` — 14 synthetic tests for the format rules that broke during
development (numbering, doses/ages, sections, option grids, RTL, key grids, marks, no default answer,
overrides surviving a re-parse, the cleaner never inventing an answer).
