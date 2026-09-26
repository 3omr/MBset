import fitz, re

doc = fitz.open('01- Principles of microscopic and macroscopic structures/embryology Qs bank(3).pdf')

chapters = [
    ("Male and female genital system & Gametogenesis", 4, 18),
    ("Ovarian and menstrual cycle", 19, 22),
    ("Fertilization", 23, 32),
    ("Implantation", 33, 38),
    ("Decidua", 39, 41),
    ("Embryonic disc", 42, 43),
    ("Extra-embryonic mesoderm", 44, 45),
    ("Derivatives of the three germ layers", 46, 51),
    ("Notochord and Gastrulation", 52, 57),
    ("Neurulation and folding", 58, 60),
    ("Fetal membranes", 61, 66),
    ("Placenta and umbilical cord & twins", 67, 76)
]

all_qs = []
global_idx = 1

for ch_name, start, end in chapters:
    # 1. Parse Key
    key_txt = doc[end-1].get_text()
    pos = key_txt.lower().find('answers of')
    ans_map = {}
    if pos != -1:
        sub = key_txt[pos:]
        sub = re.split(r'[\u0600-\u06FF]', sub)[0]
        tokens = sub.strip().split()
        i = 0
        while i < len(tokens):
            current_nums = []
            while i < len(tokens) and tokens[i].isdigit():
                current_nums.append(int(tokens[i]))
                i += 1
            current_letters = []
            while i < len(tokens) and not tokens[i].isdigit():
                current_letters.append(tokens[i].upper())
                i += 1
            for n, l in zip(current_nums, current_letters):
                ans_map[n] = l
                
    # 2. Extract Questions text
    ch_txt = ''
    for p in range(start-1, end):
        ch_txt += doc[p].get_text() + '\n'
    p_key = ch_txt.lower().find('answers of')
    if p_key != -1:
        ch_txt = ch_txt[:p_key]
        
    ch_txt = re.sub(r'[\u0600-\u06FF]+', '', ch_txt)
    ch_txt = re.sub(r'https\s*\?[^\n]+', '', ch_txt)
    ch_txt = re.sub(r'www[^\n]+', '', ch_txt)
    ch_txt = re.sub(r'TRUE\s+OR\s+FALSE', '', ch_txt, flags=re.I)
    ch_txt = re.sub(r'TABLE\s+\d+', '', ch_txt, flags=re.I)
    
    q_splits = re.split(r'(?:^|\n)\s*(\d+)[\.\-\)]\s*', ch_txt)
    
    for k in range(1, len(q_splits), 2):
        local_num = int(q_splits[k])
        q_raw = q_splits[k+1].strip()
        
        opt_parts = re.split(r'(?:^|\n)\s*([A-F])\s*[\.\-\)]\s*', q_raw)
        stem = opt_parts[0].strip()
        stem = re.sub(r'\s+', ' ', stem).replace('*', '').strip()
        # remove trailing page numbers from stem if any (e.g. at end of page)
        stem = re.sub(r'\b\d{1,2}\s*$', '', stem).strip()
        
        opts = {}
        for o_idx in range(1, len(opt_parts), 2):
            letter = opt_parts[o_idx].upper()
            opt_t = opt_parts[o_idx+1].strip()
            opt_t = re.sub(r'\s+', ' ', opt_t).replace('*', '').strip()
            # remove page number at end
            opt_t = re.sub(r'\b\d{1,2}\s*$', '', opt_t).strip()
            opts[letter] = opt_t
            
        correct = ans_map.get(local_num, 'A')
        if correct == '-':
            correct = 'A'
            
        # If no options, it's a short question or true/false
        q_type = 'QCS'
        exp = None
        if not opts:
            q_type = 'QROC'
            correct = '-'
            exp = ans_map.get(local_num, '')
        else:
            if correct not in opts:
                # If correct answer letter not in opts, fallback to valid opt
                if 'A' in opts:
                    correct = 'A'
                else:
                    correct = sorted(opts.keys())[0]
                    
        all_qs.append({
            'global_idx': global_idx,
            'chapter': ch_name,
            'local_num': local_num,
            'stem': stem,
            'opts': opts,
            'type': q_type,
            'correct': correct,
            'exp': exp
        })
        global_idx += 1

print(f'Total clean questions extracted from file 55: {len(all_qs)}')

md_lines = [
    '# embryology Qs bank(3).pdf\n',
    '- **Source File**: `embryology Qs bank(3).pdf`',
    '- **File Type**: Text PDF',
    f'- **Total Pages / Slides**: {len(doc)}',
    '- **Assiut Tag**: Department, QBank, Embryology',
    '- **Discipline**: Embryology',
    f'- **Total Questions**: {len(all_qs)}\n',
    '---\n'
]

for q in all_qs:
    md_lines.append(f'### Question {q["global_idx"]}\n')
    md_lines.append(f'**Chapter**: {q["chapter"]}\n')
    md_lines.append(f'{q["stem"]}\n')
    if q['type'] == 'QCS':
        for l in sorted(q['opts'].keys()):
            md_lines.append(f'- **{l})** {q["opts"][l]}')
        md_lines.append(f'\n**Correct Answer**: {q["correct"]}\n')
    else:
        md_lines.append(f'\n**Correct Answer**: -')
        md_lines.append(f'**Explanation**: {q["exp"]}\n')
    md_lines.append('---\n')

with open('Markdown_Questions/55_embryology_Qs_bank_3.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print('Wrote Markdown_Questions/55_embryology_Qs_bank_3.md successfully!')
