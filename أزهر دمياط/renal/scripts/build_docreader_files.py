import urllib.request, json, re, os

docreader_configs = [
    {
        'qid': 2813,
        'filename': '24_Physiology_Department_Book_Questions_2026_MCQ.md',
        'source_file': 'Physiology Department book  Questions 2026(MCQ) .md',
        'tag': 'Department, Physiology 2026',
        'tagSuggere': 'Physiology',
        'year': 2026,
        'type': 'QCS'
    },
    {
        'qid': 2839,
        'filename': '25_Physiology_Department_Book_Questions_MCQ_2025.md',
        'source_file': 'PhysiologyDepartmentbookQuestions(MCQ) 2025.md',
        'tag': 'Department, Physiology 2025',
        'tagSuggere': 'Physiology',
        'year': 2025,
        'type': 'QCS'
    },
    {
        'qid': 2389,
        'filename': '20_Histology_Department_Book_questions_MCQ_2026.md',
        'source_file': 'HistologyDepartmentbookquestions(MCQ) 2026.md',
        'tag': 'Department, Histology 2026',
        'tagSuggere': 'Histology',
        'year': 2026,
        'type': 'QCS'
    },
    {
        'qid': 2840,
        'filename': '22_Parasitology_Department_Book_Questions_2026_MCQ.md',
        'source_file': 'ParasitologyDepartment book Questions 2026(MCQ).md',
        'tag': 'Department, Parasitology 2026',
        'tagSuggere': 'Parasitology',
        'year': 2026,
        'type': 'QCS'
    },
    {
        'qid': 2763,
        'filename': '19_Formative_2026.md',
        'source_file': 'Formative 2026.md',
        'tag': 'Exams, Formative 2026',
        'tagSuggere': None,
        'year': 2026,
        'type': 'QCS'
    },
    {
        'qid': 2759,
        'filename': '17_Formative_2022.md',
        'source_file': 'Formative2022.md',
        'tag': 'Exams, Formative 2022',
        'tagSuggere': None,
        'year': 2022,
        'type': 'QCS'
    },
    {
        'qid': 2697,
        'filename': '26_Physiology_Department_Book_Questions_Written_2025.md',
        'source_file': 'PhysiologyDepartmentbookQuestions(Written) 2025.md',
        'tag': 'Department, Microbiology 2025',
        'tagSuggere': 'Microbiology',
        'year': 2025,
        'type': 'QCS'
    },
]

def clean_text(s):
    if not s:
        return ""
    # Strip Arabic
    s = re.sub(r'[\u0600-\u06FF]+', '', s)
    # Strip invisible unicode
    s = s.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    # Strip leading numbering
    s = re.sub(r'^\s*(?:\d+[\.\-\)]|[A-Z][\.\)]|\- \*\*[A-F]\*\*)\s*', '', s)
    # Normalize spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def answer_letter(raw_options, correct_idx):
    """Letter of the site's correct option, or '?' when the site gives no usable answer.

    `correctOptionIndex` points into the RAW option list (before empty options are dropped). A
    missing, non-integer or out-of-range index, or one pointing at an empty option, means the site
    has no answer: return '?' — never default to 0 (= A), never invent an answer.
    """
    if isinstance(correct_idx, str) and correct_idx.strip().isdigit():
        correct_idx = int(correct_idx.strip())
    if not isinstance(correct_idx, int) or isinstance(correct_idx, bool):
        return '?'
    if not 0 <= correct_idx < len(raw_options) or not raw_options[correct_idx]:
        return '?'
    kept = sum(1 for opt in raw_options[:correct_idx] if opt)   # position after empties are dropped
    return chr(65 + kept)

def fetch_and_build():
    os.makedirs('renal/Markdown_Questions', exist_ok=True)
    
    for cfg in docreader_configs:
        qid = cfg['qid']
        target_fn = cfg['filename']
        src_fn = cfg['source_file']
        tag = cfg['tag']
        year = cfg['year']
        tagSuggere = cfg['tagSuggere']
        
        print(f"Fetching Quiz {qid} -> {target_fn}...")
        url = f"https://doc-reader-guide.com/mcq-quizzes/{qid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8')
        chunks = re.findall(r'self\.__next_f\.push\(\[1,\"(.*?)\"\]\)', html)
        full_text = ''.join(chunks).encode('utf-8').decode('unicode_escape')
        
        q_start = full_text.find('"questions":[')
        start = q_start + len('"questions":')
        bracket_depth = 0
        end = start
        for i in range(start, len(full_text)):
            if full_text[i] == '[':
                bracket_depth += 1
            elif full_text[i] == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    end = i + 1
                    break
        qs = json.loads(full_text[start:end])
        print(f"  Loaded {len(qs)} questions.")
        
        # Build clean markdown
        md_lines = []
        md_lines.append(f"# {src_fn}")
        md_lines.append("")
        md_lines.append(f"- **Source File**: `{src_fn}`")
        md_lines.append(f"- **Tag**: `{tag}`")
        md_lines.append(f"- **Year**: {year}")
        md_lines.append(f"- **Discipline / Subject**: `{tagSuggere}`")
        md_lines.append(f"- **Total Questions**: {len(qs)}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        for idx, q in enumerate(qs, 1):
            stem = clean_text(q.get('text', ''))
            raw_options = [clean_text(opt) for opt in q.get('options', [])]
            options = [opt for opt in raw_options if opt]
            correct_letter = answer_letter(raw_options, q.get('correctOptionIndex'))
            if correct_letter == '?':
                print(f"  [!] Q{idx}: no usable correctOptionIndex ({q.get('correctOptionIndex')!r}) — answer left '?'")
            exp = clean_text(q.get('explanation', ''))
            
            md_lines.append(f"### Question {idx}")
            md_lines.append("")
            md_lines.append(stem)
            md_lines.append("")
            for opt_idx, opt_text in enumerate(options):
                opt_letter = chr(65 + opt_idx)
                md_lines.append(f"- **{opt_letter})** {opt_text}")
            md_lines.append("")
            md_lines.append(f"**Correct Answer**: {correct_letter}")
            if exp:
                md_lines.append(f"**Explanation**: {exp}")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
            
        out_path = os.path.join('renal/Markdown_Questions', target_fn)
        with open(out_path, 'w', encoding='utf-8') as f_out:
            f_out.write('\n'.join(md_lines))
        print(f"  Wrote {out_path} successfully!")

if __name__ == '__main__':
    fetch_and_build()
