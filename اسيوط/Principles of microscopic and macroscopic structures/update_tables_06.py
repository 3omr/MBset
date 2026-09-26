import re

with open('Markdown_Questions/06_Anatomy_Qs_Bank_3.md', encoding='utf-8') as f:
    text = f.read()

# Fix Table 1 in Intro (Q27 to Q31)
intro_opts = {
    'A': 'Erect',
    'B': 'At the side',
    'C': 'Flat on the floor',
    'D': 'At a Level',
    'E': 'Facing forward'
}
intro_items = [
    (27, 'Arm', 'B'),
    (28, 'Eyes', 'E'),
    (29, 'Head', 'D'),
    (30, 'Feet', 'C'),
    (31, 'Body', 'A')
]

for qnum, item, ans in intro_items:
    old_pattern = rf'### Question {qnum}\n\n\*\*Topic\*\*: Introduction & skin\n\n{item}\n\n- \*\*[A-E]\)\*\* [^\n]+\n\n\*\*Correct Answer\*\*: [A-E]'
    new_block = f'### Question {qnum}\n\n**Topic**: Introduction & skin\n\nIn anatomical position, the position of {item.lower()} is:\n\n'
    for l in sorted(intro_opts.keys()):
        new_block += f'- **{l})** {intro_opts[l]}\n'
    new_block += f'\n**Correct Answer**: {ans}'
    text = re.sub(old_pattern, new_block, text)

# Fix Table 1 in Skeletal (Q135 to Q138)
skel_opts = {
    'A': 'Movement that makes the angle between two bones smaller',
    'B': 'Moving part toward the midline',
    'C': 'Moving a part away from the midline',
    'D': 'Moving your head from side to side',
    'E': 'Turning the palm toward the posterior'
}
skel_items = [
    (135, 'Flexion', 'A'),
    (136, 'Adduction', 'B'),
    (137, 'Abduction', 'C'),
    (138, 'Rotation', 'D')
]

for qnum, item, ans in skel_items:
    old_pattern = rf'### Question {qnum}\n\n\*\*Topic\*\*: Skeletal system\n\n{item}\n\n(?:- \*\*[A-E]\)\*\* [^\n]+\n*)+\n\*\*Correct Answer\*\*: [A-E]'
    new_block = f'### Question {qnum}\n\n**Topic**: Skeletal system\n\n{item} is defined as:\n\n'
    for l in sorted(skel_opts.keys()):
        new_block += f'- **{l})** {skel_opts[l]}\n'
    new_block += f'\n**Correct Answer**: {ans}'
    text = re.sub(old_pattern, new_block, text)

with open('Markdown_Questions/06_Anatomy_Qs_Bank_3.md', 'w', encoding='utf-8') as f:
    f.write(text)

# Also update 44_anatomy_Qs_bankk.md for Q27-Q31
with open('Markdown_Questions/44_anatomy_Qs_bankk.md', encoding='utf-8') as f:
    t44 = f.read()

for qnum, item, ans in intro_items:
    old_pattern = rf'### Question {qnum}\n\n{item}\n\n- \*\*[A-E]\)\*\* [^\n]+\n\n\*\*Correct Answer\*\*: [A-E]'
    new_block = f'### Question {qnum}\n\nIn anatomical position, the position of {item.lower()} is:\n\n'
    for l in sorted(intro_opts.keys()):
        new_block += f'- **{l})** {intro_opts[l]}\n'
    new_block += f'\n**Correct Answer**: {ans}'
    t44 = re.sub(old_pattern, new_block, t44)

with open('Markdown_Questions/44_anatomy_Qs_bankk.md', 'w', encoding='utf-8') as f:
    f.write(t44)

print('Updated matching questions in 06 and 44 successfully!')
