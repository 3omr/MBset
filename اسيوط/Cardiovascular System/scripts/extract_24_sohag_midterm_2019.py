#!/usr/bin/env python3
"""Source 24 — OTHER EXAMS/Sohag midterm 2019.PDF.

A clean digital paper that declares its own total on page 1 ("Number of questions =96 Q"),
which is the authority the extraction is checked against.

Layout quirk that drives the parser: options are NOT one per line. The paper packs two
(sometimes four) options onto a single physical line to save space —
    a) 5%.            b) 10%            c) 20%        d) 80%
— and mixes `a)` with `a.` markers, sometimes with the space eaten (`a.Sympathetic`,
`d . Arteriolar`). So an option run is found by splitting each line on every option
marker it contains rather than by matching one marker per line.

The paper prints no answer key, so every answer is `derived`.
"""
import os, re, sys, subprocess, collections
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, clean

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system',
                   'OTHER EXAMS', 'Sohag midterm 2019.PDF')
OUT = os.path.join(MOD, 'Markdown_Questions', '24_Sohag_Midterm_2019.md')
TAG, YEAR = 'External, Sohag 2019', 2019

# Derived answer key for source 24 (Sohag CVS midterm 2019). The paper prints no key.
# Letters refer to the emitted A..E order, which follows the paper's printed order.
ANSWERS = {
 1:'A',  2:'D',  3:'B',  4:'A',  5:'D',  6:'C',  7:'A',  8:'C',  9:'D', 10:'A',
11:'B', 12:'D', 13:'A', 14:'B', 15:'D', 16:'A', 17:'C', 18:'C', 19:'D', 20:'C',
21:'B', 22:'C', 23:'B', 24:'A', 25:'C', 26:'D', 27:'C', 28:'C', 29:'C', 30:'B',
31:'C', 32:'B', 33:'D', 34:'A', 35:'B', 36:'C', 37:'C', 38:'C', 39:'A', 40:'B',
41:'D', 42:'B', 43:'D', 44:'C', 45:'D', 46:'A', 47:'D', 48:'C', 49:'A', 50:'C',
51:'C', 52:'B', 53:'B', 54:'E', 55:'B', 56:'D', 57:'D', 58:'A', 59:'B', 60:'E',
61:'C', 62:'A', 63:'A', 64:'C', 65:'C', 66:'C', 67:'A', 68:'D', 69:'A', 70:'D',
71:'C', 72:'B', 73:'C', 74:'E', 75:'A', 76:'B', 77:'D', 78:'B', 79:'C', 80:'B',
81:'C', 82:'C', 83:'D', 84:'B', 85:'D', 86:'D', 87:'A', 88:'C', 89:'D', 90:'E',
91:'D', 92:'D', 93:'B', 94:'C', 95:'C', 96:'B',
}

QNUM  = re.compile(r'^\s*(\d{1,3})\s*[-.)]\s*(\S.*)$')
# An option marker is a-h followed by ')' or '.', with stray spaces around either
# ('a.Sympathetic', 'd . Arteriolar'). Four questions late in the paper switch to an
# 'a- ' hyphen marker instead, which is accepted only when a space follows, so that
# hyphenated words inside an option are not mistaken for a new option.
# Lowercase only: this paper labels options a)-e), and allowing an uppercase 'B.' would
# split the abbreviation "arterial B.P." into a bogus option 'P' (it did, in Q15/Q17).
OPTM  = re.compile(r'(?:(?<=^)|(?<=\s))\(?([a-h])(?:\s*[.)]\s*|-\s+)(?=\S)')
# Page furniture the paper prints INSIDE the last option line of a page, plus the
# sign-off rule at the very end — both must be trimmed from the option text, not just
# dropped as whole lines.
INLINE_NOISE = re.compile(r'\s*\|?\s*P\s*a\s*g\s*e\s*\d*\s*$|'
                          r'\s*(?:best wishes|good luck)[\s-]*$|\s*-{5,}\s*$', re.I)
NOISE = re.compile(r'^(Sohag University|faculty of medicine|Number of pages|'
                   r'Number of questions|Cardiovascular mid-block exam|'
                   r'Select one best answer|time allowed|\d{1,2}/\d{1,2}/\d{4}|'
                   r'\|?\s*P\s*a\s*g\s*e\s*\d*|-{5,}|best wishes|Good luck.*|'
                   r'With my best wishes.*)\s*$', re.I)


def strip_tail_noise(text):
    """Strip page furniture and the sign-off rule off the end of an option.

    These stack — the last option on the last page picks up "best wishes", then two
    dash rules, then "| P a g e 13" — and a single re.sub pass only removes the
    outermost one, because the inner ones are no longer anchored to the end. So the
    substitution is repeated until the text stops changing.
    """
    prev = None
    while prev != text:
        prev = text
        text = INLINE_NOISE.sub('', text).rstrip()
    return text


def split_options(line):
    """Split one physical line into the option fragments it carries."""
    marks = list(OPTM.finditer(line))
    if not marks:
        return []
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(line)
        out.append((m.group(1).lower(), line[m.end():end].strip()))
    return out


def main():
    text = subprocess.run(['pdftotext', '-layout', SRC, '-'],
                          capture_output=True, text=True).stdout
    declared = re.search(r'Number of questions\s*=?\s*(\d+)', text)
    declared = int(declared.group(1)) if declared else None

    blocks, cur = [], None
    for raw in text.split('\n'):
        line = raw.strip()
        if not line or NOISE.match(line):
            continue
        m = QNUM.match(line)
        # A question number only starts a new block when what follows is not itself an
        # option run — "5%. b) 10%" must not be read as question 5.
        if m and not split_options(line[:m.start(2) + 2]):
            if cur:
                blocks.append(cur)
            cur = {'n': int(m.group(1)), 'stem': [m.group(2)], 'opts': []}
            line = ''
        if not line or cur is None:
            continue
        opts = split_options(line)
        if opts:
            for letter, txt in opts:
                if txt:
                    cur['opts'].append(txt)
        elif cur['opts']:
            cur['opts'][-1] += ' ' + line
        else:
            cur['stem'].append(line)
    if cur:
        blocks.append(cur)

    questions, dropped = [], []
    for b in blocks:
        stem = clean(strip_tail_noise(' '.join(b['stem'])))
        opts = [clean(strip_tail_noise(o)) for o in b['opts']]
        opts = [o for o in opts if o]
        if not stem or len(opts) < 2:
            dropped.append((b['n'], stem[:70] if stem else '', len(opts)))
            continue
        letter = ANSWERS.get(b['n'])
        if letter is None or letter not in 'ABCDEF'[:len(opts)]:
            dropped.append((b['n'], f'no derived answer / out of range ({letter})', len(opts)))
            continue
        questions.append(Q(stem, opts, letter, 'derived', tag=TAG, year=YEAR))

    meta = {'Source file': 'Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/Sohag midterm 2019.PDF',
            'Type': 'Digital exam paper, 13 pages, declares 96 questions',
            'Tag': TAG, 'tagSuggere': 'None', 'Year': YEAR,
            'Answer source': 'derived — the paper prints no key'}
    n = write_md(OUT, 'Source 24 — Sohag CVS midterm 2019', meta, questions)

    highest = max((b['n'] for b in blocks), default=0)
    print(f'source 24: {n} questions ({n} MCQ / 0 written)')
    print(f'  counters: declared in source = {declared}, highest question number = '
          f'{highest}, parsed blocks = {len(blocks)}, ### Q = {n}')
    if declared and n != declared:
        print(f'  [!] MISMATCH: {n} extracted vs {declared} declared')
    for r in dropped:
        print(f'  [!] Q{r[0]} dropped (opts={r[2]}): {r[1]}')


if __name__ == '__main__':
    main()
