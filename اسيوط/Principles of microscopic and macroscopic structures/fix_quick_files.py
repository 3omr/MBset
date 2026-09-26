import re

# 1. Clean noise '* * *' from 16, 35, 36
for fname in ['16_First_week_quizes.md', '35_Qena_final_20_21.md', '36_Summer_sohag_2021.md']:
    path = f'Markdown_Questions/{fname}'
    c = open(path, encoding='utf-8').read()
    c = re.sub(r'\*\s+\*\s+\*', '', c)
    c = re.sub(r'-\s+\*\*([A-F])\)\*\*\s+\*\s+\*\s*', r'- **\1)** ', c)
    c = re.sub(r'-\s+\*\*([A-F])\)\*\*\s+\*', r'- **\1)** ', c)
    open(path, 'w', encoding='utf-8').write(c)
    print(f'Cleaned noise from {fname}')

# 2. Strip Arabic characters from 04, 71, 73, 74, 75
for fname in ['04_2023_Final_Assuit_دور_تاني.md', '71_امتحانات_سنين_سابقه.md', '73_زقازيق_Mcq.md', '74_فاينل_2018_دور_تاني.md', '75_مذكرة_حل_احمد_صلاح_pms.md']:
    path = f'Markdown_Questions/{fname}'
    c = open(path, encoding='utf-8').read()
    # Strip arabic chars
    c = re.sub(r'[\u0600-\u06FF]+', '', c)
    open(path, 'w', encoding='utf-8').write(c)
    print(f'Stripped Arabic from {fname}')

# 3. Fix option mismatches in 70, 73, 75
# In 70:
path = 'Markdown_Questions/70_week_2_Quizzes.md'
c = open(path, encoding='utf-8').read()
# Let's inspect any mismatch in 70
blocks = re.split(r'### Question \d+', c)
# Let's ensure if ans not in opts, fallback or add option
