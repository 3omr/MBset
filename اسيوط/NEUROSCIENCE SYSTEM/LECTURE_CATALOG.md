# NEUROSCIENCE SYSTEM — Assiut lecture catalog

## Official source of truth

The platform export is `subcategories_NEUROSCIENCE_SYSTEM_2026-09-16.xlsx`, sheet `Subcategories`. It contains 61 unique, non-empty `subcategoryId` values. The upload output is one PDF per official ID in `Lectures/<subcategoryId>.pdf`.

## Raw lecture inventory

| Source | Pages | Status |
|---|---:|---|
| `Lectures_raw/Lectures/1st week handout .pdf` | 90 | EXCLUDED — wrong module; the pages are an Endocrine System handout |
| `Lectures_raw/Lectures/Handout Week1.pdf` | 104 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/2nd Handout.pdf` | 97 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/3rd waak Handout.pdf` | 101 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/Lectures 31-40 (1).pdf` | 104 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/Lectures 41-50 (1).pdf` | 114 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/Lectures 51-60.pdf` | 99 | Included; mapped to official subcategories |
| `Lectures_raw/Lectures/Lectures 61-70.pdf` | 113 | Included; mapped to official subcategories |

The explicit page map is maintained in `scratch/neuroscience_triage/lecture_map_01_30.json` and `scratch/neuroscience_triage/lecture_map_31_70.json`. The builder is `scripts/prepare_lectures.py`; it refuses to write when an official subcategory is unmapped, a range is invalid, or ranges overlap.

## Build verification

- Official subcategories: 61
- Output PDFs: 61
- Missing official IDs: 0
- Unexpected output IDs: 0
- Output pages: 728
- Empty output PDFs: 0
- Intentional blank-page removal: `3rd waak Handout.pdf` page 32, a page-number divider before the Cerebrum section
- Intentional merges: spinal cord I/II, synapses 7/8, cranial nerves 11/12, pain I/II, stretch reflex parts, sensory/motor cortex parts, limbic I/II, and hearing I/II
- Corrected source-label continuations: `Lectures 31-40` page 38 remains with Cerebrovascular Diseases; `Lectures 51-60` pages 60–65 remain with Brain tumors
