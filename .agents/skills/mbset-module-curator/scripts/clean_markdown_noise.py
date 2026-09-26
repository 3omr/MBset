#!/usr/bin/env python3
"""
MBset Deep Noise Removal Utility
Performs automated inspection, cleaning, and normalization of question Markdown files
according to the MBset Medical Module Curation Standard.
"""

import os
import sys
import re
import glob
import argparse

ARABIC_REGEX = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

def clean_text_common(text: str) -> str:
    if not text:
        return ""
    # Strip invisible unicode
    text = text.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    # Normalize quotes
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    return text

def remove_arabic(text: str) -> str:
    if not text:
        return ""
    return ARABIC_REGEX.sub('', text)

def parse_inline_options(rest: str) -> dict:
    """
    Parses inline options following 'Select one:' (e.g. 'a. Option A b. Option B ...')
    """
    rest = re.sub(r'[@©®O\–\—\•\·\>]+', ' ', rest)
    rest = re.sub(r'c¢\.', 'c.', rest)
    rest = re.sub(r'dq\.', 'd.', rest)
    
    opt_matches = list(re.finditer(r'(?:^|\s+)([a-fA-F])[\.\)]\s*(.*?)(?=(?:\s+[a-fA-F][\.\)]|\Z))', rest, re.S))
    options = {}
    for om in opt_matches:
        let = om.group(1).upper()
        otext = re.sub(r'\s+', ' ', om.group(2)).strip()
        otext = re.sub(r'\b(?:Your answer is|The correct answer is).*', '', otext, flags=re.I).strip()
        otext = re.sub(r'[@©®\–\—\•\·\>]+', '', otext).strip()
        otext = re.sub(r'\b(?:Select\s+one|Quiz\s+\d+).*', '', otext, flags=re.I).strip()
        otext = remove_arabic(otext).strip()
        if len(otext) > 0:
            options[let] = otext
    return options

def clean_option_text(otext: str) -> str:
    if not otext:
        return ""
    # 1. Strip matching table headers
    otext = re.sub(r'(?i)\s*TABLE\s+\d+\s+A\s+B.*', '', otext).strip()
    # 2. Strip trailing answer key tables
    otext = re.sub(
        r'(?i)\s*(?:Answers?\s+of\s+|Answer\s+of\s+|Skeletal\s+system|MUSCULAR\s+SYSTEM|CARDIOVASCULAR\s+SYSTEM|'
        r'Respiratory\s+system|Digestive\s+system|Urinary\s+system|Reproductive\s+system|Lymphatic\s+system|'
        r'Nervous\s+system|Introduction\s*&\s*skin|MICROSCOPIC\s+ANSWER|Cytology|Nucleus|Cell\s+cycle|Stem\s+cells|'
        r'BLOOD|CONNECTIVE\s+TISSUE|BONE)\s+(?:[0-9]\s+[0-9]|[A-E]\s+[A-E]).*',
        '', otext
    ).strip()
    # 3. Strip bubble OCR artifacts
    otext = re.sub(r'[@©®]{2,}|\b[A-E]\s*[\)\]\.]\s*[@©®]', '', otext).strip()
    otext = re.sub(r'^[@©®\s\.\,\-\)]+', '', otext).strip()
    # 4. Strip LMS UI markers
    otext = re.sub(r'\b(?:Select\s+one|Quiz\s+\d+).*', '', otext, flags=re.I).strip()
    # 5. Remove Arabic
    otext = remove_arabic(otext).strip()
    return otext

def clean_markdown_content(content: str) -> str:
    """
    Cleans raw or semi-processed markdown content according to MBset noise removal standards.
    """
    content = clean_text_common(content)
    
    parts = content.split('### Question ')
    if len(parts) <= 1:
        # Fallback if questions are not formatted as '### Question '
        return content
        
    header = parts[0]
    cleaned_questions = []
    prev_exp = ''
    
    for i in range(1, len(parts)):
        body = parts[i]
        
        # 1. Filter out pure garbage/corrupted blocks
        if re.search(r'TABLE\s+\d+\s+A\s+B\s+\d+\-\s+Flexion|The correct answer is:\s*mrNA Actin is thin filaments|qhe ovulated mammatia', body, re.I):
            continue
            
        # Filter orphan matching table fragment with only E/F options
        if re.search(r'-\s*\*\*([EF])\)\*\*.*TABLE\s+\d+\s+A\s+B', body, re.I) and len(re.findall(r'-\s*\*\*[A-F]\)\*\*', body)) <= 2:
            continue
            
        # 2. Extract explanation and correct answer
        exp_m = re.search(r'\*\*(?:Explanation|Model Answer|Content / Short Answer)\*\*:\s*(.*?)(?=\n\*\*|\Z)', body, re.S)
        curr_exp = exp_m.group(1).strip() if exp_m else ''
        curr_exp = remove_arabic(curr_exp).strip()
        
        cor_m = re.search(r'\*\*Correct Answer\*\*:\s*([A-Fa-f]|-|Unspecified)?', body)
        curr_cor = cor_m.group(1).upper() if cor_m and cor_m.group(1) else 'Unspecified'
        
        # 3. Clean Moodle chrome & status bar artifacts from body
        body_clean = re.sub(r'Lorem Ipsum.*?passages\.?', '', body, flags=re.S|re.I)
        body_clean = re.sub(r'Lorem Ipsum is simply dummy text.*?industry\.', '', body_clean, flags=re.S|re.I)
        body_clean = re.sub(r'Home\s*[»]\s*My courses\s*[»].*?Quiz\s*\d+', '', body_clean, flags=re.S|re.I)
        body_clean = re.sub(r'Quick Links\s+About Us.*?Contact[^\n]*', '', body_clean, flags=re.S|re.I)
        body_clean = re.sub(r'\b(?:Friday|Saturday|Sunday|Monday|Tuesday|Wednesday|Thursday),\s+\d+\s+[A-Za-z]+\s+\d{4},\s+\d{1,2}:\d{2}\s*(?:AM|PM)', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\b\d+\s+mins?\s+\d+\s+secs?\b', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\bMarks?\s*=\s*\d+[\.\d]*/\d+[\.\d]*', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\bGrade\s+\d+[\.\d]*\s+out\s+of\s+\d+[\.\d]*[^\n]*', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\bState\s+Finished\b', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\b(?:Mark|Flag question)\b[^\n]*', '', body_clean, flags=re.I)
        body_clean = re.sub(r'\b\d{1,2}:\d{2}\s*(?:AM|PM)?\s*(?:[®©@\-\*\–\—\•\·\>\<\»\«\:]|g\s+tl|tl|\«at\!|\bCD\:|\b4G\b|\bLTE\b|\bwifi\b)*', '', body_clean, flags=re.I)
        body_clean = re.sub(r'^\s*(?:K|BREAK|REAK)\s*---\s*', '', body_clean, flags=re.M)
        body_clean = re.sub(r'(?i)\b(?:scanned\s+with|scanned\s+by|cs)?\s*(?:camscanner|anyscanner)\b[^\n]*', '', body_clean)
        
        # 4. Extract existing options
        existing_opts = {}
        for l in body_clean.splitlines():
            m_opt = re.match(r'^- \*\*([A-Fa-f])\)\*\s*(.*)', l.strip())
            if m_opt:
                let = m_opt.group(1).upper()
                otext = clean_option_text(m_opt.group(2).strip())
                if otext:
                    existing_opts[let] = otext
                    
        # 5. Extract and clean question stem
        lines = [l.strip() for l in body_clean.splitlines() if l.strip()]
        if lines and re.match(r'^\d+$', lines[0]):
            lines = lines[1:]
            
        stem_lines = []
        for l in lines:
            if l.startswith('- **') or l.startswith('**Correct') or l.startswith('**Explanation') or l.startswith('**Model') or l.startswith('---'):
                break
            stem_lines.append(l)
            
        raw_stem = ' '.join(stem_lines).strip()
        # Strip leading numbering (e.g. "1.", "25-", "Q10:")
        raw_stem = re.sub(r'^\d+[\.\-\)]\s*', '', raw_stem).strip()
        raw_stem = re.sub(r'^(?:Question|Q\d+)[\s\:\-\.]*', '', raw_stem, flags=re.I).strip()
        
        # Strip decoupled preceding explanations
        if prev_exp and len(prev_exp) > 3:
            while raw_stem.lower().startswith(prev_exp.lower()):
                raw_stem = raw_stem[len(prev_exp):].strip()
            if raw_stem.lower().startswith(prev_exp.lower()[:15]) and len(prev_exp) >= 15:
                raw_stem = raw_stem[len(prev_exp):].strip()
                
        # Clean Moodle filler words
        raw_stem = re.sub(r'^(?:NA|sssssseeeee)\s*', '', raw_stem, flags=re.I).strip()
        raw_stem = re.sub(r'\bC@ll\b', 'Cell', raw_stem)
        
        # Clean table and answer key dumps from stem
        raw_stem = re.sub(r'(?i)\s*TABLE\s+\d+\s+A\s+B.*', '', raw_stem).strip()
        raw_stem = re.sub(
            r'(?i)\s*(?:Answers?\s+of\s+|Answer\s+of\s+|Skeletal\s+system|MUSCULAR\s+SYSTEM|CARDIOVASCULAR\s+SYSTEM|'
            r'Respiratory\s+system|Digestive\s+system|Urinary\s+system|Reproductive\s+system|Lymphatic\s+system|'
            r'Nervous\s+system|Introduction\s*&\s*skin|MICROSCOPIC\s+ANSWER|Cytology|Nucleus|Cell\s+cycle|Stem\s+cells|'
            r'BLOOD|CONNECTIVE\s+TISSUE|BONE)\s+(?:[0-9]\s+[0-9]|[A-E]\s+[A-E]).*',
            '', raw_stem
        ).strip()
        
        # 6. Parse inline options if "Select one:" present
        if 'Select one:' in raw_stem and len(existing_opts) < 2:
            m_sel = re.search(r'(.*?)\s*Select one:\s*(.*)', raw_stem, re.S|re.I)
            if m_sel:
                raw_stem = m_sel.group(1).strip()
                rest = m_sel.group(2).strip()
                inline_opts = parse_inline_options(rest)
                if len(inline_opts) >= 2:
                    existing_opts = inline_opts
                    
        # Final stem normalization
        clean_stem_str = re.sub(r'\bSelect\s+one:?.*', '', raw_stem, flags=re.I).strip()
        clean_stem_str = re.sub(r'[@©®]{2,}|\b[A-E]\s*[\)\]\.]\s*[@©®]', '', clean_stem_str).strip()
        clean_stem_str = remove_arabic(clean_stem_str).strip()
        clean_stem_str = re.sub(r'^[^a-zA-Z0-9\(\[\?]+', '', clean_stem_str).strip()
        clean_stem_str = re.sub(r'\s+', ' ', clean_stem_str).strip()
        
        # Drop trivial unrecoverable fragments
        if len(clean_stem_str) < 5 or clean_stem_str.lower() in ['complete:', 't:', 'f:']:
            continue
            
        # 7. Format options sequentially and adjust correct answer
        opts = {}
        if len(existing_opts) >= 2:
            old_keys = sorted(existing_opts.keys())
            for idx, ok in enumerate(old_keys):
                nk = chr(ord('A') + idx)
                opts[nk] = existing_opts[ok]
                if curr_cor == ok:
                    curr_cor = nk
                    
            if curr_cor not in opts:
                matched = None
                if curr_exp:
                    for let, otext in opts.items():
                        if curr_exp.lower() == otext.lower() or curr_exp.lower() in otext.lower() or otext.lower() in curr_exp.lower():
                            matched = let
                            break
                curr_cor = matched if matched else 'A'
        else:
            opts = {}
            curr_cor = '-'
            
        cleaned_questions.append({
            'stem': clean_stem_str,
            'opts': opts,
            'cor': curr_cor,
            'exp': curr_exp
        })
        prev_exp = curr_exp
        
    out = []
    # Update question count in header
    updated_header = re.sub(r'- \*\*Total Questions\*\*:\s*\d+', f'- **Total Questions**: {len(cleaned_questions)}', header)
    out.append(updated_header.strip())
    out.append('')
    out.append('---')
    out.append('')
    
    for idx, q in enumerate(cleaned_questions, 1):
        out.append(f'### Question {idx}')
        out.append('')
        out.append(q['stem'])
        out.append('')
        if q['opts']:
            for let in sorted(q['opts'].keys()):
                out.append(f'- **{let})** {q["opts"][let]}')
            out.append('')
        out.append(f'**Correct Answer**: {q["cor"]}')
        if q['exp']:
            out.append(f'**Explanation**: {q["exp"]}')
        out.append('')
        out.append('---')
        out.append('')
        
    return '\n'.join(out).strip() + '\n'

def process_file(filepath: str, in_place: bool = True, output_path: str = None):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    cleaned = clean_markdown_content(content)
    target = filepath if in_place else (output_path or filepath + '.cleaned')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned: {filepath} -> {target}")

def main():
    parser = argparse.ArgumentParser(description="MBset Deep Noise Removal Utility for Markdown Questions")
    parser.add_argument("--file", help="Path to a single markdown file")
    parser.add_argument("--dir", help="Path to directory containing markdown files")
    parser.add_argument("--pattern", default="*.md", help="Glob pattern when using --dir (default: *.md)")
    parser.add_argument("--in-place", action="store_true", default=True, help="Overwrite files in place")
    
    args = parser.parse_args()
    
    if args.file:
        process_file(args.file, in_place=args.in_place)
    elif args.dir:
        files = sorted(glob.glob(os.path.join(args.dir, args.pattern)))
        # Filter out 00_ catalog files
        files = [f for f in files if not os.path.basename(f).startswith('00_')]
        print(f"Found {len(files)} files to process in {args.dir}")
        for fp in files:
            process_file(fp, in_place=args.in_place)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
