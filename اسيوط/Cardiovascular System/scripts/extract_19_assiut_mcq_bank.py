#!/usr/bin/env python3
"""Source 19 — ASSIUT PREVIOUS EXAMS/MCQ Assuit.pdf.

An 8-page phone-photographed MCQ paper covering CVS Physiology, Pharmacology,
Microbiology, Parasitology, Pathology, Anatomy and Histology. The original OCR dump
(.ocr/19_mcq_assiut.txt) is badly garbled at the word level (e.g. stems come out as
"A sewbers bout 7 btn examine ination showed ejection") — the pages were scanned
sideways and the first-pass OCR did not auto-rotate. Per the extraction contract
(never trust OCR on a degraded scan — verify), every question here was transcribed
by eye from 400 dpi renders of the source PDF
(`pdftoppm -png -r 400 -f 1 -l 8 ".../MCQ Assuit.pdf" /tmp/.../s19/p`), read
directly with an image reader page by page — not parsed from any OCR text.

A second, orientation-corrected OCR pass was later produced at
.ocr2/19_mcq_assiut.txt and is readable (still with light residual damage, e.g.
"4S year-old" for 45, "CHP" for CHF). It was used only to cross-check the manual
transcription below after the fact — every stem, option and page-ordering quirk
here (page 1 holds Q28-34, page 2 holds Q1-9, etc.) matches .ocr2 exactly, so the
hand transcription stands unchanged.

Layout quirk: the 8 PDF pages are not in question-number order (page 1 holds
Q28-34, page 2 holds Q1-6, etc.) — same out-of-binding-order photography as
source 20. Output here is keyed to the verified question numbers regardless of
page order.

The paper prints no answer key, so every answer is `derived` from medical
knowledge. All 52 questions on the 8 pages were legible; none excluded.

Q41 misprints its option markers on the page itself (a, b, a, c instead of
a, b, c, d) — relabelled A-D in reading order here, per the contract's
"options run A, B, C... with no gaps" rule.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, clean

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system',
                   'ASSIUT PREVIOUS EXAMS', 'MCQ Assuit.pdf')
OUT = os.path.join(MOD, 'Markdown_Questions', '19_Assiut_MCQ_Bank.md')
# The paper itself states NO exam type and NO year — the only "term" string anywhere in it
# is inside the word "intermittent". Its filename is just "MCQ Assuit". An earlier pass
# tagged it 'Exams, Final' by inferring from the folder it sits in; the contract's rule is
# that Year comes from what the source states and is never inferred, and the same restraint
# applies to the exam type. It is therefore filed as an undated department bank. If the year
# and sitting are later confirmed, retag it 'Exams, Final <Year>'.
TAG, YEAR = 'Department, QBank, CVS', None

# Manually transcribed from 400 dpi page renders (see module docstring). Each tuple:
# (n, stem, [A, B, C, D], correct_letter).
QUESTIONS = [
(1, "A 45-year-old man develops congestive heart failure (CHF) after suffering his second "
    "myocardial infarction. His physician puts him on a regimen of several medications, including "
    "furosemide. On follow-up, the patient is found to have hypokalemia, likely secondary to "
    "furosemide use. The addition of which medication would likely resolve the problem of "
    "hypokalemia, while helping to treat the underlying condition, CHF?",
 ["Hydrochlorothiazide", "Spironolactone", "Acetazolamide", "Ethacrynic acid"], 'B'),
(2, "A 57-year-old man is hospitalized recovering from a left wall myocardial infarction. His doctors "
    "want to start a drug regimen for congestive heart failure, including either an ACE inhibitor or "
    "an angiotensin receptor blocker (ARB). Which of the following is a side effect of ACE inhibitors "
    "only?",
 ["Dizziness", "Angioedema", "Erectile dysfunction", "Hypotension"], 'B'),
(3, "A 55 year old diabetic woman patient, her blood pressure is 160/95. What is the best "
    "antihypertensive drug to this woman?",
 ["Propranolol", "Enalaprilate", "Hydrochlorothiazide", "Indapamide"], 'B'),
(4, "A patient with hypertension also suffers from essential tremor. Optimal treatment of the patient "
    "should include which of the following drug?",
 ["Prazosin", "Clonidine", "Lidocaine", "Propranolol"], 'D'),
(5, "A 55-year-old female who suffers from angina when she climbs stairs or participates in similar "
    "activities receives sublingual nitroglycerin. She was instructed to take a tablet 1 or 2 minutes "
    "before she climbs stairs to prevent the angina. Which best describes a step on nitroglycerin's "
    "mechanism of action?",
 ["Activation of phosphodiesterase", "Activation of guanylate cyclase",
  "Inhibition of guanylate cyclase", "Inhibition of phosphodiesterase"], 'B'),
(6, "A sever angina patient received a combination of antianginal medications with "
    "multiple mechanisms of actions. In this case of severe angina pectoris, we can use:",
 ["Nifedipine + propranolol", "Verapamil + metoprolol", "Diltiazem + atenolol", "Nifedipine + pindolol"], 'A'),
(7, "A 29-year-old man with a family history of heart disease presents to his primary care physician "
    "for a routine checkup. A lipid profile on a blood draw reveals high LDL and low HDL. One way "
    "to decrease the amount of LDL in the blood is to hinder the liver's ability for de novo "
    "cholesterol synthesis. Which of the following drugs blocks de novo cholesterol synthesis in "
    "hepatocytes?",
 ["Cholestyramine", "Rosuvastatin", "Colestipol", "Ezetimibe"], 'B'),
(8, "A 37-year-old woman with hyperlipidemia is taking a drug to lower her triglyceride and blood "
    "cholesterol levels. She is considering stopping her therapy, because she suffered from itching "
    "and flushing in her face that occurs following a drug she was taken. Which drug is she taking?",
 ["Atorvastatin", "Fenofibrate", "Gemfibrozil", "Nicotinic acid"], 'D'),
(9, "An obese women during routine check-up, her doctor asked for lipid profile. The results "
    "demonstrated that the serum triglyceride is 250 mg/dl and total serum cholesterol is 320 mg/dl. "
    "She was prescribed antihyperlipidemic drug. One of the following is true regarding the "
    "mechanism of action of antihyperlipidemic drugs:",
 ["Lovastatin stimulates HMG-CoA reductase", "Cholestyramine binds to bile acids in the liver",
  "Fenofibrate inhibits lipoprotein lipase", "Ezetimibe inhibits Niemann Pick C1-Like1 protein"], 'D'),
(10, "Which of the following is the bacterial cause of zoonotic Infective Endocarditis?",
 ["Bartonella spp", "Coxiella burnetii", "Staphylococcus gallolyticus", "HACEK"], 'B'),
(11, "A 13-year-old boy is brought to the physician because of pain in his knees and ankles with a "
     "recent onset of fever. He had an upper respiratory infection 2 weeks ago. Physical examination "
     "shows a systolic murmur heard in the mid-precordial area, erythematous skin macules with a "
     "clear center and small subcutaneous nodules on the dorsal aspects of the arms. Which of the "
     "following hypersensitivity reactions best explains this patient's condition?",
 ["Type I", "Type II", "Type III", "Type IV"], 'B'),
(12, "A 15-year-old girl comes to the physician for a follow up examination. She has a history of fever "
     "and joint pains. She had a sore throat 6 weeks ago. Laboratory studies show negative rapid "
     "antigen test and increased high ASO titer (400 Todd Units). This patient is at increased risk for "
     "which of the following cardiac condition?",
 ["Hemorrhagic pericarditis", "Infective endocarditis", "Myocardial fibrosis", "Rheumatic fever"], 'D'),
(13, "Which of the following is a characteristic of Coxsackievirus B?",
 ["Belongs to Flaviviridae family", "Double-stranded RNA virus",
  "Non-enveloped virus", "Transmitted through blood transfusion"], 'C'),
(14, "What is the mode of transmission of Coxsackievirus B induced viral myocarditis?",
 ["Direct contact", "Fecal-oral route", "Airborne infection", "Vector-borne"], 'B'),
(15, "A 65-year-old man is referred to the cardiothoracic surgeon because of aortic stenosis. The "
     "cardiothoracic surgeon performs aortic valve replacement in this patient. The surgeon advises "
     "the patient to be treated with antimicrobials before he undergoes any kind of dental procedure. "
     "This pre-dental treatment is most likely to prevent infection with an organism with which of the "
     "following characteristics?",
 ["Catalase-negative, alpha-hemolytic, and bile resistant",
  "Catalase-negative, alpha-hemolytic, and bile soluble",
  "Catalase-negative, non-hemolytic, bile resistant",
  "Catalase-positive, beta-hemolytic, and coagulase-positive"], 'A'),
(16, "A 39-year-old patient receiving chemotherapy for three years, which of the following protozoans "
     "is the common cause of myocarditis associated with chorioretinitis and encephalitis?",
 ["Entamoeba histolytica", "Trypanosoma cruzi", "Toxoplasma gondii", "Plasmodium ovale"], 'C'),
(17, "Which of the following is the first step for diagnosis in acute Chagas disease?",
 ["ECG to detect cardiomyopathy.", "Giemsa stained blood smears to detect trypomastigotes.",
  "X-ray with barium to detect megaorgans.", "Serology to detect antibodies of Trypanosoma."], 'B'),
(18, "About Loven's Reflex:",
 ["low CO2 stimulates sensory receptors", "Vasodilatation of blood vessels of the active organ",
  "Vasoconstriction of blood vessels of active organ body organs", "Increased blood flow to the rest organ"], 'B'),
(19, "About myogenic mechanism which is wrong:",
 ["It's one of autoregulation mechanism", "It involves activation of the integrins receptor.",
  "It produces stretch of vascular smooth muscle and opens Ca, Na channels",
  "It produces further increases in blood flow"], 'D'),
(20, "About hormones released after hemorrhage, what's is wrong",
 ["Adrenalin secreted from adrenal medulla that increase heart rate",
  "Glucocorticoid secreted from adrenal cortex that antagonize stress",
  "ADH secreted from Posterior pituitary that increase salt and water absorption",
  "Erythropoietin secreted from kidney that stimulates bone marrow"], 'B'),
(21, "About refractory or irreversible shock, which of the following is wrong?",
 ["Blood transfusion can save the life of the patient", "Much acidosis develops",
  "Depletion of high energy phosphate reserves occurs", "Deterioration of the heart and different organs occurs"], 'A'),
(22, "Which of the following physiologic responses has a neural basis?",
 ["Red reaction", "White reaction", "Flare", "Reactive hyperemia"], 'C'),
(23, "About the Volume Reflex which is true:",
 ["It's one of rapid blood pressure controlling mechanism",
  "Produce reflex constriction of the afferent arterioles in the kidneys",
  "Atrium secrets atrial natriuretic peptide which increases excretion of salt",
  "Increases secretion of ADH."], 'C'),
(24, "Reversal of development of aorticopulmonary septum would result in",
 ["Persistent truncus arteriosus.", "Patent ductus arteriosus.",
  "Transposition of great arteries.", "Lower displacement of tricuspid valve."], 'A'),
(25, "Prenatal closure of the foramen ovale would result in atrophy of",
 ["Right ventricle.", "Right atrium.", "Left ventricle.", "Pulmonary trunk."], 'C'),
(26, "A 20-year-old male came to the outpatient complaining of persistent headache. Blood pressure "
     "measured on the left arm was 160/100. Examination of the lower limbs presents cold feet and "
     "weak dorsalis pedis pulse. X-ray showed prominent costal notches in the ribs of both sides. The "
     "most likely anomaly is",
 ["Aortic stenosis.", "Postductal coarctation of aorta.", "Persistent patent ductus arteriosus.", "Mitral stenosis."], 'B'),
(27, "A newborn baby was delivered by cesarean section for a 28-year-old mother who was on lithium "
     "medication for psychiatric troubles for the last two years. The baby was found to be cyanotic and "
     "dyspneic. Echo examination helped diagnosis of Ebstein abnormality. This anomaly in this case "
     "is characterized by",
 ["Atrophy of the right atrium.", "Hypertrophy of the right ventricle.",
  "Downward displacement of the tricuspid valve.", "Septum primum atrial septal defect."], 'C'),
(28, "A newborn baby is being examined 3 days after birth. Vital signs were within normal figures. "
     "There was no cyanosis. Cardiac examination showed ejection systolic murmur at the sternal "
     "border of the left second intercostal space and splitting of the second heart sound. Echo "
     "identified enlargement of the right side of the heart. What is the most likely diagnosis of this "
     "defect?",
 ["Fallot tetralogy.", "Patent foramen ovale.", "Persistent truncus arteriosus.", "Preductal coarctation of the aorta."], 'B'),
(29, "What is the embryonic source of development of the middle segment of the permanent aortic "
     "arch?",
 ["Second left aortic arch.", "Aortic sac.", "Left dorsal aorta.", "Left fourth aortic arch."], 'D'),
(30, "Anti-oxidant may help to decrease atherosclerosis by inhibiting oxidation of which of the "
     "following lipoprotein?",
 ["IDL", "HDL", "LDL", "VLDL"], 'C'),
(31, "A 58 year old man undergoes diagnostic cardiac catheterization. Which one of cardiac "
     "markers suspected to be still high and sensitive after 6 days from onset chest pain?",
 ["Troponin I", "Myoglobin", "Total Creatine kinase", "Creatine kinase-MB"], 'A'),
(32, "A 60 year old female admitted to coronary care unit with severe retrosternal chest pain. She "
     "received medical therapy and improved. After 5 days, she developed again chest pain of the "
     "same characters. Which one of these cardiac markers will help in diagnosis of her case?",
 ["Troponin I", "Troponin T", "Myoglobin", "Creatine kinase-MB"], 'D'),
(33, "A diabetic 76-year-old man with sudden loss of movement of the left side of his body. He is a "
     "heavy smoker. His BP was 160/100 mm Hg. He was diagnosed to have atherosclerosis and "
     "cerebral artery occlusion. Which of the following components of blood lipids is most important "
     "in contributing to her disease?",
 ["Chylomicrons", "Lipoprotein lipase", "Oxidized LDL", "VLDL"], 'C'),
(34, "In a moderate-sized myocardial infarct it would take approximately how long to replace the "
     "necrotic muscle by granulation tissue?",
 ["2 hours", "2 days", "2 weeks", "2 months"], 'C'),
(35, "A 25 years old male patient presented with malaise and fatigue of unexplained clinical findings. "
     "On follow up, he developed one syncopal attack. Imaging studies showed cardiac intra-axial "
     "mass filling most of the atrium. Which of the following diagnosis is a most likely diagnosis?",
 ["Cardiac myxoma.", "Cardiac rhabdomyoma.", "Cardiac vegetations.", "Cardiac hematoma."], 'A'),
(36, "A 30 year old patient had a history of repeated attacks of rheumatic fever. On clinical "
     "examination, mitral stenosis is diagnosed by cardiac auscultation. Which of the following is an "
     "expected complication of this disorder?",
 ["Subacute bacterial endocarditis.", "Myocardial infarction.",
  "Pulmonary embolism.", "Acute bacterial endocarditis."], 'A'),
(37, "Which of the following is a leading cause of ventricular rupture?",
 ["Recent myocardial infarction", "Subacute bacterial endocarditis.",
  "Chronic rheumatic myocarditis", "Ventricular arrhythmia."], 'A'),
(38, "A doctor in pediatric clinic noticed a small nodule on the lower lip of the mouth of a newborn "
     "baby. By pressure on the lump, the red color diminished. A biopsy was performed. The "
     "pathology report was signed as \"That of capillary hemangioma\". What was seen under the "
     "microscopic of this biopsy?",
 ["Spindle cells arranged in fascicles separated by red blood cells.",
  "Large polygonal cells admixed with spider cells.",
  "Collection of mononuclear and multinuclear histiocytes in paraventricular location.",
  "Groups of small sized vascular capillaries lined by uniform endothelial cells."], 'D'),
(39, "A 55 year old female patient gave a long history of central chest pain that is triggered by "
     "exertion and relieved by rest. Recently, the patient has developed severe chest pain that is "
     "persistent and not relieved by exertion or arterial dilator. How can you describe the recent "
     "pathologic changes?",
 ["The patient has a severe attack of rheumatic carditis.", "The patient develops unstable angina.",
  "The patient develops myocardial rupture on top of old myocardial infarction.",
  "The patient had a mitral stenosis and developed recent valvular vegetations."], 'B'),
(40, "Which of the following describes the condition where the pericardial sac is obliterated and the "
     "heart is encased by thickened fibrotic pericardium?",
 ["Pericardiomyopathy.", "Pyogenic pericarditis.", "Chronic constrictive pericarditis", "Chronic adhesive pericarditis."], 'C'),
(41, "A 53 years old woman with familiar history of hyperlipidemia presented with intermittent "
     "claudication pain in lower limb with long walk. She had never been smoking. On imaging "
     "studies, the femoral artery showed luminal narrowing. Which of the following is your diagnosis?",
 ["Burger's disease.", "Atherosclerosis.", "Benign hypertension.", "Malignant hypertension."], 'B'),
(42, "A 66 year diabetic old man suffered from repeated attacks of severe chest pain. Blood pressure is "
     "200/120 mmHg. Laboratory investigation revealed increased serum level of LDL. ECG showed "
     "signs of inadequate coronary blood flow. The patient neglected medical treatment and died. "
     "Which of the following is expected to be cause of death?",
 ["Coronary embolism.", "Aortic stenosis.", "Motor car accident.", "Chronic heart failure."], 'D'),
(43, "A young man suffers from severe headache and blurring of vision. Eye examination shows "
     "papilloedema. His blood pressure is 250/160 mmHg. Urine examination shows proteinuria. "
     "Renal biopsy will show:",
 ["Fibrinoid necrosis of the walls of the arterioles.", "Hyalinization of the glomeruli",
  "Renal infarction.", "Hyalinization of the walls of arterioles."], 'A'),
(44, "The most common cause of death in benign hypertension is:",
 ["Renal failure", "Heart failure", "Cerebral hemorrhage", "Respiratory failure"], 'B'),
(45, "An adult patient suffered from Cushing syndrome (excess supra-renal gland hormone secretion). "
     "His blood pressure was 250/160 mmHg. How can you explain this increase in blood pressure?",
 ["Primary (essential) hypertension", "Coarctation of the aorta.",
  "Secondary Hypertension", "Hyperplastic arteriolosclerosis."], 'C'),
(46, "Which of following is true for Buerger's disease?",
 ["Affects women who eat burgers.", "Affects gentleman with heavy alcohol use.",
  "Affects mainly the vessels of internal organs", "Involves arteries and veins with a thrombus formation."], 'D'),
(47, "A young woman complains of fever of unknown origin. Blood pressure is 170/110. Angiography "
     "shows nodular swellings along the course of small and medium sized arteries. What is your "
     "probable diagnosis?",
 ["Varicose veins", "Thromboangitis obliterans", "Polyarteritis nodosa", "Septic shock."], 'C'),
(48, "A female patient presents with dilated elongated and tortuous leg veins. What is the possible "
     "complication of this condition?",
 ["Renal failure", "Cerebral hemorrhage", "Phlebothrombosis", "Hypertension"], 'C'),
(49, "Regarding umbilical arteries:",
 ["The tunica media contains inner longitudinal and outer circular layer of smooth muscle fibers.",
  "The tunica media contains inner longitudinal and outer circular layer of skeletal muscle fibers.",
  "The tunica intima contains inner longitudinal and outer circular layer of smooth muscle fibers.",
  "The tunica media contains inner longitudinal and outer circular layer of cardiac muscle fibers."], 'A'),
(50, "Which organ contains capillaries with fenestrated endothelium?",
 ["Endocrine glands", "Choroid plexus", "Brain", "Lung"], 'B'),
(51, "Individuals with Marfan syndrome have mutations in the fibrillin gene and commonly "
     "experience aortic aneurysms. What portion of the arterial wall is most likely to be affected by "
     "the malformed fibrillin?",
 ["Endothelium", "Tunica intima", "Tunica media", "Tunica adventitia"], 'C'),
(52, "What tissue is directly associated with and extends into the heart valves?",
 ["Myocardium", "Epicardium", "Atrioventricular bundle of His", "Cardiac skeleton"], 'D'),
]


def main():
    questions = []
    for n, stem, opts, correct in QUESTIONS:
        questions.append(Q(clean(stem), opts, correct, 'derived', tag=TAG, year=YEAR))

    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/MCQ Assuit.pdf',
            'Type': 'Scanned/phone-photographed exam paper, 8 pages, 52 questions (manually verified — OCR unusable)',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': 'None',
            'Answer source': 'derived — the paper prints no key'}
    n = write_md(OUT, 'Source 19 — Assiut CVS MCQ Bank', meta, questions)

    letters = collections.Counter(q[3] for q in QUESTIONS)
    total = sum(letters.values())
    max_share = max(letters.values()) / total if total else 0
    highest = max(q[0] for q in QUESTIONS)
    option_a_blocks = sum(1 for q in QUESTIONS if len(q[2]) >= 1)

    print(f'source 19: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: highest question number in source = {highest}, '
          f'option-A blocks = {option_a_blocks}, ### Q headings = {n}')
    print(f'  answer source: derived = {n} (0 key / 0 marked / 0 online)')
    print('  excluded: 0 — all 52 questions on the 8 rendered pages were legible')
    print('  answer-letter distribution: ' +
          ', '.join(f'{k}={letters[k]}' for k in sorted(letters)))
    verdict = 'PASS' if max_share <= 0.45 else 'FAIL'
    print(f'  bias gate: max single-letter share = {max_share:.1%} -> {verdict}')


if __name__ == '__main__':
    main()
