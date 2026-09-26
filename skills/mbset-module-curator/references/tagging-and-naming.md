# Tagging & Naming Reference

Tagging rules and merge strategies across all MBset modules. Tags are how students filter by source, so a tag that does not match one of these families is a defect.

---

## Damietta taxonomy

| Family | Pattern | `tagSuggere` | `Year` | Real examples in the repo |
| :--- | :--- | :--- | :--- | :--- |
| **Department books** | `Department, <Subject> <Year>` | `<Subject>` | book year | `Department, Physiology 2026`, `Department, Histology 2026`, `Department, Pharmacology 2025` |
| **End-round exams** | `Exams, End <Year>` | `None` | exam year | `Exams, End 2021`, `Exams, End 2026` |
| **Final exams** | `Exams, Final <Year>` | `None` | exam year | `Exams, Final 2022`, `Exams, Final 2025` |
| **Formatives** | `Exams, Formative <Year>` | `None` | exam year | `Exams, Formative 2025`, `Exams, Formative 2022` |
| **Professor / doctor collections** | `Professor, Dr <Name> <Year>` | `<Subject>` when single-subject | collection year | `Professor, Dr Elmorshdy 2025` (MCQ and written collections of the same doctor share the tag) |
| **External sources** | `External, <Source> <Year>` | `<Subject>` or `None` | if known | `External, Psycho 404 2026`, `External, Zagazig 2021` |

Rules:
- `<Subject>` is always a capitalized standard discipline: `Anatomy`, `Physiology`, `Histology`, `Biochemistry`, `Microbiology`, `Parasitology`, `Pathology`, `Pharmacology`.
- `<Year>` is the year stated in the source file or its filename — never inferred from the module's current academic year.
- Multidisciplinary sources (exams, formatives) get `tagSuggere = None`, because they mix subjects.
- A second-round exam keeps its own label: `Exams, Final 2026 Round 2`.
- **Formatives of the same year are one tag, not two.** Formative 1 and Formative 2 of 2025 both carry `Exams, Formative 2025`; the round number is not part of the tag. Keep the two source files separate in `Markdown_Questions/` (Stage 1 is still 1-to-1) — only the tag is shared.
- Older banks tagged formatives `Formative, Formative <N> <Year>`. That family is retired: rewrite it to `Exams, Formative <Year>` when touching the module.
- **One canonical spelling per professor.** Source filenames transliterate the same name several ways (`Dr elmorshdy questions(MCQ) 2025.pdf` and `Dr Morshdy revision Questions(Written) 2025.pdf` are the **same** doctor). Pick one spelling — `Dr Elmorshdy` — and use it in every tag for that person, whatever the filename says. Two spellings split one professor into two filters for students, which is a defect. Before creating a new `Professor,` tag, check the tag census (below) for a variant of the same name already in use.

---

## Assiut taxonomy

For modules belonging to the Assiut curriculum (`AssiutUniv_*`):

### 1. `Exams`
* Midterm: `Exams, Midterm <Year>` — Final: `Exams, Final <Year>`
* `Year`: integer matching the exam year, or `None`.

### 2. `Department`
* **Question banks**: `Department, QBank, <Subject> <Year>` (or without the year when the source has none). `tagSuggere = <Subject>`.
* **Quizzes**: `Department, Quizzes, Week <N>` / `Department, Quizzes, Quiz <Name>` — **no year** in the tag or the `Year` column unless it is explicitly in the source filename.
* **Formatives**: `Department, Formative, Week <N>` — same no-year rule.
* **Group discussions**: `Department, GDs, <Subject> GD <N> <Year>`.

### 3. `External`
* `External, <Source> <Year>` or `External, Dr. <Name>` — material from outside the faculty. `tagSuggere = <Subject>` when single-subject.

---

## Tag merging & deduplication

When a question recurs across sources:

1. **Concatenate unique tags** into one comma-separated string, department/professor tags first, then exams in chronological or discovery order:
   `Department, Histology 2026, Exams, End 2025, End 2021`
2. **Preserve `tagSuggere`**: if any occurrence carries a discipline (from a department/professor source), keep it.
3. **`Year`**: keep the department-book year, or the most recent exam year when there is no department source.
4. Never emit the same tag twice in one string, and never merge two different families into one token (`Department, Exams 2025` is wrong).

---

## Sanity check before upload

```bash
python scripts/audit_question_bank.py --excel <Module>/<Module>_Questions.xlsx --by-tag
```
The per-tag table it prints doubles as a tag census: any group whose name does not match a family above, or whose question count does not match the catalog, is a tagging error.
