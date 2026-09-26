#!/usr/bin/env python3
"""Source 23 — OTHER EXAMS/sohag final 2021.pdf.

A scanned (photographed, not CamScanner-cropped) exam paper: "CVS-206 -
Final-block Exam, Summer Course - Second Year", 22/9/2021, declaring 11
printed pages and 96 questions in its header table.

Only 9 images actually got scanned into this PDF, and two of the paper's own
pages are simply absent from the file (not damaged — never photographed):
printed page 2 (questions 10-18) and printed page 5 (questions 37-45). Those
18 questions cannot be recovered from this source at all and are logged as
EXCLUDED. Question 19's stem also straddles the missing page 2 / present
page 3 boundary — only its last line ("...atrial fibrillation, ONE of the
following drugs must be used:") survived, so it is EXCLUDED too rather than
guessing the missing clinical scenario; note that 25 and 28 are believed to
be rescans of this same Sohag 2021 final/midterm pair, so full stems may be
recoverable from a sibling source.

Answers are hand-marked on the paper: the *correct* option is highlighted in
yellow (sometimes with a checkmark stroke through the letter too). A plain
diagonal slash/X through a letter with no yellow is the student's own
elimination scratch on a wrong option, not a positive mark, so it is ignored.
Four questions (51, 75, 78, 82) carry only such scratches and no highlighted
option at all; their answers are 'derived' from standard physiology/anatomy
teaching and counted separately.

All questions and options were transcribed directly from the rendered page
images (300 dpi) rather than parsed from OCR text — the photographed pages
have wood-grain backgrounds, skew and finger/thumb intrusions that make a
regex-over-OCR approach unreliable for a mixed a)/A. marker paper like this.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/sohag final 2021.pdf'
OUT = os.path.join(MOD, 'Markdown_Questions', '23_Sohag_Final_2021.md')
TAG, YEAR = 'External, Sohag 2021', 2021

# (qnum, stem, [options], correct_letter, source) — source is 'marked' unless
# noted 'derived' for the four questions with no highlighted option.
DATA = [
(1, "Regarding aorta it is characterized by:",
 ["Rich in collagen fibers that act as secondary heart",
  "Large muscular or distributing artery",
  "The tunica media contains fenestrated elastic laminae and smooth muscles",
  "Tunica intima is separated from media by thick internal elastic lamina"], 'C', 'marked'),
(2, "Medium sized veins are characterized by:",
 ["The tunica adventitia is very thin.", "Prominent internal elastic lamina.",
  "Contain valves.", "Regulate the amount of blood entering a particular organ."], 'C', 'marked'),
(3, "Which layer contains cardiac muscle fibers?",
 ["Perimysium", "Myocardium", "Endocardium", "Heart valves", "Epicardium"], 'B', 'marked'),
(4, "The cell lining of the internal surface of the blood vessel is:",
 ["Smooth muscle", "Fibroblast", "Pericyte", "Endothelial"], 'D', 'marked'),
(5, "Vasa vasorum:",
 ["Lymph nodes", "Valves", "Small nerve fibers", "Elastic arteries",
  "Present in the adventitia of large blood vessels"], 'E', 'marked'),
(6, "Coronary blood vessels located at which layer?",
 ["Epicardium", "Myocardium", "Endocardium", "Sub-endocardium"], 'A', 'marked'),
(7, "Which of the following are irregular spaces found specifically in the liver, spleen, "
    "and bone marrow?",
 ["Continuous capillaries", "Fenestrated capillaries", "Sinusoidal capillaries",
  "AV anastomoses"], 'C', 'marked'),
(8, "The Fenestrated Capillaries:",
 ["Visceral capillaries contain fenestrae", "Present in the intestine, choroid and kidney.",
  "Irregular spaces between the epithelial components of liver", 'Both "a & b"'], 'D', 'marked'),
(9, "All the following parasites affect cardiac muscle except:",
 ["Toxoplasma gondii", "Trypanosoma cruzi", "Trichinella spiralis", "Taenia saginata"],
 'D', 'marked'),
# Q10-18 (printed page 2) and Q37-45 (printed page 5) are missing from the scan entirely.
# Q19's stem straddled the missing page 2 / surviving page 3 boundary and is unrecoverable.
(20, "Which ONE of the following drugs is used in the management of congestive heart failure:",
 ["Propranolol.", "Verapamil.", "Captopril.", "Nifedipine."], 'C', 'marked'),
(21, "One of the following drugs reduces preload in a patient with congestive heart failure:",
 ["Nitroglycerine.", "Digoxin.", "Carvedilol.", "Dopamine."], 'A', 'marked'),
(22, "Particularly effective in suppressing ventricular arrhythmias associated with "
     "myocardial infarction:",
 ["Lidocaine", "Quinidine", "Flecainide", "Atropine"], 'A', 'marked'),
(23, "What is the major mechanism of action of class III antiarrhythmic agents?",
 ["Inhibition of sodium influx", "Inhibition of L-type calcium channels",
  "Inhibition of potassium channels", "Inhibition of sodium-potassium ATPase"], 'C', 'marked'),
(24, "Select one of the drugs that is not useful in cardiac arrhythmias.",
 ["Digoxin", "Nifedipine", "Magnesium sulfate", "Adenosine"], 'C', 'marked'),
(25, "Statins cannot be used in combination with fibrates as both drugs increase the risk of:",
 ["Myopathy.", "Hepatotoxicity.", "Gout.", "Hyperglycemia."], 'A', 'marked'),
(26, "Mechanism of action of ezetimibe is:-",
 ["Inhibits HMG-Co reductase.", "binds to NPC1L1 protein on the GIT epithelium.",
  "activates PPARS which regulate gene transcription.",
  "prevents reabsorption of bile acids."], 'B', 'marked'),
(27, "The following statements are correct about atorvastatin except:",
 ["inhibit HMG-CoA enzyme", "may induce hepatotoxicity and myopathy.",
  "monitoring liver and muscle enzyme is recommended during therapy.",
  "inhibit bile acids absorption."], 'D', 'marked'),
(28, "Patients receiving thiazides must receive a diet rich in:",
 ["Sodium", "Potassium.", "Calcium.", "Magnesium."], 'B', 'marked'),
(29, "The following does NOT predispose to atherosclerosis:",
 ["Hypertension.", "High fat diet.", "Diabetes mellitus.", "Smoking.",
  "Rheumatic heart disease"], 'E', 'marked'),
(30, "One of the following is not a feature of Fallot's tetralogy",
 ["Pulmonary stenosis", "Right to left shunt", "Left to right shunt",
  "Raised risk of systemic thrombosis", "Cyanosis"], 'C', 'marked'),
(31, "A 20-years-old man with a history of bone marrow transplantation complained of tooth "
     "ache for 2 weeks. He had a tooth extraction and 5 days later he suffered from fever, "
     "malaise and pink spots on his hands. He was admitted to the emergency room. On "
     "clinical examination his temperature was 38.5 °C, heart rate 110/min, and blood "
     "pressure 90/60 mmHg. Laboratory findings were leukocytosis (with predominant "
     "neutrophils), thrombocytopenia, elevated ESR with weak heart beats. What is the most "
     "suggestive diagnosis?",
 ["Rheumatic pancarditis.", "Acute suppurative tonsillitis", "Acute pneumonia.",
  "Infective endocarditis.", "Acute suppurative gingivitis."], 'D', 'marked'),
(32, "How could you confirm the diagnosis in the previous disease?",
 ["X-ray chest", "Echocardiography.", "Liver functions test.", "Blood culture.",
  "Renal function test"], 'D', 'marked'),
(33, "What is the predisposing factor for the previous disease?",
 ["Tooth extraction.", "Tooth infection.", "Impaired immunity.",
  "Bone marrow transplantation.", "All of the above."], 'E', 'marked'),
(34, "What is the most serious complication of this disease?",
 ["Pneumonia.", "Acute valvulitis with vegetation.", "Chronic valvulitis with fibrosis.",
  "Tooth abscess.", "Pericardial fibrosis"], 'B', 'marked'),
(35, "In Malignant hypertension, the vascular lesions include all of the following except:",
 ["Acute arteriolar necrosis", "Cellular hyperplasia",
  "Arteriolar hyalinosis and elastosis", "Endarteritis obliterans"], 'C', 'marked'),
(36, "Atherosclerosis affects:",
 ["Arteries.", "Capillaries.", "Veins.", "Venules.", "Cardiac chambers"], 'A', 'marked'),
# Q37-45 (printed page 5) missing from the scan.
(46, "Why is the myocardium of the right ventricle (RV) thinner than that of the left "
     "ventricle (LV)?",
 ["the RV pumps into the pulmonary circuit which has less resistance than the systemic "
  "circuit.", "the RV pumps a smaller volume of blood than the LV.",
  "the RV pumps blood out with a slower exit speed than the LV.",
  "the RV chamber has a smaller volume than the LV."], 'A', 'marked'),
(47, "The following structures open into the right atrium except which?",
 ["The superior vena cava", "The coronary sinus", "The anterior cardiac vein",
  "The right pulmonary veins"], 'D', 'marked'),
(48, "Conducting system of the heart is composed of the following structures except which?",
 ["The Purkinje plexus", "The deep cardiac plexus", "The sinuatrial node",
  "The atrioventricular bundle."], 'B', 'marked'),
(49, "The following anatomic facts regarding the right coronary artery are correct except "
     "which?",
 ["It gives rise to a marginal branch.",
  "It passes forward between the right auricle and pulmonary trunk.",
  "It gives rise to anterior interventricular branch.",
  "It arises from the anterior aortic sinus."], 'C', 'marked'),
(50, "Pain arising in the heart is commonly referred to the following skin areas except "
     "which?",
 ["Up into the neck and jaw", "Down the medial side of the arm", "The point of the shoulder",
  "The epigastric area"], 'D', 'marked'),
(51, "Which statement about the conducting system of heart is correct?",
 ["The sinoatrial node lies in the crista terminalis, next to the entrance of the inferior "
  "vena cava.", "The atrioventricular node lies next to the opening of the coronary sinus.",
  "The bundle of His divides in the membranous part of the interventricular septum.",
  "The right bundle branch has anterior and posterior divisions."], 'B', 'derived'),
(52, "Which statement about the valves of the heart is correct?",
 ["Both the pulmonary and aortic valves are bicuspid.",
  "The 1st heart sound corresponds to closure of the aortic and pulmonary valves.",
  "Closure of the aortic valve is best heard in the left 2nd intercostal space.",
  "The chordae tendinae prevent eversion of the atrioventricular valves."], 'C', 'marked'),
(53, "Which statement about the right coronary artery is incorrect?",
 ["Supplies the atrioventricular node in 90% of cases.",
  "Usually gives off the posterior interventricular artery.",
  "Contributes to the posterior interventricular artery in a co-dominant circulation.",
  "Arises from the right posterior aortic sinus."], 'D', 'marked'),
(54, "Which statement regarding the fetal circulation is correct?",
 ["The septum secundum lies to the left of the septum primum.",
  "The ductus arteriosus closes at birth.",
  "The foramen ovale is a defect in the septum primum.",
  "The ligamentum teres is the embryological remnant of the right umbilical vein."],
 'D', 'marked'),
(55, "A drug which has a positive inotropic effect means that this drug",
 ["increases the excitability of the contractile cells of the heart.",
  "increases the excitability of the pace maker of the heart",
  "increases the contractility of the contractile cells.", "Increases the heart rate"],
 'C', 'marked'),
(56, "Which of the following increases the afterload of the contracting ventricle?",
 ["Systemic hypertension increases the afterload in front of the left ventricle",
  "Venous return increases the afterload in front of the right ventricle",
  "Venous return increases the afterload in front of the left ventricle",
  "Pulmonary hypertension increases the afterload in front of the left ventricle"],
 'A', 'marked'),
(57, "Starling's law of the heart",
 ["does not operate in the failing heart.", "does not operate during exercise.",
  "explains the increase in heart rate produced by exercise.",
  "explains the increase in cardiac output that occurs when venous return is increased."],
 'D', 'marked'),
(58, "The isometric contraction of the cardiac cycle",
 ['coincides with the "C" wave in jugular venous pressure curve',
  "all cardiac valves are closed", "the ventricle contains the end-diastolic volume of blood",
  "all of the above is correct"], 'D', 'marked'),
(59, "The fourth heart sound is caused by",
 ["closure of the aortic and pulmonary valves.",
  "vibrations in the ventricular wall during systole.", "ventricular filling.",
  "closure of the mitral and tricuspid valves."], 'C', 'marked'),
(60, "The dicrotic notch on the aortic pressure curve is caused by",
 ["closure of the mitral valve.", "closure of the tricuspid valve.",
  "closure of the aortic valve.", "closure of the pulmonary valve."], 'C', 'marked'),
(61, "The second heart sound is caused by",
 ["closure of the aortic and pulmonary valves.",
  "vibrations in the ventricular wall during systole.", "ventricular filling.",
  "closure of the mitral and tricuspid valves."], 'A', 'marked'),
(62, "Which of the following is the main drive for venous return?",
 ["Thoracic movement", "Skeletal muscle contraction", "Dilatation of arterioles",
  "Venous pressure gradient."], 'D', 'marked'),
(63, "Which one of these medical conditions leads to heart failure with preserved ejection "
     "fraction",
 ["Systemic hypertension", "Aortic valve incompetence", "Mitral stenosis",
  "Mitral incompetence"], 'C', 'marked'),
(64, "Stroke volume is increased by",
 ["venoconstriction", "increase in afterload", "decrease in contractility",
  "increase in heart rate"], 'D', 'marked'),
(65, "Which of the following receptors is activated by changes in O2 and CO2 tension in "
     "blood",
 ["Carotid sinus", "Muscle proprioceptors", "Carotid body", "Right atrial baroreceptors",
  "Aortic arch baroreceptors."], 'C', 'marked'),
(66, "Blood pressure increases and heart rate decreases (Cushing reflex) in response to",
 ["Exercise", "Increased body temperature", "Exposure to high altitude",
  "Increased intracranial pressure"], 'D', 'marked'),
(67, "Which of the following types of molecules are the major structural components of the "
     "cell membrane?",
 ["phospholipids and cellulose", "nucleic acids and proteins", "phospholipids and proteins",
  "proteins and cellulose", "glycoproteins and cholesterol"], 'C', 'marked'),
(68, "In order for a protein to be an integral membrane protein it would have to be which "
     "of the following?",
 ["Hydrophilic", "Hydrophobic", "spin the whole thickness of the cell membrane",
  "completely covered with phospholipids", "exposed on only one surface of the membrane"],
 'C', 'marked'),
(69, "Which of these often serve as ion channels across the cell membrane?",
 ["phospholipids", "integral proteins", "peripheral proteins", "integrins", "glycoproteins"],
 'B', 'marked'),
(70, "RMP of a nerve:",
 ["is caused by equal distribution of ions along both sides of the membrane.",
  "is caused by selective permeability of the membrane to the ions.",
  "Na+ - K+ pump has no role in RMP.", "is caused mainly by inward movement of Na+ ions."],
 'B', 'marked'),
(71, "As regards conduction of action potential in a nerve:",
 ["in thick myelinated nerve fibers can reach up to 120 meter/second.",
  "can be increased by increasing calcium.", "can be increased by cooling.",
  "is conducted with decrement."], 'A', 'marked'),
(72, "Repolarization:",
 ["Occurs at first gradual then becomes fast.",
  "Results from closure of sodium gates and opening of potassium gates.",
  "is represented by the ascending limb of the spike.",
  "is followed by appearance of response."], 'B', 'marked'),
(73, "The fastest rate of conduction in the heart is at.........",
 ["Internodal fibers.", "Atrial and ventricular muscles.", "AVN.", "Purkinje fibers."],
 'D', 'marked'),
(74, "Damage of the left bundle branch of the conducting system results in:",
 ["Sudden death due to stop of left ventricular contraction.",
  "Delayed contraction of the left ventricle than the right ventricle.",
  "Nothing because the 2 ventricles are one syncytium.",
  "The right bundle branch divides and supplies the 2 ventricles."], 'B', 'marked'),
(75, "In Lead I in ECG:",
 ["The right arm is connected with negative electrode and the left arm is connected to "
  "the positive electrode.",
  "The right arm is connected with negative electrode and the left foot is connected to "
  "the positive electrode.",
  "The left arm is connected with negative electrode and the left foot is connected to "
  "the positive electrode.",
  "The right arm is connected with positive electrode and both the left arm and left foot "
  "are connected to the positive electrode."], 'A', 'derived'),
(76, "Which of the following conditions is associated with short PR interval:",
 ["Myocardial infarction.", "First degree heart block.", "AV nodal rhythm.",
  "Vagal stimulation."], 'C', 'marked'),
(77, "Which of the following types of arrhythmias is associated with irregular pulse:",
 ["Sinus tachycardia.", "Atrial fibrillation.", "AV nodal rhythm.", "Bundle branch block."],
 'B', 'marked'),
(78, "Atrial pulse in a patient of atrial flutter is expected to be about:",
 ["200-400 beats/min.", "400-600 beats/min.", "150 beats/min.", "Less than 60 beats/min."],
 'A', 'derived'),
(79, "Increased blood flow to the exercising muscles can be explained by all of the "
     "following EXCEPT:",
 ["Sympathetic stimulation of skeletal muscle blood vessels.",
  "Stimulation of the arterial baroreceptors.", "Heat liberated from the active muscles.",
  "Accumulation of metabolites."], 'B', 'marked'),
(80, "During muscular exercise:",
 ["Cardiac output increases.", "Systolic blood pressure decreases in most types of "
  "exercises.", "Diastolic blood pressure rises during running.",
  "Renal vessels dilate markedly."], 'A', 'marked'),
(81, "Which of the following has the highest total cross-sectional area in the body?",
 ["Arteries", "Arterioles", "Capillaries", "Venules", "Veins"], 'C', 'marked'),
(82, "The velocity of blood flow",
 ["is higher in the capillaries than the arterioles.",
  "is higher in the veins than in the venules.", "is higher in the veins than the arteries.",
  "falls to zero in the descending aorta during diastole.",
  "is reduced in a constricted area of a blood vessel."], 'B', 'derived'),
(83, "When the radius of the resistance vessels is increased, which of the following is "
     "increased?",
 ["Systolic blood pressure", "Diastolic blood pressure", "Viscosity of the blood",
  "Hematocrit", "Capillary blood flow"], 'E', 'marked'),
(84, "Which of the following factors increases BP?",
 ["higher viscosity", "vasoconstriction", "maximum increase in heart rate",
  "all of the above"], 'D', 'marked'),
(85, "Mean arterial pressure (MAP) is equal to?",
 ["cardiac output * resistance", "Cardiac output * stroke volume",
  "resistance * heart rate", "Heart rate * pulse rate"], 'A', 'marked'),
(86, "Which of the following factors decreases BP?",
 ["Vasoconstriction", "release of antidiuretic hormone (ADH)", "increased blood volume",
  "None of the above"], 'D', 'marked'),
(87, "A substance derived from vascular endothelium and causes vasodilation, this can be:",
 ["Endothelin-1", "Thromboxane-A2", "Prostaglandin H2", "Prostacyclin"], 'D', 'marked'),
(88, "Thromboxane A2 is",
 ["Vasoconstrictor and helps platelet aggregation",
  "Vasodilator and inhibits platelet aggregation",
  "Released mainly from vascular endothelium", "A & C"], 'A', 'marked'),
(89, "Regarding muscular exercises:",
 ["Systolic blood pressure decreases during playing football.",
  "Diastolic blood pressure rises during weight lifting.",
  "The skeletal muscle blood flow increases up to 20% of the COP.",
  "Venous return remains constant."], 'B', 'marked'),
(90, "The highest phospholipid content is found in ...",
 ["Chylomicrons", "VLDL", "LDL", "HDL"], 'D', 'marked'),
(91, "The class of lipoproteins that is protective against atherosclerosis is ...",
 ["Low-density lipoproteins", "Very low-density lipoproteins", "High-density lipoproteins",
  "Chylomicrons"], 'C', 'marked'),
(92, "Chylomicron is a type of lipoprotein that transports triglycerides from the "
     "intestine to peripheral tissues. Which of the following is an integral "
     "apolipoprotein present in chylomicron?",
 ["Apo B100", "Apo B48", "Apo CII", "ApoE"], 'B', 'marked'),
(93, "The earliest cardiac marker raised in myocardial infarction is -------",
 ["Creatine kinase - MB", "LDH", "AST (GOT)", "Cardiac troponin"], 'D', 'marked'),
(94, "CPK-1 is present in:",
 ["Brain", "Myocardium", "Skeletal muscle", "Liver"], 'A', 'marked'),
(95, "After myocardial infarction which type of LDH is or are predominate:",
 ["LDH1", "LDH4 & LDH5", "LDH3", "LDH2"], 'A', 'marked'),
(96, "One of the following is NOT a criteria of cardiac biomarker",
 ["Sensitive", "Diagnostic value", "Intracellular", "Prognostic value"], 'C', 'marked'),
]

EXCLUDED = (
    [(n, 'page missing from scan (printed page 2)') for n in range(10, 19)] +
    [(19, 'stem straddles the missing page 2 / page 3 boundary — only the tail survived')] +
    [(n, 'page missing from scan (printed page 5)') for n in range(37, 46)]
)


def main():
    questions = []
    for qnum, stem, opts, letter, src in DATA:
        assert letter in 'ABCDE'[:len(opts)], f'Q{qnum} answer {letter} out of range'
        questions.append(Q(stem, opts, letter, src, tag=TAG, year=YEAR))

    meta = {'Source file': SRC,
            'Type': 'Scanned exam paper (photographed), 9 of 11 printed pages present, '
                    '78 of 96 declared questions recoverable',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'marked — yellow-highlighted option on the scan (73 Qs); '
                              'derived — no highlighted option, answered from physiology/'
                              'anatomy knowledge (4 Qs: 51, 75, 78, 82)'}
    n = write_md(OUT, 'Source 23 — Sohag CVS final 2021', meta, questions)

    src_counter = collections.Counter(q.source for q in questions)
    letter_counter = collections.Counter(q.correct for q in questions)
    highest = max(qn for qn, *_ in DATA)
    print(f'source 23: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: declared in source = 96, highest question number = {highest}, '
          f'parsed blocks = {len(DATA)}, ### Q = {n}')
    print(f'  excluded: {len(EXCLUDED)} questions — {EXCLUDED[0][1]} (x9), '
          f'{EXCLUDED[9][1]}, {EXCLUDED[10][1]} (x9)')
    print(f'  answer source: {dict(src_counter)}')
    print(f'  answer letters: {dict(sorted(letter_counter.items()))}')
    top = max(letter_counter.values()) / sum(letter_counter.values()) * 100
    print(f'  top letter share: {top:.1f}%' + (' <== BIAS FAIL' if top > 45 else ''))
    print('  NOTE: this paper may be a re-scan of the same Sohag 2021 final as source 25 '
          '(فاينل سوهاج 2021) — not deduplicated here per Stage-1 contract.')


if __name__ == '__main__':
    main()
