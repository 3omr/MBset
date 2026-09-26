#!/usr/bin/env python3
"""Source 08 — GD/2nd week-CVS- cases.pdf.

Four G.D. sessions: rheumatic fever & infective endocarditis (Microbiology,
5 cases), myocarditis & pericarditis (Parasitology, 9 cases), carditis
(Pathology, 5 case-embedded MCQs — see below), and cardiac reserve/COP
(Physiology, 3 sub-cases). As in the other weekly files, "G.D. (N): title
(Subject)" is a running FOOTER for the block it names; Case 1 of GD 1 (the
first-degree-heart-block boy) sits before the GD 1 header and was
mis-attributed subject=None/gd=None by raw forward parsing — corrected to
Microbiology/GD 1 below. This trailing-header bug was deliberately NOT fixed
in the parser update (it risks mis-assigning subjects the other way), so
these manual overrides stay.

Re-extracted against the corrected lib_gd.parse() — expected 97 items / 5
MCQ, up from the earlier 90/0. The 5 recovered MCQs are GD 3's "Cases of
carditis" (Pathology): each case there is itself a single case-embedded MCQ
("...Which of the following is the most likely diagnosis? A. ... B. ...")
with no numbered sub-question line, the exact shape the original buggy
parser could not capture. Two of the five (Aschoff bodies / antecedent
streptococcal-infection type) duplicate source 06's two carditis MCQs
verbatim — the compiler's stem-based dedup will merge them; the other three
(mitral stenosis diagnosis, Aschoff-nodule complication, cause of acute
heart failure) are genuinely new.

The corrected parser's new case_opts-collection rule (options appearing
before any sub-question line are kept, not discarded) has one side effect
here: the GD 2 Parasitology section labels its two acute-Chagas vignettes
"a)" and "b)" (e.g. "Case 1: (Acute chagas disease) a) A 25-year-old
journalist..."), and that lone "a)"/"b)" line matches the option-line regex,
so raw parse() emits two spurious single-option "MCQ" items whose stem is
just "(Acute chagas disease)" and whose one "option" is the entire patient
paragraph. These are not real multiple-choice questions (a valid MCQ never
has one option) — they are recast below as two written items (the same
paragraph as the vignette, with a real standalone question), keeping the
item count at 97 while keeping the MCQ count at the genuine 5.

No answer key is printed anywhere; every answer is `derived`.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '08_GD_Week_2_Cases.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/2nd week-CVS- cases.pdf'

V1 = ('A 20-year-old man presented with painful swelling in his feet, knees and right '
      'wrist 14 days after a throat infection. An ECG at the onset of symptoms showed '
      'first-degree heart block. ESR was 108 mm/hr, CRP 336 mg/ml. Treatment was '
      'started with ciprofloxacin for presumed cellulitis. He developed chest pain and '
      'fever (38.5°C). ASO titres were raised at >800 units/ml, anti-DNAse B 3840 '
      'units/ml. Throat swab showed scanty candida only.')
V2 = ('A 32-year-old female with a history of congenital mitral valve prolapse has been '
      'experiencing fever and shortness of breath. She recently underwent a tooth '
      'extraction. Physical examination revealed a new murmur that was not present '
      'before.')
V3 = ('A 16-year-old female was hospitalized after collapsing without loss of '
      'consciousness, with a new erythematous raised rash on her thighs, preceded by a '
      '2-week history of headache, fever and sore throat. Discharge diagnosis was '
      '"viral syndrome." Nine days later she was readmitted with acute right knee pain, '
      'malaise, and persistent rash. CRP and ESR were elevated. A systolic ejection '
      'murmur was heard and echocardiography revealed polyvalvular disease.')
V4 = ('A 28-year-old patient presented with acute onset of severe high-grade fever and '
      'signs of heart failure. A heart murmur was heard that was not present before, as '
      'well as periodontal infection. His arms showed needle marks of IV drug use.')
V5 = ('A 26-year-old female presented to her village clinic with cough, fever and sore '
      'throat, progressing to labored breathing, tachypnea, anorexia and fatigue. She '
      'had a prominent cardiac murmur and cardiomegaly on chest X-ray. Echocardiogram '
      'showed severe mitral insufficiency and moderate aortic regurgitation. ASO titer '
      'was elevated.')

VC1 = ('A 25-year-old journalist recently returned to Egypt from Brazil, with fever, '
       'anorexia, weight loss, dyspnea, myalgia, mild hepatosplenomegaly, generalized '
       'lymphadenopathy, and unilateral (right) upper/lower eyelid edema with '
       'conjunctivitis. Cardiomegaly was detected with ECG suggestive of right bundle '
       'branch block. A Giemsa-stained blood smear showed flagellated, spindle-shaped '
       '(some C-shaped) protozoa with undulating membranes.')
VC2 = ('A 34-year-old engineer working in Ecuador presented with dyspnea, two weeks of '
       'malaise and headache after being bitten by a big bee-like insect, followed by '
       'fever, malaise, anorexia and headache. Exam showed tachycardia (120/min), '
       'normal BP, fever (40°C), diffuse upper-face edema, and a tender reddish nodule '
       'on the side of the neck. WBC was elevated with relative lymphocytosis; a blood '
       'smear was obtained.')
VC3 = ('A 49-year-old woman who recently immigrated to the US from Nicaragua presented '
       'with dysphagia, constipation, and abdominal pain (no bowel motion for over a '
       'week). Exam showed tachycardia and a distended abdomen; ECG showed a type I '
       'bundle-branch block.')
VC4 = ('A 35-year-old Latin American immigrant to Brazil presented with congestive '
       'heart failure and poor perfusion, no significant past history. ECG showed '
       'right bundle branch block and first-degree AV block. Echocardiogram showed '
       'thinned, dilated ventricles, an apical aneurysm, and ventricular thrombus; '
       'catheterization showed no coronary artery disease.')
VC5 = ('A 60-year-old man was admitted with a one-month history of persistent fever, '
       'epigastric pain, anorexia, vomiting and scleral icterus. The liver was enlarged '
       'and tender. Chest X-ray suggested pericardial effusion, confirmed by '
       'echocardiography. Abdominal ultrasound/CT showed a large abscess in the left '
       'lobe of the liver rupturing upward into the pericardium; thick, "anchovy-sauce" '
       'pus was aspirated from both the liver abscess and pericardial cavity.')
VC6 = ('A 20-year-old male on chemotherapy for the past two years after resection of a '
       'malignant colonic mass presented with chest pain radiating to the right arm, '
       'headache, myalgia and asthenia. Exam was otherwise normal; ECG showed an '
       'incomplete right bundle branch block; echocardiography was unremarkable; '
       'cardiac MRI showed myocardial edema. Toxoplasma-specific immunoglobulins were '
       'positive, and he recovered after specific anti-toxoplasma treatment.')
VC7 = ('A 32-year-old man presented to Assiut University Hospital with chest pain '
       'radiating to the left arm, worse with deep breathing and lying down, for three '
       'days with moderate fever and arthralgia, plus two weeks of asthenia and '
       'bilateral neck lymphadenopathy. Exam: feverish (37.3°C), normal BP, HR 95, '
       'harsh murmur. ECG showed nonspecific repolarization abnormalities with '
       'elevated cardiac enzymes; echocardiogram showed moderate pericardial effusion; '
       'CBC showed absolute and relative monocytosis. Serology was positive for '
       'toxoplasmosis, and he improved with specific treatment.')
VC8 = ('A 21-year-old woman presented with a small, increasingly painful swelling in '
       'the right forearm for one year, a convulsion with loss of consciousness six '
       'months ago, and progressive dyspnea, palpitation, fatigue and mild lower-limb '
       'edema. Routine labs were normal except a mildly elevated ESR. Excision of the '
       'forearm swelling and histopathology identified the lesion.')
VC9 = ('A 19-year-old Indian man presented with 6 months of headache and vomiting, 3 '
       'months of convulsions, and one month of decreased vision with bilateral '
       'proptosis. Exam showed subcutaneous nodules over the right eyelids with mild '
       'bilateral proptosis; labs were normal. CT/MRI of the brain showed multiple '
       'small (3-7 mm) cystic lesions in the cerebral hemispheres, cerebellum, '
       'extra-ocular muscles and neck soft tissues; chest CT showed similar lesions in '
       'both lungs and the cardiac muscle. ECG showed right bundle branch block; '
       'echocardiography confirmed multiple disseminated cystic cardiac lesions — '
       'disseminated cysticercosis.')

V_AHMED = ('Ahmed is a 52-year-old, significantly overweight manager with occasional '
           'angina relieved by nitroglycerin. He woke with crushing chest pressure '
           'radiating down his left arm, unrelieved by nitroglycerin, with nausea and '
           'sweating. In the emergency room his BP was 105/80, with inspiratory rales '
           '(pulmonary edema) and cold, clammy skin. Sequential ECGs and cardiac '
           'enzymes suggested a left ventricular wall myocardial infarction. His '
           'ejection fraction, by echocardiography, was 0.35 (normal 0.55).')
V_HODA = ('Hoda, a 27-year-old assistant manager, woke from a deep sleep more than an '
          'hour late for work and moved rapidly from lying to standing. She briefly '
          'felt lightheaded, thought she might faint, and felt her heart "racing"; the '
          'lightheadedness resolved as she walked toward the bathroom.')
V_MONA = ('Mona, a healthy 34-year-old female volunteer (25-40 years old, no '
          'medications, normal weight and blood pressure), had control measurements of '
          'blood pressure, heart rate, and arterial/venous PO2 taken, with stroke '
          'volume estimated, then walked on a treadmill for 30 minutes at 3 mph. '
          'Systolic/diastolic BP went from 110/70 to 145/60 mmHg, heart rate from 75 to '
          '130 beats/min, estimated stroke volume from 80 to 110 mL, arterial PO2 '
          'stayed at 100 mmHg, and venous PO2 fell from 40 to 25 mmHg.')

TAG_MICRO = 'Department, GDs, Microbiology GD 1'
TAG_PARA = 'Department, GDs, Parasitology GD 2'
TAG_PATH = 'Department, GDs, Pathology GD 3'
TAG_PHYS = 'Department, GDs, Physiology GD 4'

ITEMS = [
    # --- GD 1: rheumatic fever and infective endocarditis cases (Microbiology) ---
    (V1 + ' What is the probable diagnosis of this condition?', None, None,
     'Acute rheumatic fever with carditis — migratory polyarthritis, first-degree AV '
     'block (carditis), elevated ASO/anti-DNAse B titers, and chest pain/fever '
     'following an antecedent throat infection satisfy the revised Jones criteria.',
     TAG_MICRO, 'Microbiology'),
    (V1 + ' Which infection may lead to this disease?', None, None,
     'Pharyngitis caused by group A beta-hemolytic Streptococcus (Streptococcus '
     'pyogenes).',
     TAG_MICRO, 'Microbiology'),
    (V1 + ' What is the pathophysiology of the disease?', None, None,
     'Antibodies raised against the streptococcal M-protein cross-react with cardiac '
     'myosin/valve glycoproteins and with joint and CNS antigens (molecular mimicry, '
     'a type II hypersensitivity reaction), producing carditis, migratory arthritis, '
     'chorea and skin findings 2-4 weeks after the pharyngitis.',
     TAG_MICRO, 'Microbiology'),
    (V1 + ' What is the role of lab testing in diagnosis?', None, None,
     'ASO and anti-DNAse B titers document the antecedent streptococcal infection '
     '(throat culture is often negative by the time rheumatic fever appears), while '
     'ESR and CRP provide evidence of systemic inflammation, both used as Jones minor '
     'criteria alongside the clinical major criteria.',
     TAG_MICRO, 'Microbiology'),
    (V1 + ' What is the best prophylactic measure for the disease?', None, None,
     'Long-term secondary prophylaxis with intramuscular benzathine penicillin G '
     'every 3-4 weeks to prevent recurrent streptococcal pharyngitis and further '
     'rheumatic carditis.',
     TAG_MICRO, 'Microbiology'),

    (V2 + ' What is the most probable diagnosis of the case?', None, None,
     'Infective endocarditis superimposed on the pre-existing mitral valve prolapse, '
     'precipitated by transient bacteremia from the dental extraction.',
     TAG_MICRO, 'Microbiology'),
    (V2 + ' What is the course of the disease?', None, None,
     'Untreated infective endocarditis follows a course of persistent bacteremia and '
     'fever, progressive valve destruction (worsening regurgitant murmur, heart '
     'failure), and septic embolization to the brain, spleen, kidneys and skin '
     '(Osler nodes, Janeway lesions, splinter hemorrhages) unless treated promptly '
     'with prolonged IV antibiotics.',
     TAG_MICRO, 'Microbiology'),
    (V2 + ' What is the causative organism?', None, None,
     'Viridans group streptococci (e.g. Streptococcus sanguinis/mitis) are the '
     'classic cause of subacute endocarditis following a dental procedure on an '
     'already abnormal valve.',
     TAG_MICRO, 'Microbiology'),

    (V3 + ' What is the probable diagnosis of this condition?', None, None,
     'Acute rheumatic fever with polyvalvular carditis, the earlier "viral syndrome" '
     'actually representing the antecedent streptococcal pharyngitis.',
     TAG_MICRO, 'Microbiology'),
    (V3 + ' What is the role of group A streptococci in the pathogenesis of the '
     'disease?', None, None,
     'Cross-reactive (molecular mimicry) antibody and T-cell responses to '
     'streptococcal M-protein epitopes damage the heart valves and joints, producing '
     'the systemic features of rheumatic fever.',
     TAG_MICRO, 'Microbiology'),
    (V3 + ' Which antibody titer tests are performed in the diagnosis of such a '
     'disease?', None, None,
     'The antistreptolysin O (ASO) titer and the anti-DNAse B titer are the standard '
     'tests used to confirm a recent group A streptococcal infection.',
     TAG_MICRO, 'Microbiology'),
    (V3 + ' How does the prevalence of the disease vary by race?', None, None,
     'Acute rheumatic fever is far more prevalent in developing regions and lower '
     'socioeconomic groups, where crowding and limited access to antibiotics for '
     'streptococcal pharyngitis are common; some populations (e.g. Aboriginal '
     'Australians, sub-Saharan Africans, South Asians) show disproportionately high '
     'rates, reflecting both HLA-linked genetic susceptibility and environmental/'
     'healthcare-access factors rather than race itself.',
     TAG_MICRO, 'Microbiology'),
    (V3 + ' What are the cardiac complications of the disease?', None, None,
     'Pancarditis (myocarditis, pericarditis, valvulitis), progression to chronic '
     'rheumatic valve disease (mitral stenosis being most characteristic), heart '
     'failure, and arrhythmias.',
     TAG_MICRO, 'Microbiology'),

    (V4 + ' What is the most probable diagnosis of the case?', None, None,
     'Acute infective endocarditis, most likely involving a right-sided '
     '(tricuspid) valve given the IV drug use, with periodontal infection as an '
     'additional bacteremia source.',
     TAG_MICRO, 'Microbiology'),
    (V4 + ' What is the causative organism?', None, None,
     'Staphylococcus aureus is the leading cause of acute infective endocarditis in '
     'intravenous drug users, typically affecting the tricuspid valve.',
     TAG_MICRO, 'Microbiology'),
    (V4 + ' What is the best diagnostic test?', None, None,
     'Blood cultures (at least three sets from different sites/times) combined with '
     'echocardiography (transthoracic, or transesophageal if non-diagnostic) to '
     'demonstrate vegetations, applying the modified Duke criteria.',
     TAG_MICRO, 'Microbiology'),
    (V4 + ' What is an alternative test in case of failure of routine testing?',
     None, None,
     'If blood cultures are negative (culture-negative endocarditis), serology or '
     'PCR for fastidious organisms (HACEK group, Bartonella, Coxiella) or '
     'broad-range 16S rRNA PCR on excised valve tissue can identify the organism.',
     TAG_MICRO, 'Microbiology'),

    (V5 + ' What is the probable diagnosis of this condition?', None, None,
     'Acute rheumatic fever with carditis involving both the mitral and aortic '
     'valves.',
     TAG_MICRO, 'Microbiology'),
    (V5 + ' What probable factor in the history is relevant to the diagnosis?',
     None, None,
     'Her recent cough, fever and sore throat — an antecedent streptococcal '
     'pharyngitis — 2-3 weeks before the cardiac presentation.',
     TAG_MICRO, 'Microbiology'),
    (V5 + ' What are the limitations of throat culture in such a disease?', None, None,
     'Throat culture is often negative by the time rheumatic fever manifests (the '
     'streptococcal infection has usually cleared by 2-4 weeks), has variable '
     'sensitivity, and cannot distinguish an active infection from asymptomatic '
     'carriage.',
     TAG_MICRO, 'Microbiology'),
    (V5 + ' What is the role of blood culture in the workup of such a disease?',
     None, None,
     'Blood culture does not diagnose rheumatic fever itself, since it is a '
     'post-infectious immune phenomenon rather than active bacteremia, but it is '
     'essential to exclude infective endocarditis as a differential in a febrile '
     'patient with a new murmur.',
     TAG_MICRO, 'Microbiology'),

    # --- GD 2: myocarditis and pericarditis cases (Parasitology) ---
    (VC1 + ' What clinical and laboratory clues in this presentation point toward a '
     'systemic protozoal (rather than bacterial or viral) infection?', None, None,
     'Recent travel to an endemic area (Brazil), prolonged fever with weight loss, '
     'generalized lymphadenopathy and hepatosplenomegaly, unilateral periorbital '
     'edema with conjunctivitis (Romaña\'s sign), cardiomegaly with a conduction '
     'abnormality, and — most specifically — flagellated protozoa seen directly on a '
     'Giemsa-stained blood smear together point to a systemic protozoal infection '
     '(acute Chagas disease) rather than a bacterial or viral cause.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' What is the name of this patient\'s illness, and which blood protozoan '
     'parasite is causing the infection?', None, None,
     'Acute Chagas disease (American trypanosomiasis), caused by Trypanosoma cruzi.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' How is this infection transmitted?', None, None,
     'Via the feces of an infected triatomine bug, deposited near the bite wound or '
     'mucous membranes and rubbed in by the host (contaminative transmission); also '
     'congenital transmission, blood transfusion, organ transplant, and rarely oral '
     'ingestion of contaminated food/drink.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' Why is the vector for this protozoan known as the "kissing bug"?',
     None, None,
     'Triatomine bugs characteristically bite the face — around the lips and eyes '
     '— of a sleeping host.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' Describe the infective and diagnostic stages of this parasite.', None, None,
     'The infective stage is the metacyclic trypomastigote (in the bug\'s feces); the '
     'diagnostic stage in the acute phase is the trypomastigote seen on Giemsa-'
     'stained blood smears, while amastigotes are the intracellular tissue form.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' What is the name of the lesion that may develop at the site of '
     'inoculation, and what is the name given to the unilateral eye edema seen in '
     'this disease?', None, None,
     'The inoculation-site skin lesion is a chagoma; unilateral periorbital edema '
     'with conjunctivitis is Romaña\'s sign.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' Which methods are available to diagnose this infection?', None, None,
     'Direct microscopy of blood smears in the acute phase, xenodiagnosis/blood '
     'culture, PCR, and serology (ELISA/IFA for IgG) for the chronic phase.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' How does this parasite differ from other parasites in the same genus?',
     None, None,
     'Trypanosoma cruzi multiplies intracellularly (as amastigotes in tissues), '
     'unlike the African trypanosomes (T. brucei gambiense/rhodesiense), which '
     'remain extracellular in blood and lymph and are transmitted by the tsetse fly '
     'bite rather than by contaminative bug feces.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' How is this infection treated?', None, None,
     'Benznidazole or nifurtimox, most effective when given in the acute phase.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' This infection may be acquired during blood transfusion. List other '
     'protozoan parasitic infections that may be transmitted during blood '
     'transfusions.', None, None,
     'Plasmodium species (malaria), Toxoplasma gondii, Babesia species, and '
     'Leishmania species.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' Explain the cardiac abnormalities found in this patient.', None, None,
     'Direct parasitic invasion and immune-mediated inflammation of the myocardium '
     '(acute myocarditis) impair conduction (right bundle branch block) and '
     'contractility, producing cardiomegaly.',
     TAG_PARA, 'Parasitology'),
    (VC1 + ' What other complications may occur?', None, None,
     'Chronic Chagas cardiomyopathy (dilated cardiomyopathy, arrhythmia, apical '
     'aneurysm, mural thrombus/embolism) and megaesophagus/megacolon from '
     'destruction of the myenteric autonomic plexus.',
     TAG_PARA, 'Parasitology'),

    (VC2 + ' What clinical and laboratory clues in this presentation point toward the '
     'same systemic protozoal infection as the previous case?', None, None,
     'Recent travel/work in an endemic area (Ecuador) with an insect bite followed by '
     'fever, malaise and headache; a localized inoculation-site nodule with diffuse '
     'facial/periorbital edema; tachycardia; and a reactive lymphocytosis together '
     'suggest acute Chagas disease (Trypanosoma cruzi), to be confirmed on the blood '
     'smear.',
     TAG_PARA, 'Parasitology'),
    (VC2 + ' What is the mode of infection of the causative parasite?', None, None,
     'Contamination of the bite wound or mucous membranes/conjunctiva with feces of '
     'the triatomine bug containing metacyclic trypomastigotes of Trypanosoma cruzi.',
     TAG_PARA, 'Parasitology'),
    (VC2 + ' How can you confirm your diagnosis?', None, None,
     'Microscopic examination of Giemsa-stained blood smears for trypomastigotes '
     '(acute phase), supported by serology or PCR.',
     TAG_PARA, 'Parasitology'),
    (VC2 + ' What is the pathology and pathophysiology of acute myocarditis?', None, None,
     'T. cruzi amastigotes multiply within myocardial fibers, rupturing them and '
     'provoking a lymphocytic/macrophage inflammatory infiltrate that damages '
     'myocytes and the conduction system, impairing contractility and causing '
     'arrhythmia or conduction block.',
     TAG_PARA, 'Parasitology'),
    (VC2 + ' What is the best drug used for this case?', None, None,
     'Benznidazole (first-line) or nifurtimox.',
     TAG_PARA, 'Parasitology'),
    (VC2 + ' Mention the methods to prevent and control these cases.', None, None,
     'Vector control (insecticide spraying, improved housing to eliminate triatomine '
     'habitats), screening of blood and organ donors, and treatment of infected '
     'mothers/infants to prevent congenital transmission.',
     TAG_PARA, 'Parasitology'),

    (VC3 + ' What is the causative protozoan responsible for this case?', None, None,
     'Trypanosoma cruzi.',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' What is the vector of the responsible protozoan?', None, None,
     'Triatomine ("kissing") bugs, e.g. Triatoma, Rhodnius and Panstrongylus '
     'species.',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' What is the classic sign associated with the acute form of this '
     'condition?', None, None,
     'Romaña\'s sign (unilateral periorbital edema) or a chagoma at the inoculation '
     'site.',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' Where in the world is this condition commonly found?', None, None,
     'Endemic to rural Latin America, from Mexico and Central America through South '
     'America.',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' What is the pathophysiology of this condition?', None, None,
     'Chronic inflammatory destruction of the myenteric (Auerbach\'s) plexus neurons '
     'abolishes normal peristalsis, producing megaesophagus (dysphagia) and '
     'megacolon (constipation, abdominal distension).',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' What is the appropriate treatment for this condition?', None, None,
     'Benznidazole or nifurtimox for the underlying infection, plus symptomatic or '
     'surgical management of the megaesophagus/megacolon in advanced disease.',
     TAG_PARA, 'Parasitology'),
    (VC3 + ' What other disease is caused by the other protozoan species that causes '
     'this condition?', None, None,
     'Other Trypanosoma species (T. brucei gambiense and T. brucei rhodesiense) '
     'cause African sleeping sickness, transmitted by the tsetse fly.',
     TAG_PARA, 'Parasitology'),

    (VC4 + ' What is the suggestive diagnosis of this case?', None, None,
     'Chronic Chagas cardiomyopathy.',
     TAG_PARA, 'Parasitology'),
    (VC4 + ' What is the pathology and pathophysiology of chronic cardiomyopathy?',
     None, None,
     'Longstanding immune-mediated myocardial inflammation and fibrosis produce a '
     'dilated, thin-walled cardiomyopathy with apical aneurysm formation, conduction '
     'disturbances (bundle branch/AV block), and mural thrombus predisposing to '
     'embolism.',
     TAG_PARA, 'Parasitology'),
    (VC4 + ' What is the mode of infection of the causative parasite?', None, None,
     'Contamination of skin or mucosa with feces of the triatomine bug containing '
     'metacyclic trypomastigotes.',
     TAG_PARA, 'Parasitology'),
    (VC4 + ' How can you confirm your diagnosis?', None, None,
     'Serology (IgG ELISA/IFA — the mainstay in the chronic phase, since '
     'parasitemia is low), supported by PCR, with echocardiography documenting the '
     'structural cardiac findings.',
     TAG_PARA, 'Parasitology'),
    (VC4 + ' Which other systems are most commonly affected in this disease?', None, None,
     'The gastrointestinal tract (megaesophagus, megacolon from myenteric plexus '
     'destruction) and, less commonly, the peripheral/autonomic nervous system.',
     TAG_PARA, 'Parasitology'),

    (VC5 + ' What is the causative parasite of this case?', None, None,
     'Entamoeba histolytica.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' What is the mode of infection of the causative parasite?', None, None,
     'Fecal-oral ingestion of mature (quadrinucleate) Entamoeba histolytica cysts in '
     'contaminated food or water.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' Can abscesses caused by this parasite occur in organs other than the '
     'liver?', None, None,
     'Yes — amoebic abscesses most often involve the liver but can also occur in the '
     'lung, brain and spleen via hematogenous (portal, then systemic) spread.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' Which serological tests were probably ordered to confirm the diagnosis?',
     None, None,
     'Indirect hemagglutination (IHA) and ELISA for anti-Entamoeba antibodies.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' What is the possible differential diagnosis?', None, None,
     'Pyogenic liver abscess, hydatid (Echinococcus) cyst, and other causes of '
     'pericardial effusion (tuberculous, viral, or malignant pericarditis).',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' What is the pathogenesis of the disease?', None, None,
     'Trophozoites invade the colonic mucosa causing flask-shaped ulcers, then '
     'travel via the portal vein to the liver, where they cause coagulative '
     'necrosis (an "anchovy-sauce" abscess); an abscess in the left lobe can rupture '
     'directly upward through the diaphragm into the pericardium.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' How can you properly treat this case?', None, None,
     'Metronidazole (a tissue amoebicide) followed by a luminal agent (e.g. '
     'paromomycin) to eradicate intestinal cysts, plus percutaneous or surgical '
     'drainage of the pericardial/liver collection given the rupture.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' What risk to the patient exists in performance of a surgical procedure '
     'to obtain a liver aspirate?', None, None,
     'Risk of spilling infected material and secondary bacterial infection, of '
     'provoking further rupture or spread of the abscess into adjacent structures '
     '(pericardium, pleura, peritoneum), and of hemorrhage.',
     TAG_PARA, 'Parasitology'),
    (VC5 + ' Discuss methods of control and prevention of infection with this '
     'parasite.', None, None,
     'Improved sanitation and safe water supply, proper sewage disposal, food and '
     'water hygiene, and treatment/screening of asymptomatic cyst carriers and food '
     'handlers.',
     TAG_PARA, 'Parasitology'),

    (VC6 + ' What is the association between the patient\'s history of receiving '
     'chemotherapy and this infection?', None, None,
     'Chemotherapy-induced immunosuppression allows reactivation of latent tissue '
     'cysts of Toxoplasma gondii (or increases susceptibility to new infection), '
     'leading to clinically apparent toxoplasmic myocarditis.',
     TAG_PARA, 'Parasitology'),
    (VC6 + ' Which other group of individuals is at risk when infected with this '
     'parasite?', None, None,
     'Immunocompromised patients generally (HIV/AIDS, transplant recipients on '
     'immunosuppressants) and the fetus of a mother with primary infection during '
     'pregnancy (congenital toxoplasmosis).',
     TAG_PARA, 'Parasitology'),
    (VC6 + ' How might this patient be treated?', None, None,
     'Pyrimethamine plus sulfadiazine with folinic acid to reduce bone-marrow '
     'toxicity; clindamycin is an alternative in sulfa-allergic patients.',
     TAG_PARA, 'Parasitology'),
    (VC6 + ' How is this infection transmitted?', None, None,
     'Ingestion of undercooked meat containing tissue cysts, ingestion of oocysts '
     'from cat feces-contaminated food/soil/water, congenital transplacental '
     'transmission, and rarely blood transfusion or organ transplant.',
     TAG_PARA, 'Parasitology'),
    (VC6 + ' What is the commonest habitat of this parasite in immunocompromised '
     'patients?', None, None,
     'The central nervous system (causing toxoplasmic encephalitis) is the most '
     'common site of reactivation, though the myocardium and other organs can also '
     'be involved.',
     TAG_PARA, 'Parasitology'),
    (VC6 + ' What are the diagnostic and infective stages of this parasite?', None, None,
     'The infective stages are the oocyst (shed in cat feces) and the tissue cyst '
     '(bradyzoites, from undercooked meat); the diagnostic stage seen in active '
     'infection is the tachyzoite.',
     TAG_PARA, 'Parasitology'),

    (VC7 + ' What is the mode of transmission of the causative parasite?', None, None,
     'Ingestion of undercooked meat containing tissue cysts or of food/water '
     'contaminated with cat-feces oocysts, or congenital transmission.',
     TAG_PARA, 'Parasitology'),
    (VC7 + ' Mention people at risk of this parasite.', None, None,
     'Immunocompromised individuals, pregnant women (risk of congenital '
     'toxoplasmosis), and anyone consuming undercooked meat or handling '
     'cat litter/contaminated soil.',
     TAG_PARA, 'Parasitology'),
    (VC7 + ' How would you confirm your diagnosis?', None, None,
     'Serology (IgM/IgG for Toxoplasma) supported by echocardiography for the '
     'pericardial effusion; PCR can be used in equivocal cases.',
     TAG_PARA, 'Parasitology'),
    (VC7 + ' What is the recommended treatment of toxoplasmosis?', None, None,
     'Pyrimethamine plus sulfadiazine with folinic acid (spiramycin is used instead '
     'in pregnancy to reduce fetal transmission).',
     TAG_PARA, 'Parasitology'),

    (VC8 + ' Which parasitic infection do you think this patient has?', None, None,
     'Cysticercosis.',
     TAG_PARA, 'Parasitology'),
    (VC8 + ' Which helminth causes this infection?', None, None,
     'Taenia solium, the pork tapeworm, whose larval stage (cysticercus) causes '
     'cysticercosis.',
     TAG_PARA, 'Parasitology'),
    (VC8 + ' How do humans acquire this infection?', None, None,
     'By ingesting Taenia solium eggs (from contaminated food/water or fecal-oral '
     'autoinfection); the eggs hatch into oncospheres that penetrate the gut wall and '
     'migrate to tissues (muscle, brain, eye, subcutaneous tissue) to form cysticerci.',
     TAG_PARA, 'Parasitology'),
    (VC8 + ' How do you diagnose extra-intestinal infection with this parasite?',
     None, None,
     'Imaging (CT/MRI showing cystic lesions, sometimes with a visible scolex), '
     'serology (ELISA for anticysticercal antibodies), and histopathology of any '
     'excised nodule.',
     TAG_PARA, 'Parasitology'),
    (VC8 + ' Which treatment is available for this infection?', None, None,
     'Albendazole (or praziquantel) with corticosteroids to control inflammation '
     'around dying cysts, plus surgical excision of accessible lesions such as the '
     'forearm nodule; neurocysticercosis with mass effect may require surgery.',
     TAG_PARA, 'Parasitology'),

    (VC9 + ' What is the name of the parasite causing this infection?', None, None,
     'Taenia solium (larval cysticercus stage — cysticercosis).',
     TAG_PARA, 'Parasitology'),
    (VC9 + ' What is the mode of transmission of the causative parasite?', None, None,
     'Fecal-oral ingestion of Taenia solium eggs, from a tapeworm carrier\'s feces '
     'contaminating food or water, or by autoinfection.',
     TAG_PARA, 'Parasitology'),
    (VC9 + ' How would you confirm your diagnosis?', None, None,
     'CT/MRI showing multiple small cystic lesions (brain, muscle, orbit, heart), '
     'often with a visible scolex, combined with serology (ELISA) for anticysticercal '
     'antibodies.',
     TAG_PARA, 'Parasitology'),

    # --- GD 3: Cases of carditis (Pathology) ---
    # These five cases are each a single case-embedded MCQ (the vignette itself ends
    # "Which of the following is the most likely diagnosis?" with options printed
    # directly under it, no numbered sub-question line) — exactly the shape the
    # original buggy parser could not capture. Cases 2 and "Q5" duplicate source 06's
    # two carditis MCQs verbatim; the compiler's stem-based dedup will merge them.
    ('A 44-year-old woman presents with worsening fatigue and dyspnea. The pertinent '
     'medical history is that she had repeated attacks of rheumatic fever during '
     'childhood. Physical examination finds a diastolic murmur. A chest radiograph '
     'shows an enlarged left atrium. Which of the following is the most likely '
     'diagnosis?',
     ['Aortic regurgitation', 'Aortic stenosis', 'Mitral regurgitation',
      'Mitral stenosis', 'Pulmonary stenosis'],
     'D',
     'Repeated childhood rheumatic fever, a diastolic murmur, and an enlarged left '
     'atrium are the classic picture of chronic rheumatic mitral stenosis: fibrous '
     'fusion and calcification of the mitral leaflets and commissures obstructs '
     'diastolic left-atrial emptying, dilating the left atrium and producing a '
     'mid-diastolic murmur.',
     TAG_PATH, 'Pathology'),
    ('A 6-year-old boy develops fever, joint pain, and a diffuse skin rash '
     'approximately 3 weeks after recovering from a sore throat. Physical '
     'examination finds several small skin nodules, and laboratory examination finds '
     'an elevated erythrocyte sedimentation rate along with an elevated '
     'antistreptolysin O titer. Which of the following abnormalities is most '
     'characteristic of this boy\'s disease?',
     ['Anitschkow cells within the epidermis', 'Aschoff bodies within the myocardium',
      'Langhans giant cells within the dermis',
      'Psammoma bodies within the endocardium',
      'Virchow cells within the nasopharynx'],
     'B',
     'The picture is acute rheumatic fever following streptococcal pharyngitis. Its '
     'pathognomonic lesion is the Aschoff body in the myocardium — a focus of '
     'fibrinoid necrosis surrounded by lymphocytes, plasma cells and plump activated '
     'macrophages (Anitschkow cells, which lie in the myocardium, not the '
     'epidermis).',
     TAG_PATH, 'Pathology'),
    ('A 10-year-old girl suffering from fleeting (migratory) arthritis developed '
     'chest pain. Auscultation shows a friction rub. Endocardial biopsy reveals '
     'Aschoff nodules. Which of the following complications is this girl liable to '
     'develop?',
     ['Aortic aneurysm', 'Infective endocarditis', 'Cerebral hemorrhage', 'Toxemia',
      'Anemia'],
     'B',
     'Rheumatic valvulitis (Aschoff nodules, friction rub from pericarditis) scars '
     'and deforms the heart valves; a damaged valve is the single most important '
     'predisposing factor for later infective endocarditis, since it provides a '
     'surface for platelet-fibrin thrombus formation and bacterial seeding during '
     'any bacteremia.',
     TAG_PATH, 'Pathology'),
    ('A 12-year-old boy had a respiratory infection. Two weeks later he presented '
     'with fever and polyarthritis; laboratory investigations revealed a raised ESR '
     'and elevated C-reactive protein. Two days later, the child developed signs of '
     'acute heart failure. The most possible cause of this failure is:',
     ['Myocardial infarction', 'Toxic myocarditis', 'Acute valvulitis', 'Septicemia',
      'Fibrinous pericarditis'],
     'B',
     'In acute rheumatic carditis, diffuse (toxic) myocarditis — interstitial '
     'inflammation with Aschoff bodies infiltrating the myocardium — directly '
     'impairs contractility and is the usual cause of acute pump failure in a child '
     'this early in the illness, whereas valvulitis alone produces murmurs rather '
     'than acute heart failure at this stage, and myocardial infarction/septicemia '
     'do not fit a 12-year-old with post-streptococcal arthritis.',
     TAG_PATH, 'Pathology'),
    ('Which of the following types of infection precedes, by several weeks, the '
     'development of acute rheumatic fever?',
     ['Group A beta-hemolytic streptococcal infection of the pharynx',
      'Group D alpha-hemolytic streptococcal infection of the heart',
      'Staphylococcus aureus infection of the lungs',
      'Streptococcus pyogenes infection of the skin',
      'Treponema pallidum infection of the abdominal aorta'],
     'A',
     'Acute rheumatic fever follows pharyngitis with group A beta-hemolytic '
     'streptococci (Streptococcus pyogenes) by 1-5 weeks. It is a type II '
     'hypersensitivity reaction: antibodies against streptococcal M protein '
     'cross-react with cardiac antigens. Streptococcal skin infection causes '
     'post-streptococcal glomerulonephritis, not rheumatic fever.',
     TAG_PATH, 'Pathology'),

    # --- GD 4: cardiac reserve and COP cases (Physiology) ---
    (V_AHMED + ' Which information provided in the case tells you that Ahmed\'s stroke '
     'volume was decreased?', None, None,
     'The low-normal blood pressure (105/80) despite a large infarct, the cold, '
     'clammy skin (reflex vasoconstriction compensating for reduced output), and the '
     'markedly reduced ejection fraction (0.35 versus normal 0.55) together indicate '
     'a fall in stroke volume.',
     TAG_PHYS, 'Physiology'),
    (V_AHMED + ' What is the meaning of Ahmed\'s decreased ejection fraction?', None, None,
     'Ejection fraction is the proportion of end-diastolic volume ejected per beat; a '
     'fall to 0.35 means his infarcted, weakened left ventricle pumps out only about '
     '35% of its filled volume instead of the normal ~55%, reflecting impaired '
     'contractility.',
     TAG_PHYS, 'Physiology'),
    (V_AHMED + ' Why did pulmonary edema develop?', None, None,
     'The failing left ventricle cannot eject its preload adequately, so blood backs '
     'up and raises left atrial and pulmonary venous/capillary hydrostatic pressure, '
     'forcing fluid out of the pulmonary capillaries into the alveolar interstitium '
     'and airspaces.',
     TAG_PHYS, 'Physiology'),
    (V_AHMED + ' What is the suspected type of heart failure (left or right)?',
     None, None,
     'Left-sided heart failure — pulmonary edema and reduced ejection fraction from '
     'left ventricular infarction.',
     TAG_PHYS, 'Physiology'),

    (V_HODA + ' There was a brief, initial decrease in arterial pressure that caused '
     'her light-headedness. Describe the sequence of events that produced this '
     'transient fall in arterial pressure.', None, None,
     'Standing shifts roughly 500-700 mL of blood into the dependent leg veins under '
     'gravity, reducing venous return, ventricular filling (preload), stroke volume '
     'and hence cardiac output and arterial pressure.',
     TAG_PHYS, 'Physiology'),
    (V_HODA + ' Why did the decrease in arterial pressure cause her to feel '
     'light-headed?', None, None,
     'The transient drop in arterial pressure briefly reduces cerebral perfusion '
     'pressure below the level needed for adequate brain blood flow, producing '
     'light-headedness.',
     TAG_PHYS, 'Physiology'),
    (V_HODA + ' Describe the specific effects of the reflex that restored her '
     'arterial pressure on heart rate and myocardial contractility, and the receptors '
     'involved.', None, None,
     'The fall in arterial pressure unloads the arterial (carotid sinus/aortic arch) '
     'baroreceptors, reducing their afferent firing; this reflexively increases '
     'sympathetic (beta-1 adrenergic) and decreases parasympathetic (vagal) outflow '
     'to the heart, raising heart rate and contractility.',
     TAG_PHYS, 'Physiology'),
    (V_HODA + ' How does each component of the reflex help to restore arterial '
     'pressure?', None, None,
     'Since MAP = cardiac output x total peripheral resistance (CO = HR x SV), the '
     'reflex rise in heart rate and contractility increases cardiac output, while '
     'sympathetically driven arteriolar vasoconstriction increases TPR — both raise '
     'arterial pressure back toward normal.',
     TAG_PHYS, 'Physiology'),
    (V_HODA + ' In addition to the reflex correction of blood pressure, walking to '
     'the bathroom helped return her arterial pressure to normal. How did walking '
     'help?', None, None,
     'Rhythmic contraction of the leg skeletal muscles compresses the deep veins '
     '(the "muscle pump"), propelling blood back toward the heart and increasing '
     'venous return, which helps restore stroke volume and arterial pressure.',
     TAG_PHYS, 'Physiology'),

    (V_MONA + ' Describe the cardiovascular responses to moderate exercise, '
     'including the roles of the autonomic nervous system and local control of blood '
     'flow in skeletal muscle. What is the ultimate purpose of these responses?',
     None, None,
     'Exercise increases sympathetic (and decreases parasympathetic) outflow, '
     'raising heart rate and contractility, while local metabolic vasodilators '
     '(adenosine, CO2, K+, H+, lactate) in active skeletal muscle override '
     'sympathetic vasoconstriction to increase local blood flow; the purpose is to '
     'increase oxygen and nutrient delivery to the exercising muscle in proportion '
     'to its increased metabolic demand.',
     TAG_PHYS, 'Physiology'),
    (V_MONA + ' What were Mona\'s mean arterial pressure and pulse pressure for the '
     'control and exercise periods, respectively?', None, None,
     'Control: pulse pressure = 110-70 = 40 mmHg, MAP ≈ 70 + 1/3(40) ≈ 83 mmHg. '
     'Exercise: pulse pressure = 145-60 = 85 mmHg, MAP ≈ 60 + 1/3(85) ≈ 88 mmHg — MAP '
     'rose only modestly while pulse pressure roughly doubled.',
     TAG_PHYS, 'Physiology'),
    (V_MONA + ' What was her cardiac output for the control and exercise periods, '
     'respectively? Which factor (stroke volume or heart rate) made the greater '
     'contribution to the increase in cardiac output?', None, None,
     'Control CO ≈ 75 x 80 mL = 6000 mL/min (6 L/min); exercise CO ≈ 130 x 110 mL = '
     '14300 mL/min (~14.3 L/min). Heart rate rose proportionally more (about 73%) '
     'than stroke volume (about 38%), so the increase in heart rate made the greater '
     'contribution to the rise in cardiac output.',
     TAG_PHYS, 'Physiology'),
    (V_MONA + ' What is the significance of the observed change in pulse pressure?',
     None, None,
     'The widened pulse pressure during exercise reflects the larger stroke volume '
     'ejected rapidly into the aorta, raising systolic pressure — a normal, healthy '
     'hemodynamic response to exercise rather than a sign of arterial stiffening.',
     TAG_PHYS, 'Physiology'),
    (V_MONA + ' Why was the systolic pressure increased during exercise? Why did the '
     'diastolic pressure remain essentially unchanged?', None, None,
     'Systolic pressure rises because the larger stroke volume, ejected more '
     'forcefully, distends the aorta further; diastolic pressure changes little (or '
     'falls slightly) because exercise-induced vasodilation in skeletal muscle lowers '
     'total peripheral resistance, offsetting the effect of the increased cardiac '
     'output on diastolic runoff.',
     TAG_PHYS, 'Physiology'),
]


def main():
    qs = []
    for stem, options, correct, exp, tag, subj in ITEMS:
        qs.append(Q(stem, options, correct, 'derived', exp=exp, tag=tag, tag_suggere=subj))
    meta = {'Source file': SRC,
            'Type': 'GD case handout, 18 pages; 4 G.D. sessions across Microbiology, '
                    'Parasitology, Pathology (dropped — see script docstring) and '
                    'Physiology',
            'Tag': 'Department, GDs, <Subject> GD <N>', 'tagSuggere': 'varies by item',
            'Year': 'None',
            'Answer source': 'derived — no key is printed anywhere in the source'}
    n = write_md(OUT, 'Source 08 — GD Week 2 Cases', meta, qs)
    mcq = sum(1 for s, o, c, e, t, sj in ITEMS if o)
    ans = collections.Counter(c for s, o, c, e, t, sj in ITEMS if o)
    print(f'source 08: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: option-A blocks = {mcq}; ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({mcq} MCQs — bias gate n/a, <15)')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
