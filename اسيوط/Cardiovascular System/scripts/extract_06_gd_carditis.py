#!/usr/bin/env python3
"""Source 06 — GD/1- Carditis.pdf.

Mostly a pathology reading handout on carditis (Prof. Mahmoud Farouk Sherif); the
question content is the short "CASES:" section at the end, which holds two MCQs.
No key is printed anywhere in the file, so both answers are `derived` and explained.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '06_GD_Carditis.md')
TAG = 'Department, GDs, Pathology GD 1'

QUESTIONS = [
    ('A 6-year-old boy develops fever, joint pain, and a diffuse skin rash approximately '
     '3 weeks after recovering from sore throat. Physical examination finds several small '
     'skin nodules, and laboratory examination finds an elevated erythrocyte sedimentation '
     'rate along with an elevated antistreptolysin O titer. Which of the following '
     'abnormalities is most characteristic of this disease?',
     ['Anitschkow cells within the epidermis',
      'Aschoff bodies within the myocardium',
      'Langhans giant cells within the dermis',
      'Psammoma bodies within the endocardium',
      'Virchow cells within the nasopharynx'],
     'B',
     'The picture is acute rheumatic fever following streptococcal pharyngitis. Its '
     'pathognomonic lesion is the Aschoff body in the myocardium — a focus of fibrinoid '
     'necrosis surrounded by lymphocytes, plasma cells and plump activated macrophages '
     '(Anitschkow cells, which lie in the myocardium, not the epidermis).'),

    ('Which of the following types of infection precedes, by several weeks, the '
     'development of acute rheumatic fever?',
     ['Group A beta-hemolytic streptococcal infection of the pharynx',
      'Group D alpha-hemolytic streptococcal infection of the heart',
      'Staphylococcus aureus infection of the lung',
      'Streptococcus pyogenes infection of the skin',
      'Treponema pallidum infection of the abdominal aorta'],
     'A',
     'Acute rheumatic fever follows pharyngitis with group A beta-hemolytic streptococci '
     '(Streptococcus pyogenes) by 1-5 weeks. It is a type II hypersensitivity: antibodies '
     'against streptococcal M protein cross-react with cardiac antigens. Streptococcal '
     'skin infection causes post-streptococcal glomerulonephritis, not rheumatic fever.'),
]


def main():
    qs = [Q(stem, opts, correct, 'derived', exp=exp, tag=TAG, tag_suggere='Pathology')
          for stem, opts, correct, exp in QUESTIONS]
    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/GD/1- Carditis.pdf',
            'Type': 'Pathology reading handout, 7 pages; questions in the "CASES:" section',
            'Tag': TAG, 'tagSuggere': 'Pathology', 'Year': 'None',
            'Answer source': 'derived — the handout prints no key'}
    n = write_md(OUT, 'Source 06 — GD Carditis cases', meta, qs)
    ans = collections.Counter(q.correct for q in qs)
    print(f'source 06: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: MCQ stems in the CASES section = 2, option-A blocks = 2, ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({n} MCQs — bias gate n/a)')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
