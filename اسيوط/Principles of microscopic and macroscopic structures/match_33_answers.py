import re, os

md_dir = '/home/omar/MBset/اسيوط/Principles of microscopic and macroscopic structures/Markdown_Questions'

ref_files = ['75_مذكرة_حل_احمد_صلاح_pms.md', '06_Anatomy_Qs_Bank_3.md', '07_Anatomy_Qs_Bank_4.md', '64_q_bank_anatomy.md']
clean_database = []

for rf in ref_files:
    path = os.path.join(md_dir, rf)
    with open(path) as fp:
        content = fp.read()
    for q in content.split('### Question ')[1:]:
        lines = [l.strip() for l in q.split('\n') if l.strip()]
        stem = lines[1] if len(lines) > 1 else ''
        opts = [l for l in lines if re.match(r'-\s*\*\*[A-F]\)', l)]
        corr = [l for l in lines if l.startswith('**Correct Answer**:')]
        c_val = corr[0].split(':')[-1].strip() if corr else ''
        if opts and c_val in ['A', 'B', 'C', 'D', 'E', 'F']:
            words = set(re.findall(r'[a-zA-Z]{4,}', stem.lower()))
            clean_database.append((words, stem, opts, c_val))

print(f'Total reference questions loaded: {len(clean_database)}')

target_file = os.path.join(md_dir, '33_Important_Anatomy_Qs_bank.md')
with open(target_file) as fp:
    t33 = fp.read()

qs = t33.split('### Question ')
out_qs = [qs[0]]

matched_count = 0

for i in range(1, len(qs)):
    q = qs[i]
    lines = [l.strip() for l in q.split('\n') if l.strip()]
    num = lines[0]
    stem = lines[1] if len(lines) > 1 else ''
    opts = [l for l in lines if re.match(r'-\s*\*\*[A-F]\)', l)]
    corr = [l for l in lines if l.startswith('**Correct Answer**:')]
    c_val = corr[0].split(':')[-1].strip() if corr else '-'
    
    q_words = set(re.findall(r'[a-zA-Z]{4,}', stem.lower()))
    
    best_match = None
    best_overlap = 0
    
    if len(q_words) >= 3:
        for ref_words, ref_stem, ref_opts, ref_c in clean_database:
            overlap = len(q_words.intersection(ref_words))
            if overlap > best_overlap and overlap >= 3:
                best_overlap = overlap
                best_match = (ref_stem, ref_opts, ref_c)
    
    if best_match and c_val == 'A':
        ref_stem, ref_opts, ref_c = best_match
        ref_ans_text = ''
        for ropt in ref_opts:
            if ropt.startswith(f'- **{ref_c})**'):
                ref_ans_text = ropt[8:].strip().lower()
                break
        
        target_c = None
        if ref_ans_text:
            for opt in opts:
                let = opt[4:5]
                words_ans = [w for w in ref_ans_text.split() if len(w) > 3]
                if words_ans and any(w in opt.lower() for w in words_ans):
                    target_c = let
                    break
        
        if not target_c and ref_c in [o[4:5] for o in opts]:
            target_c = ref_c
        
        if target_c and target_c != 'A':
            q = re.sub(r'\*\*Correct Answer\*\*:\s*.*', f'**Correct Answer**: {target_c}', q)
            matched_count += 1
    
    out_qs.append(q)

new_content = '### Question '.join(out_qs)
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Successfully matched and updated {matched_count} questions in 33!')
