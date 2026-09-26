"""Shared helpers for CVS question extraction."""
import re, unicodedata

ARABIC = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
INVISIBLE = re.compile(r'[​-‏‪-‮﻿­]')

NOTATION = [
    (re.compile(r'\bCa\s*\*\*'), 'Ca²⁺'), (re.compile(r'\bCa\+\+'), 'Ca²⁺'),
    (re.compile(r'\bNa\s*\*(?!\*)'), 'Na⁺'), (re.compile(r'\bNa\+(?!\w)'), 'Na⁺'),
    (re.compile(r'\bK\+(?!\w)'), 'K⁺'), (re.compile(r'\bH\+(?!\w)'), 'H⁺'),
    (re.compile(r'\bCl-(?!\w)'), 'Cl⁻'), (re.compile(r'\bHCO3-'), 'HCO₃⁻'),
    (re.compile(r'(?<![A-Za-z])B(?=[12]\b)'), 'β'),
    (re.compile(r'\bum\b'), 'µm'), (re.compile(r'-->|->'), '→'),
    (re.compile(r'\bO2\b'), 'O₂'), (re.compile(r'\bCO2\b'), 'CO₂'),
]

def clean(s):
    """Normalise one piece of question text: whitespace, invisibles, notation."""
    if s is None:
        return None
    s = unicodedata.normalize('NFKC', s)
    s = INVISIBLE.sub('', s).replace('\xa0', ' ')
    s = s.replace('', ' ').replace('', '').replace('', '')
    s = re.sub(r'\s*\n\s*', ' ', s)
    s = re.sub(r'[ \t]{2,}', ' ', s).strip()
    for rx, rep in NOTATION:
        s = rx.sub(rep, s)
    return s.strip(' .;,')

def strip_numbering(stem):
    """Drop a leading question number/marker from a stem."""
    return re.sub(r'^\s*(?:\[MCQ\]\s*)?(?:###\s*)?Q?\s*\d{1,3}\s*[\.\)\-:]\s*', '', stem).strip()

def has_arabic(s):
    return bool(s and ARABIC.search(s))


class Q:
    """One extracted question."""
    def __init__(self, stem, options=None, correct=None, source=None,
                 exp=None, image=None, qtype=None, tag=None, tag_suggere=None,
                 year=None, note=None):
        self.stem = clean(stem)
        self.options = [clean(o) for o in (options or [])]
        self.correct = correct
        self.source = source            # key | marked | online | derived
        self.exp = clean(exp)
        self.image = image
        self.type = qtype or ('QROC' if not options else 'QCS')
        self.tag = tag
        self.tag_suggere = tag_suggere
        self.year = year
        self.note = note

    def render(self, n):
        out = [f'### Q{n}: {self.stem}', '']
        if self.type == 'QCS':
            for i, o in enumerate(self.options):
                out.append(f'- **{chr(65 + i)})** {o}')
            out.append('')
            out.append(f'**Correct Answer:** {self.correct}')
            out.append(f'**Answer Source:** {self.source}')
        else:
            out.append('**Correct Answer:** -')
            out.append(f'**Answer Source:** {self.source}')
        if self.image:
            out.append(f'**Image:** {self.image}')
        if self.exp:
            out.append(f'**EXP:** {self.exp}')
        # Per-question tagging. Most sources carry one tag for the whole file and the
        # catalog supplies it, but a source like the Moodle quiz export holds ~36
        # different quizzes, so the tag has to travel with the question.
        if self.tag:
            out.append(f'**Tag:** {self.tag}')
        if self.tag_suggere:
            out.append(f'**tagSuggere:** {self.tag_suggere}')
        if self.year:
            out.append(f'**Year:** {self.year}')
        out += ['', '---', '']
        return '\n'.join(out)


def write_md(path, title, meta, questions):
    """Write one source's questions in the fixed Stage-1 markdown format."""
    body = [f'# {title}', '']
    for k, v in meta.items():
        body.append(f'- **{k}:** {v}')
    body += ['', '---', '']
    for i, q in enumerate(questions, 1):
        body.append(q.render(i))
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(body).rstrip() + '\n')
    return len(questions)


def match_correct(answer_text, options):
    """Map Moodle's 'The correct answer is: <text>' back to an option letter."""
    def norm(s):
        return re.sub(r'[^a-z0-9]', '', (s or '').lower())
    target = norm(answer_text)
    if not target:
        return None
    for i, o in enumerate(options):
        if norm(o) == target:
            return chr(65 + i)
    for i, o in enumerate(options):          # truncation-tolerant fallback
        no = norm(o)
        if no and (no.startswith(target) or target.startswith(no)):
            return chr(65 + i)
    return None
