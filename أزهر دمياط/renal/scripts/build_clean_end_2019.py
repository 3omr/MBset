import re

questions = [
    {
        "num": 1,
        "stem": "18th years female developed acute RT abdominal pain. She is diagnosed as stone in her ureter. In operation, the doctor identify the ureter as:",
        "options": [
            "A whitish cord which is non-pulsatile.",
            "Shows peristaltic activity when gently pinched with forceps.",
            "A whitish cord which is pulsatile.",
            "A & B.",
            "A & C."
        ],
        "correct": "D"
    },
    {
        "num": 2,
        "stem": "10th years boy suffering from abdominal pain. The doctor told his mother the kidney is Pelvic in site, which means:",
        "options": [
            "Opposite the sacrum and above the aortic bifurcation.",
            "Opposite the sacrum and below the aortic bifurcation.",
            "Opposite the sacrum at the aortic bifurcation.",
            "Opposite the sacrum at the common iliac bifurcation.",
            "Opposite the sacrum and below the common iliac bifurcation."
        ],
        "correct": "B"
    },
    {
        "num": 3,
        "stem": "30th years old female developed swelling on her back. She diagnosed as a tumour located on the posterior surface of the right kidney, the following muscles that might be invaded EXCEPT:",
        "options": [
            "Psoas major muscle.",
            "Rectus abdominis muscle.",
            "Transverse abdominis muscle.",
            "Quadratus lumborum muscle.",
            "Diaphragm."
        ],
        "correct": "B"
    },
    {
        "num": 4,
        "stem": "A pregnant female in the 4th week of human development. Which one of the following events is correct:",
        "options": [
            "The pronephric tubules disappear in both sexes at the end of the 4th week.",
            "The pronephric tubules disappear in both sexes early in the 4th week.",
            "The mesonephros stage appear early in the 4th week.",
            "A & B.",
            "A & C."
        ],
        "correct": "E"
    },
    {
        "num": 5,
        "stem": "20th years old male suffering from suprapubic pain. He has a problem in urinary bladder, which parts of the bladder is completely covered by peritoneum:",
        "options": [
            "Base.",
            "Infero-lateral surfaces.",
            "Neck.",
            "Superior surface.",
            "Apex."
        ],
        "correct": "D"
    },
    {
        "num": 6,
        "stem": "20th years old male suffering from retention of urine. The doctor asks the nurse to insert a catheter. She must use the following technique:",
        "options": [
            "At first, the external meatus should initially be pointed downwards.",
            "The penis is held up over the anterior abdominal wall to straighten the anterior curve.",
            "The penis is held down to the anterior abdominal wall.",
            "At first, the external meatus should initially be pointed upward.",
            "A & B."
        ],
        "correct": "B"
    },
    {
        "num": 7,
        "stem": "Collection of cortical tissue found between the medullary pyramids are called:",
        "options": [
            "Medullary rays",
            "Renal columns of Bertin",
            "Interlobular cortex",
            "Collecting ducts"
        ],
        "correct": "B"
    },
    {
        "num": 8,
        "stem": "The membranous urethra is lined by:",
        "options": [
            "Stratified squamous epithelium",
            "Stratified columnar epithelium",
            "Transitional epithelium",
            "Pseudostratified columnar epithelium"
        ],
        "correct": "D"
    },
    {
        "num": 9,
        "stem": "The juxtaglomerular apparatus is characterized by all the following EXCEPT:",
        "options": [
            "Located at vascular pole of the renal corpuscle",
            "Include mesangial cells located within the glomerulus",
            "Include cells found in the afferent arteriole",
            "Includes cells of the macula densa"
        ],
        "correct": "B"
    },
    {
        "num": 10,
        "stem": "The lumen of glomerular capillaries is lined by:",
        "options": [
            "Podocyte foot processes",
            "Mesangial cells",
            "Fenestrated endothelium",
            "Juxtaglomerular cells",
            "Continuous endothelium"
        ],
        "correct": "C"
    },
    {
        "num": 11,
        "stem": "In healthy adult individuals, the desire to void urine is first felt at a bladder volume of:",
        "options": [
            "50 ml",
            "150 ml",
            "400 ml",
            "600 ml"
        ],
        "correct": "B"
    },
    {
        "num": 12,
        "stem": "As regards Na handling in the kidney:",
        "options": [
            "It is reabsorbed by transcellular pathway only in PCDs.",
            "About 45% of filtered Na is reabsorbed from LH",
            "It is secreted in the CCDs",
            "It is reabsorbed passively in thin part of ascending limb of LH."
        ],
        "correct": "D"
    },
    {
        "num": 13,
        "stem": "Regarding the transport of glucose by renal tubules:",
        "options": [
            "In a healthy person, the distal tubule reabsorbs all the filtered glucose",
            "Glucose is secreted into tubular fluid in small amounts",
            "The transport maximum of glucose is about 37 mg/min",
            "Glucose transport by renal tubule is linked to sodium transport"
        ],
        "correct": "D"
    },
    {
        "num": 14,
        "stem": "In normal adult human on an average diet, the major buffer responsible for titratable acid in urine is:",
        "options": [
            "HCO3-",
            "Urea",
            "Uric acid",
            "Phosphate"
        ],
        "correct": "D"
    },
    {
        "num": 15,
        "stem": "Normally most of titratable acidity of urine is attributed to acid buffered by:",
        "options": [
            "Bicarbonate",
            "Phosphate",
            "Ammonia",
            "Uric acid"
        ],
        "correct": "B"
    },
    {
        "num": 16,
        "stem": "About micturition reflex, rise of intravesical pressure (IVP) produces all of the following EXCEPT:",
        "options": [
            "Contraction of detrusor muscle",
            "Relaxation of internal urethral sphincter",
            "Relaxation of external urethral sphincter",
            "Inhibition of spinal micturition reflex"
        ],
        "correct": "D"
    },
    {
        "num": 17,
        "stem": "When a person is dehydrated, hypotonic tubular fluid will be found in the:",
        "options": [
            "Glomerular filtrate",
            "Proximal tubule",
            "Loop of Henle (ascending limb / early DCT)",
            "Collecting ducts"
        ],
        "correct": "C"
    },
    {
        "num": 18,
        "stem": "The greatest amount of hydrogen ions secreted by proximal tubules is associated with:",
        "options": [
            "Excretion of potassium ions",
            "Excretion of hydrogen ions",
            "Reabsorption of calcium ions",
            "Reabsorption of bicarbonate ions",
            "Reabsorption of phosphate ions"
        ],
        "correct": "D"
    },
    {
        "num": 19,
        "stem": "If glomerular hydrostatic pressure is 60 mmHg, colloid osmotic pressure is 32 mmHg, Bowman capsule pressure is 18 mmHg, and GFR is 125 ml/min, the filtration coefficient (Kf) is:",
        "options": [
            "12.5 ml/min/mmHg",
            "5 ml/min/mmHg",
            "25 ml/min/mmHg",
            "50 ml/min/mmHg"
        ],
        "correct": "A"
    },
    {
        "num": 20,
        "stem": "Which of the following increases Renal Blood Flow (RBF)?",
        "options": [
            "Angiotensin II",
            "Antidiuretic hormone (ADH)",
            "Strong renal sympathetic stimulation",
            "Atrial natriuretic peptide (ANP)"
        ],
        "correct": "D"
    },
    {
        "num": 21,
        "stem": "The precursors for de novo purine synthesis are all of the following EXCEPT:",
        "options": [
            "Ribose 5-phosphate",
            "Glycine",
            "Tyrosine",
            "Aspartate"
        ],
        "correct": "C"
    },
    {
        "num": 22,
        "stem": "A 58-year-old man is awoken by throbbing pain in his great toe. He is diagnosed with acute gout. Allopurinol is prescribed to inhibit which of the following enzymes:",
        "options": [
            "Amido transferase",
            "PRPP synthetase",
            "Xanthine oxidase",
            "Orotate phosphoribosyl transferase"
        ],
        "correct": "C"
    },
    {
        "num": 23,
        "stem": "Which of the following conditions is associated with hypouricemia?",
        "options": [
            "Lesch-Nyhan syndrome",
            "Adenosine deaminase deficiency",
            "Overactivity of PRPP synthetase",
            "Overactivity of amido transferase"
        ],
        "correct": "B"
    },
    {
        "num": 24,
        "stem": "Osmosis is a special case of:",
        "options": [
            "Filtration",
            "Active transport",
            "Carrier transport",
            "Diffusion"
        ],
        "correct": "D"
    },
    {
        "num": 25,
        "stem": "Red blood cells would swell in which type of solution?",
        "options": [
            "Hypotonic",
            "Isotonic",
            "Hypertonic",
            "Hydrophilic"
        ],
        "correct": "A"
    },
    {
        "num": 26,
        "stem": "The predominant anion of plasma is:",
        "options": [
            "HCO3-",
            "Cl-",
            "HPO4--",
            "SO4--"
        ],
        "correct": "B"
    },
    {
        "num": 27,
        "stem": "The metabolism and reabsorption of sodium is primarily regulated by the hormone:",
        "options": [
            "Insulin",
            "Aldosterone",
            "PTH",
            "Somatostatin"
        ],
        "correct": "B"
    },
    {
        "num": 28,
        "stem": "All of the following are normal constituents of urine EXCEPT:",
        "options": [
            "Urea",
            "Ketone bodies",
            "Ammonia",
            "Creatinine"
        ],
        "correct": "B"
    },
    {
        "num": 29,
        "stem": "Cardiac arrest in diastole may occur due to overdose / severe elevation of:",
        "options": [
            "Sodium",
            "Potassium",
            "Zinc",
            "Magnesium"
        ],
        "correct": "B"
    },
    {
        "num": 30,
        "stem": "The volume of urine excreted in a 24-hour period by an adult patient was 300 mL. This condition is termed:",
        "options": [
            "Anuria",
            "Oliguria",
            "Polyuria",
            "Dysuria"
        ],
        "correct": "B"
    },
    {
        "num": 31,
        "stem": "Peritoneal dialysis uses a ______ as the access for treatment:",
        "options": [
            "Catheter",
            "Fistula",
            "Graft",
            "Dialysis machine"
        ],
        "correct": "A"
    },
    {
        "num": 32,
        "stem": "Which of the following antibodies is commonly elevated following skin infection in post-streptococcal glomerulonephritis (PSGN)?",
        "options": [
            "Anti-streptolysin O",
            "Anti-DNAse B",
            "Anti-hyaluronic acid",
            "Anti-adenine dinucleotidase"
        ],
        "correct": "B"
    },
    {
        "num": 33,
        "stem": "A patient presents with proteinuria, edema, and symptoms of renal insufficiency. Renal biopsy shows 'tram-track' appearance of glomerular basement membrane. The diagnosis is:",
        "options": [
            "Diabetic Nephropathy",
            "IgA Nephropathy",
            "Minimal Change Disease",
            "Membranoproliferative glomerulonephritis"
        ],
        "correct": "D"
    },
    {
        "num": 34,
        "stem": "Hematuria is LEAST likely to occur in which of the following conditions:",
        "options": [
            "Transitional cell carcinoma of the renal pelvis, ureter or bladder",
            "Acute post-infectious glomerulonephritis",
            "Urinary stones",
            "Minimal change glomerulonephritis"
        ],
        "correct": "D"
    },
    {
        "num": 35,
        "stem": "Each of the following features is characteristic of pure nephrotic syndrome EXCEPT:",
        "options": [
            "Marked Proteinuria",
            "Hypoalbuminemia",
            "Edema",
            "Hypertension"
        ],
        "correct": "D"
    },
    {
        "num": 36,
        "stem": "Infantile polycystic kidney disease (ARPKD) has the following features EXCEPT:",
        "options": [
            "It has autosomal recessive inheritance",
            "It is invariably bilateral",
            "The condition often manifests primarily in adults",
            "All the collecting tubules show cylindrical or saccular dilatations"
        ],
        "correct": "C"
    },
    {
        "num": 37,
        "stem": "Collapsing sclerosis is a prominent feature of which type of primary glomerular disease:",
        "options": [
            "Membranoproliferative GN",
            "IgA nephropathy",
            "Focal segmental glomerulosclerosis (FSGS)",
            "Membranous glomerulonephritis"
        ],
        "correct": "C"
    },
    {
        "num": 38,
        "stem": "Membranoproliferative glomerulonephritis is characterized by lobular proliferation of:",
        "options": [
            "Epithelial cells",
            "Endothelial cells",
            "Mesangial cells",
            "Leucocytes"
        ],
        "correct": "C"
    },
    {
        "num": 39,
        "stem": "The primary site of action of spironolactone is the:",
        "options": [
            "Proximal Convoluted Tubule",
            "Descending limb of Loop of Henle",
            "Late distal convoluted tubule and Collecting Duct",
            "Ascending limb of loop of Henle"
        ],
        "correct": "C"
    },
    {
        "num": 40,
        "stem": "Reabsorption of which of the following is affected maximum by the action of vasopressin (ADH)?",
        "options": [
            "Water",
            "Chloride",
            "Potassium",
            "Hydrogen"
        ],
        "correct": "A"
    },
    {
        "num": 41,
        "stem": "Which of the following is a carbonic anhydrase inhibitor?",
        "options": [
            "Acetazolamide",
            "Spironolactone",
            "Benzthiazide",
            "Clopamide"
        ],
        "correct": "A"
    },
    {
        "num": 42,
        "stem": "Loop diuretics increase urinary excretion of all of the following EXCEPT:",
        "options": [
            "Calcium",
            "Sodium",
            "Magnesium",
            "Uric acid"
        ],
        "correct": "D"
    },
    {
        "num": 43,
        "stem": "Which one of the following drug combinations is therapeutically valuable in preventing hypokalemia while managing refractory edema:",
        "options": [
            "Furosemide + Hydrochlorothiazide",
            "Furosemide + Indomethacin",
            "Furosemide + Spironolactone",
            "Furosemide + Bumetanide"
        ],
        "correct": "C"
    },
    {
        "num": 44,
        "stem": "Which of the following drugs is used in the management of nephrogenic diabetes insipidus?",
        "options": [
            "Furosemide",
            "Amiloride",
            "Hydrochlorothiazide",
            "Chlorthalidone"
        ],
        "correct": "C"
    },
    {
        "num": 45,
        "stem": "Proteus mirabilis is characterized as:",
        "options": [
            "Non-motile",
            "Highly motile with swarming and urease enzyme production",
            "Gram-positive bacillus",
            "Lactose fermenter"
        ],
        "correct": "B"
    },
    {
        "num": 46,
        "stem": "Leptospira is primarily transmitted to humans through:",
        "options": [
            "Blood products",
            "Body louse",
            "Water contaminated with animal urine",
            "Ticks"
        ],
        "correct": "C"
    },
    {
        "num": 47,
        "stem": "The causative agent of infectious mononucleosis is:",
        "options": [
            "Cytomegalovirus",
            "Varicella zoster virus",
            "Epstein-Barr virus",
            "Human herpes virus 6"
        ],
        "correct": "C"
    },
    {
        "num": 48,
        "stem": "As regards hydatidosis (Echinococcus granulosus), the FALSE statement is:",
        "options": [
            "The expanding hydatid cyst causes pressure necrosis of surrounding tissues.",
            "Man acts as the definitive host.",
            "Man is infected by ingestion of Echinococcus granulosus eggs.",
            "The commonest anatomical site of cysts is the liver."
        ],
        "correct": "B"
    },
    {
        "num": 49,
        "stem": "Which of the following best describes the signs and symptoms of Trichomonas vaginalis in females?",
        "options": [
            "Foul fishy odor, and thick clumpy white vaginal discharge.",
            "Malodorous, frothy yellowish-green vaginal discharge with pruritus.",
            "Dysuria, and thin milky-white vaginal discharge.",
            "None, the condition is always completely asymptomatic."
        ],
        "correct": "B"
    },
    {
        "num": 50,
        "stem": "As regards Schistosoma haematobium, the followings are true EXCEPT:",
        "options": [
            "It causes urinary schistosomiasis.",
            "Adult worms inhabit the vesical and pelvic venous plexuses.",
            "Man is the primary natural definitive host.",
            "Snail intermediate host is Biomphalaria alexandrina."
        ],
        "correct": "D"
    }
]

md = []
md.append("# End 2019")
md.append("")
md.append("- **Source File**: `End 2019.md`")
md.append("- **Tag**: `Exams, End 2019`")
md.append("- **Year**: 2019")
md.append("- **Discipline / Subject**: `None`")
md.append(f"- **Total Questions**: {len(questions)}")
md.append("")
md.append("---")
md.append("")

for q in questions:
    md.append(f"### Question {q['num']}")
    md.append("")
    md.append(q['stem'])
    md.append("")
    for i, opt in enumerate(q['options']):
        letter = chr(65 + i)
        md.append(f"- **{letter})** {opt}")
    md.append("")
    md.append(f"**Correct Answer**: {q['correct']}")
    md.append("")
    md.append("---")
    md.append("")

with open('renal/Markdown_Questions/05_End_2019.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md).strip() + '\n')

print("Wrote renal/Markdown_Questions/05_End_2019.md successfully!")
