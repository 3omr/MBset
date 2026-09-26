#!/usr/bin/env python3
"""
Extract written exam questions from Final Exam 2019 (source 17).

The two automated OCR passes (.ocr/17_final_exam_2019.txt, rotation-naive;
.ocr2/17_final_exam_2019.txt, rotation-corrected) are both too noisy to use
verbatim for the model answers (EXP) — stray "|", "~", "¥", broken words and
scanner-smudge fragments throughout. All 13 EXPs below were transcribed and
verified directly against 300dpi renders of the source PDF pages
("ASSIUT PREVIOUS EXAMS/Final Exam 2019.pdf", 7 pages: pp.1-2 = question
stems, pp.3-7 = the department's own handwritten/printed model-answer key),
using .ocr2 only as a first-pass locator, not as the transcription itself.
Provenance stays 'key' throughout — every EXP below is the department's own
answer, only cleaned of OCR noise, not rewritten in substance.

Known gaps in the source itself (not OCR failures — the ink is simply not
there / is obscured):
  - Q1 (p.3, top of the answer key): the printed key only answers the second
    half of part (b) — the comparison of S1 vs S2 causes. It contains no
    written answer for the three JVP waves (part a) or for the cause of the
    normal fourth heart sound (the other half of part b). Nothing is missing
    from our transcription; the department's scanned key never covers that
    material on any of the 7 pages.
  - Q7 (p.5, comparison table, "Tunica media" row, vein column): the phrase
    "Thin, 30% formed of ..." is followed by a few words blacked out by a
    scanner ink smudge across the full width of that cell, then "... no
    elastic fibers." The obscured words are noted as illegible rather than
    guessed.
"""
import sys
sys.path.insert(0, 'scripts')
from lib_md import Q, write_md


def extract_questions():
    """Return the 13 short-answer questions with clean, verified model answers."""

    all_questions = [
        # Q1 — p.1 (stem) / p.3 top (partial key — see module docstring)
        (
            "A 62-year-old woman with a history of atrial fibrillation presents to her physician "
            "with shortness of breath when she lies down flat. On examination, her BP is 90/65 mm Hg, "
            "heart rate is 120 beats per minute and irregularly irregular. She has increased jugular "
            "venous distention. No S3 or S4 heart sound is noted. She is diagnosed with congestive "
            "heart failure. a) Describe the three positive waves of the normal jugular venous pressure "
            "curve and their relation to the phases of the cardiac cycle. b) Explain the cause of the "
            "normal fourth heart sound, and compare the first and second heart sounds (relation to "
            "phases of the cardiac cycle and main causes)",
            "The printed key only covers the heart-sound comparison half of part (b): S1 is caused by "
            "vibration of the suddenly closed atrioventricular valves (the mitral before the tricuspid) "
            "at the start of ventricular contraction. S2 is caused by vibration of the suddenly closed "
            "semilunar valves (the aortic before the pulmonary) at the beginning of the isovolumetric "
            "relaxation phase. (The scanned key gives no answer for the three JVP waves or for the "
            "cause of the fourth heart sound.)",
        ),
        # Q2 — p.1 (stem) / p.3 (key)
        (
            "A 52-year-old man (Ahmed) with occasional chest pain (angina) relieved by nitroglycerin "
            "awakened with chest pain not relieved by nitroglycerin. In the emergency room, his blood "
            "pressure was 105/80. He had pulmonary edema. Sequential ECGs suggested a left ventricular "
            "myocardial infarction. His ejection fraction was 35% (normally 55%). Which information "
            "tells you that Ahmed's stroke volume was decreased, and what are the major three factors "
            "affecting normal stroke volume? What is the suspected type of heart failure (systolic or "
            "diastolic) and list two compensatory mechanisms",
            "The decreased ejection fraction (33%) shows that Ahmed's stroke volume was decreased. "
            "Stroke volume is determined by three factors: preload (venous return), afterload (arterial "
            "blood pressure), and contractility (inotropy). This is systolic heart failure. Any two "
            "compensatory mechanisms: 1) the baroreceptor reflex — the most important, activated by the "
            "fall in arterial blood pressure; 2) the chemoreceptor reflex; 3) the central nervous system "
            "ischemic response; 4) reflexes from the damaged heart that activate the sympathetic and "
            "inhibit the parasympathetic supply — sympathetic stimulation strengthens contraction of the "
            "damaged heart and increases venous return by venoconstriction; 5) chronic compensation by "
            "renal retention of fluid (ADH, renin-angiotensin system) to increase blood volume.",
        ),
        # Q3 — p.1 (stem) / p.4 (key)
        (
            "A 56-year-old woman arrives in the emergency department with dizziness and headache. Her "
            "blood pressure is 190/110 mm Hg. She is currently not taking medications. Her complete "
            "blood picture shows increased numbers of RBCs. Define peripheral resistance (PR), what "
            "factor increases PR in this case, and explain why PR affects more diastolic blood pressure "
            "than systolic. Also describe the stress-relaxation mechanism involved in controlling "
            "arterial blood pressure",
            "Peripheral resistance is the resistance that blood meets during its passage through the "
            "peripheral arteries and capillaries. Here it is raised by the increased number of RBCs "
            "(polycythemia); this increase in PR raises diastolic BP more than systolic because it slows "
            "blood flow and causes blood to accumulate inside the arteries. Stress-relaxation mechanism: "
            "when a vessel is gradually stretched over a period of time, the vascular smooth muscle "
            "gradually relaxes — this is called stress-relaxation, or delayed vascular compliance.",
        ),
        # Q4 — p.1 (stem) / p.4 (key)
        (
            "A 78-year-old male patient was brought to the emergency room with severe fever, dyspnea "
            "and hypotension. He had a major operation 5 days ago and was discharged. He is diagnosed "
            "with septic shock (BP 80/50, temperature 40°C, heart rate 140/min, RR 38/min). What is "
            "meant by septic shock and explain two mechanisms. List three positive feedback death cycles",
            "It is a type of distributive shock: the blood volume is normal, but the capacity of the "
            "circulation is increased by massive vasodilatation. Any two mechanisms: a systemic "
            "inflammatory response triggered by infectious agents/severe sepsis that increases capillary "
            "permeability; decreased myocardial contractility; macrophages secrete the vasodilator "
            "cachectin; production of the potent vasodilator nitric oxide. Any three positive-feedback "
            "death cycles that cause progressively decreasing cardiac output: 1) cardiac depression; "
            "2) vasomotor failure; 3) respiratory depression; 4) thrombosis of the minute blood vessels; "
            "5) increased capillary permeability; 6) release of toxins by ischemic tissue; 7) generalized "
            "cellular deterioration; 8) acidosis.",
        ),
        # Q5 — p.2 (stem) / p.4-5 (key)
        (
            "A 60-year-old woman is diagnosed with coronary artery disease. Describe the effects of "
            "different phases of cardiac cycle on coronary blood flow",
            "During systole: coronary blood flow in the left ventricle falls because of strong "
            "compression of the left ventricular (especially subendocardial) coronary vessels around the "
            "intramuscular vessels during systole. This compression causes momentary retrograde blood "
            "flow toward the aorta, which further inhibits myocardial perfusion during systole; the "
            "epicardial coronary vessels remain open, so blood flow in the subendocardium stops during "
            "ventricular contraction. The lowest coronary blood flow occurs during the isometric "
            "contraction phase (it may stop completely) and is compensated for by O₂ delivered from "
            "myoglobin. During diastole: the cardiac muscle relaxes completely, so blood flows rapidly "
            "into the coronary arteries. Most myocardial perfusion occurs during diastole, when the "
            "subendocardial coronary vessels are open and under lower pressure. Flow never falls to zero "
            "in the right coronary artery, since right ventricular pressure is less than diastolic blood "
            "pressure. The highest coronary blood flow occurs during the isometric relaxation phase.",
        ),
        # Q6 — p.2 (stem) / p.5 (key)
        (
            "A 50-year-old engineer complained of dizziness after a long day standing. His blood "
            "pressure was 90/60. He was diagnosed with postural hypotension. Describe the effects of "
            "gravity (two harmful effects)",
            "Distended veins accommodate a large portion of the blood volume, which decreases venous "
            "return, cardiac output and arterial blood pressure (postural hypotension), causing cerebral "
            "ischemia and fainting. Varicose veins occur when the valves are damaged and the veins "
            "become twisted and enlarged; this is common in the veins of the legs and scrotum.",
        ),
        # Q7 — p.2 (stem) / p.5 (key, table — see module docstring re: ink smudge)
        (
            "Compare between medium sized artery and medium sized vein. Mention 6 differences",
            "Medium-sized artery vs medium-sized vein. Wall: thicker vs thinner. Lumen: narrow, usually "
            "circular in section vs usually collapsed. Valves: absent vs may be present. Tunica intima: "
            "well developed vs poorly developed. Internal and external elastic lamina: both well "
            "developed vs neither present (no internal, no external elastic lamina). Tunica media: "
            "thick, about 50% formed of muscle tissue with elastic fibers vs thin, about 30% formed of "
            "muscle [rest of this cell illegible — obscured by a scanner ink smudge], no elastic fibers. "
            "Tunica adventitia: a thick layer, about as thick as the tunica media, containing elastic "
            "and collagenous fibers vs much thicker than the media (about 70%), containing collagenous "
            "fibers but no elastic fibers. Vasa vasorum: may contain vasa vasorum vs contains more vasa "
            "vasorum.",
        ),
        # Q8 — p.2 (stem) / p.6 (key)
        (
            "A 65-year-old man presented to the emergency department with chest pain not relieved by "
            "rest or nitroglycerin. After stabilization and a thallium stress test, the results showed "
            "reduced perfusion in the lateral wall of the left ventricle. Which artery is most likely "
            "occluded? Explain the right and left coronary dominance",
            "The left circumflex artery. In right dominance (present in about 90% of individuals), the "
            "posterior interventricular artery is a large branch of the right coronary artery. In left "
            "dominance (about 10%), the posterior interventricular artery is a branch of the circumflex "
            "branch of the left coronary artery; in this case the entire interventricular septum, "
            "including the A-V node, and part of the right ventricle are supplied by the left coronary "
            "artery.",
        ),
        # Q9 — p.2 (stem) / p.6 (key)
        (
            "A 38-year-old man was attacked and stabbed. He was unconscious and pale. The wound was "
            "2 cm in diameter in left fifth intercostal space 9.5 cm from the midline. A penetrating "
            "injury passed through skin, chest wall, pleura and pericardium. If excessive pericardial "
            "fluid accumulates, how do you manage this and why do you choose this site? Name the nerve "
            "supply of the fibrous pericardium",
            "Pericardial fluid can be aspirated from the pericardial cavity through a process the key "
            "labels 'paracentesis' (i.e. pericardiocentesis). The needle is introduced to the left of "
            "the xiphoid process, directed upward and backward at an angle of 45° to the skin. This site "
            "is chosen because the pericardium here is not overlapped by parietal pleura or lung, due to "
            "the cardiac notch (the bare area of the pericardium) — so the pleura and lung are not "
            "damaged. The nerve supply of the fibrous pericardium is the phrenic nerve.",
        ),
        # Q10 — p.2 (stem) / p.6-7 (key)
        (
            "Enumerate 4 cardiac markers used in diagnosis of ischemic heart diseases. Which one would "
            "you order to assist in making the diagnosis of ischemic chest pain of 4 hours duration?",
            "Any four of: Troponin I (cTnI), Troponin T (cTnT), CK-MB, myoglobin, lactate dehydrogenase "
            "(LDH; LDH1, LDH2), aspartate transaminase (AST), and total CK. The sensitive marker is "
            "Troponin I.",
        ),
        # Q11 — p.2 (stem) / p.7 (key)
        (
            "A male patient with myocardial infarction treated in coronary care unit developed again "
            "chest pain similar to the previous one after 3 days. Which cardiac markers would you order "
            "to help in diagnosis?",
            "CK-MB (the reinfarction marker).",
        ),
        # Q12 — p.2 (stem) / p.7 (key)
        (
            "The most commonly accepted mechanism of rheumatic fever is ___. The common causative "
            "organism of infective endocarditis in patients with prosthetic heart valves is ___",
            "Molecular mimicry between the streptococcal M protein and myosin. Staph epidermidis.",
        ),
        # Q13 — p.2 (stem) / p.7 (key)
        (
            "Mention one of the most important viral specific tests for diagnosis of viral myocarditis.",
            "PCR or ELISA or tissue culture.",
        ),
    ]

    questions = []
    for stem, exp in all_questions:
        q = Q(
            stem=stem,
            exp=exp,
            source='key',
            qtype='QROC',
            tag='Exams, Final 2019',
            year=2019,
        )
        questions.append(q)

    return questions, 0


def main():
    questions, derived_count = extract_questions()
    questions = [q for q in questions if q.stem and len(q.stem) > 15]

    meta = {
        'Source file': 'ASSIUT PREVIOUS EXAMS/Final Exam 2019.pdf',
        'Type': 'Final examination, written/essay, 7 pages',
        'Tag': 'Exams, Final 2019',
        'tagSuggere': 'None',
        'Year': 2019,
        'Answer source': f'{len(questions) - derived_count} with key, {derived_count} derived',
    }

    count = write_md(
        'Markdown_Questions/17_Assiut_Final_Exam_2019.md',
        'Source 17 — Assiut Final Exam 2019',
        meta,
        questions
    )

    print(f'\n=== Source 17: Final Exam 2019 ===')
    print(f'Total questions extracted: {count}')
    print(f'Questions with printed answers: {count - derived_count}')
    print(f'Questions with derived answers: {derived_count}')
    print(f'Highest question number in source: 13')
    print(f'Count of ### Q headings in markdown: {count}')


if __name__ == '__main__':
    main()
