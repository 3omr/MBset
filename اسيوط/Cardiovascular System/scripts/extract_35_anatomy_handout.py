#!/usr/bin/env python3
"""Source 35 — question section on pages 25-28 of "CVS-L 23.pdf".

Prof. Adel Kamel's development-of-the-CVS handout: pages 1-24 are the lecture (already
published under Lectures/ as the DEVELOPMENT and GREAT_VESSELS subcategories) and pages
25-28 are an anatomy-department question set in five parts —
  I   ten MCQs,
  I   two 5-item MATCHING blocks (11-15, 16-20),
  II  eight fill-in-the-blank "Complete" items,
  III five "Explain why" items,
  IV  five clinical cases with sub-questions.

There is NO answer key anywhere in the handout, so every answer here is `derived`,
answered from the handout's own pages 1-24. Matching blocks keep both columns inside
one stem (project SOP) rather than being split into five broken fragments.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '35_Anatomy_Development_Handout_Questions.md')
TAG = 'Department, QBank, Anatomy'

MCQ = [
    ('The cranial part of the right sinoatrial valve leaves',
     ['AV node', 'Interatrial septum', 'Crista terminalis',
      'Valve of coronary sinus', 'Oblique vein of left atrium'], 'C'),
    ('Early neonatal cyanosis is mainly due to which cardiovascular anomaly',
     ['Fallot tetralogy', 'Aortic stenosis', 'Patent ductus arteriosus',
      'Transposition of great arteries', 'Dextrocardia'], 'D'),
    ('The endocardial heart tube is mainly derived from',
     ['Progenitor cells in the epiblast', 'Endoderm of the foregut',
      'Somatic lateral mesoderm', 'Neural crest cells',
      'Thoracic dermatomyotomes'], 'C'),
    ('Formation of foramen secundum in the developing atrium is due to',
     ['Disappearance of septum primum', 'Disappearance of foramen primum',
      'Programmed cell death in the upper part of septum primum',
      'Fusion of cushions in the atrioventricular canal',
      'Development of the venae cavae'], 'C'),
    ('Spiraling of the aorticopulmonary septum is mainly caused by',
     ['Twisting of pulmonary trunk on ascending aorta',
      'Streams of blood coming from ventricles', 'Rotation of bulbotruncal canal',
      'Presence of 4 cushions inside the truncus arteriosus',
      'Delayed formation of interventricular septum'], 'B'),
    ('The commonest congenital heart anomaly is',
     ['Coarctation of aorta', 'Patent ductus arteriosus', 'Atrial septal defect',
      'Ventricular septal defect', 'Aortic valve stenosis'], 'D'),
    ('The first of the conducting system of the heart to develop is',
     ['SAN', 'AVN', 'AVB', 'Purkinje fibers', 'Moderator band'], 'B'),
    ('Sudden infant death syndrome during the first year of life is mainly due to',
     ['Abnormalities of the conducting system and its neuro-regulation',
      'Aortic valve defects', 'Coarctation of the aorta',
      'Pulmonary hypertension', 'ASD'], 'A'),
    ('Carotid arteries remain from',
     ['Aortic sac', 'Cranial part of dorsal aorta', 'Third aortic arches',
      'Fourth aortic arches', 'Truncus arteriosus'], 'C'),
    ('Coronary arteries develop from',
     ['First aortic arches', 'Blood islands deep to epicardium', 'Aortic sac',
      'Internal carotid arteries', 'Descending thoracic aorta'], 'B'),
]

MATCHING = [
    ('Match each event in column I with the appropriate embryonic day in column II. '
     'Column I: (11) Complete looping of heart tube; (12) Development of SAN; '
     '(13) Complete fusion of interventricular septum; (14) Disappearance of sinus '
     'venosus; (15) Start beating of the heart. '
     'Column II: (a) Day 49; (b) Day 28; (c) Day 70; (d) Day 22; (e) Day 35.',
     '11 - b (Day 28); 12 - e (Day 35); 13 - a (Day 49); 14 - c (Day 70); '
     '15 - d (Day 22).'),
    ('Match each cardiovascular anomaly in column I with its manifestation in column II. '
     'Column I: (16) Double aortic arches; (17) Coarctation of aorta; '
     '(18) Defective development of conducting system; (19) Fallot tetralogy; '
     '(20) Ectopia cordis. '
     'Column II: (a) Late cyanosis; (b) Thoracic exposure of the heart; '
     '(c) Dysphagia; (d) Weak pulse of lower limbs; (e) Sudden infant death.',
     '16 - c (Dysphagia, from the vascular ring compressing the oesophagus); '
     '17 - d (Weak pulse of the lower limbs); 18 - e (Sudden infant death); '
     '19 - a (Late cyanosis); 20 - b (Thoracic exposure of the heart).'),
]

COMPLETE = [
    ('Complete: the anomalies associated with Fallot tetralogy are ......, ......, '
     '......, ......',
     'Pulmonary stenosis (infundibular stenosis of the right ventricular outflow); '
     'ventricular septal defect; overriding (dextroposition) of the aorta; '
     'right ventricular hypertrophy.'),
    ('Complete: the branches of the permanent aortic arch are ......, ......, ......',
     'Brachiocephalic (innominate) artery; left common carotid artery; '
     'left subclavian artery.'),
    ('Complete: the superior vena cava is formed by fusion of ......',
     'The right common cardinal vein together with the proximal part of the right '
     'anterior cardinal vein.'),
    ('Complete: the tributaries of the azygos vein are ......',
     'The right posterior cardinal vein and the right supracardinal vein contributions '
     '— i.e. the right subcardinal-supracardinal anastomosis, the right posterior '
     'intercostal veins, the hemiazygos and accessory hemiazygos veins, and the right '
     'bronchial and oesophageal veins.'),
    ('Complete: Eisenmenger syndrome is characterized by ......',
     'Long-standing left-to-right shunt causing pulmonary hypertension and obstructive '
     'pulmonary vascular disease, which then reverses the shunt to right-to-left and '
     'produces late cyanosis.'),
    ('Complete: the cardiac anomalies with left-to-right shunts and potential late '
     'cyanosis are ......',
     'Atrial septal defect; ventricular septal defect; patent ductus arteriosus.'),
    ('Complete: the cardiac anomalies with early cyanosis are ......',
     'Transposition of the great arteries; Fallot tetralogy; tricuspid atresia '
     '(also persistent truncus arteriosus).'),
    ('State the main signs of coarctation of the aorta.',
     'Hypertension with a bounding pulse in the upper limbs; weak, delayed or absent '
     'femoral pulses with a large blood-pressure difference between upper and lower '
     'limbs; cold lower limbs, poor weight gain, and collateral circulation through '
     'enlarged intercostal arteries causing rib notching.'),
]

EXPLAIN = [
    ('Explain why the foramen ovale is patent during prenatal life.',
     'The lungs are non-functioning and pulmonary vascular resistance is high, so right '
     'atrial pressure exceeds left atrial pressure. Oxygenated placental blood is '
     'therefore shunted right-to-left across the patent foramen ovale straight into the '
     'left atrium, bypassing the pulmonary circulation.'),
    ('Explain why the ascending aorta and the pulmonary trunk are twisted around each '
     'other.',
     'Because the aorticopulmonary septum that divides the truncus arteriosus develops '
     'in a spiral course, following the spiral streams of blood leaving the ventricles; '
     'the two resulting great vessels are therefore wound around one another.'),
    ('Explain why the left horn of the sinus venosus is less important than the right '
     'horn.',
     'Blood flow is progressively shifted to the right side, so the left horn regresses '
     'and remains only as the oblique vein of the left atrium and the coronary sinus, '
     'while the enlarged right horn is absorbed into the right atrium to form its smooth '
     'part (sinus venarum).'),
    ('Explain why the two endocardial heart tubes become one.',
     'Lateral folding of the embryo brings the two endocardial tubes together in the '
     'midline, where they fuse cranio-caudally into a single heart tube.'),
    ('Explain why only the posterior part of the right atrium is smooth while most of '
     'the left atrium is smooth.',
     'The smooth part of the right atrium comes from absorption of the right horn of the '
     'sinus venosus, which supplies only its posterior part; the rest stays trabeculated '
     'as the primitive atrium (with the crista terminalis as the boundary). In the left '
     'atrium the absorbed primitive pulmonary vein and its branches supply most of the '
     'wall, leaving only the auricle trabeculated.'),
]

CASES = [
    ('A paediatrician detected a cardiac defect in an infant and explained to the '
     "baby's mother that this is a common birth defect. (a) What is the most common "
     'congenital cardiac defect and what is its percentage? (b) What problems would the '
     'infant likely have if this cardiac defect was large?',
     '(a) Ventricular septal defect — the commonest congenital cardiac defect, about '
     '25% of congenital heart defects (congenital heart defects overall occur in about '
     '8 per 1000 births). (b) A large VSD gives a big left-to-right shunt: pulmonary '
     'overcirculation with breathlessness, feeding difficulty and failure to thrive, '
     'recurrent chest infections, and congestive heart failure; if untreated it leads to '
     'pulmonary hypertension, shunt reversal and late cyanosis (Eisenmenger syndrome).'),
    ('After a pregnancy complicated by rubella virus, a female infant was born with '
     'congenital cataract and a congenital heart defect. A radiograph of the chest '
     'showed increased pulmonary vasculature and cardiac enlargement. (a) What '
     'congenital heart defect is commonly associated with maternal rubella? (b) What '
     'probably caused the cardiac enlargement?',
     '(a) Patent ductus arteriosus (pulmonary artery stenosis is also associated). '
     '(b) The left-to-right shunt through the patent ductus increases pulmonary blood '
     'flow and the volume returning to the left heart, so volume overload dilates and '
     'hypertrophies the left atrium and left ventricle — hence the enlarged heart and '
     'the increased pulmonary vasculature.'),
    ('A child is born with severe craniofacial defects and transposition of the great '
     'arteries. (a) What cell population might play a role in both anomalies, and what '
     'type of insult might have produced this? (b) Suggest a possible mechanism for TGA. '
     '(c) What are the main signs of TGA in the newborn?',
     '(a) The neural crest cells — cranial neural crest forms much of the craniofacial '
     'skeleton and also migrates into the outflow tract to form the aorticopulmonary '
     'septum. An insult killing or preventing migration of neural crest cells (for '
     'example retinoic acid, alcohol, or maternal diabetes) damages both. (b) Failure of '
     'the aorticopulmonary septum to spiral: a straight, non-spiral septum makes the '
     'aorta arise from the right ventricle and the pulmonary trunk from the left. '
     '(c) Severe cyanosis from birth that does not respond to oxygen, tachypnoea, and '
     'progressive heart failure; survival depends on mixing through a patent foramen '
     'ovale, ASD, VSD or patent ductus arteriosus.'),
    ('A patient complains of having difficulty swallowing. (a) What vascular abnormality '
     'might produce this complaint? (b) What is the embryological basis of this '
     'abnormality?',
     '(a) A vascular ring — most often a double aortic arch, or an aberrant right '
     'subclavian artery (dysphagia lusoria) — compressing the oesophagus. (b) In a '
     'double aortic arch the distal part of the right dorsal aorta fails to regress, so '
     'both fourth aortic arches persist and encircle the trachea and oesophagus. In an '
     'aberrant right subclavian artery the right fourth arch and the right dorsal aorta '
     'cranial to the seventh intercostal artery regress instead, so the right subclavian '
     'arises from the descending aorta and crosses behind the oesophagus.'),
    ('During prenatal monitoring, a doctor discovered prenatal closure of the foramen '
     'ovale. Which chamber of the heart is expected to be overloaded, and would any '
     'procedure be indicated to help this fetus?',
     'The right atrium — and with it the right ventricle — is overloaded, because '
     'placental blood returning through the inferior vena cava can no longer cross into '
     'the left atrium; the result is right heart hypertrophy and dilatation with '
     'underdevelopment of the left heart, and hydrops fetalis. Yes: balloon atrial '
     'septostomy to reopen an interatrial communication, or early delivery, is indicated.'),
]


def main():
    qs = []
    for stem, opts, correct in MCQ:
        qs.append(Q(stem, opts, correct, 'derived', tag=TAG, tag_suggere='Anatomy'))
    for stem, model in MATCHING + COMPLETE + EXPLAIN + CASES:
        qs.append(Q(stem, None, '-', 'derived', exp=model, qtype='QROC',
                    tag=TAG, tag_suggere='Anatomy'))

    meta = {'Source file': 'Lectures_raw/1- Cardiovascular system/CVS-L 23.pdf (pages 25-28)',
            'Type': 'Anatomy department handout question section, 4 pages',
            'Tag': TAG, 'tagSuggere': 'Anatomy', 'Year': 'None',
            'Answer source': 'derived — the handout prints NO answer key; answers come '
                             'from the same handout\'s lecture pages 1-24'}
    n = write_md(OUT, 'Source 35 — Anatomy development handout questions', meta, qs)

    mcq = len(MCQ)
    ans = collections.Counter(q.correct for q in qs if q.type == 'QCS')
    top = max(ans.values()) / sum(ans.values()) * 100
    print(f'source 35: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: numbered items in source = 10 MCQ + 2 matching + 8 complete + '
          f'5 explain + 5 cases = 30; option-A blocks = {mcq}; ### Q = {n}')
    print(f'  answer sources: {{\'derived\': {n}}}')
    print(f'  answer distribution: {dict(sorted(ans.items()))}, top={top:.0f}% '
          f'({mcq} MCQs — under 15, bias gate n/a)')
    print(f'  derived: {n}  <-- the whole file; the source has no key')


if __name__ == '__main__':
    main()
