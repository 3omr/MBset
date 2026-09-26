#!/usr/bin/env python3
"""
MBset Module Questions Builder
==============================

Stage 4 of the pipeline: compiles the verified `Markdown_Questions/*.md` files into
the canonical 31-column `<Module>_Questions.xlsx`.

It parses the Stage-1 markdown format directly, so the Excel can always be rebuilt
from the markdown — the markdown is the source of truth, the Excel is a build artifact.

Markdown block format
---------------------
    ### Q1: <stem>

    - **A)** option
    - **B)** option

    **Correct Answer:** B
    **Answer Source:** key
    **Image:** Images/05_Q1.png
    **EXP:** explanation / model answer

    ---

Usage
-----
    python build_module_template.py \
        --markdown CVS/Markdown_Questions \
        --catalog  CVS/Markdown_Questions/00_CATALOG_OF_ALL_FILES.md \
        --category-id DamiettaFa_CVS --category-name CVS \
        --out CVS/CVS_Questions.xlsx

Tag / tagSuggere / Year per file come from the catalog table when `--catalog` is given;
otherwise pass `--tag-map tags.json` mapping markdown filename -> {Tag, tagSuggere, Year}.
"""

import argparse
import glob
import json
import os
import re
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl")

HEADERS = [
    'id', 'Cas', 'Text', 'Image', 'explanationImage',
    'A', 'B', 'C', 'D', 'E', 'F',
    'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP',
    'Correct', 'Hint', 'EXP', 'Note', 'Type',
    'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
    'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks'
]

ARABIC = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
QUESTION_HEADER = re.compile(
    r'^###\s*Q(\d+)\s*(?:(?:\(.*\)|\[.*\])\s*)?:\s*(.*)$', re.M
)
OPT = re.compile(r'^\s*[-*]\s*\*\*([A-F])\)\*\*\s*(.+?)\s*$', re.M)


def field(name):
    return re.compile(r'^\*\*' + name + r':\*\*\s*(.+?)\s*$', re.M)


def field_value(match):
    if not match or match.group(1).strip().lower() in ('none', 'null', 'n/a'):
        return None
    return match.group(1).strip()


CORRECT, SOURCE, IMAGE = field('Correct Answer'), field('Answer Source'), field('Image')
QUESTION_TAG, QUESTION_SUBJECT = field('Tag'), field('tagSuggere')
QUESTION_YEAR = re.compile(r'^\*\*Year:\*\*\s*((?:19|20)\d{2})\s*$', re.M)
EXPL = re.compile(
    r'^\*\*EXP:\*\*\s*(.*?)(?=^\*\*(?:Source Pages|Year|Tag|tagSuggere|Note):\*\*|^---\s*$|\Z)',
    re.S | re.M,
)
SUBJECTS = ('Anatomy', 'Physiology', 'Histology', 'Biochemistry', 'Microbiology',
            'Parasitology', 'Pathology', 'Pharmacology')


def scrub(text, strip_numbering=True):
    if text is None:
        return None
    t = ARABIC.sub('', str(text))
    # OCR/PDF extraction can leak ASCII control characters (notably backspace)
    # into cells; openpyxl rejects them and they are never meaningful medical
    # content.
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', t)
    t = t.replace('​', '').replace('﻿', '').replace('\xa0', ' ')
    if strip_numbering:
        t = re.sub(r'^\s*(?:###\s+)?(?:Q\d+|\d{1,3})\s*[\.\-\:\)]\s*', '', t)
    t = re.sub(r'^\[(?:MCQ|Written)\]\s*[\:\-]?\s*', '', t, flags=re.I)
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip() or None


def question_blocks(markdown):
    headers = list(QUESTION_HEADER.finditer(markdown))
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(markdown)
        body = markdown[header.end():end].split('\n---')[0]
        yield int(header.group(1)), header.group(2), body


def question_metadata(body):
    correct = CORRECT.search(body)
    source = SOURCE.search(body)
    image = IMAGE.search(body)
    explanation = EXPL.search(body)
    tag = QUESTION_TAG.search(body)
    subject = QUESTION_SUBJECT.search(body)
    year = QUESTION_YEAR.search(body)
    return {
        'Correct': correct.group(1).strip().upper() if correct else '',
        'source': source.group(1).strip().lower() if source else None,
        'Image': image.group(1).strip() if image else None,
        'EXP': scrub(explanation.group(1)) if explanation else None,
        'Tag': field_value(tag),
        'tagSuggere': field_value(subject),
        'Year': int(year.group(1)) if year else None,
    }


def parse_question(filename, number, heading_stem, body):
    starts = [match.start() for match in (OPT.search(body), CORRECT.search(body)) if match]
    stem_body = body[:min(starts)] if starts else body
    options = {letter: scrub(text, strip_numbering=False) for letter, text in OPT.findall(body)}
    question = {'n': number, 'file': filename, 'Text': scrub(heading_stem + '\n' + stem_body)}
    question.update(question_metadata(body))
    question.update({letter: options.get(letter) for letter in 'ABCDEF'})
    question['Type'] = 'QCS' if sum(bool(question[L]) for L in 'ABCDEF') >= 2 else 'QROC'
    if question['Type'] == 'QROC':
        question.update({letter: None for letter in 'ABCDEF'})
        question['Correct'] = '-'
    return question


def parse_markdown(path):
    raw = open(path, encoding='utf-8').read()
    return [parse_question(os.path.basename(path), *block) for block in question_blocks(raw)]


def repack(q):
    """Guarantee options start at A and run without gaps; move Correct with them."""
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
    if q['Correct'] in mapping:
        q['Correct'] = mapping[q['Correct']]
    return q


def parse_catalog(path):
    """Read Tag / tagSuggere / Year per markdown file from the catalog table."""
    meta = {}
    if not path or not os.path.exists(path):
        return meta
    for line in open(path, encoding='utf-8'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip().strip('*`') for c in line.strip().strip('|').split('|')]
        md = next((c for c in cells if c.endswith('.md')), None)
        if not md:
            continue
        tag = next((c for c in cells
                    if re.match(r'^(Department|Exams|Formative|Professor|External),', c)), None)
        year = next((c for c in reversed(cells) if re.fullmatch(r'(19|20)\d{2}', c)), None)
        subj = next((c for c in cells if c in SUBJECTS), None)
        if not year and tag:
            m = re.search(r'(19|20)\d{2}', tag)
            year = m.group(0) if m else None
        meta[os.path.basename(md)] = {'Tag': tag, 'tagSuggere': subj,
                                      'Year': int(year) if year else None}
    return meta


def build(md_dir, meta, category_id, category_name, out_path, strict=True):
    questions = []
    for fp in sorted(glob.glob(os.path.join(md_dir, '*.md'))):
        if os.path.basename(fp).startswith('00_'):
            continue
        fm = meta.get(os.path.basename(fp), {})
        if strict and not fm.get('Tag'):
            sys.exit(f"[-] no Tag for {os.path.basename(fp)} — fix the catalog or pass --tag-map")
        for q in parse_markdown(fp):
            q.update({'Tag': q.get('Tag') or fm.get('Tag'),
                      'tagSuggere': q.get('tagSuggere') or fm.get('tagSuggere'),
                      'Year': q.get('Year') or fm.get('Year')})
            questions.append(repack(q))

    # ---- deduplicate on the normalized stem
    seen, deduped = {}, []
    for q in questions:
        key = re.sub(r'[^a-z0-9]', '', (q['Text'] or '').lower())
        if not key:
            continue
        if key in seen:
            ex = seen[key]
            tags = [t.strip() for t in (str(ex['Tag'] or '') + ', ' + str(q['Tag'] or '')).split(',') if t.strip()]
            ex['Tag'] = ', '.join(dict.fromkeys(tags))
            ex['tagSuggere'] = ex.get('tagSuggere') or q.get('tagSuggere')
            ex['Image'] = ex.get('Image') or q.get('Image')
            if ex['Type'] == 'QROC' and q['Type'] == 'QCS':   # MCQ wins, keeps the model answer
                model = ex.get('EXP')
                ex.update({k: q[k] for k in list('ABCDEF') + ['Type', 'Correct']})
                ex['EXP'] = q.get('EXP') or model
            else:
                ex['EXP'] = ex.get('EXP') or q.get('EXP')
            continue
        seen[key] = q
        deduped.append(q)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = category_name[:31]
    ws.append(HEADERS)
    for q in deduped:
        ws.append([
            None,                       # id — platform assigns
            None,                       # Cas
            q['Text'],
            q.get('Image'),
            None,                       # explanationImage
            q.get('A'), q.get('B'), q.get('C'), q.get('D'), q.get('E'), q.get('F'),
            None, None, None, None, None, None,           # A_EXP - F_EXP
            q.get('Correct') or '-',
            None,                       # Hint
            q.get('EXP'),
            None,                       # Note
            q['Type'],
            category_id, category_name,
            None, None,                 # subcategoryId / subcategoryName
            q.get('tagSuggere'),
            q.get('Year'),
            q.get('Tag'),
            None, None,                 # ImageMasks / ExplanationImageMasks
        ])
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    wb.save(out_path)

    mcq = sum(1 for q in deduped if q['Type'] == 'QCS')
    derived = sum(1 for q in deduped if q.get('source') == 'derived')
    no_src = sum(1 for q in deduped if q['Type'] == 'QCS' and not q.get('source'))
    print(f"[+] {out_path}: {len(deduped)} questions "
          f"({mcq} MCQ / {len(deduped) - mcq} written), "
          f"{len(questions) - len(deduped)} duplicates merged")
    if derived:
        print(f"[!] {derived} answers are 'derived' (no key in the source) — report these to the user")
    if no_src:
        print(f"[!] {no_src} MCQs carry no **Answer Source:** label — Stage 2 is incomplete")
    print(f"    next: python scripts/validate_questions_excel.py {out_path}")
    print(f"          python scripts/audit_question_bank.py --excel {out_path} --by-tag")


def main():
    ap = argparse.ArgumentParser(description="Compile verified markdown into the master 31-column Excel")
    ap.add_argument('--markdown', required=True, help='<Module>/Markdown_Questions directory')
    ap.add_argument('--catalog', help='00_CATALOG_OF_ALL_FILES.md to read Tag/tagSuggere/Year from')
    ap.add_argument('--tag-map', help='JSON: {"05_End_2021.md": {"Tag": "...", "tagSuggere": null, "Year": 2021}}')
    ap.add_argument('--category-id', required=True)
    ap.add_argument('--category-name', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--allow-missing-tags', action='store_true')
    args = ap.parse_args()

    meta = parse_catalog(args.catalog)
    if args.tag_map:
        meta.update(json.load(open(args.tag_map, encoding='utf-8')))
    build(args.markdown, meta, args.category_id, args.category_name, args.out,
          strict=not args.allow_missing_tags)


if __name__ == '__main__':
    main()
