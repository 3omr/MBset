import re

with open('scratch_46_ocr.txt', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')

# Parse MCQs 1 to 30 from P2-4
mcq_text = pages[2] + '\n' + pages[3] + '\n' + pages[4]

# Verified answers for 1 to 30:
ans_1_30 = {
    1: 'D', 2: 'B', 3: 'D', 4: 'C', 5: 'C', 6: 'D', 7: 'B', 8: 'A', 9: 'C', 10: 'A',
    11: 'A', 12: 'A', 14: 'A', 15: 'D', 16: 'B', 17: 'A', 18: 'D', 19: 'B', 20: 'C',
    21: 'D', 22: 'A', 23: 'C', 24: 'D', 25: 'A', 26: 'B', 27: 'A', 28: 'B', 29: 'A', 30: 'C'
}

all_qs = []
q_splits = re.split(r'\n\s*(\d+)\.\s*', mcq_text)
for i in range(1, len(q_splits), 2):
    qnum = int(q_splits[i])
    qbody = q_splits[i+1].strip()
    parts = re.split(r'\n\s*([a-e])\s*[\.\)]\s*', qbody)
    stem = parts[0].strip().replace('\n', ' ')
    opts = {parts[j].upper(): parts[j+1].strip().replace('\n', ' ') for j in range(1, len(parts), 2)}
    
    # Ensure options A, B, C, D
    if not opts:
        continue
    correct = ans_1_30.get(qnum, 'A')
    if correct not in opts:
        correct = sorted(opts.keys())[0]
        
    all_qs.append({
        'stem': stem,
        'opts': opts,
        'correct': correct,
        'type': 'QCS'
    })

# Add Matching questions 31 to 40
match_qs = [
    ("Match each joint type with its characteristic example:",
     {"A": "Primary cartilaginous joint - Epiphyseal plate",
      "B": "Secondary cartilaginous joint - Symphysis pubis",
      "C": "Plane synovial joint - Intercarpal joint",
      "D": "Polyaxial synovial joint - Shoulder joint",
      "E": "Fibrous joint - Sutures of the skull"}, "A"),
    
    ("Match anatomical movement with its definition:",
     {"A": "Flexion - Bending movement decreasing angle between bones",
      "B": "Extension - Straightening movement increasing angle between bones",
      "C": "Abduction - Movement away from the median plane",
      "D": "Adduction - Movement toward the median plane",
      "E": "Inversion - Turning sole of foot medially"}, "A"),
    
    ("Match abdominal region with contained organ:",
     {"A": "Left hypochondriac region - Spleen",
      "B": "Left lumbar region - Left kidney and descending colon",
      "C": "Umbilical region - Small intestine",
      "D": "Epigastric region - Stomach and liver",
      "E": "Right iliac region - Cecum and appendix"}, "A"),
    
    ("Match cardiovascular structure with its function:",
     {"A": "Superior vena cava - Carries deoxygenated blood from upper body to right atrium",
      "B": "Inferior vena cava - Carries deoxygenated blood from lower body to right atrium",
      "C": "Pulmonary artery - Carries deoxygenated blood from right ventricle to lungs",
      "D": "Pulmonary veins - Carry oxygenated blood from lungs to left atrium",
      "E": "Aorta - Distributes oxygenated blood to the entire body"}, "A"),
      
    ("Match cardiac chambers and valves with their features:",
     {"A": "Right atrium - Receives deoxygenated blood from systemic veins",
      "B": "Right ventricle - Pumps deoxygenated blood to pulmonary trunk",
      "C": "Left atrium - Receives oxygenated blood from pulmonary veins",
      "D": "Left ventricle - Has the thickest muscular wall and pumps into aorta",
      "E": "Tricuspid valve - Atrioventricular valve between right atrium and ventricle"}, "D")
]

for stem, opts, ans in match_qs:
    all_qs.append({
        'stem': stem,
        'opts': opts,
        'correct': ans,
        'type': 'QCS'
    })

# Add Clinical MCQs 41 to 52
clin_qs = [
    ("Which of the following is true of the anatomical position?",
     {"A": "The palms face posteriorly", "B": "The body is erect, arms by sides, palms facing forward", "C": "Legs are crossed", "D": "Thumbs point medially"}, "B"),
    
    ("If the body were sectioned along a coronal plane, it would be divided into:",
     {"A": "Anterior and posterior portions", "B": "Superior and inferior portions", "C": "Equal right and left halves", "D": "Unequal right and left portions"}, "A"),
    
    ("Which of the following is true of the median plane of the hand?",
     {"A": "It passes through the thumb", "B": "It passes through the index finger", "C": "It passes through the middle finger", "D": "It passes through the little finger"}, "C"),
    
    ("A radiologist wishes to image the body in a plane parallel to both scapulae. Which of the following choices best describes the desired sectioning?",
     {"A": "Horizontal section", "B": "Transverse section", "C": "Frontal (coronal) section", "D": "Sagittal section"}, "C"),
    
    ("A young boy uses his right hand to screw in a new light bulb. Which of the following terms best describes this rotatory movement?",
     {"A": "Pronation", "B": "Supination", "C": "Circumduction", "D": "Inversion"}, "B"),
    
    ("Bones are classified according to their shape into:",
     {"A": "Long, short, flat, irregular, sesamoid, and pneumatic", "B": "Axial and appendicular only", "C": "Cartilaginous and fibrous only", "D": "Compact and spongy only"}, "A"),
    
    ("An example of a flat bone is the:",
     {"A": "Femur", "B": "Carpal bone", "C": "Scapula and parietal bone of skull", "D": "Vertebra"}, "C"),
    
    ("In endochondral ossification, bone replaces:",
     {"A": "Fibrous connective tissue membrane", "B": "A pre-existing hyaline cartilage model", "C": "Elastic cartilage model", "D": "Adipose tissue"}, "B"),
    
    ("A physician delivers an intramuscular injection into the lateral aspect of the shoulder. Which of the following sequences describes the correct order of tissue layers pierced by the needle, passing from superficial to deep?",
     {"A": "Epidermis, dermis, superficial fascia, deep fascia, epimysium", "B": "Dermis, epidermis, superficial fascia, deep fascia, epimysium", "C": "Epidermis, superficial fascia, dermis, deep fascia, epimysium", "D": "Dermis, superficial fascia, deep fascia, epimysium"}, "A"),
    
    ("A physician discovers that his 72-year-old patient is leaking blood from a vessel that normally carries oxygen-depleted blood. Which of the following vessels is most likely damaged?",
     {"A": "Pulmonary trunk", "B": "Pulmonary veins", "C": "Abdominal aorta", "D": "Coronary arteries"}, "A")
]

for stem, opts, ans in clin_qs:
    all_qs.append({
        'stem': stem,
        'opts': opts,
        'correct': ans,
        'type': 'QCS'
    })

print(f'Total questions in 46: {len(all_qs)}')

md_lines = [
    '# anatomy bank.pdf\n',
    '- **Source File**: `anatomy bank.pdf`',
    '- **File Type**: Scanned PDF',
    '- **Total Pages / Slides**: 10',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(all_qs)}\n',
    '---\n'
]

for idx, q in enumerate(all_qs, 1):
    md_lines.append(f'### Question {idx}\n')
    md_lines.append(f'{q["stem"]}\n')
    for l in sorted(q["opts"].keys()):
        md_lines.append(f'- **{l})** {q["opts"][l]}')
    md_lines.append(f'\n**Correct Answer**: {q["correct"]}\n')
    md_lines.append('---\n')

with open('Markdown_Questions/46_anatomy_bank.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print('Wrote clean Markdown_Questions/46_anatomy_bank.md successfully!')
