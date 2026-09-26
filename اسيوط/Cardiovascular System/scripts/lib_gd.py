"""Parser for the CVS group-discussion (GD) case files.

Every GD file in this module follows the same department template:

    G.D. (1): <session title> (<Subject>)
    Case 1:
    <clinical vignette, several lines>
    Questions:                    <- optional
    1- <sub-question>             <- '1-' or '1.'
       A) <option>                <- optional; present only on MCQ sub-questions
       B) <option>
    2- <sub-question>
    Case 2:
    ...

The vignette belongs to every sub-question under it, so it is copied into each stem —
the compiler has no concept of a shared preamble and a student filtering by tag must
still see the case.

None of these files print an answer key, which the caller is expected to handle by
supplying answers explicitly; the parser only reports structure.
"""
import re

CASE   = re.compile(r'^\s*Case\s*-?\s*(\d+)\s*[:.]?\s*$', re.I)
CASE_I = re.compile(r'^\s*Case\s*-?\s*(\d+)\s*[:.]\s*(\S.*)$', re.I)
GD     = re.compile(r'^\s*G\.?\s*D\.?\s*\(?\s*(\d+)\s*\)?\s*[:.]?\s*(.*)$', re.I)
QNUM   = re.compile(r'^\s*Q?\s*(\d{1,2})\s*[-.):]\s*(\S.*)$')
# Some sessions bullet their sub-questions instead of numbering them. Requiring a
# trailing '?' or ':' was too strict: the department frequently writes a bulleted
# sub-question with no terminal punctuation at all ("- What is the diagnosis") or
# ends it with a full stop ("- Mention name and location of the arteries which
# their pulsation can be palpated in the body."). Those were silently dropped —
# 21 real questions in source 07, 16 in 09 and 10 in 10. So a bullet also counts
# as a sub-question when it opens with an interrogative or an instruction verb,
# which is how every question in these files is phrased. Bulleted vignette facts
# (findings, lab values, drug lists) do not start that way, so they still pass
# through as case text; verified against all seven GD sources — only 07, 09 and
# 10 change, and every recovered item was hand-checked as a genuine question.
CUE    = (r'(?:What|Why|How|When|Where|Which|Who|Mention|Explain|Describe|'
          r'Enumerate|Compare|Discuss|State|Name|Give|List|Comment|Define|'
          r'Write|Can\s+we|Correct)\b')
BULLET = re.compile(r'^\s*[-\u2022\u2013]\s*(\S.*[?:]|' + CUE + r'.*?)\s*$')
OPT    = re.compile(r'^\s*\(?([A-Ha-h])\s*[.)]\s+(\S.*)$')
QMARK  = re.compile(r'^\s*Questions?\s*:?\s*$', re.I)
# Bibliographic citations under a case ("Source: Cases in Human Parasitology ...
# case number 24- page 93.") otherwise parse as a sub-question numbered 24.
CITE   = re.compile(r'^\s*(Source|Reference|Ref)\s*:', re.I)
SUBJ   = re.compile(r'\((Anatomy|Physiology|Histology|Biochemistry|Microbiology|'
                    r'Parasitology|Pathology|Pharmacology)\)', re.I)


def strip_chrome(lines, patterns):
    """Drop running headers/footers and bare page numbers."""
    out = []
    for ln in lines:
        s = ln.strip()
        if not s or re.fullmatch(r'\d{1,3}', s):
            continue
        if any(p.search(s) for p in patterns):
            continue
        out.append(ln.rstrip())
    return out


def parse(text, chrome=()):
    """-> list of dicts: {case, gd, subject, vignette, num, stem, options}"""
    pats = [re.compile(p, re.I) for p in chrome]
    lines = strip_chrome(text.split('\n'), pats)

    items, gd_no, gd_title, subject = [], None, None, None
    case_no, vignette, cur = None, [], None
    case_opts = []
    in_q = in_cite = False

    def flush():
        """Emit the open sub-question, or the case itself when it IS the question.

        Three shapes occur in these files and all three must survive:
          1. vignette + numbered sub-questions   -> one item per sub-question
          2. vignette + bulleted sub-questions   -> same
          3. vignette that ends in "...which of the following?" with the options
             printed directly under it and NO sub-question line at all -> one item
             whose stem is the vignette. Dropping this shape silently lost five
             pathology MCQs from the week-2 file before it was fixed.
        """
        nonlocal cur, case_opts
        if cur and cur['stem']:
            cur['vignette'] = ' '.join(vignette).strip()
            items.append(cur)
        elif case_opts and vignette:
            items.append({'case': case_no, 'gd': gd_no, 'gd_title': gd_title,
                          'subject': subject, 'num': 1,
                          'stem': ' '.join(vignette).strip(),
                          'options': list(case_opts), 'vignette': ''})
        cur = None
        case_opts = []

    for raw in lines:
        line = raw.strip()

        if CITE.match(line):
            in_cite = True
            continue
        if in_cite:
            # a citation runs until the next structural marker
            if not (CASE.match(line) or CASE_I.match(line) or GD.match(line)
                    or QMARK.match(line)):
                continue
            in_cite = False

        m = GD.match(line)
        if m and not QNUM.match(line):
            flush()
            gd_no, gd_title = m.group(1), m.group(2).strip()
            sm = SUBJ.search(gd_title)
            subject = sm.group(1).capitalize() if sm else subject
            pending_subject = sm is None
            continue

        if 'pending_subject' in dir() and pending_subject:
            sm = SUBJ.search(line)
            if sm:
                subject = sm.group(1).capitalize()
                pending_subject = False
                continue
            pending_subject = False

        m = CASE.match(line) or CASE_I.match(line)
        if m:
            flush()
            case_no = int(m.group(1))
            vignette = [m.group(2)] if m.lastindex and m.lastindex > 1 else []
            case_opts = []
            in_q = False
            continue

        if QMARK.match(line):
            in_q = True
            continue

        m = QNUM.match(line) or BULLET.match(line)
        if m:
            if m.re is BULLET:
                num, text = (cur['num'] + 1 if cur else 1), m.group(1)
            else:
                num, text = int(m.group(1)), m.group(2)
            flush()
            in_q = True
            cur = {'case': case_no, 'gd': gd_no, 'gd_title': gd_title,
                   'subject': subject, 'num': num,
                   'stem': text.strip(), 'options': [], 'vignette': ''}
            continue

        m = OPT.match(line)
        if m:
            # Options under a vignette with no sub-question line belong to the case.
            (cur['options'] if cur is not None else case_opts).append(m.group(2).strip())
            continue

        if cur is not None:
            if cur['options']:
                cur['options'][-1] += ' ' + line
            else:
                cur['stem'] += ' ' + line
        elif case_opts:
            case_opts[-1] += ' ' + line
        elif not in_q:
            vignette.append(line)

    flush()
    return items


def stem_with_case(item):
    """The stem a student should see: vignette first, then the sub-question."""
    v = re.sub(r'\s+', ' ', item['vignette']).strip()
    q = re.sub(r'\s+', ' ', item['stem']).strip()
    return f'{v} {q}'.strip() if v else q
