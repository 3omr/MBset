import fitz, re

doc = fitz.open('renal/Raw_PDF_Questions/Renal/End 2024.pdf')
full_lines = []
for p in doc:
    for l in p.get_text().splitlines():
        l_s = l.strip()
        if l_s and not any(h in l_s.lower() for h in ['free phalasstine', 'direected by', 'ayoub']):
            full_lines.append(l_s)

raw_qs = []
curr_q = None

for l in full_lines:
    m_q = re.match(r'^(?:(\d{1,2})\s*\)|(II)\))\s*(.*)', l)
    if m_q:
        if curr_q: raw_qs.append(curr_q)
        qnum = int(m_q.group(1)) if m_q.group(1) else 11
        curr_q = {'num': qnum, 'lines': [m_q.group(3)] if m_q.group(3) else []}
    else:
        if curr_q: curr_q['lines'].append(l)

if curr_q: raw_qs.append(curr_q)

correct_keys = {
    1: 'B', 2: 'A', 3: 'D', 4: 'D', 5: 'C',
    6: 'A', 7: 'A', 8: 'B', 9: 'C', 10: 'C',
    11: 'C', 12: 'D', 13: 'A', 14: 'A', 15: 'A',
    16: 'B', 17: 'A', 18: 'D', 19: 'D', 20: 'D',
    21: 'A', 22: 'C', 23: 'A', 24: 'A', 25: 'C',
    26: 'B', 27: 'A', 28: 'B', 29: 'C', 30: 'B',
    31: 'C', 32: 'C', 33: 'B', 34: 'C', 35: 'A',
    36: 'A', 37: 'D', 38: 'D', 39: 'C', 40: 'B',
    41: 'C', 42: 'D', 43: 'D', 44: 'D', 45: 'C',
    46: 'B', 47: 'A', 48: 'B', 49: 'B', 50: 'B'
}

md = [
    '# End 2024',
    '',
    '- **Source File**: `End 2024.pdf`',
    '- **Tag**: `Exams, End 2024`',
    '- **Year**: 2024',
    '- **Discipline / Subject**: `None`',
    f'- **Total Questions**: {len(raw_qs)}',
    '',
    '---',
    ''
]

for q in raw_qs:
    qnum = q['num']
    lines = q['lines']
    
    stem_parts = []
    options = []
    
    for l in lines:
        m_opt = re.match(r'^[a-dA-D]\s*[\)\.]\s*(.+)', l)
        if m_opt:
            options.append(m_opt.group(1).strip())
        else:
            if not options:
                stem_parts.append(l)
            else:
                options[-1] += " " + l
                
    stem = " ".join(stem_parts).strip()
    stem = re.sub(r'\s+', ' ', stem)
    
    md.append(f"### Question {qnum}")
    md.append("")
    md.append(stem)
    md.append("")
    for i, opt in enumerate(options):
        letter = chr(65 + i)
        clean_opt = re.sub(r'[\.\-\_xX\>]+$', '', opt).strip()
        md.append(f"- **{letter})** {clean_opt}")
    md.append("")
    corr = correct_keys.get(qnum, 'A')
    md.append(f"**Correct Answer**: {corr}")
    md.append("")
    md.append("---")
    md.append("")

with open('renal/Markdown_Questions/10_End_2024.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md).strip() + '\n')

print(f"Wrote renal/Markdown_Questions/10_End_2024.md: {len(raw_qs)} questions!")
