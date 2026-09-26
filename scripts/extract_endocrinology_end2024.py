#!/usr/bin/env python3
"""Curate the marked 2024 Endocrinology summative scan."""

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
        ("For a patient with diabetes and BP 170/110, which target statement is not accurate?", ["HbA1c <7%", "Fasting plasma glucose <130 mg/dL", "Postprandial glucose <180 mg/dL", "BP <150/100 mmHg", "HDL >40 mg/dL"], "D"),
        ("Which is not a goal of treatment for Mr Ali?", ["Improve symptoms", "Avoid hypoglycemia", "Increase body weight", "Prevent diabetic complications", "Improve insulin sensitivity"], "C"),
        ("Which statement describes gestational diabetes correctly?", ["It may start in the first trimester", "It does not require treatment", "It induces fetal macrosomia", "It never recurs in subsequent pregnancies", "The patient is not at risk of type 2 diabetes later"], "C"),
        ("Screening of congenital adrenal hyperplasia is usually by measuring", ["17-hydroxyprogesterone", "Aldosterone", "Renin", "Metanephrine", "Epinephrine"], "A"),
        ("The most hopeful etiology of delayed puberty is", ["Turner syndrome", "Klinefelter syndrome", "Constitutional delay", "Severe systemic disease", "Gonadal irradiation in childhood"], "C"),
        ("In secondary hyperaldosteronism, which is false?", ["It may or may not be associated with hypertension", "Renin is not elevated", "Hypokalemia is manifest", "Decompensated liver cirrhosis is a cause", "Salt restriction is essential in treatment"], "B"),
        ("The following is not characteristic of primary hyperaldosteronism", ["It is an important cause of secondary hypertension", "Headache and fatigue may occur", "A high aldosterone/renin ratio", "Hyperkalemia is found", "Hypertension without hypokalemia"], "D"),
        ("Pseudohyperaldosteronism is not characterized by", ["Hypertension without hypokalemia", "A mineralocorticoid other than aldosterone", "Excessive licorice ingestion", "Renin is not elevated", "Aldosterone is not elevated"], "A"),
        ("In boys, delayed puberty is lack of testicular enlargement at the age of", ["12 years", "13 years", "14 years", "15 years", "16 years"], "C"),
        ("In treatment of hypothyroidism, which is false?", ["Levothyroxine is usually used", "Start with a high dose then gradually down-titrate", "For proper absorption take it on an empty stomach", "Do not take it simultaneously with calcium or iron"], "B"),
        ("Gynecomastia is caused by", ["Elevated serum testosterone", "Elevated prolactin", "Reduced free testosterone/estrogen ratio", "Reduced progesterone"], "C"),
        ("Hypogonadotropic secondary hypogonadism includes all the following except", ["Sheehan syndrome", "Kallmann syndrome", "Growth-hormone deficiency", "Hyperprolactinemia", "Acromegaly"], "C"),
        ("Which statement is false in pituitary adenoma?", ["All adenomas secrete hormones", "Acromegaly is usually a macroadenoma", "Prolactinoma is the most prevalent secretory adenoma", "Medical treatment is effective in most prolactinomas", "Surgery is the treatment of choice for acromegaly"], "A"),
        ("Which class of drugs does not cause hyperprolactinemia?", ["Prokinetic drugs", "Antipsychotics", "Antidepressants", "Proton-pump inhibitors", "Pioglitazone"], "E"),
        ("Which suppresses ADH release?", ["Rise in plasma volume", "Low plasma osmolality", "Stress", "Sleep"], "B"),
        ("Which is a potential complication of Cushing syndrome?", ["Osteoporosis", "Hypoglycemia", "Hypothyroidism", "Low blood pressure", "Anemia"], "A"),
        ("The primary cause of Addison disease is", ["Autoimmune destruction of the adrenal glands", "Iatrogenic disease", "Pituitary dysfunction", "Genetic mutation", "Adrenal tumor"], "A"),
        ("The following is not an adrenal cause of hypertension", ["Conn syndrome", "Pheochromocytoma", "Congenital adrenal hyperplasia", "Cushing syndrome", "Addison disease"], "E"),
        ("Which is false about parathyroid hormone actions?", ["Stimulates bone resorption", "Inhibits bone resorption", "Increases phosphate excretion by kidneys", "Stimulates calcitriol synthesis in kidneys"], "B"),
        ("The secretion of ACTH is correctly described by", ["It shows a circadian rhythm", "It decreases during stress", "It is inhibited by aldosterone", "It is stimulated by glucocorticoids", "It is stimulated by epinephrine"], "A"),
        ("Postoperative complications of pituitary adenoma include", ["CSF leak", "Diabetes insipidus", "Apoplexy", "All of the above"], "D"),
        ("Regarding basal insulin therapy, which statement is wrong?", ["It consists of long-acting insulin preparations", "It lowers fasting plasma glucose", "It suppresses hepatic glucose production", "It lowers postprandial plasma glucose"], "D"),
        ("Type 1 diabetes mellitus is characterized by all the following except", ["Most cases present acutely", "Obesity is an important predisposing factor", "Insulin therapy is always needed", "Positive family history is less common than in type 2", "Islet-cell antibodies are present in the majority"], "B"),
        ("Hypoglycemic symptoms include all the following except", ["Pallor", "Irritability and bad behavior", "Dizziness", "Tiredness", "Dry skin"], "E"),
        ("All the following are correct about diet in type 1 diabetes except", ["A 6-year-old child needs around 1000 kcal daily", "Meal and snack timing and calories should be fixed", "50–55% of calories should be carbohydrate", "High-fiber food is encouraged", "Complex carbohydrates are preferable to simple sugars"], "A"),
        ("All the following are early manifestations of congenital hypothyroidism except", ["Feeding difficulties", "Large protruding tongue", "Large anterior fontanelle", "Excessive sleepiness", "Prolonged neonatal jaundice"], "B"),
        ("After thyroidectomy, progressive swelling and stridor despite successful intubation require", ["Fiberoptic laryngoscopy", "Intravenous calcium", "Broad-spectrum antibiotics", "Wound exploration", "High-dose steroids and antihistamines"], "D"),
        ("The best preoperative approach to a pheochromocytoma patient is", ["Fluid restriction", "An alpha blocker 24 hours before surgery", "An alpha blocker for 1–3 weeks before surgery", "A beta blocker before alpha blockade", "Beta blockade followed by alpha blockade for one week"], "C"),
        ("The most appropriate next step in thyroid storm is", ["Emergent subtotal thyroidectomy", "Emergent total thyroidectomy", "Emergent hemodialysis", "Fluids, antithyroid drugs, beta blockers, iodine and steroids", "Emergent radiation therapy"], "D"),
        ("The most common cause of primary hyperparathyroidism is", ["A single parathyroid adenoma", "Multiple parathyroid adenomas", "Parathyroid hyperplasia", "Parathyroid carcinoma"], "A"),
    ]
    questions = [{"stem": stem, "options": {"ABCDE"[i]: value for i, value in enumerate(options)}, "correct": correct} for stem, options, correct in data]
    module.write_mcq(
        ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/01_End_2024.md",
        "Endocrinology End Exam 2024",
        questions,
        "30 MCQs recovered from the marked five-page scan; answers were read from the marked circles and source annotations.",
        "marked",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
