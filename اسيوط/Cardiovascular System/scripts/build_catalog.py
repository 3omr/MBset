#!/usr/bin/env python3
"""Stage 3 — regenerate Markdown_Questions/00_CATALOG_OF_ALL_FILES.md.

One row per SOURCE FILE, built by walking the raw source tree and the extracted
markdown together, so a source that was never extracted shows up as a blank row
rather than silently vanishing — that is the whole point of the catalog.

    python3 scripts/build_catalog.py
"""
import os, re, glob, collections

MOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MD  = os.path.join(MOD, 'Markdown_Questions')
RAW = os.path.join(MOD, 'Raw_PDF_Questions', '1- Cardiovascular system')
LEC = os.path.join(MOD, 'Lectures_raw', '1- Cardiovascular system')
OUT = os.path.join(MD, '00_CATALOG_OF_ALL_FILES.md')

# index -> (source path relative to the module root, note)
SOURCES = {
    1:  ('Raw_PDF_Questions/1- Cardiovascular system/All Quizzes CVS.pdf', ''),
    2:  ('Raw_PDF_Questions/1- Cardiovascular system/All  formatives  CVS.pdf', ''),
    3:  ('Raw_PDF_Questions/1- Cardiovascular system/All CVS GDs.pdf', ''),
    4:  ('Raw_PDF_Questions/1- Cardiovascular system/department CVS bank.pdf', ''),
    5:  ('Raw_PDF_Questions/1- Cardiovascular system/parasitology department.pdf', ''),
    6:  ('Raw_PDF_Questions/1- Cardiovascular system/GD/1- Carditis.pdf', ''),
    7:  ('Raw_PDF_Questions/1- Cardiovascular system/GD/1st week-CVS-206-cases.pdf', ''),
    8:  ('Raw_PDF_Questions/1- Cardiovascular system/GD/2nd week-CVS- cases.pdf', ''),
    9:  ('Raw_PDF_Questions/1- Cardiovascular system/GD/3rd week-CVS-206 cases.pdf', ''),
    10: ('Raw_PDF_Questions/1- Cardiovascular system/GD/4th week-CVS-206 cases.pdf', ''),
    11: ('Raw_PDF_Questions/1- Cardiovascular system/GD/Cases CVS-206- final (merged).pdf',
         'merged re-issue of weeks 1-4; duplicates collapse at compile time'),
    12: ('Raw_PDF_Questions/1- Cardiovascular system/GD/Cases of CVS-  parasitology-2023-2024.pdf', ''),
    13: ('Raw_PDF_Questions/1- Cardiovascular system/GD/Cases of CVS-  parasitology-2023-2024-1.pdf',
         'near-duplicate of 12'),
    14: ('Raw_PDF_Questions/1- Cardiovascular system/GD/Micro GD cases CVS block 2023 student.pptx', ''),
    15: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/CVS final written 2022.pdf', ''),
    16: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/CVS written 2022 دور تاني.pdf',
         'second round of the 2022 final'),
    17: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/Final Exam 2019.pdf', ''),
    18: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/Final Written 2019,2020.pdf',
         'two exam years bound in one file'),
    19: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/MCQ Assuit.pdf', ''),
    20: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/midterm Assuit.pdf', ''),
    21: ('Raw_PDF_Questions/1- Cardiovascular system/ASSIUT PREVIOUS EXAMS/Written Final CVS 2021.pdf', ''),
    22: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/Qena cvs midterm 2020 (answered) .pdf', ''),
    23: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/sohag final 2021.pdf', ''),
    24: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/Sohag midterm 2019.PDF', ''),
    25: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/فاينل سوهاج 2021.pdf',
         'Arabic filename: "Final Sohag 2021"'),
    26: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/فاينل قنا ٢٠٢٠.pdf',
         'Arabic filename: "Final Qena 2020"'),
    27: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/ميد جنوب الوادى .pdf',
         'Arabic filename: "Midterm South Valley"'),
    28: ('Raw_PDF_Questions/1- Cardiovascular system/OTHER EXAMS/ميد سوهاج 2021.pdf',
         'Arabic filename: "Midterm Sohag 2021"'),
    # 29-34: the PRACTICAL EXAMS folder. Excluded from this module by the user's
    # decision, not by a processing failure. The raw files are left on disk under
    # Raw_PDF_Questions/ so the decision stays reversible.
    29: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/CVS practical bank.pdf', ''),
    30: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/CVS practical exam (answered) .pdf', ''),
    31: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/PRACTICAL EXAM 2020.pdf', ''),
    32: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/SUMMER PRACTICAL EXAM 2021.pdf', ''),
    33: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/summer practical exam 2021.jpg', ''),
    34: ('Raw_PDF_Questions/1- Cardiovascular system/PRACTICAL EXAMS/summer practical exam 2021(1).jpg', ''),
    35: ('Lectures_raw/1- Cardiovascular system/CVS-L 23.pdf',
         'question section on pages 25-28 of the anatomy handout'),
    36: ('Lectures_raw/1- Cardiovascular system/Lecture 40, 41.pptx',
         'MCQs on slides 46-47 of the physiology deck'),
}

EXCLUDED = {
    idx: 'EXCLUDED - practical exams are out of scope for this module (user decision)'
    for idx in range(29, 35)
}

HEAD = re.compile(r'^- \*\*(.+?):\*\*\s*(.*)$', re.M)


def md_stats(path):
    t = open(path, encoding='utf-8').read()
    head = dict(HEAD.findall(t.split('\n---', 1)[0]))
    total = len(re.findall(r'^### Q', t, re.M))
    written = len(re.findall(r'^\*\*Correct Answer:\*\* -\s*$', t, re.M))
    src = collections.Counter(re.findall(r'^\*\*Answer Source:\*\* (\S+)', t, re.M))
    ans = collections.Counter(a for a in re.findall(r'^\*\*Correct Answer:\*\* (\S+)', t, re.M)
                              if a != '-')
    top = max(ans.values()) / sum(ans.values()) * 100 if ans else 0
    tags = collections.Counter(re.findall(r'^\*\*Tag:\*\* (.+)$', t, re.M))
    tag = head.get('Tag') or (tags.most_common(1)[0][0] if tags else '')
    if len(tags) > 1:
        tag = f'{len(tags)} per-question tags'
    gate = 'n/a' if sum(ans.values()) < 15 else ('PASS' if top <= 45 else 'FAIL')
    return {'total': total, 'mcq': total - written, 'written': written,
            'src': ', '.join(f'{k}:{v}' for k, v in sorted(src.items())),
            'dist': ', '.join(f'{k}:{v}' for k, v in sorted(ans.items())),
            'top': f'{top:.0f}%', 'gate': gate, 'tag': tag,
            'tagSuggere': head.get('tagSuggere', ''), 'Year': head.get('Year', ''),
            'type': head.get('Type', '')}


def main():
    by_index = {}
    for fp in sorted(glob.glob(os.path.join(MD, '*.md'))):
        name = os.path.basename(fp)
        if name.startswith('00_'):
            continue
        m = re.match(r'(\d+)_', name)
        if m:
            by_index[int(m.group(1))] = (name, fp)

    rows, totals = [], collections.Counter()
    for idx in sorted(SOURCES):
        src_rel, note = SOURCES[idx]
        src_abs = os.path.join(MOD, src_rel)
        exists = 'yes' if os.path.exists(src_abs) else 'MISSING'
        if idx in by_index:
            name, fp = by_index[idx]
            s = md_stats(fp)
            totals['total'] += s['total']; totals['mcq'] += s['mcq']
            totals['written'] += s['written']
            status = 'extracted'
        else:
            name, s = '', {k: '' for k in ('total', 'mcq', 'written', 'src', 'dist',
                                           'top', 'gate', 'tag', 'tagSuggere',
                                           'Year', 'type')}
            status = EXCLUDED.get(idx, 'NOT EXTRACTED')
        rows.append((idx, os.path.basename(src_rel), exists, name, s, status, note))

    cols = ['#', 'Source file', 'On disk', 'Markdown', 'Total', 'MCQ', 'Written',
            'Answer sources', 'Answer distribution', 'Top letter', 'Bias gate',
            'Tag', 'tagSuggere', 'Year', 'Status', 'Note']
    out = ['# CVS (Assiut) — catalog of all question sources', '',
           'One row per source file. A source that is deliberately not extracted still',
           'appears here with `EXCLUDED — <reason>` in Status; a blank Markdown column',
           'means the source has not been processed yet.', '',
           '| ' + ' | '.join(cols) + ' |',
           '| ' + ' | '.join('---' for _ in cols) + ' |']
    for idx, src, exists, name, s, status, note in rows:
        out.append('| ' + ' | '.join(str(x) for x in [
            idx, src, exists, name, s['total'], s['mcq'], s['written'], s['src'],
            s['dist'], s['top'], s['gate'], s['tag'], s['tagSuggere'], s['Year'],
            status, note]) + ' |')
    done = sum(1 for r in rows if r[5] == 'extracted')
    excluded = sum(1 for r in rows if r[5].startswith('EXCLUDED'))
    in_scope = len(rows) - excluded
    out += ['', f'**{done} / {in_scope} in-scope sources extracted '
                f'({excluded} excluded) — '
                f"{totals['total']} questions ({totals['mcq']} MCQ / "
                f"{totals['written']} written).**"]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f'[+] {OUT}: {done}/{in_scope} in-scope sources ({excluded} excluded), '
          f'{totals["total"]} questions')
    for idx, src, exists, name, s, status, note in rows:
        if status.startswith('EXCLUDED'):
            continue
        if status != 'extracted' or exists != 'yes' or s['gate'] == 'FAIL':
            print(f'    [!] {idx:>2} {src[:55]:<55} on-disk={exists} {status} gate={s["gate"]}')


if __name__ == '__main__':
    main()
