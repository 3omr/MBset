#!/usr/bin/env python3
"""Source 21 — ASSIUT PREVIOUS EXAMS/Written Final CVS 2021.pdf.

The file is the department's printed ANSWER MODEL for the 2021-2022 CVS-206 final
("Answer Model of CVS-206 - 2021-2022 -Final exam"), so every answer here is `key`:
transcribed from the paper, not derived.

WHY THIS FILE IS TRANSCRIBED BY HAND RATHER THAN PARSED
The six pages are photographed SIDEWAYS. `tesseract --psm 6` does not auto-rotate, so the
first OCR pass returned vertically-sliced gibberish for pages 2-6 and an earlier extraction
pass wrote those five pages off as "unreadable scan" and shipped only page 1. They are not
unreadable — re-OCR'd with orientation detection (.ocr2/21_final_written_2021.txt) they are
legible, and the questions below come from that text, read against the rendered pages.

Two further properties of the scan that the counters have to account for:
  * pages 3 and 6 are duplicate photographs of the SAME page (the post-haemorrhage hormone
    list), so the page count overstates the content;
  * the model prints its questions with the department's own inconsistent numbering (1, 2A-C,
    3, then a run that restarts), so questions are renumbered continuously Q1..QN here.

Handwritten annotations over the print are stripped, never guessed at.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '21_Assiut_Final_Written_2021.md')
TAG, YEAR = 'Exams, Final 2021', 2021

# (stem, model answer as printed). All QROC — this is a written paper.
QUESTIONS = [
    ('Mention 4 complications of myocardial infarction.',
     'Ventricular arrhythmias; cardiac rupture with haemopericardium; rupture of a papillary '
     'muscle or septal rupture; ventricular mural thrombosis; systemic or pulmonary '
     'embolization; ventricular aneurysm (weeks to months post-infarct); and chronic '
     'ischaemic heart disease (months to years post-infarct).'),

    ('A 60-year-old man arrives at the emergency department complaining of pain in the left '
     'arm. Laboratory studies show an elevated troponin I level and the patient is treated '
     'for an acute myocardial infarction. A subsequent echocardiogram shows a wall motion '
     'abnormality of the posterior interventricular septum. Which occluded artery would most '
     'likely cause this condition?',
     'The posterior interventricular (posterior descending) artery.'),

    ('A 60-year-old man is treated for an acute myocardial infarction and echocardiography '
     'shows a wall motion abnormality of the posterior interventricular septum, from '
     'occlusion of the posterior interventricular artery. Describe the distribution of this '
     'artery.',
     'It gives branches to both the right and left ventricles, including the inferior wall '
     'and the posterior part of the interventricular septum. A large septal branch supplies '
     'the atrioventricular node.'),

    ('Compare the interior of the right and left ventricles (four aspects only).',
     '1. The walls of the left ventricle are about three times thicker than those of the '
     'right ventricle. 2. In cross section the left ventricle is circular while the right is '
     'crescentic, because the ventricular septum bulges into the right ventricular cavity. '
     '3. The left ventricle has two large papillary muscles (anterior and posterior); the '
     'right has three (anterior, septal and posterior). 4. The part of the left ventricle '
     'below the aortic orifice is smooth and is called the aortic vestibule, while the part '
     'of the right ventricle below the pulmonary orifice is smooth and is called the '
     'infundibulum. 5. There is no moderator band in the left ventricle, but one is present '
     'in the right.'),

    ('Define the staircase phenomenon and explain its mechanism.',
     'Definition: a stepwise increase in the strength of myocardial contraction on increasing '
     'the frequency of the heart rate; it occurs over the first few beats until a steady '
     'maximum is reached. Mechanism: Treppe is believed to be due to increased availability '
     'of calcium ions for binding to troponin C, because the stimuli fall during the '
     'supernormal phase of their predecessors.'),

    ('A 56-year-old woman arrives in the emergency department complaining of attacks of chest '
     'pain, dizziness and headache. Her blood pressure is 190/110 mmHg and she has signs of '
     'heart failure. Describe the volume reflex that controls arterial blood pressure.',
     'An increase in atrial pressure stimulates the atrial receptors, which leads to '
     'vasodilatation of the afferent arterioles and to secretion of atrial natriuretic '
     'peptide (ANP). Both promote loss of salt and water, reducing blood volume and returning '
     'arterial blood pressure towards normal.'),

    ('List the endocrine hormones released after haemorrhage, giving the role and the site of '
     'release of each.',
     'Epinephrine and norepinephrine (adrenal medulla): enhance vasoconstriction of the skin '
     'and splanchnic area, dilate the coronary arteries to help coronary blood flow, increase '
     'heart rate and improve contractility, and increase hepatic formation of fibrinogen and '
     'prothrombin, shortening the coagulation time. Aldosterone (adrenal cortex): sodium and '
     'water reabsorption by the kidney, raising blood volume and returning arterial blood '
     'pressure towards normal. Antidiuretic hormone (posterior pituitary): water reabsorption '
     'by the kidney, restoring blood volume and blood pressure. Angiotensin II. '
     'Glucocorticoids (adrenal cortex): increase resistance to stress. Erythropoietin '
     '(kidney, in response to lack of oxygen): stimulates red cell formation by the bone '
     'marrow.'),

    ('Mention the factors controlling venous pressure.',
     '1. Gravity: in the recumbent position gravity has negligible effect; on sitting or '
     'standing the blood columns become vertical, so gravity raises the pressure in veins '
     'below heart level and lowers it above, by about 0.77 mmHg per centimetre. 2. The rate '
     'of inflow of blood into the veins: arteriolar dilatation tends to raise venous pressure. '
     '3. The rate of outflow from the veins: venous pressure changes little while the heart '
     'can handle the venous return, but in right-sided heart failure blood stagnates in the '
     'veins and venous pressure rises generally; a local rise follows mechanical occlusion of '
     'a vein. 4. Venomotor tone: it raises venous pressure and antagonises venous dilatation. '
     '5. The respiratory pump: during inspiration venous return increases and venous pressure '
     'falls. 6. The skeletal muscle pump: venous pressure does not rise during muscular '
     'exercise because outflow from the veins is accelerated at the same time.'),

    ('Ali is 34 years old and takes part in a training programme. During exercise his systolic '
     'blood pressure was 145 mmHg, his diastolic blood pressure was 70 mmHg and his heart rate '
     'was 200 beats/min. What type of exercise is Ali doing (isometric or isotonic), why did '
     'his diastolic blood pressure decrease, and why does his heart rate increase (three items '
     'only)?',
     'Isotonic (dynamic) exercise. The diastolic pressure falls because of vasodilatation in '
     'the active muscles produced by excess local metabolites. The heart rate rises because '
     'of: impulses from higher centres; the Bainbridge reflex from increased venous return; '
     'the Alam-Smirk reflex; increased activity of the respiratory centre; stimulation of the '
     'chemoreceptors; the rise in body temperature; and secretion of adrenaline.'),

    ('Mention the function of the carotid sinus.',
     'It is a baroreceptor: when stimulated by a rise in arterial blood pressure it sends '
     'inhibitory impulses to the respiratory and cardiovascular centres.'),

    ('Describe the transverse portion of the intercalated disc.',
     'It is formed of fascia adherens and numerous desmosomes, which provide strong adhesion '
     'between adjacent cardiac myocytes.'),

    ('How are endothelial cells connected, and what is the functional importance of that '
     'connection?',
     'They are connected by tight junctions, which prevent the leakage of plasma proteins out '
     'of the vessel.'),
]

# Content visible on the scan but NOT recoverable well enough to ship.
EXCLUDED = [
    ('page 2', 'Only a handwritten-over fragment survives ("effect of the phases of the '
                'cardiac cycle on coronary blood flow"); the question text and its model '
                'answer are obscured by annotation. EXCLUDED - unreadable scan.'),
    ('page 5', 'A left-sided heart failure item ("This is Lt. side heart failure", two '
               'causes: ischaemic heart disease and increased afterload) whose own question '
               'stem is covered by handwriting. EXCLUDED - unreadable scan.'),
]


def main():
    qs = [Q(stem, None, '-', 'key', exp=ans, qtype='QROC', tag=TAG, year=YEAR)
          for stem, ans in QUESTIONS]
    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/Written Final CVS 2021.pdf',
            'Type': "Printed answer model, 6 photographed pages (pages 3 and 6 are duplicates)",
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'key — the file IS the department answer model'}
    n = write_md(OUT, 'Source 21 — Assiut CVS final written 2021 (answer model)', meta, qs)
    print(f'source 21: {n} questions (0 MCQ / {n} written)')
    print(f'  counters: distinct question items on the 5 unique pages = {n + len(EXCLUDED)}, '
          f'printed answer blocks = {n}, ### Q headings = {n}')
    print(f"  answer sources: {{'key': {n}}}")
    print(f'  derived: 0')
    for where, why in EXCLUDED:
        print(f'  [!] {where}: {why}')


if __name__ == '__main__':
    main()
