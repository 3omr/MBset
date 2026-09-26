#!/usr/bin/env python3
"""Source 09 — GD/3rd week-CVS-206 cases.pdf.

Six G.D. sessions (Histology / Anatomy / Biochemistry / Pathology / Physiology /
Pharmacology), 11 pages.

This file is re-derived from the FIXED lib_gd.py parser, which recognizes
bulleted ("-"/"•") sub-questions, vignette-embedded MCQs, and "Qn:"
numbering in addition to the "N-" numbered sub-questions the original parser
required. Re-parsing with the fixed parser (see scripts/../parse_09.txt used
to build this file) recovers G.D. 2 (Anatomy, congenital great-vessel
anomalies), G.D. 3 (Biochemistry, dyslipidemia) and G.D. 4 (Pathology,
hypertension), which the old 29-item version of this script dropped entirely
along with three of G.D. 5's four cases and one MCQ embedded directly in a
G.D. 1 vignette.

RE-VERIFICATION (2026-09-16) against a SECOND lib_gd.py fix: the BULLET rule
used to require a bulleted sub-question to end in "?" or ":", which silently
dropped every bulleted question that ended in a plain full stop or no
punctuation at all. Re-parsing with the twice-fixed parser yields 63 raw rows
(scripts/../parse2_09.txt) instead of the 47 the previous fix produced. Every
one of the 63 rows was matched by hand, content-for-content, against the 54
ITEMS below (verified two ways: a manual line-by-line reconciliation against
`pdftotext -layout` of the source PDF, and an automated keyword-overlap check
of all 63 STEM lines against this file's text — every row scores >=60%
distinctive-word overlap with an existing item). Result: **no new items were
needed** — all 63 rows were already represented, because:
  - The 11 extra rows the second parser fix newly recovers (63 vs the
    previous fix's 47, before the 3 hand-added no-cue cases below) are all
    un-numbered bare "-"/"•" sub-questions that this script's original
    author had *already* manually recovered and folded into a single
    combined written item per case (see judgement call 4) — the parser
    catching up to a fix that was already applied by hand does not add new
    content, it only lets the parser stop silently dropping what the
    hand-curation had already restored.
  - The 3 cases with no bulleted/numbered cue at all (G.D. 3 Case 1, G.D. 3
    Case 3, and G.D. 5 Case 1 — see judgement call 3) still produce zero
    parser chunks even with the twice-fixed parser, because they use bare
    narrative prose with no cue character whatsoever; they remain the 3
    items added here directly from the source text.
  - 52 (of the 63 raw rows, combined per the case-grouping convention in
    judgement call 4) + the pre-existing 3 no-cue additions = the same 54
    total this script already had. See judgement calls 1-5 below for the
    per-case reasoning; nothing has changed except confirming, against the
    now-fully-fixed parser, that it agrees with the hand curation.

Judgement calls made while reconciling the fixed parser's 47 raw chunks
against the source text directly (`pdftotext -layout`):

1. As in source 07/08/10, the "G.D. (N): title (Subject)" label is a running
   FOOTER for the block it names, so raw forward attribution mis-tags several
   items; subjects/GD numbers below are verified against each item's actual
   content and the case-block headers in the source, not the parser's
   forward guess.
2. The fixed parser still has two remaining defects, both fixed here by hand:
   (a) a trailing bare "-" bulleted sub-question is sometimes swallowed into
   the text of an MCQ's LAST option instead of starting a new item (G.D. 2
   Case 3's "aortic arch" MCQ, G.D. 2 Case 7's "DiGeorge" MCQ, and G.D. 4
   Case 1's "coronary atherosclerosis" MCQ all have this bug) — the glued
   tail is split out into its own separate written item in each case;
   (b) pdftotext glues adjacent option letters into one token across a
   column break (b.Familialhypercholesterolemia, Type 2diabetes,
   "phagocytosis I. pinocytosis J. receptor-mediated endocytosis") — fixed
   by reading the option list back from the raw text.
3. Three cases have NO bulleted/numbered cue at all — just a bare closing
   sentence after the vignette — so even the twice-fixed parser (63-row
   parse2_09.txt) produces zero chunks for them, and they are added here
   from the source text directly (never silently drop a question that is in
   the source): G.D. 3 Case 1 ("write your biochemical report on this
   case"), G.D. 3 Case 3 (cardiac markers over 3 h/24 h/72 h), and G.D. 5
   Case 1 (ABP definitions and reflexes). [Correction from the earlier
   version of this note: G.D. 2 Case 6 ("name the branches of the ascending
   aorta and aortic arch") DOES carry a bare "-" cue in the source
   ("-Name the branches of the ascending and arch of aorta.") and IS
   recovered directly by the twice-fixed parser as row 19 of
   parse2_09.txt — it was never actually a no-cue case, it only looked like
   one against the older, less-fixed parser.] These 3 genuinely-uncued cases
   bring the true count to 54 rather than the raw parser's 47 (at the time
   this script was first written) or 63 (after both parser fixes, before
   case-grouping — see the re-verification note above); nothing beyond what
   is actually printed on the page is added, and nothing printed on the page
   is dropped.
4. Where the source bundles several bare "-"/"•" sub-questions with no
   numbering into one prompt (e.g. G.D. 2 Case 1's "four abnormalities /
   other cyanotic causes", G.D. 4 Case 2's "diagnosis / causes / cause of
   death"), they are kept as ONE combined written item with a multi-part
   EXP, matching how the fixed parser itself treats every other instance of
   this exact pattern in this source (it only starts a new item on an
   explicit number such as "1-", "2.", "Q1:").
5. GD 6's two cases (hyperlipidemia, then hydralazine/hypertension) both sit
   before the GD 6 header and are correctly Pharmacology/GD 6 (not
   Physiology/GD 5, which a naive forward-footer read would suggest).

No answer key is printed anywhere in the source; every answer is `derived`.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '09_GD_Week_3_Cases.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/3rd week-CVS-206 cases.pdf'

# ---------------------------------------------------------------- G.D. 1 ---
V_ATHERO = ('In sections of coronary arteries from a patient who died of a heart '
            'attack, a pathologist finds the endothelium of the right coronary artery '
            'intact, but the lumen almost completely occluded by a thickened tunica '
            'intima containing a necrotic core of lipid material and cell debris.')

V_MI = ('A 45-year-old man had been well until he was awakened by chest pain radiating '
        'to both arms and neck, associated with diaphoresis. His blood pressure was '
        '160/110. He was treated with diuretics (furosemide) but continued to gain '
        'weight. Two days after the onset of chest pain he had a cardiac arrest and '
        'died; he had been diagnosed with myocardial infarction.')

# ---------------------------------------------------------------- G.D. 2 ---
V_TOF = ('A 5-year-old boy is seen in the emergency department after an attack of '
         'breathlessness during which he lost consciousness. His mother says he has '
         'had several such attacks before and that his skin turns blue. '
         'Echocardiography shows tetralogy of Fallot.')

V_CLAUD = ('A 48-year-old obese man presents with lower-leg pain that occurs after '
           'walking a few city blocks and is relieved by rest. His blood pressure is '
           '165/85 mmHg, pulse 83/min, respiratory rate 18/min, and he admits to '
           'smoking two packs of cigarettes a day.')

V_CAROTID = ('A 73-year-old man with a history of hypertension and type II diabetes '
             'mellitus presents with sudden-onset right-sided paralysis. Ultrasound '
             'shows significant atherosclerosis of the internal carotid artery.')

V_COARCT = ('On examination, the upper body of a 7-year-old boy is much more '
            'developed than his lower body. Blood pressure in the upper extremities '
            'exceeds that in the lower extremities, the lower extremities are cold, '
            'and femoral pulses are absent.')

V_VRING = ('A patient complains of difficulty swallowing and difficulty breathing. A '
           'barium contrast study shows constriction of the esophagus at the level of '
           'the third thoracic vertebra, and an aortogram shows a vascular ring '
           'around the trachea and esophagus.')

V_ANEURYSM = ('A 39-year-old woman has dilation of the ascending aorta due to an '
              'aneurysm (a weakness in the vessel wall).')

V_DIGEORGE = ('Two days after an uneventful delivery, a female infant develops '
              'intermittent respiratory distress and cyanosis. Cultures are positive '
              'for bacterial infection and broad-spectrum antibiotics are begun. The '
              'infant remains hypocalcemic and hyperphosphatemic despite a calcium '
              'gluconate infusion. Examination shows an acutely ill infant with '
              'low-set ears and midface hypoplasia. Chest x-ray shows bilateral '
              'perihilar infiltrates with no thymic shadow, and chromosomal analysis '
              'reveals a 22q11.2 deletion.')

# ---------------------------------------------------------------- G.D. 3 ---
V_LIPIDPROFILE = ('A 50-year-old diabetic patient attends a routine health check-up. '
                   'His lipid profile shows total cholesterol 310 mg/dl, HDL 30 '
                   'mg/dl, LDL 200 mg/dl, and triglycerides 210 mg/dl.')

V_STATIN = ('A 62-year-old man is prescribed a drug that inhibits the enzyme '
            'HMG-CoA reductase.')

V_CARDIACMARKERS = 'A patient presents with ischemic chest discomfort.'

V_XANTHOMA = ('A 22-year-old woman presents with a fusiform swelling of the Achilles '
              'tendon that, on biopsy, shows cholesterol-laden macrophages (foam '
              'cells) among the collagen fibers. She has had joint pains for several '
              'years, and both parents developed arthritis with xanthomas starting in '
              'middle age. She is referred to a nutritionist and treated with an '
              'enzyme inhibitor.')

V_MI_MARKERS = ('A 48-year-old man with a history of hypertension and high '
                 'cholesterol presents to the emergency department with chest pain '
                 'for 60 minutes, described as a substernal pressure "like an '
                 'elephant on my chest," with shortness of breath and diaphoresis. '
                 'His ECG shows ST elevations consistent with myocardial infarction.')

V_LDLUPTAKE = ('Liver cells in culture were kept at 0°C and treated with trypsin '
               'to digest the receptors on the cell surface. The temperature was then '
               'raised to 37°C and radioactive LDL was added to the culture '
               'medium. Several hours later the labeled LDL was found inside the '
               'cells.')

# ---------------------------------------------------------------- G.D. 4 ---
V_CORONARY_ATHERO = ('A 60-year-old diabetic man suffers repeated attacks of severe '
                      'chest pain. His blood pressure is 200/120 mmHg, laboratory '
                      'investigation shows an increased serum LDL level, and his ECG '
                      'shows signs of inadequate coronary blood flow.')

V_MALIG_HTN = ('A young man suffers from severe headache and blurring of vision. His '
               'blood pressure is 250/160 mmHg, eye examination shows papilloedema, '
               'and urine examination shows proteinuria.')

# ---------------------------------------------------------------- G.D. 5 ---
V_ABP1 = ('A 56-year-old woman arrives in the emergency department complaining of '
          'dizziness and headache. Her blood pressure is 210/140 mmHg. She is not '
          'currently taking any medications and has not seen a doctor in several '
          'years.')

V_RENAL17 = ('A 17-year-old patient complains of severe headache. Blood pressure is '
             '260/160 mmHg. Kidney function tests are abnormal, and there is '
             'narrowing of the left renal artery.')

V_HASAN = ('Hasan is a 77-year-old man presenting to establish care as a new '
           'patient. He complains of increasing frequency of headaches over the '
           'last few weeks. BP 174/88 mmHg, HR 77 beats/min, height 73 inches, '
           'weight 254 lb.')

V_RAS = ('Hosam is a 58-year-old who has smoked two packs of cigarettes a day for 40 '
         'years; his weight is 210 lb (5 ft 9 in tall). His blood pressure was 180/125 '
         '(normal 120/80), with a continuous abdominal bruit on examination. Plasma '
         'renin activity was 10 ng/mL/hr (normal 0.9-3.3), consistent with left renal '
         'artery stenosis.')

# ---------------------------------------------------------------- G.D. 6 ---
V_LIPID = ('An obese woman having a routine check-up has a lipid profile showing serum '
           'triglyceride 250 mg/dl and total serum cholesterol 320 mg/dl.')

V_HYDRA = ('A patient with severe essential hypertension on multiple medications '
           'recently had hydralazine added to his regimen. He now reports flushing and '
           'headaches since starting it.')

TAG_HIST = 'Department, GDs, Histology GD 1'
TAG_ANAT = 'Department, GDs, Anatomy GD 2'
TAG_BIOCHEM = 'Department, GDs, Biochemistry GD 3'
TAG_PATH = 'Department, GDs, Pathology GD 4'
TAG_PHYS = 'Department, GDs, Physiology GD 5'
TAG_PHARM = 'Department, GDs, Pharmacology GD 6'

ITEMS = [
    # ================================================================
    # G.D. 1: Hypertension and atherosclerosis (Histology) — Case 1
    # ================================================================
    (V_ATHERO + ' These findings are most consistent with a diagnosis of:',
     ['atherosclerosis', 'mitral valve insufficiency', 'aneurysm',
      'vessel blockage by an embolism'],
     'A',
     'A thickened intima with a necrotic lipid/debris core narrowing the lumen while '
     'the endothelium stays intact is the defining lesion of an atheromatous plaque, '
     'i.e. atherosclerosis; an embolism would instead show an intraluminal '
     'thromboembolic mass, not intimal thickening.',
     TAG_HIST, 'Histology'),
    (V_ATHERO + ' What are the major layers of the vessel wall?', None, None,
     'An artery wall has three tunics: the tunica intima (endothelium, subendothelial '
     'connective tissue and internal elastic lamina), the tunica media (smooth muscle '
     'and elastic fibers), and the tunica adventitia (connective tissue with vasa '
     'vasorum and nerves).',
     TAG_HIST, 'Histology'),
    (V_ATHERO + ' Which layer is affected in this patient?', None, None,
     'The tunica intima is affected — it is thickened by an atheromatous plaque with a '
     'necrotic lipid core, narrowing the lumen while the endothelium remains grossly '
     'intact; the media is relatively spared at this stage.',
     TAG_HIST, 'Histology'),
    (V_ATHERO + ' How can you differentiate between the different layers of the '
     'wall?', None, None,
     'The intima is the innermost layer, lined by a single endothelial layer and '
     'bounded externally by the internal elastic lamina; the media lies between the '
     'internal and external elastic laminae and is composed mainly of circularly '
     'arranged smooth muscle with elastic fibers; the adventitia is the outermost, '
     'looser connective-tissue layer carrying vasa vasorum and autonomic nerves.',
     TAG_HIST, 'Histology'),

    # G.D. 1 — Case 2
    (V_MI + ' The event most likely associated with this patient\'s problem was:',
     ['Occlusion of a coronary vein', 'Occlusion of a coronary artery',
      'Stabbed with ice pick', 'Broken heart'],
     'B',
     'Sudden cardiac arrest two days after a myocardial infarction most likely '
     'reflects a fatal ventricular arrhythmia triggered by the acute coronary-artery '
     'occlusion itself; coronary veins do not supply the myocardium, so their '
     'occlusion would not cause infarction.',
     TAG_HIST, 'Histology'),
    ('What is the most characteristic histological feature of the coronary artery?',
     None, None,
     'The coronary arteries are muscular (distributing) arteries, characterized by a '
     'thick tunica media of circularly arranged smooth muscle and a prominent '
     'internal elastic lamina, which lets them actively regulate myocardial blood '
     'flow by vasoconstriction/dilation.',
     TAG_HIST, 'Histology'),
    ('Mention other specialized medium-sized (muscular) vessels.', None, None,
     'Other muscular arteries include the radial, femoral, splenic, and renal '
     'arteries — medium-to-small distributing arteries with a thick smooth-muscle '
     'media that regulates blood flow to specific organs and regions.',
     TAG_HIST, 'Histology'),

    # ================================================================
    # G.D. 2: Congenital anomalies of the great vessels (Anatomy)
    # ================================================================
    (V_TOF + ' In tetralogy of Fallot there are four abnormalities — what are '
     'they? What other congenital heart diseases may cause early or late '
     'cyanosis?', None, None,
     'Tetralogy of Fallot comprises: (1) a large ventricular septal defect, (2) '
     'pulmonary infundibular/valvular stenosis causing right ventricular outflow '
     'obstruction, (3) an aorta that overrides the VSD, and (4) right ventricular '
     'hypertrophy secondary to the obstruction. Other causes of early cyanosis '
     'include transposition of the great arteries, truncus arteriosus, and total '
     'anomalous pulmonary venous connection; late (Eisenmenger) cyanosis can develop '
     'in initially acyanotic left-to-right shunts (VSD, ASD, PDA) once pulmonary '
     'vascular resistance rises enough to reverse the shunt.',
     TAG_ANAT, 'Anatomy'),

    (V_CLAUD + ' Which of the following types of vessels is most likely involved '
     'in the pathologic process underlying this patient\'s symptoms?',
     ['Arteries', 'Arterioles', 'Capillaries', 'Veins', 'Venules'],
     'A',
     'Intermittent claudication relieved by rest is the classic presentation of '
     'peripheral artery disease from atherosclerosis of the medium/large muscular '
     'distributing arteries of the lower limb (not arterioles, capillaries or the '
     'venous system).',
     TAG_ANAT, 'Anatomy'),
    (V_CLAUD + ' What are the tributaries of the superior vena cava, and what is '
     'the anatomy of the azygos venous system?', None, None,
     'The superior vena cava is formed by the union of the right and left '
     'brachiocephalic veins and receives the azygos vein just before entering the '
     'right atrium. The azygos vein ascends in the posterior mediastinum along the '
     'right side of the vertebral bodies, arising from the union of the right '
     'ascending lumbar and right subcostal veins, arches over the root of the right '
     'lung to drain into the SVC, and receives the right posterior intercostal '
     'veins, the hemiazygos and accessory hemiazygos veins (which cross the midline '
     'from the left side), the right bronchial veins, and the esophageal and '
     'mediastinal veins.',
     TAG_ANAT, 'Anatomy'),

    (V_CAROTID + ' The internal carotid artery is embryologically derived from '
     'the:',
     ['First aortic arch', 'Second aortic arch', 'Third aortic arch',
      'Fourth aortic arch', 'Sixth aortic arch'],
     'C',
     'The third pharyngeal (aortic) arch artery forms the common carotid artery and '
     'the proximal part of the internal carotid artery; the distal internal carotid '
     'is derived from the dorsal aorta cranial to the third arch.',
     TAG_ANAT, 'Anatomy'),
    (V_CAROTID + ' State the developmental sources of the permanent (definitive) '
     'aortic arch derivatives.', None, None,
     'Of the six paired embryonic aortic arches: the 1st mostly regresses (small '
     'contribution to the maxillary artery); the 2nd mostly regresses (contributes '
     'to the hyoid and stapedial arteries); the 3rd forms the common carotid artery '
     'and the proximal internal carotid artery; the left 4th forms the definitive '
     'arch of the aorta (between the left common carotid and left subclavian '
     'origins), while the right 4th forms the proximal right subclavian artery; the '
     '5th regresses without forming any adult structure; and the 6th forms the '
     'proximal pulmonary arteries, with the left 6th also giving the ductus '
     'arteriosus.',
     TAG_ANAT, 'Anatomy'),

    (V_COARCT + ' What is the possible congenital abnormality causing these '
     'manifestations, what are its main varieties, and what collateral '
     'circulations may help ameliorate it?', None, None,
     'This is coarctation of the aorta. Its two main varieties are preductal '
     '(infantile) coarctation, with narrowing proximal to the ductus arteriosus '
     'and often a patent ductus supplying the lower body, and postductal '
     '(adult/juxtaductal) coarctation, with narrowing near or just distal to the '
     'ligamentum/ductus arteriosus. In postductal coarctation, collateral flow to '
     'the descending aorta develops via the internal thoracic (internal mammary) '
     'artery to the anterior intercostal arteries, which anastomose with the '
     'posterior intercostal arteries, and via the subclavian artery\'s costocervical '
     'and scapular anastomoses — enlargement of these collaterals over time causes '
     'the characteristic rib notching.',
     TAG_ANAT, 'Anatomy'),

    (V_VRING + ' Which of the following developmental abnormalities explains '
     'this finding?',
     ['Abnormal persistence of the right dorsal aorta',
      'Abnormal persistence of the right fourth aortic arch',
      'Abnormal persistence of the right seventh inter-segmental artery',
      'Abnormal persistence of the right sixth aortic arch',
      'Abnormal persistence of the right third aortic arch'],
     'B',
     'A complete vascular ring encircling the trachea and esophagus is classically '
     'caused by a double aortic arch, which results from abnormal persistence of '
     'the right fourth aortic arch (instead of its normal regression), so that both '
     'a right- and left-sided arch form and encircle the trachea/esophagus.',
     TAG_ANAT, 'Anatomy'),

    (V_ANEURYSM + ' Name the branches of the ascending aorta and of the arch of '
     'the aorta.', None, None,
     'The ascending aorta gives off the right and left coronary arteries. The arch '
     'of the aorta gives off, in order from right to left, the brachiocephalic '
     '(innominate) trunk, the left common carotid artery, and the left subclavian '
     'artery.',
     TAG_ANAT, 'Anatomy'),

    (V_DIGEORGE + ' Which of the following findings is best correlated with '
     'this disorder?',
     ['Biventricular hypertrophy', 'Conotruncal defects', 'Mitral valve prolapse',
      'Pulmonary valve stenosis', 'Tortuous internal carotid arteries'],
     'B',
     'DiGeorge syndrome (22q11.2 deletion) disrupts neural-crest-derived pharyngeal '
     'arch development and classically produces conotruncal cardiac defects (e.g. '
     'tetralogy of Fallot, truncus arteriosus, interrupted aortic arch) together '
     'with thymic and parathyroid hypoplasia.',
     TAG_ANAT, 'Anatomy'),
    (V_DIGEORGE + ' How would you explain the association of facial '
     'deformities and congenital heart defects in this syndrome?', None, None,
     'Both the facial structures (low-set ears, midface hypoplasia) and the '
     'conotruncal/outflow-tract cardiac structures derive from a shared population '
     'of neural-crest cells that migrate through the pharyngeal arches and pouches. '
     'The 22q11.2 deletion disrupts this single neural-crest-cell population, so '
     'one developmental defect produces the facial, cardiac, thymic and '
     'parathyroid anomalies together.',
     TAG_ANAT, 'Anatomy'),

    # ================================================================
    # G.D. 3: Dyslipidemia cases (Biochemistry)
    # ================================================================
    (V_LIPIDPROFILE + ' Write your biochemical report on this case.', None, None,
     'All values are abnormal: total cholesterol (310 mg/dl) and LDL (200 mg/dl) '
     'are markedly elevated and atherogenic, HDL (30 mg/dl) is low and so provides '
     'less reverse-cholesterol-transport protection, and triglycerides (210 mg/dl) '
     'are elevated — an overall mixed (combined) dyslipidemia with a high '
     'LDL/HDL ratio. In a diabetic patient this pattern carries significant '
     'cardiovascular risk and warrants lifestyle modification together with statin '
     'therapy (± a fibrate for the triglycerides).',
     TAG_BIOCHEM, 'Biochemistry'),

    (V_STATIN + ' This patient most likely has which of the following '
     'conditions?',
     ['Chronic inflammation', 'Familial hypercholesterolemia', 'Hypertension',
      'Hyperuricemia', 'Type 2 diabetes'],
     'B',
     'HMG-CoA reductase inhibitors (statins) are prescribed to lower markedly '
     'elevated LDL cholesterol, the hallmark of familial hypercholesterolemia; '
     'none of the other listed conditions is a primary statin indication.',
     TAG_BIOCHEM, 'Biochemistry'),

    (V_CARDIACMARKERS + ' Which cardiac-marker enzymes would you order to '
     'assist in the diagnosis? Compare and contrast the enzyme pattern if the '
     'process has been going on for 3 hours, 24 hours, or 72 hours, and explain '
     'the various enzymes that might be elevated during the course of an '
     'infarction.', None, None,
     'The standard cardiac markers are myoglobin, CK-MB, and troponin I/T. '
     'Myoglobin rises earliest (1-4 h) but is not cardiac-specific and normalizes '
     'by about 24 h. CK-MB rises at 4-6 h, peaks around 24 h, and normalizes by '
     '48-72 h, which makes it useful for detecting reinfarction. Troponin rises '
     'later, at 3-4 h, peaks at 24-48 h, but stays elevated for 7-10 days. So at '
     '3 hours mainly myoglobin (and early troponin) may be elevated; at 24 hours '
     'both troponin and CK-MB are typically high while myoglobin has already '
     'fallen; and at 72 hours troponin remains elevated while CK-MB has usually '
     'returned to normal.',
     TAG_BIOCHEM, 'Biochemistry'),

    (V_XANTHOMA + ' Which of the following is most likely elevated in the '
     'blood of this woman?',
     ['Chylomicron remnants', 'Chylomicrons', 'High density lipoproteins (HDL)',
      'Low density lipoproteins (LDL)', 'Very low density lipoproteins (VLDL)'],
     'D',
     'Tendon xanthomas with foam cells and a family history of premature '
     'arthritis/xanthomas, treated with an enzyme inhibitor (a statin), is '
     'classic familial hypercholesterolemia — an LDL-receptor defect that causes '
     'markedly elevated plasma LDL.',
     TAG_BIOCHEM, 'Biochemistry'),

    (V_MI_MARKERS + ' Which of the following laboratory results would be '
     'expected?',
     ['Elevated myoglobin, elevated troponin I, and elevated CK-MB',
      'Normal myoglobin, elevated troponin I, and normal CK-MB',
      'Elevated myoglobin, normal troponin I, and normal CK-MB',
      'Normal myoglobin, normal troponin I, and elevated CK-MB',
      'Normal myoglobin, normal troponin I, and normal CK-MB'],
     'E',
     'At only 60 minutes after symptom onset, none of the standard cardiac '
     'markers has had time to rise yet — myoglobin (the earliest marker) does not '
     'become detectable until roughly 1-2 hours, and troponin and CK-MB rise '
     'later still — so all three would still be normal at this point.',
     TAG_BIOCHEM, 'Biochemistry'),

    (V_LDLUPTAKE + ' This specific process of LDL uptake is:',
     ['active transport', 'facilitated diffusion', 'phagocytosis', 'pinocytosis',
      'receptor-mediated endocytosis'],
     'E',
     'Destroying surface receptors with trypsin abolishes LDL uptake, showing '
     'uptake depends on cell-surface receptors; LDL binds LDL receptors that '
     'cluster in clathrin-coated pits which then internalize, the defining '
     'mechanism of receptor-mediated endocytosis.',
     TAG_BIOCHEM, 'Biochemistry'),

    # ================================================================
    # G.D. 4: Hypertension cases (Pathology)
    # ================================================================
    (V_CORONARY_ATHERO + ' The most possible diagnosis is:',
     ['Hypertension', 'Coronary embolism', 'Aortic stenosis',
      'Coronary atherosclerosis', 'Coarctation of the aorta'],
     'D',
     'Repeated chest pain with ECG evidence of inadequate coronary flow in a '
     'diabetic, hypertensive patient with elevated LDL points to atherosclerotic '
     'narrowing of the coronary arteries (coronary atherosclerosis) rather than '
     'embolism, valvular disease, or coarctation.',
     TAG_PATH, 'Pathology'),
    (V_CORONARY_ATHERO + ' Enumerate the risk factors for atherosclerosis '
     'mentioned in this case, mention other risk factors for atherosclerosis, '
     'and state the effects of atherosclerosis.', None, None,
     'Risk factors mentioned in the case: diabetes mellitus, hypertension, and '
     'elevated LDL/hyperlipidemia. Other major risk factors include smoking, '
     'obesity, male sex, advancing age, family history, physical inactivity, and '
     'low HDL. Effects of atherosclerosis include narrowing of the vessel lumen '
     'causing ischemia (e.g. angina, claudication), plaque rupture with '
     'thrombosis causing infarction (myocardial infarction, stroke), aneurysm '
     'formation from wall weakening, and embolization of plaque material.',
     TAG_PATH, 'Pathology'),

    (V_MALIG_HTN + ' Renal biopsy will show:',
     ['Hyalinization of the glomeruli', 'Hyalinization of the walls of arterioles',
      'Fibrinoid necrosis of the walls of the arterioles', 'Renal infarction',
      'Necrosis of the renal papillae'],
     'C',
     'Severe headache, blurred vision, papilloedema and markedly elevated blood '
     'pressure (250/160) describe malignant (accelerated) hypertension, whose '
     'characteristic renal lesion is fibrinoid necrosis of the arteriolar walls.',
     TAG_PATH, 'Pathology'),
    (V_MALIG_HTN + ' What is the diagnosis, what are the causes of '
     'hypertension, and what are the causes of death in this disease?', None,
     None,
     'The diagnosis is malignant (accelerated) hypertension. Causes of '
     'hypertension include primary (essential) hypertension and secondary '
     'causes — renal (renal artery stenosis, glomerulonephritis, chronic kidney '
     'disease), endocrine (Cushing syndrome, primary hyperaldosteronism, '
     'phaeochromocytoma), coarctation of the aorta, and pregnancy-related '
     '(pre-eclampsia). Death in malignant hypertension results from complications '
     'such as renal failure, congestive heart failure, cerebral hemorrhage '
     '(hemorrhagic stroke), and aortic dissection.',
     TAG_PATH, 'Pathology'),

    # ================================================================
    # G.D. 5: Cases of ABP (Physiology)
    # ================================================================
    (V_ABP1 + ' Define arterial blood pressure and peripheral resistance and '
     'give their normal values, and explain the reflexes that control arterial '
     'blood pressure.', None, None,
     'Arterial blood pressure (ABP) is the force exerted by circulating blood on '
     'the arterial walls, normally about 120/80 mmHg (mean arterial pressure '
     '≈ 93 mmHg). Peripheral (total peripheral) resistance is the resistance '
     'the systemic vasculature (mainly the arterioles) offers to blood flow, '
     'normally about 20 mmHg·min/L (≈ 1 PRU). ABP is controlled '
     'short-term by the baroreceptor reflex (carotid sinus and aortic arch '
     'baroreceptors sense pressure changes and adjust autonomic outflow to heart '
     'rate, contractility and vascular tone) and the chemoreceptor reflex, and '
     'longer-term by the renin-angiotensin-aldosterone system and other '
     'renal/humoral mechanisms that regulate blood volume.',
     TAG_PHYS, 'Physiology'),

    (V_RENAL17 + ' What is the diagnosis, what are the causes of hypertension '
     'in this case, and how are hypertension and the abnormal kidney function '
     'related?', None, None,
     'The diagnosis is renovascular (secondary) hypertension from left renal '
     'artery stenosis. The narrowed renal artery reduces perfusion pressure '
     'sensed by the juxtaglomerular apparatus, which raises renin secretion; '
     'renin generates angiotensin II, a vasoconstrictor that also stimulates '
     'aldosterone-driven sodium and water retention, both of which raise arterial '
     'pressure. The resulting hypertension and the reduced renal blood flow '
     'together impair glomerular filtration and kidney function, which in turn '
     'perpetuates the abnormal renin-angiotensin activation.',
     TAG_PHYS, 'Physiology'),

    (V_HASAN + ' What is the suggested diagnosis, and what is its type?', None,
     None,
     'The diagnosis is hypertension (BP 174/88 mmHg meets Stage 2 criteria on '
     'the elevated systolic reading). Given his age and the relatively normal '
     'diastolic pressure, this is most consistent with primary (essential), '
     'predominantly isolated systolic hypertension, reflecting age-related loss '
     'of large-artery elastic compliance rather than a secondary cause.',
     TAG_PHYS, 'Physiology'),
    (V_HASAN + ' Explain the relation between heart rate and arterial blood '
     'pressure.', None, None,
     'Mean arterial pressure = cardiac output × total peripheral resistance, '
     'and cardiac output = heart rate × stroke volume, so, all else equal, '
     'an increase in heart rate raises cardiac output and therefore raises '
     'arterial blood pressure; conversely a fall in heart rate lowers cardiac '
     'output and pressure. The baroreflex normally buffers this relationship by '
     'adjusting heart rate in the opposite direction to any pressure change.',
     TAG_PHYS, 'Physiology'),

    (V_RAS + ' How did occlusion of the left renal artery lead to an increase in '
     'plasma renin activity?', None, None,
     'The reduced renal perfusion pressure distal to the stenosis is sensed by the '
     'juxtaglomerular apparatus, which responds by increasing renin secretion in an '
     'attempt to restore glomerular filtration pressure.',
     TAG_PHYS, 'Physiology'),
    (V_RAS + ' How did the increase in plasma renin activity cause an elevation in '
     'arterial blood pressure (renovascular hypertension)?', None, None,
     'Renin cleaves angiotensinogen to angiotensin I, which ACE converts to '
     'angiotensin II — a potent vasoconstrictor that also stimulates aldosterone '
     'secretion, causing sodium and water retention; both actions raise arterial '
     'pressure.',
     TAG_PHYS, 'Physiology'),
    (V_RAS + ' The abdominal bruit was caused by turbulent blood flow through the '
     'stenosed renal artery. Why did narrowing of the artery cause the flow to become '
     'turbulent?', None, None,
     'Once blood velocity through the narrowed lumen exceeds a critical (Reynolds '
     'number) threshold, laminar flow breaks down into turbulent eddies, and this '
     'turbulence generates the audible vibration heard as a bruit.',
     TAG_PHYS, 'Physiology'),

    # ================================================================
    # G.D. 6: Hyperlipidemia and hypertension cases (Pharmacology)
    # ================================================================
    (V_LIPID + ' What is the diagnosis of the case?', None, None,
     'Combined (mixed) hyperlipidemia — both serum triglycerides and total '
     'cholesterol are elevated above normal.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What are the best drugs for the treatment of this case?', None, None,
     'A statin (HMG-CoA reductase inhibitor) is first-line for the elevated '
     'cholesterol; if triglycerides remain markedly high despite statin therapy, a '
     'fibrate can be added.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What is the mechanism of action of statins?', None, None,
     'Statins competitively inhibit HMG-CoA reductase, the rate-limiting enzyme of '
     'hepatic cholesterol synthesis; the resulting fall in intracellular cholesterol '
     'up-regulates hepatic LDL-receptor expression, increasing clearance of LDL from '
     'plasma.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What are the precautions during the use of statins?', None, None,
     'Monitor liver enzymes for hepatotoxicity and creatine kinase for myopathy or '
     'rhabdomyolysis, avoid or dose-adjust with strong CYP3A4 inhibitors '
     '(macrolides, azole antifungals, grapefruit juice, fibrates — especially '
     'gemfibrozil), and avoid in pregnancy.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' Why is cholestyramine not effective alone in the treatment of '
     'hyperlipidemia?', None, None,
     'Bile-acid sequestrants only block intestinal reabsorption of bile acids; the '
     'liver compensates by upregulating cholesterol (and HMG-CoA reductase) '
     'synthesis, which blunts the LDL-lowering effect and can even raise '
     'triglycerides unless combined with a statin.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What is the role of nicotinic acid in the treatment of '
     'hyperlipidemia?', None, None,
     'Niacin inhibits lipolysis in adipose tissue and hepatic triglyceride '
     'synthesis, reducing VLDL (and consequently LDL) production; it is also the '
     'most effective agent available for raising HDL cholesterol.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What is the non-lipid-lowering effect of statins?', None, None,
     'Statins have pleiotropic effects independent of LDL lowering: improved '
     'endothelial function, anti-inflammatory and plaque-stabilizing actions, and '
     'reduced platelet aggregation.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' When does the risk of myopathy increase with statins?', None, None,
     'Risk rises with high statin doses, renal or hepatic impairment, hypothyroidism, '
     'advanced age, and co-administration of drugs that inhibit statin metabolism '
     '(fibrates — especially gemfibrozil — macrolides, azole antifungals, '
     'cyclosporine).',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' Mention two new antihyperlipidemic drugs.', None, None,
     'PCSK9 inhibitors (e.g. evolocumab, alirocumab), which increase hepatic '
     'LDL-receptor recycling, and ezetimibe, which blocks intestinal cholesterol '
     'absorption; newer agents also include bempedoic acid and inclisiran.',
     TAG_PHARM, 'Pharmacology'),
    (V_LIPID + ' What is the receptor that mediates the action of gemfibrozil?',
     None, None,
     'Gemfibrozil, a fibrate, acts through PPAR-alpha (peroxisome '
     'proliferator-activated receptor alpha), which up-regulates lipoprotein lipase '
     'and fatty-acid oxidation, lowering triglycerides.',
     TAG_PHARM, 'Pharmacology'),
    (V_HYDRA + ' What are the adverse effects of hydralazine?', None, None,
     'Reflex tachycardia and palpitations, flushing, headache, fluid retention/edema, '
     'and — with chronic use, especially in slow acetylators — a drug-induced '
     'lupus-like syndrome.',
     TAG_PHARM, 'Pharmacology'),
    (V_HYDRA + ' What is the mechanism of action of hydralazine?', None, None,
     'Hydralazine directly relaxes arteriolar smooth muscle (via NO release/cGMP '
     'signaling), reducing peripheral resistance, with little effect on the venous '
     'side of the circulation.',
     TAG_PHARM, 'Pharmacology'),
    (V_HYDRA + ' Why is monotherapy with hydralazine not recommended?', None, None,
     'Arteriolar dilation triggers baroreceptor-mediated reflex sympathetic '
     'activation — tachycardia, increased contractility, and increased renin release '
     'causing sodium and water retention — which offsets the antihypertensive '
     'effect unless combined with a beta-blocker and a diuretic.',
     TAG_PHARM, 'Pharmacology'),
    ('What is the drug of choice in the treatment of hypertensive emergency?',
     None, None,
     'IV sodium nitroprusside is the classic first-line agent for rapid, titratable '
     'blood-pressure control in a hypertensive emergency (IV labetalol or nicardipine '
     'are also commonly used, depending on the clinical scenario).',
     TAG_PHARM, 'Pharmacology'),
    ('Mention 5 vasodilator drugs belonging to different groups.', None, None,
     'Hydralazine (direct arteriolar dilator), minoxidil (K+-channel opener), '
     'sodium nitroprusside (NO donor), nifedipine (calcium-channel blocker), and '
     'prazosin (alpha-1 blocker).',
     TAG_PHARM, 'Pharmacology'),
    ('Mention 5 different antihypertensive drugs that can cause postural '
     'hypotension. How is it managed?', None, None,
     'Prazosin and other alpha-1 blockers, methyldopa, guanethidine, ganglion '
     'blockers, and high-dose diuretics; it is managed by starting at a low dose, '
     'dosing at bedtime, up-titrating gradually, and advising the patient to rise '
     'slowly from sitting/lying.',
     TAG_PHARM, 'Pharmacology'),
    ('Mention 3 antihypertensive drugs used to treat hypertension during '
     'pregnancy.', None, None,
     'Methyldopa, labetalol, and nifedipine are the standard oral agents; IV '
     'hydralazine is used for acute severe hypertension/pre-eclampsia.',
     TAG_PHARM, 'Pharmacology'),
    ('Mention 5 different antihypertensive combinations that maintain normal serum '
     'potassium.', None, None,
     'ACE inhibitor or ARB plus a thiazide diuretic; ACE inhibitor plus a '
     'calcium-channel blocker; a thiazide plus a potassium-sparing diuretic (e.g. '
     'amiloride); a beta-blocker plus a thiazide; and an ARB plus a calcium-channel '
     'blocker — in each pairing the potassium-losing thiazide (where used) is '
     'balanced by a potassium-sparing partner.',
     TAG_PHARM, 'Pharmacology'),
    ('What are the antihypertensive mechanisms of beta-blockers?', None, None,
     'Beta-blockers reduce cardiac output through negative chronotropic and '
     'inotropic effects, reduce renin release from the juxtaglomerular apparatus '
     '(beta-1 blockade), and reduce central sympathetic outflow.',
     TAG_PHARM, 'Pharmacology'),
    ('Why is losartan preferable over captopril in some cases of hypertension?',
     None, None,
     'Losartan (an ARB) blocks the renin-angiotensin system at the AT1 receptor '
     'without inhibiting kininase II, so unlike the ACE inhibitor captopril it does '
     'not cause bradykinin-mediated dry cough or angioedema.',
     TAG_PHARM, 'Pharmacology'),
]


def main():
    qs = []
    for stem, options, correct, exp, tag, subj in ITEMS:
        qs.append(Q(stem, options, correct, 'derived', exp=exp, tag=tag, tag_suggere=subj))
    meta = {'Source file': SRC,
            'Type': 'GD case handout, 11 pages; 6 G.D. sessions across Histology, '
                    'Anatomy, Biochemistry, Pathology, Physiology and Pharmacology',
            'Tag': 'Department, GDs, <Subject> GD <N>', 'tagSuggere': 'varies by item',
            'Year': 'None',
            'Answer source': 'derived — no key is printed anywhere in the source'}
    n = write_md(OUT, 'Source 09 — GD Week 3 Cases', meta, qs)
    mcq = sum(1 for s, o, c, e, t, sj in ITEMS if o)
    ans = collections.Counter(c for s, o, c, e, t, sj in ITEMS if o)
    print(f'source 09: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: option-A blocks = {mcq}; ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    gate = 'n/a, <15' if mcq < 15 else f'max share {max(ans.values()) / mcq:.0%}'
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({mcq} MCQs — bias gate {gate})')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
