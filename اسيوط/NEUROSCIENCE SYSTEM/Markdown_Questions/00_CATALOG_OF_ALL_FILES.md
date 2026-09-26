# NEUROSCIENCE SYSTEM (Assiut) — catalog of all question sources

Stage 0 inventory created from `CNSQuestions.zip` on 2026-09-16. The archive
containers are preserved in the module root; every contained source is listed
below. Extraction is in progress; each completed row records its measured
question count and answer provenance.

The official platform export is
`subcategories_NEUROSCIENCE_SYSTEM_2026-09-16.xlsx` and contains 61
subcategories under `AssiutUniv_NEUROSCIENCE_SYSTEM`.

| # | Source file | Type | Pages | Target Markdown | Total | MCQ | Written | Answer sources | Answer distribution | Bias gate | Tag | tagSuggere | Year | Status | Note |
| --- | --- | --- | ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `CNS/ASSIUT’S PREVIOUS EXAMS/2023 Summer CNS B.pdf` | PDF | 7 | `01_2023_Summer_CNS_B.md` | 8 | 0 | 8 | key:8 | n/a | n/a | Exams, Final 2023 | None | 2023 | extracted | model-answer paper; top-level exam numbering retained and each QROC includes all subparts |
| 2 | `CNS/ASSIUT’S PREVIOUS EXAMS/All CNS midterm and final exams Assuit.pdf` | PDF | 136 | `02_All_CNS_midterm_final_Assuit.md` | 401 | 218 | 183 | derived:262, key:139 | A:37, B:52, C:47, D:35, E:47 | 24% / PASS | Exams, Midterm/Final (per section) | discipline per section | per section | extracted | pages 2–11, 12–18, 19–63, 64–73, 98–116, and 117–125 reconciled; pages 74–97 and 126–136 are explicit duplicate copies; five unreadable MCQ fragments excluded and documented |
| 3 | `CNS/ASSIUT’S PREVIOUS EXAMS/CNS FINAL 2024.pdf` | PDF | 9 | `03_CNS_Final_2024_Model.md` | 9 | 0 | 9 | key:9 | n/a | n/a | Exams, Final 2024 | None | 2024 | extracted | model-answer paper; nine top-level QROCs with complete subpart answers |
| 4 | `CNS/ASSIUT’S PREVIOUS EXAMS/Final 2024.jpg` | JPG | n/a | `04_Final_2024_page1.md` | 4 | 4 | 0 | marked:4 | A:0, B:3, C:1 | 75% / INVESTIGATE (four-item page) | Exams, Final 2024 | None | 2024 | extracted | page image; Q4 option E restored from the paired page-2 image |
| 5 | `CNS/ASSIUT’S PREVIOUS EXAMS/Mid exam 2020.pdf` | PDF | 11 | `05_Mid_exam_2020.md` | 68 | 68 | 0 | derived:68 | A:8, B:17, C:13, D:14, E:16 | 25% / PASS | Exams, Midterm 2020 | None | 2020 | extracted | cover declares 75 MCQs, but supplied scan visibly contains Q1–Q48 and Q56–Q75 only; missing Q49–Q55 documented and not invented |
| 6 | `CNS/ASSIUT’S PREVIOUS EXAMS/final 2022.pdf` | PDF | 18 | `06_Final_2022.md` | 131 | 87 | 44 | derived:131 | A:17, B:15, C:21, D:15, E:19 | 24% / PASS | Exams, Final 2022 | discipline per section | 2022 | extracted | 8 essay prompts split into 44 QROC records with full derived model answers; 87 MCQs, no legible printed key; Q72/Q73/Q86 wording defects documented |
| 7 | `CNS/ASSIUT’S PREVIOUS EXAMS/final 2024(1).jpg` | JPG | n/a | `07_Final_2024_page2.md` | 7 | 6 | 1 | marked:6, derived:1 | A:1, B:2, D:3 (one unresolved written defect) | 50% / INVESTIGATE (six-item page) | Exams, Final 2024 | None | 2024 | extracted | page image; Q11 is cut off after option C and converted to QROC with explicit defect note |
| 8 | `CNS/ASSIUT’S PREVIOUS EXAMS/final CNS summer 2024.pdf` | PDF | 9 | `08_Final_CNS_summer_2024.md` | 57 | 0 | 57 | key:57 | n/a | n/a | Exams, Final 2024 | discipline per section | 2024 | extracted | first page is a phone status-bar capture; printed model-answer subparts on pages 2–9 retained as individual QROC records |
| 9 | `CNS/All CNS quizzes.pdf` | PDF | 285 | `09_All_CNS_quizzes.md` | 621 | 621 | 0 | key:616, derived:5 | A:136, B:119, C:126, D:112, E:128 | 22% / PASS (per-week gate also passed) | Department, Quizzes, Week 1–7 (per section) | None | None | extracted | five source answer lines name multiple/duplicate correct options; normalized as derived and retained for review |
| 10 | `CNS/CNS Gds.pdf` | PDF | 116 | `10_CNS_Gds.md` | 310 | 66 | 244 | derived:310 | A:23, B:11, C:16, D:12, E:3, F:1 | 35% / PASS | Department, GDs, Subject GD N (per section) | discipline per item | None | extracted | sections GD2–GD7 mapped to source pages 3–116; 224 QROC model answers completed and eight figure crops linked under `Images/` |
| 11 | `CNS/CNS definitions.pdf` | PDF | 7 | `11_CNS_definitions.md` | 104 | 0 | 104 | key:104 | n/a | n/a | Department, QBank, General 2024 | None | 2024 | extracted | coordinate-aware two-column table |
| 12 | `CNS/Department Qs.pdf` | PDF | 19 | `12_Department_Qs.md` | 23 | 23 | 0 | key:6, marked:12, derived:5 | per-subject | 30% / PASS | Department, QBank, Subject (per section) | discipline per item | None unless present | extracted | repeated department cards retained; blank/explanatory pages excluded and logged in the Markdown header |
| 13 | `CNS/Farmatives Answered.pdf` | PDF | 60 | `13_Farmatives_Answered.md` | 66 | 65 | 1 | key:29, marked:3, derived:34 | A:14, B:15, C:12, D:12, E:12 | 23% / PASS | Department, Formative, Week 1–7 (per item) | discipline per item | None | extracted | one two-answer marked item converted to QROC with a full model answer; no Arabic after cleaning |
| 14 | `CNS/Mid Formatives.pdf` | PDF | 15 | `14_Mid_Formatives.md` | 40 | 40 | 0 | derived:40 | A:8, B:9, C:10, D:8, E:5 | 25% / PASS | Department, Formative, Week 1 | None | None | extracted | four ten-question attempts; no embedded key, answers derived and spot-checked; Moodle/comment noise removed |
| 15 | `CNS/Mid GDs Answered.pdf` | PDF | 247 | `15_Mid_GDs_Answered.md` | 192 | 49 | 143 | key:157, marked:11, derived:24 | A:12, B:10, C:15, D:9, E:2, F:1 | 31% / PASS | Department, GDs, Subject GD N (per section) | discipline per item | None | extracted | missing keys are documented in the Markdown header; four figure-dependent items now link to local crops under `Images/` |
| 16 | `CNS/Mid quizzes.pdf` | PDF | 202 | `16_Mid_quizzes.md` | 368 | 368 | 0 | key:364, derived:4 | A:74, B:65, C:72, D:90, E:67 | 24% / PASS | Department, Quizzes, Week 1–4 (per section) | None | None | extracted | text layer plus page-by-page OCR; four blank/ambiguous source keys normalized as derived; five source blocks retain printed option defects |
| 17 | `CNS/OTHER EXAMS/FINAL - 30 - CNS - M3WAN - ext.pdf` | PDF | 24 | `17_M3WAN_Final_30.md` | 150 | 150 | 0 | key:149, derived:1 | A:28, B:45, C:34, D:33, E:10 | 30% / PASS | External, M3WAN | None | None | extracted | Q27 printed key says ALL; derived D retained for review |
| 18 | `CNS/OTHER EXAMS/FINAL - CNS - 32 - M3WAN.pdf` | PDF | 13 | `18_M3WAN_Final_32.md` | 75 | 75 | 0 | key:75 | A:24, B:26, C:19, D:6 | 35% / PASS | External, M3WAN | None | None | extracted | M3WAN form number 32 retained as source identity, not Year |
| 19 | `CNS/OTHER EXAMS/MID & FINAL 31 - CNS - M3WAN .pdf` | PDF | 17 | `19_M3WAN_Mid_Final_31.md` | 100 | 100 | 0 | key:100 | A:19, B:22, C:35, D:20, E:4 | 35% / PASS | External, M3WAN | None | None | extracted | M3WAN form number 31 retained as source identity, not Year |
| 20 | `CNS/OTHER EXAMS/MID 30 - CNS - M3WAN.pdf` | PDF | 13 | `20_M3WAN_Mid_30.md` | 75 | 75 | 0 | key:66, derived:9 | A:15, B:22, C:14, D:19, E:5 | 29% / PASS | External, M3WAN | None | None | extracted | nine source-grid blanks/ambiguous cells were explicitly marked derived; final spot-check required |
| 21 | `CNS/OTHER EXAMS/mid 32 CNS - M3WAN.pdf` | PDF | 9 | `21_M3WAN_Mid_32.md` | 37 | 37 | 0 | key:37 | A:18, B:8, C:6, D:5 | 49% / INVESTIGATE | External, M3WAN | None | None | extracted | A-heavy distribution requires spot-check; M3WAN form number 32 is not Year |
| 22 | `CNS/OTHER EXAMS/midterm 2020.pdf` | PDF | 8 | `22_Midterm_2020.md` | 75 | 74 | 1 | derived:75 | A:15, B:21, C:16, D:21, E:1 (one unresolved written defect) | 28% / PASS | External, Midterm 2020 | None | 2020 | extracted | one defective EXCEPT item converted to QROC because all four legible options were true; no printed key was legible |
| 23 | `CNS/Qs bank MCQ (CNS-Metabolism-Endocrine).pdf` | PDF | 21 | `23_Qs_bank_CNS_Guyton.md` | 89 | 89 | 0 | key:89 | A:24, B:19, C:20, D:23, E:3 | 27% / PASS | External, Guyton 2016 | None | 2016 | extracted | CNS Q1–Q89 extracted; Metabolism/Endocrine key tables had no corresponding question pages and were explicitly excluded |
| 24 | `CNS/Qs bank(1).pdf` | PDF | 13 | `24_Qs_bank_1.md` | 56 | 56 | 0 | derived:56 | A:17, B:10, C:16, D:13 | 30% / PASS | Department, QBank, Physiology | Physiology | None | extracted | CNS Physiology Part I scan; no dependable answer-key page |
| 25 | `CNS/Qs bank.pdf` | PDF | 30 | `25_Qs_bank_2.md` | 48 | 48 | 0 | derived:48 | A:20, B:9, C:10, D:9 | 42% / PASS | Department, QBank, Physiology | Physiology | None | extracted | CNS Physiology Part II scan; no dependable answer-key page |
| 26 | `CNS/department Q.pdf` | PDF | 43 | `26_department_Q.md` | 66 | 51 | 15 | key:15, marked:16, derived:35 | A:6, B:16, C:13, D:13, E:3 | 31% / PASS | Department, QBank, Subject (per section) | discipline per item | None | extracted | mixed spinal-cord, stretch-reflex, parasitology, microbiology, and basal-ganglia cards; incomplete basal-ganglia options converted to QROC with defects documented |
| 27 | `CNS/pharma Qs bank.pdf` | PDF | 25 | `27_Pharmacology_Qs_bank.md` | 138 | 91 | 47 | marked:91, key:47 | A:21, B:24, C:21, D:25 | 27% / PASS | Department, QBank, Pharmacology | Pharmacology | None | extracted | two MCQ sections; second written section omits item 14 |
| 28 | `CNS/physiology Qs bank MCQ.pdf` | PDF | 15 | `28_Physiology_Qs_bank_MCQ.md` | 87 | 87 | 0 | marked:40, derived:47 | A:14, B:28, C:23, D:22 | 32% / PASS | Department, QBank, Physiology | Physiology | None | extracted | option-label anomalies repacked; derived answers require final spot-check |

## Source reconciliation

| Inventory | Count |
| --- | ---: |
| Question sources in expanded archive | 28 |
| PDF question sources | 26 |
| JPG question sources | 2 |
| Lecture PDFs in expanded archive | 8 |
| Official subcategories | 61 |
| Markdown question files completed | 28 |

## Final question-bank build

| Measure | Result |
| --- | ---: |
| Markdown input records | 3405 |
| Normalized duplicate records removed | 344 |
| Final Excel rows | 3061 |
| Final QCS / QROC | 2294 / 767 |
| Answer provenance | key:1959, derived:944, marked:158 |
| Excel schema validation | PASS — 31/31 canonical columns, 0 errors |
| Excel forensic audit | PASS — no hard findings |

The Excel audit retains three non-blocking warnings: 2230 rows have no Year
because their source has no year, 13 duplicate option-text cases remain as
source variants, and 3 very short option values remain for review. Twelve
reviewed answer-conflict records are documented in `CONFLICT_REVIEW.md`.
