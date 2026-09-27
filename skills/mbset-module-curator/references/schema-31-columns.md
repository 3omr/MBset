# 32-Column Question Bank Schema Specification

The exact schema required by the MBset platform for importing questions, plus the migration map for the legacy layout found in older modules.

## Canonical header (use this for all new work)

```
id, Cas, Text, Image, explanationImage, A, B, C, D, E, F,
A_EXP, B_EXP, C_EXP, D_EXP, E_EXP, F_EXP, Correct, Hint, EXP, Note, Type,
categoryId, categoryName, subcategoryId, subcategoryName,
tagSuggere, Year, Tag, ImageMasks, ExplanationImageMasks, ModelAnswer
```

In use by `CVS_Questions.xlsx`, `CNS_Questions.xlsx`, `NHB_Questions.xlsx`, `Behavioral_science_Questions.xlsx`.

| Index | Column | Format | Mandatory | Default | Description |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **0** | `id` | Empty | NO | `None` | **Must be empty.** Platform assigns the ID on import. |
| **1** | `Cas` | String | NO | `None` | Case study / patient vignette. |
| **2** | `Text` | String | **YES** | - | Clean stem: no Arabic, no leading numbering, no markdown markers. |
| **3** | `Image` | String | COND | `None` | **Mandatory for figure-dependent questions** — relative path such as `Images/05_Q1.png`. |
| **4** | `explanationImage` | String | NO | `None` | Explanation image. |
| **5** | `A` | String | COND | `None` | Option A. Mandatory for `QCS`. |
| **6** | `B` | String | COND | `None` | Option B. Mandatory for `QCS`. |
| **7-10** | `C`-`F` | String | NO | `None` | Options C-F, filled sequentially with no gaps. |
| **11-16** | `A_EXP`-`F_EXP` | String | NO | `None` | Per-option explanations. |
| **17** | `Correct` | String | COND | `None` | `QCS`: one uppercase `A`-`F` that exists among populated options. `QROC`: empty. |
| **18** | `Hint` | String | NO | `None` | Hint. |
| **19** | `EXP` | String | NO | `None` | Explanation for `QCS`; empty for `QROC`. |
| **20** | `Note` | String | NO | `None` | Internal note. |
| **21** | `Type` | String | **YES** | - | `'QCS'` or `'QROC'`. |
| **22** | `categoryId` | String | **YES** | - | e.g. `'DamiettaFa_CVS'`. |
| **23** | `categoryName` | String | **YES** | - | e.g. `'CVS'`. |
| **24** | `subcategoryId` | String | NO | `None` | Blank for bulk question upload. |
| **25** | `subcategoryName` | String | NO | `None` | Blank for bulk question upload. |
| **26** | `tagSuggere` | String | NO | `None` | Discipline for department/professor sources; `None` for general exams. |
| **27** | `Year` | Integer | **YES** | - | Exam/publication year from the source. |
| **28** | `Tag` | String | **YES** | - | Comma-separated taxonomy tags. |
| **29** | `ImageMasks` | String | NO | `None` | Mask coordinates. |
| **30** | `ExplanationImageMasks` | String | NO | `None` | Mask coordinates for explanations. |
| **31** | `ModelAnswer` | String | COND | `None` | `QROC`: the complete model answer (platform import format). Empty for `QCS`. |

---

## Key platform invariants

1. **Nullability** — empty cells are Python `None` (blank cells via `openpyxl`), never the strings `'None'` or `'null'`.
2. **`id`** — always empty; numeric IDs collide with existing database records.
3. **`Type` discrimination**
   - `QCS`: at least `A` and `B` populated, `Correct` ∈ `{A..F}` and present among the populated options.
   - `QROC`: options `A`-`F` all `None`, `Correct` and `EXP` empty, `ModelAnswer` holds the model answer. (In the markdown a written item still carries `**Correct Answer:** -` and its model answer as `**EXP:**`; the builder moves it.)
4. **Sequential options** — `A` first, no letter gaps. After repacking, move `Correct` with the options.
5. **No duplicate normalized stems** in the finished file.
6. **`Image`** — populated for every figure-dependent question; a figure-dependent question with an empty `Image` is a defect.

---

## Legacy layout (do not produce; migrate when touched)

`Genetics_Questions.xlsx` and `POD_Questions.xlsx` use a different 31-column header:

```
id, category, categoryName, title, Text, A, B, C, D, E, F,
image, image_A, image_B, image_C, image_D, image_E, Correct, justification, EXP, Cas, Type,
difficulty, importance, subcategoryId, subcategoryName, tagSuggere, Year, Tag, repetition, verified
```

### Migration map → canonical

| Legacy | Canonical | Note |
| :--- | :--- | :--- |
| `category` | `categoryId` | Same value |
| `categoryName` | `categoryName` | Unchanged |
| `title` | — | Drop (fold into `Text` only if it carries stem content) |
| `Text`, `A`-`F`, `Correct`, `EXP`, `Cas`, `Type`, `subcategoryId`, `subcategoryName`, `tagSuggere`, `Year`, `Tag` | same name | Unchanged |
| `image` | `Image` | Rename |
| `image_A`-`image_E` | `A_EXP`-`E_EXP` are **not** equivalents | Drop unless they hold per-option images; then keep the paths aside and re-attach manually |
| `justification` | `EXP` | Merge into `EXP` if `EXP` is empty, else append |
| `difficulty`, `importance`, `repetition`, `verified` | — | Drop (curation metadata, keep in the catalog instead) |
| — | `explanationImage`, `A_EXP`-`F_EXP`, `Hint`, `Note`, `ImageMasks`, `ExplanationImageMasks` | Add as `None` |

Column **order** matters as much as the names: the canonical order above is what the validator enforces.
