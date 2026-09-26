import re

target_file = '/home/omar/MBset/اسيوط/Principles of microscopic and macroscopic structures/Markdown_Questions/33_Important_Anatomy_Qs_bank.md'
with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip bullet noise and AnyScanner noise across file 33
# 1. Clean bullet noise like '* * * '
content = re.sub(r'(-\s*\*\*[A-F]\*\*)\s*[\*•·\-\s@©®]+', r'\1 ', content)
# 2. Clean watermarks
content = re.sub(r'(?i)anyscanner|anyscan', '', content)
# 3. Clean trailing noise
content = re.sub(r'[\s@©®]+(?=\n|$)', '', content)

qs = content.split('### Question ')
header = qs[0]

cleaned_qs = []
discarded = 0

for i in range(1, len(qs)):
    q = qs[i].strip()
    lines = [l.strip() for l in q.split('\n') if l.strip()]
    num = lines[0]
    stem = lines[1] if len(lines) > 1 else ''
    opts = [l for l in lines if l.startswith('- **')]
    corr = [l for l in lines if l.startswith('**Correct Answer**:')]
    c_val = corr[0].split(':')[-1].strip() if corr else '-'
    
    # Clean stem of leading numbering noise like '1 A . . 5 ? joe '
    clean_stem = re.sub(r'^\d+\s*([A-Za-z\.\?\s_]{1,10})?', '', stem).strip()
    if len(clean_stem) < 15 or len(opts) < 2 and c_val != '-':
        discarded += 1
        continue
    
    # Clean options
    clean_opts = []
    for opt in opts:
        # remove internal OCR garbage
        clean_opt = re.sub(r'[\*•·@©®]+', '', opt).strip()
        clean_opts.append(clean_opt)
    
    # Rebuild question
    q_lines = [num, clean_stem] + clean_opts + [f'**Correct Answer**: {c_val}']
    cleaned_qs.append('\n\n'.join(q_lines) + '\n\n---\n')

print(f'Cleaned {len(cleaned_qs)} questions, discarded {discarded} unresolvable fragments')

new_content = header + '### Question ' + '### Question '.join(cleaned_qs)
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
