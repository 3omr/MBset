#!/usr/bin/env python3
"""Source 14 — GD/Micro GD cases CVS block 2023 student.pptx.

A 15-slide student deck of microbiology group-discussion cases on infective
endocarditis / rheumatic fever. Read directly from the slide XML (zipfile +
regex over <a:r>/<a:rPr>/<a:t> runs) instead of converting to PDF, because a
PDF render would flatten bold formatting that could mark a correct answer —
see scripts/extract_36_physio_slide_mcqs.py for the same technique on another
deck in this module.

Slide inventory: slide 1 is a title slide, slide 2 is an "are you ready?"
filler image, slide 15 is a "thanks" filler image — none carry question
content and are excluded. Slides 3-14 hold 7 clinical-vignette cases with 12
MCQs total (1-3 sub-questions per case; the vignette is prepended to every
sub-question stem, matching the GD-case convention used elsewhere in this
module).

Bold-run check: every slide bolds only the "Case N:" label and the question
stem — never an answer option — and no run anywhere in the deck carries
<a:highlight>. So no option is marked as correct anywhere in the source;
every answer here is `derived` from medical knowledge, not `marked`.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '14_GD_Micro_Cases_2023.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/Micro GD cases CVS block 2023 student.pptx'
TAG = 'Department, GDs, Microbiology GD 1 2023'
SUBJ = 'Microbiology'
YEAR = 2023

V1 = ("A 20-year-old man presented with painful swelling in his feet, knees and "
      "right wrist 14 days after a throat infection. His ESR was 108 mm/hr, CRP "
      "336 mg/ml. Antistreptolysin O titers were raised at > 800 units/ml, anti "
      "DNAse B 3840 units/ml. Throat swab showed scanty candida only.")

V2 = ("A 32-year-old female with history of congenital mitral valve prolapse has "
      "been experiencing fever and shortness of breath. She recently had a tooth "
      "extraction. Physical examination revealed a new murmur at the heart which "
      "was not present before.")

V3 = ("A 55-year-old patient presented with acute onset of high-grade fever and "
      "signs of heart failure. On examination a heart murmur was heard. He had a "
      "history of colorectal cancer that was removed by surgery followed by "
      "chemotherapy.")

V4 = ("A 16-year-old female was hospitalized after experiencing malaise; a new "
      "erythematous, raised rash on thighs. Directly preceding this, she had a "
      "2-week history of headache, fever, and sore throat.")

V5 = ("A 28-year-old patient presented with acute onset of severe high-grade fever "
      "and signs of heart failure. On examination a heart murmur was heard which "
      "was not present before as well as the presence of periodontal infection. "
      "His arms showed needle marks of IV drug users.")

V6 = ("A 26-year-old female presented to her village clinic with cough, fever, "
      "and sore throat. She was found to have a prominent cardiac murmur and "
      "cardiomegaly on chest X-ray. An echocardiogram showed severe mitral "
      "insufficiency, and moderate aortic regurgitation. An ASO titer was "
      "elevated.")

V7 = ("A 16-year-old female was hospitalized after experiencing malaise; a new "
      "erythematous, raised rash on thighs. Directly preceding this, she had a "
      "2-week history of headache, fever, and sore throat. Nine days later she "
      "was readmitted with acute onset of right knee pain, generalized malaise, "
      "and persistent rash. Her CRP and ESR were elevated. Echocardiography "
      "revealed polyvalvular disease.")

def v(vignette, stem):
    return f'{vignette} {stem}'

QUESTIONS = [
    # Case 1 (slides 3-4) — acute rheumatic fever
    (v(V1, "This patient is at increased risk for which of the following cardiac "
           "condition?"),
     ['Hemorrhagic pericarditis', 'Infective endocarditis', 'Mitral valve prolapse',
      'Myocardial fibrosis', 'Rheumatic heart disease'], 'E',
     'The migratory polyarthritis, very high ESR/CRP and a strongly raised ASO/anti-'
     'DNAse B titer 2 weeks after a throat infection indicate acute rheumatic fever; '
     'its long-term cardiac risk is chronic rheumatic heart disease from recurrent '
     'valvulitis (especially mitral).'),

    (v(V1, "Which microorganism may lead to this disease?"),
     ['Catalase-negative, alpha-hemolytic, and bile resistant',
      'Catalase-negative, alpha-hemolytic, and bile soluble',
      'Catalase-negative, beta-hemolytic',
      'Catalase-negative, bile resistant, group D carbohydrate-positive',
      'Catalase-positive and beta-hemolytic'], 'C',
     'Acute rheumatic fever follows pharyngitis with group A beta-hemolytic '
     'Streptococcus pyogenes, which is catalase-negative and beta-hemolytic — '
     'distinguishing it from the alpha-hemolytic viridans/pneumococcal group and '
     'from catalase-positive staphylococci.'),

    # Case 2 (slides 5-6) — subacute bacterial endocarditis after dental work
    (v(V2, "Which of the following is most likely responsible for the patient's "
           "current condition?"),
     ['Catalase-negative, alpha-hemolytic, and bile resistant',
      'Catalase-negative, alpha-hemolytic, and bile soluble',
      'Catalase-negative, beta-hemolytic',
      'Catalase-negative, bile resistant, group D carbohydrate-positive',
      'Catalase-positive and beta-hemolytic'], 'A',
     'Endocarditis on a previously abnormal valve (mitral valve prolapse) following '
     'a dental procedure is classically caused by viridans streptococci — '
     'catalase-negative, alpha-hemolytic, and bile resistant (unlike bile-soluble '
     'Streptococcus pneumoniae).'),

    (v(V2, "What is the course of the disease?"),
     ['Acute', 'Chronic', 'Late-onset', 'Subacute'], 'D',
     'Viridans streptococcal endocarditis on an already-damaged valve typically has '
     'an indolent, subacute course over weeks, unlike the fulminant course of '
     'acute (e.g. staphylococcal) endocarditis.'),

    # Case 3 (slide 7) — Streptococcus gallolyticus (bovis) endocarditis with
    # colorectal cancer
    (v(V3, "What is the most probable causative microorganism?"),
     ['Gram-negative rod', 'Gram-positive, catalase-negative cocci',
      'Gram-positive, catalase-negative, optochin-resistant cocci',
      'Gram-positive, catalase-positive cocci', 'Gram-positive yeast'], 'C',
     'Endocarditis associated with colorectal malignancy is classically caused by '
     'Streptococcus gallolyticus (bovis), a group D streptococcus that is '
     'gram-positive, catalase-negative and optochin-resistant, distinguishing it '
     'from optochin-sensitive Streptococcus pneumoniae.'),

    # Case 4 (slide 8) — acute rheumatic fever, evidence of prior GAS
    (v(V4, "Prior infection with GAS can be demonstrated in patients with acute "
           "rheumatic fever by which one of the following?"),
     ['Blood culture', 'Skin culture', 'Culture of a heart valve in a patient with '
      'carditis.', 'A high titer of antibody against the hyaluronic acid capsule',
      'A high titer of antibody against streptolysin O'], 'E',
     'By the time rheumatic fever manifests, the throat infection has usually '
     'cleared, so cultures are typically negative; serologic evidence of recent '
     'group A streptococcal infection — a rising or high antistreptolysin O (ASO) '
     'titer — is the standard way to document the antecedent infection.'),

    # Case 5 (slides 9-11) — acute (staphylococcal) endocarditis, IV drug use
    (v(V5, "What is the most probable causative organism?"),
     ['Gram-positive, catalase-negative cocci, optochin-sensitive cocci',
      'Gram-positive, catalase-negative, optochin-resistant cocci',
      'Gram-negative rods', 'Gram-positive, catalase-positive cocci',
      'Gram-positive yeast'], 'D',
     'Acute, aggressive endocarditis in an intravenous drug user is classically '
     'caused by Staphylococcus aureus, a gram-positive, catalase-positive coccus.'),

    (v(V5, "What is the best diagnostic test?"),
     ['Antistreptolysin O test', 'Throat culture',
      'Culture of blood sample on blood agar', 'Blood culture'], 'D',
     'Blood culture (ideally 2-3 sets before antibiotics) is the cornerstone '
     'investigation for infective endocarditis and a major Duke criterion.'),

    (v(V5, "What is alternative test in case of failure of routine testing?"),
     ['Antistreptolysin O test', 'PCR', 'Antibiotic Susceptibility test',
      'Culture of blood sample on blood agar'], 'B',
     'When standard blood cultures are negative (culture-negative endocarditis, '
     'e.g. after prior antibiotics or fastidious organisms), PCR-based molecular '
     'detection of pathogen DNA from blood or excised valve tissue is the '
     'recommended alternative.'),

    # Case 6 (slides 12-13) — rheumatic carditis
    (v(V6, "The pathogenesis of this disease is based on production of antibodies "
           "against which of the following structures?"),
     ['Actin of heart muscle', 'Streptolysin O toxin of Streptococcus pyogenes',
      'M protein of Streptococcus viridans', 'M protein of Streptococcus pyogenes',
      'Capsule of Streptococcus pyogenes'], 'D',
     'Rheumatic fever/carditis is a type II hypersensitivity reaction: antibodies '
     'raised against the M protein of Streptococcus pyogenes cross-react (molecular '
     'mimicry) with cardiac myosin and valve glycoproteins, producing carditis.'),

    (v(V6, "The value of Rapid Antigen Detection test in diagnosis of Rheumatic "
           "fever is:"),
     ['Positive result rules out diagnosis of the disease',
      'Positive result confirms diagnosis of the disease',
      'Negative result rules out diagnosis of the disease',
      'Negative result confirms diagnosis of the disease'], 'B',
     'The rapid antigen detection test (RADT) for group A Streptococcus has high '
     'specificity but only moderate sensitivity: a positive result is essentially '
     'confirmatory of current/recent GAS infection, whereas a negative result does '
     'not reliably exclude it (false negatives are common).'),

    # Case 7 (slide 14) — recurrent rheumatic fever
    (v(V7, "What is the best diagnostic test?"),
     ['Throat culture', 'Antistreptolysin O test', 'Blood culture',
      'Tube agglutination test'], 'B',
     'By the time polyarthritis/carditis recurs, the throat infection has usually '
     'resolved and cultures are often negative; a raised antistreptolysin O (ASO) '
     'titer is the standard serologic evidence of antecedent GAS infection used to '
     'support the Jones criteria.'),
]


def main():
    qs = [Q(stem, opts, correct, 'derived', exp=exp, tag=TAG, tag_suggere=SUBJ,
             year=YEAR)
          for stem, opts, correct, exp in QUESTIONS]
    meta = {'Source file': SRC,
            'Type': 'PowerPoint, 15 slides (1 title + 2 filler images excluded); '
                    '7 clinical-vignette GD cases, 12 MCQs',
            'Tag': TAG, 'tagSuggere': SUBJ, 'Year': YEAR,
            'Answer source': 'derived — no run in the slide XML bolds or highlights '
                              'an option, so no option is marked correct anywhere'}
    n = write_md(OUT, 'Source 14 — GD Microbiology Cases (CVS block, 2023)', meta, qs)

    ans = collections.Counter(q.correct for q in qs)
    total = sum(ans.values())
    max_share = max(ans.values()) / total if total else 0
    print(f'source 14: {n} questions ({n} MCQ / 0 written), 7 cases')
    print(f'  counters: content slides = 12 (slides 3-14; slide 1 title, slides 2 '
          f'and 15 filler images excluded), option-A blocks = 12, ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} '
          f'(n={total}, max share={max_share:.1%}; <15 MCQs, bias gate n/a)')
    print(f'  derived: {n} (all)')


if __name__ == '__main__':
    main()
