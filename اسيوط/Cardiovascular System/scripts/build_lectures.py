#!/usr/bin/env python3
"""Build CVS/Lectures/<subcategoryId>.pdf from the raw lecture drop.

Mapping was derived by reading the first page / slide of every one of the 43 raw
files and matching it to the platform subcategory export (42 rows).
"""
import os, subprocess, fitz, openpyxl

MOD = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(MOD, "Lectures_raw", "1- Cardiovascular system")
PPT = "/tmp/pptx2pdf"
OUT = os.path.join(MOD, "Lectures")
CAT = "AssiutUniv_CARDIOVASCULAR_SYSTEM"

def raw(n):  return os.path.join(RAW, n)
def ppt(n):  return os.path.join(PPT, n)


def ensure_ppt(path):
    """PPT is a scratch cache that does not survive a reboot, so rebuild any
    missing conversion from the .pptx next to the other raw lectures instead of
    dying on a stale path — this script has to stay re-runnable from a clean
    machine."""
    if os.path.exists(path):
        return
    src = os.path.join(RAW, os.path.basename(path)[:-4] + ".pptx")
    if not os.path.exists(src):
        raise FileNotFoundError(f"no cached PDF and no source pptx for {path!r}")
    os.makedirs(PPT, exist_ok=True)
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf",
                    "--outdir", PPT, src], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(path):
        raise RuntimeError(f"libreoffice did not produce {path!r}")
    print(f"  (converted {os.path.basename(src)})")

# suffix -> list of (path, first_page, last_page) 1-based inclusive; None,None = whole doc
MAP = {
 "ANATOMY_OF_THE_MEDIASTINUM_PERICARDIUM_HEART": [(raw("1- anatomy of heart for d marwa.pdf"), None, None)],
 "DEVELOPMENT_AND_CONGENITAL_ANOMALIES_OF_THE_HEART": [(raw("2- CVS- L 2 Anatomy.pdf"), 1, 16)],
 "ANATOMY_OF_THE_GREAT_VESSELS": [(raw("CVS-L 23.pdf"), 17, 24)],
 "ANATOMY_OF_THE_BLOOD_SUPPLY_AND_NERVE_SUPPLY_OF_THE_HEART": [(raw("6 -blood supplyof the heart for d marwa.pdf"), None, None)],

 "BASIC_STRUCTURE_OF_THE_HEART": [(ppt("3- CVS-L 3 Histology.pdf"), None, None)],
 "BLOOD_VESSELS": [(ppt("24-25- CVS-L 24,25 Histology.pdf"), 1, 22)],
 "BLOOD_CAPILLARIES_SPECIALIZED_ARTERIES_AND_SENSORY_STRUCTURES_OF_BLOOD_VESSELS": [(ppt("24-25- CVS-L 24,25 Histology.pdf"), 23, 37)],

 "ELECTROPHYSIOLOGY_OF_CARDIAC_MUSCLE_AND_ORIGIN_OF_THE_HEART_BEAT": [(raw("4- Electrophyio&Rhyth (lecture 4)_compressed.pdf"), None, None)],
 "CARDIAC_MUSCLE_EXCITATION_CONTRACTION_COUPLING": [(raw("5- Cardiac Contractility(Lectures 5).pdf"), None, None)],
 "CONDUCTION_SYSTEM_IN_THE_HEART": [(raw("7- conductive system(Lectures 7).pdf"), None, None)],
 "THE_ELECTROCARDIOGRAM": [(raw("lecture 8 normal ECG 2023 Eman.pdf"), None, None)],
 "ABNORMAL_ECG_AND_ARRHYTHMIA": [(raw("9- Abnormal ECG (Lecture 9).pdf"), None, None)],
 "CARDIAC_CYCLE": [(raw("10- Cardiac Cycle(Lecture 10).pdf"), None, None)],
 "JUGULAR_CURVE_AND_RADIAL_CURVE_AND_HEART_SOUND": [(raw("11- JVP& APW &HS(Lecture 11).pdf"), None, None)],
 "HEART_RATE_ANDCARDIOVASCULA_R_REFLEXES": [(ppt("18- CVS-L 18 Physiology.pdf"), 1, 34)],
 "CARDIAC_OUTPUT_AND_CARDIAC_RESERVE": [(ppt("19- CVS-L19 Physiology.pdf"), None, None)],
 "HEART_FAILURE": [(ppt("21- CVS-L 21 Physiology.pdf"), None, None)],
 "HEMODYNAMICS": [(ppt("26- CVS-L 26 Physiology.pdf"), None, None)],
 "BLOOD_PRESSURE_AND_FLOW_IN_THE_ARTERIES_AND_ARTERIOLES": [(ppt("27- CVS-L 27 Physiology.pdf"), None, None)],
 "REGULATION_OF_THE_VASCULATURE_BY_THE_ENDOTHELIUM": [(ppt("28- CVS-L 28 Physiology.pdf"), None, None)],
 "THE_MICROCIRCULATION_AND_THE_VENOUS_SYSTEM": [(ppt("34-35- CVS-L 34,35 Physiology.pdf"), 1, 25)],
 "THE_CORONARY_CIRCULATIONS_AND_VASCULAR_SMOOTH_MUSCLE_EXCITATION_CONTRACTION_COUPLING": [(ppt("34-35- CVS-L 34,35 Physiology.pdf"), 26, 41)],
 # "Lecture 40, 41.pptx" is two lectures in one deck: s1-35 = L40 Haemorrhage &
 # Shock, s36-45 = L41 Summary of CVS reflexes + adaptation to exercise.
 # (s46-47 are MCQs and are extracted as a question source, not a lecture.)
 "SHOCK_AND_HEMORRHAGE": [(ppt("Lecture 40, 41.pdf"), 1, 35)],
 "CARDIOVASCULAR_REFLEXES_AND_EFFECT_OF_EXERCISE": [(ppt("Lecture 40, 41.pdf"), 36, 45)],

 "RHEUMATIC_FEVER": [(raw("12- CVS-L 12 Microbiology.pdf"), None, None)],
 "INFECTIVEENDOCARDITIS": [(raw("13- CVS- L13 Microbiology.pdf"), None, None)],
 "VIRALMYOCARDITIS": [(raw("15- CVS-L 15 Microbiology.pdf"), None, None)],

 "CARDITIS": [(raw("14- Inflammatory Disorders of The Heart.pdf"), None, None)],
 "ATHEROSCLEROSIS": [(raw("29- CVS-L29.pdf"), None, None)],
 "HYPERTENSION": [(raw("CVS-L 30.pdf"), None, None)],
 "ISCHEMIC_HEART_DISEASE": [(raw("CVS-L 37.pdf"), None, None)],
 "VACUITIES_ANEURYSM_AND_VARICOSE_VEIN": [(raw("CVS-L39.pdf"), None, None)],

 "CARDIAC_INVOLVEMENT_WITH_PARASITIC_INFESTATIONS": [
     (raw("Parasitology-CVS-206-handout-Lecture 17    2023-2024.pdf"), None, None),
     (raw("Cardiovascular Parasite (2).pdf"), None, None),
     (raw("Table (2).pdf"), None, None)],

 "ANTIARRHYTHMIC_DRUGS": [(raw("20- CVS- L20 Pharmacology.pdf"), None, None)],
 "DRUGS_USED_IN_THETREATMENT_OF_HEART_FAILURE": [(raw("22- CVS-L22 Pharmacology.pdf"), None, None)],
 "ANTIHYPERTENSIVE_DRUGS": [(raw("31- CVS-L31 Pharmacology.pdf"), None, None)],
 "TREATMENT_OF_HYPERLIPIDEMIA": [(raw("33- CVS-L33 Pharmacology.pdf"), None, None)],
 "DRUGS_USED_TO_TREAT_ANGINA_PECTORIS": [(raw("L38 Pharmacology Week 4 (1).pdf"), None, None)],

 "PLASMA_LIPOPROTEINS_AND_CHOLESTEROL_HYPERLIPIDEMIA": [(raw("32- CVS -L 32.pdf"), None, None)],
 "CARDIAC_ENZYMES_AND_OTHER_PROTEINS_MARKERS": [(raw("36- CVS-L36-cardiac markers-22.pdf"), None, None)],
}

# No lecture file exists in the Drive drop for these two platform rows.
MISSING = {
 "VALVULAR_AND_CONGENITAL_HEART_DISEASES":
    "No Pathology lecture on valvular/congenital heart disease in the Drive drop. "
    "The only unmatched Pathology file is 'CVS-L 16 Pathology.pdf' = Tumors of the "
    "Cardiovascular System, which is a different topic and was NOT substituted.",
 "VACUITIES_ANEURYSM_AND_VARICOSE_VEIN_2":
    "Platform row tagged Pharmacology but named after the Pathology vasculitis "
    "lecture. All five real Pharmacology lectures (L20, L22, L31, L33, L38) are "
    "already mapped, so no file matches this row.",
}

def main():
    os.makedirs(OUT, exist_ok=True)
    wb = openpyxl.load_workbook([os.path.join(MOD, f) for f in os.listdir(MOD)
                                 if f.startswith("subcategories_")][0])
    ids = [r[2] for r in wb.active.iter_rows(min_row=2, values_only=True) if r[2]]
    suffixes = {i[len(CAT) + 1:]: i for i in ids}

    unknown = set(MAP) | set(MISSING) - set(suffixes)
    assert not (set(MAP) | set(MISSING)) - set(suffixes), \
        f"suffixes not in export: {(set(MAP)|set(MISSING))-set(suffixes)}"
    uncovered = set(suffixes) - set(MAP) - set(MISSING)
    assert not uncovered, f"export rows with no decision: {uncovered}"

    for suffix, parts in sorted(MAP.items()):
        out = fitz.open()
        for path, a, b in parts:
            if path.startswith(PPT):
                ensure_ppt(path)
            src = fitz.open(path)
            n = src.page_count
            out.insert_pdf(src, from_page=(a or 1) - 1, to_page=(b or n) - 1)
            src.close()
        dst = os.path.join(OUT, suffixes[suffix] + ".pdf")
        out.save(dst, garbage=4, deflate=True)
        print(f"{out.page_count:4d}p  {suffixes[suffix]}.pdf")
        out.close()

    print()
    for suffix, why in MISSING.items():
        print(f"MISSING  {suffixes[suffix]}\n         {why}\n")
    print(f"written {len(MAP)} / {len(ids)} subcategories")

if __name__ == "__main__":
    main()
