import re

md_path = 'surgery/Markdown_Questions/24_Azhar_Cairo_QBank.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

header = content[:content.find('### Question 1')]
blocks = re.split(r'\n(?=### Question \d+)', content[content.find('### Question 1'):])

cleaned_blocks = []

# Specific stem corrections dictionary for heavily garbled OCR stems
stem_fixes = {
    1: "Five days after cholecystectomy, an asymptomatic middle aged woman is found to have a serum sodium 120meq/l. Proper management would be:",
    7: "A 30-year-old woman in the last trimester of pregnancy suddenly develops massive swelling of the left lower extremity from the inguinal ligament to the ankle. The correct sequence of work up and treatment should be:",
    52: "Each of the following is a recognized complication of massive blood transfusion EXCEPT:",
    133: "C-reactive protein (CRP):",
    188: "A patient is brought to the emergency room following a motor vehicle collision with blunt chest trauma against the steering wheel. Examination reveals multiple palpable rib fractures and flail chest. Initial management should be:",
    193: "A patient sustains a gunshot wound to the left buttock. He is hemodynamically stable. There is no exit wound. Management would include:",
    200: "A 26-year-old man sustains a gunshot wound to the abdomen. Exploration reveals a laceration of the infra-renal inferior vena cava. Initial management should be:",
    208: "In a patient with third-degree burns, application of skin grafts over the eschar should be performed in order to:",
    214: "Total extracellular fluid space is determined primarily by which of the following?",
    221: "Infections that require operative treatment include all of the following EXCEPT:",
    230: "The tumor, node, metastases (TNM) classification of malignant melanoma includes all of the following EXCEPT:",
    231: "A patient with a 3-mm deep melanoma of the face with a clinically positive jugular lymph node should be treated with:",
    245: "Management of leukoplakia of the oral cavity includes:",
    246: "A 4.5-kg infant, born following uncomplicated labor and delivery, is noted to have a swelling in the neck. The swelling is situated over the lower third of the sternocleidomastoid muscle. The diagnosis is:",
    281: "A 14-year-old girl has a breast mass that is well-circumscribed, firm, mobile, and non-tender. The most likely diagnosis is:",
    282: "When galactorrhea occurs in a high school girl, a diagnostic finding associated with elevated prolactin is:",
    284: "Fibrocystic disease of the breast has been associated with elevated blood levels of:",
    287: "Incisional biopsy of a breast mass in a 35-year-old woman demonstrates atypical ductal hyperplasia. The management should include:",
    288: "True statements about discharge from the nipple include:",
    300: "The benign disorder most likely to mimic carcinoma of the breast is:",
    301: "Which of the following increases the risk of breast cancer?",
    322: "Scar formation is part of the normal healing process following injury. Which of the following tissues has the ability to heal without scar formation?",
    324: "All of the following statements about thyroid hormones and metabolism are true EXCEPT:",
    329: "Initial management of a patient presenting with acute arterial occlusion of the lower extremity includes:",
    334: "A patient who develops dizziness, drop attacks, and diplopia with arm exercise most likely has:",
    340: "Which of the following is characteristic of causalgia of the extremity EXCEPT:",
    342: "Which of the following is NOT seen in phlegmasia cerulea dolens?",
    343: "The initial dose of unfractionated heparin (UFH) to fully heparinize a patient with deep venous thrombosis is:",
    344: "Initial therapy of a patient with mesenteric venous thrombosis without peritonitis is:",
    346: "The primary treatment for lymphedema is:",
    352: "A 25-year-old woman presents with painful superficial thrombophlebitis of the left leg. Conservative management should include:",
    357: "Which of the following hemodynamic abnormalities is associated with a large arteriovenous fistula?",
    361: "Which statement regarding content and preparation for elective colon resection is true?",
    362: "A fully heparinized patient develops a condition requiring emergency surgery. After cessation of heparin infusion, reversing the anticoagulant effect can be accomplished by:",
    365: "Exsanguinating hemorrhage is most likely to follow which of the following injuries?",
    366: "Frozen plasma prepared from freshly donated blood is necessary when a patient:",
    368: "Each of the following is a symptom of hemolytic transfusion reaction EXCEPT:",
    376: "Which of the following statements concerning inguinal hernia anatomy is correct?",
    379: "A sliding hernia is characterized by which of the following?",
    384: "Spontaneous closure of which of the following abnormalities of the abdominal wall occurs most frequently?",
    387: "A sliding hernia in an elderly patient:",
    388: "When a sliding hernia is present in the right groin, the most common finding is:",
    392: "The following statement(s) is/are true concerning direct inguinal hernias EXCEPT:"
}

for b in blocks:
    b_s = b.strip()
    if not b_s.startswith('### Question'): continue
    q_num = int(re.search(r'### Question (\d+)', b_s).group(1))
    
    lines = b_s.split('\n')
    stem_lines = []
    other_lines = []
    in_stem = False
    
    for l in lines:
        if re.match(r'^### Question \d+', l):
            in_stem = True
            other_lines.append(l)
            continue
        if re.match(r'^-\s+\*\*[A-F]\)\*\*', l):
            in_stem = False
            other_lines.append(l)
            continue
        if re.match(r'^-\s+\*\*Correct Answer\*\*:', l):
            in_stem = False
            other_lines.append(l)
            continue
        if in_stem:
            if l.strip():
                stem_lines.append(l.strip())
        else:
            other_lines.append(l)
            
    stem = ' '.join(stem_lines).strip()
    
    # Check if we have an explicit medical fix
    if q_num in stem_fixes:
        stem = stem_fixes[q_num]
    else:
        # General cleaning pipeline
        # Strip directions & section banners
        stem = re.sub(r'^(?:——+.*?case\.\s*|DIRECTIONS:.*?(?:case|section)\.\s*|Four answers\.\s*Select the ONE lettered answer that\s*|Select the ONE lettered answer that Is the BEST in each case\.\s*)', '', stem, flags=re.I).strip()
        stem = re.sub(r'^(?:Pre\s*-\s*and Post-operative Care & Surgical Critical Care|Basics of Surgery|Vascular Surgery|Hernia|Breast|Head & Neck|Allergy, Infections, Skin & Burns|Fluid & Metabolic Support|Wound, Healing & Trauma)\s*', '', stem, flags=re.I).strip()
        stem = re.sub(r'^\s*\(Questions \d+ through \d+\)[^A-Z]*', '', stem).strip()
        # Strip leading numbers/junk: e.g. ", 7 ", "54, ", "40 50. ", "94, "
        stem = re.sub(r'^[\s,;\.\-\–\_~|/\\0-9\(\)]+(?=[A-Z])', '', stem).strip()
        # Strip OCR banner gibberish
        stem = re.sub(r'^\s*(?:[A-Z]{2,}\s+){3,}(?=[A-Z][a-z])', '', stem).strip()
        # Clean double spaces
        stem = re.sub(r'\s{2,}', ' ', stem).strip()
        
    # Reassemble block
    new_block = [other_lines[0], '', stem, ''] + other_lines[1:]
    cleaned_blocks.append('\n'.join(new_block))

final_content = header + '\n\n---\n\n'.join(cleaned_blocks) + '\n'

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f'Successfully deep-cleaned {len(cleaned_blocks)} questions in {md_path}!')
