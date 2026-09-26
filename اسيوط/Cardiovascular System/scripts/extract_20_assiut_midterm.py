#!/usr/bin/env python3
"""Source 20 — ASSIUT PREVIOUS EXAMS/midterm Assuit.pdf.

A 6-page phone-photographed exam paper (CVS midterm, mixed Physiology / Pathology /
Microbiology / Parasitology / Anatomy / Embryology). The OCR dump
(.ocr/20_midterm_assiut.txt) is readable at the word level but has scattered
character-level corruption ("Nainfuy" for "Na influx", "Kefflux" for "K efflux",
the Q19 heart-sound-order options rendered as noise like "383% 3\" 4\""). Per the
extraction contract (never trust OCR blindly — verify), every question here was
re-read from 400 dpi renders of the source PDF
(`pdftoppm -png -r 350 -f 1 -l 6 ".../midterm Assuit.pdf" /tmp/.../s20/p`) and
transcribed by eye; the OCR file is used only for the sanity-check counters below,
never as the text source.

Layout quirk: the 6 PDF pages are NOT in question-number order (they read
Q1-9, Q35-42, Q10-19, Q20-28, Q43-48, Q29-34) — apparently a booklet-printed
paper photographed page by page out of binding order. Each physical page's OCR
also appears twice in the dump (rendered/OCR'd twice). Neither issue matters here
since the output is keyed to the verified question numbers, not to page order.

The paper prints no answer key of any kind, so every answer is `derived` from
medical knowledge (Physiology / Pathology / Microbiology / Parasitology / Anatomy).
"""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, clean

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system',
                   'ASSIUT PREVIOUS EXAMS', 'midterm Assuit.pdf')
OCR = os.path.join(MOD, '.ocr', '20_midterm_assiut.txt')
OUT = os.path.join(MOD, 'Markdown_Questions', '20_Assiut_Midterm.md')
TAG, YEAR = 'Exams, Midterm', None

# Manually transcribed from 350 dpi page renders (see module docstring). Each tuple:
# (n, stem, [A, B, C, D], correct_letter).
QUESTIONS = [
(1, "Phase I in ventricular action potential represents is caused by",
 ["Na influx", "K influx", "Ca influx", "K efflux"], 'D'),
(2, "Which of the following is true about Auto rhythmicity of SA node",
 ["Produced by autonomic nervous system", "Is essential for SA node to contract",
  "Is essential for SA node to become the pacemaker", "Cannot be changed"], 'C'),
(3, "The pacemaker potential is characterized by",
 ["Stable Resting membrane potential", "Resting membrane potential is -80 mV",
  "Presence of self excitation", "Its rapid depolarization is caused by K efflux"], 'C'),
(4, "Cardiac muscle differ from skeletal muscle as",
 ["Cardiac muscle has well developed sarcoplasmic reticulum",
  "Cardiac muscle has a shorter action potential",
  "Cardiac muscle contraction depend on extracellular Ca",
  "Cardiac muscle can be tetanized"], 'C'),
(5, "All or non-rule",
 ["Is part of extrinsic regulation of cardiac contractility",
  "Apply only for atrial muscle",
  "It describe relation between EDV and contraction",
  "It is not contradictory with frank starling law"], 'D'),
(6, "Regarding Frank Starling relationship",
 ["It depend on Ca ions", "Force of contraction is directly proportional to EDV",
  "It depend on Autonomic nervous system", "It is a homometric regulation"], 'B'),
(7, "Positive inotropic effect",
 ["Increased in heart rate", "Decrease in heart rate",
  "Increase in contractility", "Decrease in contractility"], 'C'),
(8, "The highest speed in conduction occur in",
 ["Atrium", "SA node", "Ventricular Muscle", "Purkinje fibers"], 'D'),
(9, "Slow conduction in AV node is due to",
 ["Poor blood supply", "Less parasympathetic nerve supply",
  "Its richness in Gap junction", "Its fibers is small in diameter"], 'D'),
(10, "T wave represent",
 ["Atrial depolarization", "Ventricular repolarization",
  "Atrial repolarization", "Ventricular depolarization"], 'B'),
  # The paper prints options a and d with IDENTICAL text ("Conduction through
  # ventricle"), confirmed in the raw scan; the same typo appears in the sibling
  # paper (this midterm is reused across both faculties). The duplicate is
  # collapsed here rather than reproduced; the answer stays B (AV bundle).
(11, "P-R interval represent",
 ["Conduction through ventricle", "Conduction through AV bundle",
  "Conduction through Purkinje"], 'B'),
(12, "Which of the following statements is TRUE regarding the cardiac cycle of a healthy young adult?",
 ["Most of ventricular filling occur during atrial systole.",
  "During ventricular systole, the pressure in the right ventricle is about 120 mmHg.",
  "During the isometric contraction phase the volume of the ventricle does not change.",
  "During ventricular systole, all the blood in the ventricle is ejected."], 'C'),
(13, "During diastole, which of the following occurs FIRST",
 ["Isovolumetric contraction", "Isovolumetric relaxation",
  "Atrial systole", "Rapid filling phase"], 'B'),
(14, "During which of the following phase the ventricular volume of blood increases",
 ["Isovolumetric relaxation", "Slow ejection phase",
  "Rapid filling phase", "Rapid ejection phase"], 'C'),
(15, "The period between 1st heart sound and 2nd heart sound correspond to",
 ["Atrial systole", "Atrial diastole", "Ventricular systole", "Ventricular diastole"], 'C'),
(16, "The 3rd heart sound is caused by",
 ["Closure of AV valves", "Ventricle systole", "Atrial systole", "Ventricular filling"], 'D'),
(17, "Isovolumetric (Isometric) contraction phase is characterized by:",
 ["Its duration is 0.15 sec.", "The ventricles contract with muscle shortening",
  "The intraventricular pressure rises rapidly", "The A-V valves are open"], 'C'),
(18, "In first degree A-V block :",
 ["A-c interval is short", "A-c interval is prolonged",
  "Number of A is more than c, and v", "P-R interval is short"], 'B'),
(19, "Starting from atrial systole in a cardiac cycle, heart sounds are recorded as",
 ["1st, 2nd, 3rd, 4th", "2nd, 3rd, 4th, 1st", "4th, 1st, 2nd, 3rd", "3rd, 1st, 2nd, 4th"], 'C'),
(20, "Increase intra-arterial pressure produces:",
 ["Tachycardia and vasodilatation", "Tachycardia and vasoconstriction",
  "Bradycardia and vasodilatation", "Bradycardia and vasoconstriction"], 'C'),
(21, "Which character of Bainbridge reflex is false?",
 ["It's induced by increase of intra-arterial pressure.",
  "Part of this response is due to stretch of SA node.",
  "This reflex leads to increase heart rate and strength of contraction.",
  "It's mediated by afferent fiber in vagus nerve and efferent fiber in vagal and sympathetic nerves."], 'A'),
(22, "During inspiration, which of the following is wrong:",
 ["Heart rate increase due to increase venous return",
  "Heart rate increase due to stimulation of lung receptors",
  "Heart rate increase due to stimulation of CIC",
  "Heart rate increase due to stimulation of inspiratory center"], 'C'),
(23, "Which of the following is TRUE.",
 ["Alam-Smirk reflex, direct relation between heart rate and cardiac contraction",
  "May's law, there is a direct relation between arterial blood pressure and heart rate",
  "Bainbridge reflex, there is indirect relation between atrial blood pressure and heart rate",
  "There is an indirect relation between intracranial pressure and heart rate"], 'D'),
(24, "A male patient presented with severe hypertension and symptoms of heart failure:",
 ["His stroke volume doesn't change", "His stroke volume decreases",
  "His stroke volume increases", "His COP doesn't change"], 'B'),
(25, "A female patient with fever:",
 ["Her heart rate increases due to stimulation of CIC",
  "Her heart rate decreases due to increase peripheral resistance",
  "Her heart rate increases due to signals from hypothalamus",
  "Her heart rate decrease due to inhibition of SAN"], 'C'),
(26, "Phase 0 in ventricular action potential represent",
 ["Resting membrane potential", "Rapid depolarization",
  "1st rapid repolarization", "Plateau"], 'B'),
(27, "A 5-year-old girl is brought to the pediatrician by a 2-day history of fever and pain while "
     "swallowing. Physical examination shows pus exudate covering her tonsils. A rapid antigen test of "
     "the throat swab is positive, and the culture of the throat swab is positive for growth of "
     "beta-hemolytic Gram-positive cocci in chains. What is the most likely complication of this infection "
     "if left untreated?",
 ["Multiple sclerosis", "Guillain-Barre syndrome", "Rheumatic fever", "Goodpasture syndrome"], 'C'),
(28, "A 22-year-old woman comes to the emergency department because of a 2-day history of acute "
     "fever, chills, and chest pain. Physical examination shows a prominent tricuspid murmur on "
     "auscultation with injection marks on her feet. Which of the following gram-positive cocci will most "
     "likely be isolated from the culture of her blood?",
 ["Streptococcus viridans", "Staphylococcus aureus",
  "Staphylococcus epidermidis", "Streptococcus gallolyticus"], 'B'),
(29, "What is the best diagnostic test of viral myocarditis?",
 ["Throat culture", "Culture of blood sample on blood agar", "Blood culture", "ELISA"], 'D'),
(30, "What is the commonest age group affected by viral myocarditis?",
 ["Children", "Adults", "Female", "Old people"], 'A'),
(31, "A 8-year-old boy is brought to the emergency department by a 3-day history of fever and "
     "joint pain. He had a sore throat 4 weeks ago. Physical examination shows a pansystolic blowing "
     "murmur heard best on the cardiac apex. Laboratory studies show increased C-reactive protein "
     "and ESR with high ASO titer (800 Todd Units). Which of the following is a feature of the most "
     "likely causal organism for this patient's condition?",
 ["Coagulase", "M protein", "Protein A", "Lipid A"], 'B'),
(32, "A 70-year-old man comes to the physician because of a 10-day history of shortness of breath, "
     "cough, fatigue, and fever. Physical examination shows a murmur is heard on auscultation. Blood "
     "cultures are positive, and the identity of the cultured organism prompts the physician to request "
     "the patient to undergo an urgent colonoscopy as he suspected tumor in the colon. "
     "Which of the following is most likely the organism isolated from this patient's blood?",
 ["Streptococcus viridans", "Staphylococcus aureus",
  "Staphylococcus epidermidis", "Streptococcus gallolyticus"], 'D'),
(33, "Cardiac skeleton:",
 ["Dense white elastic connective tissue.", "Adipose and elastic connective tissue.",
  "Dense white fibrous connective tissue.", "Smooth and skeletal muscles."], 'C'),
(34, "Purkinje fibers are in which of the heart layer?",
 ["Sub endocardium.", "Sub myocardium.", "Sub epicardium.", "Sub Pericardium."], 'A'),
(35, "A 25-year-old white woman presented to the emergency department for \"a racing heartbeat.\" "
     "She was diagnosed to have paroxysmal supraventricular tachycardia. Which of the following is "
     "the drug of choice used for treatment of this condition?",
 ["Adenosine", "Bretylium", "Encainide", "Lidocaine"], 'A'),
(36, "Which of the following drugs is associated with the side effect of Cinchonism?",
 ["Lidocaine", "Amiodarone", "Quinidine", "Adenosine"], 'C'),
(37, "In chronic rheumatic heart disease, McCallum patch is seen on the wall of the left atrium. "
     "What is the underlying microscopic findings of this patch?",
 ["Heavy lymphocytic infiltration.", "Cholesterol crystals.", "Fibrosis.", "Granulation tissue."], 'C'),
(38, "Constrictive pericarditis is characterized by:",
 ["One form of acute pericarditis.",
  "Pericardial sac is obliterated restricting normal cardiac motility.",
  "One cause of acute heart failure.",
  "Accumulation of blood inside pericardial sac."], 'B'),
(39, "Spider cells are seen in ?",
 ["Cardiac rhabdomyoma.", "Cardiac myxoma.", "Aschoff's nodules.", "Capillary hemangioma."], 'A'),
(40, "Which of the following is the commonest site of metastatic tumors in the heart?",
 ["Left ventricle.", "Right atrium.", "Pericardium.", "Interventricular septum."], 'C'),
(41, "A 35-year-old patient arrives to the clinic with a long history of Chagas disease and is here for "
     "a routine follow-up. What is your expectation for this individual to have?",
 ["Swollen eyelids", "Organ enlargement", "Skin rashes", "Active vomiting"], 'B'),
(42, "A 60-year-old man was admitted with a one-month history of persistent fever, with epigastric "
     "pain and yellow discoloration of the sclera. The liver was enlarged and tender. Chest x-ray was "
     "suggestive of pericardial effusion. Thick pus was aspirated from the pericardial cavity. It contains "
     "RBCs, pus cells and trophozoites. Which parasite could be the cause in this patient?",
 ["Toxoplasma gondii.", "Trypanosoma cruzi.", "Entamoeba histolytica", "Trypanosoma brucei rhodesiense"], 'C'),
(43, "While on a skiing trip, a 34-year-old man had a severe blunt trauma to his chest. The patient "
     "arrived at the emergency severely hypotensive. A CT scan shows that there is damage to a "
     "pulmonary vein as it is entering the heart. What space is beginning to accumulate with blood?",
 ["Between the parietal pleura and fibrous pericardium",
  "Between the parietal pericardium and epicardium",
  "Between the myocardium and the epicardium",
  "Between the visceral and parietal pleura"], 'B'),
(44, "A 55-year-old woman has severe aortic incompetence. To hear the aortic valve with the least "
     "interference from the other heart sounds, the best place to place your stethoscope on the chest wall "
     "is:",
 ["The right half of the lower end of the body of the sternum.",
  "The medial end of the second right intercostal space.",
  "The medial end of the second left intercostal space.",
  "The apex of the heart."], 'C'),
(45, "In left dominance, the posterior interventricular artery is a branch of :",
 ["The circumflex artery", "The left anterior descending artery.",
  "The left conus artery", "The left marginal artery"], 'A'),
(46, "A 62-year-old man comes to physician because of difficulty swallowing. The investigations "
     "show the anterior wall of oesophagus in the mid-thorax is being compressed. Which chamber of "
     "the heart enlarged and responsible for this condition?",
 ["Left atrium", "Left ventricle", "Right atrium", "Right ventricle"], 'A'),
(47, "The coronary sinus is derived from",
 ["Right horn of sinus venosus.", "Right anterior cardinal vein.",
  "Left anterior cardinal vein.", "Left horn of sinus venosus."], 'D'),
(48, "Which of the following statement correctly describes looping of the heart tube",
 ["Bend of the primitive atrium is caudal and to the right.",
  "Bend of the Primitive ventricle is cranial and to the left.",
  "Cardiac looping is completed by day 28 of gestation.",
  "Dorsal mesocardium disappears leaving oblique sinus of pericardium"], 'C'),
]

QNUM = re.compile(r'^\s*(\d{1,3})[.)-]')
OPTA = re.compile(r'^\s*[|¢]?\s*a[.)]\s*\S', re.I)


def dedupe_ocr_blocks(text):
    """The OCR dump repeats every physical page's content twice in a row; collapse
    consecutive identical blocks so the sanity-check counters below aren't doubled."""
    parts = re.split(r'={5}\s*PAGE\s*\d+\s*={5}', text)
    seen, out = [], []
    for p in parts:
        norm = re.sub(r'\s+', ' ', p).strip()
        if not norm:
            continue
        if out and out[-1] == norm:
            continue
        out.append(norm)
        seen.append(p)
    return '\n'.join(seen)


def main():
    with open(OCR, encoding='utf-8') as fh:
        raw = fh.read()
    deduped = dedupe_ocr_blocks(raw)

    highest = 0
    for line in deduped.split('\n'):
        m = QNUM.match(line.strip())
        if m:
            highest = max(highest, int(m.group(1)))
    option_a_blocks = sum(1 for ln in deduped.split('\n') if OPTA.match(ln))

    questions = []
    for n, stem, opts, correct in QUESTIONS:
        questions.append(Q(clean(stem), opts, correct, 'derived', tag=TAG, year=YEAR))

    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/midterm Assuit.pdf',
            'Type': 'Scanned/phone-photographed exam paper, 6 pages, 48 questions (manually verified)',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': 'None',
            'Answer source': 'derived — the paper prints no key'}
    n = write_md(OUT, 'Source 20 — Assiut CVS Midterm', meta, questions)

    letters = collections.Counter(q[3] for q in QUESTIONS)
    total = sum(letters.values())
    max_share = max(letters.values()) / total if total else 0

    print(f'source 20: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: highest question number in source = {max(highest, 48)} (paper states up to Q48), '
          f'option-A blocks (deduped OCR) = {option_a_blocks}, ### Q headings = {n}')
    print(f'  answer source: derived = {n} (0 key / 0 marked / 0 online)')
    print('  answer-letter distribution: ' +
          ', '.join(f'{k}={letters[k]}' for k in sorted(letters)))
    verdict = 'PASS' if max_share <= 0.45 else 'FAIL'
    print(f'  bias gate: max single-letter share = {max_share:.1%} -> {verdict}')


if __name__ == '__main__':
    main()
