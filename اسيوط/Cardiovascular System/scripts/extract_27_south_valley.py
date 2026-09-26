#!/usr/bin/env python3
"""Source 27 — OTHER EXAMS/ميد جنوب الوادى .pdf ("Midterm South Valley").

A 6-page scanned/phone-photographed exam paper (Office Lens), CVS module,
declaring "Number of pages (6)" on its own intro page and running continuous
questions 1-48 (mixed physiology/histology/anatomy/pathology/pharmacology/
microbiology — a multidisciplinary paper, hence tagSuggere = None). No year is
printed anywhere in the paper or filename, so Year = None per the contract.

The physical page order in this PDF is shuffled relative to the paper's own
question order: rendered page 1 holds Q17-24, page 2 (rotated) holds Q8-16,
page 3 is the actual first page of the paper (declares "Number of pages (6)")
and holds Q1-7, pages 4-6 hold Q25-48 in order. All 48 questions are emitted
here in their original question-number order (1..48), not PDF page order.

Both the OCR (.ocr/27_south_valley.txt) and the PDF's own partial text layer
(`pdftotext -layout`) are badly mangled by the two-column layout and phone-photo
skew/rotation, well past reliable automated parsing (confirmed by comparing
both against the rendered page images). Per the extraction contract this file
was re-rendered at 400 dpi (`pdftoppm -png -r 400`) and all 6 pages were read
by eye, with several regions re-cropped and zoomed to confirm circled answers.

Every question has its correct option hand-circled in the source (a mix of
pen/pencil circles plus some check/cross annotations on the *other* options),
which is Answer Source 'marked' — a tick on an option in the source — per the
contract. All 48 stems/options are hand-transcribed from the rendered images.

Judgement calls flagged for the curator (kept as marked/transcribed faithfully,
not silently corrected — see report):
  Q17 - circled "b" (nucleus bulges into the lumen) as the EXCEPT/false answer,
        but that statement is anatomically TRUE; the better false statement is
        "c" (desmosomes — endothelial cells are actually joined by tight/gap
        junctions). Possible mis-circle by the paper's owner.
  Q27 - circled "d" (Prazosin) for "central sympatholytic antihypertensive",
        but Prazosin is a peripheral alpha-1 blocker, not a central
        sympatholytic; the textbook answer is Clonidine ("a").
  Q38 - circled "d" (accumulation of blood inside the pericardial sac, i.e.
        haemopericardium/tamponade) for "constrictive pericarditis", but the
        textbook definition of constrictive pericarditis is "b" (obliterated
        pericardial sac restricting cardiac motility).
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '27_South_Valley_Midterm.md')
TAG, YEAR = 'External, South Valley', None
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/ميد جنوب الوادى .pdf'

# (original Q#, stem, [options A..], correct letter, explanation)
RAW = [
(1, "Which of the following is directed downward (negative wave)",
 ["P wave", "Q wave", "T wave", "R wave"], "B",
 "The Q wave is normally a small downward (negative) deflection; P, R and T waves are normally upright/positive."),
(2, "Phase 1 in ventricular action potential represent caused by",
 ["Na influx", "K influx", "Ca influx", "K efflux"], "D",
 "Phase 1 (early rapid repolarization) of the ventricular action potential is caused by a transient outward K+ current (Ito), i.e. K efflux."),
(3, "Cardiac muscle differ from skeletal muscle as",
 ["Cardiac muscle has well developed sarcoplasmic reticulum", "Cardiac muscle has a shorter action potential",
  "Cardiac muscle contraction depend on extracellular Ca", "Cardiac muscle can be tetanized"], "C",
 "Unlike skeletal muscle, cardiac muscle contraction relies on Ca2+ influx from the extracellular fluid "
 "(calcium-induced calcium release) in addition to SR stores; its SR is less developed, its action potential "
 "is much longer, and its long refractory period prevents tetanization."),
(4, "All or non-rule",
 ["Is part of extrinsic regulation of cardiac contractility", "Apply only for atrial muscle",
  "It describe relation between EDV and contraction", "It describe relation Strength of stimulus and power of contraction"], "D",
 "The all-or-none law states that once threshold is reached, a muscle fiber (or the whole heart, functionally "
 "a syncytium) contracts maximally regardless of further increase in stimulus strength — describing the "
 "relation between stimulus strength and contraction, not EDV (that is Starling's law) or extrinsic regulation."),
(5, "Regarding Frank starling relationship",
 ["It depend on Ca ions", "Force of contraction is directly proportional to EDV",
  "It depend on Autonomic nervous system", "It is a homometric regulation"], "B",
 "The Frank-Starling (heterometric) mechanism states that the force of ventricular contraction increases in "
 "direct proportion to end-diastolic volume (fiber stretch), independent of autonomic/Ca2+-mediated homometric regulation."),
(6, "Slow conduction in AV node is due to",
 ["Poor blood supply", "Less parasympathetic nerve supply", "Its richness in Gap junction", "Its fibers is small in diameter"], "D",
 "AV nodal cells are small-diameter fibers with fewer gap junctions, which slows conduction velocity through the node "
 "(the physiological AV delay)."),
(7, "The Ventricular muscle conduction speed is",
 ["0.3 - 0.5 m/s", "1.5 - 4 m/s", "0.02 - 0.05 m/s", "2 - 3 m/s"], "A",
 "Conduction velocity through ordinary ventricular (working) myocardium is about 0.3-0.5 m/s, much slower than "
 "the Purkinje system (2-4 m/s) and much faster than the AV node (0.02-0.05 m/s)."),
(8, "T wave represent",
 ["Atrial depolarization", "Ventricular repolarization", "Atrial repolarization", "Ventricular depolarization"], "B",
 "The T wave represents ventricular repolarization."),
(9, "ST segment is normally",
 ["Elevated above baseline", "At the same level of base line", "Depressed above baseline", "Longer than P-R interval"], "B",
 "The normal ST segment is isoelectric, at the same level as the baseline (neither elevated nor depressed)."),
(10, "If the distance between 2 successive R waves is 10 large squares then, Heart rate is",
 ["300 Beat / minute", "50 Beat / minute", "60 Beat / minute", "30 Beat / minute"], "D",
 "Heart rate = 300 / (number of large squares between R waves) = 300/10 = 30 beats/minute."),
  # The paper prints options a and d with IDENTICAL text ("Conduction through
  # ventricle"), confirmed in the raw scan; the same typo appears in the sibling
  # paper (this midterm is reused across both faculties). The duplicate is
  # collapsed here rather than reproduced; the answer stays B (AV bundle).
(11, "P-R interval represent",
 ["Conduction through ventricle", "Conduction through AV bundle", "Conduction through Purkinje"], "B",
 "The PR interval reflects the time for the impulse to travel from the SA node through the atria and AV "
 "node/bundle to the ventricles — dominated physiologically by AV nodal/bundle conduction delay."),
(12, "In sinus tachycardia",
 ["Pacemaker AV node", "P is abnormal in shape", "Distance between R waves are small", "T wave is inverted"], "C",
 "Sinus tachycardia is a fast sinus rhythm with normal P waves preceding each QRS, so successive R waves are "
 "closely spaced (small R-R distance) while P morphology and pacemaker site (SA node) remain normal."),
(13, "Which of the following is an example of passive ectopic",
 ["AV nodal rhythm", "Sinus bradycardia", "Extrasystole", "Atrial flutter"], "A",
 "A passive ectopic rhythm (escape rhythm) arises when a subsidiary pacemaker, such as the AV node, takes over "
 "because the sinus rate falls too low — e.g. AV nodal (junctional) rhythm; extrasystoles and flutter are active/triggered ectopics."),
(14, "R waves are irregular (i.e. There is no equal distance between successive Rs) in",
 ["1st degree heart block", "Atrial fibrillation", "Atrial flutter", "AV nodal rhythm"], "B",
 "Atrial fibrillation produces an irregularly irregular ventricular response, so the R-R intervals vary "
 "without a fixed pattern, unlike flutter, nodal rhythm or simple first-degree block, which are regular."),
(15, "The pacemaker potential is characterized by",
 ["Stable Resting membrane potential", "Resting membrane potential is -80 mV", "Presence of prepotential",
  "Its rapid depolarization is caused by K efflux"], "C",
 "SA nodal cells lack a stable resting potential; instead they show a slow spontaneous prepotential (diastolic "
 "depolarization) that drives the cell to threshold, unlike the -80 mV stable resting potential of working myocardium."),
(16, "...... lies next to the lumen and is the innermost layer of the blood vessel",
 ["Tunica Media", "Tunica adventitia", "Tunica intima", "Tunica intermedia"], "C",
 "The tunica intima is the innermost layer of a blood vessel, lining the lumen with endothelium."),
(17, "All of these about Endothelial cells are true EXCEPT",
 ["They are flattened cells resting on a basal lamina", "Its nucleus causes the cell to bulge into the vessel lumen",
  "Endothelial cells are connected together by desmosomes", "The cytoplasm contains few organelles"], "B",
 "Transcribed as marked in the source (option B circled as the exception). Medically, B is actually a TRUE "
 "statement (the bulging nucleus is a recognized EM feature of endothelium); the better false statement is C, "
 "since endothelial cells are joined mainly by tight and gap junctions, not desmosomes — flagged for the "
 "curator to double-check against the original circle."),
(18, "The Purkinje fibers are",
 ["Are smaller than ordinary cardiomyocytes", "Have many myofibrils and less mitochondria",
  "The bulk of the sarcoplasm is occupied by lipid so appeared empty",
  "Specialized conducting fibers composed of electrically excitable cells"], "D",
 "Purkinje fibers are specialized, large, electrically excitable conducting cells of the ventricular conduction "
 "system, distinct from ordinary cardiomyocytes (they are larger, with fewer myofibrils and more glycogen, giving a paler appearance)."),
(19, "Intercalated disc are present in",
 ["Skeletal muscle", "Cardiac muscle", "Smooth muscle", "All of the above"], "B",
 "Intercalated discs are a distinguishing feature of cardiac muscle, mechanically and electrically coupling "
 "adjacent cardiomyocytes; they are absent from skeletal and smooth muscle."),
(20, "Cardiac skeleton, composed of",
 ["Dense white fibrous (collagenous) connective tissue", "Cardiac muscle fibers",
  "Dense yellow elastic connective tissue", "Fascia adherens as anchoring sites for actin"], "A",
 "The fibrous (cardiac) skeleton is made of dense, white, collagenous connective tissue forming the valve "
 "rings and septa that anchor the myocardium and valves."),
(21, "Sympathetic stimulation of the heart:",
 ["Has negative chronotropic effect", "Acts through beta receptor", "Has negative dromotropy", "Acts through alpha receptor"], "B",
 "Cardiac sympathetic stimulation acts mainly through beta-1 adrenergic receptors, producing positive "
 "chronotropic, dromotropic and inotropic effects — the opposite of the negative effects listed."),
(22, "About heart rate:",
 ["The heart rate is directly proportional to the arterial blood pressure",
  "The heart rate is directly proportional to the atrial blood pressure",
  "The heart rate is indirectly proportional to high arterial CO2 pressure",
  "The heart rate is indirectly proportional to skeletal muscle hypoxia"], "B",
 "Increased atrial (venous) filling/pressure stretches the atrial wall and reflexly raises heart rate via the "
 "Bainbridge reflex — a direct relationship; rising arterial BP instead reflexly slows the heart via "
 "baroreceptors (inverse relation, as annotated in the source), and both high CO2 and muscle hypoxia reflexly increase, not decrease, heart rate."),
(23, "Venous return increase in case of:",
 ["Arterial vasoconstriction", "Venous vasoconstriction", "Arterial vasodilatation", "Venous vasodilation"], "C",
 "Arterial vasodilatation lowers resistance and increases blood flow through the tissues into the venous "
 "system, increasing venous return; venous vasoconstriction (not dilation) also raises venous return by "
 "mobilizing reservoir blood, while venous vasodilation pools blood and reduces venous return."),
(24, "Increase arterial blood pressure",
 ["Leads to decrease cardiac output in normal function heart", "Leads to no change in cardiac output in failed heart",
  "Leads to increase cardiac output in normal function heart", "Leads to decrease cardiac output in failed heart"], "D",
 "In a failing heart operating on the flat/descending part of the function curve, an acute rise in afterload "
 "(arterial pressure) further reduces stroke volume and cardiac output, unlike the normal heart which can "
 "largely compensate."),
(25, "Which of the following is the drug of choice in treatment of hypertension during pregnancy?",
 ["α-Methyl Dopa", "Clonidine", "Captopril", "Losartan"], "A",
 "Methyldopa is the classic first-line antihypertensive in pregnancy given its long safety record; ACE "
 "inhibitors/ARBs (captopril, losartan) are contraindicated in pregnancy."),
(26, "The drug of choice in treatment of hypertensive emergencies is:",
 ["Sodium nitroprusside", "Lisinopril", "Propranolol", "Thiazides"], "A",
 "IV sodium nitroprusside is a classic drug of choice for hypertensive emergencies because of its rapid onset "
 "and titratable, short-acting action."),
(27, "One of the following drugs is a central sympatholytics and used as an antihypertensive drug:",
 ["Clonidine", "Propranolol", "Minoxidil", "Prazosin"], "D",
 "Transcribed as marked in the source (option D, Prazosin, circled). Medically, Prazosin is a peripheral "
 "alpha-1 blocker, not a central sympatholytic; the textbook central sympatholytic here is Clonidine (option "
 "A) — flagged for the curator to double-check against the original circle."),
(28, "The drug of choice for treatment of hypertension with benign prostatic hyperplasia is:",
 ["Propranolol", "Furosemide", "Prazosin", "Nifedipine"], "C",
 "Prazosin (an alpha-1 blocker) relaxes prostatic/bladder-neck smooth muscle, making it useful for "
 "hypertension coexisting with benign prostatic hyperplasia."),
(29, "The following is the first drug of choice in treatment of hypertension with diabetes:",
 ["Propranolol", "Furosemide", "Prazosin", "Captopril"], "D",
 "ACE inhibitors such as captopril are first-line for hypertensive patients with diabetes because of their "
 "renoprotective effect."),
(30, "A patient taking aminoglycosides, a diuretic was prescribed to him, then the patient experienced hearing loss and damage to the ear. Which diuretic was prescribed to him?",
 ["Chlorothiazide", "Acetozolamide", "Furosemide", "Spironolactone"], "C",
 "Loop diuretics such as furosemide are ototoxic and markedly potentiate the ototoxicity of aminoglycosides "
 "when combined."),
(31, "Hydralazine (a vasodilator) can produce:",
 ["Seizures, extrapyramidal disturbances", "Tachycardia, lupus erythromatosis", "Acute hepatitis", "Aplastic anemia"], "B",
 "Hydralazine classically causes reflex tachycardia and a reversible drug-induced lupus erythematosus-like syndrome."),
(32, "Which of the following organisms is responsible for sub-acute bacterial endocarditis",
 ["Group A Streptococci", "Haemophilus influenzae", "Staphylococcus aureus", "Streptococcus viridans"], "D",
 "Streptococcus viridans, a low-virulence oral commensal, is the classic cause of subacute bacterial "
 "endocarditis, typically on previously damaged valves; Staph aureus causes the acute, fulminant form."),
(33, "Normal pleural fluid is",
 ["22-27ml", "20-25ml", "30-70ml", "10-20ml"], "B",
 "Normal pleural fluid volume is approximately 20-25 mL (a thin lubricating film)."),
(34, "Which of the following causes destruction and perforation of the cardiac valves?",
 ["Subacute bacterial endocarditis", "Acute infective endocarditis", "Rheumatic valvulitis", "Viral myocarditis"], "B",
 "Acute infective endocarditis (typically Staph aureus) is aggressive and destructive, causing rapid valve "
 "destruction/perforation, in contrast to the more indolent subacute form."),
(35, "The following are from the complication of sub-acute bacterial endocarditis except:",
 ["Infarction of multiple organs", "Focal embolic glomerulonephritis", "Pyaemia and multi-organ abscesses",
  "Mycotic aneurysm of the cerebral and mesenteric arteries"], "C",
 "Pyaemia with multiple abscesses is characteristic of the acute, virulent (Staph aureus) form of endocarditis "
 "with septic emboli; subacute bacterial endocarditis more typically causes bland emboli/infarcts, focal "
 "embolic glomerulonephritis, and mycotic aneurysms rather than suppurative abscesses."),
(36, "Regarding manifestations of rheumatic fever, which of the following is correct:",
 ["Microscopic collection of histiocytic cells seen in myocardium in rheumatic carditis (describes the Aschoff body)",
  "Fibrous adhesions seen in cases of chronic rheumatic valvulitis",
  "Involuntary movement seen due to rheumatic affection of basal ganglia",
  "Nodular lesion of the skin seen in cases of rheumatic fever (describes subcutaneous nodules)"], "C",
 "Sydenham's chorea, the involuntary, purposeless movement disorder of rheumatic fever, results from "
 "rheumatic affection of the basal ganglia. (The exact original stem wording is cut off at the top of the "
 "scanned page; reconstructed from the four listed rheumatic-fever manifestations and the circled option.)"),
(37, "Aschoff bodies is pathognomic of:",
 ["Acute infective endocarditis", "Rheumatic heart disease", "Sub-acute infective endocarditis", "Pericarditis"], "B",
 "Aschoff bodies (nodules) are the pathognomonic granulomatous lesion of rheumatic heart disease/rheumatic carditis."),
(38, "Constrictive pericarditis is characterized by:",
 ["One form of acute pericarditis", "Pericardial sac is obliterated restricting normal cardiac motility",
  "One cause of acute heart failure", "Accumulation of blood inside pericardial sac"], "D",
 "Transcribed as marked in the source (option D circled). Medically, the textbook definition of constrictive "
 "pericarditis is option B (a chronic, obliterated, rigid pericardial sac restricting cardiac filling/motility); "
 "option D instead describes haemopericardium/cardiac tamponade — flagged for the curator to double-check against the original circle."),
(39, "In rheumatic heart disease the joints shows:",
 ["Osteoarthritis", "Suppurative arthritis", "Fleeting arthritis", "Chronic non specific arthritis"], "C",
 "Rheumatic fever classically causes a migratory (fleeting) polyarthritis of large joints."),
(40, "All of the following are contents of superior mediastinum except",
 ["Trachea", "Arch of aorta", "Sympathetic trunk", "Esophagus"], "C",
 "The sympathetic trunks lie in the posterior mediastinum/paravertebral region, not within the superior "
 "mediastinum, unlike the trachea, aortic arch and esophagus which all pass through it."),
(41, "Visceral layer of serous pericardium is supplied by",
 ["Phrenic nerve", "Sympathetic trunks", "Vagus nerve", "a & b"], "C",
 "The visceral layer of serous pericardium (epicardium) receives autonomic supply mainly via the vagus nerve "
 "and cardiac plexus, unlike the parietal pericardium/fibrous pericardium which is supplied by the phrenic nerve."),
(42, "The mediastinum is divided into superior and inferior by a line extends from the sternal angle to",
 ["The lower border of T4", "The lower border of T3", "T3-T4", "T2-T3"], "A",
 "The transverse thoracic plane, at the sternal angle anteriorly, passes through the lower border of the T4 "
 "vertebra posteriorly, dividing superior from inferior mediastinum."),
(43, "Phase 0 in ventricular action potential represent",
 ["Resting membrane potential", "1st rapid repolarization", "Rapid depolarization", "Plateau"], "C",
 "Phase 0 of the ventricular action potential is the rapid upstroke (depolarization) caused by fast Na+ influx."),
(44, "Which of the following is true about Auto rhythmicity of SA node",
 ["Produced by autonomic nervous system", "Is essential for SA node to contract",
  "Is essential for SA node to become the pacemaker", "Cannot be changed"], "C",
 "Autorhythmicity (spontaneous diastolic depolarization) is an intrinsic property of SA nodal cells that "
 "allows the SA node to reach threshold fastest and thus function as the heart's normal pacemaker; it is "
 "modulated (not produced) by the autonomic nervous system and is not required merely for contraction."),
(45, "The highest speed in conduction occur in",
 ["Atrium", "SA node", "Ventricular muscle", "Purkinje fibers"], "D",
 "The Purkinje fiber system has the fastest conduction velocity (about 2-4 m/s) of any cardiac tissue, "
 "enabling near-simultaneous ventricular activation."),
(46, "The lower border of the heart is formed by",
 ["Right ventricle", "Right atrium", "A small part by left ventricle", "Right ventricle and a small part by left ventricle"], "D",
 "The inferior border of the heart is formed mainly by the right ventricle, with a small contribution from the left ventricle apex."),
(47, "The aortic orifice guarded by the aortic valve that consists of",
 ["Three cusps one posterior and two anterior cusps", "Three cusps one anterior and two posterior cusps",
  "Two cusps", "Three cusps anterior, posterior and septal"], "B",
 "The aortic valve has three semilunar cusps: one anterior (right) cusp and two posterior (left and "
 "non-coronary) cusps."),
(48, "All of the following open into the right atrium except",
 ["Inferior vena cava", "Superior vena cava", "Coronary sinus", "Posterior interventricular artery"], "D",
 "The IVC, SVC and coronary sinus all drain directly into the right atrium; the posterior interventricular "
 "artery is a coronary artery branch running on the heart's surface, not an opening into the atrium."),
]


def main():
    questions = []
    for _, stem, opts, letter, exp in RAW:
        questions.append(Q(stem, opts, letter, 'marked', exp=exp, tag=TAG, year=YEAR))

    meta = {'Source file': SRC,
            'Type': 'Scanned/phone-photo PDF, 6 pages, 2-column layout, declares 48 questions',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': 'None',
            'Answer source': 'marked — every option is hand-circled in the scanned source '
                              '(3 circles flagged as likely mis-marks; see script docstring)'}
    n = write_md(OUT, 'Source 27 — South Valley CVS midterm', meta, questions)

    letters = collections.Counter(r[3] for r in RAW)
    mcq = len(RAW)
    highest = max(r[0] for r in RAW)
    print(f'source 27: {n} questions ({mcq} MCQ / 0 written)')
    print(f'  counters: declared in source = 48, highest question number = {highest}, '
          f'option-A blocks = {len(RAW)}, ### Q = {n}')
    print(f'  answer source breakdown: marked={mcq}, derived=0')
    total = sum(letters.values())
    dist = ', '.join(f'{k}={v} ({v*100//total}%)' for k, v in sorted(letters.items()))
    top = max(letters.values()) / total
    verdict = 'PASS' if top <= 0.45 else ('INVESTIGATE' if top <= 0.60 else 'FAIL')
    print(f'  answer distribution: {dist}  -> bias gate: {verdict} (top={top*100:.0f}%, n={total})')
    print('  judgement calls: Q17, Q27, Q38 circled answers look medically questionable '
          '(likely mis-circles in the source) — transcribed as marked, flagged for double-check. '
          'Q36 original stem text is cut off at the top of the scanned page; reconstructed from the options.')


if __name__ == '__main__':
    main()
