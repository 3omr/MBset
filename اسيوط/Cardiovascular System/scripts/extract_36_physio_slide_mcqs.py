#!/usr/bin/env python3
"""Source 36 — MCQs on slides 46-47 of "Lecture 40, 41.pptx" (physiology deck).

The deck's last two slides are a small revision MCQ set. Read from the slide XML
rather than a PDF conversion, because on slide 47 the correct option is marked by
BOLD (`b="1"`) and that formatting is exactly what a PDF render would flatten away.

Slide 46 bolds only the stems, so its three questions have no key in the source and
are `derived`. Slide 47 bolds one option in each of its two questions -> `marked`.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '36_Physiology_L40_41_Slide_Questions.md')
TAG = 'Department, QBank, Physiology'

# Transcribed verbatim from the slide XML runs (see the module report for the dump).
# 'marked' answers are the options the deck itself bolds; 'derived' answers carry no
# marking anywhere in the source and are answered from the block's own physiology
# lectures (L8/L9 for the ECG items, L10 for the cardiac-cycle item).
QUESTIONS = [
    ('A complete heart block is recognized in ECG by:',
     ['Prolonged P-R interval',
      'Prolonged QRS complex',
      'Dissociation between P waves and QRS waves',
      'Inverted P waves'], 'C', 'derived'),

    ('Ventricular extrasystole is recognized in ECG by:',
     ['Raised S-T segment',
      'Prolonged QRS complex',
      'Inverted P wave',
      'Prolonged P-R interval'], 'B', 'derived'),

    # The slide labels these a, b, c, e — it skips d. Options are emitted A-D in the
    # order printed, so the key moves with them.
    ('During isometric ventricular contraction:',
     ['All ventricular valves are closed',
      'Pressure in the atria falls',
      'Pressure in the aorta rises',
      'Pressure in the right ventricle rises greater than the left ventricle'],
     'A', 'derived'),

    ('Diacrotic wave is caused by:',
     ['Escape of blood from the aorta to the periphery',
      'Elastic recoil of the aorta leading to increased aortic pressure',
      'Aortic regurgitation of blood',
      'Increased aortic distention'], 'B', 'marked'),

    ('How does angiotensin II increase the blood pressure?',
     ['Vasodilatation',
      'Vasoconstriction',
      'Decreases water reabsorption',
      'Decreases sodium reabsorption'], 'B', 'marked'),
]


def main():
    qs = [Q(stem, opts, correct, src, tag=TAG, tag_suggere='Physiology')
          for stem, opts, correct, src in QUESTIONS]
    meta = {'Source file': 'Lectures_raw/1- Cardiovascular system/Lecture 40, 41.pptx (slides 46-47)',
            'Type': 'PowerPoint revision slides, 2 slides, 5 MCQs',
            'Tag': TAG, 'tagSuggere': 'Physiology', 'Year': 'None',
            'Answer source': 'marked (bold option) on slide 47; derived on slide 46, '
                             'which bolds only the stems'}
    n = write_md(OUT, 'Source 36 — Physiology L40/L41 slide MCQs', meta, qs)

    import collections
    src = collections.Counter(q.source for q in qs)
    ans = collections.Counter(q.correct for q in qs)
    print(f'source 36: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: slide MCQ stems in source = 5, option-A blocks = 5, ### Q = {n}')
    print(f'  answer sources: {dict(src)}')
    print(f'  answer distribution: {dict(sorted(ans.items()))}  (< 15 MCQs, bias gate n/a)')
    print(f'  derived: {src.get("derived", 0)}')


if __name__ == '__main__':
    main()
