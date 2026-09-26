import re, os

def parse_exam(fname):
    p = os.path.join('renal/markdown_output', fname)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Pre-clean
    text = re.sub(r'[\u0600-\u06FF]+', '', text)
    text = text.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    
    # Split into lines
    lines = text.splitlines()
    
    questions = []
    curr_q = None
    
    q_re = re.compile(r'^\s*(?:\*{0,2}(\d+)\s*[\.\)]|\#+\s*(\d+)[\.\)])\s*(.+)')
    opt_re = re.compile(r'^\s*(?:-\s*)?(?:\*{0,2}\(?([a-fA-FkKgG1-5])[\.\)]\*{0,2}|([A-Fa-f])\))\s*(.+)')
    
    for l in lines:
        l_str = l.strip()
        if not l_str:
            continue
        # Check header noise
        if any(h in l_str.lower() for h in ['summative exam', 'end module', 'faculty of medicine', 'date:', 'time allowed', 'model:', 'page ', 'free phalasstine', 'docreader', 'doc-reader']):
            continue
            
        m_q = q_re.match(l_str)
        if m_q:
            if curr_q and curr_q.get('stem'):
                questions.append(curr_q)
            qnum = m_q.group(1) or m_q.group(2)
            stem = m_q.group(3).strip().strip('*').strip()
            curr_q = {'num': qnum, 'stem': stem, 'options': [], 'raw_lines': []}
            continue
            
        if curr_q is not None:
            m_opt = opt_re.match(l_str)
            if m_opt:
                letter = m_opt.group(1) or m_opt.group(2)
                otext = m_opt.group(3).strip().strip('*').strip()
                curr_q['options'].append((letter, otext))
            else:
                if not curr_q['options']:
                    curr_q['stem'] += ' ' + l_str
                else:
                    # continuation of last option
                    last_l, last_t = curr_q['options'][-1]
                    curr_q['options'][-1] = (last_l, last_t + ' ' + l_str)
                    
    if curr_q and curr_q.get('stem'):
        questions.append(curr_q)
        
    return questions

for fname in ['End 2019.md', 'End 2022.md', 'End 2023.md', 'End 2024.md', 'End 2026.md']:
    qs = parse_exam(fname)
    opt_counts = [len(q['options']) for q in qs]
    print(f'{fname:15s}: {len(qs)} Qs | avg options: {sum(opt_counts)/len(opt_counts):.1f} | min options: {min(opt_counts)} | max options: {max(opt_counts)}')
