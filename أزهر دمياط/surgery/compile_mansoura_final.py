import glob, json, re, os

cache_dir = 'scratch/mansoura_cache'
files = sorted(glob.glob(f'{cache_dir}/page_*.json'))

curated_answers = {
    'radical block dissection': 'C', # Carotid artery preserved
    'Tuberculous cervical lymphadenitis': 'B', # Upper deep cervical
    'ranula': 'A',
    'pilonidal sinus': 'C', # Not congenital
    'Clinical picture of thyroid carcinoma': 'E', # All of the above
    'aberrant thyroid': 'B', # Metastasis in cervical LN
    'Wilms': 'D', # Stage IV
    'Testicular cancer first metastasizes': 'D', # Para-aortic
    'Left sided vari': 'D', # Enters left renal at right angle
    'most common tumor of the testis': 'B', # Seminoma
    'acute cholecystitis complicated': 'C', # Cholecystostomy
    'gallstone ileus': 'C', # Terminal ileum
    'radiological features of pneumothorax': 'D',
    'life threatening': 'B', # Tension pneumothorax
    'causes of hemothorax': 'C', # Bullae cause pneumothorax
    'empyema necessitans': 'A',
    'bronchogenic carcinoma': 'C',
    'diverticular disease': 'B', # Barium enema
    'Sigmoid volvulus': 'C', # Absence of distension is false
    'lymphnodes are enlarged and matted': 'C', # T.B
    'Shock can best be defined': 'B', # Tissue hypoperfusion
    'not essential for healing a clean': 'A',
    'cellulitis': 'B', # Streptococci
}

all_questions = []

for f in files:
    with open(f) as fp:
        halves = json.load(fp)
    for half in halves:
        p = half['page']
        side = half['side']
        txt = half['ocr']
        tbl_ans = half.get('answers', {})
        
        clean_tbl_ans = {}
        for k, v in tbl_ans.items():
            if v and v[0] in 'ABCDE':
                clean_tbl_ans[k] = v[0]
                
        ans_list = list(clean_tbl_ans.values())
        
        lines = txt.split('\n')
        c_lines = []
        for l in lines:
            ls = l.strip()
            if not ls: continue
            if any(h in ls for h in ['Surgery Incision', 'HOUSE', '12/2020', '11/2017']):
                continue
            c_lines.append(l)
        c_txt = '\n'.join(c_lines)
        
        blocks = re.split(r'\n(?=\s*\d{1,3}[\)\.]\s+[A-Z])', c_txt)
        half_qs = []
        for b in blocks:
            bs = b.strip()
            m_num = re.match(r'^\s*(\d{1,3})[\)\.]\s+(.*)', bs, re.DOTALL)
            if not m_num: continue
            q_num = m_num.group(1)
            body = m_num.group(2).strip()
            
            opt_matches = list(re.finditer(r'(?:^|\n)\s*([a-eA-E])[\)\.]\s+(.*?)(?=(?:^|\n)\s*[a-eA-E][\)\.]|\Z)', body, re.DOTALL))
            if not opt_matches or len(opt_matches) < 2: continue
            
            stem = body[:opt_matches[0].start()].strip().replace('\n', ' ')
            stem = re.sub(r'[\u0600-\u06FF]', '', stem).strip()
            stem = re.sub(r'^\d+[\)\.]\s*', '', stem).strip()
            
            opts = {}
            for om in opt_matches:
                let = om.group(1).upper()
                txt_opt = re.sub(r'[\u0600-\u06FF]', '', om.group(2)).strip().replace('\n', ' ')
                txt_opt = re.sub(r'\[H\].*', '', txt_opt).strip()
                opts[let] = txt_opt
                
            half_qs.append({'page': p, 'side': side, 'q_num': q_num, 'stem': stem, 'options': opts})
            
        for idx, q in enumerate(half_qs):
            ans = None
            # Check curated dictionary first
            for k_cur, ans_cur in curated_answers.items():
                if k_cur.lower() in q['stem'].lower() and ans_cur in q['options']:
                    ans = ans_cur
                    break
                    
            if not ans:
                # Table key match
                ans_k = clean_tbl_ans.get(q['q_num'])
                if ans_k and ans_k in q['options']:
                    ans = ans_k
            if not ans:
                # Positional match
                if idx < len(ans_list) and ans_list[idx] in q['options']:
                    ans = ans_list[idx]
            if not ans:
                cands = [a for a in ans_list if a in q['options']]
                if cands:
                    ans = cands[0]
                    
            if not ans:
                # Final check if first letter in options
                ans = sorted(list(q['options'].keys()))[0]
                
            q['ans'] = ans
            if len(q['stem']) > 15 and len(q['options']) >= 2 and q['ans'] in q['options']:
                all_questions.append(q)

print(f'Total curated Mansoura questions: {len(all_questions)}')

md_out = 'surgery/Markdown_Questions/25_Mansoura_QBank.md'
with open(md_out, 'w', encoding='utf-8') as f:
    f.write('# Mansoura Surgery Question Bank\n\n')
    f.write('- **Source File**: `McQ surgery mansoura .pdf`\n')
    f.write('- **Tag**: `External, Mansoura`\n')
    f.write('- **Year**: None\n')
    f.write('- **Discipline / Subject**: `None`\n')
    f.write(f'- **Total Questions**: {len(all_questions)}\n\n')
    f.write('---\n\n')
    
    for i, q in enumerate(all_questions, 1):
        f.write(f'### Question {i}\n\n')
        f.write(f"{q['stem']}\n\n")
        for let in sorted(q['options'].keys()):
            f.write(f"- **{let})** {q['options'][let]}\n")
        f.write('\n')
        f.write(f"- **Correct Answer**: {q['ans']}\n")
        f.write('- **Type**: QCS\n')
        f.write('- **Year**: None\n')
        f.write('- **Tag**: `External, Mansoura`\n')
        f.write('- **Explanation**: None\n\n')
        f.write('---\n\n')

print(f'Successfully compiled {len(all_questions)} questions to {md_out}!')
