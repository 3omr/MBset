#!/usr/bin/env python3
"""Extract the 51-question Schwartz endocrine surgery scan.

The PDF is a two-column question/explanation layout.  The left column is
parsed separately and the answer letters are paired from the right-column
answer lines.  A small set of pages whose OCR lost the option labels is
reconstructed from the visible source layout.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/33_Schwartz.md"
COLUMNS = ROOT / "scratch/endo_schwartz_columns.txt"
spec = importlib.util.spec_from_file_location("endo_remaining", ROOT / "scripts/extract_endocrinology_remaining.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


ANSWERS = [
    "B", "B", "C", "B", "A", "B", "D", "B", "A", "A", "D", "B", "C", "B", "D", "A", "C", "B", "C", "B",
    "B", "D", "C", "D", "A", "A", "D", "D", "D", "A", "D", "B", "A", "C", "D", "D", "B", "D", "C", "D",
    "A", "B", "A", "A", "C", "B", "C", "C", "B", "C", "C",
]


def page_left(page: int) -> str:
    text = COLUMNS.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r"----- PAGE (\d+) COL (\d+) -----", text)
    for index in range(1, len(parts), 3):
        if parts[index] == str(page) and parts[index + 1] == "1":
            return parts[index + 2]
    raise KeyError(page)


def scrub_page(text: str) -> str:
    text = re.sub(r"(?m)^\s*(?:8€|jeuaupy|plosAy|plosA|PIOIAY|YALdWHD|Chapter).*?$", "", text)
    text = re.sub(r"(?m)^\s*FIG\..*$", "", text)
    text = re.sub(r"(?m)^\s*\d{3,4}\s*$", "", text)
    return text


def auto_questions(page: int, expected: int) -> list[dict]:
    parsed = module.parse_unumbered(scrub_page(page_left(page)), ["A"] * expected)
    cleaned: list[dict] = []
    for question in parsed:
        stem = module.clean(question["stem"])
        stem = re.sub(r"^.*?(?=\d+\.\s|Which |The |Secreted |Which of |A patient |Following |The initial |The most |In patients )", "", stem, flags=re.I)
        stem = re.sub(r"^\d+\.\s*", "", stem)
        stem = re.sub(r"\s+(?:8€|jeuaupy|plosAy|PIOIAY|YALdWHD|Schwartz|See)\b.*$", "", stem, flags=re.I)
        options = {}
        for label, value in question["options"].items():
            value = module.clean(value)
            value = re.sub(r"\s+(?:8€|jeuaupy|plosAy|PIOIAY|YALdWHD|Schwartz|See)\b.*$", "", value, flags=re.I)
            value = re.sub(r"\s+(?:An|Se|P|T)\s*$", "", value)
            if value:
                options[label] = value
        if stem and len(options) >= 2:
            cleaned.append({"stem": stem, "options": options})
    if len(cleaned) != expected:
        raise RuntimeError(f"Schwartz page {page}: expected {expected}, got {len(cleaned)}")
    return cleaned


def manual(stem: str, options: list[str]) -> dict:
    return {"stem": stem, "options": {"ABCDE"[i]: value for i, value in enumerate(options)}}


def main() -> int:
    questions: list[dict] = []
    questions.append(manual("The most common position of the right recurrent laryngeal nerve is", ["Anterior to the inferior thyroid artery", "Posterior to the inferior thyroid artery", "Between the branches of the inferior thyroid artery", "Absent (nonrecurrent laryngeal nerve)"]))
    questions += auto_questions(2, 4)
    questions += [
        manual("The left adrenal vein drains into the", ["IVC", "Left renal vein", "Left gonadal vein", "Splenic vein"]),
        manual("Which of the following is an effect of thyroid hormones?", ["Positive inotropic effect on the heart", "Maintenance of the normal hypoxic drive to breathe", "Increased protein turnover", "All of the above"]),
        manual("The origin of the superior thyroid artery is", ["Internal carotid artery", "External carotid artery", "Thyrocervical trunk", "Innominate artery"]),
    ]
    questions += auto_questions(4, 1)
    questions += auto_questions(5, 2)
    questions += auto_questions(6, 2)
    questions += auto_questions(7, 2)
    questions += auto_questions(8, 1)
    questions += [
        manual("Which of the following is a function of aldosterone?", ["Increased potassium absorption", "Increased hydrogen ion absorption", "Increased sodium absorption", "None of the above"]),
        manual("Glucocorticoids are produced in the", ["Zona glomerulosa", "Zona fasciculata", "Zona reticularis", "Adrenal medulla"]),
        manual("The paired lateral thyroid anlages originate from", ["Ectoderm", "Mesoderm", "Endoderm", "Neural crest"]),
        manual("Cholesterol is the precursor of all adrenal hormones. The first product is", ["Progesterone", "Pregnenolone", "17-alpha-hydroxypregnenolone", "11-deoxycorticosterone"]),
    ]
    questions += auto_questions(10, 1)
    questions += [
        manual("Which of the following is not commonly seen in MEN1 syndrome?", ["Gastrinoma", "Insulinoma", "Prolactinoma", "Pheochromocytoma"]),
        manual("Painful subacute thyroiditis: which statement is false?", ["It results in hypothyroidism in more than 80% of patients", "It occurs most commonly in women over 70 years", "It is often preceded by an upper respiratory infection", "It requires thyroidectomy for relief in more than 50% of patients"]),
        manual("Which test has the highest sensitivity for localizing parathyroid adenomas?", ["Ultrasound", "Fine-cut CT scan", "PET scan", "Sestamibi scan"]),
    ]
    questions += auto_questions(12, 3)
    questions += auto_questions(13, 1)
    questions += auto_questions(14, 5)
    questions += [manual("A patient with bilateral adrenal enlargement and hyperaldosteronism should next undergo", ["Unilateral adrenalectomy", "Bilateral adrenalectomy", "Selective venous catheterization", "Medical management"])]
    questions += auto_questions(16, 1)
    questions += auto_questions(17, 4)
    questions += auto_questions(18, 3)
    questions += [
        manual("Which syndrome is not typically associated with increased risk of pheochromocytoma?", ["Familial adenomatous polyposis", "Carney syndrome", "Von Hippel–Lindau syndrome", "Sturge–Weber syndrome"]),
        manual("The most common cause of hyperthyroidism is", ["Graves disease", "Toxic multinodular goiter", "Plummer disease", "Thyroiditis"]),
    ]
    questions += auto_questions(20, 2)
    questions += [
        manual("Which CT finding is most suggestive of adrenal cancer?", ["Tumor heterogeneity", "Adjacent lymphadenopathy", "Size greater than 6 cm", "Lesion enhancement"]),
        manual("The most sensitive test to diagnose pheochromocytoma is", ["Plasma VMA", "Urinary VMA", "Plasma metanephrines", "Urinary metanephrines"]),
        manual("Thyroid hormone production is inhibited by", ["Epinephrine", "Glucocorticoids", "Human chorionic gonadotropin", "Alphafetoprotein"]),
        manual("The first diagnostic test ordered for a solitary thyroid nodule is", ["Radioactive iodine scan", "CT or MRI", "Fine-needle aspiration", "Core needle biopsy"]),
        manual("Which cancer does not occur in a thyroglossal duct cyst?", ["Papillary thyroid cancer", "Follicular thyroid cancer", "Medullary thyroid cancer", "Hürthle cell cancer"]),
    ]
    if len(questions) != 51 or len(ANSWERS) != 51:
        raise RuntimeError(f"Schwartz total mismatch questions={len(questions)} answers={len(ANSWERS)}")
    for question, answer in zip(questions, ANSWERS):
        question["correct"] = answer
    module.write_mcq(
        OUT,
        "Schwartz endocrine surgery review",
        questions,
        "51 MCQs recovered from the two-column source; the column layout was separated before extraction and answers were paired from the printed explanation column.",
        "key",
    )
    print(f"Wrote {OUT} ({len(questions)} questions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
