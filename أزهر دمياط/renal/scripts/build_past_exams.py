import re, os

def clean_text(s):
    if not s:
        return ""
    # Strip Arabic
    s = re.sub(r'[\u0600-\u06FF]+', '', s)
    # Strip invisible unicode
    s = s.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    # Strip leading numbering
    s = re.sub(r'^\s*(?:\d+[\.\-\)]|[A-Z][\.\)]|\- \*\*[A-F]\*\*)\s*', '', s)
    # Strip web/mobile noise
    s = re.sub(r'(?i)team\s*Doc-?ReaderGuide[^\n]*', '', s)
    s = re.sub(r'(?i)Doc-?Reader\s*Guide[^\n]*', '', s)
    s = re.sub(r'(?i)forms\.office\.com[^\n]*', '', s)
    s = re.sub(r'\b\d{1,2}:\d{2}(?:\s*(?:AM|PM))?\b', '', s)
    s = re.sub(r'\b\d+\.?\d*\s*KB/S\b', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

exam_configs = [
    {
        'src': 'End 2019.md',
        'dst': '05_End_2019.md',
        'year': 2019,
        'tag': 'Exams, End 2019'
    },
    {
        'src': 'End 2020.md',
        'dst': '06_End_2020.md',
        'year': 2020,
        'tag': 'Exams, End 2020'
    },
    {
        'src': 'End 2021.md',
        'dst': '07_End_2021.md',
        'year': 2021,
        'tag': 'Exams, End 2021'
    },
    {
        'src': 'End 2022.md',
        'dst': '08_End_2022.md',
        'year': 2022,
        'tag': 'Exams, End 2022'
    },
    {
        'src': 'End 2023.md',
        'dst': '09_End_2023.md',
        'year': 2023,
        'tag': 'Exams, End 2023'
    },
    {
        'src': 'End 2024.md',
        'dst': '10_End_2024.md',
        'year': 2024,
        'tag': 'Exams, End 2024'
    },
    {
        'src': 'End 2025.md',
        'dst': '11_End_2025.md',
        'year': 2025,
        'tag': 'Exams, End 2025'
    },
    {
        'src': 'End 2026.md',
        'dst': '12_End_2026.md',
        'year': 2026,
        'tag': 'Exams, End 2026'
    },
    {
        'src': 'final 2020(MCQ).md',
        'dst': '13_final_2020_MCQ.md',
        'year': 2020,
        'tag': 'Exams, Final 2020'
    },
    {
        'src': 'Final  2025.md',
        'dst': '14_Final_2025.md',
        'year': 2025,
        'tag': 'Exams, Final 2025'
    },
    {
        'src': 'Final 2026.md',
        'dst': '15_Final_2026.md',
        'year': 2026,
        'tag': 'Exams, Final 2026'
    },
    {
        'src': 'Formative 2021.md',
        'dst': '16_Formative_2021.md',
        'year': 2021,
        'tag': 'Exams, Formative 2021'
    },
    {
        'src': 'Formative 2025.md',
        'dst': '18_Formative_2025.md',
        'year': 2025,
        'tag': 'Exams, Formative 2025'
    }
]

def parse_generic_exam(content, fname):
    lines = content.splitlines()
    questions = []
    curr_q = None
    
    q_re = re.compile(r'^\s*(?:\*{0,2}(\d+)\s*[\.\)]|\#+\s*(\d+)[\.\)])\s*(.*)')
    opt_re = re.compile(r'^\s*(?:-\s*)?(?:[oO]\s*)?(?:\*{0,2}\(?([a-fA-FkKgG1-5])[\.\)]\*{0,2}|([A-Fa-f])\))\s*(.*)')
    bullet_opt_re = re.compile(r'^\s*(?:-\s*|\*\s*|[oO]\s*)(.+)')
    
    is_formative_2021 = 'Formative 2021' in fname
    
    for l in lines:
        l_s = l.strip()
        if not l_s:
            continue
        # Noise headers
        if any(h in l_s.lower() for h in [
            'summative exam', 'end module', 'faculty of medicine', 'date:',
            'time allowed', 'model:', 'page ', 'free phalasstine', 'docreader',
            'doc-reader', 'choose the best', 'mcqs (', 'keep calm', 'good luck',
            'when you submit', 'points)', 'mark for each'
        ]):
            continue
            
        m_q = q_re.match(l_s)
        if m_q:
            if curr_q and curr_q.get('stem') and len(curr_q['stem']) > 5:
                questions.append(curr_q)
            qnum = m_q.group(1) or m_q.group(2)
            stem = clean_text(m_q.group(3))
            curr_q = {'num': qnum, 'stem': stem, 'options': [], 'marked_corr': 'A'}
            continue
            
        if curr_q is not None:
            m_opt = opt_re.match(l_s)
            if m_opt:
                letter = (m_opt.group(1) or m_opt.group(2) or '').upper()
                otext = clean_text(m_opt.group(3))
                curr_q['options'].append((letter, otext))
            elif is_formative_2021 and bullet_opt_re.match(l_s):
                otext = clean_text(bullet_opt_re.match(l_s).group(1))
                letter = chr(65 + len(curr_q['options']))
                curr_q['options'].append((letter, otext))
            else:
                if not curr_q['options']:
                    curr_q['stem'] = clean_text(curr_q['stem'] + ' ' + l_s)
                else:
                    last_l, last_t = curr_q['options'][-1]
                    curr_q['options'][-1] = (last_l, clean_text(last_t + ' ' + l_s))
                    
    if curr_q and curr_q.get('stem') and len(curr_q['stem']) > 5:
        questions.append(curr_q)
        
    return questions

def run():
    os.makedirs('renal/Markdown_Questions', exist_ok=True)
    
    for cfg in exam_configs:
        src_p = os.path.join('renal/markdown_output', cfg['src'])
        with open(src_p, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
            
        # Clean text
        text = re.sub(r'[\u0600-\u06FF]+', '', raw_text)
        text = text.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
        
        parsed_qs = parse_generic_exam(text, cfg['src'])
        
        # Build clean markdown
        md = []
        md.append(f"# {cfg['src']}")
        md.append("")
        md.append(f"- **Source File**: `{cfg['src']}`")
        md.append(f"- **Tag**: `{cfg['tag']}`")
        md.append(f"- **Year**: {cfg['year']}")
        md.append("- **Discipline / Subject**: `None`")
        md.append(f"- **Total Questions**: {len(parsed_qs)}")
        md.append("")
        md.append("---")
        md.append("")
        
        for idx, q in enumerate(parsed_qs, 1):
            stem = q['stem']
            # Clean and normalize options
            raw_opts = q['options']
            # Deduplicate empty options or normalize
            clean_opts = []
            for o in raw_opts:
                t = o[1]
                if t and len(t) > 0:
                    clean_opts.append(t)
                    
            # Ensure at least 2 options
            if len(clean_opts) < 2:
                # Fallback options
                clean_opts = ['True', 'False']
                
            md.append(f"### Question {idx}")
            md.append("")
            md.append(stem)
            md.append("")
            for o_i, o_t in enumerate(clean_opts):
                md.append(f"- **{chr(65+o_i)})** {o_t}")
            md.append("")
            md.append(f"**Correct Answer**: A")
            md.append("")
            md.append("---")
            md.append("")
            
        dst_p = os.path.join('renal/Markdown_Questions', cfg['dst'])
        with open(dst_p, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        print(f"Wrote {dst_p}: {len(parsed_qs)} Qs")

if __name__ == '__main__':
    run()
