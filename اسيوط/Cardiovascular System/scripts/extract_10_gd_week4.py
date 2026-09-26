#!/usr/bin/env python3
"""Source 10 — GD/4th week-CVS-206 cases.pdf.

Four G.D. sessions across five subjects: Pharmacology (GD 1), Anatomy and
Pathology (both numbered GD 2 — "a: Anatomy" covers a myocardial-infarction
coronary-anatomy case, "b: Pathology" covers an ischemic-heart-disease case),
and Physiology (GD 3 and GD 4). As in the other weekly files, the "G.D. (N):
title (Subject)" label is a running FOOTER for the block it names, so raw
lib_gd.parse() forward-attribution mis-tags everything after each header as
belonging to the *next* header. That is corrected below by reading the
source directly rather than trusting the parser's per-item GD/subject field.

lib_gd.py has now been fixed a SECOND time: its BULLET rule used to require
a bulleted "-" sub-question to end in "?" or ":", which silently dropped
every bulleted question that instead ends in a plain full stop (or no
terminal punctuation at all). Re-parsing this source against the twice-fixed
parser now yields 61 raw rows (it yielded 51 raw rows when the previous
version of this file — with 57 curated items — was written), cross-checked
against `pdftotext -layout` of the source PDF
(/tmp/.../scratchpad/parse2_10.txt and .../scratchpad/raw10.txt). That
closes exactly the gap the previous pass flagged as unrecoverable:

1. GD 2 "a: Anatomy" Case 4 — "A 65-year-old female was brought to the
   emergency room ... low blood pressure and high heart rate ..." — was
   missing its one bulleted sub-question, "Mention name and location of the
   arteries which their pulsation can be palpated in the body." (no
   terminal "?"/":"). Now restored as one new written item.
2. GD 2 "b: Pathology" Case 2 — "A woman complains of fever of unknown
   etiology... nodular swellings along the course of small and medium
   sized arteries" (a polyarteritis-nodosa-like vasculitis vignette) — was
   missing both its bulleted sub-questions, "What is the diagnosis" and
   "Mention effects of this disease" (neither ends in "?"/":"). Now
   restored as two new written items.
3. GD 2 "b: Pathology" Case 3 — "A female patient presents with dilated
   elongated and tortuous leg veins" (varicose veins) — was missing both
   its bulleted sub-questions, "What is the diagnosis" and "Mention the
   complications of this condition and enumerate which one of these
   complications could be fatal and How?". Now restored as two new
   written items.

That is 5 new items (57 -> 62). All five are genuinely new content, not
duplicates of anything already curated below — grep of the prior script
for "pulsat", "nodosa", "varicos" turned up nothing before this pass.

Judgement calls made while adding the 5 new items:

a. Case 2 (Anatomy) and Case 2/Case 3 (Pathology) in the source share the
   number "2" — the "G.D. (N): title (Subject)" footer line is confirmed
   to belong to the block it trails, not the block it heads (as with every
   other footer in this source), so the two new Pathology cases are tagged
   `Department, GDs, Pathology GD 2` (not Anatomy) and the pulsation
   question is tagged `Department, GDs, Anatomy GD 2` — matching the raw
   text's own section headers ("a: Anatomy" / "b: Pathology") rather than
   position in the parse stream.
b. The polyarteritis and varicose vignettes are short (one or two
   sentences) and are prefixed to both of their case's sub-questions
   verbatim from the raw PDF text, exactly as every other case vignette in
   this file is reused across its sub-questions.
c. "What is the diagnosis" in the source has no question mark; it is kept
   without one to match the source's own wording (as elsewhere in this
   file, punctuation is not invented).
d. Both new pathology answers and the new anatomy answer are `derived`
   (no key/mark is printed anywhere in this source) and are 1-3 sentence
   clinically-grounded answers to the question as posed, consistent with
   every other item in this file.

The remaining, pre-existing judgement calls from the prior pass are kept
for reference:

4. The raw parse glues a trailing bulleted sub-question onto the *last*
   option of the coronary-anatomy MCQ ("...Right coronary artery Fourth
   week ... -What does the left anterior descending ... supply?"). The
   footer noise is deleted and the sub-question is split into its own
   written item.
5. "An old man presented with acute chest pain and sudden death..." was
   parsed as an MCQ whose "options" are really four separate written
   sub-questions (diagnosis / expected site / pathogenesis / gross and
   microscopic changes); these are emitted as four separate written items
   sharing the one vignette, not as a single MCQ.
6. GD 4's Case 3 (a 55-year-old man with JVP-positive left-sided heart
   failure with infarction) uses "-" bulleted sub-questions; its two
   questions are kept as curated items.
7. "45-year-old man presented with severe lower limb edema..." — the parse
   truncates the leading age ("year-old man..."); the full sentence is
   restored from the raw PDF text.

Everything else (the 57 previously curated items) is reused verbatim from
the prior version of this script — already hand-checked against the
source, wording and answers unchanged, and confirmed by this pass not to
duplicate any of the 5 newly-recovered rows.

No answer key is printed anywhere in this source; every answer is
`derived` from medical knowledge and justified against the case as given.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '10_GD_Week_4_Cases.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/4th week-CVS-206 cases.pdf'

V_ANGINA = ('A physician decides to place a patient on a calcium channel blocker for '
            'treatment of her angina. Calcium channel blockers can relax the smooth '
            'muscle of blood vessels and can also have various effects on cardiac '
            'contractility, conduction, and heart rate.')

V_DIGOXIN = ('Hoda Ali, 30 years old, has a history of rheumatic fever 10 years ago '
             'treated with Benzathine penicillin G. Two weeks ago she developed heart '
             'failure and started digoxin, furosemide and captopril. Three days ago '
             'she developed severe vomiting and atrial fibrillation and was diagnosed '
             'with digoxin toxicity.')

V_HYPOVOL = ('Mavis, a 78-year-old widow, was brought to the emergency room after '
             'passing bright red blood in her stool all day, initially attributed to '
             'hemorrhoids; she takes up to 10 aspirin tablets daily for arthritis. In '
             'the ER she was light-headed, pale, cold and anxious. Hematocrit was 29% '
             '(normal 36-46%). Supine BP/HR were 90/60 and 105/min; upright BP/HR were '
             '75/45 and 135/min. Colonoscopy later showed bleeding diverticula that '
             'had stopped spontaneously; she received two units of whole blood.')

V_SEPTIC = ('A 78-year-old male patient was brought to the emergency room with severe '
            'fever, dyspnea and hypotension, 5 days after a major operation and '
            'hospital discharge. He was diagnosed with septic shock: BP 80/50, '
            'temperature 40°C, HR 140/min regular, RR 38/min.')

V_HF1 = ('A 45-year-old man presented with severe lower-limb edema, dyspnea and other '
         'symptoms of congestive heart failure.')

V_HF2 = ('A 60-year-old woman arrives at the emergency department with severe burning '
         'pain in her left arm. Laboratory studies show an elevated troponin I level '
         'and she is treated for an acute myocardial infarction. Her ejection '
         'fraction is below 30%.')

V_MI_ANAT1 = ('A 75-year-old woman arrives at the emergency department and states '
              'that her left arm is numb. She is diaphoretic. Laboratory studies show '
              'an elevated troponin I level and the patient is treated for an acute '
              'MI. A subsequent echocardiogram shows a wall motion abnormality of the '
              'posterior interventricular septum.')

V_MI_ANAT2 = ('A 45-year-old man with a history of stable angina presents to the '
              'emergency department with an episode of chest pain that is not '
              'relieved by rest or nitroglycerin. After stabilization in the '
              'telemetry unit for 2 days, he undergoes a thallium stress test. The '
              'results show reduced perfusion of the lateral wall of the left '
              'ventricle.')

V_MI_ANAT3 = ('A 70-year-old woman with a history of type II diabetes mellitus '
              'presents to the emergency department with crushing substernal chest '
              'pain radiating to her neck and jaw. Emergency cardiac catheterization '
              'with percutaneous coronary intervention (PCI) shows a 90% occlusion of '
              'her left anterior descending artery. ECG reveals an anterior wall '
              'ST-segment-elevation MI. The patient was diagnosed with myocardial '
              'infarction with a ruptured anterior papillary muscle of the left '
              'ventricle.')

V_PULSE = ('A 65-year-old female was brought to the emergency room by her sister. '
           'Early in the day, she had seen bright red blood in her stool, which she '
           'attributed to hemorrhoids. However, the bleeding continued all day, and '
           'she could no longer ignore it. In the emergency room, she had low blood '
           'pressure and high heart rate. An infusion of normal saline and blood was '
           'started immediately.')

V_OLDMAN = ('An old man presented with acute chest pain and sudden death. Postmortem '
            'examination of the heart showed a pale soft area.')

V_POLYARTERITIS = ('A woman complains of fever of unknown etiology. Blood pressure is '
                    '180/100 mmHg. Angiography shows nodular swellings along the '
                    'course of small and medium sized arteries.')

V_VARICOSE = ('A female patient presents with dilated, elongated and tortuous leg '
              'veins.')

V_JVP = ('A 55-year-old obese male was rushed to the casualty with chest pain '
         'radiating to the left arm, associated sweating and severe dyspnea. He is a '
         'chronic smoker and a known hypertensive on irregular treatment for the past '
         '15 years. He was diagnosed with left-sided heart failure with infarction. '
         'HR 120/min, BP 160/100 mmHg, respiratory rate 35/min, elevated JVP.')

TAG_PHARM1 = 'Department, GDs, Pharmacology GD 1'
TAG_ANAT2 = 'Department, GDs, Anatomy GD 2'
TAG_PATH2 = 'Department, GDs, Pathology GD 2'
TAG_PHYS3 = 'Department, GDs, Physiology GD 3'
TAG_PHYS4 = 'Department, GDs, Physiology GD 4'

ITEMS = [
    # --- GD 1: Cases of Angina and CHF (Pharmacology) — angina case ---
    (V_ANGINA + ' Which one of the channel blockers would be most effective in '
     'reducing heart rate and contractility?', None, None,
     'A non-dihydropyridine calcium channel blocker such as verapamil (or '
     'diltiazem) — these act preferentially on cardiac L-type calcium channels, '
     'slowing SA/AV nodal conduction and reducing heart rate and myocardial '
     'contractility, unlike the dihydropyridines (e.g. nifedipine), which act mainly '
     'on vascular smooth muscle.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' Can we use nifedipine alone to treat angina?', None, None,
     'It is not ideal alone: nifedipine causes marked arteriolar vasodilation with '
     'reflex sympathetic activation and tachycardia, which increases myocardial '
     'oxygen demand and can worsen angina; it is usually combined with a '
     'beta-blocker to blunt the reflex tachycardia.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' The combination between calcium channel blockers and beta blockers '
     'may be indicated or contraindicated. Explain.', None, None,
     'A dihydropyridine CCB (nifedipine, amlodipine) with a beta-blocker is a '
     'rational, often-indicated combination, since the beta-blocker prevents the '
     'reflex tachycardia caused by the CCB. Combining a non-dihydropyridine CCB '
     '(verapamil, diltiazem) with a beta-blocker is usually contraindicated, because '
     'both depress SA/AV nodal conduction and myocardial contractility, risking '
     'severe bradycardia, heart block or heart failure.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' What are the antianginal effects of organic nitrates, calcium '
     'channel blockers and beta blockers?', None, None,
     'Nitrates cause predominant venodilation (reducing preload) with some coronary '
     'vasodilation, lowering myocardial oxygen demand. Calcium channel blockers '
     'reduce afterload via arteriolar dilation and relieve coronary vasospasm (the '
     'non-dihydropyridines also reduce heart rate/contractility). Beta-blockers '
     'reduce heart rate, contractility and myocardial oxygen demand, and are '
     'particularly effective for exertional (stable) angina.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' What is the dangerous drug interaction of organic nitrates?',
     None, None,
     'Co-administration with phosphodiesterase-5 inhibitors (e.g. sildenafil) causes '
     'severe, potentially fatal hypotension from excessive additive NO/cGMP-mediated '
     'vasodilation.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' Why are some members of the calcium channel blockers used in '
     'pregnant women?', None, None,
     'Dihydropyridine CCBs such as nifedipine are used to treat hypertension/'
     'pre-eclampsia and as a tocolytic in pregnancy because, unlike ACE inhibitors '
     'or ARBs, they are not teratogenic and give effective, controllable reduction of '
     'blood pressure or uterine tone.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' What is the drug of choice for controlling an acute attack of '
     'angina pectoris?', None, None,
     'Sublingual (or spray) nitroglycerin, for its rapid onset of venodilation and '
     'reduction of preload/myocardial oxygen demand.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' Why are beta-blockers contraindicated in variant angina?',
     None, None,
     'Variant (Prinzmetal) angina is caused by coronary artery vasospasm; blocking '
     'beta-2 receptors leaves alpha-adrenergic vasoconstriction unopposed, which can '
     'worsen the spasm and precipitate further ischemia.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' What is the drug of choice for prophylaxis of Prinzmetal angina?',
     None, None,
     'Calcium channel blockers (e.g. nifedipine, diltiazem) are first-line, as they '
     'directly relieve coronary vasospasm; long-acting nitrates are also used.',
     TAG_PHARM1, 'Pharmacology'),
    (V_ANGINA + ' Can we use pindolol in the management of angina? Why?', None, None,
     'No — pindolol is a beta-blocker with intrinsic sympathomimetic activity '
     '(partial agonism), so it does not reliably lower heart rate and contractility '
     'and is a poor choice for angina, which requires full beta-blockade to reduce '
     'myocardial oxygen demand.',
     TAG_PHARM1, 'Pharmacology'),

    # --- GD 1: Cases of Angina and CHF (Pharmacology) — digoxin-toxicity case ---
    (V_DIGOXIN + ' What is the possible cause of digoxin toxicity in this case?',
     None, None,
     'Furosemide-induced hypokalemia (with possible renal impairment) potentiates '
     'digoxin\'s binding to the myocardial Na+/K+-ATPase, precipitating toxicity even '
     'at a therapeutic digoxin dose.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What are the early manifestations of digoxin toxicity?', None, None,
     'Anorexia, nausea and vomiting, and visual disturbances (blurred or '
     'yellow-green vision, halos around lights) are the classic early GI/CNS signs, '
     'often preceding cardiac arrhythmias.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What are the lines of treatment of digoxin toxicity?', None, None,
     'Stop digoxin; correct hypokalemia and other electrolyte disturbances '
     '(cautiously); give digoxin-specific antibody fragments (Digibind) for severe '
     'toxicity or life-threatening arrhythmias; and treat arrhythmias with agents '
     'such as lidocaine/phenytoin for ventricular arrhythmias or atropine/pacing for '
     'bradyarrhythmias, avoiding calcium salts and quinidine-type drugs.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What are the precipitating factors for digoxin toxicity?',
     None, None,
     'Hypokalemia, hypomagnesemia, hypercalcemia, renal impairment (reduced digoxin '
     'clearance), hypothyroidism, and interacting drugs (quinidine, verapamil, '
     'amiodarone) that raise serum digoxin levels.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What is the rationale for using beta-blockers in cases of CHF?',
     None, None,
     'Chronic sympathetic overactivity in heart failure is initially compensatory but '
     'ultimately accelerates adverse remodeling and mortality; beta-blockers, '
     'introduced cautiously at low dose in stable patients, blunt this toxicity, '
     'reduce heart rate and oxygen demand, and improve long-term survival and '
     'ejection fraction.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What is the first-line treatment for CHF?', None, None,
     'An ACE inhibitor (or ARB/ARNI) plus a beta-blocker forms the cornerstone of '
     'first-line therapy, with diuretics for symptomatic volume overload and a '
     'mineralocorticoid-receptor antagonist added in more advanced disease.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' Can we use quinidine to control AF in this case?', None, None,
     'No — quinidine displaces digoxin from tissue-binding sites and reduces its '
     'renal clearance, raising serum digoxin levels and worsening the existing '
     'toxicity, so it is contraindicated here.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' What is the role of anticoagulants in cases of AF?', None, None,
     'Anticoagulation (e.g. warfarin or a DOAC) reduces the risk of atrial thrombus '
     'formation and embolic stroke, which is markedly increased in atrial '
     'fibrillation, especially with underlying rheumatic valve disease.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' Correction of AF is best done using what approach?', None, None,
     'Rate control (beta-blocker or a non-dihydropyridine CCB) or, if needed, rhythm '
     'control with electrical or pharmacological (e.g. amiodarone) cardioversion '
     'after adequate anticoagulation.',
     TAG_PHARM1, 'Pharmacology'),
    (V_DIGOXIN + ' How can we prevent the recurrence of AF?', None, None,
     'Long-term antiarrhythmic therapy (e.g. amiodarone), treatment of the '
     'underlying cause (rheumatic valve disease), ongoing rate/rhythm control, and '
     'continued anticoagulation to prevent thromboembolism.',
     TAG_PHARM1, 'Pharmacology'),

    # --- GD 2a: Myocardial infarction cases (Anatomy) — Case 1: coronary MCQ ---
    (V_MI_ANAT1 + ' Stenosis of which of the following arteries would most likely '
     'cause this condition?',
     ['Acute marginal artery', 'Circumflex artery', 'Left anterior descending artery',
      'Posterior descending artery', 'Right coronary artery'], 'E',
     'The posterior third of the interventricular septum is supplied by the '
     'posterior descending (interventricular) artery, which in the ~85% of people '
     'who are right-dominant arises from the right coronary artery — so RCA is the '
     'single best-answer vessel whose stenosis produces this posterior-septal wall '
     'motion abnormality.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT1 + ' What does the left anterior descending (LAD or anterior '
     'interventricular) coronary artery supply?', None, None,
     'The LAD supplies the anterior two-thirds of the interventricular septum, the '
     'anterior wall of the left ventricle and the apex of the heart, via its septal '
     'perforator and diagonal branches.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT1 + ' What branches come off the LAD?', None, None,
     'Septal perforator branches, which supply the anterior two-thirds of the '
     'interventricular septum, and diagonal branches, which supply the anterolateral '
     'wall of the left ventricle.',
     TAG_ANAT2, 'Anatomy'),

    # --- GD 2a: Myocardial infarction cases (Anatomy) — Case 2 ---
    (V_MI_ANAT2 + ' Which artery is most likely occluded?',
     ['Left anterior descending', 'Left circumflex', 'Left main coronary',
      'Right coronary'], 'B',
     'The lateral wall of the left ventricle is supplied by the obtuse marginal '
     'branches of the left circumflex artery, so reduced perfusion there localizes '
     'the occlusion to the left circumflex.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT2 + ' What is the anatomical basis of the referred cardiac pain?',
     None, None,
     'Cardiac nociceptive afferents travel with sympathetic fibers back to spinal '
     'cord segments T1-T4/T5, converging on the same dorsal horn neurons that '
     'receive somatic afferents from the chest wall and medial (ulnar side of the) '
     'left arm; the brain cannot distinguish the two inputs, so the pain is '
     'perceived as arising from those somatic dermatomes (referred pain) rather '
     'than the heart itself.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT2 + ' Name the branches of the right coronary arteries?', None, None,
     'The SA nodal artery, the right (acute) marginal artery, the AV nodal artery, '
     'and — in right-dominant hearts — the posterior descending (interventricular) '
     'artery, together with smaller branches to the right atrium and right '
     'ventricle.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT2 + ' What is the meaning of the right and left coronary dominance? '
     'What arteries of the heart are most commonly occluded? Why do occlusions '
     'rapidly lead to infarct in the heart?', None, None,
     'Coronary dominance refers to which artery gives rise to the posterior '
     'descending artery supplying the posterior third of the septum and the '
     'diaphragmatic surface: right-dominant (~85%, from the RCA), left-dominant '
     '(~8%, from the LCx), or codominant (~7%, from both). The left anterior '
     'descending artery is the vessel most commonly occluded, because it supplies '
     'the largest territory of myocardium (anterior wall, anterior septum and '
     'apex). Occlusions cause rapid infarction because the coronary arteries are '
     'functional end-arteries with poor pre-existing collateral supply, so an '
     'abrupt occlusion leaves the downstream myocardium acutely and severely '
     'ischemic within minutes.',
     TAG_ANAT2, 'Anatomy'),

    # --- GD 2a: Myocardial infarction cases (Anatomy) — Case 3 ---
    (V_MI_ANAT3 + ' Which artery supplies the papillary muscles?', None, None,
     'The anterolateral papillary muscle has a dual blood supply from the LAD '
     '(diagonal branches) and the left circumflex (marginal branches), while the '
     'posteromedial papillary muscle has a single blood supply, usually from the '
     'posterior descending artery — which is why it is more vulnerable to '
     'ischemic rupture; the anterior papillary muscle rupture described here '
     'follows the LAD occlusion given in the vignette.',
     TAG_ANAT2, 'Anatomy'),
    (V_MI_ANAT3 + ' What is the significance of the papillary muscles? Describe the '
     'interior features of the right atrium and right ventricle of the heart.',
     None, None,
     'The papillary muscles anchor the chordae tendineae to the atrioventricular '
     'valve cusps, preventing the cusps from prolapsing or everting into the atria '
     'during ventricular systole; their ischemic rupture (as here) causes acute, '
     'severe atrioventricular valve regurgitation. Right atrium: a smooth posterior '
     'wall (sinus venarum) and a rough anterior wall (pectinate muscles) separated '
     'by the crista terminalis, with the openings of the superior and inferior '
     'venae cavae (the latter guarded by the valve of the IVC), the coronary sinus '
     '(guarded by its own valve), and the fossa ovalis on the interatrial septum. '
     'Right ventricle: trabeculae carneae line its walls, the moderator band '
     '(septomarginal trabecula, carrying the right bundle branch) crosses to the '
     'anterior papillary muscle, and the supraventricular crest separates the '
     'smooth-walled infundibulum (conus arteriosus, leading to the pulmonary valve) '
     'from the trabeculated inflow guarded by the tricuspid valve and its papillary '
     'muscles/chordae tendineae.',
     TAG_ANAT2, 'Anatomy'),

    # --- GD 2a: Myocardial infarction cases (Anatomy) — Case 4 ---
    (V_PULSE + ' Mention name and location of the arteries which their pulsation can '
     'be palpated in the body.', None, None,
     'Superficial (superficial temporal, in front of the tragus of the ear), facial '
     '(along the lower border of the mandible, at the anterior edge of the masseter), '
     'common carotid (in the neck, lateral to the larynx/thyroid cartilage), '
     'subclavian (in the supraclavicular fossa), axillary (in the axilla), brachial '
     '(medial to the biceps tendon in the cubital fossa/medial arm), radial (lateral '
     'wrist, over the distal radius), ulnar (medial wrist, over the distal ulna), '
     'femoral (at the mid-inguinal point, below the inguinal ligament), popliteal '
     '(deep in the popliteal fossa behind the knee), posterior tibial (behind the '
     'medial malleolus) and dorsalis pedis (dorsum of the foot, between the first and '
     'second metatarsals) — these palpable pulses matter clinically for assessing '
     'this patient\'s circulatory (hypovolemic-shock) status at the bedside.',
     TAG_ANAT2, 'Anatomy'),

    # --- GD 2b: Ischemic heart cases (Pathology) — Case 1 ---
    (V_OLDMAN + ' What is the diagnosis?', None, None,
     'Acute myocardial infarction — coagulative necrosis of the myocardium '
     'following coronary occlusion, consistent with sudden cardiac death and a '
     'pale, soft infarcted area at autopsy.',
     TAG_PATH2, 'Pathology'),
    (V_OLDMAN + ' What is the part of the heart expected to show the mentioned '
     'pathology? Why?', None, None,
     'The left ventricular wall (most often its anterior wall, in LAD territory), '
     'because the left ventricle has the highest workload and myocardial oxygen '
     'demand of any cardiac chamber, and its subendocardial region is the '
     'watershed zone most vulnerable to a compromised coronary blood supply.',
     TAG_PATH2, 'Pathology'),
    (V_OLDMAN + ' Discuss the pathogenesis of this condition.', None, None,
     'An atherosclerotic plaque in a coronary artery ruptures or fissures, exposing '
     'thrombogenic subendothelial collagen and lipid core; platelet adhesion/'
     'aggregation and activation of the coagulation cascade form an occlusive '
     'thrombus. The abrupt loss of blood flow causes myocardial ischemia that '
     'progresses to irreversible coagulative necrosis if flow is not restored '
     'within roughly 20-40 minutes, beginning in the vulnerable subendocardium and '
     'extending outward to become transmural with more prolonged occlusion.',
     TAG_PATH2, 'Pathology'),
    (V_OLDMAN + ' If the patient did not die, describe the gross and microscopic '
     'changes that occur in the affected area of the heart.', None, None,
     'Gross: 0-24 hours — usually normal or with dark mottling; 1-3 days — pale '
     'yellow-tan infarct with a hyperemic border; 3-7 days — the infarct centre is '
     'maximally soft and yellow (as in this case) with a hemorrhagic red-brown rim; '
     '1-2 weeks — a depressed red-gray granulation-tissue border; 2-8 weeks — '
     'progressive replacement by a gray-white fibrous scar. Microscopic: coagulative '
     'necrosis with loss of nuclei and striations becomes visible by 4-24 hours; a '
     'dense neutrophilic infiltrate appears at 1-3 days; macrophages remove necrotic '
     'debris and granulation tissue (fibroblasts, new capillaries, myofibroblasts) '
     'forms by 1-2 weeks; and a dense, collagenous, relatively acellular scar is '
     'complete by about 2 months.',
     TAG_PATH2, 'Pathology'),

    # --- GD 2b: Ischemic heart cases (Pathology) — Case 2 (polyarteritis nodosa) ---
    (V_POLYARTERITIS + ' What is the diagnosis', None, None,
     'Polyarteritis nodosa — a necrotizing vasculitis of small- and medium-sized '
     'muscular arteries, classically presenting with fever of unknown origin, '
     'hypertension (from renal artery involvement) and angiographically visible '
     'nodular arterial aneurysms/swellings.',
     TAG_PATH2, 'Pathology'),
    (V_POLYARTERITIS + ' Mention effects of this disease', None, None,
     'Renal artery involvement causes renin-mediated hypertension and renal '
     'infarction/impairment; mesenteric artery involvement causes abdominal pain, '
     'bowel ischemia and even perforation; coronary artery involvement can cause '
     'myocardial infarction; peripheral nerve artery involvement causes mononeuritis '
     'multiplex; skin artery involvement causes subcutaneous nodules, livedo '
     'reticularis and ulcers; and the weakened aneurysmal arterial wall can rupture, '
     'causing potentially fatal hemorrhage.',
     TAG_PATH2, 'Pathology'),

    # --- GD 2b: Ischemic heart cases (Pathology) — Case 3 (varicose veins) ---
    (V_VARICOSE + ' What is the diagnosis', None, None,
     'Varicose veins — dilated, elongated, tortuous superficial leg veins resulting '
     'from incompetence of their valves, which allows venous reflux and sustained '
     'venous hypertension.',
     TAG_PATH2, 'Pathology'),
    (V_VARICOSE + ' Mention the complications of this condition and enumerate which '
     'one of these complications could be fatal and How?', None, None,
     'Complications include superficial thrombophlebitis, venous (stasis) eczema and '
     'hyperpigmentation from hemosiderin deposition, lipodermatosclerosis, chronic '
     'venous (stasis) ulceration, and hemorrhage from a ruptured varix. The most '
     'dangerous complication is deep vein thrombosis with pulmonary embolism, which '
     'can be fatal: a thrombus forms in (or propagates into) the deep venous system, '
     'dislodges, and travels via the inferior vena cava and right heart to lodge in '
     'the pulmonary arteries, obstructing pulmonary blood flow and causing acute '
     'right heart strain, hypoxia and, if massive, sudden cardiovascular collapse '
     'and death.',
     TAG_PATH2, 'Pathology'),

    # --- GD 3: Hemorrhage and Shock cases (Physiology) ---
    (V_HYPOVOL + ' What is the most likely diagnosis in this patient, and what is '
     'its underlying cause?', None, None,
     'Hypovolemic shock from acute lower gastrointestinal (diverticular) '
     'hemorrhage, aggravated by her heavy aspirin use, which impairs platelet '
     'function and predisposes to bleeding.',
     TAG_PHYS3, 'Physiology'),
    ('What is the definition of circulatory shock? What are the major causes?',
     None, None,
     'Shock is a state of inadequate tissue perfusion relative to metabolic demand, '
     'leading to cellular hypoxia. Major categories are hypovolemic (hemorrhage, '
     'fluid loss), cardiogenic (pump failure), obstructive (tamponade, pulmonary '
     'embolism), and distributive (septic, anaphylactic, neurogenic) shock.',
     TAG_PHYS3, 'Physiology'),
    (V_HYPOVOL + ' After the gastrointestinal blood loss, what sequence of events led '
     'to her decreased arterial pressure?', None, None,
     'Blood loss reduces venous return and thus cardiac preload and stroke volume, '
     'lowering cardiac output and arterial pressure; the resulting fall in arterial '
     'pressure unloads the arterial baroreceptors, triggering reflex sympathetic '
     'activation.',
     TAG_PHYS3, 'Physiology'),
    (V_HYPOVOL + ' Why was her arterial pressure lower in the upright position than '
     'in the lying (supine) position?', None, None,
     'Standing lets gravity pool additional blood in the dependent leg veins, further '
     'reducing venous return and preload in an already volume-depleted patient, which '
     'drops stroke volume and arterial pressure even further (orthostatic '
     'hypotension).',
     TAG_PHYS3, 'Physiology'),
    (V_HYPOVOL + ' Her heart rate was elevated (105/min) when supine. Why? Why was it '
     'even more elevated (135/min) when upright?', None, None,
     'Baroreceptor-mediated reflex tachycardia compensates for the reduced stroke '
     'volume to help preserve cardiac output; standing further reduces venous return '
     'and unloads the baroreceptors even more, driving a still greater compensatory '
     'tachycardia.',
     TAG_PHYS3, 'Physiology'),
    (V_HYPOVOL + ' Why was her hematocrit decreased, and why was this decrease '
     'potentially dangerous?', None, None,
     'Ongoing loss of whole blood, together with dilution from IV saline and '
     'interstitial fluid shifting into the vasculature, lowers the hematocrit; a low '
     'hematocrit reduces the blood\'s oxygen-carrying capacity, compounding the '
     'tissue hypoxia already caused by hypoperfusion.',
     TAG_PHYS3, 'Physiology'),
    (V_HYPOVOL + ' Why was her skin pale and cold?', None, None,
     'Reflex sympathetic vasoconstriction shunts blood away from the skin (and other '
     'non-vital vascular beds) to preserve perfusion of the brain and heart, '
     'producing pallor and cool extremities.',
     TAG_PHYS3, 'Physiology'),
    ('Compare skin temperature in hypovolemic shock and septic shock.', None, None,
     'In hypovolemic (and cardiogenic) shock the skin is cold and clammy because of '
     'compensatory vasoconstriction, whereas in early (warm/distributive) septic '
     'shock the skin is often warm and flushed from inflammatory vasodilation, '
     'though late, decompensated septic shock can also become cold and mottled.',
     TAG_PHYS3, 'Physiology'),
    (V_SEPTIC + ' What is the most likely diagnosis, and what supports it?', None, None,
     'Septic shock secondary to a post-operative infection: fever, tachycardia, '
     'tachypnea and hypotension five days after a major operation are consistent '
     'with an evolving surgical-site or systemic infection progressing to sepsis.',
     TAG_PHYS3, 'Physiology'),
    ('What is meant by septic shock?', None, None,
     'A form of distributive shock caused by a dysregulated systemic response to '
     'infection, producing profound vasodilation, capillary leak and hypotension '
     'that persists despite adequate fluid resuscitation, requiring vasopressor '
     'support.',
     TAG_PHYS3, 'Physiology'),
    ('Mention other types of distributive shock.', None, None,
     'Anaphylactic shock (IgE-mediated massive histamine release) and neurogenic '
     'shock (loss of sympathetic vasomotor tone, e.g. after spinal cord injury); '
     'toxic shock syndrome is another example.',
     TAG_PHYS3, 'Physiology'),
    (V_SEPTIC + ' Explain the increased heart rate in this case.', None, None,
     'Sympathetic activation compensates for the profound vasodilation and relative '
     'hypovolemia of sepsis, and the fever itself directly raises the sinus node\'s '
     'firing rate.',
     TAG_PHYS3, 'Physiology'),
    ('What is the relation between heart rate and temperature?', None, None,
     'Heart rate rises by roughly 10 beats/min for every 1°C rise in body '
     'temperature, because fever increases metabolic rate and sympathetic tone at '
     'the SA node.',
     TAG_PHYS3, 'Physiology'),
    (V_SEPTIC + ' Explain the hypotension in this case.', None, None,
     'Septic shock produces hypotension through widespread inflammatory, '
     'cytokine/nitric-oxide-mediated vasodilation that lowers systemic vascular '
     'resistance, together with capillary leak that reduces effective circulating '
     'volume.',
     TAG_PHYS3, 'Physiology'),

    # --- GD 4: Heart failure cases (Physiology) — Case 1 ---
    ('A 45-year-old man presented with severe lower-limb edema, dyspnea and other '
     'symptoms of congestive heart failure. What type of heart failure does this most '
     'likely represent?', None, None,
     'Predominantly right-sided (or biventricular) congestive heart failure: '
     'systemic venous congestion produces the dependent lower-limb edema, while '
     'concurrent left-sided/pulmonary involvement contributes to the dyspnea.',
     TAG_PHYS4, 'Physiology'),
    (V_HF1 + ' Explain the causes of edema in the lower limb in this case.', None, None,
     'Right heart failure raises systemic venous and capillary hydrostatic pressure, '
     'and the reduced cardiac output activates the renin-angiotensin-aldosterone '
     'system, causing salt and water retention; both effects push fluid into the '
     'interstitium of the dependent legs.',
     TAG_PHYS4, 'Physiology'),
    (V_HF1 + ' What is the mechanism of dyspnea in this case?', None, None,
     'Left-sided (or combined) failure raises pulmonary capillary hydrostatic '
     'pressure, causing interstitial and alveolar fluid accumulation that stiffens '
     'the lungs and impairs gas exchange, producing dyspnea.',
     TAG_PHYS4, 'Physiology'),
    ('Mention the causes of right heart failure.', None, None,
     'Left heart failure is the most common cause (via chronic pulmonary venous '
     'congestion), followed by chronic lung disease/pulmonary hypertension (cor '
     'pulmonale), pulmonic or tricuspid valve disease, and right ventricular '
     'infarction.',
     TAG_PHYS4, 'Physiology'),
    ('What is meant by compensated heart failure?', None, None,
     'A state in which cardiac output and tissue perfusion are maintained, usually '
     'at rest, through compensatory mechanisms — sympathetic activation, RAAS '
     'activation, and ventricular hypertrophy/remodeling — even though these '
     'mechanisms raise filling pressures and predispose to eventual decompensation.',
     TAG_PHYS4, 'Physiology'),

    # --- GD 4: Heart failure cases (Physiology) — Case 2 ---
    (V_HF2 + ' Explain the reduced ejection fraction in this case.', None, None,
     'Myocardial infarction destroys contractile tissue in the affected wall, '
     'reducing the force of ventricular contraction, so a smaller fraction of '
     'end-diastolic volume is ejected with each beat.',
     TAG_PHYS4, 'Physiology'),
    (V_HF2 + ' Mention the causes of left-sided heart failure.', None, None,
     'Ischemic heart disease/myocardial infarction, hypertension, aortic and mitral '
     'valve disease, and dilated cardiomyopathy.',
     TAG_PHYS4, 'Physiology'),
    (V_HF2 + ' Explain why right-sided failure can occur in this case.', None, None,
     'Extensive left ventricular infarction raises left atrial and pulmonary venous '
     'pressure, producing pulmonary hypertension that increases right ventricular '
     'afterload and can precipitate right heart failure (or, if the infarct extends '
     'to the RV, direct right ventricular involvement can do the same).',
     TAG_PHYS4, 'Physiology'),

    # --- GD 4: Heart failure cases (Physiology) — Case 3 (JVP, Lt-sided failure) ---
    (V_JVP + ' Mention the relation between arterial blood pressure and heart rate.',
     None, None,
     'Via the baroreceptor reflex, arterial pressure and heart rate normally vary '
     'inversely in the short term — a fall in arterial pressure unloads the '
     'baroreceptors and reflexly raises heart rate (and contractility) to help '
     'restore pressure, while a rise in pressure reflexly slows heart rate. More '
     'directly, mean arterial pressure = cardiac output × total peripheral '
     'resistance, and cardiac output = heart rate × stroke volume, so a sustained '
     'tachycardia (without an offsetting fall in stroke volume or resistance) '
     'raises arterial pressure — consistent with this patient\'s tachycardia (120/'
     'min) and hypertension (160/100 mmHg).',
     TAG_PHYS4, 'Physiology'),
    (V_JVP + ' Mention the causes of heart failure in this case.', None, None,
     'Long-standing, poorly-controlled hypertension (chronic pressure overload/'
     'afterload driving left ventricular hypertrophy) and chronic smoking '
     '(accelerating coronary atherosclerosis) have culminated in an acute '
     'myocardial infarction that acutely impairs left ventricular contractility — '
     'together producing left-sided heart failure, with the elevated JVP reflecting '
     'the resulting secondary systemic venous congestion.',
     TAG_PHYS4, 'Physiology'),
]


def main():
    qs = []
    for stem, options, correct, exp, tag, subj in ITEMS:
        qs.append(Q(stem, options, correct, 'derived', exp=exp, tag=tag, tag_suggere=subj))
    meta = {'Source file': SRC,
            'Type': 'GD case handout, 7 pages; 4 G.D. sessions across Pharmacology, '
                    'Anatomy, Pathology and Physiology',
            'Tag': 'Department, GDs, <Subject> GD <N>', 'tagSuggere': 'varies by item',
            'Year': 'None',
            'Answer source': 'derived — no key is printed anywhere in the source'}
    n = write_md(OUT, 'Source 10 — GD Week 4 Cases', meta, qs)
    mcq = sum(1 for s, o, c, e, t, sj in ITEMS if o)
    ans = collections.Counter(c for s, o, c, e, t, sj in ITEMS if o)
    print(f'source 10: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: option-A blocks = {mcq}; ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({mcq} MCQs — bias gate n/a, <15)')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
