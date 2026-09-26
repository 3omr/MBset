#!/usr/bin/env python3
"""Source 18 — Final Written 2019,2020.pdf (Assiut, .ocr/18_final_written_2019_2020.txt).

The filename names two years, and the OCR confirms this is genuinely two
exam papers bound into one PDF, not one exam re-dated:

  * Pages 1-2 (OCR): "Assiut University ... Final Exam. Date: 11/12/2019",
    "Part II: Short questions (13 questions, 22.5 marks)". Thirteen clinical
    short-answer questions, Q1-13, each printing ONLY the question (no
    "Answer:" text anywhere for this block) followed by an "End of
    questions" line and a practical-exam schedule note.
    -> tagged 'Exams, Final 2019' / Year 2019. All 13 answers are written
       from standard cardiovascular physiology/anatomy/pathology and marked
       'derived' since the paper prints no key at all for this section.
       (This block is the same 2019 sitting also present standalone as
       source 17 / Markdown_Questions/17_Assiut_Final_Exam_2019.md - the
       Stage-4 compiler's stem-dedup is expected to merge the two.)

  * Pages 3 onward (OCR): a differently structured paper - "I- Complete:",
    "II- Essay questions:" - with no date of its own anywhere in the OCR
    text, but every question here DOES carry a fully printed model answer.
    Since the filename declares only two years and the first block is
    unambiguously 2019, this second block is the 2020 sitting by
    elimination.
    -> tagged 'Exams, Final 2020' / Year 2020, answer source 'key'.

Every page in the OCR text is duplicated verbatim (scanning artifact, not
missing content). The decorative logo header on page 1/2 and the
"Practical exam on 12-12-2018" scheduling note are page furniture and are
stripped, not treated as question content.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '18_Assiut_Final_Written_2019_2020.md')
SRC_TXT = os.path.join(MOD, '.ocr', '18_final_written_2019_2020.txt')

TAG_2019 = 'Exams, Final 2019'
TAG_2020 = 'Exams, Final 2020'


def build_2019():
    """Part II: Short questions, 11/12/2019 - no printed key anywhere; all derived."""
    Qs = []

    Qs.append(Q(
        stem="A 62-year-old woman with a history of atrial fibrillation "
             "presents with shortness of breath when lying flat. On "
             "examination her BP is 90/65 mmHg, heart rate 120/min and "
             "irregularly irregular, with increased jugular venous distention; "
             "no S3 or S4 is noted. She is diagnosed with congestive heart "
             "failure. a) Describe the three positive waves of the normal "
             "jugular venous pressure curve and their relation to the phases "
             "of the cardiac cycle. b) Explain the cause of the normal fourth "
             "heart sound, and compare the first and second heart sounds "
             "(relation to phases of the cardiac cycle and main causes)",
        exp="a) The 'a' wave: due to atrial contraction, at the end of "
            "ventricular diastole. The 'c' wave: due to bulging of the closed "
            "tricuspid valve into the right atrium at the start of ventricular "
            "systole (isovolumic contraction). The 'v' wave: due to a rise in "
            "atrial pressure as blood fills the atrium against the closed "
            "tricuspid valve during ventricular systole, peaking just before "
            "the tricuspid valve opens in early diastole. b) The fourth heart "
            "sound is produced by vibration of the ventricular wall during "
            "rapid ventricular filling caused by atrial contraction in late "
            "diastole; it is not normally audible and becomes audible mainly "
            "when the ventricle is stiff/hypertrophied. S1 occurs at the start "
            "of ventricular systole (isovolumic contraction) and is caused by "
            "closure of the atrioventricular (mitral and tricuspid) valves; S2 "
            "occurs at the start of ventricular diastole (isovolumic "
            "relaxation) and is caused by closure of the semilunar (aortic and "
            "pulmonary) valves.",
        source='derived',
    ))

    Qs.append(Q(
        stem="Ahmed, 52 years old, had occasional angina relieved by "
             "nitroglycerin, then awoke with chest pain not relieved by "
             "nitroglycerin. In the emergency room his BP was 105/80, he had "
             "pulmonary oedema, and sequential ECGs suggested a left "
             "ventricular myocardial infarction; his ejection fraction was "
             "35% (normally 55%). a) Which information tells you that Ahmed's "
             "stroke volume was decreased, and what are the three major "
             "factors affecting normal stroke volume? b) What is the "
             "suspected type of heart failure in this case (systolic or "
             "diastolic), and list two compensatory mechanisms of heart "
             "failure",
        exp="a) The markedly reduced ejection fraction (EF = stroke "
            "volume/end-diastolic volume) shows the stroke volume was "
            "decreased. The three major factors affecting stroke volume are "
            "preload (venous return / end-diastolic volume), afterload "
            "(arterial pressure/resistance against which the ventricle "
            "ejects), and myocardial contractility. b) Systolic heart failure "
            "(reduced ejection fraction/contractility). Compensatory "
            "mechanisms of heart failure (any two): the Frank-Starling "
            "mechanism, sympathetic activation (increased heart rate and "
            "contractility), activation of the renin-angiotensin-aldosterone "
            "system, and ventricular hypertrophy/dilatation.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 56-year-old woman presents with dizziness and headache; her "
             "blood pressure is 190/110 mmHg. She takes no medications, and "
             "her complete blood picture shows an increased number of RBCs "
             "with otherwise normal indices. a) What is meant by peripheral "
             "resistance (PR)? What factor is increasing PR in this case, and "
             "why does PR affect diastolic blood pressure more than systolic? "
             "b) Describe the stress-relaxation mechanism involved in "
             "controlling arterial blood pressure",
        exp="a) Peripheral resistance is the resistance offered mainly by the "
            "arterioles to blood flow, determined chiefly by vessel radius and "
            "blood viscosity. Here the raised RBC count (polycythaemia) "
            "increases blood viscosity, which raises PR. PR affects diastolic "
            "pressure more than systolic because diastolic pressure depends "
            "mainly on the rate of run-off of blood through the peripheral "
            "resistance vessels during diastole (when there is no active "
            "ejection), whereas systolic pressure is determined more by "
            "stroke volume and arterial compliance. b) Stress-relaxation "
            "(delayed compliance): when the volume/pressure in a blood vessel "
            "is suddenly increased, the wall stretches immediately, but over "
            "the following minutes the vascular smooth muscle gradually "
            "relaxes, letting the vessel accommodate the extra volume with "
            "only a small further rise in pressure - buffering acute changes "
            "in blood volume or pressure.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 78-year-old male was brought to the emergency room with "
             "severe fever, dyspnoea and hypotension, 5 days after a major "
             "operation, and was diagnosed with septic shock (BP 80/50, "
             "temperature 40°C, heart rate 140/min, RR 38/min); his blood "
             "pressure later fell further as the shock became progressive. "
             "a) What is meant by septic shock, and explain two mechanisms of "
             "septic shock. b) List three positive-feedback death cycles",
        exp="a) Septic shock is a distributive (vasodilatory) type of "
            "circulatory shock caused by severe systemic infection, in which "
            "bacterial toxins trigger a severe inflammatory response. Two "
            "mechanisms: 1) release of inflammatory mediators (e.g. cachectin/"
            "TNF from macrophages) causing severe vasodilatation and increased "
            "capillary permeability with loss of plasma volume; 2) production "
            "of the potent vasodilator nitric oxide, worsening hypotension "
            "together with decreased myocardial contractility. b) "
            "Positive-feedback death cycles (any three): 1) cardiac "
            "depression -> decreased cardiac output -> decreased coronary "
            "perfusion -> further cardiac depression. 2) progressive CNS "
            "(vasomotor centre) ischaemia -> further depression of "
            "vasoconstrictor tone -> further hypotension. 3) tissue hypoxia "
            "and acidosis -> capillary/cell damage and increased capillary "
            "permeability -> further loss of effective blood volume -> "
            "worsening shock. 4) widespread blood clotting (disseminated "
            "intravascular coagulation) -> blocked capillaries -> further "
            "tissue hypoxia.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 60-year-old woman complains of chest pain and is diagnosed "
             "with angina pectoris. Describe the effects of the different "
             "phases of the cardiac cycle on coronary blood flow",
        exp="Coronary blood flow occurs mainly during diastole. During "
            "systole, ventricular contraction compresses the intramural "
            "coronary vessels and sharply reduces flow, especially in the "
            "subendocardial layer of the left ventricle, where flow is "
            "essentially absent during systole because intraventricular "
            "pressure there is briefly close to or exceeds aortic pressure. "
            "During diastole, the myocardium relaxes and releases this "
            "compression, so coronary flow rises rapidly and most of it "
            "occurs in this phase. Because diastole shortens more than "
            "systole as heart rate rises, tachycardia reduces the time "
            "available for coronary filling and can precipitate ischaemia in "
            "a patient with angina.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 50-year-old man complained of dizziness after a long day "
             "standing at work; his blood pressure was 90/60 and he was "
             "diagnosed with postural hypotension. Describe two other harmful "
             "effects of gravity",
        exp="1) Dependent (ankle) oedema: pooling of blood in the leg veins "
            "raises capillary hydrostatic pressure, forcing fluid into the "
            "interstitial tissue of the lower limbs. 2) Varicose veins: "
            "chronically increased venous pressure in the dependent limbs "
            "over-distends and damages the venous valves, leading to "
            "varicosity of the superficial leg veins.",
        source='derived',
    ))

    Qs.append(Q(
        stem="Compare a medium-sized artery and a medium-sized vein (mention "
             "6 differences)",
        exp="1) Wall thickness: thicker relative to the lumen in the artery, "
            "thinner in the vein. 2) Lumen: smaller and rounder in the "
            "artery, wider and often irregular/collapsed in the vein. "
            "3) Tunica media: thick with abundant smooth muscle and elastic "
            "fibres in the artery, thin with little muscle in the vein. "
            "4) Internal elastic lamina: well-developed and prominent in the "
            "artery, poorly developed or absent in the vein. 5) Valves: "
            "absent in arteries, present in veins (especially of the limbs) "
            "to prevent backflow. 6) Vasa vasorum: penetrate only the outer "
            "part of the wall in the artery (the inner part is nourished "
            "directly by the high-pressure luminal blood), but penetrate the "
            "whole thickness of the wall in the vein (lower luminal pressure).",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 65-year-old man presented with chest pain not relieved by "
             "rest or nitroglycerin. After stabilisation, a thallium stress "
             "test showed reduced perfusion of the lateral wall of the left "
             "ventricle. a) Which artery is most likely occluded? b) Explain "
             "right and left coronary dominance",
        exp="a) The circumflex artery. b) Coronary dominance is defined by "
            "which coronary artery gives rise to the posterior interventricular "
            "(posterior descending) artery: in right dominance (the majority "
            "of people) the right coronary artery gives rise to it; in left "
            "dominance, the circumflex branch of the left coronary artery "
            "gives rise to it instead.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A 38-year-old man was stabbed during a fight and arrived "
             "unconscious and pale; a 2 cm wound was present in the left "
             "fifth intercostal space, 9.5 cm from the midline, penetrating "
             "skin, chest wall, pleura and pericardium. a) If excessive "
             "pericardial fluid accumulates in the pericardial space, how do "
             "you manage this, and why is this site chosen? b) Name the nerve "
             "supply of the fibrous pericardium",
        exp="a) Pericardiocentesis (needle aspiration of pericardial fluid), "
            "usually via a subxiphoid approach - this site is chosen because "
            "it avoids the pleura and the major coronary vessels while giving "
            "direct access to the pericardial sac. b) The phrenic nerve (C3-C5).",
        source='derived',
    ))

    Qs.append(Q(
        stem="Enumerate four cardiac markers used in the diagnosis of "
             "ischaemic heart disease. Which one would you order to assist in "
             "diagnosing ischaemic chest pain of about four hours' duration?",
        exp="Cardiac markers: troponin (I or T), CK-MB, myoglobin, and LDH "
            "(or AST). For chest pain of about four hours' duration, "
            "myoglobin is preferred because it is the earliest marker to "
            "rise (within 1-3 hours); troponin, already detectable by this "
            "time and highly specific, is also an appropriate choice.",
        source='derived',
    ))

    Qs.append(Q(
        stem="A patient with myocardial infarction, treated in the coronary "
             "care unit, develops chest pain again after 3 days, similar to "
             "the previous episode. Which cardiac marker would you order to "
             "help in diagnosis?",
        exp="CK-MB, because troponin remains elevated for up to 10-14 days "
            "after the original infarction and so cannot distinguish "
            "reinfarction, whereas CK-MB returns to normal within 48-72 hours "
            "and a new rise indicates reinfarction.",
        source='derived',
    ))

    Qs.append(Q(
        stem="Complete: a) the most commonly accepted mechanism of rheumatic "
             "fever is ______ between the streptococcal M protein and cardiac "
             "tissue. b) ______ is the most common causative organism of "
             "infective endocarditis in patients with prosthetic heart valves",
        exp="a) Molecular mimicry between the streptococcal M protein and "
            "cardiac (myosin) antigens. b) Staphylococcus epidermidis "
            "(coagulase-negative staphylococci).",
        source='derived',
    ))

    Qs.append(Q(
        stem="Mention one of the most important virus-specific tests for the "
             "diagnosis of viral myocarditis",
        exp="Viral-specific PCR (polymerase chain reaction) performed on "
            "endomyocardial biopsy tissue to detect the viral genome (viral "
            "serology/IgM titres is an accepted alternative).",
        source='derived',
    ))

    for q in Qs:
        q.tag = TAG_2019
        q.tag_suggere = None
        q.year = 2019
    return Qs


def build_2020():
    """'I- Complete' + 'II- Essay questions' block - fully keyed, undated in
    the OCR; assigned to 2020 by elimination (the filename names only 2019
    and 2020, and the first block is unambiguously the 2019 sitting)."""
    Qs = []

    Qs.append(Q(
        stem="Complete: 1) Genetic deficiency of lipoprotein lipase causes "
             "primary hyperlipoproteinaemia of type ______, where ______ and "
             "______ are markedly increased. 2) A 42-year-old woman diagnosed "
             "with Tangier disease has laboratory data showing a very low "
             "concentration of ______",
        exp="1) Type I; chylomicrons and VLDL are markedly increased. "
            "2) HDL (with LCAT activity also reduced), accompanied by "
            "accumulation of cholesterol in the tissues.",
        source='key',
    ))

    Qs.append(Q(
        stem="Ahmed, 66 years old, presents with severe chest pain that has "
             "gotten progressively worse over the past 8 hours. What are the "
             "best two cardiac markers that can help in diagnosis?",
        exp="Troponin, CK-MB, or myoglobin - any two of these choices are "
            "sufficient.",
        source='key',
    ))

    Qs.append(Q(
        stem="Enumerate: a) The function of endothelial cells. b) The layers "
             "of the heart wall",
        exp="a) Functions of endothelial cells: 1) They provide a smooth "
            "surface. 2) They secrete collagen, laminin, endothelin and "
            "nitric oxide. 3) They carry membrane-bound enzymes acting on "
            "bradykinin, serotonin, prostaglandins, thrombin, norepinephrine "
            "and lipoprotein lipase. b) Layers of the heart wall: the "
            "endocardium, the myocardium, and the epicardium.",
        source='key',
    ))

    Qs.append(Q(
        stem="A 55-year-old male presents with tight burning substernal chest "
             "pain; a thallium stress test shows hypoperfusion of the cardiac "
             "muscle forming the lateral surface of the right atrium. a) "
             "Which coronary artery is most likely occluded, and what is the "
             "origin of this artery? b) State the interior features of the "
             "right atrium other than the openings",
        exp="a) The right coronary artery, which arises from the anterior "
            "aortic sinus of the ascending aorta. b) The interior of the "
            "right atrium is divided into a smooth posterior part behind a "
            "ridge (the crista terminalis) and a roughened anterior part in "
            "front of the ridge, ridged by bundles of muscle (the musculi "
            "pectinati). The smooth part shows a shallow depression (the "
            "fossa ovalis) bounded superiorly by a ridge (the anulus ovalis) "
            "on the interatrial septum.",
        source='key',
    ))

    Qs.append(Q(
        stem="A 34-year-old woman took part in an exercise program; her "
             "blood pressure and heart rate were monitored before and after "
             "exercise (systolic BP rose from 110 to 145 mmHg, diastolic BP "
             "fell from 70 to 60 mmHg, heart rate rose from 75 to 130 "
             "beats/min). a) Enumerate: 1) two reasons for the increase in "
             "heart rate during exercise; 2) two local effects on skeletal "
             "muscle after exercise. b) Explain the decrease in diastolic "
             "blood pressure after isotonic exercise",
        exp="a1) Two reasons for the rise in heart rate during exercise (any "
            "two): increased body temperature, increased adrenaline "
            "secretion, signals from the right atrium (Bainbridge reflex), or "
            "signals from chemoreceptors, respiratory centres, or skeletal "
            "muscle. a2) Two local effects on skeletal muscle after exercise "
            "(any two): increased blood flow to the active muscles, increased "
            "O2 supply to the active muscles, increased formation of tissue "
            "fluid, and increased lymph formation and drainage. b) The "
            "diastolic blood pressure falls after isotonic exercise because "
            "accumulated vasodilator metabolites in the exercising muscle "
            "produce vasodilatation, reducing total peripheral resistance.",
        source='key',
    ))

    Qs.append(Q(
        stem="An 82-year-old male patient complained of several attacks of "
             "syncope (fainting); the physician noted a systolic murmur and a "
             "significantly diminished aortic component of the second heart "
             "sound. Mention the phase of the cardiac cycle during which the "
             "second heart sound is heard, and describe two events of this "
             "phase",
        exp="The isometric (isovolumic) relaxation phase, of about 0.06 sec "
            "duration. Events of this phase (any two): ventricular relaxation "
            "begins suddenly, letting intraventricular pressure fall rapidly "
            "without any change in ventricular volume; the elevated pressure "
            "in the large arteries causes sudden closure of the aortic and "
            "pulmonary valves (producing the second heart sound); atrial "
            "pressure is still increasing; all four heart valves are closed; "
            "the T wave of the ECG ends during this phase.",
        source='key',
    ))

    Qs.append(Q(
        stem="A 45-year-old presents with severe lower-limb oedema and other "
             "symptoms of right-sided heart failure; on examination he has "
             "sclerotic arteries and a blood pressure of 160/100 mmHg. a) "
             "Mention the role of normal arterial elasticity in maintaining "
             "arterial blood pressure (3 items). b) Explain the lower-limb "
             "oedema in this case, and enumerate two factors affecting "
             "capillary pressure",
        exp="a) Roles of normal arterial elasticity (any three): buffering "
            "excessive changes in arterial blood pressure; preventing a great "
            "increase in systolic pressure during systole because the aorta "
            "distends; preventing an excessive fall in diastolic pressure "
            "during diastole (maintaining a sufficiently high diastolic "
            "pressure) because the aorta recoils as its capacity decreases; "
            "converting the intermittent cardiac output into a continuous "
            "flow of blood; enhancing cardiac mechanical efficiency; and "
            "increasing coronary blood flow. b) The oedema is due to "
            "right-sided heart failure causing increased venous pressure and "
            "so increased capillary pressure, which increases the filtration "
            "force. Two factors affecting capillary pressure (any two): local "
            "regulatory mechanisms (autoregulation, vasodilator metabolites), "
            "active capillary contraction (chemical, nervous, physical or "
            "mechanical control), and extracapillary passive factors "
            "(diameter of the arterioles, venous pressure, gravity).",
        source='key',
    ))

    Qs.append(Q(
        stem="List three factors affecting venous return",
        exp="Any three of: the pressure gradient, the skeletal muscle pump, "
            "the respiratory (thoracic) pump, the diameter of the arterioles, "
            "venous tone, capillary tone, gravity, arterial pulsation, and "
            "blood volume.",
        source='key',
    ))

    for q in Qs:
        q.tag = TAG_2020
        q.tag_suggere = None
        q.year = 2020
    return Qs


def main():
    q2019 = build_2019()
    q2020 = build_2020()
    questions = q2019 + q2020

    meta = {
        'Source file': 'ASSIUT PREVIOUS EXAMS/Final Written 2019,2020.pdf',
        'Type': 'Scanned written exam, OCR at 300 dpi, 7 pages (two exam '
                'papers bound in one PDF; every page duplicated in the OCR '
                'text)',
        'Tag': 'Exams, Final 2019 / Exams, Final 2020 (per-question, see below)',
        'tagSuggere': 'None',
        'Year': 'per-question (2019 or 2020)',
        'Answer source': f'{sum(1 for q in questions if q.source == "key")} key '
                          f'(2020 block), '
                          f'{sum(1 for q in questions if q.source == "derived")} '
                          f'derived (2019 block, no printed key at all)',
    }

    n = write_md(OUT, 'Source 18 — Assiut Final Written 2019, 2020', meta, questions)

    with open(SRC_TXT, encoding='utf-8') as f:
        raw = f.read()
    answer_blocks = raw.lower().count('answer')

    print('=== Source 18: Assiut Final Written 2019, 2020 ===')
    print(f'Total questions: {n} (all written/QROC; 0 MCQ)')
    print(f'  2019 block (Part II Short Questions, 11/12/2019): {len(q2019)} '
          f'questions, all derived (paper prints no key at all for this '
          f'section)')
    print(f'  2020 block ("I- Complete" + "II- Essay questions", undated in '
          f'the OCR, assigned by elimination): {len(q2020)} questions, all key')
    print('Completeness counters:')
    print('  highest question number in source: 13 (2019 block, "Part II: '
          'Short questions (13 questions...)" printed explicitly in the '
          'header) + roman-numeral/unnumbered sections in the 2020 block '
          '(1 complete-the-blank item bundling 2 sub-blanks + 7 essay '
          f'questions = 8) -> {n} emitted after continuous renumbering')
    print(f'  raw occurrences of the word "answer" in the OCR text (both '
          f'duplicated page copies): {answer_blocks}')
    print(f'  ### Q headings written to markdown: {n}')
    print('Exclusions: none - every question in both blocks has a legible '
          'stem; the 2019 block simply has no printed key anywhere, so all '
          '13 of its questions are marked derived rather than excluded.')
    print('Note: the header states "Part II: Short questions", implying a '
          'Part I (likely MCQs) existed in the original PDF but was not '
          'captured by this OCR pass - nothing from a Part I is present in '
          '.ocr/18_final_written_2019_2020.txt to extract.')
    print('Note: the 2019 block (13 questions) closely parallels the '
          'standalone source 17 (Markdown_Questions/17_Assiut_Final_Exam_2019.md) '
          '- both are the same 11/12/2019 sitting; the Stage-4 compiler\'s '
          'stem-based dedup is expected to merge duplicate questions between '
          'the two files.')


if __name__ == '__main__':
    main()
