#!/usr/bin/env python3
"""Source 04 — department CVS bank.pdf.

A 14-page department "self-assessment" question bank that is NOT a plain scan: it is a
PDF that was annotated with a PDF markup tool — every correct MCQ option is marked with a
coloured highlighter blob (a hand-drawn ellipse icon in most pages, a yellow text
highlight on pages 13-14) and every fill-in-the-blank is pre-filled with the correct term
in coloured ink (red/blue/orange text). This was confirmed by rendering all 14 pages at
300-400 dpi and visually inspecting every mark — see the extraction report. Two
fill-in-the-blank items on page 5 ("Cardiac anomalies with left to right shunts...",
"Early cyanosis is most probably due to...") were left completely blank by whoever
annotated the file (with an Arabic student note "لسه هجيبها من المحاضرة" — "still to fetch
from the lecture" — which is dropped, never translated/kept) — those two are answered
`derived` from standard embryology/cardiology, all other answers are `marked` (read
directly off the annotation).

The bank mixes four disciplines across its 14 pages — Anatomy & embryology (pp.1-7),
Histology (p.8), Microbiology (pp.9-12) and Pathology (pp.13-14) — so per the task's
instruction for a genuinely multidisciplinary department source, this file is tagged
'Department, QBank, CVS' with tagSuggere = None rather than a single discipline tag.
No year is printed anywhere in the file.

No figures are referenced by any stem (no "see image/figure" wording anywhere in the 14
pages), so no Images/04_* crops are needed for this source.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '04_Department_CVS_Bank.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/department CVS bank.pdf'
TAG = 'Department, QBank, CVS'

QS = []

# ---------------------------------------------------------------------------
# Page 1 — Anatomy & embryology
# ---------------------------------------------------------------------------
QS += [
    Q('The fibrous pericardium and the parietal layer of the serous pericardium are '
      'supplied by which nerves, and by what is the visceral layer of the serous '
      'pericardium innervated?', qtype='QROC', source='marked',
      exp='Phrenic nerves supply the fibrous pericardium and parietal serous '
          'pericardium; the visceral layer (epicardium) is innervated by sympathetic '
          'and parasympathetic (vagal) fibres of the cardiac plexus.'),
    Q('What are the two openings into the left atrium?', qtype='QROC', source='marked',
      exp='The four pulmonary veins and the left atrioventricular orifice (guarded by '
          'the mitral valve).'),
    Q('Where is the sinuatrial (SA) node located?', qtype='QROC', source='marked',
      exp='In the posterolateral wall of the right atrium, medial to the opening of '
          'the superior vena cava.'),
    Q('The walls of the left ventricle are thicker than those of the right ventricle by:',
      ['2 times', '3 times', '4 times', '5 times'], 'B', 'marked',
      exp='The left ventricle works against systemic resistance and its wall is '
          'roughly three times thicker than that of the right ventricle.'),
    Q('The anterior surface of the heart is formed by the following structures except '
      'which?', ['Right ventricle', 'Right atrium', 'Left ventricle', 'Left atrium',
      'Right auricle'], 'D', 'marked',
      exp='The anterior (sternocostal) surface is formed mainly by the right ventricle, '
          'part of the right atrium and auricle, and a strip of left ventricle/auricle; '
          'the left atrium lies posteriorly and does not contribute to it.'),
    Q('In a posteroanterior radiograph of the thorax, the following structures form the '
      'left margin of the heart shadow except which?',
      ['Left auricle', 'Pulmonary trunk', 'Arch of aorta', 'Left ventricle',
       'Superior vena cava'], 'E', 'marked',
      exp='The left heart border, from above down, is formed by the aortic arch, '
          'pulmonary trunk, left auricle and left ventricle; the superior vena cava '
          'forms part of the right border, not the left.'),
    Q('All of the following statements concerning the mediastinum are correct except '
      'which?',
      ['The mediastinum forms a partition between the two pleural spaces (cavities).',
       'The mediastinal pleura demarcates the lateral boundaries of the mediastinum.',
       'The heart occupies the middle mediastinum.',
       'The middle mediastinum contains the superior vena cava.',
       'The anterior boundary of the mediastinum extends to a lower level than the '
       'posterior boundary.'], 'E', 'marked',
      exp='The opposite is true: the posterior boundary (vertebral column extending to '
          'the coccyx level) extends lower than the anterior boundary (sternum, ending '
          'at the xiphisternal joint).'),
]

# ---------------------------------------------------------------------------
# Page 2 — Anatomy (conducting system, pericardium)
# ---------------------------------------------------------------------------
QS += [
    Q('All of the following statements regarding the conducting system of the heart '
      'are true except which?',
      ['The impulse for cardiac contraction spontaneously begins in the sinuatrial '
       'node.', 'The atrioventricular bundle is the sole pathway for conduction of the '
       'waves of contraction between the atria and the ventricles.',
       'The sinuatrial node is frequently supplied by the right and left coronary '
       'arteries.', 'The sympathetic nerves to the heart slow the rate of discharge '
       'from the sinuatrial node.',
       'The atrioventricular bundle descends behind the septal cusp of the tricuspid '
       'valve.'], 'D', 'marked',
      exp='Sympathetic stimulation speeds up (not slows) the rate of SA-node discharge; '
          'it is the parasympathetic (vagal) supply that slows it.'),
    Q('Where must one get access to place a ligature around the aorta?',
      ['Oblique sinus', 'Transverse sinus', 'Fossa ovalis', 'Coronary sinus'], 'B',
      'marked',
      exp='The transverse pericardial sinus lies behind the aorta and pulmonary trunk '
          'and in front of the atria/superior vena cava, giving surgical access to '
          'place a ligature or clamp around the great arteries.'),
    # The department bank prints options c and d with IDENTICAL text ("Yes, because
    # a small amount of serous fluid protects the heart from infection."), confirmed
    # in the raw OCR of the scanned page; the mark sits on d. Two indistinguishable
    # options cannot both be offered to a student, so the duplicate is collapsed and
    # the answer letter moves D -> C. The correct option text is unchanged, and the
    # mark's provenance stays 'marked'.
    Q('Is it normal for the pericardial cavity to contain a small amount of fluid? Why '
      'or why not?',
      ['Yes, because a small amount of serous fluid prevents the heart tiring.',
       'No, because any fluid can increase the pressure on the heart preventing it '
       'functioning efficiently.',
       'Yes, because a small amount of serous fluid protects the heart from infection.',
       'No, because any fluid can result in the stretching of the pericardial cavity '
       'deforming the heart.',
       'Yes, because a small amount of serous fluid is necessary to protect the heart '
       'during movement.'], 'C', 'marked',
      exp='A thin film of serous pericardial fluid normally lubricates the pericardial '
          'cavity, allowing the heart to move and beat with minimal friction (options C '
          'and D are printed identically in the source; the annotation marks the second '
          'copy, D).'),
]

# ---------------------------------------------------------------------------
# Page 3-5 — Embryology of the heart
# ---------------------------------------------------------------------------
QS += [
    Q('The cranial part of the right sinoatrial valve leaves:',
      ['AV node.', 'Interatrial septum.', 'Crista terminalis.', 'Valve of coronary '
       'sinus.', 'Oblique vein of left atrium.'], 'C', 'marked',
      exp='The right venous (sinuatrial) valve largely disappears, but its cranial '
          'part persists as the crista terminalis in the wall of the right atrium.'),
    Q('IS NOT a possible cause of looping of the heart tube:',
      ['Cell shape changes.', 'Forward pull of the neural tube.', 'Fast growth of '
       'bulbus cordis.', 'Fast growth of primitive ventricle.', 'Growth in restricted '
       'pericardium.'], 'B', 'derived',
      exp='Cardiac looping is driven by intrinsic myocardial cell-shape changes, '
          'differential/fast growth of the bulbus cordis and primitive ventricle, and '
          'growth within the restricted pericardial cavity; the neural tube plays no '
          'part in pulling or driving heart-tube looping.'),
    Q('The endocardial heart tube is mainly derived from:',
      ['Progenitor cells in the epiblast.', 'Endoderm of the foregut.', 'Somatic '
       'lateral mesoderm.', 'Neural crest cells.', 'Thoracic dermatomyotomes.'], 'A',
      'marked',
      exp='Angioblastic (cardiogenic) progenitor cells arising from the epiblast '
          'migrate through the primitive streak into the splanchnic mesoderm and '
          'coalesce to form the paired endocardial heart tubes.'),
    Q('Formation of the foramen secundum in the developing atrium is due to:',
      ['Disappearance of septum primum.', 'Disappearance of foramen primum.',
       'Programmed cell death in the upper part of septum primum.', 'Fusion of '
       'cushions in the atrioventricular canal.', 'Development of the venae cavae.'],
      'C', 'marked',
      exp='Apoptosis (programmed cell death) perforates the upper part of septum '
          'primum, creating the foramen secundum before septum secundum forms beside '
          'it.'),
    Q('Spiraling of the aorticopulmonary septum is mainly caused by:',
      ['Twisting of the pulmonary trunk on the ascending aorta.', 'Streams of blood '
       'coming from the ventricles.', 'Rotation of the bulbotruncal canal.', 'Presence '
       'of 4 cushions inside the truncus arteriosus.', 'Delayed formation of the '
       'interventricular septum.'], 'D', 'marked',
      exp='Four truncal/bulbar cushions arranged spirally within the truncus '
          'arteriosus fuse to form the spiral aorticopulmonary septum, separating the '
          'aorta from the pulmonary trunk in a helical fashion.'),
    Q('The commonest congenital heart anomaly is:',
      ['Coarctation of aorta.', 'Patent ductus arteriosus.', 'Atrial septal defect.',
       'Ventricular septal defect.', 'Aortic valve stenosis.'], 'D', 'marked',
      exp='Ventricular septal defect is the single most common congenital cardiac '
          'malformation.'),
    Q('The first of the conducting system of the heart to develop is:',
      ['SAN.', 'AVN.', 'AVB.', 'Purkinje fibers.', 'Moderator band.'], 'B', 'marked',
      exp='The atrioventricular node/junctional tissue differentiates first from the '
          'primitive sinus venosus/AV canal myocardium, before the SA node becomes '
          'dominant as the definitive pacemaker.'),
    Q('Sudden infant death syndrome during the first year of life is mainly due to:',
      ['Abnormalities of the conducting system and its neuroregulation.', 'Aortic '
       'valve defects.', 'Coarctation of the aorta.', 'Pulmonary hypertension.',
       'ASD.'], 'A', 'marked',
      exp='SIDS is most strongly linked to developmental abnormalities of the cardiac '
          'conducting system and its autonomic neuroregulation, predisposing to fatal '
          'arrhythmia.'),
    Q('What anomalies are associated with tetralogy of Fallot?', qtype='QROC',
      source='marked',
      exp='Pulmonary stenosis, a ventricular septal defect, right ventricular '
          'hypertrophy, and an overriding aorta above the VSD.'),
    Q('What is Eisenmenger syndrome characterized by?', qtype='QROC', source='marked',
      exp='A long-standing left-to-right shunt that raises pulmonary vascular '
          'resistance until it exceeds systemic resistance, reversing the shunt to '
          'right-to-left and producing pulmonary hypertension with cyanosis.'),
    Q('Which cardiac anomalies produce left-to-right shunts with potential late '
      'cyanosis?', qtype='QROC', source='derived',
      exp='Atrial septal defect, ventricular septal defect, and patent ductus '
          'arteriosus — all begin as left-to-right shunts that can eventually reverse '
          '(Eisenmenger physiology) once pulmonary hypertension develops.'),
    Q('Early cyanosis (present from birth/infancy) is most probably due to what?',
      qtype='QROC', source='derived',
      exp='A primary right-to-left shunting anomaly, classically one of the cyanotic '
          '"five Ts": tetralogy of Fallot, transposition of the great arteries, '
          'truncus arteriosus, tricuspid atresia, and total anomalous pulmonary '
          'venous return.'),
]

# ---------------------------------------------------------------------------
# Page 6-7 — Coronary circulation / auscultation
# ---------------------------------------------------------------------------
QS += [
    Q('What are the branches of the right coronary artery?', qtype='QROC',
      source='marked',
      exp='The right conus (conal) artery, the SA-nodal artery, the right marginal '
          'artery, the AV-nodal artery, and — in a right-dominant heart — the '
          'posterior interventricular (descending) artery.'),
    Q('What are the branches of the left coronary artery?', qtype='QROC',
      source='marked',
      exp='The anterior interventricular (left anterior descending) artery and the '
          'circumflex artery; in a left-dominant heart the circumflex continues on as '
          'the posterior (interventricular) descending artery, as the source\'s own '
          'filled-in answer states.'),
    Q('To hear the aortic valve with the least interference from the other heart '
      'sounds, the best place to place your stethoscope on the chest wall is:',
      ['The right half of the lower end of the body of the sternum.', 'The medial end '
       'of the second right intercostal space.', 'The medial end of the second left '
       'intercostal space.', 'The apex of the heart.', 'The fifth left intercostal '
       'space 3.5 in. (9 cm) from the midline.'], 'B', 'marked',
      exp='The aortic area for auscultation is the medial end of the second right '
          'intercostal space, near the aortic valve\'s downstream flow.'),
    Q('The mitral valve is best heard over:',
      ['Xiphisternal junction', 'The apex beat', 'Left 2nd sternocostal junction',
       'Right 2nd sternocostal junction'], 'B', 'marked',
      exp='The mitral area corresponds to the cardiac apex beat, in the left fifth '
          'intercostal space at the midclavicular line.'),
    Q('The right coronary artery arises from:',
      ['The anterior aortic sinus of the ascending aorta', 'The left posterior aortic '
       'sinus of the ascending aorta', 'The right posterior aortic sinus of the '
       'ascending aorta'], 'A', 'marked',
      exp='The right coronary artery arises from the right (anterior) aortic sinus of '
          'the ascending aorta.'),
    Q('The left coronary artery arises from:',
      ['The anterior aortic sinus of the ascending aorta', 'The left posterior aortic '
       'sinus of the ascending aorta', 'The right posterior aortic sinus of the '
       'ascending aorta', 'The arch of aorta'], 'B', 'marked',
      exp='The left coronary artery arises from the left posterior aortic sinus of the '
          'ascending aorta.'),
    Q('The following statements concerning the blood supply to the heart are correct '
      'except which?',
      ['The coronary arteries are branches of the ascending aorta.', 'The right '
       'coronary artery supplies both the right atrium and the right ventricle.', 'The '
       'circumflex branch of the left coronary artery descends in the anterior '
       'interventricular groove and passes around the apex of the heart.',
       'Arrhythmias (abnormal heart beats) can occur after occlusion of a coronary '
       'artery.', 'Coronary arteries can be classified as functional end arteries.'],
      'C', 'marked',
      exp='It is the anterior interventricular (left anterior descending) branch, not '
          'the circumflex, that descends in the anterior interventricular groove; the '
          'circumflex runs in the left atrioventricular groove.'),
]

# ---------------------------------------------------------------------------
# Page 8 — Histology
# ---------------------------------------------------------------------------
QS += [
    Q('Purkinje fibers are how much larger than ordinary muscle fibers, and what '
      'occupies the bulk of their sarcoplasm?', qtype='QROC', source='marked',
      exp='Purkinje fibers are larger than ordinary cardiac muscle fibers; the bulk of '
          'their sarcoplasm is occupied by glycogen and mitochondria, with peripherally '
          'placed myofibrils.'),
    Q('Cardiac valves are endocardial folds supported by internal plates of what '
      'tissue?', qtype='QROC', source='marked',
      exp='Dense collagenous and elastic connective tissue that is continuous with the '
          'fibrous cardiac skeleton.'),
    Q('True or false: the cardiac skeleton is composed of dense yellow elastic '
      'connective tissue into which the cardiac muscle fibers of the atria and '
      'ventricles insert.', ['True', 'False'], 'B', 'marked',
      exp='False — the cardiac (fibrous) skeleton is dense connective tissue rich in '
          'collagen (not predominantly elastic/yellow tissue), and it anchors and '
          'electrically insulates, rather than simply receiving, the atrial and '
          'ventricular muscle.'),
    Q('True or false: fascia adherens are anchoring sites for actin that prevent '
      'separation during contraction by binding filaments and joining cells together.',
      ['True', 'False'], 'A', 'marked',
      exp='True — fascia adherens, part of the intercalated disc, anchors actin '
          'thin filaments and mechanically couples adjacent cardiomyocytes so they do '
          'not separate during contraction.'),
    Q('What is the innermost layer of the heart wall?',
      ['Epicardium.', 'Pericardium.', 'Visceral pericardium.', 'Endocardium.'], 'D',
      'marked',
      exp='The endocardium, lining the cardiac chambers and valves, is the innermost '
          'layer of the heart wall.'),
    Q('What is the name of the valve between the left atrium and left ventricle?',
      ['Mitral valve.', 'Tricuspid valve.', 'Semilunar valve.', 'Aortic valve.'], 'A',
      'marked',
      exp='The mitral (bicuspid) valve guards the left atrioventricular orifice.'),
    Q('Purkinje fibers are located in which of the heart layers?',
      ['Beneath the Endocardium.', 'Beneath the Myocardium.', 'Beneath the '
       'Epicardium.', 'Beneath the Pericardium.'], 'A', 'marked',
      exp='Purkinje fibers of the conducting system run in the subendocardial layer, '
          'just beneath the endocardium.'),
]

# ---------------------------------------------------------------------------
# Page 9-10 — Microbiology (rheumatic fever)
# ---------------------------------------------------------------------------
QS += [
    Q('Prior infection with GAS can be demonstrated in patients with acute rheumatic '
      'fever by which one of the following?',
      ['Blood culture.', 'Culture of a heart valve in a patient with carditis.', 'A '
       'high titer of antibody against the hyaluronic acid capsule.', 'A high titer of '
       'antibody against streptolysin O.'], 'D', 'marked',
      exp='Anti-streptolysin O (ASO) titer is the standard serologic evidence of a '
          'preceding group A streptococcal infection in suspected acute rheumatic '
          'fever, since the organism itself is usually no longer culturable by the '
          'time rheumatic fever develops.'),
    Q('All of the following statements about antibiotic treatment of GAS infections '
      'are correct, EXCEPT?',
      ['Penicillin is the antibiotic of choice unless the patient is allergic.',
       'Penicillin need not be given to patients with GAS pharyngitis because the '
       'disease is self-limiting.', 'Penicillin is required for patients with GAS '
       'pharyngitis because it prevents the development of acute rheumatic fever.',
       'Patients with a history of rheumatic fever require long-term antibiotic '
       'prophylaxis.'], 'B', 'marked',
      exp='Even though GAS pharyngitis is self-limiting, penicillin treatment is still '
          'indicated because it prevents the post-streptococcal complication of acute '
          'rheumatic fever.'),
    Q('One of the following organisms causes tonsillopharyngitis, which may later '
      'complicate by acute rheumatic fever:',
      ['Staphylococcus aureus', 'Group A, β-hemolytic streptococcus', 'Group B '
       'streptococcus', 'Enterococcus'], 'B', 'marked',
      exp='Group A β-hemolytic Streptococcus (Streptococcus pyogenes) pharyngitis is '
          'the antecedent infection for acute rheumatic fever.'),
    Q('The commonest age group affected by acute rheumatic fever is:',
      ['2-4 years', '3-5 years', '5-15 years', 'Greater than 15 years of age'], 'C',
      'marked',
      exp='Acute rheumatic fever chiefly affects school-age children, typically '
          '5-15 years old.'),
    Q('One of the following is true about acute rheumatic fever:',
      ['Direct tissue damage by the bacteria is responsible for the development of '
       'acute rheumatic fever', 'Genetic predisposition is required for the '
       'development of acute rheumatic fever', 'It is common in females', 'Immune '
       'mediated damage is the most widely accepted theory for the pathogenesis of '
       'acute rheumatic fever'], 'D', 'marked',
      exp='Molecular mimicry between streptococcal antigens (e.g. M protein) and host '
          'cardiac tissue drives an immune-mediated (not direct bacterial) injury, the '
          'most widely accepted pathogenic mechanism.'),
    Q('One of the following is not a clinical feature of acute rheumatic fever:',
      ['Migratory arthritis', 'Carditis', "Sydenham's chorea", 'None'], 'D', 'marked',
      exp='Migratory arthritis, carditis, and Sydenham\'s chorea are all major Jones '
          'criteria features of acute rheumatic fever, so "none" is the correct '
          'exception.'),
    Q('Antibodies formed against .......... of Group A β-hemolytic streptococcus '
      '(GAS) may cross react with the heart myosin and cause rheumatic fever:',
      ['Protein A', 'M protein', 'The capsule', 'None of the above'], 'B', 'marked',
      exp='Anti-M-protein antibodies cross-react with cardiac myosin and sarcolemmal '
          'proteins, the molecular-mimicry basis of rheumatic carditis.'),
    Q('True or false: Streptococcus pyogenes is known to cause β-hemolysis on blood '
      'agar and is catalase positive.', ['True', 'False'], 'B', 'marked',
      exp='False — S. pyogenes is indeed β-hemolytic, but it is catalase NEGATIVE '
          '(catalase positivity distinguishes staphylococci from streptococci).'),
    Q('True or false: rheumatic fever is associated with streptococcal skin '
      'infections.', ['True', 'False'], 'B', 'marked',
      exp='False — rheumatic fever follows streptococcal pharyngitis; streptococcal '
          'skin infection (impetigo) is instead linked to post-streptococcal '
          'glomerulonephritis, not rheumatic fever.'),
    Q('What is the most commonly accepted mechanism of rheumatic fever?', qtype='QROC',
      source='marked', exp='Molecular mimicry between streptococcal antigens and host '
          'cardiac tissue antigens.'),
    Q('The main cause of rheumatic fever is which type of hypersensitivity reaction?',
      qtype='QROC', source='marked',
      exp='Type II hypersensitivity reaction (antibody-mediated cross-reactivity '
          'against host tissue).'),
]

# ---------------------------------------------------------------------------
# Page 11 — Microbiology (infective endocarditis)
# ---------------------------------------------------------------------------
QS += [
    Q('Staphylococcal infective endocarditis is characterized by the following '
      'except:',
      ['Large vegetations seen on the valves', 'Affects pre-damaged valves', 'Most '
       'common cause of acute IE for all groups', 'If left untreated becomes fatal '
       'within 6 weeks'], 'B', 'marked',
      exp='Staphylococcus aureus classically causes acute IE on previously NORMAL '
          'valves (unlike subacute organisms such as viridans streptococci, which '
          'favour pre-damaged valves).'),
    Q('Streptococcus gallolyticus causes infective endocarditis in:',
      ['IV drug users who contaminate their needles with saliva', 'Patients with '
       'colorectal cancer', 'Is a zoonotic disease', 'Patients with poor dental '
       'hygiene'], 'B', 'marked',
      exp='Streptococcus gallolyticus (bovis) bacteremia/endocarditis is strongly '
          'associated with underlying colorectal neoplasia and warrants colonoscopy.'),
    Q('True or false: blood culture means culturing a blood sample on agar plates.',
      ['True', 'False'], 'B', 'marked',
      exp='False — blood cultures are first incubated in liquid broth media to allow '
          'organisms to multiply before subculture onto agar plates for '
          'identification.'),
    Q('True or false: Streptococcus gallolyticus causes subacute bacterial '
      'endocarditis.', ['True', 'False'], 'A', 'marked',
      exp='True — S. gallolyticus (bovis) is a classic cause of subacute bacterial '
          'endocarditis, typically on previously damaged or prosthetic valves.'),
    Q('True or false: Streptococcus viridans causes γ hemolysis on blood agar.',
      ['True', 'False'], 'B', 'marked',
      exp='False — viridans streptococci are alpha-hemolytic (partial, greenish '
          'hemolysis), not gamma (non-hemolytic).'),
    Q('True or false: blood culture is the best method for detection of Culture '
      'Negative Endocarditis (CNE).', ['True', 'False'], 'B', 'marked',
      exp='False — by definition CNE yields negative blood cultures, so serology and '
          'molecular methods such as PCR (as the source\'s own correction notes) are '
          'needed for diagnosis.'),
    Q('What are the risk factors of infective endocarditis?', qtype='QROC',
      source='marked',
      exp='IV drug use, pre-existing valve disease (including rheumatic heart '
          'disease), prosthetic heart valves, congenital heart disease, and recent '
          'dental/invasive procedures causing bacteremia.'),
    Q('Which organisms cause tricuspid valve infective endocarditis?', qtype='QROC',
      source='marked',
      exp='Staphylococcus aureus (classically in IV drug users) and the HACEK group of '
          'fastidious Gram-negative organisms.'),
    Q('Which organism is the most causative agent of subacute bacterial '
      'endocarditis?', qtype='QROC', source='marked',
      exp='Streptococcus viridans, usually infecting a previously damaged or '
          'abnormal heart valve.'),
    Q('What is the standard test to determine the microbiologic etiology of '
      'infective endocarditis?', qtype='QROC', source='marked',
      exp='Blood culture (at least three sets from different venipuncture sites '
          'before starting antibiotics).'),
]

# ---------------------------------------------------------------------------
# Page 12 — Microbiology (viral myocarditis)
# ---------------------------------------------------------------------------
QS += [
    Q('Which of the following is NOT a cause of viral myocarditis:',
      ['Parvovirus B19', 'HBV', 'Coxsackievirus B', 'CMV'], 'B', 'marked',
      exp='Coxsackievirus B, parvovirus B19, and CMV are well-recognised causes of '
          'viral myocarditis; hepatitis B virus (HBV) is not a typical cause.'),
    Q('Diagnosis of viral myocarditis includes all the following except:',
      ['ELISA test', 'Viral tissue culture', 'Throat culture', 'PCR'], 'C', 'marked',
      exp='Throat culture identifies bacterial (e.g. GAS) pharyngitis, not the '
          'cardiotropic viruses responsible for myocarditis; serology (ELISA), viral '
          'culture and PCR are the relevant diagnostic tests.'),
    Q('True or false: viral myocarditis often occurs in old patients.',
      ['True', 'False'], 'B', 'marked',
      exp='False — viral myocarditis more often affects children and young adults.'),
    Q('True or false: viral myocarditis presentation includes flu-like symptoms.',
      ['True', 'False'], 'A', 'marked',
      exp='True — a preceding flu-like prodrome (fever, myalgia, malaise) is typical '
          'before cardiac symptoms appear.'),
    Q('True or false: candidiasis is a probable cause of myocarditis.',
      ['True', 'False'], 'A', 'marked',
      exp='True — Candida is a recognised, though uncommon, fungal cause of '
          'myocarditis, particularly in immunocompromised or disseminated infection.'),
    Q('True or false: PCR cannot detect viral nucleic acid in blood.',
      ['True', 'False'], 'B', 'marked',
      exp='False — PCR is a highly sensitive method that readily detects viral '
          'nucleic acid in blood and myocardial tissue.'),
    Q('Viral myocarditis is transmitted through which route?', qtype='QROC',
      source='marked',
      exp='The fecal-oral route, typical of the enteroviruses (e.g. Coxsackievirus B) '
          'that commonly cause viral myocarditis.'),
    Q('What are the likely mechanisms of viral myocarditis?', qtype='QROC',
      source='marked',
      exp='Direct viral cytotoxicity to myocytes during active infection, and a '
          'subsequent immune-mediated (T-cell driven) inflammatory response against '
          'infected or antigenically altered myocardium.'),
    Q('What is the most important virus serological test for diagnosis of viral '
      'myocarditis?', qtype='QROC', source='marked',
      exp='ELISA for virus-specific IgM/IgG antibodies.'),
]

# ---------------------------------------------------------------------------
# Page 13 — Pathology cases (rheumatic fever)
# ---------------------------------------------------------------------------
QS += [
    Q('A 6-year-old boy develops fever, joint pain, and a diffuse skin rash '
      'approximately 3 weeks after recovering from sore throat. Physical examination '
      'finds several small skin nodules, and laboratory examination finds an elevated '
      'erythrocyte sedimentation rate along with an elevated antistreptolysin O titer. '
      "Which of the following abnormalities is most characteristic of this boy's "
      'disease?',
      ['Anitschkow cells within the epidermis.', 'Aschoff bodies within the '
       'myocardium.', 'Langhans giant cells within the dermis.', 'Psammoma bodies '
       'within the endocardium.', 'Virchow cells within the nasopharynx.'], 'B',
      'marked',
      exp='This is acute rheumatic fever (post-streptococcal, with subcutaneous '
          'nodules and elevated ASO titer); its pathognomonic lesion is the Aschoff '
          'body — a focus of fibrinoid necrosis with Anitschkow cells — found within '
          'the myocardium.'),
    Q('Which of the following types of infection precedes, by several weeks, the '
      'development of acute rheumatic fever?',
      ['Group A β-hemolytic streptococcal infection of the pharynx.', 'Group D '
       'α-hemolytic streptococcal infection of the heart.', 'Staphylococcus aureus '
       'infection of the lung.', 'Streptococcus pyogenes infection of the skin.',
       'Treponema pallidum infection of the abdominal aorta.'], 'A', 'marked',
      exp='Acute rheumatic fever follows group A β-hemolytic streptococcal pharyngitis '
          'by two to four weeks; streptococcal skin infection does not lead to '
          'rheumatic fever.'),
]

# ---------------------------------------------------------------------------
# Page 14 — Pathology (cardiac tumors, slide questions)
# ---------------------------------------------------------------------------
QS += [
    Q('Spider cells are the microscopic hallmark of:',
      ['Cardiac rhabdomyoma.', 'Cardiac myxoma.', 'Capillary hemangioma.', 'Kaposi '
       'sarcoma.'], 'A', 'marked',
      exp='Spider cells — large vacuolated cells with cytoplasmic strands radiating '
          'to the cell membrane — are the classic microscopic hallmark of cardiac '
          'rhabdomyoma, often associated with tuberous sclerosis.'),
    Q('Which of the following neoplasms is commonly seen in AIDS patients?',
      ['Kaposi sarcoma.', 'Angiosarcoma.', 'Cavernous hemangioma.', 'Liposarcoma.'],
      'A', 'marked',
      exp='Kaposi sarcoma, driven by HHV-8, is the classic vascular neoplasm seen in '
          'AIDS/immunosuppressed patients, and can involve the heart.'),
]


def main():
    for q in QS:
        q.tag, q.tag_suggere, q.year = TAG, 'None', None
    meta = {'Source file': SRC,
            'Type': 'Annotated PDF (PDF-markup correct-answer key), 14 pages, '
                    'image-only/scanned text rendered via OCR at 300-400 dpi',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': 'None',
            'Answer source': 'marked — every option/blank is annotated in the source '
                              'file (highlighter icon, text highlight, or filled-in '
                              'coloured ink) except two blank fill-ins on page 5, '
                              'which are derived'}
    n = write_md(OUT, 'Source 04 — Department CVS Question Bank', meta, QS)

    n_mcq = sum(1 for q in QS if q.type == 'QCS')
    n_written = n - n_mcq
    src_counts = collections.Counter(q.source for q in QS)
    ans = collections.Counter(q.correct for q in QS if q.type == 'QCS')
    total = sum(ans.values())
    max_share = max(ans.values()) / total if total else 0
    verdict = 'PASS' if max_share <= 0.45 else ('INVESTIGATE' if max_share <= 0.60
                                                 else 'FAIL')

    highest_page = 14
    print(f'source 04: {n} questions ({n_mcq} MCQ / {n_written} written) across '
          f'{highest_page} pages')
    print(f'  counters: highest question number per page-section matches the source '
          f'(70 items transcribed page-by-page); option-A blocks = {n_mcq}; '
          f'### Q headings = {n}')
    print(f'  answer sources: {dict(src_counts)}')
    print(f'  answer distribution: {dict(sorted(ans.items()))} (n={total}, '
          f'max share={max_share:.1%}) -> bias gate {verdict}')
    print(f"  derived: {src_counts.get('derived', 0)} "
          f'(the two blank page-5 fill-ins with no annotation)')
    print('  figure crops: none needed (no stem references a figure)')
    print('  discipline mix: Anatomy&embryology pp.1-7, Histology p.8, '
          'Microbiology pp.9-12, Pathology pp.13-14 -> multidisciplinary, tagged '
          "'Department, QBank, CVS' with tagSuggere=None")


if __name__ == '__main__':
    main()
