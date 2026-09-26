#!/usr/bin/env python3
"""Source 05 — parasitology department.pdf.

Despite the filename this is not a printed bank: it is another Moodle quiz review
export (Lecture 17, Quiz 17 — Cardiac Involvement with Parasitic Infections), the
same format as source 01, so the source-01 parser is reused rather than duplicated.
Moodle prints 'The correct answer is: ...' under each question, so provenance is `key`.
"""
import os, re, sys, collections, fitz
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, match_correct
from extract_01_quizzes import harvest, parse, quiz_at, TAIL

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system',
                   'parasitology department.pdf')
OUT = os.path.join(MOD, 'Markdown_Questions', '05_Parasitology_Department_Bank.md')
TAG = 'Department, QBank, Parasitology'


def main():
    doc = fitz.open(SRC)
    markers, content, headers = harvest(doc)
    bounds = [(m[0], m[1]) for m in markers] + [(10 ** 6, 0)]

    questions, no_key, dropped = [], [], []
    for i, (pno, y0, num) in enumerate(markers):
        chunk = [t for (bp, by, t) in content if (pno, y0 - 6) <= (bp, by) < bounds[i + 1]]
        stem, options, answer, _tf = parse(chunk)
        options = [TAIL.sub('', o).strip() for o in options]
        if not stem:
            dropped.append((num, 'empty stem', '', 0))
            continue
        if answer is None:
            no_key.append((num, stem[:70], len(options)))
            continue
        if not options:
            questions.append(Q(stem, None, '-', 'key', exp=answer, qtype='QROC',
                               tag=TAG, tag_suggere='Parasitology'))
            continue
        if len(options) < 2:
            dropped.append((num, 'single option', stem[:70], len(options)))
            continue
        letter = match_correct(answer, options)
        if letter is None:
            dropped.append((num, f'unmatched {answer[:40]!r}', stem[:70], len(options)))
            continue
        questions.append(Q(stem, options, letter, 'key', tag=TAG,
                           tag_suggere='Parasitology'))

    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/parasitology department.pdf',
            'Type': 'Moodle quiz review export (Lecture 17 / Quiz 17), 15 pages',
            'Tag': TAG, 'tagSuggere': 'Parasitology', 'Year': 'None',
            'Answer source': 'key — Moodle prints the correct answer under each question'}
    n = write_md(OUT, 'Source 05 — Parasitology department bank (Moodle)', meta, questions)

    raw = '\n'.join(p.get_text() for p in doc)
    keys = len(re.findall(r'The correct answers? (?:is|are)', raw))
    ans = collections.Counter(q.correct for q in questions if q.type == 'QCS')
    mcq = sum(ans.values())
    top = max(ans.values()) / mcq * 100 if ans else 0
    print(f'source 05: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: Question markers = {len(markers)}, printed keys = {keys}, '
          f'### Q = {n}')
    print(f"  answer sources: {{'key': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))}, top={top:.0f}% '
          f'({"PASS" if mcq < 15 or top <= 45 else "FAIL"})')
    print('  derived: 0')
    for r in no_key:
        print(f'  [!] Q{r[0]} has no printed key and was skipped: {r[1]}')
    for r in dropped:
        print(f'  [!] Q{r[0]} dropped: {r[1]}')


if __name__ == '__main__':
    main()
