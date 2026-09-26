import re

c = open('Markdown_Questions/75_مذكرة_حل_احمد_صلاح_pms.md', encoding='utf-8').read()

# Let's split into header and questions
parts = c.split('### Question 1\n')
header = parts[0]
q_text = '### Question 1\n' + parts[1]

# Split all questions
blocks = re.split(r'### Question \d+\n', q_text)[1:]

# Let's clean each question and merge fragments
# We can identify fragmented blocks by:
# 1) Starts with incomplete lowercase sentence
# 2) Has missing options
# Let's write specific replacements for the known split blocks

replacements = {
    16: """### Question 16

What happens during dorsiflexion?

- **A)** The bottom of the foot moves toward the calf, decreasing the angle between those two surfaces, which leaves the toes pointing away from the body
- **B)** The top of the foot moves toward the shin, decreasing the angle between those two surfaces, leaving the toes pointing toward the head
- **C)** The foot twists to the left
- **D)** The foot twists to the right

**Correct Answer**: B

---
""",
    17: "", # merged into 16
    18: "", # merged into 16

    19: """### Question 19

What happens during plantarflexion?

- **A)** The top of the foot moves toward the shin, decreasing the angle between those surfaces
- **B)** The bottom of the foot moves toward the calf, decreasing the angle between those surfaces, pointing toes away from the body
- **C)** The foot moves medially
- **D)** The foot moves laterally

**Correct Answer**: B

---
""",

    29: """### Question 29

Which statement describes flexion?

- **A)** Movement that increases the angle between two structures or joints, causing the structures to straighten or move apart
- **B)** Movement that decreases the angle between two structures or joints, causing the structures to bend or move closer together
- **C)** Flexing a muscle
- **D)** Relaxing a muscle

**Correct Answer**: B

---
""",
    30: "", # merged into 29
    31: "", # merged into 29

    33: """### Question 33

The plane which divides body into anterior and posterior parts is:

- **A)** Sagittal
- **B)** Coronal
- **C)** Transverse
- **D)** Mid sagittal

**Correct Answer**: B

---
""",

    40: """### Question 40

Which statement is false regarding the anatomical position?

- **A)** The body is erect and facing forward
- **B)** The arms are at the sides
- **C)** The feet are parallel and flat on the floor
- **D)** The palms are facing backward (posteriorly)
- **E)** The thumbs point laterally

**Correct Answer**: D

---
""",

    111: """### Question 111

The axial skeleton groups together which sets of bones?

- **A)** The arms and hands, the legs and feet
- **B)** The pectoral and pelvic girdles
- **C)** The skull and facial bones only
- **D)** Bones of the skull and face, thoracic cage and vertebral column

**Correct Answer**: D

---
""",
    112: "",

    224: """### Question 224

At E/M level the centrioles show:

- **A)** Nine triplets of microtubules and no central singles
- **B)** Nine triplets of microtubules and two central singles
- **C)** Nine doublets of microtubules and two central singles
- **D)** Nine doublets of microtubules and no central singles

**Correct Answer**: A

---
""",
    225: "",

    232: """### Question 232

Lipids in the plasma membrane:

- **A)** Are phospholipid and cholesterol
- **B)** Phospholipid molecules consist of 2 hydrophobic fatty acid chains and 2 hydrophilic heads
- **C)** The hydrophobic chains project outward
- **D)** Cholesterol is located outside the bilayer

**Correct Answer**: A

---
""",
    233: "",

    297: """### Question 297

Regarding Golgi saccules:

- **A)** Their convex surfaces give rise to secretory vesicles
- **B)** They are interconnected with each other
- **C)** They are continuous with the nuclear membrane
- **D)** Their concave surface is the forming surface

**Correct Answer**: B

---
""",
    298: "",

    311: """### Question 311

Transfer vesicles originate from:

- **A)** Rough endoplasmic reticulum
- **B)** Lysosomes
- **C)** Cell membrane
- **D)** Peroxisomes
- **E)** Immature (cis) face of Golgi

**Correct Answer**: A

---
""",

    328: """### Question 328

Which of following plays an important role in secretory system of cells?

- **A)** Cilia
- **B)** Mitochondria
- **C)** Centrioles
- **D)** Golgi apparatus

**Correct Answer**: D

---
""",

    365: """### Question 365

Which organelle protects the cells from the damaging effect of medications and toxins?

- **A)** Ribosomes
- **B)** Lysosomes
- **C)** Smooth endoplasmic reticulum
- **D)** Centrosome
- **E)** Peroxisomes

**Correct Answer**: C

---
""",

    433: """### Question 433

Where does the spinal cord start and finish?

- **A)** It extends from the foramen magnum to L1 - L2
- **B)** It extends from foramen magnum to S2
- **C)** It extends from C1 to coccyx
- **D)** It extends from C7 to L5

**Correct Answer**: A

---
""",
    434: "",

    457: """### Question 457

Which nerve cells carry impulses from the brain to the muscles?

- **A)** Sensory neurons
- **B)** Motor neurons
- **C)** Interneurons
- **D)** Glial cells

**Correct Answer**: B

---
""",
    458: "",

    474: """### Question 474

Which of the following best describes the arrangement of lymphatic vessels?

- **A)** A one-way system of vessels beginning in tissues and returning lymph to the cardiovascular system
- **B)** A circular system of vessels carrying blood to and from heart
- **C)** A system that collects fluid from arteries and veins and returns it to kidneys
- **D)** A system that pumps lymph through lymphatic heart

**Correct Answer**: A

---
""",
    475: "",
    476: "",

    505: """### Question 505

The systemic circulation refers to which of the following?

- **A)** The movement of blood from the left ventricle through the body tissues and back to the right atrium
- **B)** The movement of blood into the coronary arteries only
- **C)** Blood flow through capillaries into the pulmonary veins
- **D)** Blood flow from the digestive tract to liver

**Correct Answer**: A

---
""",
    506: "",

    541: """### Question 541

Which of the following characteristics are true of epithelia?

- **A)** They line body surfaces
- **B)** They are avascular
- **C)** They have minimal intercellular substance
- **D)** All of the above

**Correct Answer**: D

---
""",
    542: "",

    586: """### Question 586

The function of simple squamous epithelium is:

- **A)** Diffusion and filtration
- **B)** Covering, secretion, absorption
- **C)** Secretion, protection
- **D)** Transport of particles

**Correct Answer**: A

---
""",
    587: "",

    765: """### Question 765

Notochord, choose one wrong statement:

- **A)** Helps formation of neural tube
- **B)** Gives nucleus pulposus
- **C)** Forms the vertebral bodies
- **D)** Induces overlying ectoderm

**Correct Answer**: C

---
""",
    766: """### Question 766

Regarding somites, mark one correct statement:

- **A)** They develop from the lateral plate mesoderm
- **B)** They develop from intermediate mesoderm
- **C)** They develop from paraxial mesoderm
- **D)** They give rise to the nervous system

**Correct Answer**: C

---
""",

    771: """### Question 771

Regarding somites, mark one correct statement:

- **A)** Sclerotome forms vertebrae and ribs
- **B)** Myotome forms skeletal muscle
- **C)** Dermatome forms dermis of skin
- **D)** All of the above

**Correct Answer**: D

---
""",
    772: "",

    807: """### Question 807

Regarding the placenta, mark one correct statement:

- **A)** Decidua basalis is the maternal part of placenta
- **B)** Chorion frondosum is the fetal part of placenta
- **C)** Syncytiotrophoblast synthesizes progesterone and hCG
- **D)** All of the above

**Correct Answer**: D

---
""",
    808: "",
    809: "",

    812: """### Question 812

Regarding full-term placenta, mark one correct statement:

- **A)** Full term placenta is discoid in shape
- **B)** Its diameter is about 15-25 cm
- **C)** Its weight is about 500 gm
- **D)** Its fetal surface is smooth and covered by amnion
- **E)** All of the above

**Correct Answer**: E

---
""",
    813: "",

    818: """### Question 818

Which of the following represents the maternal part of placenta?

- **A)** Decidua basalis
- **B)** Chorion frondosum
- **C)** Amnion
- **D)** Yolk sac

**Correct Answer**: A

---
""",
    819: "",

    825: """### Question 825

Regarding twins, mark one correct statement:

- **A)** In case of early separation of the zygote, each monozygotic twin has its own placenta
- **B)** Ahmad and Dina can be diagnosed as monozygotic twins
- **C)** Conjoined twins always have separate placentas
- **D)** Dizygotic twins are always identical

**Correct Answer**: A

---
""",
    826: ""
}

# Apply replacements to blocks
cleaned_blocks = []
for idx, b in enumerate(blocks, 1):
    if idx in replacements:
        rep = replacements[idx]
        if rep.strip():
            cleaned_blocks.append(rep)
    else:
        cleaned_blocks.append(f'### Question {idx}\n' + b)

print(f'Total blocks before: {len(blocks)}, after: {len(cleaned_blocks)}')

# Re-number sequentially 1 to N
final_blocks = []
for new_num, b in enumerate(cleaned_blocks, 1):
    # replace the Question \d+ with new_num
    b = re.sub(r'### Question \d+\n', f'### Question {new_num}\n', b, count=1)
    final_blocks.append(b.strip() + '\n\n---\n')

# Build final text
header = re.sub(r'Total Questions: \d+', f'Total Questions: {len(final_blocks)}', header)
final_text = header.strip() + '\n\n---\n\n' + '\n'.join(final_blocks)

open('Markdown_Questions/75_مذكرة_حل_احمد_صلاح_pms.md', 'w', encoding='utf-8').write(final_text)
print('Successfully repaired 75_مذكرة_حل_احمد_صلاح_pms.md!')
