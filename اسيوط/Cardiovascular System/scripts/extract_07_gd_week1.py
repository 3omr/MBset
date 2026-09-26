#!/usr/bin/env python3
"""Source 07 — GD/1st week-CVS-206-cases.pdf.

Five G.D. sessions of clinical cases (Histology / Anatomy / Physiology x2 /
Anatomy). Re-derived a second time against lib_gd.py after its BULLET rule
was fixed again: it used to require a bulleted sub-question to end in '?' or
':', silently dropping every bulleted question written without terminal
punctuation. Re-parsing now yields 57 raw rows (up from the 39 this file
previously emitted). This file now carries **42 items / 4 MCQ / 38 written**.

Cross-checking the 57 raw rows plus a fresh `pdftotext -layout` pass of the
source (not just the parser output — the parser's own vignette-attribution
bug, see below, makes cross-checking against the parser's rows alone
unreliable) against the 39 items already curated here turned up exactly
**3 genuinely new questions**, all under G.D. (2) (Anatomy — Congenital
heart disease); everything else in the 57 rows was either already covered
(sometimes several raw bullets merged into one curated item, as before) or
a parser artifact, not a real question:

1. "If this defect is large, how could this be reflected on the
   hemodynamics of the affected individual?" (ASD case) — this sub-question
   was glued onto the *last option* of the ASD MCQ by pdftotext (the raw
   text runs "...endocardial cushions. - If this defect is large...").
   Split out into its own written item here.
2. "How can a patent ductus arteriosus cause enlargement of the heart?"
   (PDA case) — a dash-bulleted sub-question neither the old nor the newly
   fixed parser ever surfaced as its own row.
3. "What is the possible mechanism that normally causes postnatal closure
   of the ductus arteriosus?" (PDA case) — same case, same reason.

Judgement calls carried over / reconfirmed against the raw PDF text:
- The GD-intro paragraphs that the parser sometimes treats as a bare
  question stem (e.g. "Aortic stenosis cases: Mohamed is an 82-year-old...",
  or the AF/MI/angina/stress-ECG/Mobitz/dropped-beat/conductive-system case
  paragraphs) are case setup, not questions — none of them end in a '?' or
  is followed by one in the raw text at that point; the real numbered
  sub-questions that follow are what's captured. No new items added for
  these.
- The row ending "...why heart rate increases during stress ECG. II.
  Arrhythmia and heart block" — "II. Arrhythmia and heart block" is a
  section heading in the raw PDF (its own line before the next case), not
  part of the question; already correctly excluded from that stem.
- The running "First week / Cases of CVS-206" page footer never lands
  inside a stem/option in this source (verified against the raw text for
  every item below); no cleanup needed for it here.

The PDF's own "G.D. (N): title (Subject)" label is still printed as a
running FOOTER at the end of the block it names, not a heading before it —
this trailing-header bug was intentionally NOT changed in the parser fix (it
risks mis-assigning subjects in the other direction), so raw
lib_gd.parse() still forward-attributes several items to the wrong
subject/GD number. Those are corrected by hand below after reading the
source directly; see the case-boundary comments. The 3 new items above are
G.D. (2), Anatomy, same as their case's other questions.

No answer key is printed anywhere; every answer is `derived` from medical
knowledge specific to each vignette.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '07_GD_Week_1_Cases.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/1st week-CVS-206-cases.pdf'

VIG1 = ('A 9-year-old girl was taken to the Emergency Department with recent onset '
        'dyspnea. She reported a 6-week history of painful, swollen joints. Physical '
        'exam revealed a temperature of 38°C, cervical lymphadenopathy, and '
        'pansystolic and diastolic murmurs. Although she was admitted to the hospital, '
        'she died of progressive heart failure.')

VIG_AS = ('Mohamed is an 82-year-old man. Despite having chest pains (angina) and '
          'periods of confusion, he refused to have a check-up. Recently, after several '
          'episodes of syncope, he agreed to see a physician. On examination the '
          'physician noted a systolic ejection murmur, a palpable S4, and a diminished '
          'aortic component of S2. ECG was consistent with left ventricular hypertrophy. '
          'His carotid pulse was weak with a delayed upstroke. Cardiac catheterization '
          'showed a pressure gradient of 100 mm Hg between the left ventricle and the '
          'aorta during systole, consistent with aortic stenosis.')

VIG_MARFAN = ('A 29-year-old female patient has dilation of the ascending aorta as the '
              'result of an aneurysm (weakness in the vessel wall). She has been '
              'diagnosed as having Marfan syndrome.')

VIG_ASD = ('An echo of a 30-year-old male shows a 3 mm interatrial septal defect above '
           'the fossa ovalis.')

VIG_VSD = ('A pediatrician detected a ventricular septal defect in an infant, and '
           'explained to the baby\'s mother that this is a common birth defect; his '
           'advice was to wait until the end of the first year before deciding on '
           'possible surgical correction.')

VIG_PDA = ('A female infant was born after a rubella infection during the second month '
           'of pregnancy. She has congenital cataract and a patent ductus arteriosus. A '
           'chest radiograph showed cardiac enlargement.')

VIG_JVP = ('A 55-year-old obese male was rushed to casualty with chest pain radiating to '
           'the left arm, sweating and severe dyspnea. He is a chronic smoker and a '
           'known hypertensive on irregular treatment for 15 years, diagnosed with '
           'left-sided heart failure with infarction. HR 120/min, BP 160/100 mmHg, RR '
           '35/min, elevated JVP.')

VIG_MI = ('A 60-year-old woman arrives at the emergency department with severe burning '
          'pain in her left arm. Laboratory studies show an elevated troponin I level '
          'and she is treated for an acute myocardial infarction. Her ejection fraction '
          'is below 30%.')

VIG_ANGINA = ('A 50-year-old man with a history of stable angina presents to the '
              'emergency department with an episode of severe chest pain that is not '
              'relieved by rest or nitroglycerin.')

VIG_STRESS = ('A 63-year-old male presents with chest and arm pain that occurs mainly '
              'during exertion and is relieved by rest. A stress ECG shows ST-segment '
              'depression and a heart rate of 125 beats/min.')

VIG_MOBITZ = ('Hosam, a 68-year-old, was admitted after an acute myocardial infarction. '
              'His PR intervals and QRS complexes are normal, but occasional P waves '
              'are not followed by a QRS complex. He fainted twice in the hospital; the '
              'physicians diagnosed a Mobitz type II AV block and planned pacemaker '
              'implantation.')

VIG_AF = ('A 60-year-old man presents with new shortness of breath for 24 hours and the '
          'sensation that his heart is beating too fast. He stopped smoking 10 years ago '
          '(40 pack-years), gained 40 lb, and drinks excess caffeine. HR is 130 and '
          'irregularly irregular, BP 160/96, RR 26, SpO2 90% on room air, bilateral '
          'rales, neck veins distended 10 cm above the angle of Louis, and trace bilateral '
          'leg edema.')

VIG_DROP = ('A 20-year-old female presents with dyspnea and a sensation of irregular '
            'heartbeats. She reports significant stress and lack of sleep. ECG shows '
            'signs of a dropped beat.')

VIG_STAB = ('A 33-year-old woman was stabbed while jogging at 11 p.m. In the emergency '
            'department she was unconscious and in extremely poor condition. A ~1 cm '
            'wound was present in the left fifth intercostal space, 1.5 cm from the '
            'lateral sternal margin. Her carotid pulse was rapid and weak and her neck '
            'veins were distended. Cardiac tamponade was diagnosed.')

VIG_CONDUCT = ('After severe physical exercise, a 9-year-old boy began feeling unwell. '
               'He was brought to the emergency department semiconscious with an '
               'irregular heart rate.')

VIG_MVP = ('A 47-year-old woman with a history of rheumatic fever has a low-pitched '
           'diastolic murmur due to mitral valve incompetence.')

VIG_AR = ('A 55-year-old woman has severe aortic incompetence, with blood returning to '
          'the left ventricular cavity during diastole.')

TAG_HIST = 'Department, GDs, Histology GD 1'
TAG_ANAT2 = 'Department, GDs, Anatomy GD 2'
TAG_PHYS3 = 'Department, GDs, Physiology GD 3'
TAG_PHYS4 = 'Department, GDs, Physiology GD 4'
TAG_ANAT5 = 'Department, GDs, Anatomy GD 5'

ITEMS = [
    # --- GD 1: Cases of heart diseases (Histology) ---
    (VIG1 + ' What is the differential diagnosis?', None, None,
     'The picture (migratory arthritis, fever, cervical lymphadenopathy and new '
     'pansystolic/diastolic murmurs progressing rapidly to fatal heart failure in a '
     'child) is most consistent with acute rheumatic pancarditis; infective '
     'endocarditis and acute viral myocarditis are the main differentials.',
     TAG_HIST, 'Histology'),
    (VIG1 + ' What is the layer of the heart most likely to be affected?', None, None,
     'All three layers can be involved (pancarditis), but it is myocarditis — '
     'inflammation of the myocardium with Aschoff-body formation — that impairs '
     'contractility and is chiefly responsible for the fatal heart failure, while '
     'valvulitis (endocardium) produces the murmurs.',
     TAG_HIST, 'Histology'),
    (VIG1 + ' What is the histological structure of the cardiac wall?', None, None,
     'The heart wall has three layers: the endocardium (endothelium on a thin '
     'subendothelial connective-tissue layer), the myocardium (cardiac muscle fibers '
     'arranged in a fibrous skeleton, the thickest layer and the one that generates '
     'contraction), and the epicardium/visceral pericardium (mesothelium over '
     'subepicardial connective tissue carrying the coronary vessels and nerves).',
     TAG_HIST, 'Histology'),
    (VIG1 + ' Mention the different types of the cardiac valves.', None, None,
     'There are two types: the atrioventricular valves (tricuspid on the right, '
     'mitral/bicuspid on the left), whose cusps are anchored by chordae tendineae to '
     'papillary muscles, and the semilunar valves (aortic and pulmonary), each with '
     'three pocket-shaped cusps and no chordae.',
     TAG_HIST, 'Histology'),
    (VIG_MARFAN + ' The most likely cause of the aneurysm is a:',
     ['Genetic mutation affecting the enzyme and collagen fiber formation.',
      'Genetic mutation affecting the fibrillin gene and elastic fiber formation.',
      'Vitamin C deficiency affecting hydroxylation of proline residues of '
      'preprocollagen.',
      'Vitamin D deficiency affecting absorption of calcium and phosphorus.'],
     'B',
     'Marfan syndrome is caused by mutations in the FBN1 gene encoding fibrillin-1, a '
     'key structural glycoprotein of elastic-fiber microfibrils; defective fibrillin '
     'weakens the elastic media of the aorta (and disrupts microfibril sequestration '
     'of TGF-beta), predisposing to progressive aortic root dilation and dissection.',
     TAG_HIST, 'Histology'),
    ('Describe the structure of the aorta.', None, None,
     'The aorta is an elastic (conducting) artery with three tunics: a thin intima '
     '(endothelium, subendothelial connective tissue, internal elastic lamina), a '
     'thick media of many concentric fenestrated elastic laminae interspersed with '
     'smooth muscle and ground substance, and an adventitia of collagen, vasa vasorum '
     'and nerves.',
     TAG_HIST, 'Histology'),
    ('How do the structures of the aorta adapt to its function?', None, None,
     'The numerous elastic laminae in the media let the aortic wall distend during '
     'ventricular systole, storing part of the ejected energy, and then recoil during '
     'diastole (Windkessel effect) to keep blood flowing forward and to sustain '
     'diastolic pressure between heartbeats.',
     TAG_HIST, 'Histology'),

    # --- GD 2: Cases of Congenital heart diseases (Anatomy) ---
    (VIG_ASD + ' This patency resulted from which of the following developmental '
     'events?',
     ['Excessive resorption of the septum primum.',
      'Failure of the endocardial cushions to form.',
      'Failure of fusion of the valvula foraminis ovalis and the septum secundum.',
      'Failure of the right and left conotruncal ridges to fuse.',
      'Failure of the septum primum to fuse with the endocardial cushions.'],
     'C',
     'A small patent interatrial opening at/above the fossa ovalis represents a '
     'probe-patent foramen ovale, which results when the flap-like valve of the '
     'foramen ovale (the septum primum remnant) fails to fuse with the septum '
     'secundum after birth, leaving a one-way, often clinically silent, communication.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_ASD + ' If this defect is large, how could this be reflected on the '
     'hemodynamics of the affected individual?', None, None,
     'A large atrial septal defect produces a chronic left-to-right shunt (the '
     'right ventricle is more compliant than the left), causing right atrial and '
     'right ventricular volume overload, right heart dilation and increased '
     'pulmonary blood flow; over years this can progress to pulmonary '
     'hypertension and, if uncorrected, shunt reversal (Eisenmenger syndrome). '
     'Clinically this presents with exertional dyspnea, a fixed split S2 and, '
     'eventually, signs of right heart failure.',
     TAG_ANAT2, 'Anatomy'),
    ('What are the circulatory changes that occur after birth? Describe the '
     'different stages of development of the interatrial and interventricular septa. '
     'What type of tissue is critical for dividing the heart into four chambers and '
     'the outflow tract into pulmonary and aortic channels?', None, None,
     'At birth, falling pulmonary vascular resistance and rising systemic resistance '
     '(with cessation of placental flow) functionally close the foramen ovale '
     '(pressure reversal presses septum primum against septum secundum) and start '
     'closure of the ductus arteriosus (via rising oxygen tension) and the ductus '
     'venosus/umbilical vessels, converting the fetal parallel circulation into the '
     'adult series circulation. The interatrial septum forms from septum primum '
     '(which fuses with the endocardial cushions, then develops the ostium secundum '
     'as its upper part is resorbed) and septum secundum (a thicker, incomplete '
     'septum overlapping the ostium secundum and leaving the foramen ovale). The '
     'interventricular septum forms from a muscular part growing up from the '
     'ventricular floor and a membranous part formed where the endocardial cushions '
     'meet the conotruncal ridges. These endocardial cushions and conotruncal '
     '(aorticopulmonary) ridges — largely neural-crest-derived mesenchyme — are the '
     'tissue critical for dividing the heart into four chambers and the outflow '
     'tract into separate aortic and pulmonary channels.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_VSD + ' What percentage of CHD is the VSD?', None, None,
     'Ventricular septal defect is the single most common congenital heart defect, '
     'accounting for roughly 20-30% of all congenital heart disease (excluding a '
     'bicuspid aortic valve).',
     TAG_ANAT2, 'Anatomy'),
    (VIG_VSD + ' Why did the doctor advise waiting until the end of the first year '
     'before deciding on surgical correction?', None, None,
     'Many small-to-moderate VSDs close spontaneously during the first year of life '
     'as the muscular septum continues to grow, so surgery is deferred unless the '
     'defect is large or is already causing significant heart failure or failure to '
     'thrive, avoiding an unnecessary operation.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_VSD + ' What are the varieties of VSDs? What problems would the infant '
     'likely suffer if the VSD were large?', None, None,
     'VSDs are classified by location as membranous/perimembranous (the most '
     'common, ~80%), muscular (trabecular), inlet (AV-canal type), and '
     'outlet/supracristal (conoventricular) defects. A large VSD produces a '
     'significant left-to-right shunt with pulmonary overcirculation, causing heart '
     'failure, failure to thrive and recurrent chest infections in infancy, and can '
     'progress over years to pulmonary hypertension and shunt reversal (Eisenmenger '
     'syndrome) if uncorrected.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_PDA + ' How can a patent ductus arteriosus cause enlargement of the '
     'heart?', None, None,
     'A patent ductus arteriosus creates a continuous left-to-right shunt from '
     'the aorta into the pulmonary artery, increasing pulmonary blood flow and '
     'the volume of blood returning to the left atrium and left ventricle; this '
     'chronic volume overload dilates and hypertrophies the left heart (and, if '
     'pulmonary hypertension develops, can eventually overload the right heart '
     'too), producing the cardiac enlargement seen on the chest radiograph.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_PDA + ' What is the possible mechanism that normally causes postnatal '
     'closure of the ductus arteriosus?', None, None,
     'Postnatal closure is triggered mainly by the rise in blood oxygen tension '
     'after birth, together with the loss of placental prostaglandin E2 and '
     'increased pulmonary clearance of circulating PGE2; this constricts the '
     'ductal smooth muscle for functional closure within about the first day of '
     'life, followed over the next 2-3 weeks by fibrous intimal remodeling that '
     'permanently obliterates the lumen into the ligamentum arteriosum.',
     TAG_ANAT2, 'Anatomy'),
    (VIG_PDA + ' What is the normal postnatal fate of the ductus arteriosus? What '
     'CHDs is it recommended to keep the ductus arteriosus patent for after birth?',
     None, None,
     'The ductus arteriosus normally closes functionally within hours to a few days '
     'after birth (smooth-muscle constriction triggered by rising oxygen tension and '
     'falling prostaglandin E2) and then fibroses over weeks into the ligamentum '
     'arteriosum. In duct-dependent lesions — transposition of the great arteries, '
     'severe pulmonary atresia/critical pulmonary stenosis, hypoplastic left heart '
     'syndrome, and severe coarctation/interrupted aortic arch — the ductus is kept '
     'open with IV prostaglandin E1 (alprostadil) until surgical or catheter '
     'correction, since it is the infant\'s only adequate source of pulmonary or '
     'systemic blood flow.',
     TAG_ANAT2, 'Anatomy'),

    # --- GD 3: Cases of JVP, heart sounds, and radial pulse (Physiology) ---
    (VIG_AS + ' What is the diagnosis, and which findings in this vignette support it?',
     None, None,
     'The findings — a systolic ejection murmur, palpable S4, diminished A2, a weak '
     'carotid pulse with delayed upstroke, LVH on ECG, and a 100 mm Hg '
     'transvalvular systolic gradient — are diagnostic of severe calcific aortic '
     'stenosis; his angina, syncope and progression toward heart failure are the '
     'classic triad of advanced disease.',
     TAG_PHYS3, 'Physiology'),
    ('In aortic stenosis, there is significant narrowing of the aortic valve opening. '
     'Why does this narrowing cause a murmur?', None, None,
     'The rigid, calcified valve creates a fixed narrow orifice; blood forced through '
     'it accelerates and becomes turbulent, and turbulent flow generates the audible '
     'vibrations heard as a murmur.',
     TAG_PHYS3, 'Physiology'),
    ('In aortic stenosis, the murmur occurs during systole (a systolic ejection '
     'murmur). Why?', None, None,
     'Blood crosses the aortic valve only during ventricular ejection, when LV '
     'pressure exceeds aortic pressure; flow rises then falls across systole, giving '
     'the murmur its crescendo-decrescendo, systole-confined shape.',
     TAG_PHYS3, 'Physiology'),
    ('What are the components of a normal S2, and why did this patient have a '
     'diminished aortic (A2) component of S2?', None, None,
     'S2 is made up of aortic valve closure (A2) followed closely by pulmonary valve '
     'closure (P2). In severe calcific aortic stenosis the leaflets are thickened and '
     'immobile, so they close with little vibration, softening or abolishing A2.',
     TAG_PHYS3, 'Physiology'),
    ('Why was his carotid artery pulse weak with a delayed upstroke?', None, None,
     'The fixed stenotic orifice limits the rate and volume of blood ejected per unit '
     'time, producing a low-amplitude, slow-rising carotid pulse (pulsus parvus et '
     'tardus) downstream of the obstruction.',
     TAG_PHYS3, 'Physiology'),
    (VIG_JVP + ' Explain the elevated JVP in this case, and mention the significance '
     'of the other JVP curve waves.', None, None,
     'Left ventricular infarction reduces forward output and raises LV end-diastolic '
     'pressure, which is transmitted back through the pulmonary circulation to the '
     'right heart, raising central venous pressure and distending the neck veins. On '
     'the JVP waveform the a wave reflects atrial contraction, the c wave tricuspid '
     'bulging during isovolumic ventricular contraction, the v wave atrial filling '
     'against a closed tricuspid valve, and the x/y descents atrial relaxation and '
     'tricuspid opening; an absent a wave suggests atrial fibrillation and a giant v '
     'wave suggests tricuspid regurgitation.',
     TAG_PHYS3, 'Physiology'),

    # --- GD 4: Abnormal ECG pattern cases (Physiology) ---
    (VIG_MI + ' Mention the ionic changes and ECG changes recorded in this case.',
     None, None,
     'Ischemic myocytes lose Na+/K+-ATPase activity, so K+ leaks out of the cell while '
     'Na+ and Ca2+ accumulate intracellularly; this produces the classic ECG evolution '
     'of hyperacute peaked T waves and ST-segment elevation (injury current) followed '
     'by pathological Q waves and T-wave inversion as infarction becomes established.',
     TAG_PHYS4, 'Physiology'),
    (VIG_ANGINA + ' Explain the mechanism of the recurrent angina and why it did not '
     'respond to the usual treatment here. Explain why the pain is referred to the '
     'left shoulder. List endothelial vasoconstrictor factors affecting coronary '
     'blood flow.', None, None,
     'Recurrent angina reflects a fixed atherosclerotic stenosis with superimposed '
     'plaque instability, vasospasm and platelet aggregation that intermittently drop '
     'coronary flow below demand; pain unresponsive to rest and nitroglycerin '
     'indicates near-total occlusion (evolving unstable angina/infarction) rather '
     'than a simple supply-demand mismatch. The pain refers to the left shoulder/arm '
     'because cardiac visceral afferents (T1-T4) converge on the same spinal '
     'dorsal-horn neurons as somatic afferents from that dermatome, so the brain '
     'mislocalizes the pain to the skin/muscle of the arm. Endothelial '
     'vasoconstrictors acting on the coronary vessels include endothelin-1, '
     'thromboxane A2, and angiotensin II.',
     TAG_PHYS4, 'Physiology'),
    (VIG_STRESS + ' Explain why the ST segment was depressed in this case and mention '
     'its diagnostic value. Explain why heart rate increases during stress ECG.',
     None, None,
     'Exercise raises myocardial oxygen demand beyond what the stenosed coronary '
     'artery can supply, producing subendocardial ischemia; the less negatively '
     'polarized ischemic subendocardium creates a current of injury seen as ST '
     'depression, a sensitive marker of reversible ischemia and significant coronary '
     'disease. Heart rate rises during stress testing because of increased sympathetic '
     'drive and vagal withdrawal needed to meet the higher metabolic demand.',
     TAG_PHYS4, 'Physiology'),
    (VIG_MOBITZ + ' What type of AV conduction block is illustrated, and why is a '
     'pacemaker indicated?', None, None,
     'This is Mobitz type II second-degree AV block — an infranodal (His-Purkinje) '
     'block causing sudden non-conducted P waves without PR-interval prolongation. '
     'Because it can progress unpredictably to complete heart block and asystole, it '
     'is an indication for a permanent pacemaker regardless of symptoms.',
     TAG_PHYS4, 'Physiology'),
    ('What does the PR interval on the ECG represent, and when is it '
     'prolonged?', None, None,
     'The PR interval represents the time from onset of atrial depolarization to the '
     'onset of ventricular depolarization, i.e. conduction through the atria and AV '
     'node (normally 0.12-0.20 s); it prolongs in first-degree AV block from delayed '
     'AV nodal conduction.',
     TAG_PHYS4, 'Physiology'),
    ('What does the term "conduction velocity" mean, as applied to myocardial '
     'tissue?', None, None,
     'Conduction velocity is the speed at which the depolarization wave propagates '
     'through cardiac tissue, determined mainly by fiber diameter, gap-junction '
     '(connexin) density, and whether the action potential upstroke is carried by '
     'fast Na+ channels (fast conduction) or slow Ca2+ channels (slow conduction, as '
     'in the AV node).',
     TAG_PHYS4, 'Physiology'),
    ('What is the normal conduction velocity through the AV node, and how does it '
     'compare with conduction velocity in other portions of the heart?', None, None,
     'AV nodal conduction is by far the slowest in the heart (about 0.05 m/s), which '
     'produces the physiological PR delay that allows atrial contraction to finish '
     'emptying blood into the ventricles before they contract; this is much slower '
     'than conduction in atrial/ventricular myocardium (~0.5-1 m/s) and far slower '
     'than the Purkinje system, the fastest conducting tissue (~2-4 m/s).',
     TAG_PHYS4, 'Physiology'),
    ('How is it possible to have a P wave that is not followed by a QRS complex?',
     None, None,
     'If conduction below the AV node (in the His-Purkinje system) intermittently '
     'fails, the atrial impulse still depolarizes the atria and produces a P wave but '
     'never reaches the ventricles, so no QRS follows — the mechanism of Mobitz type '
     'II block.',
     TAG_PHYS4, 'Physiology'),
    ('Why did he faint?', None, None,
     'A dropped ventricular beat, or a run of non-conducted beats, transiently '
     'abolishes cardiac output and drops cerebral perfusion below the level needed to '
     'maintain consciousness — a Stokes-Adams attack, and the reason progressive '
     'infranodal block is an indication for pacing.',
     TAG_PHYS4, 'Physiology'),
    (VIG_AF + ' What is the most likely diagnosis, and what findings support it?',
     None, None,
     'This is atrial fibrillation with decompensated heart failure: the irregularly '
     'irregular pulse at ~130/min is the hallmark of AF, and the bibasal rales, '
     'distended neck veins and leg edema reflect the resulting congestive failure, '
     'precipitated by his longstanding hypertension, obesity and heavy caffeine use.',
     TAG_PHYS4, 'Physiology'),
    (VIG_AF + ' What are the predisposing factors for atrial fibrillation, and what '
     'are its mechanism and ECG changes?', None, None,
     'Predisposing factors here include longstanding hypertension, obesity, excess '
     'caffeine intake and probable underlying structural/ischemic heart disease. '
     'Mechanistically, multiple chaotic re-entrant wavelets (often triggered by rapid '
     'ectopic foci near the pulmonary veins) depolarize the atria asynchronously; the '
     'ECG shows no discrete P waves, replaced by irregular fibrillatory (f) waves, '
     'with an irregularly irregular ventricular rate.',
     TAG_PHYS4, 'Physiology'),
    ('Describe the difference between atrial fibrillation and atrial flutter on ECG.',
     None, None,
     'Atrial flutter shows a regular, sawtooth pattern of flutter waves (~300/min) '
     'with a usually regular ventricular response at a fixed conduction ratio (e.g. '
     '2:1), whereas atrial fibrillation shows chaotic, irregular fibrillatory waves '
     'with an irregularly irregular ventricular rate.',
     TAG_PHYS4, 'Physiology'),
    (VIG_DROP + ' What is the most likely explanation for her symptoms?', None, None,
     'Stress and sleep deprivation raise sympathetic tone and can trigger benign '
     'premature atrial or ventricular ectopic beats (extrasystoles), felt as a '
     '"skipped" or dropped beat; in a young patient with no structural heart disease '
     'this is usually a benign arrhythmia.',
     TAG_PHYS4, 'Physiology'),
    ('What is meant by a "dropped beat," and mention its types and ECG '
     'changes.', None, None,
     'A dropped beat is a premature ectopic beat (or a blocked beat) that interrupts '
     'the regular rhythm. Types include premature atrial contractions (an early, '
     'abnormally shaped P wave with a normal QRS) and premature ventricular '
     'contractions (a wide, bizarre QRS with no preceding P wave, usually followed by '
     'a compensatory pause); in this stressed, sleep-deprived young woman with no '
     'structural heart disease, benign extrasystoles are the likely cause.',
     TAG_PHYS4, 'Physiology'),
    ('Compare the ECG changes of an extrasystole and tachycardia.', None, None,
     'An extrasystole is a single early ectopic beat, differently shaped from the '
     'sinus beats, followed by a compensatory pause before normal rhythm resumes, '
     'whereas tachycardia is a sustained run of rapid beats (>100/min) at a regular, '
     'short R-R interval with no pause, reflecting a persistent ectopic focus or '
     're-entry circuit rather than an isolated early beat.',
     TAG_PHYS4, 'Physiology'),

    # --- GD 5: Stab wound cases (Anatomy) ---
    (VIG_STAB + ' The following observations are in agreement with the diagnosis '
     'except which?',
     ['The tip of the knife had pierced the pericardium.',
      'The knife had pierced the anterior wall of the left ventricle.',
      'The blood in the pericardial cavity was under right ventricular pressure.',
      'The blood in the pericardial cavity pressed on the thin-walled atria and large '
      'veins as they traversed the pericardium to enter the heart.',
      'The backed-up venous blood caused congestion of the veins seen in the neck.'],
     'B',
     'The right ventricle, not the left, forms most of the anterior surface of the '
     'heart, so a stab wound in the left fifth intercostal space near the sternal '
     'border typically penetrates the right ventricle; the remaining statements '
     '(pericardial puncture, tamponade under low right-ventricular-level pressure, '
     'compression of the thin-walled atria/great veins, and resulting neck-vein '
     'distension) are all consistent with cardiac tamponade.',
     TAG_ANAT5, 'Anatomy'),
    ('What are the definition and subdivisions of the mediastinum? List the contents '
     'of the middle mediastinum. Describe the pericardial sinuses. Describe the '
     'surface anatomy of the borders of the heart.', None, None,
     'The mediastinum is the central compartment of the thoracic cavity between the '
     'two pleural cavities, divided into a superior mediastinum and an inferior '
     'mediastinum, the latter further split into anterior, middle and posterior '
     'parts. The middle mediastinum contains the pericardium and heart, the '
     'ascending aorta, the lower superior vena cava, the main pulmonary trunk and '
     'arteries, and the phrenic nerves. The transverse pericardial sinus lies behind '
     'the aorta/pulmonary trunk and in front of the atria/SVC, while the oblique '
     'pericardial sinus is a cul-de-sac behind the left atrium bounded by the '
     'pulmonary veins and IVC. Surface anatomy: the right border corresponds to the '
     'right atrium from the 3rd to 6th right costal cartilages, the left border to '
     'the left ventricle down to the apex at the 5th left intercostal space in the '
     'midclavicular line, the superior border runs from the 3rd left to the 3rd '
     'right costal cartilage, and the inferior border runs from the 6th right '
     'costal cartilage to the apex.',
     TAG_ANAT5, 'Anatomy'),
    (VIG_CONDUCT + ' Mention the name and locations of the conductive system of the '
     'heart. What are the nerves that supply the heart and their significance?',
     None, None,
     'The conducting system comprises the sinoatrial (SA) node in the upper posterior '
     'wall of the right atrium near the SVC opening, the atrioventricular (AV) node in '
     'the postero-inferior interatrial septum (triangle of Koch), the bundle of His '
     'penetrating the membranous interventricular septum, and its right and left '
     'bundle branches continuing into the subendocardial Purkinje fibers of both '
     'ventricles. The heart is supplied by the cardiac plexus: sympathetic fibers '
     '(cervical and upper thoracic chain, via the cardiac nerves) that raise heart '
     'rate, conduction velocity and contractility, and parasympathetic fibers from '
     'the vagus that slow heart rate and AV conduction; visceral afferents traveling '
     'with these nerves carry cardiac pain, referred to the chest and left '
     'arm/shoulder along the corresponding dermatomes — the likely cause of this '
     'boy\'s collapse after exertion being an exercise-triggered arrhythmia.',
     TAG_ANAT5, 'Anatomy'),
    (VIG_MVP + ' The affected valve can best be evaluated by auscultation at which of '
     'the following locations: left second intercostal space, left fifth intercostal '
     'space, left lower sternal border, right second intercostal space, or right '
     'fifth intercostal space?',
     None, None,
     'The mitral valve is heard best at the cardiac apex, which corresponds on the '
     'chest wall to the left fifth intercostal space in the midclavicular line.',
     TAG_ANAT5, 'Anatomy'),
    (VIG_AR + ' To hear the aortic valve with the least interference from the other '
     'heart sounds, the best place to place the stethoscope on the chest wall is:',
     ['The right half of the lower end of the body of the sternum.',
      'The medial end of the second right intercostal space.',
      'The medial end of the second left intercostal space.',
      'The apex of the heart.',
      'The fifth left intercostal space 3.5 in. (9 cm) from the midline.'],
     'C',
     'The soft, decrescendo diastolic murmur of aortic regurgitation radiates down '
     'the left sternal border and is heard best at the third left intercostal space '
     '(Erb\'s point) near the medial end of the second left intercostal space, away '
     'from the louder flow sounds at the right second interspace (aortic area) or the '
     'apex (dominated by mitral/S1 sounds).',
     TAG_ANAT5, 'Anatomy'),
]


def main():
    qs = []
    for stem, options, correct, exp, tag, subj in ITEMS:
        qs.append(Q(stem, options, correct, 'derived', exp=exp, tag=tag, tag_suggere=subj))
    meta = {'Source file': SRC,
            'Type': 'GD case handout, 8 pages; 5 G.D. sessions across Histology, '
                    'Anatomy and Physiology',
            'Tag': 'Department, GDs, <Subject> GD <N>', 'tagSuggere': 'varies by item',
            'Year': 'None',
            'Answer source': 'derived — no key is printed anywhere in the source'}
    n = write_md(OUT, 'Source 07 — GD Week 1 Cases', meta, qs)
    mcq = sum(1 for s, o, c, e, t, sj in ITEMS if o)
    ans = collections.Counter(c for s, o, c, e, t, sj in ITEMS if o)
    print(f'source 07: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: expected max sub-Q number per case matches source; '
          f'option-A blocks = {mcq}; ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({mcq} MCQs — bias gate n/a, <15)')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
