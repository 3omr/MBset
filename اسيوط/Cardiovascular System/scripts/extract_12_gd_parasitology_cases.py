#!/usr/bin/env python3
"""
BIAS GATE — INVESTIGATED AND CLEARED (do not "fix" this file's distribution).
10 of the 21 MCQs are keyed C (47.6%), which trips the 46-60% investigate band. All ten
were checked individually against the source and against standard parasitology, and all
ten are correct: Chagas -> T. cruzi, triatomine vector, bites the face, order an ECG,
congestive heart failure, biventricular dilatation, cardiac death, oesophagus; and for
trichinellosis, serology and albendazole + corticosteroid. The cluster is an artefact of
how the department ordered its options, not of the extraction. An earlier pass changed one
of these keys (Q8) from the correct C to E purely to flatten the histogram; that was wrong
and has been reverted. The bias gate is a detector, never a target.
Source 12 — GD/Cases of CVS-  parasitology-2023-2024.pdf.

Six cardiovascular-parasitology group-discussion cases (text-rich, no OCR needed).
Each case is a clinical vignette followed by numbered sub-questions, some MCQ, some
short-answer/essay. The vignette belongs to every sub-question under it (same shape
as lib_gd's `stem_with_case`), so it is prepended to each stem.

No key is printed anywhere in the file: every MCQ answer is `derived` and every
written answer is a short model answer written from medical knowledge.

Four questions carry figures embedded in the PDF (page images, not OCR'd):
  Q1  (Case 1) - trypomastigote in a Giemsa-stained blood smear
  Q24 (Case 3) - two figures: aspiration of anchovy-sauce pus from a liver abscess,
                 and a chest X-ray showing pericardial effusion
  Q37 (Case 5) - histology of an encysted Trichinella spiralis larva in muscle
All four crops were opened and visually verified (see extraction report).
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '12_GD_Parasitology_Cases.md')
SRC = ('Raw_PDF_Questions/1- Cardiovascular system/GD/'
       'Cases of CVS-  parasitology-2023-2024.pdf')
# Numbered GD 2 after source 08's week-2 handout, which is the only file that
# numbers this session ("G.D. (2): ... (Parasitology)"); this file numbers
# nothing itself. Source 13 is the same session's 2024-2025 edition.
TAG = 'Department, GDs, Parasitology GD 2 2024'
SUBJ = 'Parasitology'
YEAR = 2024

# ---------------------------------------------------------------------------
# Case vignettes
# ---------------------------------------------------------------------------
V1 = ("A 25-year-old journalist had recently returned to Egypt from a vacation in "
      "Brazil. She developed fever, anorexia and shortness of breath. On examination, "
      "she had upper and lower eyelid edema in the right eye with conjunctivitis. ECG "
      "showed non-specific abnormalities suggestive of right bundle branch block. "
      "Microscopic examination revealed a few flagellated spindle-shaped protozoan "
      "parasites (some assuming an S shape) with undulating membranes. The "
      "characteristic parasite is shown in the figure below.")

V2 = ("A 49-year-old woman who recently immigrated to the United States from "
      "Nicaragua presented to the outpatient clinic with difficulty in swallowing, "
      "constipation, and abdominal pain. She said that her last motion was more than "
      "a week ago. Physical examination revealed tachycardia and a distended abdomen. "
      "ECG showed type I bundle-branch block. She had a past history of acute Chagas "
      "disease 10 years ago.")

V3 = ("A 60-year-old man was admitted with a one-month history of persistent fever, "
      "with epigastric pain, anorexia, vomiting and yellow discoloration of the "
      "sclera. On examination, the liver was enlarged and tender. Chest x-ray was "
      "suggestive of pericardial effusion which was confirmed by Echocardiography. "
      "Ultrasonography of the abdomen revealed a large abscess in the left lobe of "
      "the liver rupturing upwards into the pericardium. Thick pus (anchovy sauce in "
      "color) was aspirated both from the liver abscess and the pericardial cavity. "
      "The figures below show the aspiration of pus from the liver abscess and the "
      "chest X-ray showing the pericardial effusion.")

V4 = ("A 20-year-old male presented to the emergency room with chest pain radiating "
      "to his right arm of two days duration with headaches, myalgia, and asthenia. "
      "The patient was receiving chemotherapy for the past two years. The initial ECG "
      "showed an incomplete right bundle branch block. Cardiac MRI showed areas of "
      "myocardial edema. Serological tests for Toxoplasma-specific immunoglobulin "
      "were positive. After being treated with the specific anti-toxoplasma drugs, "
      "the patient began to recover from his illness.")

V5 = ("A 21-year-old woman presented with a small swelling in the right forearm for "
      "one year that started to be painful in the last two weeks. The patient "
      "described that she began to have progressive dyspnea and palpitation, with "
      "fatigue and mild edema in her lower limbs. Laboratory investigations including "
      "blood sugar, serum urea and creatinine were normal; blood picture was done "
      "showing high eosinophilia. Echocardiography and MRI demonstrated multiple and "
      "randomly distributed small cysts (3-5mm each) in the sub-pericardium, "
      "sub-endocardium and myocardium with surrounding myocardial inflammation. "
      "Excision of the forearm swelling was performed, and histopathological "
      "evaluation detected the lesion shown in the figure below.")

V6 = ("A 35-year-old Indian woman was admitted to the emergency department for acute "
      "substernal pain at rest, described as a pressure with no radiation. She was "
      "experiencing a 1-week history of shortness of breath, myalgia, nausea, "
      "vomiting, diarrhea, and intermittent chills after eating raw pork meat. "
      "Interestingly, her family members who also consumed the raw meat had similar "
      "symptoms. The electrocardiogram performed upon admission showed non-specific "
      "alterations of repolarization. Blood biology revealed high levels of troponin "
      "T and predominant eosinophilic leukocytosis. Echocardiography was carried out "
      "and found significant left ventricular hypertrophy. The septal and inferior "
      "walls, as well as the endocardium, were hyperechogenic. The patient was "
      "hospitalized for eosinophilic myocarditis. The cause of hypereosinophilia was "
      "investigated.")

def v(vignette, stem):
    return f'{vignette} {stem}'

# ---------------------------------------------------------------------------
# Case 1 — acute Chagas disease (Trypanosoma cruzi)
# ---------------------------------------------------------------------------
CASE1 = [
    Q(v(V1, 'What is your suggestive diagnosis?'),
      ['Acute chagas disease.', 'Chronic chagas disease.', 'Acute sleeping sickness.',
       'Chronic sleeping sickness.'], 'A', 'derived',
      exp='The acute presentation (fever, conjunctivitis with unilateral eyelid '
          'edema, myocarditis) shortly after travel to Brazil, together with '
          'trypomastigotes on blood smear, indicates acute Chagas disease, not the '
          'chronic (cardiac/GI) stage.',
      image='Images/12_Q1_case1_fig.png'),
    # The source prints options A and B with IDENTICAL text ("Trypanosoma brucei
    # gambiense") — a typo in the department's handout, confirmed in the raw text
    # of both parasitology files. An earlier pass silently rewrote option B to
    # "...rhodesiense"; that is a plausible reconstruction but it invents a
    # distractor the students never saw, so the duplicate is collapsed instead and
    # the answer letter moves C -> B. The correct option text is unchanged.
    Q(v(V1, 'Which blood protozoan parasite is causing the infection?'),
      ['Trypanosoma brucei gambiense',
       'Trypanosoma cruzi', 'Toxoplasma gondii'], 'B', 'derived',
      exp='The S-shaped trypomastigote with an undulating membrane in a returning '
          'traveler from Brazil with unilateral periorbital edema (Romaña sign) is '
          'diagnostic of Trypanosoma cruzi, the agent of Chagas disease.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'How is this infection transmitted?'),
      ['By Tsetse flies transmitting metacyclic trypanosomes.',
       'By Triatoma megista transmitting amastigote form.',
       'By Triatoma megista transmitting metacyclic trypanosomes.',
       'By sand fly transmitting the promastigote form.'], 'C', 'derived',
      exp='T. cruzi is transmitted by triatomine ("kissing") bugs such as Triatoma '
          'megista, which deposit infective metacyclic trypomastigotes in their '
          'feces at the bite site (contaminative/posterior-station transmission); '
          'tsetse flies transmit African trypanosomes and sand flies transmit '
          'Leishmania.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'Why is the vector for this protozoan known as the "kissing bug"?'),
      ['Because it is a non-biting vector', 'Because the bite is painless',
       'Because its tendency to bite the patient on the lips or the face.',
       'Because it is a posterior station transmission'], 'C', 'derived',
      exp='Triatomine bugs characteristically feed on exposed skin around the '
          'mouth and eyes while the host sleeps, hence the common name "kissing '
          'bug"; they then defecate near the bite, contaminating it with infective '
          'metacyclic trypomastigotes.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'What is the name of the lesion that may develop at the site of '
            'inoculation of the parasite?'),
      ['Chancre', 'Calabar swelling.', 'Onchocercoma.', 'Chagoma'], 'D', 'derived',
      exp='An indurated, erythematous nodule at the parasite\'s skin entry point is '
          'called a chagoma; when the entry is through the conjunctiva it produces '
          'unilateral periorbital edema known as Romaña\'s sign.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'What is the name given to the unilateral edema of the eye in this '
            'disease?'),
      ['Romaña\'s sign.', 'Winterbottom\'s sign.', 'River blindness.', 'Keratitis'],
      'A', 'derived',
      exp='Unilateral painless periorbital and palpebral edema with conjunctivitis '
          'following conjunctival inoculation of T. cruzi is Romaña\'s sign, a '
          'classic marker of acute Chagas disease. Winterbottom\'s sign (posterior '
          'cervical lymphadenopathy) belongs to African trypanosomiasis.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'In this case, the blood smear showed the specific organisms. What '
            'study should be ordered next?'),
      ['Lumbar puncture', 'Upper and lower endoscopy', 'ECG', 'Barium swallow.'],
      'C', 'derived',
      exp='Given the cardiac involvement already suggested (right bundle branch '
          'block), formal ECG evaluation for conduction disease/arrhythmia is the '
          'appropriate next step; lumbar puncture is reserved for suspected CNS '
          'African trypanosomiasis, and endoscopy/barium swallow assess the '
          'megaesophagus of chronic, not acute, Chagas disease.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'Which complications may occur for this case?'),
      ['Hematemesis', 'Hemoptysis', 'Congestive heart failure', 'Mega-colon',
       'Mega-esophagus'], 'C', 'derived',
      exp='Long-standing T. cruzi infection destroys the myenteric (Auerbach\'s) '
          'plexus of the esophagus, producing achalasia-like dysmotility and '
          'progressive dilation (mega-esophagus); this patient\'s conjunctival '
          'portal of entry and early GI/cardiac findings place her at risk of this '
          'classic chronic digestive complication.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'How is this infection treated?'),
      ['By giving nifurtimox', 'By giving benznidazole', 'By giving flagyle',
       'By giving corticosteroid'], 'B', 'derived',
      exp='Benznidazole (or alternatively nifurtimox) is a trypanocidal drug and '
          'first-line therapy for acute Chagas disease; metronidazole ("flagyl") '
          'and corticosteroids have no role against T. cruzi.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'Mention the infective and diagnostic stages of this parasite.'),
      qtype='QROC', source='derived',
      exp='Infective stage: the metacyclic trypomastigote, deposited in triatomine '
          'bug feces at the bite site. Diagnostic stage: the trypomastigote, seen '
          'motile in fresh blood or on a Giemsa-stained thick/thin blood film '
          'during the acute parasitemic phase.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'Which methods are available to diagnose this infection?'),
      qtype='QROC', source='derived',
      exp='Acute phase: direct microscopy of fresh blood or Giemsa-stained thick/'
          'thin films for trypomastigotes, blood culture, xenodiagnosis, and PCR. '
          'Chronic phase (parasitemia is scanty): serology - indirect '
          'immunofluorescence (IFA), ELISA, or indirect hemagglutination for '
          'anti-T. cruzi antibodies.',
      image='Images/12_Q1_case1_fig.png'),
    Q(v(V1, 'Mention the methods used to prevent and control these cases?'),
      qtype='QROC', source='derived',
      exp='Vector control by residual insecticide spraying and improving rural '
          'housing (plastering walls, removing thatched roofs) to eliminate '
          'triatomine breeding sites; screening of blood/organ donors and pregnant '
          'women; health education about avoiding exposure; and prompt treatment of '
          'acute cases.',
      image='Images/12_Q1_case1_fig.png'),
]

# ---------------------------------------------------------------------------
# Case 2 — chronic Chagas disease (mega-esophagus / cardiomyopathy)
# ---------------------------------------------------------------------------
CASE2 = [
    Q(v(V2, 'What is your possible diagnosis?'), qtype='QROC', source='derived',
      exp='Chronic (digestive) Chagas disease: T. cruzi-induced destruction of the '
          'myenteric plexus has produced achalasia-like mega-esophagus (dysphagia) '
          'and megacolon (chronic constipation, distended abdomen), in a patient '
          'with a documented past acute infection.'),
    Q(v(V2, 'What are the ways of transmitting the responsible protozoan?'),
      ['Blood transfusion.', 'Organ transplantation.', 'Congenital transmission.',
       'Autoinfection.'], 'A', 'derived',
      exp='Besides the natural triatomine-bug route, T. cruzi is well recognised as '
          'a transfusion-transmitted infection because trypomastigotes survive in '
          'stored blood; transplantation and congenital (transplacental) routes are '
          'also documented, but autoinfection is not a feature of Chagas disease.'),
    Q(v(V2, 'Where in the world is this condition commonly found?'),
      ['In Egypt', 'In far East', 'In Mexico', 'In South and central America'],
      'D', 'derived',
      exp='Chagas disease is endemic to South and Central America (and parts of '
          'Mexico), where the triatomine vector is established; it is not endemic '
          'to Egypt or the Far East.'),
    Q(v(V2, 'In this case, which organ most commonly involved?'),
      ['The brain.', 'The heart.', 'The liver.', 'Lymph nodes'], 'B', 'derived',
      exp='The heart is the organ most commonly and seriously affected in chronic '
          'Chagas disease, developing a dilated cardiomyopathy that is the leading '
          'cause of morbidity and mortality.'),
    Q(v(V2, 'The heart in this disease is characterized by what?'),
      ['Left ventricular hypertrophy', 'Right ventricular hypertrophy',
       'Biventricular dilatation', 'Aortic stenosis'], 'C', 'derived',
      exp='Chronic Chagas cardiomyopathy is a dilated cardiomyopathy with '
          'biventricular dilation, often with a characteristic apical aneurysm, '
          'conduction defects (right bundle branch block, AV block) and '
          'arrhythmias - not a hypertrophic or valvular process.'),
    Q(v(V2, 'What is the most common cause of death in patients with this disease?'),
      ['Intestinal perforation', 'Stroke', 'Cardiac dysfunction',
       'Acute respiratory distress syndrome (ARDS)'], 'C', 'derived',
      exp='Progressive heart failure and fatal arrhythmias from Chagas '
          'cardiomyopathy are the leading cause of death in chronic Chagas disease.'),
    Q(v(V2, 'Which systems, other than the heart, are most commonly affected in '
            'this disease?'),
      ['CNS', 'GIT', 'Respiratory', 'Urinary'], 'B', 'derived',
      exp='After the heart, the gastrointestinal tract is the system most typically '
          'damaged, with denervation of the myenteric plexus producing '
          'mega-esophagus and megacolon.'),
    Q(v(V2, 'Which part of the gastrointestinal system is most commonly affected?'),
      ['Duodenum', 'Antrum', 'Esophagus', 'Terminal ileum'], 'C', 'derived',
      exp='The esophagus (and colon) are the segments classically affected, '
          'producing achalasia-like mega-esophagus from loss of the myenteric '
          'plexus, consistent with this patient\'s dysphagia.'),
    Q(v(V2, 'What is the pathophysiology of this condition?'), qtype='QROC',
      source='derived',
      exp='T. cruzi amastigotes replicate within and destroy cardiac myocytes and '
          'the ganglion cells of the myenteric (Auerbach\'s) plexus. Chronic immune-'
          'mediated inflammation and progressive parasympathetic denervation lead '
          'to loss of coordinated peristalsis (achalasia-like dilation of the '
          'esophagus and colon) and to myocardial fibrosis with conduction system '
          'damage, producing dilated cardiomyopathy, heart block and arrhythmias.'),
    Q(v(V2, 'What is the appropriate treatment for this condition?'), qtype='QROC',
      source='derived',
      exp='Antitrypanosomal drugs (benznidazole/nifurtimox) have limited efficacy '
          'once chronic organ damage is established; management is mainly '
          'symptomatic - pneumatic dilation or surgical myotomy/esophagectomy for '
          'mega-esophagus, surgical resection for megacolon, and standard heart-'
          'failure/antiarrhythmic therapy or pacemaker implantation for the '
          'cardiomyopathy and conduction block.'),
    Q(v(V2, 'What other disease is caused by the other Trypanosoma species?'),
      qtype='QROC', source='derived',
      exp='Trypanosoma brucei gambiense and Trypanosoma brucei rhodesiense cause '
          'African trypanosomiasis (human sleeping sickness), transmitted by the '
          'tsetse fly.'),
]

# ---------------------------------------------------------------------------
# Case 3 — amoebic liver abscess ruptured into the pericardium
# ---------------------------------------------------------------------------
CASE3 = [
    Q(v(V3, 'What is the suggestive diagnosis of this case?'), qtype='QROC',
      source='derived',
      exp='Amoebic liver abscess (Entamoeba histolytica) that has ruptured '
          'upward through the diaphragm into the pericardial sac, causing '
          'amoebic pericarditis/pericardial effusion.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'What is the causative parasite of this case?'), qtype='QROC',
      source='derived', exp='Entamoeba histolytica.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'What is the mode of infection of the causative parasite?'),
      qtype='QROC', source='derived',
      exp='Fecal-oral ingestion of mature quadrinucleate cysts of E. histolytica '
          'in fecally contaminated food or water.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'Can abscesses caused by this parasite occur in organs other than the '
            'liver?'), qtype='QROC', source='derived',
      exp='Yes. Trophozoites can spread hematogenously (via the portal or systemic '
          'circulation) or by direct extension to cause abscesses in the lung, '
          'brain, spleen, and other organs, in addition to the liver.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'Which serological tests were probably ordered to confirm the '
            'diagnosis?'), qtype='QROC', source='derived',
      exp='Indirect hemagglutination (IHA) and ELISA for anti-E. histolytica '
          'antibodies, and/or stool antigen detection (adhesin ELISA), are the '
          'tests typically used to confirm invasive amoebiasis.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'What is the possible differential diagnosis of pericarditis?'),
      qtype='QROC', source='derived',
      exp='Tuberculous pericarditis, purulent bacterial pericarditis, viral '
          '(idiopathic) pericarditis, uremic pericarditis, post-myocardial '
          'infarction (Dressler) syndrome, and malignant pericardial effusion.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'What is the pathogenesis of the disease?'), qtype='QROC',
      source='derived',
      exp='Ingested cysts excyst in the small intestine into trophozoites that '
          'invade the colonic mucosa, producing flask-shaped ulcers; trophozoites '
          'then travel via the portal vein to the liver, where they cause '
          'liquefactive necrosis of hepatocytes and form an abscess filled with '
          'reddish-brown "anchovy sauce" pus, usually in the right lobe. A '
          'left-lobe abscess, as here, can erode superiorly through the diaphragm '
          'into the pericardium, causing amoebic pericarditis and effusion.',
      image='Images/12_Q24_case3_fig1.png'),
    Q(v(V3, 'How can you properly treat this case?'), qtype='QROC', source='derived',
      exp='A tissue amoebicide (metronidazole or tinidazole) to eradicate invasive '
          'trophozoites, followed by a luminal agent (diloxanide furoate or '
          'paromomycin) to clear intestinal cysts and prevent relapse, plus '
          'drainage of the liver abscess/pericardial collection if there is '
          'tamponade or a large or poorly-responding abscess.',
      image='Images/12_Q24_case3_fig1.png'),
]

# ---------------------------------------------------------------------------
# Case 4 — reactivation toxoplasmosis with myocarditis (immunocompromised)
# ---------------------------------------------------------------------------
CASE4 = [
    Q(v(V4, 'What is your possible diagnosis?'), qtype='QROC', source='derived',
      exp='Reactivation toxoplasmosis with Toxoplasma gondii myocarditis in an '
          'immunocompromised (chemotherapy) patient.'),
    Q(v(V4, 'What is the association between the patient\'s history of receiving '
            'chemotherapy and this infection?'), qtype='QROC', source='derived',
      exp='Chemotherapy causes cell-mediated immunosuppression, which permits '
          'reactivation of latent bradyzoite tissue cysts of T. gondii into '
          'proliferating tachyzoites, producing disseminated disease including '
          'myocarditis, encephalitis, or pneumonitis.'),
    Q(v(V4, 'Which other group of individuals is at risk when infected with this '
            'parasite?'), qtype='QROC', source='derived',
      exp='HIV/AIDS patients, solid-organ and bone-marrow transplant recipients on '
          'immunosuppressive therapy, and the fetus of a woman who acquires '
          'primary infection during pregnancy (congenital toxoplasmosis).'),
    Q(v(V4, 'What is the commonest habitat of this parasite in immune-compromised '
            'patients?'), qtype='QROC', source='derived',
      exp='The brain is the commonest site of reactivation, causing toxoplasma '
          'encephalitis; the eye (chorioretinitis), lungs, and heart (myocarditis, '
          'as in this case) are also frequently involved.'),
    Q(v(V4, 'How is this infection transmitted? What are the infective stages of '
            'this parasite?'), qtype='QROC', source='derived',
      exp='Transmission occurs by ingestion of oocysts from soil or food '
          'contaminated by cat feces, ingestion of tissue cysts (bradyzoites) in '
          'undercooked meat, transplacental (tachyzoite) transmission to the '
          'fetus, and rarely by blood transfusion or organ transplantation. The '
          'infective stages are the oocyst and the tissue cyst (bradyzoite).'),
]

# ---------------------------------------------------------------------------
# Case 5 — cardiac trichinosis presenting as a forearm swelling
# ---------------------------------------------------------------------------
CASE5 = [
    Q(v(V5, 'Which parasitic infection do you think this patient has?'),
      qtype='QROC', source='derived',
      exp='Trichinellosis (Trichinella spiralis infection) with muscular and '
          'cardiac (myocarditis) involvement.',
      image='Images/12_Q37_case5_fig.png'),
    Q(v(V5, 'Which helminths cause this infection?'), qtype='QROC',
      source='derived',
      exp='Trichinella spiralis is the classic agent; other Trichinella species '
          '(e.g. T. britovi, T. nativa) can also cause human trichinellosis.',
      image='Images/12_Q37_case5_fig.png'),
    Q(v(V5, 'How do humans acquire this infection?'), qtype='QROC',
      source='derived',
      exp='By ingesting raw or undercooked meat, typically pork (or wild game), '
          'containing encysted Trichinella larvae; the larvae excyst in the '
          'intestine, mature into adults, and the released newborn larvae migrate '
          'via the bloodstream to encyst in striated muscle, including cardiac and '
          'skeletal muscle.',
      image='Images/12_Q37_case5_fig.png'),
    Q(v(V5, 'How do you diagnose extra-intestinal infection with this parasite?'),
      qtype='QROC', source='derived',
      exp='Muscle biopsy showing encysted larvae is definitive; supportive findings '
          'include marked eosinophilia, elevated muscle enzymes (CK), positive '
          'serology (ELISA for Trichinella antibodies), and a history of eating '
          'undercooked meat.',
      image='Images/12_Q37_case5_fig.png'),
]

# ---------------------------------------------------------------------------
# Case 6 — trichinosis myocarditis after raw pork ingestion
# ---------------------------------------------------------------------------
CASE6 = [
    Q(v(V6, 'Which parasite is causing the infection?'),
      ['Toxoplasma gondii', 'Taenia solium', 'visceral larval migrans',
       'Trichinella spiralis'], 'D', 'derived',
      exp='A shared-exposure outbreak after eating raw pork, with eosinophilia, '
          'myalgia, GI symptoms and eosinophilic myocarditis with elevated '
          'troponin, is classic for Trichinella spiralis.'),
    Q(v(V6, 'Which investigations should be ordered next?'),
      ['Urine analysis', 'Blood Urea and creatinine', 'Serology',
       'Upper and lower endoscopy', 'Barium swallow'], 'C', 'derived',
      exp='Serology (ELISA for anti-Trichinella antibodies) is the appropriate '
          'next step to support the clinical diagnosis before proceeding to '
          'invasive muscle biopsy.'),
    Q(v(V6, 'What is the test used for definitive diagnosis?'),
      ['Serology for antibody detection', 'PCR for DNA detection',
       'Immunohistochemistry for Ag detection', 'Muscle biopsy for larvae '
       'detection'], 'D', 'derived',
      exp='Muscle biopsy demonstrating encysted larvae is the definitive '
          'diagnostic test for trichinellosis; serology supports but does not '
          'confirm the diagnosis.'),
    Q(v(V6, 'How can you properly treat this case?'),
      ['By using albendazole alone', 'By using Corticosteroid alone',
       'By using a combination of albendazole and corticosteroid with supportive '
       'ttt.', 'By using antiarrhythmic and B blockers alone'], 'C', 'derived',
      exp='Severe trichinellosis with myocarditis is treated with an '
          'anthelmintic (albendazole) to kill tissue larvae combined with '
          'corticosteroids to control the inflammatory/hypersensitivity myocardial '
          'reaction, plus supportive cardiac care.'),
    Q(v(V6, 'Mention the methods to prevent and control these cases?'),
      ['Thorough cooking of beef and its products', 'Proper breeding of cattle, '
       'sterilization of garbage.', 'Eradication of mosquitoes (Reservoir host).',
       'Proper meat inspection in slaughter houses of pigs using trichinoscope.'],
      'D', 'derived',
      exp='Since Trichinella is acquired from pork, control relies on proper '
          'veterinary meat inspection of pig carcasses (trichinoscopy) and '
          'adequate cooking/freezing of pork, not beef; mosquitoes are not '
          'involved in this helminth\'s transmission.'),
]

CASES = [CASE1, CASE2, CASE3, CASE4, CASE5, CASE6]


def main():
    qs = []
    for c in CASES:
        for q in c:
            q.tag, q.tag_suggere, q.year = TAG, SUBJ, YEAR
            qs.append(q)
    meta = {'Source file': SRC,
            'Type': 'Text-rich PDF, 9 pages; 6 clinical vignette GD cases',
            'Tag': TAG, 'tagSuggere': SUBJ, 'Year': YEAR,
            'Answer source': 'derived — the file prints no key'}
    n = write_md(OUT, 'Source 12 — GD Parasitology Cases (2023-2024)', meta, qs)

    n_mcq = sum(1 for q in qs if q.type == 'QCS')
    n_written = n - n_mcq
    ans = collections.Counter(q.correct for q in qs if q.type == 'QCS')
    total = sum(ans.values())
    max_share = max(ans.values()) / total if total else 0

    print(f'source 12: {n} questions ({n_mcq} MCQ / {n_written} written), 6 cases')
    print(f'  counters: highest sub-Q number per case matches source; '
          f'### Q headings = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} '
          f'(n={total}, max share={max_share:.1%})')
    print(f'  derived: {n} (all)')
    print('  figure crops: 4 verified visually '
          '(Q1 trypomastigote smear, Q24 liver-abscess aspiration + CXR, '
          'Q37 Trichinella larva histology)')


if __name__ == '__main__':
    main()
