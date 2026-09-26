import glob, json, re, os

cache_dir = 'scratch/mansoura_cache'
files = sorted(glob.glob(f'{cache_dir}/page_*.json'))

all_questions = []

for f in files:
    with open(f) as fp:
        halves = json.load(fp)
    for half in halves:
        p = half['page']
        side = half['side']
        txt = half['ocr']
        tbl_ans = half.get('answers', {})
        
        # Clean answers dict
        clean_tbl_ans = {}
        for k, v in tbl_ans.items():
            if v and v[0] in 'ABCDE':
                clean_tbl_ans[k] = v[0]
                
        ans_list = list(clean_tbl_ans.values())
        
        # Clean text
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
            
            # Options
            opt_matches = list(re.finditer(r'(?:^|\n)\s*([a-eA-E])[\)\.]\s+(.*?)(?=(?:^|\n)\s*[a-eA-E][\)\.]|\Z)', body, re.DOTALL))
            if not opt_matches or len(opt_matches) < 2: continue
            
            stem = body[:opt_matches[0].start()].strip().replace('\n', ' ')
            stem = re.sub(r'[\u0600-\u06FF]', '', stem).strip()
            
            opts = {}
            for om in opt_matches:
                let = om.group(1).upper()
                txt_opt = re.sub(r'[\u0600-\u06FF]', '', om.group(2)).strip().replace('\n', ' ')
                opts[let] = txt_opt
                
            half_qs.append({'page': p, 'side': side, 'q_num': q_num, 'stem': stem, 'options': opts})
            
        # Match answers
        for idx, q in enumerate(half_qs):
            # 1. Exact key match
            ans = clean_tbl_ans.get(q['q_num'])
            if ans and ans in q['options']:
                q['ans'] = ans
            # 2. Positional match
            elif idx < len(ans_list) and ans_list[idx] in q['options']:
                q['ans'] = ans_list[idx]
            else:
                # 3. Find any candidate from ans_list that is in q['options']
                cands = [a for a in ans_list if a in q['options']]
                if cands:
                    q['ans'] = cands[0]
                else:
                    # Fallback to standard answer if available
                    q['ans'] = sorted(list(q['options'].keys()))[0] # temporary fallback
                    q['fallback'] = True
                    
            if len(q['stem']) > 15 and len(q['options']) >= 2:
                all_questions.append(q)

print(f'Extracted {len(all_questions)} questions from Mansoura QBank.')
fallbacks = [q for q in all_questions if q.get('fallback')]
print(f'Questions requiring answer verification/refinement: {len(fallbacks)}')
mismatches = [q for q in all_questions if q['ans'] not in q['options']]
print(f'Option mismatches: {len(mismatches)}')
