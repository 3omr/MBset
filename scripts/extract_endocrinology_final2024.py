#!/usr/bin/env python3
"""Curate the scanned Endocrinology final 2024 MCQ source."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("endo_remaining", ROOT / "scripts/extract_endocrinology_remaining.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main() -> int:
    data = [
        ("Which statement is wrong regarding physiological basal insulin?", ["It has anabolic actions", "It continues for 24 hours", "It continues during fasting", "It has no peak of elevation"], "D"),
        ("Which is unusual in metabolic syndrome?", ["Diabetes", "Atherosclerosis", "Fatty liver", "PCOS", "Hypotension"], "E"),
        ("Which statement is false regarding diffuse goiter?", ["It means enlargement of the whole thyroid with a smooth surface", "It may be hyperthyroid, hypothyroid or euthyroid", "It cannot be caused by thyroiditis", "It does not indicate malignancy"], "C"),
        ("Myxedema coma is characterized by", ["Hyperglycemia", "Hyperventilation", "Hypothermia", "Sweating", "Agitation and tremors"], "C"),
        ("Screening of diabetic nephropathy is usually by", ["Urinary albumin/creatinine ratio", "Serum albumin/creatinine", "Serum creatinine", "Blood urea", "Routine urinalysis"], "A"),
        ("The most essential measure for prevention of diabetic microvascular complications is", ["Good glycemic control", "Weight reduction", "Exercise", "Increasing HDL", "Antioxidants"], "A"),
        ("Which is a potential complication of Cushing syndrome?", ["Osteoporosis", "Hypoglycemia", "Hypothyroidism", "Low blood pressure", "Anemia"], "A"),
        ("In diabetic patients, hypoglycemia is least likely to occur in", ["The elderly", "Childhood", "Associated hyperthyroidism", "Associated hypopituitarism", "Associated hypoadrenalism"], "C"),
        ("The primary cause of Addison disease is", ["Autoimmune adrenal destruction", "Iatrogenic disease", "Pituitary dysfunction", "Genetic mutation", "Adrenal tumor"], "A"),
        ("Which can precipitate diabetic ketoacidosis?", ["Infection", "Surgery", "Neglecting insulin doses", "All of the above", "None of the above"], "D"),
        ("Which suggests type 1 rather than type 2 diabetes?", ["Central obesity", "Maternal family history of diabetes", "Recurrent diabetic ketoacidosis", "Hypertension", "Dyslipidemia"], "C"),
        ("The first symptom or sign of puberty in a boy is", ["Testicular enlargement", "Penile enlargement", "Linear growth", "Ability to ejaculate"], "A"),
        ("To screen for long-standing Sheehan syndrome, simply measure", ["FSH", "TSH", "ACTH", "Growth hormone", "Prolactin"], "E"),
        ("Which is not correct regarding thyroiditis?", ["It may occur as a side effect of amiodarone or interferon", "Hashimoto thyroiditis is the commonest cause of hypothyroidism", "Hashimoto thyroiditis may have an initial toxic phase", "Goiter is diffuse when present", "High radioiodine uptake is characteristic"], "E"),
        ("A patient with hypercalcemia and osteitis fibrosa cystica most likely has", ["Sarcoidosis", "Vitamin D intoxication", "Paget disease", "Metastatic carcinoma", "Primary hyperparathyroidism"], "E"),
        ("A 2-cm cold thyroid nodule with follicular cells on FNA is initially treated with", ["External-beam radiation", "Multidrug chemotherapy", "TSH suppression", "Prophylactic neck dissection with total thyroidectomy", "Thyroid lobectomy"], "E"),
        ("Which adrenal mass could be observed after a complete metabolic work-up?", ["A nonfunctioning 3-cm solid mass", "A nonfunctioning 7-cm cystic mass", "A functioning 2-cm cystic mass", "A nonfunctioning solid mass that doubled in one year", "A 10-cm solid mass"], "A"),
        ("In management of diabetic ketoacidosis, all are correct except", ["The starting fluid is saline", "Regular insulin is given at 0.1 U/kg/hour", "Potassium chloride is added after 12–24 hours", "Glucose fall should not exceed 100 mg/dL/hour", "A nasogastric tube is used in coma"], "C"),
        ("The most likely cause of insulin-dependent type 1 diabetes is", ["Chromosomal imbalance", "An enzyme defect preventing insulin action", "Autoimmune beta-cell destruction", "A high-carbohydrate diet", "Chronic emotional stress"], "C"),
        ("A full-term newborn has low T4 and high TSH shortly after birth. The diagnosis is", ["Congenital hyperthyroidism", "Congenital hypothyroidism", "Transient hypothyroidism", "Secondary hypothyroidism due to hypopituitarism", "None of the above"], "B"),
        ("Regarding hypogonadism, which is false?", ["The clinical picture differs with age of occurrence", "Primary hypogonadism has a worse prognosis than secondary", "It can be caused by pituitary disorders", "It does not occur with liver-cell failure", "Anosmia with hypogonadism is Kallmann syndrome"], "D"),
        ("Which antidiabetic class has cardiovascular protective benefit?", ["SGLT2 inhibitors", "Sulfonylureas", "DPP-4 inhibitors", "Insulin", "Metformin"], "A"),
        ("Which is false regarding prolactinoma?", ["It presents with galactorrhea-amenorrhea syndrome", "It may be a micro- or macroadenoma", "It often responds well to medical treatment", "Drug-related hyperprolactinemia may present similarly", "Pressure symptoms are always absent"], "E"),
        ("In addition to water reabsorption, ADH enhances reabsorption of", ["Urea", "Glucose", "Carbon dioxide", "Sodium", "Phosphate"], "A"),
    ]
    questions = [{"stem": stem, "options": {"ABCDE"[i]: value for i, value in enumerate(options)}, "correct": correct} for stem, options, correct in data]
    module.write_mcq(
        ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/31_Endocrine_Final_2024.md",
        "Endocrinology Final 2024",
        questions,
        "24 recoverable MCQs reconstructed from the OCR scan; marked choices were preserved where legible and remaining choices were derived from the source wording.",
        "marked",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
