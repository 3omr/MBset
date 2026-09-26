#!/usr/bin/env python3
"""Curate the marked 2023 Endocrinology summative exam."""

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
        ("Factors most likely to contribute to diabetic ketoacidosis include all of the following except", ["Overeating", "Vomiting", "Omission of insulin doses", "Infection"], "A"),
        ("Post-operative complications of pituitary adenoma include the following except", ["Diabetes insipidus", "Diabetes mellitus", "Hypothalamic injury", "CSF leak"], "B"),
        ("Which diabetes drug is least likely to cause weight gain?", ["Glimepiride", "Liraglutide", "Pioglitazone", "Repaglinide"], "B"),
        ("A 72-year-old man with hypoglycemia most likely took which medication?", ["Acarbose", "Glyburide", "Metformin", "Pioglitazone"], "B"),
        ("One of the following is false about parathyroid hormone actions", ["Stimulates resorption of calcium, phosphate and magnesium from bone", "Inhibits resorption of calcium, phosphate and magnesium from bone", "Increases calcium and magnesium reabsorption by the kidneys", "Increases phosphate excretion by the kidneys"], "B"),
        ("One of the following is false about calcitriol actions", ["Increases intestinal calcium absorption", "Increases formation of calcium-binding protein", "Increases PTH secretion", "Promotes bone mineralization"], "C"),
        ("Which statement about aldosterone is true?", ["It is secreted from zona reticularis", "It increases potassium reabsorption from distal tubules", "It increases sodium reabsorption from proximal tubules", "Its secretion is increased by increased plasma potassium"], "D"),
        ("Which hormone stabilizes the lysosomal membrane?", ["Aldosterone", "Growth hormone", "Cortisol", "Dehydroepiandrostenedione"], "C"),
        ("Regarding Graves disease, which is false?", ["It is the most common cause of hyperthyroidism", "It is autoimmune in nature", "It is best treated surgically", "Exophthalmos may precede thyroid manifestations in young girls"], "C"),
        ("The following is a very rare cause of hyperthyroidism", ["Graves disease", "Pituitary adenoma", "Toxic multinodular goiter", "Toxic solitary nodule"], "B"),
        ("The most accurate description of findings in hypoparathyroidism is", ["Low serum calcium with spontaneous fractures", "Low serum calcium with tetany", "High serum calcium with tetany", "High serum calcium with low serum phosphorus"], "B"),
        ("In Addison disease", ["Hypokalemia is evident", "Hyperpigmentation is characteristic", "Hypotension is unusual", "Steroid replacement should not be increased during stress"], "B"),
        ("The following does not lead to short stature", ["Sheehan syndrome", "Cretinism", "Turner syndrome", "Excessive corticosteroid therapy in childhood"], "A"),
        ("The following is false regarding pituitary hypofunction", ["It is usually panhypopituitarism", "It is usually of gradual course", "Hypogonadism occurs early", "Treatment is replacement of levothyroxine then cortisol"], "D"),
        ("In a male patient with primary hyperaldosteronism, the best antihypertensive drug is", ["Spironolactone", "Eplerenone", "ACE inhibitor", "Loop diuretic"], "A"),
        ("The following is not a complication of hyperparathyroidism", ["Renal stones", "Pancreatitis", "Gallbladder stones", "Osteoporosis"], "C"),
        ("The main electrolyte disturbance causing nephrogenic diabetes insipidus is", ["Hypernatremia", "Hypomagnesemia", "Hypophosphatemia", "Hypercalcemia"], "D"),
        ("The main stimulus of vasopressin secretion is", ["Hypoglycemia", "Angiotensin II", "Increased plasma osmolality", "Carbamazepine"], "C"),
        ("The underlying etiology of hypoparathyroidism does not include", ["Autoimmune disease", "Parathyroid adenoma", "Developmental defect", "Surgical removal"], "B"),
        ("Isolated growth-hormone deficiency is not characterized by", ["Disproportionate dwarfism", "Good mental function", "Normal gonads", "Normal other pituitary hormones"], "A"),
        ("Hypoglycemia does not occur in", ["Addison disease", "Hypopituitarism", "Myxedema coma", "Hyperthyroidism"], "D"),
        ("Regarding precocious puberty, which is false?", ["It is often idiopathic but may indicate a brain tumor", "It has a bad psychological impact", "Premature epiphyseal closure can result in short stature", "Early management is not essential"], "D"),
        ("Which is a major secondary cause of dyslipidemia?", ["Hyperthyroidism", "Diabetes mellitus", "Familial combined hyperlipidemia", "Apo C2 deficiency"], "B"),
        ("Among the following adrenal disorders, this is not associated with hypertension", ["Adrenal crisis", "Pheochromocytoma", "Conn syndrome", "Cushing syndrome"], "A"),
        ("Which is false regarding prolactinoma?", ["It presents with galactorrhea-amenorrhea syndrome", "It may be a micro- or macroadenoma", "It does not respond to medical treatment", "Drug-related hyperprolactinemia should be excluded before diagnosis"], "C"),
        ("A 17-year-old with a 3-cm papillary thyroid nodule and no metastases should receive", ["Thyroxine therapy", "Radioactive iodine therapy", "Excision of the nodule", "Total thyroidectomy"], "D"),
        ("About postoperative stridor after thyroidectomy, all are true except", ["Unilateral recurrent-laryngeal nerve injury causes stridor", "Dyspnea from a deep neck hematoma should be immediately evacuated", "Laryngeal edema causes stridor", "Tracheal collapse from tracheomalacia is a rare cause"], "A"),
        ("About thyroid cancer, all are true except", ["FNA is enough to diagnose follicular carcinoma", "Anaplastic carcinoma spreads mainly by local infiltration", "Follicular carcinoma spreads mainly hematogenously", "Malignancy appears as a cold nodule on isotope scan"], "A"),
        ("A full-term newborn has decreased T4 and increased TSH shortly after birth. The diagnosis is", ["Congenital hyperthyroidism", "Congenital hypothyroidism", "Transient hypothyroidism", "Secondary hypothyroidism due to hypopituitarism"], "B"),
        ("Type 1 diabetes mellitus is characterized by all the following except", ["Most cases present acutely", "Obesity is an important predisposing factor", "Insulin therapy is always needed", "Islet-cell antibodies are present in the majority of cases"], "B"),
    ]
    questions = [{"stem": stem, "options": {"ABCDE"[i]: value for i, value in enumerate(options)}, "correct": correct} for stem, options, correct in data]
    module.write_mcq(
        ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/27_End_2023.md",
        "Endocrinology End Exam 2023",
        questions,
        "30 MCQs recovered from the marked scan; answers were read from marked choices where visible and otherwise checked against the source wording.",
        "marked",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
