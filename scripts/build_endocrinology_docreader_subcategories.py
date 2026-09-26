#!/usr/bin/env python3
"""Build the fresh Endocrinology subcategories sheet from DocReader's layout.

This is a Phase 1 upload sheet: categoryId and subcategoryId stay empty so the
platform can assign official IDs after upload.  The four subject groups and
the 46 lecture names are transcribed from DocReader module 176.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "أزهر دمياط/Endocrinology/subcategories_Endocrinology_2026-09-18.xlsx"

HEADERS = [
    "categoryId", "categoryName", "subcategoryId", "name", "tag", "type",
    "pdf", "studyRecommendations", "pdfVersion", "pdfDate", "pdfNote",
    "questionsCount", "orderIndex",
]


GROUPS: list[tuple[str, list[str]]] = [
    (
        "Internal Medicine",
        [
            "Introduction to Endocrinology",
            "Hashimoto's Thyroiditis",
            "Hyperthyroidism",
            "Hypothyroidism",
            "Hyperparathyroidism",
            "Hypoparathyroidism",
            "Bone mineral disorders",
            "Adrenal Hypersecretion",
            "Endocrine hypertension",
            "Cushing's Syndrome",
            "Adrenal Hypofunction",
            "Polyglandular Autoimmune Endocrinopathies",
            "Prolactinoma & Galactorrhea, Non-Functioning Adenomas and Pituitary Apoplexy",
            "Acromegaly",
            "Panhypopituitarism",
            "Approach to a case of short stature",
            "Obesity, Metabolic Syndrome & Nutritional assessment",
            "Disorders of Puberty (delayed and precocious)",
            "Posterior pituitary disorders (Diabetes Insipidus, SIADH)",
            "Hirsutism (CAH, PCOS)",
            "Male hypogonadism & Gynecomastia",
            "Carcinoid, MEN syndromes, Insulinoma",
            "Introduction to Diabetes, Glucose homeostasis",
            "Different Types of DM",
            "Type 1 Diabetes Mellitus",
            "Macrovascular diabetic Complications",
            "Type 2 Diabetes Mellitus",
            "Microvascular diabetic Complications",
            "Dysglycemic Emergencies",
            "Bunnies of Diabetes Education",
            "Dyslipidemia",
        ],
    ),
    (
        "Surgery",
        [
            "Approach to a case of goiter",
            "Non-neoplastic thyroid disease",
            "Applied anatomy of Thyroid & Parathyroid Glands: Surgical Management of Thyroid & Parathyroid Disorders",
            "Adrenal Tumors: Surgical Approach",
            "Applied Anatomy of the Pituitary & Hypothalamus: Pituitary Tumors Surgical Management",
        ],
    ),
    (
        "Pediatric",
        [
            "Congenital hypothyroidism (cretinism)",
            "Disorders of sex differentiation",
            "Growth Hormone disorders in Pediatrics",
            "Diabetes in Pediatrics & Diabetic ketoacidosis",
        ],
    ),
    (
        "Integrated Sessions",
        [
            "Bio: Calcium homeostasis",
            "Clinical Pathology: Laboratory Diagnosis of Diabetes & Endocrine Diseases",
            "Pharma: Diabetes Pharmacotherapy",
            "Radiology: Structural & Functional Imaging of Endocrine Gland",
        ],
    ),
]


def build() -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Subcategories"
    sheet.append(HEADERS)

    order = 10
    for tag, names in GROUPS:
        for name in names:
            # Phase 1: leave both IDs empty for platform assignment.
            sheet.append([
                None, "Endocrinology", None, name, tag,
                None, None, None, None, None, None, 0, order,
            ])
            order += 10

    header_fill = PatternFill("solid", fgColor="0F6B78")
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    widths = {
        "A": 18, "B": 20, "C": 18, "D": 78, "E": 22, "F": 12,
        "G": 12, "H": 24, "I": 14, "J": 14, "K": 24, "L": 16, "M": 12,
    }
    for column, width in widths.items():
        sheet.column_dimensions[column].width = width
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=cell.column == 4)
    sheet.row_dimensions[1].height = 24
    OUT.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(OUT)
    print(f"Wrote {OUT}")
    print(f"lectures={sheet.max_row - 1} groups={len(GROUPS)}")


if __name__ == "__main__":
    build()
