#!/usr/bin/env python3
"""Curate the four-page Mogy pediatric endocrine question scan.

The source has a printed answer strip and one figure-matching item.  The
matching item is kept as QROC with the recovered mapping and the figure crop,
because the 31-column platform schema cannot represent a multi-part matching
key as one single MCQ letter.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "أزهر دمياط/Endocrinology/Markdown_Questions/25_Mcq_endocrine_Mogy_Pediatrics.md"


def main() -> int:
    mcqs = [
        ("Type 1 diabetes mellitus is characterized by all the following except", [
            "Majority of cases present acutely", "Obesity is an important predisposing factor", "Insulin therapy is always needed", "Positive family history is less common than in type 2 diabetes", "Islet-cell antibodies are present in the majority of cases",], "B"),
        ("All the following are correct about insulin therapy in uncomplicated type 1 diabetes mellitus except", [
            "Dose is 0.3–1 U/kg/day", "Intermediate-acting insulin comprises two-thirds of the dose", "Majority of patients are managed by twice-daily injections", "Confinement in bed due to a fractured hip needs a decrease of the dose", "Infection needs an increase of the dose by 10–15%",], "D"),
        ("Hypoglycemic symptoms include all the following except", ["Pallor", "Irritability and bad behavior", "Dizziness", "Tiredness", "Dry skin"], "E"),
        ("All the following are correct about diet in type 1 diabetes mellitus except", [
            "Daily caloric intake of a 6-year-old child should be around 1000 kcal", "Timing and caloric content of meals and snacks should be fixed", "Caloric intake should be 50–55% from carbohydrates", "High-fiber food is encouraged", "Complex carbohydrates are preferable to simple sugars",], "A"),
        ("In the management of diabetic ketoacidosis, all the following are correct except", [
            "The starting intravenous fluid is saline", "Regular insulin is given at 0.1 U/kg/hour", "Potassium chloride is added after 12–24 hours", "The drop in blood glucose should not exceed 100 mg/dL/hour", "A nasogastric tube is introduced to empty the stomach if the patient is comatose",], "C"),
        ("All the following are early manifestations of congenital hypothyroidism except", ["Feeding difficulties", "Large protruding tongue", "Large anterior fontanelle", "Excessive sleepiness", "Prolonged neonatal jaundice"], "B"),
        ("All the following are correct about congenital hypothyroidism except", [
            "Most cases are due to aplasia", "Treatment starting at 6 months is unlikely to result in normal mental development", "A delay in the screening test for a few weeks makes it insensitive", "The thyroxine dose per kilogram decreases with age", "Fever and diarrhea are common manifestations of overdosage",], "C"),
        ("All the following are correct about constitutional delay in growth and puberty except", ["Normal birth size", "Short stature becomes evident at adolescence", "Bone age is delayed", "Parental height is average", "Final height is short"], "E"),
        ("Which of the following is correct about growth-hormone deficiency?", ["It is the commonest cause of short stature", "BMI is below average", "Birth weight and length are lower than average", "Infantile body proportions", "Mentality is below average"], "D"),
        ("Children with constitutional delay in growth and puberty can expect ultimately to be", ["Of normal height and weight", "Short and obese", "Short but of proportionate weight", "Tall but of proportionate weight", "Tall and obese"], "A"),
        ("According to current theory, the most likely cause of insulin-dependent type 1 diabetes mellitus is", ["Chromosomal imbalance", "An enzyme defect preventing proper insulin action", "Autoimmune destruction of pancreatic beta cells", "A high-carbohydrate diet over a long period", "Chronic emotional stress"], "C"),
        ("A full-term normal-weight newborn has decreased T4 and increased TSH shortly after birth. The most likely diagnosis is", ["Congenital hyperthyroidism", "Congenital hypothyroidism", "Transient hypothyroidism", "Secondary hypothyroidism due to hypopituitarism", "None of the above"], "B"),
        ("Manifestations of thyroxine overdosage in management of hypothyroidism in a young child may include any of the following except", ["Tachycardia", "Fever", "Sleeplessness", "Diarrhea", "Vomiting"], "E"),
        ("All the following are correct about the national screening programme for congenital hypothyroidism except", [
            "A dry blood spot is taken from a prick heel capillary blood sample", "The sample is collected from the third to the seventh day of life", "TSH is measured", "Positive cases should immediately start lifelong treatment", "Blood sampling of premature infants should not be delayed",], "D"),
        ("Match the numbered height curves in the figure with the appropriate diagnosis", [
            "A — acquired hypothyroidism; B — growth-hormone deficiency; C — precocious puberty; D — familial short stature; E — constitutional delay in growth and puberty",], "-"),
        ("All the following statements about familial short stature are true except", ["Growth retardation is present from early childhood", "Ultimate height is below average", "Bone age is usually retarded", "Onset of puberty usually occurs at the normal time", "The shape of the growth curve is normal"], "C"),
        ("All the following may be manifestations of an insulin reaction (hypoglycemia) in an insulin-dependent diabetic patient except", ["Loss of appetite", "Sweating", "Lethargy", "Bizarre behavior", "Slurred speech"], "A"),
        ("Factors most likely to contribute to development of diabetic ketoacidosis include all the following except", ["Overeating", "Vomiting", "Omission of insulin doses", "Infection", "Lack of patient education"], "B"),
        ("Nutritional obesity may be complicated by all the following except", ["Hypertension and cardiovascular disease", "Gallbladder disease", "Type 2 diabetes mellitus", "Type 1 diabetes mellitus", "Hypercholesterolemia"], "D"),
        ("A 7-year-old child has weight-for-length at the 85th percentile and length-for-age at the 10th percentile. The most likely diagnosis is", ["He is normal", "Nutritional obesity", "Nutritional stunting", "Chronic renal failure", "Acquired hypothyroidism"], "E"),
    ]

    lines = [
        "# Endocrine and metabolic disorders — Mogy Pediatrics — extracted questions",
        "",
        "Total recoverable questions: 20 (19 QCS, 1 matching QROC)",
        "",
        "> Status: Answer strip and marked answers were read from the source. Q15 is a figure-dependent matching item and is represented as QROC with its source mapping.",
        "",
    ]
    for index, (stem, options, correct) in enumerate(mcqs, start=1):
        if index == 15:
            lines += [
                f"### Q{index}: {stem}",
                "",
                "**Correct Answer:** -",
                "**Answer Source:** marked",
                "**Image:** Images/25_Q15.png",
                "**EXP:** Source mapping: A (acquired hypothyroidism) → curve 2; B (growth-hormone deficiency) → curve 5; C (precocious puberty) → curve 1; D (familial short stature) → curve 3; E (constitutional delay in growth and puberty) → curve 4.",
                "",
                "---",
                "",
            ]
            continue
        lines += [f"### Q{index}: {stem}", ""]
        for position, option in enumerate(options):
            lines.append(f"- **{'ABCDE'[position]})** {option}")
        lines += ["", f"**Correct Answer:** {correct}", "**Answer Source:** key", "", "---", ""]
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
