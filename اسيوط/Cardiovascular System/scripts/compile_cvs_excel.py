#!/usr/bin/env python3
"""Stage 4 — compile Markdown_Questions/*.md into the 31-column master Excel.

Differs from the generic scripts/build_module_template.py in one way that this module
needs: a question may carry its OWN `**Tag:**` / `**tagSuggere:**` / `**Year:**` lines.
Source 01 is a single PDF holding ~36 different departmental quizzes, so a file-level
tag from the catalog cannot describe it. Per-question values win; the catalog supplies
the default for every question that has none.

    python3 scripts/compile_cvs_excel.py
"""
import os, re, sys, glob, collections
import openpyxl

MOD  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MD   = os.path.join(MOD, 'Markdown_Questions')
CAT  = os.path.join(MD, '00_CATALOG_OF_ALL_FILES.md')
OUT  = os.path.join(MOD, 'Cardiovascular_System_Questions.xlsx')
CATEGORY_ID   = 'AssiutUniv_CARDIOVASCULAR_SYSTEM'
CATEGORY_NAME = 'Cardiovascular System'

HEADERS = ['id', 'Cas', 'Text', 'Image', 'explanationImage',
           'A', 'B', 'C', 'D', 'E', 'F',
           'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP',
           'Correct', 'Hint', 'EXP', 'Note', 'Type',
           'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
           'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks']

ARABIC   = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
BLOCK    = re.compile(r'^###\s*Q(\d+)\s*:\s*(.*?)(?=^###\s*Q\d+\s*:|\Z)', re.S | re.M)
OPT      = re.compile(r'^\s*[-*]\s*\*\*([A-F])\)\*\*\s*(.+?)\s*$', re.M)
SUBJECTS = ('Anatomy', 'Physiology', 'Histology', 'Biochemistry',
            'Microbiology', 'Parasitology', 'Pathology', 'Pharmacology')


def field(name):
    return re.compile(r'^\*\*' + re.escape(name) + r':\*\*\s*(.+?)\s*$', re.M)


F = {k: field(k) for k in ('Correct Answer', 'Answer Source', 'Image', 'EXP',
                           'Tag', 'tagSuggere', 'Year')}


def scrub(text):
    if text is None:
        return None
    t = ARABIC.sub('', str(text))
    t = t.replace('​', '').replace('﻿', '').replace('\xa0', ' ')
    t = re.sub(r'^\s*(?:###\s+)?(?:Q\d+|\d{1,3})\s*[.\-:)]\s*', '', t)
    t = re.sub(r'^\[(?:MCQ|Written)\]\s*[:\-]?\s*', '', t, flags=re.I)
    return re.sub(r'[ \t]+', ' ', t).strip() or None


def parse_markdown(path):
    raw = open(path, encoding='utf-8').read()
    out = []
    for num, body in BLOCK.findall(raw):
        body = body.split('\n---')[0]
        cuts = [m.start() for m in (OPT.search(body), F['Correct Answer'].search(body)) if m]
        stem = scrub(body[:min(cuts)] if cuts else body)
        opts = {L: scrub(v) for L, v in OPT.findall(body)}
        g = {k: (rx.search(body).group(1).strip() if rx.search(body) else None)
             for k, rx in F.items()}
        q = {'n': int(num), 'file': os.path.basename(path), 'Text': stem,
             'Correct': (g['Correct Answer'] or '').upper(),
             'source': (g['Answer Source'] or '').lower() or None,
             'Image': g['Image'], 'EXP': scrub(g['EXP']),
             'Tag': g['Tag'], 'tagSuggere': g['tagSuggere'],
             'Year': int(g['Year']) if (g['Year'] or '').isdigit() else None}
        for L in 'ABCDEF':
            q[L] = opts.get(L)
        if len([L for L in 'ABCDEF' if q[L]]) >= 2 and q['Correct'] not in ('-', ''):
            q['Type'] = 'QCS'
        else:
            q['Type'] = 'QROC'
            for L in 'ABCDEF':
                q[L] = None
            q['Correct'] = '-'
        out.append(q)
    return out


def repack(q):
    """Options must start at A and run without gaps; Correct moves with them."""
    if q['Type'] != 'QCS':
        return q
    filled = [L for L in 'ABCDEF' if q[L]]
    if filled == list('ABCDEF'[:len(filled)]):
        return q
    mapping = {old: 'ABCDEF'[i] for i, old in enumerate(filled)}
    vals = [q[old] for old in filled]
    for L in 'ABCDEF':
        q[L] = None
    for i, v in enumerate(vals):
        q['ABCDEF'[i]] = v
    q['Correct'] = mapping.get(q['Correct'], q['Correct'])
    return q


def parse_catalog(path):
    meta = {}
    if not os.path.exists(path):
        return meta
    for line in open(path, encoding='utf-8'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip().strip('*`') for c in line.strip().strip('|').split('|')]
        md = next((c for c in cells if c.endswith('.md')), None)
        if not md:
            continue
        tag = next((c for c in cells if re.match(
            r'^(Department|Exams|Professor|External),', c)), None)
        subj = next((c for c in cells if c in SUBJECTS), None)
        year = next((c for c in reversed(cells) if re.fullmatch(r'(19|20)\d{2}', c)), None)
        if not year and tag:
            m = re.search(r'(19|20)\d{2}', tag)
            year = m.group(0) if m else None
        meta[os.path.basename(md)] = {'Tag': tag, 'tagSuggere': subj,
                                      'Year': int(year) if year else None}
    return meta


STOP = set('a an the of in on to for and or is are was were be been with by from as at '
           'this that these those which what who whom его his her its their it he she they '
           'you your we our i me my not no yes do does did has have had can could will would '
           'may might must shall should about after before during between into through over '
           'under above below than then there here all any some each every both more most '
           'other such only own same so too very s t don now'.split())


def content_words(text):
    """Bag of meaningful words used to spot the SAME question paraphrased twice."""
    return {w for w in re.findall(r'[a-z]+', (text or '').lower())
            if len(w) > 2 and w not in STOP}


def tail_words(text, n=14):
    """Content words of the END of a stem — where the actual question lives."""
    ws = [w for w in re.findall(r'[a-z]+', (text or '').lower())
          if len(w) > 2 and w not in STOP]
    return set(ws[-n:])


# Tag families, in the order the tagging SOP requires them to appear: department
# and professor tags first, then exams, then other faculties. Without a fixed
# order the merged string depends on which source happened to compile first, so
# the same pair of sources could produce both "External, Qena 2020, Sohag 2021"
# and "External, Sohag 2021, Qena 2020" — two different strings for one tag set,
# which the platform shows students as two separate filters.
TAG_FAMILIES = ('Department', 'Professor', 'Exams', 'External')

# 'Exams' and 'External' are flat lists of exam labels, so their members can be
# put in a fixed chronological order to stop the same pair rendering as both
# "Sohag 2019, Sohag 2021" and "Sohag 2021, Sohag 2019". 'Department' is NOT
# sortable: it carries its own sub-headings ('Quizzes', 'QBank', 'GDs',
# 'Formative') that must keep their position ahead of the members they
# introduce, so it is left in insertion order.
SORTABLE_FAMILIES = ('Exams', 'External')


def _tag_order(label):
    year = re.search(r'\b(20\d{2})\b', label)
    return (int(year.group(1)) if year else 0, label)


def join_tags(*tag_strings):
    """Merge tag strings into one canonical comma-separated string.

    Parts are grouped under the family heading that introduced them, families
    come out in TAG_FAMILIES order, and each part appears once. A part that
    precedes any family heading keeps its position at the front.
    """
    grouped, loose = {}, []
    for ts in tag_strings:
        family = None
        for part in (p.strip() for p in (ts or '').split(',')):
            if not part:
                continue
            if part in TAG_FAMILIES:
                family = part
                grouped.setdefault(family, [])
            elif family is None:
                if part not in loose:
                    loose.append(part)
            elif part not in grouped[family]:
                grouped[family].append(part)
    out = list(loose)
    for family in TAG_FAMILIES:
        members = grouped.get(family)
        if not members:
            continue
        out.append(family)
        out.extend(sorted(members, key=_tag_order)
                   if family in SORTABLE_FAMILIES else members)
    return ', '.join(out)


def near_duplicate(a, b, threshold=0.75, tail_threshold=0.6):
    """The same exam question transcribed twice by two different passes.

    Exact stem normalisation cannot see it: sources 17 and 18 are the same 2019 sitting,
    and "Ahmed, 52 years old, had occasional angina..." vs "A 52-year-old man (Ahmed) with
    occasional chest pain (angina)..." normalise to different keys.

    Two guards keep this from eating real content, both learned the hard way — a first,
    looser version of this function merged 154 questions and collapsed distinct
    sub-questions of a single group-discussion case into one:

    1. Only ACROSS different source files. Within one file, repeated text is the design:
       every GD sub-question carries its case vignette in the stem, so a whole case's
       sub-questions look near-identical on a whole-stem comparison.
    2. The TAIL must match too. The vignette is shared; the discriminating question sits at
       the end of the stem, so overlap is required there as well as overall.

    Every merge is still printed for review, because a false merge silently deletes a real
    question and no later gate would notice.
    """
    if a['Type'] != b['Type'] or a['file'] == b['file']:
        return False
    wa, wb = content_words(a['Text']), content_words(b['Text'])
    if len(wa) < 6 or len(wb) < 6:
        return False
    shorter, longer = sorted((len(wa), len(wb)))
    if shorter / longer < 0.5:
        return False
    if len(wa & wb) / len(wa | wb) < threshold:
        return False
    ta, tb = tail_words(a['Text']), tail_words(b['Text'])
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= tail_threshold


def main():
    meta = parse_catalog(CAT)
    questions, untagged = [], collections.Counter()
    for fp in sorted(glob.glob(os.path.join(MD, '*.md'))):
        name = os.path.basename(fp)
        if name.startswith('00_'):
            continue
        fm = meta.get(name, {})
        for q in parse_markdown(fp):
            q['Tag'] = q['Tag'] or fm.get('Tag')
            q['tagSuggere'] = q['tagSuggere'] or fm.get('tagSuggere')
            if q['Year'] is None:
                q['Year'] = fm.get('Year')
            if not q['Tag']:
                untagged[name] += 1
            questions.append(repack(q))

    if untagged:
        print('[-] questions with no Tag (fix the catalog or the markdown):')
        for k, v in untagged.items():
            print(f'      {k}: {v}')
        sys.exit(1)

    # ---- dedupe on the normalized stem; MCQ beats written, tags merge
    seen, deduped = {}, []
    for q in questions:
        key = re.sub(r'[^a-z0-9]', '', (q['Text'] or '').lower())
        if not key:
            continue
        if key in seen:
            ex = seen[key]
            ex['Tag'] = join_tags(ex['Tag'], q['Tag'])
            ex['tagSuggere'] = ex['tagSuggere'] or q['tagSuggere']
            ex['Image'] = ex['Image'] or q['Image']
            ex['Year'] = ex['Year'] or q['Year']
            if ex['Type'] == 'QROC' and q['Type'] == 'QCS':
                model = ex['EXP']
                ex.update({k: q[k] for k in list('ABCDEF') + ['Type', 'Correct']})
                ex['EXP'] = q['EXP'] or model
            # Same precedence the near-duplicate pass below applies: a key-backed
            # answer beats a derived one. Without this the exact-stem pass silently
            # kept whichever copy happened to be compiled first, so a printed
            # department answer could be thrown away in favour of our own guess.
            elif ex.get('source') != 'key' and q.get('source') == 'key':
                ex['EXP'], ex['Correct'], ex['source'] = q['EXP'], q['Correct'], q['source']
            else:
                ex['EXP'] = ex['EXP'] or q['EXP']
            continue
        seen[key] = q
        deduped.append(q)

    # ---- second pass: fold in near-duplicates the exact-stem pass could not see
    merged_near = []
    kept = []
    for q in deduped:
        hit = None
        for k in kept:
            if near_duplicate(q, k):
                hit = k
                break
        if hit is None:
            kept.append(q)
            continue
        hit['Tag'] = join_tags(hit['Tag'], q['Tag'])
        hit['tagSuggere'] = hit['tagSuggere'] or q['tagSuggere']
        hit['Image'] = hit['Image'] or q['Image']
        hit['Year'] = hit['Year'] or q['Year']
        # prefer a key-backed answer over a derived one when the pair disagrees
        if hit.get('source') != 'key' and q.get('source') == 'key':
            hit['EXP'], hit['Correct'], hit['source'] = q['EXP'], q['Correct'], q['source']
        else:
            hit['EXP'] = hit['EXP'] or q['EXP']
        merged_near.append((hit['file'], q['file'], (q['Text'] or '')[:90]))
    deduped = kept

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = CATEGORY_NAME[:31]
    ws.append(HEADERS)
    for q in deduped:
        ws.append([None, None, q['Text'], q['Image'], None,
                   q['A'], q['B'], q['C'], q['D'], q['E'], q['F'],
                   None, None, None, None, None, None,
                   q['Correct'] or '-', None, q['EXP'], None, q['Type'],
                   CATEGORY_ID, CATEGORY_NAME, None, None,
                   q['tagSuggere'], q['Year'], q['Tag'], None, None])
    wb.save(OUT)

    mcq = sum(1 for q in deduped if q['Type'] == 'QCS')
    src = collections.Counter(q['source'] for q in deduped)
    print(f'[+] {OUT}')
    print(f'    {len(deduped)} questions ({mcq} QCS / {len(deduped) - mcq} QROC), '
          f'{len(questions) - len(deduped)} duplicates merged')
    print(f'    answer sources: {dict(src)}')
    if merged_near:
        print(f'    {len(merged_near)} near-duplicates merged (same question, '
              f'different transcription) — review:')
        for a, b, t in merged_near:
            print(f'      {b} -> {a}: {t}')
    if src.get('derived'):
        print(f"[!] {src['derived']} answers are 'derived' — no key existed in the source")
    missing = sum(1 for q in deduped if q['Type'] == 'QCS' and not q['source'])
    if missing:
        print(f'[!] {missing} MCQs carry no Answer Source label — Stage 2 incomplete')


if __name__ == '__main__':
    main()
