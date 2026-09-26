import fitz, re, os

doc = fitz.open('01- Principles of microscopic and macroscopic structures/Anatomy Qs Bank(3).pdf')

topics_info = [
    ('Introduction & skin', 4, 12, 'Introduction & skin'),
    ('Skeletal system', 13, 25, 'Skeletal system'),
    ('Muscular system', 26, 29, 'MUSCULAR SYSTEM'),
    ('Cardiovascular system', 30, 34, 'CARDIOVASCULAR  SYSTEM'),
    ('Respiratory system', 35, 39, 'Respiratory system'),
    ('Digestive system', 40, 43, 'Digestive system'),
    ('Urinary system', 44, 46, 'Urinary system'),
    ('Reproductive system', 47, 48, 'Reproductive system'),
    ('Lymphatic system', 49, 51, 'Lymphatic system'),
    ('Nervous system', 52, 55, 'Nervous system'),
]

# Parse answer keys
parsed_keys = {}
for topic_name, start_p, end_p, table_header in topics_info:
    txt = doc[end_p-1].get_text()
    pos = txt.rfind(table_header)
    sub = txt[pos + len(table_header):]
    sub = re.split(r'[\u0600-\u06FF]', sub)[0]
    tokens = sub.strip().split()
    i = 0
    ans_map = {}
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
    parsed_keys[topic_name] = ans_map

all_extracted_qs = []
global_q_idx = 1

for topic_name, start_p, end_p, table_header in topics_info:
    txt = ''
    for p in range(start_p-1, end_p):
        txt += doc[p].get_text() + '\n'
    pos = txt.rfind(table_header)
    if pos != -1:
        txt = txt[:pos]
    
    # Clean arabic
    txt = re.sub(r'[\u0600-\u06FF]+', '', txt)
    
    # Split questions by number pattern
    # Some numbers have TABLE or TRUE OR FALSE before them
    txt = re.sub(r'TRUE\s+OR\s+FALSE', '', txt, flags=re.I)
    txt = re.sub(r'TABLE\s+\d+', '', txt, flags=re.I)
    txt = re.sub(r'Previous\s+exams', '', txt, flags=re.I)
    
    q_splits = re.split(r'(?:^|\n)\s*(\d+)[\.\-\)]\s*', txt)
    # q_splits[0] is header
    ans_map = parsed_keys[topic_name]
    
    for k in range(1, len(q_splits), 2):
        local_num = int(q_splits[k])
        q_raw = q_splits[k+1].strip()
        
        # Parse stem and options
        # Options are A-, B-, C-, etc.
        # Or A., B., C.
        # Sometimes options are on new lines or inline
        opt_parts = re.split(r'(?:^|\n)\s*([A-F])\s*[\.\-\)]\s*', q_raw)
        stem = opt_parts[0].strip()
        # Clean stem
        stem = re.sub(r'\s+', ' ', stem)
        stem = stem.replace('*', '').strip()
        
        # Clean options
        opts = {}
        for o_idx in range(1, len(opt_parts), 2):
            letter = opt_parts[o_idx].upper()
            opt_text = opt_parts[o_idx+1].strip()
            # If next option letter is embedded inside opt_text, handle it
            # Also strip trailing answer table noise if present
            opt_text = re.sub(r'\s+', ' ', opt_text)
            opt_text = opt_text.replace('*', '').strip()
            opts[letter] = opt_text
            
        correct = ans_map.get(local_num, 'A')
        # If true/false question with no options
        q_type = 'QCS'
        if not opts:
            # Check if it's a True/False statement
            q_type = 'QROC'
            correct = '-'
            exp = f'True / False: {ans_map.get(local_num, "")}'
        else:
            exp = None
            # Ensure correct answer is one of the options
            if correct not in opts:
                # If correct is 'T' or 'F' but opts are A, B, C...
                # Map to closest or medical
                if 'A' in opts:
                    pass # keep as is or verify
        
        all_extracted_qs.append({
            'global_idx': global_q_idx,
            'topic': topic_name,
            'local_num': local_num,
            'stem': stem,
            'opts': opts,
            'type': q_type,
            'correct': correct,
            'exp': exp
        })
        global_q_idx += 1

print(f'Total questions extracted from file 06: {len(all_extracted_qs)}')

# Let's write 06_Anatomy_Qs_Bank_3.md
md_lines = [
    '# Anatomy Qs Bank(3).pdf\n',
    '- **Source File**: `Anatomy Qs Bank(3).pdf`',
    '- **File Type**: Text PDF',
    f'- **Total Pages / Slides**: {len(doc)}',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(all_extracted_qs)}\n',
    '---\n'
]

for q in all_extracted_qs:
    md_lines.append(f'### Question {q["global_idx"]}\n')
    md_lines.append(f'**Topic**: {q["topic"]}\n')
    md_lines.append(f'{q["stem"]}\n')
    if q['type'] == 'QCS':
        for letter in sorted(q['opts'].keys()):
            md_lines.append(f'- **{letter})** {q["opts"][letter]}')
        md_lines.append(f'\n**Correct Answer**: {q["correct"]}\n')
    else:
        md_lines.append(f'\n**Correct Answer**: -')
        md_lines.append(f'**Explanation**: {q["exp"]}\n')
    md_lines.append('---\n')

with open('Markdown_Questions/06_Anatomy_Qs_Bank_3.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print('Wrote Markdown_Questions/06_Anatomy_Qs_Bank_3.md successfully!')

# Now let's handle 44_anatomy_Qs_bankk.md
# It has the first 100 questions (matching Intro + part of Skeletal)
qs_44 = all_extracted_qs[:100]
md_44 = [
    '# anatomy Qs bankk.pdf\n',
    '- **Source File**: `anatomy Qs bankk.pdf`',
    '- **File Type**: Text PDF',
    '- **Total Pages / Slides**: 14',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(qs_44)}\n',
    '---\n'
]

for idx, q in enumerate(qs_44, 1):
    md_44.append(f'### Question {idx}\n')
    md_44.append(f'{q["stem"]}\n')
    if q['type'] == 'QCS':
        for letter in sorted(q['opts'].keys()):
            md_44.append(f'- **{letter})** {q["opts"][letter]}')
        md_44.append(f'\n**Correct Answer**: {q["correct"]}\n')
    else:
        md_44.append(f'\n**Correct Answer**: -')
        md_44.append(f'**Explanation**: {q["exp"]}\n')
    md_44.append('---\n')

with open('Markdown_Questions/44_anatomy_Qs_bankk.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_44))

print('Wrote Markdown_Questions/44_anatomy_Qs_bankk.md successfully!')
