import re

c35 = open('Markdown_Questions/35_Qena_final_20_21.md', encoding='utf-8').read()
blocks35 = re.split(r'### Question \d+\n\n', c35)[1:]

c41 = open('Markdown_Questions/41_anatomy_Qs_bank_1.md', encoding='utf-8').read()
blocks41 = re.split(r'### Question \d+\n\n', c41)[1:]

all_blocks = blocks35 + blocks41

md_lines = [
    '# امتحانات واسئله القسم.pptx\n',
    '- **Source File**: `امتحانات واسئله القسم.pptx`',
    '- **File Type**: PPTX (Presentation Slides)',
    '- **Total Pages / Slides**: 26',
    '- **Assiut Tag**: Exams, Past Exams Compilation',
    '- **Discipline**: Anatomy & Embryology',
    f'- **Total Questions**: {len(all_blocks)}\n',
    '---\n'
]

for idx, b in enumerate(all_blocks, 1):
    # Strip any residual arabic
    b_clean = re.sub(r'[\u0600-\u06FF]+', '', b).strip()
    md_lines.append(f'### Question {idx}\n\n' + b_clean + '\n\n---\n')

open('Markdown_Questions/72_امتحانات_واسئله_القسم.md', 'w', encoding='utf-8').write('\n'.join(md_lines))
print(f'Successfully wrote clean 72_امتحانات_واسئله_القسم.md with {len(all_blocks)} questions!')
