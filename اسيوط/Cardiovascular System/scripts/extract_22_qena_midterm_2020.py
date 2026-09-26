#!/usr/bin/env python3
"""Source 22 — OTHER EXAMS/Qena cvs midterm 2020 (answered).pdf.

A scanned (CamScanner) image-only PDF, 7 pages of questions (48 MCQs total, as
declared on page 1: "48 سؤال اختيار من متعدد") plus 2 pages (8-9) of a
handwritten answer key ("1-D", "2-A", ... "48-D") written by the student who
scanned the paper.

pdftotext returns ~1 char/page (image-only) and tesseract OCR on the question
pages is noisy enough (crooked photo, wood-grain background, stray marks) to
mis-read question numbers and even scramble whole lines on page 3. Because the
paper is small (48 Qs) and the layout is clean one-option-per-line printed
text, the questions below were transcribed by reading the rendered page PNGs
directly (300 dpi) rather than trusting a regex over OCR text — see the
extraction report for this source.

The handwritten key on pages 8-9 is a dedicated answer list (not a mark on the
question itself), so provenance is 'key'. A few entries in the key have a
crossed-out letter replaced by another (e.g. "39- ~~D~~ C"); the surviving
(uncrossed) letter is used. Spot-checked against known pharmacology facts
(Q1 Class IA = Quinidine = D, Q2 first-line PSVT = Adenosine = A, Q26 LV wall
3x RV wall = E) — all match the transcribed key.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/'
       'Qena cvs midterm 2020 (answered) .pdf')
OUT = os.path.join(MOD, 'Markdown_Questions', '22_Qena_Midterm_2020.md')
TAG, YEAR = 'External, Qena 2020', 2020

# (stem, [options]) in paper order, 1-indexed via enumerate below.
RAW = [
("Which one of the followings is a Class IA antiarrhythmic drug?",
 ["Sotalol.", "Lidocaine.", "Verapamil.", "Quinidine."]),
("Which one of the followings is the first drug of choice for the treatment of "
 "paroxysmal supraventricular tachycardia?",
 ["Adenosine.", "Amrinone.", "Lidocaine.", "Esmolol."]),
("One of the following vasodilator drugs releases NO in vascular smooth muscles:",
 ["Nifedipine.", "Hydralazine.", "Minoxidil.", "Sodium nitroprusside."]),
("Indicate the drug that is useful in terminating ventricular but not atrial tachycardias:",
 ["Verapamil.", "Lidocaine.", "Sotalol.", "Digoxin."]),
("The drug of choice in treatment of hypertension with pregnancy is:",
 ["Captopril.", "Atenolol.", "α-methyl dopa.", "Gynecomastia."]),
("The drug of choice in treatment of hypertension with BPH:",
 ["Verapamil.", "Prazosin.", "Enalapril.", "Propanolol."]),
("Hydralazine (a vasodilator) can produce:",
 ["Seizures, extrapyramidal disturbances.", "Tachycardia, lupus erythromatosis.",
  "Acute hepatitis.", "Aplastic anemia."]),
("Vegetation that can be complicated by pyemic abscess is:",
 ["Due to acute bacterial endocarditis.", "Due to sub-acute bacterial endocarditis.",
  "Due to rheumatic endocarditis.", "Due to systemic lupus erythromatosis."]),
("Rheumatic chorea is characterized by:",
 ["Slow and rapid", "Rapid and involuntary", "Rapid and voluntary", "Slow and voluntary"]),
("Which of the following is a clinical presentation of aortic stenosis?",
 ["Hypotension and syncopial attacks.", "Diastolic murmur.", "Cyanosis.", "Hypertension"]),
("In atheroma cholesterol crystal are found:",
 ["In macrophages and polymorphs", "In smooth muscle cells and macrophages",
  "Free in tissues and in macrophages",
  "Free in tissues, in macrophages and in smooth muscles."]),
("In benign hypertension, the arterial wall shows:",
 ["fibrinoid necrosis", "Concentric hyperplasia", "Hyalinosis only", "Hyalinosis and elastosis"]),
("Prinzmetal angina is:",
 ["Severe form of angina and caused by coronary artery spasm",
  "Severe form of angina and caused by coronary emboli",
  "Mild form of angina and caused by atherosclerosis",
  "Mild form of angina and caused by coronary emboli"]),
("The most important complication of varicose veins is:",
 ["Oedema.", "Thrombosis and embolism.", "Haemorrhage.", "Trophic skin changes."]),
("The most abundant tissue element forming the media of small, muscular arteries is:",
 ["cardiac muscle.", "smooth muscle.", "collagen fibers.", "elastic fibers."]),
("Purkinje fibers:",
 ["generate electrical impulses.", "conduct electrical impulses through the myocardium.",
  "synchronize the heartbeat.", "are found along the innermost layer of the myocardium.",
  "all of the above"]),
("Thick, collagenous rings located at the sites of origin of large vessels and valves "
 "of the heart are referred to as:",
 ["the fibrous skeleton of the heart.", "the sino-atrial nodes.", "intercalated discs.",
  "cusps of the valves.", "none of the above"]),
("Heart valves normally consist of an endothelial surface covering:",
 ["cardiac muscle fibers.", "hyaline cartilage.", "loose areolar connective tissue.",
  "fibrocollagenous and fibroelastic connective tissue.", "adipose connective tissue."]),
("Vasa vasorum are:",
 ["blood vessels of the myocardium.", "nerves that supply the blood vessels.",
  "nerves of the heart.", "blood vessels within the walls of the blood vessels."]),
("One of the following is a feature of the right atrium:",
 ["Infundibulum", "Limbus fossa ovalis", "Septal papillary muscles",
  "Septomarginal trabeculae", "Trabeculae carnae"]),
("The coronary sinus develops from:",
 ["Absorbed pulmonary veins", "Left half of common atrium", "Left horn of sinus venosus",
  "Right half of common atrium", "Right horn of sinus venosus"]),
("The coronary sulcus separates the:",
 ["Two atria", "Two ventricles", "Atria & the ventricles", "SVC & IVC", "Apex & the base"]),
("One of the following vessels is NOT directly attach to the heart:",
 ["Arch of aorta", "Inferior vena cava.", "Pulmonary trunk", "Pulmonary veins",
  "Superior vena cava"]),
("Cusps of the pulmonary valve are:",
 ["Anterior & posterior", "Anterior, posterior & septal",
  "Anterior, posterior right & posterior left", "Posterior, anterior right & anterior left",
  "Medial, lateral & anterior."]),
("Posterior mediastinum contains all the following, EXCEPT:",
 ["Azygos vein", "Descending thoracic aorta", "Esophagus", "Trachea", "Vagus nerve."]),
("The wall of the left ventricle is 3 times thicker than the wall of:",
 ["Coronary sinus.", "Coronary artery.", "Left atrium.", "Right atrium.", "Right ventricle"]),
("About the changes in cardiac excitability, in which phase the heart cannot be stimulated:",
 ["Negative after potential.", "Relative refractory period.", "Absolute refractory period.",
  "Supernormal phase of excitability."]),
("During relative refractory period:",
 ["The heart can be stimulated by strong stimulus", "The heart respond maximally to weak stimulus.",
  "It corresponds to the depolarization period.", "The heart can be stimulated by a weak stimulus."]),
("The atrioventricular node cells:",
 ["Found in the left atria.", "Generate impulses at lower rate than SAN.",
  "Connected to the S-N node by the A-V bundle.",
  "Able to generate impulses because their membrane potential is stable."]),
("Pacemaker cardiac cells differ from other cardiac cells in:",
 ["Require an external stimulus in order to reach threshold.",
  "Reach threshold with much weaker stimuli than other cardiac cells.",
  "Its resting membrane potential is -85 mv.",
  "Do not require an external stimulus to reach the firing threshold."]),
("Starling's law of the heart states the relation between the strength of contraction and:",
 ["The end systolic volume.", "The heart rate.", "The end diastolic volume.",
  "The aortic pressure."]),
("Concerning the differences between skeletal and cardiac muscle?",
 ["The heart has a relatively smaller T-tubule volume.",
  "The heart has a well-developed sarcoplasmic reticulum.",
  "The heart depends more on extracellular Ca²⁺ stores than skeletal muscle.",
  "The T tubules of the heart store smaller quantities of calcium ions."]),
("The strength of the ventricular muscle decreases when there is a rise in:",
 ["Serum potassium.", "Serum calcium.", "Serum adrenaline.", "Serum pH"]),
("In atrial flutter the electrocardiogram shows:",
 ["Low QRS rate and irregular P waves.", "High QRS rate and regular P waves.",
  "Regular P waves and irregular QRS complexes.",
  "Irregular P waves and irregular QRS complexes."]),
("In atrial Fibrillation:",
 ["The electrocardiogram shows absent P waves.", "The QRS rate is high and irregular.",
  "The QRS rate is higher than P wave rate.", "The QRS complexes have an abnormal configuration."]),
("A complete heart block is recognized in ECG by:",
 ["Prolonged P-R interval.", "Prolonged QRS complex.",
  "Dissociation between P waves and QRS waves.", "Inverted P waves."]),
("Ventricular extrasystole is recognized in ECG by:",
 ["Raised S-T segment.", "Prolonged QRS complex.", "Inverted P wave.",
  "Prolonged P-R interval."]),
("During isovolumetric relaxation phase:",
 ["All ventricular valves are closed.", "Pressure in the atria falls.",
  "Pressure in the aorta rises.", "Pressure in both ventricles rises"]),
("Ventricular filling:",
 ["Occurs during ventricular systole.", "Occurs during isovolumetric contraction phase.",
  "Occurs during ventricular diastole", "Occurs during isovolumeric relaxation phase."]),
("The pulmonary valve is opened during:",
 ["Atrial systole.", "Isovolumetric contraction phase.", "Isovolumetric relaxation phase.",
  "Ventricular ejection phases."]),
("Diacrotic notch is due to:",
 ["Sudden closure of AV valves.", "Sudden closure of aortic valve.",
  "Sudden increase in aortic pressure.", "Marked decrease in ventricular pressure."]),
("A wave in jugular venous pulse occurs in:",
 ["Isometric contraction phase.", "Isometric relaxation phase.", "Maximum ejection phase.",
  "Atrial systole phase."]),
("The first heart sound differs from the second heart sound in that it is:",
 ["Heard during isovolumetric relaxation phase.", "Short lasting than second sound.",
  "Heard during isovolumetric contraction phase.", "It is an audible sound."]),
("The heart accelerates during inspiration due to:",
 ["Signals from lung stretch receptors stimulate CIC",
  "Signals from lung stretch receptors inhibit CIC",
  "Signals from right atrium stimulate CIC",
  "Signals from inspiratory centers stimulate CIC"]),
("Stimulation of CIC leads to decrease heart rate in all the following EXCEPT:",
 ["Mild pain", "Heavy blows", "Oculo-cardiac reflex", "Cushing reflex."]),
("Administration of moderated amount of blood will:",
 ["decrease the venous return and COP",
  "increase venous return and COP that continue higher even after 50 minutes.",
  "increase the capillary pressure and fluid transduction into the tissues.",
  "Constrict the veins passively."]),
("A female patient complained of severe headache and her blood pressure was 180/100 mmHg, "
 "she diagnosed as a hypertensive patient for the first time but with healthy normal heart:",
 ["Her stroke volume increases but COP decreases", "Her stroke volume and COP are increased",
  "Her stroke volume and COP are not change significantly due to compensatory mechanisms of the heart.",
  "Her stroke volume decreased but COP increased."]),
("Causes of right side failure",
 ["pulmonary disease", "Ischemia", "Hypertension", "all of above"]),
]

# Handwritten answer key transcribed from pages 8-9 (questions 1-48). Where the
# student crossed a letter out and wrote another, the surviving letter is used
# (Q39: crossed D, kept C).
KEY = ['D','A','D','B','C','B','B','A','B','A',
       'B','D','A','B','B','E','A','D','D','B',
       'C','C','A','D','D','E','C','A','B','D',
       'C','C','A','A','A','C','B','A','C','D',
       'D','D','C','B','A','C','C','D']


def main():
    assert len(RAW) == 48 == len(KEY)
    questions = []
    for i, ((stem, opts), letter) in enumerate(zip(RAW, KEY), 1):
        assert letter in 'ABCDE'[:len(opts)], f'Q{i} answer {letter} out of range'
        questions.append(Q(stem, opts, letter, 'key', tag=TAG, year=YEAR))

    meta = {'Source file': f'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/'
                            f'Qena cvs midterm 2020 (answered) .pdf',
            'Type': 'Scanned exam paper (CamScanner), 9 pages: 7 pages of questions '
                    '(48 MCQ) + 2 pages of handwritten answer key',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'key — handwritten answer list on pages 8-9 of the scan'}
    n = write_md(OUT, 'Source 22 — Qena CVS midterm 2020', meta, questions)

    src_counter = collections.Counter(q.source for q in questions)
    letter_counter = collections.Counter(q.correct for q in questions)
    print(f'source 22: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: declared in source = 48, highest question number = 48, '
          f'parsed blocks = {len(RAW)}, ### Q = {n}')
    print(f'  answer source: {dict(src_counter)}')
    print(f'  answer letters: {dict(sorted(letter_counter.items()))}')
    top = max(letter_counter.values()) / sum(letter_counter.values()) * 100
    print(f'  top letter share: {top:.1f}%' + (' <== BIAS FAIL' if top > 45 else ''))


if __name__ == '__main__':
    main()
