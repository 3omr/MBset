#!/usr/bin/env python3
"""Curate the scanned Endocrine summative 2025 exam.

The source has no reliable answer strip in the OCR layer.  The options are
recovered from the scan and the answers are explicitly marked ``derived`` so
they remain visible in the provenance audit.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("endo_remaining", ROOT / "scripts/extract_endocrinology_remaining.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main() -> int:
    questions = [
        ("In girls, precocious puberty is defined as the appearance of pubertal signs before the age of", ["8 years", "9 years", "10 years", "11 years", "12 years"], "A"),
        ("Which statement is false in pituitary adenoma?", ["All adenomas secrete hormones", "Acromegaly is usually caused by a macroadenoma", "Prolactinoma is the most prevalent secretory adenoma", "Medical treatment is effective in most cases of prolactinoma", "Surgery is the first choice for acromegaly"], "A"),
        ("The first symptom or sign of puberty in a boy is", ["Testicular enlargement", "Enlargement of the penis", "Growth spurt", "Ability to ejaculate"], "A"),
        ("This class of drugs is not a cause of hyperprolactinemia", ["Prokinetic drugs", "Antipsychotics", "H2 blockers", "Insulin sensitizers", "Antidepressants"], "D"),
        ("Presentations of pituitary disorders are by either", ["Hormonal excess", "Hormone deficiency", "Pressure manifestations", "Any combination of the above", "Any of the above"], "E"),
        ("To screen for early Sheehan syndrome, the simplest measurement is", ["TSH", "FSH", "ACTH", "Basal growth hormone", "Prolactin"], "E"),
        ("Regarding hypogonadism, which is false?", ["The clinical picture differs according to the time of occurrence", "Primary hypogonadism is less hopeful than secondary", "It can be caused by most pituitary disorders", "It cannot be caused by liver cell failure", "When associated with anosmia it is called Kallmann syndrome"], "D"),
        ("Which suggests Addison disease rather than secondary adrenal insufficiency?", ["Hyperpigmentation", "Fatigue", "Normal electrolytes", "Postural hypotension", "Headache"], "A"),
        ("Which is not characteristic of thyrotoxic crisis?", ["Heart failure", "Dehydration", "Temperature below 38 C", "Irritability", "Arrhythmia"], "C"),
        ("Subclinical hypothyroidism is diagnosed by", ["High TSH with normal FT4 and FT3", "High TSH with low FT4 and FT3", "High TSH with high FT4 and FT3", "Low TSH with normal FT4 and FT3", "Low TSH with low FT4 and FT3"], "A"),
        ("Which is false regarding subacute viral (de Quervain) thyroiditis?", ["It presents with neck pain", "It has a transient hyperthyroid phase", "Fever, malaise and high ESR may occur", "Radioiodine uptake is low", "It is caused by antithyroid drugs"], "E"),
        ("In treatment of Graves disease, which is false?", ["Medical treatment is preferred over surgery in suitable patients", "Start with antithyroid drugs and beta blockers", "Propranolol is a preferred beta blocker", "Carbimazole is preferred over propylthiouracil in most cases", "Start with low doses of antithyroid drug and increase gradually"], "E"),
        ("Precocious puberty has the hazard of", ["Lack of psychological maturation", "Lack of cognitive maturation", "Insufficient final height", "A serious underlying tumor", "All of the above"], "E"),
        ("The following is not an investigation in delayed puberty of a 15-year-old boy", ["Klinefelter karyotype", "High LH and FSH", "Delayed bone age", "Undescended testes"], "D"),
        ("The most common central cause of a 7-year-old girl with signs of puberty is", ["Hydrocephalus", "Brain tumor", "Idiopathic", "Meningitis", "Turner syndrome"], "C"),
        ("In Addison disease, secretion of which is least affected?", ["Adrenaline", "Cortisol", "Aldosterone", "Androstenedione"], "A"),
        ("Which is not a cause of secondary hypertension?", ["Conn syndrome", "Cushing syndrome", "Pheochromocytoma", "Hypoparathyroidism", "Renal artery stenosis"], "D"),
        ("The most common type of arrhythmia in thyrotoxicosis is", ["Ventricular fibrillation", "Atrial fibrillation", "Heart block", "Sinus bradycardia"], "B"),
        ("The following abnormality is not seen in Addison disease", ["Hyperkalemia", "Increased ACTH", "Hypoglycemia", "Hyponatremia"], "A"),
        ("The triad of hyponatremia, hemodilution and hypertonic urine suggests", ["Diabetes insipidus", "Diabetes mellitus", "SIADH", "Hyperaldosteronism"], "C"),
        ("Regarding secondary hyperaldosteronism, which is false?", ["It may or may not be associated with hypertension", "It is treated with salt restriction and treatment of the cause", "Renin is normal but aldosterone is high", "Hypokalemia is a manifestation"], "C"),
        ("Which is the most common and frequent cause of a low ACTH level?", ["Pituitary adenoma", "Adrenal carcinoma", "Small-cell tumor of the lung", "Adrenal adenoma"], "D"),
        ("A 45-year-old patient has pheochromocytoma. Which statement is true?", ["It is a neuroendocrine tumor of the adrenal cortex", "It is associated with MEN I", "Plasma metanephrines are a highly sensitive investigation", "It is malignant in 90% of cases"], "C"),
        ("A painless midline neck mass in front of the laryngeal cartilage that rises with tongue protrusion is most likely", ["Branchial cyst", "Cystic hygroma", "Thyroglossal cyst", "Sternomastoid tumor"], "C"),
        ("A patient with episodic severe headache, palpitations, sweating and blood pressure of 190/110 most likely has", ["Generalized anxiety disorder", "Pheochromocytoma", "Hyperthyroidism", "Cushing syndrome"], "B"),
        ("High ACTH and cortisol not suppressed by low-dose dexamethasone, but suppressed by high-dose dexamethasone, suggests", ["Adrenal Cushing syndrome", "Ectopic Cushing syndrome", "Pituitary Cushing disease", "No Cushing syndrome"], "C"),
        ("A patient with a detected RET mutation and a family history of medullary thyroid carcinoma should receive", ["Annual thyroid ultrasound only", "Prophylactic total thyroidectomy", "Fine-needle aspiration biopsy", "Chemotherapy to prevent carcinoma"], "B"),
        ("All the following are correct about congenital hypothyroidism except", ["Most cases are due to aplasia", "Treatment beginning at 6 months is unlikely to result in normal mental development", "A delay in screening for a few weeks makes it insensitive", "The thyroxine dose per kilogram decreases with age"], "A"),
        ("All the following are early manifestations of congenital hypothyroidism except", ["Feeding difficulties", "Large protruding tongue", "Large anterior fontanelle", "Excessive sleepiness", "Prolonged neonatal jaundice"], "E"),
    ]
    qs = [{"stem": stem, "options": {"ABCDE"[i]: option for i, option in enumerate(options)}, "correct": correct} for stem, options, correct in questions]
    module.write_mcq(
        ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/26_Endocrine_summative_2025.md",
        "Endocrine summative 2025",
        qs,
        "29 MCQs recovered from the scan; the source jumps from Q27 to Q29, so one declared numbered block is absent. Options were reconstructed from OCR and answers are derived because no reliable answer key was present.",
        "derived",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
