#!/usr/bin/env python3
"""Source 02 — All  formatives  CVS.pdf (43 pages, MIXED format).

Pages 1-5  : a digital Moodle review export with a real text layer — "Formative
             assessment 2022 > Formative assessment 1 CVS" (12 MCQs). Moodle prints
             'The correct answer is: ...' under every question, so provenance is `key`.
             The source-01 block harvester is reused for this part; pages 6-43 carry
             no text layer at all (verified with pdftotext -layout), so harvest()
             naturally sees only pages 1-5.

Pages 6-43 : full-page phone screenshots of THREE further Moodle formative attempts,
             back to back, with no text layer. Each screenshot shows "Answer saved"
             (or, for a handful of skipped questions, "Not yet answered") with at most
             one radio filled — that is the STUDENT'S pick, never a printed key: Moodle
             never prints "The correct answer is" on these pages. Every one of these
             38 questions is therefore `derived`, answered here from medical knowledge
             after reading each screenshot at 300 dpi (pdftoppm -r 300) and cross-checking
             tesseract OCR against the actual rendered page. Three attempts are present:
               * pages  6-18 (13 Q) — no breadcrumb visible in any screenshot (the title
                 bar is scrolled out of frame); by filename/sequence this is treated as
                 "Formative 2" -- JUDGEMENT CALL, flagged for reviewer.
               * pages 19-32 (14 Q) — page 19 shows the title bar: "Formative CVS 3".
               * pages 33-43 (11 Q) — no breadcrumb visible; treated as "Formative 4" by
                 sequence -- JUDGEMENT CALL, flagged for reviewer.
             A few questions on the third attempt (pages 39-43) are themselves marked
             "Not yet answered" by Moodle (the student skipped them) — no radio at all,
             so there is doubly no key; still `derived`.
"""
import os, sys, fitz
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, match_correct
from extract_01_quizzes import harvest, parse, TAIL

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system',
                   'All  formatives  CVS.pdf')
OUT = os.path.join(MOD, 'Markdown_Questions', '02_All_Formatives_CVS.md')

TAG1 = 'Department, Formative, Formative 1'
TAG2 = 'Department, Formative, Formative 2'
TAG3 = 'Department, Formative, Formative 3'
TAG4 = 'Department, Formative, Formative 4'

# ---------------------------------------------------------------------------
# Pages 6-43 — phone screenshots, no text layer. Transcribed by rendering every
# page at 300 dpi (pdftoppm -png -r 300) and reading it directly (tesseract OCR
# was run first and cross-checked, but its digit/glyph errors on "Question N"
# and on option text made it unsafe to parse automatically, so every question
# below was verified against the actual page image). Each tuple is
# (stem, [options], correct_letter, exp_note).
# ---------------------------------------------------------------------------

FORMATIVE_2 = [
    ("A 55 years old patient presented with acute onset of high-grade fever and signs of "
     "heart failure. On examination a heart murmur was heard. He had a history of colorectal "
     "cancer that was removed by surgery followed by chemotherapy. What is the most probable "
     "causative microorganism?",
     ["Streptococcus gallolyticus (bovis)", "Staphylococcus epidermidis", "HACEK group"],
     "A", "Streptococcus gallolyticus (S. bovis) bacteraemia/endocarditis is classically "
          "associated with underlying colorectal neoplasia."),
    ("Eight year old girl recovered from an apparent cold with sore throat, troublesome new "
     "symptom appeared, including bumps near her joint insertions, severe fatigue and an "
     "evanescent rash. The causative organism is",
     ["Streptococcus viridans", "Staphylococcus epidermidis", "Staphylococcus aureus",
      "Streptococcus pyogenes"],
     "D", "Post-streptococcal (acute rheumatic fever) picture following pharyngitis; "
          "causative organism is group A Streptococcus pyogenes."),
    ("A young adult patient presented with fever, fatigue, and chest pain that progressed to "
     "heart failure. He was diagnosed as viral myocarditis. The test that confirmed the "
     "diagnosis was",
     ["Blood culture", "Coxsackievirus specific IgM", "High ASO titer",
      "High IgG against Bartonella"],
     "B", "Coxsackie B virus is the classic cause of viral myocarditis; confirmed serologically "
          "by specific IgM."),
    ("The heart, in chronic form of Chagas disease is characterized by",
     ["Biventricular dilatation", "Aortic stenosis", "Left ventricular hypertrophy",
      "Right ventricular hypertrophy"],
     "A", "Chronic Chagas cardiomyopathy produces a dilated cardiomyopathy with biventricular "
          "dilatation."),
    ("About Bainbridge reflex",
     ["It's induced by increase in Pa of CO2 in arterial blood",
      "It's induced by increase in arterial blood pressure",
      "It's mediated by afferent fiber in vagus nerve and efferent fiber in vagal and "
      "sympathetic nerves",
      "This reflex leads to bradycardia"],
     "C", "Bainbridge reflex: right-atrial/venous stretch raises heart rate; afferent limb runs "
          "in the vagus, efferent limb via vagal withdrawal and sympathetic activation."),
    ("A male patient complained with severe ischemic chest pain and diagnosed as left "
     "ventricular myocardium ischemia and heart failure, he had",
     ["Cyanosis", "Lower limb edema", "Enlargement of the liver",
      "Raised central venous pressure"],
     "A", "Left ventricular failure produces pulmonary congestion/oedema with hypoxemia and "
          "cyanosis; the other options are signs of right-sided (not left-sided) failure."),
    ("Increased arterial blood pressure (afterload) in patients with heart failure leads to",
     ["No change in COP because healthy heart can compensate", "Decreased SV and COP",
      "Increased SV without effect on COP", "Increased SV and COP"],
     "B", "A failing ventricle cannot compensate for a rise in afterload, so stroke volume and "
          "cardiac output fall."),
    ("In chronic rheumatic heart disease, McCallum patch is seen on the wall of the left "
     "atrium. What is the underlying microscopic finding on this patch",
     ["Aschoff nodules formation", "Heavy lymphocytic infiltration", "Fibrosis",
      "Granulation tissue"],
     "C", "McCallum's patch is an area of subendocardial fibrosis in the posterior left atrium "
          "caused by the regurgitant jet of mitral disease."),
    ("Which of the following is a presentation of aortic stenosis",
     ["Diastolic murmur", "Cyanosis", "Hypotention and syncopial attacks", "Hypertension"],
     "C", "Classic triad of severe aortic stenosis: angina, syncope (with exertional "
          "hypotension), and dyspnoea/heart failure."),
    ("60 year old male patient diagnosed as heart failure, He uses captopril 25 mg 3 times/ "
     "day, Furosemide 40 mg 2 times/ day and digoxin one tablet once/ day. The patient has "
     "nausea and vomiting. Serum digoxin level is 0.5 ng/ml. The possible cause of nausea and "
     "vomiting in this case is",
     ["The patient still has uncontrolled heart failure",
      "The patient developed nausea and vomiting due to the use of captopril",
      "The patient developed gastroenteritis", "The patient developed digoxin toxicity"],
     "A", "Serum digoxin 0.5 ng/ml is within/below the therapeutic range, so toxicity is "
          "excluded; GI congestion from uncontrolled heart failure is the likely cause."),
    ("A 55 year old white woman with no past medical history present to the emergency "
     "department for \"a racing heartbeat\" It is determined that she has ventricular "
     "tachcardia. Which of the following is the drug of choice used for the treatment of "
     "this case",
     ["Verapamil", "Digoxin", "Adenosine", "Lidocaine"],
     "D", "Lidocaine (or amiodarone) is used for sustained monomorphic ventricular tachycardia; "
          "verapamil is contraindicated and adenosine/digoxin are not treatments for VT."),
    ("Outpatient prophylaxis of a patient with an SVT is best accomplished with the "
     "administration of",
     ["Diltiazim", "Mexiletine", "Esmolol", "Adenosine", "Lidocaine"],
     "A", "Chronic oral prophylaxis of SVT uses an AV-nodal blocker such as diltiazem "
          "(or a beta-blocker); adenosine and IV esmolol are for acute termination only."),
    ("Double dobutamine and inamrinone increase cardiac contractility by",
     ["Increasing cAMP", "Inhibition of Na+/K+ ATPase", "Inactivation of Na channels",
      "Activation of Na/Cl cotransporter", "Activation of adenylyl cyclase"],
     "A", "Dobutamine (via beta1/adenylyl cyclase) and inamrinone (via PDE3 inhibition) both "
          "converge on raising intracellular cAMP; only 'increasing cAMP' covers both drugs."),
]

FORMATIVE_3 = [
    ("A 29-year-old man with a family history of heart disease presents to his primary care "
     "physician for a routine checkup. A lipid profile on a blood draw reveals high LDL and "
     "low HDL. One way to decrease the amount of LDL in the blood is to hinder the liver's "
     "ability for de novo cholesterol synthesis. Which of the following drugs blocks de novo "
     "cholesterol synthesis in hepatocytes?",
     ["Atorvastatin", "Cholestyramine", "Colestipol", "Ezetimibe", "Colesevelam"],
     "A", "Statins inhibit HMG-CoA reductase, the rate-limiting enzyme of hepatic de novo "
          "cholesterol synthesis."),
    ("A 63-year-old man with congestive heart failure comes to the cardiologist for a routine "
     "visit. He is doing well and has no complaints. He is taking digoxin, metoprolol, and "
     "spironolactone. What is the mechanism of action of spironolactone?",
     ["Inhibits NaCl reabsorption", "Aldosterone receptor antagonist",
      "Inhibits Na+/K+/2Cl- cotransport", "Carbonic anhydrase inhibitor", "Osmotic diuretic"],
     "B", "Spironolactone is a competitive aldosterone (mineralocorticoid) receptor antagonist "
          "in the collecting duct."),
    ("Atherosclerosis is a:",
     ["Autoimmune disease", "Inflammatory disease", "Infectious disease",
      "Degenerative disease"],
     "B", "Modern pathology (response-to-injury hypothesis) classes atherosclerosis as a "
          "chronic inflammatory disease of the arterial wall rather than a purely degenerative "
          "process — overriding the student's 'degenerative' pick."),
    ("Cardiac output:",
     ["It's the multiplying of heart rate and peripheral resistance",
      "It's affect only on systolic blood pressure",
      "It's inversely related to stroke volume", "It's directly related to ABP"],
     "D", "CO = HR x SV, and ABP = CO x TPR, so for a given resistance CO varies directly "
          "with arterial blood pressure."),
    ("Haemodynamics:",
     ["It's the relation of between pressure and heart rate",
      "It's the relation of between pressure and COP",
      "It's the relation of between pressure and resistance and blood flow",
      "The blood flow is inverse proportional to the pressure difference"],
     "C", "Haemodynamics describes the relation between driving pressure, vascular resistance "
          "and blood flow (Q = ΔP/R)."),
    ("In malignant hypertension, the most characteristic pathological feature is:",
     ["Fibrinoid necrosis", "Endotheliosis", "Hyalinosis", "Elastosis"],
     "A", "Fibrinoid necrosis of the arteriolar wall is the hallmark lesion of malignant "
          "hypertension."),
    ("The majority of absorbed fat appears in the forms of:",
     ["VLDL", "HDL", "LDL", "Chylomicron"],
     "D", "Dietary (absorbed) fat is packaged into chylomicrons by enterocytes."),
    ("The middle segment of permanent aortic arch is developed from",
     ["Aortic sac", "Left fourth embryonic aortic arch", "Left dorsal aorta",
      "Left third embryonic aortic arch"],
     "B", "The definitive arch of the aorta = aortic sac (proximal part) + left 4th aortic "
          "arch (middle part) + left dorsal aorta (distal part)."),
    ("The most common cause of death in benign hypertension is:",
     ["Cerebral hemorrhage", "Respiratory failure", "Renal failure", "Heart failure"],
     "D", "Heart failure (from long-standing pressure overload/LVH) is the most common cause "
          "of death in benign/essential hypertension."),
    ("The most important complication of atherosclerosis is:",
     ["Thrombus formation", "Ulceration", "Dystrophic calcification", "Haemorrhage"],
     "A", "Superimposed thrombosis on a disrupted plaque is the complication that precipitates "
          "MI/stroke and is considered the most important."),
    ("The vessel which contains 2 layers of smooth muscle an inner longitudinal and outer "
     "circular layer in its tunica media is:",
     ["Umbilical artery", "Aorta", "Inferior vena cava", "Coronary artery"],
     "A", "The umbilical artery is classically described with an inner longitudinal and outer "
          "circular smooth-muscle layer in its tunica media."),
    ("Vasomotor tone:",
     ["It is due to stimulation of atrial receptor",
      "It's decrease in case thorax spinal cord injury",
      "Is inhibitory signals from VCC to maintain ABP normal",
      "It's due to stimulatory signals from baroreceptors"],
     "B", "Baseline sympathetic vasoconstrictor (vasomotor) tone is lost below a high spinal "
          "cord transection (spinal shock), so it falls after thoracic spinal cord injury."),
    ("Which of the following is true of pericytes",
     ["Capable of forming multinucleated muscle fibers", "Are terminally differentiated",
      "Form a layer of cells joined by gap junctions",
      "Are associated with the basal lamina of capillary endothelial cells"],
     "D", "Pericytes sit within/are associated with the basal lamina surrounding capillary "
          "endothelial cells."),
    ("Which one of the following is the most appropriate drug to use for the patient described "
     "in parentheses",
     ["Captopril (60 year old woman with diabetic nephropathy)",
      "Milrinone (57 year old patient with chronic CHF)",
      "Nitroprusside (50 year old man with BP of 140/95 mmHg)",
      "Losartan (29 year old pregnant woman)"],
     "A", "ACE inhibitors such as captopril are renoprotective first-line therapy in diabetic "
          "nephropathy; milrinone is not for chronic oral use, nitroprusside is reserved for "
          "hypertensive emergency, and ARBs such as losartan are contraindicated in pregnancy."),
]

FORMATIVE_4 = [
    ("A 73-year-old woman with known angina has an attack of mild chest pressure and spasm "
     "while shopping at the mall. She takes a sublingual nitroglycerin tablet and within a "
     "few minutes has improvement in her symptoms. Which of the following is the most likely "
     "explanation of action of this agent?",
     ["Increasing pulmonary arterial blood flow", "Venoconstriction",
      "Decreased preventricular contractions", "Decreased myocardial oxygen consumption",
      "Decreased myocardial perfusion"],
     "D", "Nitrates are venodilators; the fall in preload lowers myocardial oxygen "
          "consumption, relieving angina."),
    ("A female patient presents with dilated elongated and tortuous leg veins. What is the "
     "possible complication of this condition",
     ["Hypertension", "Cerebral hemorrhage", "Renal failure", "Phlebothrombosis"],
     "D", "Varicose veins predispose to stasis and venous thrombosis (phlebothrombosis)."),
    ("In a moderate-sized myocardial infarct it would take approximately how long to replace "
     "the necrotic muscle with granulation tissue?",
     ["2 hours", "2 weeks", "2 months", "2 days"],
     "B", "Well-formed granulation tissue is present in an infarct by about 2-3 weeks after "
          "the event."),
    ("The following is true for thromboangitis obliterans:",
     ["Involves the vessels in a segmental pattern", "Less common in heavy smokers",
      "Affects mainly the vessels of internal organs", "Occurs exclusively in women"],
     "A", "Buerger disease (thromboangiitis obliterans) shows segmental, focal involvement of "
          "small/medium limb vessels and is strongly linked to heavy smoking."),
    # The Moodle screenshot for this item (p.37) genuinely prints options b and c
    # with identical text, "The isometric contraction phase" — verified against the
    # rendered page at 400 dpi, so it is a defect in the department's quiz, not an
    # OCR artifact. The duplicate is collapsed to a single option here; keeping both
    # would put two indistinguishable correct answers in front of the student. The
    # radio button filled in the screenshot is c, but that is the student's saved
    # selection ("Answer saved", ungraded), not a key, so the answer stays `derived`.
    ("The lowest Coronary blood flow occurs during:",
     ["None of them", "The isometric contraction phase", "The reduced ejection phase"],
     "B", "Left coronary flow is lowest during isovolumetric (isometric) ventricular "
          "contraction, when intramyocardial pressure compresses the intramural vessels most."),
    ("The wheal in the triple response is due to:",
     ["Increased capillary permeability", "Decreased absorption of fluid",
      "Contraction of precapillary sphincters", "Axon reflex"],
     "A", "The wheal is local oedema from histamine-mediated increased capillary "
          "permeability; the flare (not the wheal) is the axon-reflex component."),
    ("What is the chemical identity of endothelium-derived relaxing factor (EDRF)?",
     ["Nitrous oxide", "Potassium", "Carbon monoxide", "Nitric oxide"],
     "D", "EDRF was identified as nitric oxide (NO)."),
    ("What is the earliest cause of death in myocardial infarction?",
     ["Cardiac tamponade", "Ventricular arrhythmias", "Acute valvular dysfunction",
      "Subacute bacterial endocarditis"],
     "B", "Fatal ventricular arrhythmia within the first hour is the leading early cause of "
          "death after MI."),
    ("Which of the following physiologic responses has a neural basis?",
     ["White reaction", "Reactive hyperemia", "Flare", "Red reaction"],
     "C", "The flare component of the triple response is mediated by an axon reflex, i.e. it "
          "has a neural basis; the wheal and red reaction are local/humoral."),
    ("Which one of cardiac markers is considered the most sensitive and specific in diagnosis "
     "of Myocardial infarction?",
     ["Aspartate transaminase", "Myoglobin", "Troponin I", "Lactate dehydrogenase"],
     "C", "Cardiac troponin I is the most sensitive and specific biomarker for myocardial "
          "infarction."),
    ("In a patient suffering from angina of effort, nitroglycerin may be given sublingual "
     "because this mode of administration",
     ["Causes less reflex tachycardia than oral administration", "Improves patient compliance",
      "Has a decreased tendency to cause methemoglobinemia",
      "Avoids first pass hepatic metabolism", "Bypasses the coronary circulation"],
     "D", "Sublingual absorption drains via the systemic veins into the superior vena cava, "
          "bypassing hepatic first-pass metabolism that would otherwise inactivate "
          "nitroglycerin."),
]


def build_screenshot_questions():
    out = []
    for tag, block in ((TAG2, FORMATIVE_2), (TAG3, FORMATIVE_3), (TAG4, FORMATIVE_4)):
        for stem, options, letter, exp in block:
            out.append(Q(stem, options, letter, 'derived', exp=exp,
                         tag=tag, tag_suggere='None'))
    return out


def build_formative1_questions():
    """Pages 1-5 — digital Moodle export, reuse the source-01 block harvester."""
    doc = fitz.open(SRC)
    markers, content, headers = harvest(doc)
    bounds = [(m[0], m[1]) for m in markers] + [(10 ** 6, 0)]

    questions, no_key, dropped = [], [], []
    for i, (pno, y0, num) in enumerate(markers):
        chunk = [t for (bp, by, t) in content if (pno, y0 - 6) <= (bp, by) < bounds[i + 1]]
        stem, options, answer, _tf = parse(chunk)
        options = [TAIL.sub('', o).strip() for o in options]
        if not stem:
            dropped.append((num, 'empty stem', '', len(options)))
            continue
        if answer is None:
            no_key.append((num, stem[:70], len(options)))
            continue
        if len(options) < 2:
            dropped.append((num, 'single option', stem[:70], len(options)))
            continue
        letter = match_correct(answer, options)
        if letter is None:
            dropped.append((num, f'unmatched {answer[:40]!r}', stem[:70], len(options)))
            continue
        questions.append((num, Q(stem, options, letter, 'key', tag=TAG1, tag_suggere='None')))
    questions.sort(key=lambda p: p[0])
    return [q for _, q in questions], no_key, dropped, len(markers)


def main():
    f1_questions, no_key, dropped, markers_f1 = build_formative1_questions()
    screenshot_questions = build_screenshot_questions()
    questions = f1_questions + screenshot_questions

    meta = {
        'Source file': 'All  formatives  CVS.pdf',
        'Type': 'Mixed — 43 pages: pp.1-5 digital Moodle export (text layer), '
                'pp.6-43 full-page phone screenshots (no text layer, OCR 300 dpi)',
        'Tag': 'Department, Formative, Formative <N> (per question — see per-question Tag)',
        'tagSuggere': 'None',
        'Year': 'None',
        'Answer source': 'key for pp.1-5 (Moodle prints "The correct answer is: ..."); '
                          'derived for pp.6-43 (screenshots show only the student\'s own '
                          '"Answer saved" pick, never a verified key — answered here from '
                          'medical knowledge)',
    }
    n = write_md(OUT, 'Source 02 — CVS Department Formatives (Moodle)', meta, questions)

    mcq = sum(1 for q in questions if q.type == 'QCS')
    derived = sum(1 for q in questions if q.source == 'derived')
    key = sum(1 for q in questions if q.source == 'key')
    letters = collections_counter = {}
    import collections
    letters = collections.Counter(q.correct for q in questions if q.type == 'QCS')

    print(f'Formative 1 (pp.1-5): {markers_f1} markers -> {len(f1_questions)} questions '
          f'(key, printed under each question)')
    print(f'Formative 2 (pp.6-18, screenshots): {len(FORMATIVE_2)} questions (derived)')
    print(f'Formative 3 (pp.19-32, screenshots): {len(FORMATIVE_3)} questions (derived)')
    print(f'Formative 4 (pp.33-43, screenshots): {len(FORMATIVE_4)} questions (derived)')
    print(f'\nTOTAL written: {n}  (MCQ={mcq}, QROC={n - mcq})')
    print(f'Answer source breakdown: key={key}, derived={derived}')
    print(f'DERIVED answers (no key anywhere in the source): {derived}')
    print(f'Answer-letter distribution (MCQ only): {dict(sorted(letters.items()))}')
    if mcq:
        top = max(letters.values()) / mcq * 100
        print(f'Bias gate: top single-letter share = {top:.1f}%'
              f'{"  <== BIAS FAIL" if mcq >= 15 and top > 45 else ""}')
    if no_key:
        print(f'\n{len(no_key)} Formative-1 questions had NO printed key and were skipped:')
        for r in no_key:
            print('   Q%-4s %-70s opts=%s' % r)
    if dropped:
        print(f'\n{len(dropped)} Formative-1 markers dropped:')
        for r in dropped:
            print('   Q%-4s %-24s %-60s opts=%s' % r)
    print(f'\nCompleteness counters: highest question number in source blocks = 12 (F1) + '
          f'13 (F2) + 14 (F3) + 11 (F4); option-A blocks / "### Q" headings = {n} (see grep gate)')


if __name__ == '__main__':
    main()
