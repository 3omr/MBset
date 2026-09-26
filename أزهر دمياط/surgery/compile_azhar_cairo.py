import os, re, glob

ocr_dir = '/home/omar/.gemini/antigravity/brain/33aa757e-e03d-4fcf-ae5d-db89a47b0b0e/scratch/ocr'
red_sec2_dir = 'scratch/azhar_sec2_red'

sec2_answers = {
    1:'D', 2:'B', 3:'C', 4:'C', 5:'C', 6:'D', 7:'A', 8:'C', 9:'A',
    10:'D', 11:'C', 12:'B', 13:'A', 14:'C', 15:'C', 16:'A', 17:'A', 18:'A',
    19:'D', 20:'B', 21:'E', 22:'B', 23:'B', 24:'D', 25:'A', 26:'D', 27:'A', 28:'D', 29:'C',
    30:'C', 31:'D', 32:'A', 33:'D', 34:'C', 35:'A', 36:'A', 37:'D', 38:'D', 39:'B', 40:'B', 41:'B', 42:'D'
}

sections = [
    (1, 8, 'Pre- and Post-operative Care & Surgical Critical Care'),
    (9, 16, 'Shock, Haemorrhage & Blood Transfusion'),
    (17, 32, 'Wound, Healing & Trauma'),
    (33, 51, 'Fluid & Metabolic Support'),
    (52, 61, 'Allergy, Infections, Skin & Burns'),
    (62, 71, 'Breast'),
    (72, 74, 'Head & Neck'),
    (75, 83, 'Vascular Surgery'),
    (84, 88, 'Hernia')
]

def clean_ocr(text):
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        if not s:
            cleaned.append('')
            continue
        if re.search(r'Page\s*\|\s*\d+', s, re.I): continue
        if re.search(r'^\s*\d+\s*[-—]\s*$', s): continue
        if any(h in s.upper() for h in ['BASIC SURGERY', 'BASICS OF SURGERY', 'MCQ CLINICAL', 'BY: MOHAMED ALAA', 'MCO CLINICAL', 'SHOCK']):
            continue
        cleaned.append(l)
    t = '\n'.join(cleaned)
    t = t.replace('©)', 'c)').replace('¢)', 'c)').replace('€)', 'e)').replace('@)', 'e)')
    t = t.replace('©.', 'c.').replace('¢.', 'c.').replace('€.', 'e.').replace('@.', 'e.')
    t = t.replace('¢', 'c').replace('©', 'c').replace('«', '').replace('»', '')
    t = re.sub(r'\b[Jj]s\b', 'is', t)
    return t

def parse_options(block, default_ans):
    ans = default_ans
    if not ans:
        ans_m = re.search(r'(?:[Aa]nswer|The answer)\s*:?\s*(?:is|js)?\s*\(?\s*([A-Fa-f0-9])\s*\)?', block, re.I)
        if ans_m:
            char = ans_m.group(1).upper()
            if char == '2': char = 'A'
            ans = char
            
    # Remove ONLY the answer line, leaving any subsequent options intact!
    clean_block = re.sub(r'\n\s*(?:[Aa]nswer|The answer)\s*:?\s*(?:is|js)?\s*\(?\s*[A-Fa-f0-9]\s*\)?[\.\s]*', '\n', block, flags=re.I).strip()
    clean_block = re.sub(r'^\s*(?:\d{1,2}|[&~])\s*[\.,\)&~]\s*', '', clean_block)
    
    # Replace common symbol distortions
    clean_block = clean_block.replace('©)', 'c)').replace('¢)', 'c)').replace('€)', 'e)').replace('@)', 'e)')
    clean_block = clean_block.replace('oe 6', 'd)').replace('o)', 'e)')
    
    lines = clean_block.split('\n')
    stem_lines = []
    opt_chunks = []
    in_opts = False
    
    for l in lines:
        l_str = l.strip()
        if not l_str: continue
        if re.search(r'^[a-fA-F][\)\.]\s+', l_str):
            in_opts = True
        if in_opts:
            parts = re.split(r'(?<=\S)\s+(?=[a-fA-F][\)\.]\s+)', l_str)
            for p in parts:
                p_str = p.strip()
                if re.match(r'^[a-fA-F][\)\.]\s+', p_str):
                    opt_chunks.append(p_str)
                elif opt_chunks:
                    opt_chunks[-1] += ' ' + p_str
                else:
                    stem_lines.append(p_str)
        else:
            stem_lines.append(l_str)
            
    stem = ' '.join(stem_lines).strip()
    stem = re.sub(r'^(?:DIRECTIONS:.*?\n|Is the BEST in each Case\.?\s*)', '', stem, flags=re.I).strip()
    stem = re.sub(r'[\u0600-\u06FF]', '', stem).strip()
    
    options = {}
    for opt in opt_chunks:
        m = re.match(r'^([a-fA-F])[\)\.]\s+(.*)', opt)
        if m:
            let = m.group(1).upper()
            body = m.group(2).strip()
            # If body has internal option like "foo d) bar"
            sub_m = re.search(r'(.*?)\s+([b-fB-F])[\)\.]\s+(.*)', body)
            if sub_m:
                options[let] = re.sub(r'[\u0600-\u06FF]', '', sub_m.group(1)).strip()
                sub_let = sub_m.group(2).upper()
                options[sub_let] = re.sub(r'[\u0600-\u06FF]', '', sub_m.group(3)).strip()
            else:
                body = re.sub(r'[\u0600-\u06FF]', '', body).strip()
                options[let] = body
            
    if not stem or len(options) < 2 or not ans:
        return None
        
    return {
        'stem': stem,
        'options': options,
        'answer': ans
    }

all_questions = []

for start_p, end_p, sec_name in sections:
    print(f'Processing {sec_name} (Pages {start_p}-{end_p})...')
    if start_p == 9:
        txt = '\n'.join([clean_ocr(open(f'{red_sec2_dir}/page_{p:02d}.txt').read()) for p in range(9, 17)])
        dir_m = re.search(r'DIRECTIONS:.*?\n\s*\n', txt, re.DOTALL | re.I)
        if dir_m:
            txt = txt[dir_m.end():]
        raw_splits = re.split(r'\n(?=\s*(?:\d{1,2}(?:[\.,\)]|\s+)|6&)\s+[A-Z])', txt)
        q_idx = 1
        for s in raw_splits:
            s_str = s.strip()
            if len(s_str) < 25 or 'DIRECTIONS:' in s_str: continue
            ans_let = sec2_answers.get(q_idx, 'A')
            parsed = parse_options(s_str, ans_let)
            if parsed:
                parsed['section'] = sec_name
                all_questions.append(parsed)
                q_idx += 1
    else:
        txt = '\n'.join([clean_ocr(open(f'{ocr_dir}/page_{p:02d}.txt').read()) for p in range(start_p, end_p+1)])
        dir_m = re.search(r'DIRECTIONS:.*?\n\s*\n', txt, re.DOTALL | re.I)
        if dir_m:
            txt = txt[dir_m.end():]
        ans_pattern = r'((?:[Aa]nswer|The answer)\s*:?\s*(?:is\s*)?\(?\s*([A-Fa-f0-9])\s*\)?[\.\s]*)'
        parts = re.split(ans_pattern, txt)
        for i in range(0, len(parts)-2, 3):
            q_text = parts[i].strip()
            ans_let = parts[i+2].upper()
            if ans_let == '2': ans_let = 'A'
            if len(q_text) > 20:
                parsed = parse_options(q_text, ans_let)
                if parsed:
                    parsed['section'] = sec_name
                    all_questions.append(parsed)

print(f'\nTotal extracted questions: {len(all_questions)}')

md_out = 'surgery/Markdown_Questions/24_Azhar_Cairo_QBank.md'
with open(md_out, 'w', encoding='utf-8') as f:
    f.write('# Azhar Cairo Surgery Question Bank\n\n')
    f.write('- **Source File**: `بنك أزهر القاهرة .pdf`\n')
    f.write('- **Tag**: `External, Azhar Cairo`\n')
    f.write('- **Year**: None\n')
    f.write('- **Discipline / Subject**: `None`\n')
    f.write(f'- **Total Questions**: {len(all_questions)}\n\n')
    f.write('---\n\n')
    
    cur_sec = None
    for i, q in enumerate(all_questions, 1):
        sec = q.get('section', '')
        if sec != cur_sec:
            cur_sec = sec
            f.write(f'## {cur_sec}\n\n')
            
        f.write(f'### Question {i}\n\n')
        f.write(f"{q['stem']}\n\n")
        for let in sorted(q['options'].keys()):
            f.write(f"- **{let})** {q['options'][let]}\n")
        f.write('\n')
        f.write(f"- **Correct Answer**: {q['answer']}\n")
        f.write('- **Type**: QCS\n')
        f.write('- **Year**: None\n')
        f.write('- **Tag**: `External, Azhar Cairo`\n')
        f.write('- **Explanation**: None\n\n')
        f.write('---\n\n')

print(f'Successfully wrote {len(all_questions)} questions to {md_out}!')
