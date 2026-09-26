#!/usr/bin/env python3
"""Source 01 — All Quizzes CVS.pdf (Moodle review export, 138 pages, 36 quizzes).

Three shapes appear in this one export and all three are handled:
  * MCQ            — 'a. text' options, key printed as 'The correct answer is: <text>'
  * true / false   — bare 'True'/'False' options, key as "The correct answer is 'True'."
  * fill-in-blank  — no options, an 'Answer:' placeholder, key as 'The correct answer
                     is: <text>'; emitted as QROC.
Parsing is block-based rather than line-based because Moodle wraps long options as
'a.\\n<text>' inside a single block, and the file mixes two page layouts, so blocks
are classified by their text and never by an x threshold.
Quizzes the student left unanswered print no key; those questions are reported and
skipped rather than guessed.
"""
import os, re, sys, fitz
sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md, match_correct

MOD = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system', 'All Quizzes CVS.pdf')
OUT = os.path.join(MOD, 'Markdown_Questions', '01_All_Quizzes_CVS.md')

QMARK  = re.compile(r'^Question\s+(\d+)$')
GUTTER = re.compile(r'^(Not yet answered|Not answered|Correct|Incorrect|Partially correct|'
                    r'Marked out of [\d.]+|Mark [\d.]+ out of|[\d.]+)$')
HEADER = re.compile(r'Lecture\s*([0-9][0-9 andAND\-–]*?)\s*:\s*(.*?)\s*Quiz\s*([0-9&\-– ]+)', re.S)
OPT_IN = re.compile(r'^([a-h])\.\s+(\S.*)$', re.S)
OPT_HD = re.compile(r'^([a-h])\.\s*$')
ANS_TF = re.compile(r"^The correct answer is '(True|False)'\.?$")
ANS    = re.compile(r'^The correct answers? (?:is|are):\s*(.*)$', re.S)
NOISE  = re.compile(r'^(Select one:?|Answer:|Flag question|Clear my choice|Your answer is .*|'
                    r'Lorem Ipsum.*|Quick Links|About Us|Terms of use|FAQ|Support|Contact|ll|'
                    r'type and tronic.*|Started on.*|State.*|Finished|Completed on.*|Time taken.*|'
                    r'Marks.*|Grade.*|Home.*My courses.*|[\d.]+/[\d.]+|'
                    r'[\d.]+ out of [\d.]+ \([\d.]+%\)|Quizzes Week.*|'
                    r'(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day, .*|\d+ (secs?|mins?).*)$', re.I | re.S)
TAIL   = re.compile(r'\s*(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day, \d.*$', re.S)


# Quiz 2 was exported from an attempt the student never submitted, so Moodle
# printed no key for any of its 8 questions and no key exists anywhere in the
# source. They are answered from the module's own lecture material and standard
# embryology, and carry `derived` provenance so the bias gate can see them.
# Q7 follows the Assiut lecture itself ("A-V node is the first to appear as an
# outgrowth from cells of the dorsal atrioventricular wall").
DERIVED_QUIZ2 = {
    1: 'Failure of postnatal fusion of septum primum and septum secundum',
    2: 'No cyanosis occurred prenatally or postnatally',
    3: 'Ventricular septal defect',
    4: 'Crista terminalis',
    5: 'Programmed cell death in the upper part of septum primum',
    6: 'Ventricular septal defect',
    7: 'AVN',
    8: 'Abnormalities of the conducting system and its neuroregulation',
}


# The Moodle page footer is a multi-block run of filler text. Only its first block
# starts with "Lorem Ipsum"; the continuation blocks ("industry's standard dummy text
# ever since the 1500s ...", "Follow Us") start mid-sentence, so a line-anchored filter
# lets them through and they get appended to the last option on the page. Any block
# carrying one of these signatures anywhere in it is page furniture and is dropped whole.
FOOTER = re.compile(r'(?i)lorem ipsum|dummy text|galley of type|typesetting|'
                    r'quick links|follow us|terms of use|about us|'
                    r'lmsace|powered by moodle|copyright\s*©|'
                    r'assiut university\s+faculty of medicine')


def norm(block):
    return block.replace('\xa0', ' ').strip()


def harvest(doc):
    markers, content, headers = [], [], []
    for pno, page in enumerate(doc):
        blocks = [(y0, norm(text))
                  for _x0, y0, _x1, _y1, text, *_ in page.get_text('blocks')]
        for i, (y0, t) in enumerate(blocks):
            if not t:
                continue
            first = t.split('\n')[0].strip()
            if QMARK.match(first) and len(t.split('\n')) <= 2:
                markers.append((pno, y0, int(QMARK.match(first).group(1))))
                continue
            if GUTTER.match(first) and len(t.split('\n')) <= 2:
                continue
            if FOOTER.search(t):
                continue
            if HEADER.search(t):
                headers.append((pno, y0, HEADER.search(t)))
                continue
            # Moodle usually emits "Lecture N : <title> ... Quiz N" as one block,
            # but for Quiz 24-25 it splits the "Quiz 24-25" label into a block of
            # its own. Without this lookahead that header is never recognised and
            # its nine questions silently inherit the previous quiz's tag.
            if i + 1 < len(blocks) and re.search(r'Lecture\s*[0-9]', t):
                joined = HEADER.search(t + '\n' + blocks[i + 1][1])
                if joined:
                    headers.append((pno, y0, joined))
                    continue
            content.append((pno, y0, t))
    for s in (markers, content, headers):
        s.sort(key=lambda r: (r[0], r[1]))
    return markers, content, headers


def parse(chunk):
    """chunk is a list of page blocks -> (stem, options, answer_text, is_tf)."""
    stem, options, answer, tf = [], [], None, False
    for block in chunk:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        head, rest = lines[0], ' '.join(lines[1:])

        m = ANS_TF.match(head)
        if m:
            answer, tf = m.group(1), True
            continue
        m = ANS.match(block.replace('\n', ' ').strip()) or ANS.match(head)
        if m:
            answer = (m.group(1).strip() or rest).strip().rstrip('.')
            continue
        if OPT_HD.match(head):                       # 'a.' alone, text on next lines
            options.append(rest)
            continue
        m = OPT_IN.match(head)
        if m:
            options.append(' '.join([m.group(2)] + lines[1:]))
            continue
        if head in ('True', 'False'):
            options.append(head)
            tf = True
            continue
        body = [l for l in lines
                if not (NOISE.match(l) or GUTTER.match(l) or QMARK.match(l))]
        if not body:
            continue
        if options:
            options[-1] += ' ' + ' '.join(body)      # continuation of the last option
        else:
            stem.extend(body)
    return ' '.join(stem), options, answer, tf


def quiz_at(headers, pos):
    cur = None
    for pno, y0, m in headers:
        if (pno, y0) <= pos:
            cur = m
        else:
            break
    return cur


def main():
    doc = fitz.open(SRC)
    markers, content, headers = harvest(doc)
    bounds = [(m[0], m[1]) for m in markers] + [(10 ** 6, 0)]

    questions, no_key, dropped, derived = [], [], [], 0
    for i, (pno, y0, num) in enumerate(markers):
        lo, hi = (pno, y0 - 6), bounds[i + 1]
        chunk = [t for (bp, by, t) in content if lo <= (bp, by) < hi]
        stem, options, answer, tf = parse(chunk)
        options = [TAIL.sub('', o).strip() for o in options]
        hdr = quiz_at(headers, (pno, y0))
        quiz = re.sub(r'\s+', ' ', hdr.group(3)).strip() if hdr else '?'
        lec = re.sub(r'\s+', ' ', hdr.group(2)).strip() if hdr else ''
        # Moodle publishes some sessions as a combined page ("Quiz 19&21",
        # "Quiz 24-25", "Quiz 34- 35"). Tagging those verbatim would leave a
        # student filtering for "Quiz 21" or "Quiz 25" with nothing, so each
        # number in the label becomes its own tag under the Quizzes family.
        nums = re.findall(r'\d+', quiz)
        tag = 'Department, Quizzes, ' + ', '.join(f'Quiz {n}' for n in nums) \
            if nums else f'Department, Quizzes, Quiz {quiz}'
        note = f'Quiz {quiz} — {lec}'

        if not stem:
            dropped.append((quiz, num, 'empty stem', '', len(options)))
            continue
        if answer is None and quiz == '2' and num in DERIVED_QUIZ2:
            answer, src = DERIVED_QUIZ2[num], 'derived'
            derived += 1
        else:
            src = 'key'
        if answer is None:
            no_key.append((quiz, num, stem[:70], len(options)))
            continue
        if not options:                               # fill-in-the-blank -> QROC
            questions.append(Q(stem, None, '-', 'key', exp=answer,
                               qtype='QROC', tag=tag, note=note))
            continue
        if len(options) < 2:
            dropped.append((quiz, num, 'single option', stem[:70], len(options)))
            continue
        letter = match_correct(answer, options)
        if letter is None:
            dropped.append((quiz, num, f'unmatched {answer[:40]!r}', stem[:70], len(options)))
            continue
        questions.append(Q(stem, options, letter, src, tag=tag, note=note))

    meta = {'Source file': 'All Quizzes CVS.pdf',
            'Type': 'Moodle quiz review export, 138 pages, 36 quizzes',
            'Tag': 'Department, Quizzes, Quiz <N> (per question)',
            'tagSuggere': 'None', 'Year': 'None',
            'Answer source': 'key — Moodle prints the correct answer under each question',
            'Markers in source': len(markers),
            'Emitted': 'see counts below'}
    n = write_md(OUT, 'Source 01 — CVS Department Quizzes (Moodle)', meta, questions)
    print(f'DERIVED answers (no key anywhere in the source): {derived}')
    print(f'{len(markers)} markers -> {n} questions written '
          f'({sum(1 for q in questions if q.type == "QROC")} QROC)')
    if no_key:
        print(f'\n{len(no_key)} questions have NO KEY printed in the source '
              f'(unanswered quiz attempt) and were skipped:')
        for r in no_key:
            print('   quiz %-7s Q%-3s %-72s opts=%s' % r)
    if dropped:
        print(f'\n{len(dropped)} markers dropped:')
        for r in dropped:
            print('   quiz %-7s Q%-3s %-24s %-60s opts=%s' % r)


if __name__ == '__main__':
    main()
