import os, re, glob, openpyxl

COLUMNS = [
    'id', 'Cas', 'Text', 'Image', 'explanationImage',
    'A', 'B', 'C', 'D', 'E', 'F',
    'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP',
    'Correct', 'Hint', 'EXP', 'Note', 'Type',
    'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
    'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks'
]

def clean_text(s):
    if not s:
        return ''
    s = re.sub(r'[\u0600-\u06FF]+', '', s)
    s = s.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    s = re.sub(r'^\s*(?:\d+[\.\-\)]|[A-Z][\.\)]|\- \*\*[A-F]\*\*)\s*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def normalize_key(stem, opts=None):
    # Full stem normalized
    s = clean_text(stem).lower()
    s = re.sub(r'[^a-z0-9]', '', s)
    if opts:
        # Append first 2 options to avoid false collisions of different questions with same vignette
        opt_s = ''.join(clean_text(o or '').lower() for o in opts[:2])
        opt_s = re.sub(r'[^a-z0-9]', '', opt_s)
        s = s + '_' + opt_s[:40]
    return s

def parse_md_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as fp:
        txt = fp.read()
        
    tag_match = re.search(r'\- \*\*Tag\*\*: `(.*?)`', txt)
    year_match = re.search(r'\- \*\*Year\*\*: (\d+)', txt)
    disc_match = re.search(r'\- \*\*Discipline / Subject\*\*: `(.*?)`', txt)
    
    tag = tag_match.group(1) if tag_match else 'Department'
    year = int(year_match.group(1)) if year_match else 2026
    disc_raw = disc_match.group(1) if disc_match else 'None'
    tag_suggere = disc_raw if disc_raw != 'None' else None
    
    # Split questions by '### Question <N>' or '### Q<N>:'
    blocks = re.split(r'###\s+(?:Question\s+\d+|Q\d+:|\d+\.|\d+\))\n+', txt)[1:]
    
    questions = []
    for b_idx, b in enumerate(blocks):
        b = b.strip()
        if not b:
            continue
            
        # Determine if QROC or QCS
        corr_match = re.search(r'\*\*Correct Answer\*\*:\s*([A-F\-]+)', b)
        correct_raw = corr_match.group(1).strip().upper() if corr_match else ''
        is_qroc = (correct_raw == '-') or ('**Type**: QROC' in b)
        
        # Explanation / Model answer
        exp_match = re.search(r'\*\*(?:EXP|Explanation)\*\*:\s*(.+?)(?:\n---|\Z)', b, re.DOTALL)
        exp = clean_text(exp_match.group(1)) if exp_match else None
        
        if is_qroc:
            q_type = 'QROC'
            correct = '-'
            # Stem is everything before **Correct Answer** or **Type** or **EXP**
            stem_part = re.split(r'\*\*(?:Correct Answer|Type|EXP|Explanation)\*\*:', b)[0].strip()
            stem = clean_text(stem_part)
            opts = [None] * 6
        else:
            q_type = 'QCS'
            correct = correct_raw if correct_raw in 'ABCDEF' else None
            # Stem is everything before first option - **A)**
            stem_part = b.split('- **A)**')[0].strip()
            stem = clean_text(stem_part)
            
            # Extract options
            opt_matches = re.findall(r'-\s+\*\*([A-F])\)\*\*\s*(.+)', b)
            opts = [None] * 6
            for ltr, otxt in opt_matches:
                idx = ord(ltr.upper()) - 65
                if 0 <= idx < 6:
                    opts[idx] = clean_text(otxt)
            
            # Validation: must have at least 2 options and valid correct answer
            if not opts[0] or not opts[1]:
                raise ValueError(f"File {fpath}, Question {b_idx+1}: Missing options for MCQ: {b[:100]}")
            if not correct or not opts[ord(correct)-65]:
                raise ValueError(f"File {fpath}, Question {b_idx+1}: Invalid or missing correct answer '{correct}': {b[:100]}")
        
        if len(stem) < 5:
            raise ValueError(f"File {fpath}, Question {b_idx+1}: Stem too short: '{stem}'")
            
        questions.append({
            'stem': stem,
            'type': q_type,
            'correct': correct,
            'exp': exp,
            'opts': opts,
            'tag': tag,
            'tagSuggere': tag_suggere,
            'year': year
        })
        
    return questions

def compile_all():
    files = sorted(glob.glob('renal/Markdown_Questions/*.md'))
    files = [f for f in files if '00_CATALOG' not in f]
    
    print(f'Compiling from {len(files)} markdown files...')
    
    total_raw_qs = 0
    dedup_dict = {}
    
    for f in files:
        qs = parse_md_file(f)
        total_raw_qs += len(qs)
        for q in qs:
            norm = normalize_key(q['stem'], q['opts'])
            if norm not in dedup_dict:
                dedup_dict[norm] = q
            else:
                existing = dedup_dict[norm]
                # Merge tags without duplicates
                tags_set = [t.strip() for t in existing['tag'].split(',') if t.strip()]
                new_tags = [t.strip() for t in q['tag'].split(',') if t.strip()]
                for nt in new_tags:
                    if nt not in tags_set:
                        tags_set.append(nt)
                existing['tag'] = ', '.join(tags_set)
                
                # Keep QCS over QROC, but preserve explanation
                if existing['type'] == 'QROC' and q['type'] == 'QCS':
                    q['exp'] = existing['exp'] or q['exp']
                    q['tag'] = existing['tag']
                    dedup_dict[norm] = q
                elif existing['type'] == 'QCS' and q['type'] == 'QROC':
                    if not existing['exp'] and q['exp']:
                        existing['exp'] = q['exp']
                else:
                    if not existing['exp'] and q['exp']:
                        existing['exp'] = q['exp']
                    # Keep latest year
                    existing['year'] = max(existing['year'], q['year'])
                    if not existing['tagSuggere'] and q['tagSuggere']:
                        existing['tagSuggere'] = q['tagSuggere']

    print(f'Total raw questions: {total_raw_qs}')
    print(f'Total unique questions after deduplication: {len(dedup_dict)}')
    
    # Build Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Questions'
    ws.append(COLUMNS)
    
    for norm, q in dedup_dict.items():
        row = [
            None,                       # id (MUST be None)
            None,                       # Cas
            q['stem'],                  # Text
            None,                       # Image
            None,                       # explanationImage
            q['opts'][0],               # A
            q['opts'][1],               # B
            q['opts'][2],               # C
            q['opts'][3],               # D
            q['opts'][4],               # E
            q['opts'][5],               # F
            None, None, None, None, None, None, # A_EXP - F_EXP
            q['correct'],               # Correct
            None,                       # Hint
            q['exp'],                   # EXP
            None,                       # Note
            q['type'],                  # Type
            'DamiettaFa_RENAL',         # categoryId
            'Renal',                    # categoryName
            None,                       # subcategoryId (MUST be None)
            None,                       # subcategoryName (MUST be None)
            q['tagSuggere'],            # tagSuggere
            q['year'],                  # Year
            q['tag'],                   # Tag
            None,                       # ImageMasks
            None                        # ExplanationImageMasks
        ]
        ws.append(row)
        
    out_xlsx = 'renal/Renal_Questions.xlsx'
    wb.save(out_xlsx)
    print(f'Saved master question bank to {out_xlsx} with {len(dedup_dict)} rows.')

if __name__ == '__main__':
    compile_all()
