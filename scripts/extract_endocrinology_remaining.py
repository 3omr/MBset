#!/usr/bin/env python3
"""Source-specific extraction recipes for the next Endocrinology batch.

This file intentionally keeps the recipes separate.  The scans in this module
use different layouts and answer conventions, so a single regex pass would
silently lose stems/options.  Outputs are Markdown staging files; the Excel
gate is still handled by the later audit/compiler stage.
"""

from __future__ import annotations

import re
import subprocess
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "أزهر دمياط/Endocrinology"
RAW = MODULE / "Raw_PDF_Questions"
OCR_TEXT = MODULE / "OCR_Text/Raw_PDF_Questions"
OUT = MODULE / "Markdown_Questions"


def clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]", "", text)
    text = re.sub(r"[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", text)
    text = text.replace("\ufeff", "").replace("\u200b", "").replace("\xa0", " ")
    text = text.replace("->", "→")
    text = re.sub(r"\s*\*\s*1\s*point\b", "", text, flags=re.I)
    text = re.sub(r"\)?\s*\d+\s*\(", " ", text)
    for broken, repaired in {
        "f ollowing": "following",
        "f ull": "full",
        "t ongue": "tongue",
        "t reat": "treat",
        "t hyroid": "thyroid",
        "t hyrox": "thyrox",
        "t hyro": "thyro",
        "t hyrotox": "thyrotox",
        "manif est": "manifest",
        "congenit al": "congenital",
        "st atements": "statements",
        "secret ion": "secretion",
        "reabsorpt ion": "reabsorption",
        "medicat ions": "medications",
        "parat hyroid": "parathyroid",
        "hypot hyroidism": "hypothyroidism",
        "hyper t hyroidism": "hyperthyroidism",
        "t reat ment": "treatment",
        "st ridor": "stridor",
        "f or": "for",
        "f rom": "from",
        "Sweeting": "Sweating",
    }.items():
        text = text.replace(broken, repaired)
    text = re.sub(r"\bCa\s*\*\*\b", "Ca²⁺", text)
    text = re.sub(r"\bNa\s*\*\b", "Na⁺", text)
    text = re.sub(r"\bB1\b", "β1", text)
    text = re.sub(r"\bum\b", "µm", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -\t")


def pdf_text(filename: str) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(RAW / filename), "-"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"pdftotext failed: {filename}")
    return result.stdout


def ocr_text(filename: str) -> str:
    path = OCR_TEXT / f"{Path(filename).stem}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return pdf_text(filename)


def write_mcq(path: Path, title: str, questions: list[dict], note: str, answer_source: str) -> None:
    lines = [f"# {title} — extracted questions", "", f"Total recoverable MCQs: {len(questions)}", ""]
    if note:
        lines += [f"> Status: {note}", ""]
    for index, question in enumerate(questions, start=1):
        lines += [f"### Q{index}: {question['stem']}", ""]
        for label in "ABCDEF":
            if question["options"].get(label):
                lines.append(f"- **{label})** {question['options'][label]}")
        lines += ["", f"**Correct Answer:** {question['correct']}", f"**Answer Source:** {answer_source}", "", "---", ""]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_qroc(path: Path, title: str, questions: list[dict], note: str) -> None:
    lines = [f"# {title} — extracted written questions", "", f"Total recoverable QROC: {len(questions)}", ""]
    if note:
        lines += [f"> Status: {note}", ""]
    for index, question in enumerate(questions, start=1):
        lines += [
            f"### Q{index}: {question['stem']}",
            "",
            "**Correct Answer:** -",
            "**Answer Source:** derived",
            f"**EXP:** {question['answer']}",
            "",
            "---",
            "",
        ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def option_match(line: str):
    return re.match(r"^\s*(?:[]\s*)?(?:[.(\-)]\s*)*([A-Ea-e])\s*[.)\-:]\s*(.*)$", line)


def normalize_marked_questions(text: str, question_numbers: set[int]) -> str:
    """Move the scanned question number from a line suffix to its heading."""
    output: list[str] = []
    for raw_line in text.replace("\r", "").splitlines():
        line = re.sub(r"[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", raw_line)
        if "CamScanner" in line or "Microsoft Forms" in line:
            continue
        match = re.match(r"^(.*?)(?:\s+|^)[.\-]?\s*(\d{1,2})\s*$", line.strip())
        if match and int(match.group(2)) in question_numbers and "total marks" not in line.casefold():
            output.append(f"{match.group(2)}. {match.group(1).strip()}")
        else:
            output.append(line)
    return "\n".join(output)


def parse_marked_pdf(filename: str, question_numbers: set[int]) -> list[dict]:
    text = normalize_marked_questions(pdf_text(filename), question_numbers)
    headings = list(re.finditer(r"(?m)^\s*(\d{1,2})\.\s*(.*)$", text))
    questions: list[dict] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[heading.start():end]
        body = re.sub(r"(?m)^\s*\d{1,2}\.\s*", "", block, count=1)
        option_matches = list(re.finditer(
            r"(?m)^\s*(?:[]\s*)?(?:[.(\-)]\s*)*([A-Ea-e])\s*[.)\-:]\s*(.*)$",
            body,
        ))
        if not option_matches:
            continue
        options: dict[str, str] = {}
        for option_index, match in enumerate(option_matches):
            option_end = option_matches[option_index + 1].start() if option_index + 1 < len(option_matches) else len(body)
            value = body[match.end():option_end]
            value = f"{match.group(2)} {value}"
            value = re.sub(r"[]", "", value)
            value = clean(value)
            if value:
                options[match.group(1).upper()] = value

        correct: str | None = None
        for marked in re.finditer("", body):
            after = body[marked.end():]
            option = re.search(r"(?:^|\n)\s*(?:[.(\-)]\s*)*([A-Ea-e])\s*[.)\-:]", after)
            if option:
                correct = option.group(1).upper()
                break
        if not correct or len(options) < 2:
            continue

        filled = [label for label in "ABCDEF" if options.get(label)]
        if filled != list("ABCDEF"[:len(filled)]):
            mapping = {old: "ABCDEF"[position] for position, old in enumerate(filled)}
            options = {mapping[old]: options[old] for old in filled}
            correct = mapping.get(correct, correct)

        stem = clean(body[:option_matches[0].start()])
        stem = re.sub(r"^\W+", "", stem)
        stem = re.sub(r"\s*\(?\s*\d+\s*\)?\s*\*\s*", " ", stem)
        stem = re.sub(r"\s+", " ", stem).strip(" -*")
        if stem:
            questions.append({"stem": stem, "options": options, "correct": correct})
    return questions


def extract_marked_formatives() -> None:
    first = parse_marked_pdf("1st Endo Formative  (22-23).PDF", set(range(4, 19)))
    second = parse_marked_pdf("2nd Endo Formative  (22- 23) ans.pdf", set(range(4, 44)))
    write_mcq(
        OUT / "23_1st_Endo_Formative_22_23.md",
        "Endocrine formative 1 (2022–2023)",
        first,
        "Marked answers recovered from the form. One incomplete numbered block was excluded because it had no recoverable options.",
        "marked",
    )
    write_mcq(
        OUT / "24_2nd_Endo_Formative_22_23.md",
        "Endocrine formative 2 (2022–2023)",
        second,
        "Marked answers recovered from the form. Q32 was an incomplete form fragment with no recoverable options.",
        "marked",
    )


def parse_unumbered(text: str, answers: list[str]) -> list[dict]:
    """Parse a clean, unnumbered single-column question list.

    A new stem is recognized after a blank separator once the current option
    list has started.  Wrapped option lines remain attached to their option;
    this recipe is used only for the two sources whose layout was inspected.
    """
    lines = text.replace("\r", "").splitlines()
    questions: list[dict] = []
    stem: list[str] = []
    options: dict[str, str] = {}
    current: str | None = None
    had_blank = False

    def finish() -> None:
        nonlocal stem, options, current
        if stem and len(options) >= 2:
            cleaned_stem = clean(" ".join(stem))
            cleaned_options = {key: clean(value) for key, value in options.items() if clean(value)}
            if cleaned_stem and len(cleaned_options) >= 2:
                questions.append({"stem": cleaned_stem, "options": cleaned_options})
        stem, options, current = [], {}, None

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line == "\f":
            had_blank = True
            continue
        match = option_match(raw_line)
        if match:
            label, value = match.group(1).upper(), match.group(2)
            if label == "A" and options:
                finish()
            current = label
            options[current] = value
            had_blank = False
            continue
        if options and had_blank:
            finish()
        if options and current:
            options[current] = f"{options[current]} {line}"
        else:
            stem.append(line)
        had_blank = False
    finish()

    if len(questions) != len(answers):
        raise RuntimeError(f"question/answer count mismatch: {len(questions)} vs {len(answers)}")
    for question, answer in zip(questions, answers):
        question["correct"] = answer
    return questions


def extract_formative_2020() -> None:
    text = pdf_text("Endo  formative 20_21.pdf")
    # The source has no printed key. These letters are derived from the
    # recovered options and are explicitly reported as derived below.
    answers = [
        "B", "A", "D", "D", "A", "A", "A", "D", "B", "D", "C", "D",
        "D", "C", "C", "C", "E", "A", "C", "A", "E", "C", "B", "C",
    ]
    questions = parse_unumbered(text, answers)
    write_mcq(
        OUT / "18_Endo_formative_20_21.md",
        "Endocrine formative 2020–2021",
        questions,
        "24 MCQs recovered; the source contains no answer key, so all answers are derived and require spot-checking.",
        "derived",
    )


def extract_formative_2025() -> None:
    text = ocr_text("Endocrine formative 2025.pdf")
    text = re.sub(r"^.*?(?=Myxedema coma is characterized by)", "", text, count=1, flags=re.S)
    answers = list("CADACCEEDCDEBDA")
    questions = parse_unumbered(text, answers)
    write_mcq(
        OUT / "19_Endocrine_formative_2025.md",
        "Endocrine formative 2025",
        questions,
        "15 MCQs recovered from the online-form export; the file contains no answer key, so all answers are derived.",
        "derived",
    )


def extract_written_exams() -> None:
    write_qroc(
        OUT / "20_Endocrinology_Final_Exam_2023.md",
        "Endocrinology Final Exam 2023",
        [
            {"stem": "Indications of insulin.", "answer": "Indications include type 1 diabetes, diabetic ketoacidosis, hyperosmolar hyperglycemic state, pregnancy when insulin is required, severe uncontrolled hyperglycemia, and acute illness or surgery when oral agents are unsuitable."},
            {"stem": "Complications of hyperparathyroidism.", "answer": "Complications include renal stones or nephrocalcinosis, bone disease and fractures, hypercalcemic crisis, peptic symptoms, pancreatitis, neuropsychiatric symptoms, and cardiovascular effects such as hypertension and arrhythmias."},
            {"stem": "Compare primary and secondary hypoadrenalism regarding causes, clinical picture, investigations, and treatment.", "answer": "Primary disease is adrenal failure, commonly autoimmune, with low cortisol and aldosterone, high ACTH, hyperpigmentation, hypotension, hyponatremia and hyperkalemia. Secondary disease is due to pituitary or hypothalamic ACTH deficiency, with low cortisol, low or inappropriately normal ACTH, no marked hyperpigmentation and preserved aldosterone. Diagnosis uses morning cortisol, ACTH and an ACTH stimulation test; treatment is glucocorticoid replacement, with mineralocorticoid replacement when primary disease causes aldosterone deficiency, plus treatment of the cause."},
            {"stem": "Enumerate risk factors for diabetic nephropathy and how to screen and treat it.", "answer": "Risk factors include long diabetes duration, poor glycemic control, hypertension, smoking, dyslipidemia, family history, and pre-existing renal disease. Screen with urine albumin-to-creatinine ratio and estimated GFR, repeated to confirm persistence. Treatment includes glycemic and blood-pressure control, an ACE inhibitor or ARB when albuminuria or hypertension is present, lipid management, smoking cessation, and avoidance of nephrotoxins."},
            {"stem": "Define precocious puberty, subclinical hypothyroidism, and metabolic syndrome.", "answer": "Precocious puberty is the appearance of secondary sexual characteristics before age 8 in girls or before age 9 in boys. Subclinical hypothyroidism is elevated TSH with normal free T4. Metabolic syndrome is the clustering of central obesity, raised blood pressure, dysglycemia, high triglycerides and low HDL, diagnosed by the accepted criteria when the required number of components is present."},
            {"stem": "Mention one clinical benefit of SGLT inhibitors, carbimazole, GLP-1 analogues, and pioglitazone.", "answer": "SGLT2 inhibitors reduce heart-failure hospitalization and renal progression; carbimazole controls thyroid hormone synthesis in Graves disease; GLP-1 receptor agonists improve glycemia with weight loss and cardiovascular benefit; pioglitazone improves insulin sensitivity."},
            {"stem": "Enumerate manifestations of congenital hypothyroidism.", "answer": "Manifestations may include prolonged jaundice, poor feeding, constipation, lethargy, hypotonia, hoarse cry, macroglossia, umbilical hernia, large fontanelle, dry skin, and later impaired growth and neurodevelopment if untreated."},
            {"stem": "Enumerate types and clinical manifestations of malignant thyroid disease.", "answer": "The main types are papillary, follicular, medullary and anaplastic carcinoma. Presentation may include a thyroid nodule or neck mass, cervical lymphadenopathy, hoarseness from recurrent-laryngeal involvement, dysphagia, airway symptoms, rapid enlargement in anaplastic disease, and symptoms of metastases."},
        ],
        "Eight written prompts recovered; the source supplies no model answers, so the answers are derived and must be reviewed.",
    )
    write_qroc(
        OUT / "21_Final_2022.md",
        "Endocrine Final 2022",
        [
            {"stem": "Incretin-based therapy in the treatment of diabetes mellitus.", "answer": "Incretin therapy includes GLP-1 receptor agonists and DPP-4 inhibitors. GLP-1 agonists enhance glucose-dependent insulin secretion, suppress glucagon, slow gastric emptying and promote satiety and weight loss; DPP-4 inhibitors prolong endogenous incretin activity and are weight neutral."},
            {"stem": "Clinical picture of Addison disease.", "answer": "Features include weakness, weight loss, anorexia, nausea, vomiting, abdominal pain, hyperpigmentation, postural hypotension, salt craving, hyponatremia, hyperkalemia, hypoglycemia and possible adrenal crisis."},
            {"stem": "Indications of insulin.", "answer": "Indications include type 1 diabetes, diabetic ketoacidosis, hyperosmolar state, pregnancy when needed, severe symptomatic hyperglycemia, and patients with acute illness or inadequate control on non-insulin therapy."},
            {"stem": "Case of hypothyroidism and approach to diagnosis.", "answer": "Confirm with TSH and free T4. Primary hypothyroidism shows high TSH with low free T4; central disease shows low or inappropriately normal TSH with low free T4. Test thyroid peroxidase antibodies when autoimmune disease is suspected, assess complications, and treat with levothyroxine while investigating the cause."},
            {"stem": "Drug causes of hyperprolactinemia.", "answer": "Important causes include dopamine antagonists such as antipsychotics and metoclopramide, some antidepressants, methyldopa, verapamil, opioids, estrogens and H2 blockers."},
            {"stem": "Pituitary causes of hypogonadism.", "answer": "Causes include pituitary adenoma, prolactinoma, pituitary apoplexy, Sheehan syndrome, hypophysitis, surgery, irradiation, traumatic injury and infiltrative disease."},
            {"stem": "Clinical picture of growth-hormone deficiency.", "answer": "Children have proportionate short stature, reduced growth velocity, delayed bone age, immature facial appearance, increased truncal fat and sometimes hypoglycemia. Adults may have reduced muscle mass, increased fat, low energy, impaired quality of life and adverse metabolic changes."},
            {"stem": "Enumerate functional adrenal neoplasms.", "answer": "Functional adrenal tumors include cortisol-secreting tumors causing Cushing syndrome, aldosterone-secreting adenomas causing primary hyperaldosteronism, androgen or estrogen-secreting tumors, and catecholamine-secreting pheochromocytomas."},
            {"stem": "Causes of panhypopituitarism.", "answer": "Causes include pituitary or hypothalamic tumors, surgery, radiotherapy, Sheehan syndrome, pituitary apoplexy, traumatic brain injury, hypophysitis, infections such as tuberculosis, and infiltrative disorders such as sarcoidosis or hemochromatosis."},
        ],
        "Nine written prompts recovered; the source supplies no model answers, so the answers are derived and must be reviewed.",
    )
    write_qroc(
        OUT / "22_Final_2026.md",
        "Endocrine Final 2026",
        [
            {"stem": "Compare type 1 and type 2 diabetes mellitus regarding epidemiology, pathophysiology, clinical and laboratory characteristics.", "answer": "Type 1 diabetes is usually autoimmune beta-cell destruction causing absolute insulin deficiency, often beginning in younger patients with weight loss, ketosis and low C-peptide; islet autoantibodies may be present. Type 2 diabetes is associated with insulin resistance and progressive beta-cell dysfunction, usually occurs with overweight or metabolic risk, has preserved C-peptide early, and typically presents without ketosis."},
            {"stem": "Explain measures for prevention of macrovascular complications of diabetes mellitus.", "answer": "Use individualized glycemic control, blood-pressure control, statin therapy according to cardiovascular risk, smoking cessation, regular exercise, weight management, healthy diet, antiplatelet therapy when indicated, and screening and treatment of renal disease and other cardiovascular risk factors."},
            {"stem": "Explain the clinical picture and treatment of adrenal crisis.", "answer": "Adrenal crisis presents with severe weakness, vomiting, abdominal pain, hypotension or shock, dehydration, fever, hypoglycemia, hyponatremia and hyperkalemia. Treat immediately with intravenous hydrocortisone, rapid isotonic saline, dextrose when needed, correction of electrolytes, treatment of the precipitating cause, and later transition to maintenance replacement."},
            {"stem": "Summarize the clinical manifestations of carcinoid syndrome, osteoporosis, primary hyperparathyroidism, and adverse effects of SGLT2 inhibitors.", "answer": "Carcinoid syndrome causes flushing, secretory diarrhea, bronchospasm and right-sided valvular disease. Osteoporosis is often silent until fragility fractures, vertebral pain or height loss. Primary hyperparathyroidism may cause stones, bone disease, abdominal complaints, weakness, neuropsychiatric symptoms and hypercalcemia. SGLT2 inhibitors may cause genital mycotic infections, volume depletion, urinary infections and rare euglycemic ketoacidosis."},
            {"stem": "Enumerate indications of insulin therapy, causes of thyrotoxicosis, and causes of pituitary hypogonadism.", "answer": "Insulin is indicated in type 1 diabetes, ketoacidosis, hyperosmolar state, pregnancy when necessary, severe symptomatic hyperglycemia and failure of other treatment. Causes of thyrotoxicosis include Graves disease, toxic multinodular goiter, toxic adenoma, thyroiditis, exogenous hormone and rare TSH-mediated disease. Pituitary hypogonadism may result from tumors, hyperprolactinemia, Sheehan syndrome, apoplexy, hypophysitis, surgery, irradiation, trauma and infiltrative disease."},
            {"stem": "Discuss causes of short stature and the diagnosis of diabetic ketoacidosis.", "answer": "Short stature may be familial, constitutional, nutritional, systemic, endocrine or genetic; assess growth velocity, height relative to target, bone age, thyroid function, growth-axis testing and systemic disease. Diagnose diabetic ketoacidosis by hyperglycemia or known diabetes, ketonemia or ketonuria, and metabolic acidosis; assess severity and treat with fluids, insulin, potassium monitoring and precipitant control."},
            {"stem": "Classify adrenal tumors and outline management of adrenocortical carcinoma, then describe the surgical anatomy of the thyroid.", "answer": "Adrenal tumors may be cortical or medullary, benign or malignant, and functioning or nonfunctioning. Adrenocortical carcinoma requires staging, hormonal assessment, complete en-bloc resection when possible, specialist systemic therapy for advanced disease and surveillance. The thyroid has two lobes joined by an isthmus; the superior thyroid vessels are close to the external laryngeal nerve, the inferior thyroid artery relates to the recurrent laryngeal nerve, and the parathyroids lie on the posterior surface and must be preserved."},
        ],
        "Seven written prompts recovered; the source supplies no model answers, so the answers are derived and must be reviewed.",
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    extract_formative_2020()
    extract_formative_2025()
    extract_written_exams()
    extract_marked_formatives()
    print("Wrote the formative and written-exam staging files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
