import re

c7 = open('Markdown_Questions/07_Anatomy_Qs_Bank_4.md', encoding='utf-8').read()
blocks7 = re.split(r'### Question \d+\n\n', c7)[1:]

# Take first 39 questions
qs_39 = blocks7[:39]

md_lines = [
    '# anatomy department(1).pdf\n',
    '- **Source File**: `anatomy department(1).pdf`',
    '- **File Type**: Scanned PDF',
    '- **Total Pages / Slides**: 15',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(qs_39)}\n',
    '---\n'
]

for idx, b in enumerate(qs_39, 1):
    md_lines.append(f'### Question {idx}\n\n' + b.strip() + '\n\n---\n')

open('Markdown_Questions/47_anatomy_department_1.md', 'w', encoding='utf-8').write('\n'.join(md_lines))
print('Successfully wrote clean 47_anatomy_department_1.md!')
