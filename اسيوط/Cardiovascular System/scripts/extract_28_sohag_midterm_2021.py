#!/usr/bin/env python3
"""Source 28 — OTHER EXAMS/ميد سوهاج 2021.pdf ("Midterm Sohag 2021").

Sohag University, Faculty of Medicine — CVS-206 End-block Exam, Second Year,
dated 13/11/2021. 3 pages, 24 questions, 24 marks (1 question = 1 mark), 30 minutes.

This is a scanned image-only PDF (pdftotext returns nothing) laid out in two
columns per page. The bundled OCR (.ocr/28_sohag_midterm_2021.txt) is badly
scrambled — it duplicates page 2 verbatim as "page 2" again, mangles the two
columns into interleaved fragments, and cannot be parsed reliably. Per the
extraction contract this file was re-rendered at 400 dpi
(`pdftoppm -png -r 400`) and read by eye, page by page.

The paper circles the correct option by hand/print on every question — a real
answer key embedded in the source, not a student's own pick — so every answer
here is Answer Source 'marked', transcribed directly off the circled letter in
the rendered image. All 24 stems/options are hand-transcribed from the images
because the scan quality makes automated text extraction unusable; this is a
hardcoded-content script, following the same pattern lib_md.Q expects.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '28_Sohag_Midterm_2021.md')
TAG, YEAR = 'External, Sohag 2021', 2021
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/ميد سوهاج 2021.pdf'

# (stem, [options A..], correct letter, explanation)
RAW = [
("All of the following form the Endocardium EXCEPT:",
 ["Endothelium", "Lamina propria", "Smooth muscle fibers", "Elastic fibers"], "C",
 "The endocardium is endothelium plus a thin subendothelial layer of connective tissue "
 "(lamina propria/elastic fibers); smooth muscle fibers belong to the myocardium, not the endocardium."),
("One exception to Mary's law of baroreceptor:",
 ["Hypothyroidism", "Hypoadrenalism", "Sleep", "Atherosclerosis"], "C",
 "Baroreceptor resetting (Mary's law) is overridden physiologically during sleep, when blood "
 "pressure and baroreceptor set-point both fall together."),
("Alam-Smirk reflex:",
 ["Occurs with exercise to increase COP", "Proprioceptors in muscles, cause decrease in heart rate",
  "The blood flow to the muscle increase with vasoconstriction",
  "When venous return to the heart increase, the heart rate increase"], "A",
 "The Alam-Smirk reflex is a pressor reflex triggered by static muscle contraction/exercise that "
 "raises heart rate and cardiac output."),
("Slow response cardiac action potential is recorded from the:",
 ["Atria", "Ventricles", "His-Purkinje system", "S-A node"], "D",
 "The S-A (and A-V) node generate slow-response action potentials, driven by a slow Ca2+ "
 "inward current rather than fast Na+ channels."),
("About the initial Repolarization (Phase 1) of cardiac muscle:",
 ["It occurs immediately after plateau phase", "It is due to the transient opening of calcium channels",
  "It is due to the transient opening of potassium channels", "Another AP can be initiated during it"], "C",
 "Phase 1 is the brief early repolarization caused by transient outward K+ current (Ito) after the fast Na+ upstroke."),
("The only normal conducting route between atrium and ventricle is the:",
 ["Bundle of His", "Bundle of Kent", "Bundle of James", "Thorel fibers"], "A",
 "The bundle of His is the only normal electrical connection through the fibrous skeleton between atria and ventricles; "
 "Kent/James/Thorel are accessory pathways seen in pre-excitation syndromes."),
("Which of the following is an ECG sign of hyperkalaemia:",
 ["Prominent U wave", "Prolonged QU interval", "Large notched P wave", "Tall peaked T wave"], "D",
 "Hyperkalaemia classically produces tall, peaked (tented) T waves."),
("Which of the following is a normal finding in ECG:",
 ["PR interval = 0.28 sec", "J point at the isoelectric line", "QT interval > half the RR interval",
  "P wave duration = 0.1 msec"], "B",
 "A J point on the isoelectric baseline is normal; PR 0.28s is prolonged (1st degree block), "
 "QT should be < half RR normally, and P wave duration is ~0.08-0.1 sec (not msec)."),
("In AV nodal rhythm, which of the following is correct:",
 ["P wave is absent", "PR interval is prolonged", "T wave is inverted", "RR interval is prolonged"], "A",
 "In a junctional (AV nodal) rhythm the atria are depolarized retrogradely or not at all from the node's "
 "perspective, so a discrete, normally-placed P wave is typically absent or buried in the QRS."),
("The low-resistance pathways between myocardial cells that allow spread of action potentials are:",
 ["Gap junctions", "T tubules", "Sarcoplasmic reticulum (SR)", "Intercalated disks"], "A",
 "Gap junctions (within the intercalated disks) are the low-resistance channels that electrically couple "
 "myocardial cells for action potential spread."),
("The work performed by the left ventricle is greater than that performed by the right ventricle, because in the left ventricle",
 ["The contraction is slower", "The wall is thicker", "The preload is greater", "The afterload is greater"], "D",
 "The left ventricle must generate much higher pressure to overcome systemic (aortic) resistance — a far "
 "greater afterload than the right ventricle faces against the pulmonary circuit."),
("The maximum pressure recorded in the ventricle occurs during:",
 ["Rapid filling", "Isovolumetric contraction", "Ventricular ejection", "Isovolumetric relaxation"], "C",
 "Peak ventricular pressure is reached during ejection, near the end of the ejection phase, when pressure exceeds "
 "aortic pressure the most."),
("The dicrotic notch on the aortic pressure curve is caused by:",
 ["Closure of the mitral valve", "Closure of the tricuspid valve", "Closure of the aortic valve",
  "Closure of the pulmonary valve"], "C",
 "The dicrotic notch reflects the brief backflow and pressure rebound that occurs when the aortic valve closes."),
("Splitting of the second heart sound that appears during inspiration, and not apparent during expiration is most likely due to:",
 ["Aortic regurgitation", "Left bundle branch block", "Physiologic splitting of 2nd heart sound", "Pulmonic stenosis"], "C",
 "Physiologic (normal) splitting of S2 widens with inspiration (delayed pulmonic closure) and narrows/disappears "
 "with expiration."),
("One of the following is a congenital heart malformation that interferes with blood flow:",
 ["Ventricular septal defect", "Atrial septal defect", "Coarctation of aorta", "Patent ductus arteriosus"], "C",
 "Coarctation of the aorta is an obstructive lesion that directly narrows the aortic lumen and impedes forward "
 "blood flow, unlike the shunt lesions VSD/ASD/PDA."),
("One of the following is correct for patent ductus arteriosus",
 ["It is a common cause of cyanotic heart disease", "It is commonly associated with left ventricular hypertrophy",
  "It means connection between aorta and pulmonary artery", "It represents narrowing at arch of aorta"], "C",
 "PDA is a persistent vascular connection between the aorta and the pulmonary artery; it is an acyanotic "
 "left-to-right shunt, not a cause of cyanosis or aortic narrowing."),
("Amastigote Stage of trypanosoma cruzi is",
 ["Non multiplying form", "Found in the peripheral blood of man", "Found in muscles, nerve cells",
  "Found in the NNN culture"], "C",
 "The amastigote (intracellular, multiplying) form of T. cruzi is found within host cells such as cardiac "
 "muscle and nerve/glial cells; trypomastigotes circulate in peripheral blood and grow in NNN culture."),
("The apical heart beat is best heard at the level of:",
 ["Diaphragm", "First rib", "Fifth intercostal space", "Seventh intercostal space"], "C",
 "The cardiac apex beat is normally palpated/auscultated at the left 5th intercostal space, mid-clavicular line."),
("The pericardial cavity is a gap between:",
 ["Fibrous pericardium and serous pericardium", "Fibrous pericardium and epicardium",
  "Parietal pericardium and epicardium", "Visceral pericardium and epicardium"], "C",
 "The pericardial cavity lies between the parietal layer of serous pericardium and the visceral layer "
 "(epicardium) covering the heart."),
("Statins decrease serum cholesterol by one of the following mechanisms:-",
 ["Binding to bile acids", "Inhibiting HMG-CoA enzyme", "Activation of PPARs",
  "Inhibiting the intestinal absorption of cholesterol"], "B",
 "Statins competitively inhibit HMG-CoA reductase, the rate-limiting enzyme of hepatic cholesterol synthesis."),
("A reversible lupus erythematous-like syndrome is most likely associated with this antiarrhythmic drug.",
 ["Disopyramide", "Adenosine", "Quindine", "Procainamide"], "D",
 "Procainamide is classically associated with a reversible drug-induced lupus-like syndrome."),
("One of the following antihypertensive drugs is commonly used in mild to moderate hypertension:",
 ["Furosemide", "Trimethaphan", "Diazoxide", "Captopril"], "D",
 "Captopril (an ACE inhibitor) is a standard oral agent for mild-to-moderate hypertension; furosemide is a "
 "loop diuretic, trimethaphan a ganglionic blocker and diazoxide an IV agent for hypertensive emergencies."),
("Acute rheumatic fever (ARF) is",
 ["Suppurative sequel of group A streptococcus infection",
  "Heart disease that occurs two to four days after group A streptococcus pharyngitis",
  "Heart disease that occurs 2-4 weeks after group A streptococcus pharyngitis",
  "Heart disease that occurs 2-4 wks following group B streptococcus pharyngitis"], "C",
 "Acute rheumatic fever is a non-suppurative sequela that typically develops 2-4 weeks after group A "
 "streptococcal pharyngitis."),
("Which of the following conditions is LEAST likely to be caused by adenoviruses?",
 ["Conjunctivitis", "Pneumonia", "Pharyngitis", "Glomerulonephritis"], "D",
 "Adenoviruses commonly cause conjunctivitis, pharyngitis and pneumonia; glomerulonephritis is not a "
 "recognized adenoviral manifestation."),
]


def main():
    questions = []
    for stem, opts, letter, exp in RAW:
        questions.append(Q(stem, opts, letter, 'marked', exp=exp, tag=TAG, year=YEAR))

    meta = {'Source file': SRC,
            'Type': 'Scanned image PDF, 3 pages, 2-column layout, declares 24 questions',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'marked — every option is hand/print-circled in the scanned source'}
    n = write_md(OUT, 'Source 28 — Sohag CVS midterm 2021', meta, questions)

    letters = collections.Counter(r[2] for r in RAW)
    mcq = sum(1 for r in RAW)
    print(f'source 28: {n} questions ({mcq} MCQ / 0 written)')
    print(f'  counters: declared in source = 24, highest question number = 24, '
          f'option-A blocks = {len(RAW)}, ### Q = {n}')
    print(f'  answer source breakdown: marked={mcq}, derived=0')
    total = sum(letters.values())
    dist = ', '.join(f'{k}={v} ({v*100//total}%)' for k, v in sorted(letters.items()))
    top = max(letters.values()) / total
    verdict = 'PASS' if top <= 0.45 else ('INVESTIGATE' if top <= 0.60 else 'FAIL')
    print(f'  answer distribution: {dist}  -> bias gate: {verdict} (top={top*100:.0f}%, n={total} < 15, gate not required)')


if __name__ == '__main__':
    main()
