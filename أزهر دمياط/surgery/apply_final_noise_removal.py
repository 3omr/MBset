import re

md_path = 'surgery/Markdown_Questions/24_Azhar_Cairo_QBank.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Map question number to exact clean stem
direct_fixes = {
    26: "Which of the following is true regarding post-operative fever?",
    82: "A patient presents to the emergency department because she has trouble breathing. On oral examination, the floor of the mouth is indurated, swollen, and very tender. The patient has poor dentition, but there is no evidence of an abscess. Her submandibular and submental regions are also tender and indurated. What diagnosis are you most concerned about?",
    85: "A 22-year-old man sustains a gunshot wound to the abdomen. At exploration, an apparently solitary distal small-bowel injury is treated with resection and primary anastomosis. On 7th post-operative day, small-bowel fluid drains through the operative incision. The fascia remains intact. The fistula output is 300 mL/day and there is no evidence of intra-abdominal sepsis. Correct treatment includes:",
    87: "A 36-year-old man sustains a gunshot wound to the left buttock. He is hemodynamically stable. There is no exit wound, and an x-ray of the abdomen shows the bullet to be located in the right lower quadrant. Correct management of a suspected rectal injury would include:",
    93: "Patients with a penicillin allergy are LEAST likely to have a cross-reaction with:",
    115: "Signs of malignant transformation in a chronic wound include:",
    150: "A decrease in intra-cellular water is facilitated by:",
    164: "Which of the following would lead you to an arteriogram and/or exploration of the popliteal artery?",
    364: "Which of the following clotting factors is consumed during coagulation?"
}

header_part = content[:content.find('### Question 1')]
blocks = re.split(r'\n(?=### Question \d+)', content[content.find('### Question 1'):])

fixed_blocks = []
for b in blocks:
    b_s = b.strip()
    if not b_s.startswith('### Question'): continue
    q_num = int(re.search(r'### Question (\d+)', b_s).group(1))
    
    if q_num in direct_fixes:
        # Find where options start
        opt_start = re.search(r'\n-\s+\*\*[A-F]\)\*\*', b_s)
        if opt_start:
            q_header = re.match(r'^### Question \d+', b_s).group(0)
            rest = b_s[opt_start.start():]
            new_block = f"{q_header}\n\n{direct_fixes[q_num]}\n{rest}"
            fixed_blocks.append(new_block)
            continue
            
    fixed_blocks.append(b_s)

final_text = header_part + '\n\n---\n\n'.join(fixed_blocks) + '\n'
final_text = re.sub(r'---\s*\n\s*---', '---', final_text)

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(final_text)

print(f'Successfully applied direct stem fixes to {len(direct_fixes)} questions in {md_path}!')
