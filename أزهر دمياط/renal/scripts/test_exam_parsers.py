import re, os

exam_files = [
    ('End 2019.md', 2019, 'Exams, End 2019'),
    ('End 2020.md', 2020, 'Exams, End 2020'),
    ('End 2021.md', 2021, 'Exams, End 2021'),
    ('End 2022.md', 2022, 'Exams, End 2022'),
    ('End 2023.md', 2023, 'Exams, End 2023'),
    ('End 2024.md', 2024, 'Exams, End 2024'),
    ('End 2025.md', 2025, 'Exams, End 2025'),
    ('End 2026.md', 2026, 'Exams, End 2026'),
    ('final 2020(MCQ).md', 2020, 'Exams, Final 2020'),
    ('Final  2025.md', 2025, 'Exams, Final 2025'),
    ('Final 2026.md', 2026, 'Exams, Final 2026'),
    ('Formative 2021.md', 2021, 'Exams, Formative 2021'),
    ('Formative 2025.md', 2025, 'Exams, Formative 2025'),
]

def clean_noise(text):
    # Remove Arabic
    text = re.sub(r'[\u0600-\u06FF]+', '', text)
    # Remove invisible unicode
    text = text.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    # Remove web/mobile artifacts
    text = re.sub(r'(?i)forms\.office\.com[^\n]*', '', text)
    text = re.sub(r'(?i)team\s*Doc-?ReaderGuide[^\n]*', '', text)
    text = re.sub(r'(?i)Doc-?Reader\s*Guide[^\n]*', '', text)
    text = re.sub(r'(?i)Solve it online at[^\n]*', '', text)
    text = re.sub(r'(?i)Keep calm and Go On[^\n]*', '', text)
    text = re.sub(r'(?i)Good Luck[^\n]*', '', text)
    text = re.sub(r'(?i)Direected by[^\n]*', '', text)
    text = re.sub(r'(?i)Free phalasstine[^\n]*', '', text)
    text = re.sub(r'𝙰𝚈𝙾𝚄𝙱', '', text)
    text = re.sub(r'\b\d{1,2}:\d{2}(?:\s*(?:AM|PM))?\b', '', text)
    text = re.sub(r'\b\d+\.?\d*\s*KB/S\b', '', text)
    text = re.sub(r'(?i)When you submit this form, the owner will see your name and email address\.?', '', text)
    return text

for fname, year, tag in exam_files:
    p = os.path.join('renal/markdown_output', fname)
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = clean_noise(f.read())
    
    # Let's count question stems
    stems = re.findall(r'(?m)^\s*(?:\*{0,2}\d+\s*[\.\)]|\#+\s*\d+[\.\)])\s*(.+)', content)
    print(f'{fname:25s} -> {len(stems)} stems detected')
