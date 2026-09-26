#!/usr/bin/env python3
"""Source 16 — CVS written 2022 (round 2 / second round).pdf (Assiut,
.ocr/16_final_written_2022_r2.txt). The Arabic filename means "second round".

The header on every page (lines 2-4 of the OCR) is a decorative logo/stamp
that OCR'd into unreadable glyph soup; it is not Arabic script but pure noise
and is stripped along with it. One legible fragment survives inside that
header block: "n xam_ 18/9/2022" (Final Exam, 18/9/2022) -- the September
exam date, consistent with a second-round ("دور تاني") sitting and with the
catalog's Year 2022.

Unlike source 15, this scan is clean: the body text OCR'd almost perfectly
(no handwriting overlay), every question carries a fully legible printed
model answer, and every page in the OCR text is duplicated verbatim (a
scanning artifact, not missing content). No question required a derived
answer and none was excluded.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '16_Assiut_Final_Written_2022_Round_2.md')
SRC_TXT = os.path.join(MOD, '.ocr', '16_final_written_2022_r2.txt')

TAG = 'Exams, Final 2022 Round 2'
YEAR = 2022


def build():
    Qs = []

    Qs.append(Q(
        stem="Describe the arterial pulse curve",
        exp="1) Ascending limb ('anacrotic limb'): due to a very rapid rise in "
            "arterial pressure during ventricular systole, followed by a "
            "maintained high-level pressure for 0.2-0.3 sec. 2) Descending limb "
            "('catacrotic limb'): the slow decline of pressure back to the "
            "diastolic level. During this phase there is a dicrotic notch "
            "(incisura) followed by a dicrotic wave. The dicrotic notch occurs "
            "immediately before closure of the aortic valve: as the ventricle "
            "relaxes, intraventricular pressure begins to fall rapidly and "
            "backflow of blood from the aorta toward the ventricle lets aortic "
            "pressure begin falling, but this backflow suddenly closes the "
            "aortic valve. The notch is visible on a recorded pressure wave but "
            "is not palpable at the wrist. The dicrotic wave is caused by rapid "
            "elastic recoil of the aortic wall.",
        source='key',
    ))

    Qs.append(Q(
        stem="Mention two factors affecting cardiac rhythmicity",
        exp="1) Nervous factors: the rhythmic excitation of pacemaker cells is "
            "changed by the autonomic nerves innervating the heart. "
            "Parasympathetic stimulation releases acetylcholine at the vagal "
            "nerve ending, which increases membrane permeability to potassium "
            "and its rapid outward leakage, causing hyperpolarization that "
            "decreases the resting membrane potential (-65 to -75 mV), "
            "excitability and firing rate, so it decreases the rhythmicity of "
            "the SA node. Sympathetic stimulation releases norepinephrine, which "
            "increases membrane permeability to sodium and calcium and "
            "decreases permeability to potassium, increasing the rate of "
            "pacemaker depolarization and accelerating the rate of excitation. "
            "2) Effect of temperature: a moderate rise in temperature increases "
            "rhythmicity (heat increases membrane permeability to ions, "
            "accelerating self-excitation), though prolonged elevation exhausts "
            "the heart and decreases rhythmicity; a decrease in temperature "
            "greatly decreases rhythmicity. 3) Effect of ions: excess Na+ "
            "depresses cardiac function by competing with calcium; very low "
            "sodium (water intoxication) causes death from cardiac "
            "fibrillation. Potassium favours diastole; excess extracellular K+ "
            "dilates and flaccidifies the heart and slows rhythmicity (by "
            "decreasing the resting membrane potential), and 2-3x normal "
            "levels can block A-V conduction and cause death. Calcium favours "
            "systole; excess Ca2+ causes spastic contraction (calcium rigor), "
            "while deficiency causes cardiac flaccidity and arrhythmia. "
            "4) Chemical factors: moderate acidity decreases, moderate "
            "alkalinity increases rhythmicity (excess of either stops it); "
            "adrenaline, noradrenaline and thyroxine increase, acetylcholine "
            "decreases rhythmicity. 5) Oxygen lack decreases rhythmicity.",
        source='key',
    ))

    Qs.append(Q(
        stem="What is the suggested diagnosis in this case? Describe the "
             "factors that regulate coronary blood flow",
        exp="Diagnosis: myocardial infarction. Factors influencing coronary "
            "blood flow: 1) Mechanical: coronary flow occurs mainly during "
            "diastole, since ventricular contraction in systole compresses the "
            "coronary vessels (especially the subendocardial vessels of the "
            "left ventricle, where flow is essentially absent during systole "
            "because intraventricular pressure slightly exceeds aortic "
            "pressure); tachycardia shortens diastole and so reduces left "
            "ventricular coronary flow. The right ventricle and atria show less "
            "systolic reduction because their intracavitary pressures stay "
            "well below aortic pressure. Aortic (especially diastolic) blood "
            "pressure also directly determines coronary flow. 2) "
            "Autoregulation (local metabolism): coronary flow is proportional "
            "to the myocardium's oxygen need, through a local effect of O2 "
            "deficiency on coronary smooth muscle and release of vasodilator "
            "substances (adenosine being the most powerful, plus adenosine "
            "phosphates, K+, H+, CO2, bradykinin, prostaglandins) in response "
            "to increased metabolism or reduced arterial O2. 3) Nervous: "
            "sympathetic stimulation directly relaxes small (mainly "
            "beta-receptor) coronary vessels and constricts large "
            "(alpha-receptor) coronary vessels, but indirectly increases heart "
            "rate, contractility and myocardial metabolism, so the overall "
            "effect of sympathetic stimulation is increased coronary flow; "
            "parasympathetic stimulation directly produces slight coronary "
            "vasodilatation but indirectly slows the heart and decreases "
            "myocardial metabolism, so it indirectly constricts the coronaries. "
            "4) Chemical: coronary dilators include O2 lack, vasodilator "
            "metabolites (CO2, H+, K+, lactic acid, prostaglandins, adenine and "
            "adenosine), histamine, adrenaline and noradrenaline, and nitrites "
            "(nitroglycerin, amyl nitrite, aminophylline); coronary "
            "constrictors include vasopressin (ADH) and angiotensin.",
        source='key',
    ))

    Qs.append(Q(
        stem="Define cardiovascular shock and mention the mechanism of septic "
             "shock",
        exp="Definition: shock is a generalized inadequacy of blood flow and "
            "inadequate delivery of substrates and oxygen to meet the "
            "metabolic needs of the tissues, to a degree that the tissues are "
            "damaged. Mechanisms of septic shock: 1) A severe systemic "
            "inflammatory response triggered by the presence of infectious "
            "organisms/toxins. 2) Increased capillary permeability. "
            "3) Macrophages secrete the vasodilator cachectin (TNF). "
            "4) Decreased myocardial contractility. 5) Production of the "
            "potent vasodilator nitric oxide.",
        source='key',
    ))

    Qs.append(Q(
        stem="Describe the myogenic mechanism for local regulation of blood "
             "flow",
        exp="When arterial pressure increases, blood flow initially increases "
            "then returns toward normal through negative-feedback (myogenic) "
            "mechanisms: increased pressure induces changes in extracellular "
            "matrix proteins that activate integrin receptors in vascular "
            "smooth muscle, opening L-type voltage-gated Ca2+ channels and "
            "causing Ca2+ influx, vasoconstriction and return of flow to "
            "normal. Increased pressure may also stretch the vascular smooth "
            "muscle, stimulating stretch-activated channels that allow Na+ and "
            "Ca2+ influx and depolarize the cell, an additional stimulus for "
            "opening the same Ca2+ channels. In addition, increased pressure "
            "with increased flow washes out vasodilator metabolites, which "
            "also leads to vasoconstriction and return of flow to normal.",
        source='key',
    ))

    Qs.append(Q(
        stem="Describe the abdominal compression mechanism that regulates "
             "arterial blood pressure",
        exp="The abdominal compression reflex: when the baroreceptor or "
            "chemoreceptor reflexes are activated (e.g. by a fall in arterial "
            "blood pressure), nerve signals are transmitted simultaneously to "
            "the skeletal muscles of the abdominal wall. This causes "
            "vasoconstriction and compression of the venous reservoirs of the "
            "abdomen, translocating blood out of the abdomen toward the heart "
            "and helping to raise arterial blood pressure back to normal.",
        source='key',
    ))

    Qs.append(Q(
        stem="Complete: the myocardium is composed of cardiac muscle and "
             "corresponds to the ______ of the blood vessel wall",
        exp="The tunica media.",
        source='key',
    ))

    Qs.append(Q(
        stem="Complete: the intercalated disc is composed of ______, ______ "
             "and ______",
        exp="Fascia adherens, desmosomes and gap junctions.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate the functions of endothelial cells",
        exp="1) They provide a smooth surface. 2) They secrete collagen, "
            "laminin, endothelin and nitric oxide.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate the specialized sensory structures in arteries",
        exp="The carotid sinus, and the carotid and aortic bodies.",
        source='key',
    ))

    Qs.append(Q(
        stem="A 65-year-old man presented to the emergency department with an "
             "episode of chest pain not relieved by rest or nitroglycerin. "
             "After stabilization in the telemetry unit for 2 days, he "
             "underwent a thallium stress test, which showed reduced perfusion "
             "of the lateral wall of the left ventricle. a) Which artery is "
             "most likely occluded? b) Name only two branches of the right "
             "coronary artery. c) Describe the boundaries of the transverse "
             "sinus of the pericardium",
        exp="a) The circumflex artery. b) Branches of the right coronary "
            "artery (name any two): the right conus artery, anterior "
            "ventricular branches, the right marginal artery, posterior "
            "ventricular branches, the posterior interventricular (descending) "
            "artery, atrial branches, and the artery of the sino-atrial node. "
            "c) The transverse sinus lies between the reflection of serous "
            "pericardium around the aorta and pulmonary trunk anteriorly and "
            "the reflection around the superior vena cava posteriorly.",
        source='key',
    ))

    for q in Qs:
        q.tag = TAG
        q.tag_suggere = None
        q.year = YEAR
    return Qs


def main():
    questions = build()

    meta = {
        'Source file': 'ASSIUT PREVIOUS EXAMS/CVS written 2022 دور تاني.pdf',
        'Type': 'Scanned written exam, OCR at 300 dpi, 7 pages (clean scan; '
                'every page duplicated in the OCR text; decorative header logo '
                'on every page OCR\'d into unreadable glyph noise and stripped)',
        'Tag': TAG,
        'tagSuggere': 'None',
        'Year': YEAR,
        'Answer source': f'{len(questions)} key, 0 derived',
    }

    n = write_md(OUT, 'Source 16 — Assiut Final Written 2022 Round 2', meta, questions)

    with open(SRC_TXT, encoding='utf-8') as f:
        raw = f.read()
    answer_blocks = raw.lower().count('answer')

    print('=== Source 16: Assiut Final Written 2022 Round 2 ===')
    print(f'Total questions: {n} (all written/QROC; 0 MCQ)')
    print(f'Answer-source breakdown: key={n}, derived=0')
    print('Completeness counters:')
    print('  highest question number identifiable in the printed source: 11 '
          '(source uses fresh headings per subject block - "First/Second/Third '
          'question" in Physiology, roman-numeral sections in Histology, an '
          'unnumbered case in Anatomy - continuously renumbered to Q1-Q11)')
    print(f'  raw occurrences of the word "answer" in the OCR text (both '
          f'duplicated page copies): {answer_blocks}')
    print(f'  ### Q headings written to markdown: {n}')
    print('Exclusions: none. This scan is clean and every question has a '
          'fully legible printed model answer.')


if __name__ == '__main__':
    main()
