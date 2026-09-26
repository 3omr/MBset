#!/usr/bin/env python3
"""Source 11 — GD/Cases CVS-206- final (merged).pdf.

This PDF is a literal re-issue of the four weekly GD files (source 07 + 08 +
09 + 10) concatenated back to back — same case text, same "G.D. (N): title
(Subject)" headers restarting at 1 for each week (confirmed by grepping the
merged PDF's own "G.D." lines: five headers 1-5, then four headers 1-4, then
six headers 1-6, then four headers 1-4, in that order — an exact match to
weeks 1-4). Since the content is identical, this script re-uses the
per-source ITEMS lists already built (and hand-corrected for the
trailing-header subject/GD mis-attribution, recovered/merged items, etc.) by
extract_07/08/09/10, loading each module directly from its file so the
total is a straightforward, faithful concatenation rather than a second
hand-transcription of the same questions. The per-week totals are read live
from those four modules rather than hard-coded, so this file tracks any
later correction to them automatically.

Per the extraction contract, Stage 1 does not deduplicate across sources —
source 11 is emitted in full here even though the compiler will later
collapse its items against 07-10 by normalized stem. No answer key is
printed anywhere in the source; every answer is `derived`.
"""
import os, sys, collections, importlib.util

sys.path.insert(0, os.path.dirname(__file__))
from lib_md import Q, write_md

MOD = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(MOD, 'Markdown_Questions', '11_GD_Cases_Final_Merged.md')
SRC = 'Raw_PDF_Questions/1- Cardiovascular system/GD/Cases CVS-206- final (merged).pdf'
SCRIPTS_DIR = os.path.dirname(__file__)


def _load_items(script_name):
    path = os.path.join(SCRIPTS_DIR, script_name)
    spec = importlib.util.spec_from_file_location(script_name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ITEMS


def main():
    parts = [(name, _load_items(name)) for name in (
        'extract_07_gd_week1.py', 'extract_08_gd_week2.py',
        'extract_09_gd_week3.py', 'extract_10_gd_week4.py')]
    all_items = [it for _, items in parts for it in items]
    breakdown = '+'.join(str(len(items)) for _, items in parts)
    qs = []
    for stem, options, correct, exp, tag, subj in all_items:
        qs.append(Q(stem, options, correct, 'derived', exp=exp, tag=tag, tag_suggere=subj))
    meta = {'Source file': SRC,
            'Type': 'GD case handout, 45 pages; a literal concatenation of the 4 '
                    'weekly GD case files (sources 07-10), 19 G.D. session headers '
                    'across Histology, Anatomy, Physiology, Microbiology, '
                    'Parasitology, Pathology, Biochemistry and Pharmacology',
            'Tag': 'Department, GDs, <Subject> GD <N>', 'tagSuggere': 'varies by item',
            'Year': 'None',
            'Answer source': 'derived — no key is printed anywhere in the source'}
    n = write_md(OUT, 'Source 11 — GD Cases Final Merged', meta, qs)
    mcq = sum(1 for s, o, c, e, t, sj in all_items if o)
    ans = collections.Counter(c for s, o, c, e, t, sj in all_items if o)
    print(f'source 11: {n} questions ({mcq} MCQ / {n - mcq} written)')
    print(f'  counters: {breakdown} = {len(all_items)} expected; '
          f'option-A blocks = {mcq}; ### Q = {n}')
    print(f"  answer sources: {{'derived': {n}}}")
    print(f'  answer distribution: {dict(sorted(ans.items()))} ({mcq} MCQs — bias gate n/a, <15)')
    print(f'  derived: {n}')


if __name__ == '__main__':
    main()
