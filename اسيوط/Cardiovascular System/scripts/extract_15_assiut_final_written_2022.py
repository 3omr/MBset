#!/usr/bin/env python3
"""Source 15 — CVS final written 2022.pdf (Assiut, .ocr/15_final_written_2022.txt).

This scan is the most damaged of the module's written papers: decorative Arabic
script and handwritten overlay OCR into unreadable glyph soup on top of the
actually-printed model answers, and every page in the OCR text is duplicated
verbatim (page N and page N+1 markers hold identical text) because the source
PDF pages themselves were scanned twice. The extraction below is a manual,
line-by-line transcription of only the legible printed answer text — every
stem/EXP pair was checked against the OCR by hand; nothing was invented.

Two items could not be recovered and are logged as EXCLUDED at the bottom of
main(): the tail of the "SAN location" anatomy fragment on page 2/3, and the
first blank of the biochemistry completion question (its answer "Vitamin B12
and folic acid" is legible but the blank's own stem text is not).

Q4 (exercise blood flow) has its printed answer swallowed by decorative
overlay ("...Esiptop ylved in blood pressure") -- the stem is legible so the
question is kept, but the answer is written from standard physiology and
marked 'derived' rather than guessed from the garbled print.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '15_Assiut_Final_Written_2022.md')
SRC_TXT = os.path.join(MOD, '.ocr', '15_final_written_2022.txt')

TAG = 'Exams, Final 2022'
YEAR = 2022


def build():
    Qs = []

    Qs.append(Q(
        stem="A patient developed a state of shock. What is the type of shock in "
             "this case (septic or anaphylactic), and explain the mechanisms of it",
        exp="Septic shock. Mechanisms (any four): 1) Severe vasodilatation. "
            "2) Increased capillary permeability. 3) Macrophages secrete cachectin "
            "(TNF), which produces vasodilatation. 4) Decreased myocardial "
            "contractility. 5) Production of the potent vasodilator nitric oxide.",
        source='key',
    ))

    Qs.append(Q(
        stem="A patient is diagnosed with a cardiac condition (0.5 mark). Describe "
             "Anrep's and gastrocoronary reflexes affecting coronary blood flow",
        exp="Diagnosis: Myocardial infarction. Anrep's reflex: increased venous "
            "return and venous pressure in the right atrium reflexly produces "
            "coronary vasodilatation and increases coronary blood flow. "
            "Gastrocoronary reflex: distension of the stomach with a heavy meal "
            "produces reflex coronary vasoconstriction and decreased coronary "
            "blood flow, so anginal pain may be felt in certain persons after "
            "heavy meals.",
        source='key',
    ))

    Qs.append(Q(
        stem="A patient is diagnosed with a type of heart failure (0.5 mark). "
             "Describe three factors that increase capillary permeability",
        exp="Diagnosis: Systolic heart failure. Factors increasing capillary "
            "permeability: 1) Deficiency of vitamin C, plasma proteins, or "
            "calcium. 2) Acidosis. 3) Capillary dilators such as histamine (in "
            "allergy), CO2, adenosine and bradykinin. 4) Oxygen lack, which "
            "increases capillary permeability via injury of the endothelium and "
            "accumulation of metabolites. 5) Bacterial toxins. 6) Temperature — "
            "excessive cold or heat.",
        source='key',
    ))

    Qs.append(Q(
        stem="Explain the increase of blood flow to skeletal muscle during "
             "isotonic exercise",
        exp="Exercising muscle increases its own blood flow mainly through local "
            "(active) vasodilation: accumulation of vasodilator metabolites "
            "(CO2, lactic acid, adenosine, K+, decreased O2 tension) dilates the "
            "arterioles of the active muscle (active hyperaemia/autoregulation), "
            "while sympathetic activation raises cardiac output and produces "
            "vasoconstriction in non-exercising vascular beds, redistributing "
            "blood to the working muscle.",
        source='derived',
    ))

    Qs.append(Q(
        stem="Describe the central nervous system (CNS) ischemic response as a "
             "mechanism of arterial blood pressure control",
        exp="When arterial blood pressure decreases markedly (below about 60 "
            "mmHg) and blood flow to the vasomotor centres decreases severely, "
            "cerebral ischemia occurs and produces powerful vasoconstriction and "
            "elevation of arterial blood pressure, improving blood flow to the "
            "brain. It acts as an emergency pressure-control system to prevent "
            "arterial pressure and brain blood flow from falling further to a "
            "level close to lethal — hence it is called the 'last-ditch stand' "
            "pressure control mechanism.",
        source='key',
    ))

    Qs.append(Q(
        stem="State Frank-Starling's law of the heart (definition) and its "
             "physiological significance",
        exp="Definition: within physiological limits, the force of contraction "
            "of cardiac muscle is directly proportional to its initial length, "
            "provided all other factors remain constant; the initial length of "
            "the fibres is determined by the degree of diastolic filling of the "
            "heart. Significance: as diastolic filling increases, end-diastolic "
            "volume increases and the force of ventricular contraction increases, "
            "so the heart automatically pumps whatever amount of blood flows "
            "into it from the veins without allowing excessive damming of blood "
            "in the veins. This effect is independent of innervation (autoregulation "
            "or heterometric regulation) and plays an important role in the "
            "beat-by-beat regulation of stroke volume in response to rapid "
            "changes in venous return, such as occurs with changes in posture.",
        source='key',
    ))

    Qs.append(Q(
        stem="A 54-year-old male presents with tight substernal chest pain. A "
             "thallium stress test shows hypoperfusion of the cardiac muscle "
             "forming the anterior surface of the left ventricle. a) Which "
             "coronary artery is most likely occluded in this patient? b) If the "
             "blood supply to the posterior/inferior part of the heart decreases, "
             "which artery is most likely occluded?",
        exp="a) The anterior interventricular artery (left anterior descending, "
            "LAD). b) The posterior interventricular (posterior descending) "
            "artery.",
        source='key',
    ))

    Qs.append(Q(
        stem="Complete: a) In the brain, the blood capillaries are ______, "
             "forming the blood-brain barrier. b) The valves of veins are formed "
             "of ______ that help in propelling blood towards the heart against "
             "gravity",
        exp="a) Modified continuous capillaries with very low permeability, "
            "forming the blood-brain barrier. b) Longitudinally arranged bundles "
            "of smooth muscle fibres.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate: a) The function of the carotid sinus. b) Define the "
             "vasa vasorum",
        exp="a) The carotid sinus is a baroreceptor; when stimulated by an "
            "increase in arterial blood pressure, it sends inhibitory impulses "
            "to the respiratory and cardiovascular centres. b) Larger arteries "
            "and veins contain small blood vessels in their tunica adventitia, "
            "known as the vasa vasorum, which provide them with nourishment.",
        source='key',
    ))

    Qs.append(Q(
        stem="Complete: 1) Atherosclerosis is a disease in which ______ is "
             "deposited in the subendothelial layers of the wall of the "
             "arteries. 2) Type I hyperlipidaemia is caused by deficiency of the "
             "______ enzyme, while Tangier disease is due to deficiency of the "
             "______ enzyme",
        exp="1) Oxidized LDL. 2) Lipoprotein lipase; LCAT.",
        source='key',
        note='The paper also completes a third blank ("Vitamin B12 and folic '
             'acid" = 0.5 mark) whose own question stem was not legible in the '
             'scan; that blank was dropped rather than guessed at.',
    ))

    Qs.append(Q(
        stem="Hoda Ali, 30 years old, has a history of rheumatic fever 10 years "
             "ago and was on benzathine penicillin prophylaxis. A few weeks ago "
             "she developed heart failure and is now on furosemide and captopril. "
             "3 days ago she developed atrial fibrillation and was diagnosed as "
             "a case of digoxin toxicity. a) Enumerate the clinical manifestations "
             "of digoxin toxicity. b) List four lines of treatment of digoxin "
             "toxicity",
        exp="a) Clinical manifestations of digoxin toxicity: 1) GIT effects — "
            "anorexia, nausea and vomiting are among the earliest and commonest "
            "manifestations. 2) Cardiac toxicity — bradycardia, decreased "
            "conduction through the A-V node causing partial or complete heart "
            "block, and increased excitability of the myocardium causing all "
            "types of arrhythmias. 3) CNS effects — delirium, psychosis, "
            "hallucination. 4) Ophthalmic effects — blurring of vision and "
            "abnormal colour sensation (especially yellow and green). 5) "
            "Endocrinal effects — gynaecomastia and galactorrhoea. "
            "b) Lines of treatment: 1) Stop digoxin and diuretic therapy. "
            "2) Give KCl orally (mild cases, e.g. extrasystoles) or IV (severe "
            "cases). 3) Specific treatment: atropine if sinus bradycardia or "
            "heart block; antiarrhythmic drugs such as phenytoin (atrial and "
            "ventricular arrhythmia) or lidocaine (ventricular arrhythmia only). "
            "4) Digibind (specific antibody) in severe cases, given by IV "
            "infusion, binds digoxin and decreases its free form. 5) "
            "Cholestyramine, which decreases intestinal absorption of digoxin.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate two antihypertensive drugs used to treat hypertension "
             "during pregnancy",
        exp="Methyldopa and labetalol.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate the complications of myocardial infarction",
        exp="1) Extension of the infarction. 2) Ventricular arrhythmias. "
            "3) Cardiac rupture and haemopericardium. 4) Rupture of a papillary "
            "muscle or septal rupture. 5) Ventricular thrombosis. 6) Systemic or "
            "pulmonary embolization. 7) Ventricular aneurysm (weeks to months "
            "post-infarction). 8) Chronic ischaemic heart disease (months to "
            "years post-infarction).",
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
        'Source file': 'ASSIUT PREVIOUS EXAMS/CVS final written 2022.pdf',
        'Type': 'Scanned written exam, OCR at 300 dpi, 7 pages (heavily damaged '
                'scan; every page duplicated in the OCR text; a bubble-sheet MCQ '
                'answer grid on the last page carries no recoverable question text)',
        'Tag': TAG,
        'tagSuggere': 'None',
        'Year': YEAR,
        'Answer source': f'{sum(1 for q in questions if q.source == "key")} key, '
                          f'{sum(1 for q in questions if q.source == "derived")} derived',
    }

    n = write_md(OUT, 'Source 15 — Assiut Final Written 2022', meta, questions)

    with open(SRC_TXT, encoding='utf-8') as f:
        raw = f.read()
    answer_blocks = raw.lower().count('answer')

    derived = [q for q in questions if q.source == 'derived']

    print('=== Source 15: Assiut Final Written 2022 ===')
    print(f'Total questions: {n} (all written/QROC; 0 MCQ)')
    print(f'Answer-source breakdown: key={n - len(derived)}, derived={len(derived)}')
    print(f'Derived count: {len(derived)} -> {[q.stem[:40] for q in derived]}')
    print('Completeness counters:')
    print('  highest question number identifiable in the printed source: 12 '
          '(source restarts numbering across Physiology/Anatomy/Histology/'
          'Biochemistry/clinical sections; 13 questions emitted after '
          'continuous renumbering)')
    print(f'  raw occurrences of the word "answer" in the OCR text (both '
          f'duplicated page copies): {answer_blocks}')
    print(f'  ### Q headings written to markdown: {n}')
    print('Exclusions:')
    print('  EXCLUDED - unreadable scan: a fragment after the coronary-artery '
          'anatomy question ("...wall of the right atrium in the... opening of '
          'the superior... lower part of the...") describing what is probably '
          'a question on the sinu-atrial node location; too garbled to '
          'reconstruct a stem or answer.')
    print('  EXCLUDED - unreadable scan: the MCQ bubble-sheet answer grid on '
          'the final page carries no OCR-recoverable question stems at all.')
    print('  A biochemistry completion blank ("Vitamin B12 and folic acid") '
          'was dropped from Q10 because its own question stem was illegible; '
          'the other two blanks in the same completion question were kept.')


if __name__ == '__main__':
    main()
