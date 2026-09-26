#!/usr/bin/env python3
"""Build source #2 from already-curated Markdown blocks only.

This is intentionally a reconciliation handoff, not an OCR extractor.  It
copies the verified blocks from the three composite ranges that are already
identified, deduplicates normalized stems, and records matching coverage in
the block metadata.
"""
from pathlib import Path
import re

ROOT = Path('/home/omar/MBset')
MD = ROOT / 'اسيوط/NEUROSCIENCE SYSTEM/Markdown_Questions'
OUT = MD / '02_All_CNS_midterm_final_Assuit.md'

PRIMARY = [
    ('05_Mid_exam_2020.md', '#5', 'pages 2-11', 'Exams, Midterm 2020', '2020', None),
    ('06_Final_2022.md', '#6', 'pages 64-73', 'Exams, Final 2022', '2022', 44),
    ('08_Final_CNS_summer_2024.md', '#8', 'pages 98-116', 'Exams, Final 2024', '2024', None),
]
SECONDARY = [
    ('09_All_CNS_quizzes.md', '#9', 'pages 19-63', 'Department, Quizzes, Weeks 1-4', 'None', None),
    ('10_CNS_Gds.md', '#10', 'pages 19-63', 'Department, GDs, CNS', 'None', None),
    ('14_Mid_Formatives.md', '#14', 'pages 19-63', 'Department, Formative, Weeks 1-4', 'None', None),
    ('15_Mid_GDs_Answered.md', '#15', 'pages 19-63', 'Department, GDs, CNS', 'None', None),
    ('16_Mid_quizzes.md', '#16', 'pages 19-63', 'Department, Quizzes, Weeks 1-4', 'None', None),
    ('22_Midterm_2020.md', '#22', 'composite duplicate match', 'External, Midterm 2020', '2020', None),
    ('23_Qs_bank_CNS_Guyton.md', '#23', 'composite duplicate match', 'External, Guyton 2016', '2016', None),
    ('24_Qs_bank_1.md', '#24', 'composite duplicate match', 'Department, QBank, Physiology', 'None', None),
    ('25_Qs_bank_2.md', '#25', 'composite duplicate match', 'Department, QBank, Physiology', 'None', None),
    ('27_Pharmacology_Qs_bank.md', '#27', 'composite duplicate match', 'Department, QBank, Pharmacology', 'None', None),
    ('28_Physiology_Qs_bank_MCQ.md', '#28', 'composite duplicate match', 'Department, QBank, Physiology', 'None', None),
]
SECONDARY_LABELS = {row[1] for row in SECONDARY}

def norm_stem(stem: str) -> str:
    stem = re.sub(r'^\[[^]]*\]\s*', '', stem)
    return re.sub(r'[^a-z0-9]', '', stem.lower())

def read_blocks(path: Path):
    text = path.read_text(encoding='utf-8')
    parts = re.split(r'(?m)(?=^### Q\d+:)', text)
    out = []
    for part in parts:
        m = re.match(r'^### Q(\d+): (.+?)\n', part)
        if m:
            out.append({'source_q': int(m.group(1)), 'stem': m.group(2).strip(), 'body': part.strip()})
    return out

all_sources = {}
for filename, label, pages, tag, year, _limit in PRIMARY + SECONDARY:
    all_sources[label] = (filename, pages, tag, year, read_blocks(MD / filename))

secondary_index = {}
for label, (_filename, _pages, _tag, _year, blocks) in all_sources.items():
    for block in blocks:
        secondary_index.setdefault(norm_stem(block['stem']), []).append((label, block['source_q']))

seen = set()
out_blocks = []
coverage_counts = {}
for filename, label, pages, tag, year, limit in PRIMARY:
    selected = all_sources[label][4][:limit] if limit else all_sources[label][4]
    for block in selected:
        key = norm_stem(block['stem'])
        if not key or key in seen:
            continue
        seen.add(key)
        matches = [(lab, q) for lab, q in secondary_index.get(key, [])
                   if lab in SECONDARY_LABELS]
        coverage = [f'{lab} Q{q}' for lab, q in matches]
        for lab, _q in matches:
            coverage_counts[lab] = coverage_counts.get(lab, 0) + 1
        body = re.sub(r'^### Q\d+:', '### Q{n}:', block['body'], count=1, flags=re.M)
        out_blocks.append((body, label, pages, tag, year, coverage))

header = '''# Source 2 — All CNS midterm and final exams Assiut (reconciliation handoff)

- **Source file:** Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/All CNS midterm and final exams Assuit.pdf
- **PDF pages:** 136
- **OCR policy:** No OCR performed here. This handoff copies only existing verified Markdown blocks.
- **Included composite ranges:** pages 2-11 → source #5; pages 64-73 → source #6; pages 98-116 → source #8.
- **Unresolved composite ranges:** pages 12-18, 19-63, 74-97, and 117-136 are not newly extracted in this handoff; their unique OCR blocks remain pending.
- **Deduplication:** normalized stem (`[^a-z0-9]` removed, lowercase); each copied block appears once.
- **Duplicate coverage:** exact normalized-stem matches against verified sources #9, #10, #14, #15, #16, and #22–#28 are recorded per block where found.
- **Composite page-range note:** primary ranges above are confirmed handoff ranges; secondary matches are labeled as duplicate coverage and are not re-copied.

'''

rendered = [header]
for i, (body, label, pages, tag, year, coverage) in enumerate(out_blocks, 1):
    body = body.replace('### Q{n}:', f'### Q{i}:', 1)
    # Keep the copied question content intact; add auditable source metadata.
    body += f'\n\n**Composite Page Range:** {pages}\n**Copied From:** {label}\n**Duplicate Coverage:** ' + (', '.join(coverage) if coverage else 'None')
    rendered.append(body + '\n\n---\n')

summary = f'''\n## Reconciliation counts\n\n- **Copied blocks:** {len(out_blocks)}\n- **Primary blocks:** #5={len(all_sources["#5"][4])}; #6 written subset=44; #8={len(all_sources["#8"][4])} before normalized-stem deduplication\n- **Secondary duplicate coverage counts:** ''' + ', '.join(f'{k}={v}' for k, v in sorted(coverage_counts.items())) + '\n'
OUT.write_text(''.join(rendered) + summary, encoding='utf-8')
print(f'wrote {OUT}')
print(f'copied_blocks={len(out_blocks)}')
print('secondary_coverage=' + ','.join(f'{k}:{v}' for k, v in sorted(coverage_counts.items())))
