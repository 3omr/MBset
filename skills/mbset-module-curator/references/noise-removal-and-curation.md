# Deep Noise Removal & Question Bank Curation Guide

This reference outlines the technical standards, regex rules, and verification procedures required during the **Three-Stage Question Bank Curation Pipeline**.

---

## 1. The Core Philosophy: 1-to-1 Markdown Before Excel

Raw OCR or direct PDF-to-Excel extraction inevitably injects corrupted fragments, missing options, and platform upload errors. 

**The Rule**:
1. Every source file must first be extracted to an independent `.md` file in `<Module>/Markdown_Questions/<Index>_<Name>.md`.
2. Strictly no merging or grouping in Stage 1.
3. The agent owns noise removal on every Markdown file. With `mbset.py` the parser already applies these rules (`scripts/mbset/noise.py`) and `mbset.py check` fails on any surviving noise signature; add recurring junk to the source profile's `skip_patterns` and re-parse. For markdown produced another way, `clean_markdown_noise.py --dir …` reports changes (dry run) and `--write` applies them — it never changes an answer. Never leave routine cleanup for the user.
4. Completeness and accuracy must be verified against source page counts.
5. Only then may questions be aggregated into `<Module>_Questions.xlsx`.

---

## 2. Standard Noise Signatures & Cleaning Regexes

### A. Moodle / LMS Web Chrome & Footers
Online quizzes frequently export website chrome, review metadata, and theme boilerplate.

| Artifact | Regex / Pattern | Action |
|---|---|---|
| Moodle Theme Lorem Ipsum | `r'Lorem Ipsum.*?passages\.?'` | Remove completely |
| Moodle Breadcrumbs | `r'Home\s*[»]\s*My courses\s*[»].*?Quiz\s*\d+'` | Remove completely |
| Navigation & Support Links | `r'Quick Links\s+About Us.*?Contact[^\n]*'` | Remove completely |
| Timestamps & Durations | `r'\b(?:Friday\|Saturday\|Sunday\|Monday\|Tuesday\|Wednesday\|Thursday),\s+\d+\s+[A-Za-z]+\s+\d{4},\s+\d{1,2}:\d{2}\s*(?:AM\|PM)'` | Remove completely |
| Quiz Metrics | `r'\b(?:Marks?\s*=\s*\d+[\.\d]*/\d+[\.\d]*\|Grade\s+\d+[\.\d]*\s+out\s+of\s+\d+[\.\d]*\|State\s+Finished)\b'` | Remove completely |
| Question Metadata | `r'\b(?:Mark\s+\d+[\.\d]*\s+out\s+of\s+\d+[\.\d]*\|Flag question)\b[^\n]*'` | Remove completely |

### B. Mobile Screenshot Artifacts
Students capturing quizzes on mobile devices introduce status bar icons and times.

| Artifact | Regex / Pattern | Action |
|---|---|---|
| Phone Timestamps & Icons | `r'\b\d{1,2}:\d{2}\s*(?:AM\|PM)?\s*(?:[®©@\-\*\–\—\•\·\>\<\»\«\:]\|g\s+tl\|tl\|\«at\!\|\bCD\:\|\b4G\b\|\bLTE\b\|\bwifi\b)*'` | Remove completely |
| LMS Button Artifacts | `r'\b(?:Clear my choice\|Finish attempt)\b[^\n]*'` | Remove completely |

### C. Inline Quiz Options (`Select one:`)
When quiz stems contain inline options:
```text
Which of the following is correct? Select one: a. Option A b. Option B c. Option C d. Option D
```
1. Detect `m_sel = re.search(r'(.*?)\s*Select one:\s*(.*)', raw_stem, re.S|re.I)`.
2. Extract the stem before `Select one:`.
3. Parse options using `re.finditer(r'(?:^|\s+)([a-fA-F])[\.\)]\s*(.*?)(?=(?:\s+[a-fA-F][\.\)]|\Z))', rest, re.S)`.
4. Output structured `- **A)**`, `- **B)**` markdown options.
5. If unparseable, strip `\bSelect\s+one:?.*` to keep the stem clean.

### D. Trailing Answer Key Tables
Department books frequently print answer key grids at the end of chapters, which PyMuPDF/OCR appends to the last question's option:
```text
- **D)** Splenic CARDIOVASCULAR SYSTEM 1 2 3 4 5 6 7 8 9 10 D A D A D A D C C A ...
```
* **Regex**:
  ```python
  re.sub(r'(?i)\s*(?:Answers?\s+of\s+|Answer\s+of\s+|Skeletal\s+system|MUSCULAR\s+SYSTEM|CARDIOVASCULAR\s+SYSTEM|Respiratory\s+system|Digestive\s+system|Urinary\s+system|Reproductive\s+system|Lymphatic\s+system|Nervous\s+system|Introduction\s*&\s*skin|MICROSCOPIC\s+ANSWER|Cytology|Nucleus|Cell\s+cycle|Stem\s+cells|BLOOD|CONNECTIVE\s+TISSUE|BONE)\s+(?:[0-9]\s+[0-9]|[A-E]\s+[A-E]).*', '', otext)
  ```

### E. Matching Table Headers & Corrupted Fragments
* Strip trailing `TABLE \d+ A B` headers from options.
* Discard broken matching fragments (single-word stems like `Peroxisomes` with only orphan options `E`/`F`).

### F. Bubble Marks & Radio Button Symbols
* Regex: `r'[@©®]{2,}|\b[A-E]\s*[\)\]\.]\s*[@©®]'`
* Strip leading symbols: `re.sub(r'^[@©®\s\.\,\-\)]+', '', otext)`

### G. Decoupling Preceding Explanations
In Moodle quiz reviews, the previous question's answer is often printed right above the next question number.
* When processing Question $N$, verify if its raw stem begins with Question $N-1$'s explanation/answer:
  ```python
  if prev_exp and len(prev_exp) > 3:
      while raw_stem.lower().startswith(prev_exp.lower()):
          raw_stem = raw_stem[len(prev_exp):].strip()
  ```

---

## 3. Option Sequential Integrity (Zero Option Mismatch Guarantee)

To prevent platform rejection (`Correct answer 'A' doesn't match available options (B, C, D)`):
1. **Never allow gapped options**: An MCQ must always start at `A` and proceed sequentially (`A`, `B`, `C`, `D`...).
2. If options start at `B` (e.g. `B, C, D`), repack them:
   * Old `B` $\to$ New `A`
   * Old `C` $\to$ New `B`
   * Old `D` $\to$ New `C`
   * Adjust `Correct` answer letter to match the new key.
3. If `Correct` is missing or not in `opts`: match against the explanation (`EXP`) text.
4. If fewer than 2 valid options remain: convert to `QROC` with `Correct = '-'`.

---

## 4. Medical Notation Fidelity (OCR repair)

OCR flattens the notation that makes a physiology or biochemistry option meaningful. Repair it during Stage 1; the auditor flags what survives.

| OCR output | Correct | Context |
|---|---|---|
| `Ca**`, `Ca2+`, `Ca++` | `Ca²⁺` | ion species |
| `Na*`, `Na+`, `K*`, `Cl-` | `Na⁺`, `K⁺`, `Cl⁻` | ion species |
| `HCO3-`, `H2O`, `CO2`, `O2` | `HCO₃⁻`, `H₂O`, `CO₂`, `O₂` | formulas |
| `B1`, `B2`, `a1`, `a2` in receptor names | `β1`, `β2`, `α1`, `α2` | adrenergic receptors |
| `um`, `uL`, `ug` | `µm`, `µL`, `µg` | units |
| `->`, `=>`, `_` between states | `→` | physiological arrows |
| `1` / `l` / `I` and `0` / `O` swapped inside option letters | the real letter | option lettering |

Detection regex used by the auditor: `(?:Ca|Na|K|Cl|Mg|HCO3|H)\s*\*{1,2}(?!\w)`.

Never "fix" notation by deleting it — `Voltage-gated Ca** channels` becomes `Voltage-gated Ca²⁺ channels`, not `Voltage-gated channels`, which changes the meaning of the option.

---

## 5. What noise removal must NOT touch

- Numbered lists inside a `QROC` model answer (`1. … 2. …`) are content, not leading numbering. Strip leading numbering only from the **start of a stem**.
- Fill-in-the-blank stems legitimately end in `...` or `....` — do not treat them as truncation.
- Clinical vignettes contain times and numbers (`a 65-year-old at 3:00 AM`); the phone-clock regex must be anchored to status-bar context, not applied to stems blindly.
- Option text that is genuinely one token (`Aorta`) is fine; the "option under 2 chars" check targets `A`, `-`, `.` leftovers.
