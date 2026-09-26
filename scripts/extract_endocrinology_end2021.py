#!/usr/bin/env python3
"""Curate the marked/derived Endocrinology summative 2021–2022 scan."""

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
        ("Hypoglycemic manifestations do not include", ["Pallor", "Tiredness", "Irritability", "Dry skin", "Dizziness"], "D"),
        ("Which is false regarding congenital hypothyroidism?", ["Aplasia is a common etiology", "Starting treatment at 6 months often ends in mental retardation", "A delay in screening for a few weeks makes the test insensitive", "The thyroxine dose per kilogram decreases with age", "Fever and diarrhea are common symptoms of overdose"], "A"),
        ("Which finding favors secondary adrenal insufficiency rather than Addison disease?", ["Pigmentation", "Fatigue", "Normal electrolytes", "Hypotension", "Gastrointestinal upsets"], "C"),
        ("Which is a major secondary cause of dyslipidemia?", ["Hypertension", "Diabetes mellitus", "Gout", "Familial combined hyperlipidemia", "Apo C2 deficiency"], "B"),
        ("Which statement is not correct regarding prediabetes?", ["HbA1c is 5.7–6.4%", "Insulin resistance is the main pathophysiology", "Treatment with lifestyle modification and metformin is essential", "It is not associated with increased risk of macrovascular complications", "Microvascular complications are unusual"], "D"),
        ("Among the following adrenal disorders, which is not responsible for secondary hypertension?", ["Congenital adrenal hyperplasia", "Pheochromocytoma", "Cushing syndrome", "Conn syndrome", "Addison disease"], "E"),
        ("Which is absent in pituitary apoplexy?", ["Acute loss of vision", "Headache", "Hypertension", "Meningism", "Altered conscious level"], "C"),
        ("Gynecomastia is caused by an increased", ["Prolactin level", "Testosterone level", "Estrogen/testosterone ratio", "LH/FSH ratio", "FSH/LH ratio"], "C"),
        ("The hallmark of type 1 diabetes mellitus is", ["Age at onset below 30 years", "Absence of family history", "Lean body habitus", "Absence of similar condition in the family", "Gradual onset of symptoms"], "C"),
        ("Regarding isolated growth-hormone deficiency, the following is false", ["Mental function is good", "Baby face", "Abdominal obesity", "Disproportionate dwarfism", "Absence of skeletal defects"], "D"),
        ("Hypoglycemia may occur in all the following except", ["Addison disease", "Insulinoma", "Hypopituitarism", "Myxedema coma", "Hyperthyroidism"], "E"),
        ("The confirmatory test for diabetes insipidus is", ["Insulin stimulation test", "ACTH stimulation test", "Dexamethasone suppression test", "Water-deprivation test", "Saline suppression test"], "D"),
        ("Autoimmune polyglandular syndromes do not include", ["Hypopituitarism", "Type 1 diabetes mellitus", "Hypoadrenalism (Addison disease)", "Hypocalcemia", "Autoimmune thyroiditis"], "A"),
        ("The following excludes the diagnosis of MEN type 1", ["Insulinoma", "Hypercalcemia", "Cushing disease", "Acromegaly", "Pheochromocytoma"], "C"),
        ("In Sheehan syndrome, which is false?", ["It is caused by severe peripartum hemorrhage", "It may progress gradually over years", "Adrenal failure occurs early", "Pituitary and target hormones are essential for confirmation", "Pallor is a manifestation"], "C"),
        ("Turner syndrome is not characterized by", ["Primary amenorrhea", "Short stature", "Karyotype 47,XXY", "Webbed neck", "Skeletal and mental abnormalities"], "C"),
        ("Surgical indications of pituitary adenoma include all the following except", ["Pituitary macroadenoma", "Worsening vision", "Failure of medical treatment", "Pituitary apoplexy", "Pituitary microadenoma responding to medical treatment"], "E"),
        ("Which is an effect of glucocorticoids on carbohydrate metabolism?", ["It inhibits gluconeogenesis", "It decreases glucose uptake and utilization by cells", "It decreases glucose output by the liver", "It stimulates glycogenolysis", "It inhibits intestinal glucose absorption"], "B"),
        ("One statement about a GLP-1 analogue is not true", ["It decreases appetite", "It is mainly used in treatment of type 2 diabetes", "It is given subcutaneously", "It acts more rapidly than regular insulin", "It can promote weight loss"], "D"),
        ("Which rapid-acting insulin statement is false?", ["It is given around meals", "It is given 15 minutes before a meal", "It causes more hypoglycemia than regular insulin", "It has a shorter duration than regular insulin", "It is given by intravenous route"], "C"),
        ("Which drug promotes the release of endogenous insulin?", ["Acarbose", "Sulfonylurea", "Metformin", "Pioglitazone", "Dapagliflozin"], "B"),
        ("A 17-year-old has a 3-cm papillary thyroid nodule without metastases. First-line treatment is", ["Thyroxine therapy", "Radioactive iodine therapy", "Excision of the nodule", "Hemithyroidectomy", "Total thyroidectomy"], "E"),
        ("Simple multinodular goiter is not complicated by", ["Tracheal compression", "Retrosternal extension", "Hemorrhage in a nodule", "Development of thyrotoxicosis", "Hoarseness of voice"], "E"),
        ("The secretion of ACTH", ["Shows a circadian rhythm", "Decreases during stress", "Is inhibited by aldosterone", "Is stimulated by glucocorticoids", "Is stimulated by epinephrine"], "A"),
        ("In treatment of Graves disease, all statements are true except", ["Thyroidectomy is the first-line treatment", "Agranulocytosis is a possible complication of antithyroid drugs", "Radioactive iodine is contraindicated during pregnancy", "Radioactive iodine is better avoided in exophthalmos", "Toxicity should be controlled before thyroidectomy"], "A"),
        ("For preoperative and intraoperative management of pheochromocytoma, all are used except", ["Alpha-adrenergic blockers", "Beta-adrenergic blockers as first-line antihypertensive therapy", "Correction of deficient blood volume", "Correction of dehydration", "Arterial cannula for monitoring"], "B"),
        ("Clinical manifestations of thyroid malignancy include all the following except", ["Neck pain", "Progressive enlargement of a neck mass", "Hoarseness of voice", "Jaundice", "Hard and fixed solitary thyroid nodule"], "D"),
        ("Regarding precocious puberty, which is false?", ["It is often idiopathic but may indicate a brain tumor", "It has a bad psychological impact", "It occurs more in boys than girls", "Early growth followed by epiphyseal closure can cause short adult height", "Early treatment is mandatory"], "C"),
        ("Risk factors for microvascular complications do not include", ["Long duration of diabetes", "Prolonged hyperglycemia", "Hypertension", "Insulin resistance", "Genetic factors"], "D"),
        ("Which is false regarding prolactinoma?", ["It presents with galactorrhea-amenorrhea syndrome", "It may be a micro- or macroadenoma", "It does not respond to medical treatment", "Drug-related hyperprolactinemia may present similarly", "Pressure symptoms may be absent or present"], "C"),
    ]
    questions = [{"stem": stem, "options": {"ABCDE"[i]: value for i, value in enumerate(options)}, "correct": correct} for stem, options, correct in data]
    module.write_mcq(
        ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/28_End_module_2021_2022.md",
        "Endocrinology summative 2021–2022",
        questions,
        "30 MCQs recovered from the scan; marked answers were preserved where visible and unclear choices were derived from the source wording.",
        "marked",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
