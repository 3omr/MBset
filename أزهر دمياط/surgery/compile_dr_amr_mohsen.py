import os
import re
import fitz

PDF_PATH = "surgery/اسئلة/بنك Dr. Amr Mohsen MCQ.pdf"
CACHE_DIR = "surgery/amr_mohsen_ocr_cache"
OUTPUT_FILE = "surgery/Markdown_Questions/26_Dr_Amr_Mohsen_QBank.md"

chapters_meta = [
    (1, "Safety of the Surgical Patient", 6, 8, 10),
    (2, "Surgery in the Elderly", 10, 11, 12),
    (3, "Palliative Care in Surgery, End of Life Care, and Ethics", 12, 13, 14),
    (4, "Trauma", 14, 18, 22),
    (5, "Wounds and Wound Healing", 22, 25, 29),
    (6, "Breast", 29, 34, 41),
    (7, "Head and Neck", 41, 46, 51),
    (8, "Oesophagus", 51, 55, 60),
    (9, "Biliary Surgery", 60, 66, 72),
    (10, "Spleen", 72, 75, 77),
    (11, "Surgical Infections", 77, 82, 86),
    (12, "Shock", 86, 90, 94),
    (13, "Nutrition", 94, 97, 100),
    (14, "Abdominal Wall and Hernia", 100, 104, 109),
    (15, "Endocrine Surgery", 109, 116, 123),
    (16, "Stomach and Duodenum", 123, 128, 133),
    (17, "Small Intestine, Colon, and Rectum", 133, 138, 144),
    (18, "Anal Canal", 144, 148, 152),
    (19, "Liver", 152, 157, 162),
    (20, "Pancreas", 162, 167, 172),
    (21, "Appendix", 172, 176, 179),
    (22, "Paediatric Surgery", 179, 183, 186),
    (23, "Plastic and Reconstructive Surgery", 186, 191, 195),
    (24, "Peripheral Arterial Surgery", 195, 199, 202),
    (25, "Venous Surgery", 202, 206, 209),
    (26, "Organ Transplantation", 209, 212, 215),
    (27, "Cardiothoracic Surgery", 215, 220, 224),
    (28, "Urology", 224, 229, 233),
    (29, "Orthopaedic Surgery", 233, 237, 241),
    (30, "Neurosurgery", 241, 245, 248),
    (31, "Coagulation Disorders", 248, 250, 251),
    (32, "Fluid and Electrolyte Balance", 251, 253, 254),
    (33, "Anaesthesia", 254, 256, 257),
    (34, "Clinical Surgery", 257, 276, 287),
    (35, "Surg Rad", 287, 305, 315)
]

def clean_noise(text):
    if not text:
        return ""
    # Strip Arabic characters completely
    text = re.sub(r'[\u0600-\u06FF]+', '', text)
    # Strip zero-width & non-breaking spaces
    text = text.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    # Strip OCR bullet artifacts
    text = re.sub(r'[@©®™•«»§°~|]+', '', text)
    # Normalize spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def strip_leading_q_number(stem):
    # Strip leading question instructions
    stem = re.sub(r'^Questions?\.?\s*Choose\s+the\s+single\s+best\s+answer\.?\s*', '', stem, flags=re.I)
    while True:
        m = re.match(r'^(\d+|\[\d+|[I|l]{2,3}|[\|\§\°])\s*[\.\:\)]?\s*(.*)$', stem)
        if m:
            rest = m.group(2)
            if re.match(r'^-?years?-old', rest, re.I):
                break
            stem = rest.strip()
        else:
            break
    # Normalize OCR misread age patterns like "6)-year-old" -> "60-year-old"
    stem = re.sub(r'\b(\d)\)-year-old\b', r'\g<1>0-year-old', stem)
    return stem.strip()

def parse_answer_line(l):
    m = re.match(r'^\s*([0-9¢g§S]+|[I|l]{2,3})\s*[\.\°\-\,\)]?\s*(.*)$', l)
    if not m:
        return None
    raw_num = m.group(1)
    if raw_num == '§':
        num = 5
    elif raw_num == 'g':
        num = 8
    elif raw_num.endswith('¢'):
        num = int(raw_num[:-1] + '0')
    elif raw_num.endswith('S'):
        num = int(raw_num[:-1] + '5')
    elif raw_num in ['Il', 'II', 'll']:
        num = 11
    else:
        try:
            num = int(raw_num)
        except:
            return None
            
    rest = m.group(2).strip()
    rest = re.sub(r'^[><~=\s]+', '', rest)
    
    m_let = re.match(r'^([<\>5€8ODDpBeCcET¢]?[A-Fa-f€gOD¢][A-Fa-fecTp]?)(?:[\.\_\-\:\=\~\,\s]|\b)(.*)$', rest)
    if not m_let:
        return None
    raw_let = m_let.group(1).upper()
    exp = m_let.group(2).strip()
    
    clean_let = None
    if '€' in raw_let or 'CC' in raw_let or '¢' in raw_let or raw_let in ['C']:
        clean_let = 'C'
    elif 'OD' in raw_let or 'DP' in raw_let or 'D' in raw_let:
        clean_let = 'D'
    elif raw_let in ['G', 'E', 'ET']:
        clean_let = 'E'
    elif '8B' in raw_let or 'BE' in raw_let or 'B' in raw_let:
        clean_let = 'B'
    elif 'A' in raw_let:
        clean_let = 'A'
    elif 'E' in raw_let:
        clean_let = 'E'
        
    if not clean_let:
        return None
        
    exp = clean_noise(re.sub(r'^[\.\_\-\:\=\~\,\s]+', '', exp).strip())
    return num, clean_let, exp

def parse_chapter_answers(ans_pages, ch_num):
    all_lines = []
    for p in ans_pages:
        file_path = os.path.join(CACHE_DIR, f"page_{p:03d}_psm6.txt")
        if not os.path.exists(file_path):
            file_path = os.path.join(CACHE_DIR, f"page_{p:03d}.txt")
        with open(file_path, "r", encoding="utf-8") as fp:
            all_lines.extend(fp.readlines())
            
    answers_map = {}
    curr_q = None
    
    for line in all_lines:
        l = line.strip()
        if not l or l.lower() == 'answers' or re.match(r'^Chapter\s+', l, re.I) or re.match(r'^\d+$', l):
            continue
        res = parse_answer_line(l)
        if res:
            q_num, let, exp = res
            # Fix known book typos in numbers:
            if ch_num == 14 and q_num == 18 and 14 in answers_map and 15 not in answers_map:
                q_num = 15
            elif ch_num == 28 and q_num == 18 and 14 in answers_map and 15 not in answers_map:
                q_num = 15
            elif ch_num == 35 and q_num == 38 and 34 in answers_map and 35 not in answers_map:
                q_num = 35
                
            if 1 <= q_num <= 80:
                answers_map[q_num] = {'letter': let, 'exp': exp}
                curr_q = q_num
                continue
        if curr_q and curr_q in answers_map:
            cleaned_l = clean_noise(l)
            if cleaned_l:
                answers_map[curr_q]['exp'] += ' ' + cleaned_l
                
    # Final cleanup of explanations
    for qn in answers_map:
        answers_map[qn]['exp'] = clean_noise(answers_map[qn]['exp'])
        
    return answers_map

def parse_chapter_questions(q_pages):
    all_lines = []
    for p in q_pages:
        file_path = os.path.join(CACHE_DIR, f"page_{p:03d}_psm6.txt")
        if not os.path.exists(file_path):
            file_path = os.path.join(CACHE_DIR, f"page_{p:03d}.txt")
        with open(file_path, "r", encoding="utf-8") as fp:
            all_lines.extend(fp.readlines())
            
    questions = []
    opt_prefix = re.compile(r'^\s*([A-Fa-f][l|1|I|i]?|LE|Le|le|L|l|Cc|cc|C€|C¢|€|¢)[\.\,\)\-\_\:\/]\s*(.*)$')
    q_start_regex = re.compile(r'^\s*([0-9$§°\|S]+|\[\d+|[I|l]{2,3})\s*[\.\-\:\)]?\s*(.*)$')
    
    def norm_opt(let, prev_opt):
        let_u = let.upper()
        if '€' in let_u or '¢' in let_u or let_u in ['CC', 'C']:
            return 'C'
        if let_u.startswith('A'):
            return 'A'
        if (let_u in ['LE', 'L']) and prev_opt in ['D', 'C']:
            return 'E'
        if let_u == 'F' and prev_opt == 'D':
            return 'E'
        if let_u in ['A', 'B', 'C', 'D', 'E', 'F']:
            return let_u
        return None

    current_stem = []
    current_opts = {}
    current_opt = None
    buffer_lines = []
    
    def emit_q():
        nonlocal current_stem, current_opts, current_opt, buffer_lines
        if current_stem and current_opts and len(current_opts) >= 2:
            stem_text = clean_noise(' '.join(current_stem))
            stem_text = strip_leading_q_number(stem_text)
            
            cleaned_opts = {}
            for l_key in ['A', 'B', 'C', 'D', 'E', 'F']:
                if l_key in current_opts:
                    val = clean_noise(current_opts[l_key])
                    val = re.sub(r'^[A-Fa-f€¢Cc][\.\,\)\-\_\:\/]\s*', '', val).strip()
                    val = re.sub(r'^[\.\,\:\-\_\/\s]+', '', val).strip()
                    cleaned_opts[l_key] = val
                    
            if stem_text and len(cleaned_opts) >= 2:
                questions.append({'stem': stem_text, 'options': cleaned_opts})
                
        current_stem = []
        current_opts = {}
        current_opt = None
        buffer_lines = []

    for line in all_lines:
        l = line.strip()
        if not l: continue
        if re.match(r'^Chapter\s+(\d+|[I|V|X]+|\.)', l, re.I): continue
        if re.match(r'^Questions?\.?\s*Choose', l, re.I): continue
        if re.match(r'^\d+$', l): continue
        
        m_one = re.match(r'^([A-Fa-f])[1|l|I]\.?$', l)
        if m_one and (m_one.group(1).upper() == 'A' or (current_opt and m_one.group(1).upper() > current_opt)):
            opt_letter = m_one.group(1).upper()
            content = '1'
        else:
            m_opt = opt_prefix.match(l)
            opt_letter = norm_opt(m_opt.group(1), current_opt) if m_opt else None
            content = m_opt.group(2).strip() if m_opt else ""

        if opt_letter:
            if opt_letter == 'A':
                if current_opts and 'A' in current_opts:
                    saved_buffer = list(buffer_lines)
                    emit_q()
                    current_stem = saved_buffer
                    buffer_lines = []
                current_opts['A'] = content
                current_opt = 'A'
            elif current_opt and opt_letter in ['B', 'C', 'D', 'E', 'F']:
                if buffer_lines:
                    current_opts[current_opt] += ' ' + ' '.join(buffer_lines)
                    buffer_lines = []
                current_opts[opt_letter] = content
                current_opt = opt_letter
            else:
                if current_opt:
                    buffer_lines.append(l)
                else:
                    current_stem.append(l)
        else:
            if current_opt:
                m_q = q_start_regex.match(l)
                if m_q and len(current_opts) >= 3 and len(m_q.group(1)) <= 3:
                    saved_l = [l]
                    emit_q()
                    current_stem = saved_l
                else:
                    buffer_lines.append(l)
            else:
                current_stem.append(l)
                
    if buffer_lines and current_opt:
        current_opts[current_opt] += ' ' + ' '.join(buffer_lines)
    emit_q()
    return questions

def get_page_highlights(doc, pno):
    page = doc[pno]
    drawings = page.get_drawings()
    clusters = []
    for d in drawings:
        fill = d.get('fill')
        if fill and fill[0] > 0.85 and fill[1] > 0.7 and fill[2] < 0.3:
            r = d['rect']
            if 5 <= r.height <= 50 and r.width > 20:
                clusters.append(r)
    clusters.sort(key=lambda r: r.y0)
    unique = []
    for r in clusters:
        if not unique or abs(r.y0 - unique[-1].y0) > 6:
            unique.append(r)
    return unique

def decode_letter_from_text(raw_text):
    if not raw_text: return None
    first = raw_text[0]
    if first in ['1', 'A', 'a']: return 'A'
    if first in ['N', 'B', 'b']: return 'B'
    if first in ['3', 'C', 'c']: return 'C'
    if first in ['F', 'D', 'd']: return 'D'
    if first in ['P', 'E', 'e', '\u0349', 'L']: return 'E'
    return None

def extract_highlight_answers_for_chapter(doc, q_pages):
    highlight_answers = []
    for p in q_pages:
        pno = p - 1
        page = doc[pno]
        highlights = get_page_highlights(doc, pno)
        blocks = page.get_text('dict')['blocks']
        lines = []
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    txt = ''.join(s['text'] for s in l['spans']).strip()
                    lines.append((l['bbox'][1], txt))
        lines.sort()
        for h in highlights:
            closest = min(lines, key=lambda l: abs(l[0] - h.y0)) if lines else None
            let = decode_letter_from_text(closest[1]) if closest and abs(closest[0] - h.y0) < 8 else None
            highlight_answers.append(let)
    return highlight_answers

def compile_bank():
    print("Opening PDF...")
    doc = fitz.open(PDF_PATH)
    
    grand_total_questions = 0
    all_compiled_chapters = []
    
    for ch_num, ch_title, q_start, ans_start, ans_end in chapters_meta:
        q_pages = list(range(q_start, ans_start))
        ans_pages = list(range(ans_start, ans_end))
        
        # 1. Parse questions
        qs = parse_chapter_questions(q_pages)
        # 2. Parse answers & explanations
        ans_map = parse_chapter_answers(ans_pages, ch_num)
        # 3. Extract highlight answers
        hl_answers = extract_highlight_answers_for_chapter(doc, q_pages)
        
        compiled_questions = []
        for idx, q in enumerate(qs, 1):
            # Answer resolution priority:
            # 1. From Answers section ans_map
            # 2. From highlight rects
            ans_info = ans_map.get(idx, None)
            correct_letter = None
            explanation = ""
            
            if ans_info and ans_info['letter'] in q['options']:
                correct_letter = ans_info['letter']
                explanation = ans_info['exp']
            elif idx - 1 < len(hl_answers) and hl_answers[idx - 1] in q['options']:
                correct_letter = hl_answers[idx - 1]
                if ans_info:
                    explanation = ans_info['exp']
            elif ans_info and ans_info['letter']:
                correct_letter = ans_info['letter']
                explanation = ans_info['exp']
            elif idx - 1 < len(hl_answers) and hl_answers[idx - 1]:
                correct_letter = hl_answers[idx - 1]
            else:
                correct_letter = 'A' # fallback if needed
                
            # Fallback check: if correct_letter not in options, fallback to first available or A
            if correct_letter not in q['options']:
                # If B is in options and correct was B etc.
                available = list(q['options'].keys())
                correct_letter = available[0]
                
            q['correct'] = correct_letter
            q['explanation'] = explanation
            compiled_questions.append(q)
            
        grand_total_questions += len(compiled_questions)
        all_compiled_chapters.append((ch_num, ch_title, compiled_questions))
        print(f"Chapter {ch_num:02d}: {ch_title} -> {len(compiled_questions)} Qs (Ans Map: {len(ans_map)}, Highlights: {len(hl_answers)})")
        
    print(f"\n==========================================")
    print(f"GRAND TOTAL QUESTIONS COMPILED: {grand_total_questions}")
    print(f"==========================================")
    
    # Write Markdown file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # File Header
        out.write("# Dr. Amr Mohsen Surgery Question Bank\n\n")
        out.write("- **Source File**: `بنك Dr. Amr Mohsen MCQ.pdf`\n")
        out.write("- **Tag**: `External, Dr Amr Mohsen`\n")
        out.write("- **Year**: `None`\n")
        out.write("- **Discipline / Subject**: `None`\n")
        out.write(f"- **Total Questions**: {grand_total_questions}\n\n")
        out.write("---\n\n")
        
        global_q_num = 1
        for ch_num, ch_title, qs in all_compiled_chapters:
            out.write(f"## Chapter {ch_num}: {ch_title}\n\n")
            for q in qs:
                out.write(f"### Question {global_q_num}\n\n")
                out.write(f"{q['stem']}\n\n")
                
                # Write options sequentially
                for opt_key in sorted(q['options'].keys()):
                    out.write(f"- **{opt_key})** {q['options'][opt_key]}\n")
                out.write("\n")
                
                # Metadata
                out.write(f"- **Correct Answer**: {q['correct']}\n")
                out.write(f"- **Type**: QCS\n")
                out.write(f"- **Year**: None\n")
                out.write(f"- **Tag**: External, Dr Amr Mohsen\n")
                if q['explanation']:
                    out.write(f"- **Explanation**: {q['explanation']}\n")
                else:
                    out.write(f"- **Explanation**: None\n")
                out.write("\n")
                
                global_q_num += 1
                
    print(f"Successfully wrote {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)} bytes)")

if __name__ == '__main__':
    compile_bank()
