import os

questions = [
    # MCQs (QCS)
    {
        "type": "QCS",
        "stem": "A healthy 25-year-old man experiences a sudden rise in mean arterial pressure from 90 mmHg to 140 mmHg. Renal blood flow remains almost constant. Which mechanism is primarily responsible?",
        "options": [
            "Renin release",
            "Afferent arteriole constriction by myogenic theory",
            "Efferent arteriolar constriction",
            "Increased ADH secretion"
        ],
        "correct": "B",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Which of the following changes would you expect to find in a dehydrated person deprived of water for 24 hours?",
        "options": [
            "Decreased plasma renin activity",
            "Decreased plasma antidiuretic hormone concentration",
            "Increased plasma atrial natriuretic peptide concentration",
            "Increased water permeability of the collecting duct"
        ],
        "correct": "D",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Which of the following would be expected to cause a decrease in extracellular fluid potassium concentration (hypokalemia) at least in part by stimulating potassium uptake into the cells?",
        "options": [
            "Beta-adrenergic blockade",
            "Insulin",
            "Strenuous exercise",
            "Aldosterone deficiency (Addison's disease)"
        ],
        "correct": "B",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Once the act of urination has begun, the flow of urine through the urethra leads to more contraction of the detrusor muscle. Which nerve is responsible for carrying the afferent impulses from the urethra to the spinal center for this positive feedback?",
        "options": [
            "Hypogastric nerve",
            "Vagus nerve",
            "Pudendal nerve",
            "Pelvic nerve"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "CTP is synthesized from UTP in pyrimidine biosynthesis by using the amino group transferred from:",
        "options": [
            "Aspartate",
            "Glycine",
            "Glutamine",
            "PRPP"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Dihydro-orotic acid is converted to orotic acid in pyrimidine synthesis by the enzyme:",
        "options": [
            "Dihydro-orotase",
            "Orotate phosphoribosyl transferase",
            "Dihydro-orotate dehydrogenase",
            "Thymidylate synthase"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Nutrineal solution used in peritoneal dialysis contains which of the following osmotic agents to replace protein losses?",
        "options": [
            "Amino acids",
            "Icodextrin",
            "HCO3-",
            "Glucose"
        ],
        "correct": "A",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Which of the following is the most common and serious infectious complication of peritoneal dialysis?",
        "options": [
            "Nausea",
            "Abdominal infection (peritonitis)",
            "Insomnia",
            "Respiratory problems"
        ],
        "correct": "B",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Bumetanide belongs to which of the following classes of diuretics?",
        "options": [
            "Carbonic anhydrase inhibitor",
            "Aldosterone antagonist",
            "Thiazide diuretics",
            "Loop diuretics"
        ],
        "correct": "D",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "What advice should be given to a patient taking sulfamethoxazole/trimethoprim for a urinary tract infection to prevent drug-induced crystalluria?",
        "options": [
            "Increase dietary fiber",
            "Reduce fluid intake",
            "Drink plenty of fluids",
            "Avoid high-protein foods"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "The trigone of the urinary bladder develops embryologically from:",
        "options": [
            "The vesical part of the primitive urogenital sinus",
            "The proximal part of allantois",
            "The distal part of the mesonephric duct",
            "The distal end of the ureters"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Regarding the anatomy of the ureter, which statement is INCORRECT?",
        "options": [
            "It is about 25 cm long",
            "It lies posterior to the gonadal vessels",
            "It lies posterior to the genitofemoral nerve",
            "It crosses the bifurcation of the common iliac artery"
        ],
        "correct": "C",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "Renal arteries arise from the abdominal aorta at the vertebral level of:",
        "options": [
            "L1",
            "L2",
            "L3",
            "L4"
        ],
        "correct": "A",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "A 24-year-old female presents with symptoms of acute cystitis. A midstream urine culture isolates Escherichia coli. Which bacterial structure allows this organism to adhere specifically to uroepithelial cells of the bladder (colonization virulence factor)?",
        "options": [
            "Polysaccharide capsule",
            "Fimbriae (pili)",
            "Urease enzyme",
            "Flagella"
        ],
        "correct": "B",
        "exp": None
    },
    {
        "type": "QCS",
        "stem": "A 20-year-old sexually active female presents with her third UTI in six months. Which anatomical factor best explains her increased susceptibility to bacterial entry compared to a male?",
        "options": [
            "Anatomical position of the bladder",
            "A shorter urethra facilitating easier bacterial ascent",
            "Reduced local immune defenses in the bladder",
            "Increased urinary retention due to hormonal changes"
        ],
        "correct": "B",
        "exp": None
    },

    # Written Questions (QROC)
    {
        "type": "QROC",
        "stem": "Describe the mechanism of Na+ reabsorption in the thick ascending limb of the loop of Henle.",
        "options": [],
        "correct": "-",
        "exp": "In the thick ascending limb (TAL) of Henle's loop, Na+ is actively reabsorbed across the luminal (apical) membrane via the electroneutral Na+-K+-2Cl- cotransporter (NKCC2), driven by the basolateral Na+/K+-ATPase pump. Intracellular K+ recycles back into the tubular lumen through apical ROMK channels, generating a positive lumen-transepithelial potential (~+8 mV). This positive charge drives the paracellular reabsorption of cations, including Na+, Ca2+, and Mg2+."
    },
    {
        "type": "QROC",
        "stem": "Describe the mechanism by which a high-protein diet increases Renal Blood Flow (RBF) and GFR.",
        "options": [],
        "correct": "-",
        "exp": "A high-protein diet increases plasma amino acid levels, leading to increased amino acid filtration. Reabsorption of amino acids in the proximal convoluted tubule occurs via Na+-dependent secondary active cotransporters, enhancing proximal Na+ reabsorption. Consequently, less NaCl is delivered downstream to the macula densa cells in the early distal tubule. Decreased luminal NaCl at the macula densa blunts tubuloglomerular feedback (TGF), causing afferent arteriolar vasodilation, which increases glomerular capillary hydrostatic pressure, RBF, and GFR."
    },
    {
        "type": "QROC",
        "stem": "Enumerate the primary physiological functions of intercalated cells in the collecting ducts.",
        "options": [],
        "correct": "-",
        "exp": "1. Type A Intercalated Cells: Mediate acid secretion during acidosis via apical H+-ATPase and H+/K+-ATPase pumps, reabsorbing HCO3- into blood via basolateral Cl-/HCO3- exchangers (AE1) and reabsorbing K+.\n2. Type B Intercalated Cells: Mediate base secretion during alkalosis by secreting HCO3- into the lumen via apical pendrin (Cl-/HCO3- exchanger) and pumping H+ basolaterally via H+-ATPase."
    },
    {
        "type": "QROC",
        "stem": "Compare between the proximal and distal parts of the nephron regarding Na+ reabsorption, water permeability, glucose/amino acid handling, and tubular fluid osmolarity.",
        "options": [],
        "correct": "-",
        "exp": "1. Na+ Reabsorption: Proximal part reabsorbs ~65% of filtered load; distal part reabsorbs ~5-7%.\n2. Permeability to Water: Proximal part has high, obligatory water permeability (via constitutive AQP1); distal part (TAL and early DCT) is impermeable to water, while late DCT/collecting ducts have facultative permeability regulated by ADH (AQP2).\n3. Glucose and Amino Acids: Proximal part completely reabsorbs 100% of filtered load via Na+-cotransporters (SGLT); distal part is completely impermeable (no reabsorption).\n4. Tubular Fluid Osmolarity: Proximal tubular fluid remains isosmotic (~300 mOsm/L); distal tubular fluid is hypoosmotic (~100 mOsm/L) at early DCT (diluting segment) and becomes hyperosmotic (up to 1200 mOsm/L) in collecting ducts in the presence of ADH."
    },
    {
        "type": "QROC",
        "stem": "Match the following GFR determinants with their physiological effects on GFR:\n1. Increased Renal Blood Flow\n2. Increased Bowman's capsule hydrostatic pressure\n3. Increased Plasma oncotic pressure\n4. Increased Glomerular capillary hydrostatic pressure",
        "options": [],
        "correct": "-",
        "exp": "1. Increased Renal Blood Flow -> Increases GFR by elevating filtration pressure and maintaining hydrostatic pressure along capillaries.\n2. Increased Bowman's capsule hydrostatic pressure -> Decreases GFR due to increased opposing back-pressure.\n3. Increased Plasma oncotic pressure -> Decreases GFR by opposing filtration pressure across capillary wall.\n4. Increased Glomerular capillary hydrostatic pressure -> Increases GFR by raising forward filtration hydrostatic pressure."
    },
    {
        "type": "QROC",
        "stem": "Explain why metabolic alkalosis may develop during prolonged gastric suction or severe vomiting.",
        "options": [],
        "correct": "-",
        "exp": "Gastric suction or vomiting causes massive loss of acidic gastric secretion containing HCl. As gastric parietal cells produce H+ and secrete it into the lumen, they generate an equivalent amount of HCO3- into the blood (alkaline tide). Loss of H+ prevents neutralization of this bicarbonate. Concurrently, loss of water and NaCl causes extracellular fluid (ECF) volume contraction, activating the renin-angiotensin-aldosterone system (RAAS). High aldosterone stimulates renal H+ and K+ excretion and accelerates HCO3- reabsorption in the proximal and collecting tubules, sustaining contraction metabolic alkalosis."
    },
    {
        "type": "QROC",
        "stem": "Explain the difference between Osmolarity and Osmolality.",
        "options": [],
        "correct": "-",
        "exp": "- Osmolarity: The number of osmoles of solute per liter of solution (Osm/L). It is affected by ambient temperature and pressure because liquid volume changes with temperature.\n- Osmolality: The number of osmoles of solute per kilogram of solvent (Osm/kg H2O). It is independent of temperature and pressure, making it the preferred and standard measurement in clinical medicine and body fluid physiology."
    },
    {
        "type": "QROC",
        "stem": "Enumerate the four major renal mechanisms involved in the physiological regulation of blood pH.",
        "options": [],
        "correct": "-",
        "exp": "1. Reabsorption of filtered bicarbonate (HCO3-), mainly in the proximal convoluted tubule (~85%).\n2. Active secretion of hydrogen ions (H+) by proximal tubule (Na+/H+ exchanger) and intercalated cells (H+-ATPase).\n3. Excretion of titratable acid, primarily through buffering secreted H+ with filtered monohydrogen phosphate (HPO4^2- -> H2PO4^-).\n4. Excretion of ammonium ions (NH4+), generated through renal ammoniagenesis and deamination of glutamine in proximal tubule cells."
    },
    {
        "type": "QROC",
        "stem": "Describe the metabolic sources of all atoms in the purine ring structure.",
        "options": [],
        "correct": "-",
        "exp": "- N1: Derived from Aspartate.\n- C2 and C8: Derived from N10-formyl-tetrahydrofolate (formyl-THF).\n- N3 and N9: Derived from the amide nitrogen of Glutamine.\n- C4, C5, and N7: Derived intact from Glycine.\n- C6: Derived from respiratory bicarbonate / carbon dioxide (CO2)."
    },
    {
        "type": "QROC",
        "stem": "Discuss the paradoxical antidiuretic effect of thiazide diuretics in the management of Nephrogenic Diabetes Insipidus (NDI).",
        "options": [],
        "correct": "-",
        "exp": "Thiazide diuretics inhibit the electroneutral Na+/Cl- cotransporter in the early distal convoluted tubule, producing mild natriuresis and extracellular fluid (ECF) volume depletion. This contraction stimulates compensatory hyper-reabsorption of sodium and water in the proximal convoluted tubule. Consequently, a reduced volume of tubular fluid is delivered to the loop of Henle and distal collecting ducts, paradoxically reducing the polyuria of diabetes insipidus by up to 50%."
    },
    {
        "type": "QROC",
        "stem": "Compare Torsemide vs Ethacrynic acid and Amiloride vs Triamterene regarding potency, side effects, safety, and mechanism of action.",
        "options": [],
        "correct": "-",
        "exp": "1. Torsemide vs Ethacrynic acid: Both inhibit NKCC2 in loop of Henle. Torsemide is a potent sulfonylurea loop diuretic with higher bioavailability and longer half-life; Ethacrynic acid is a phenoxyacetic acid derivative without sulfa moiety (safe in patients with severe sulfa allergy), but has a significantly higher risk of severe, permanent ototoxicity.\n2. Amiloride vs Triamterene: Both block apical epithelial sodium channels (ENaC) in cortical collecting ducts, sparing potassium. Amiloride is more potent and excreted unchanged in urine; Triamterene is metabolized by the liver, has shorter duration, and can precipitate in urine causing renal calculi (triamterene stones)."
    },
    {
        "type": "QROC",
        "stem": "Define Morris's parallelogram and explain its anatomical significance.",
        "options": [],
        "correct": "-",
        "exp": "Morris's parallelogram is a surface anatomy quadrilateral used to project the position of both kidneys onto the posterior abdominal wall (lumbar region). It is bounded by:\n- Superior horizontal line: Passing at the level of the T11 spine (transverse process).\n- Inferior horizontal line: Passing at the level of the L3 spine.\n- Medial vertical line: Parallel to the midline, 2.5 cm (1 inch) lateral.\n- Lateral vertical line: Parallel to the midline, 9.5 cm (3.75 inches) lateral."
    },
    {
        "type": "QROC",
        "stem": "Outline the embryological development of the metanephros (permanent kidney).",
        "options": [],
        "correct": "-",
        "exp": "The metanephros develops during the 5th week of intrauterine life from two separate embryological sources:\n1. Ureteric Bud: An outgrowth from the lower part of the mesonephric duct that penetrates the metanephric blastema, giving rise to the collecting system: ureter, renal pelvis, major calyces, minor calyces, and 1 to 3 million collecting ducts.\n2. Metanephric Blastema (Metanephrogenic tissue): Derived from sacral intermediate mesoderm, giving rise to the excretory units (nephrons): Bowman's capsule, proximal convoluted tubule, loop of Henle, and distal convoluted tubule."
    },
    {
        "type": "QROC",
        "stem": "Enumerate the physiological anatomical sites of ureteric constriction.",
        "options": [],
        "correct": "-",
        "exp": "1. Pelvi-ureteric junction (PUJ): Where the expanded renal pelvis tapers into the ureter.\n2. Pelvic brim: Where the ureter crosses anterior to the bifurcation of the common iliac vessels.\n3. Ureterovesical junction (UVJ): Where the ureter passes obliquely through the muscular wall of the urinary bladder."
    },
    {
        "type": "QROC",
        "stem": "A sewage worker working in public sanitation with animal excreta presents with fever, headache, severe muscle aches, conjunctival suffusion, jaundice, and acute renal failure:\n1. What is the most likely causative organism and disease?\n2. What diagnostic method is more reliable: dark-field microscopy or bacterial culture, and why?",
        "options": [],
        "correct": "-",
        "exp": "1. Organism & Disease: Leptospira interrogans; the condition is severe leptospirosis / Weil's disease (icterohemorrhagic leptospirosis).\n2. Diagnostic reliability: Dark-field microscopy and serological testing (Microscopic Agglutination Test / MAT or IgM ELISA) are far more reliable than bacterial culture. Leptospira are extremely fastidious organisms that require specialized enriched media (e.g., Fletcher's or EMJH media), grow very slowly (requiring 2 to 6 weeks of incubation), and have a very low culture yield from clinical blood and urine specimens."
    },
    {
        "type": "QROC",
        "stem": "State four distinct microbiological reasons why Chlamydia trachomatis is classified as a bacterium and not a virus.",
        "options": [],
        "correct": "-",
        "exp": "1. Chlamydia contains both DNA and RNA nucleic acids simultaneously (viruses possess only DNA or RNA, never both).\n2. Chlamydia possesses a true bacterial cell wall containing peptidoglycan, lipopolysaccharide (LPS), and an outer membrane.\n3. Chlamydia reproduces autonomously by binary fission (viruses replicate through assembly of viral components by host machinery).\n4. Chlamydia possesses 70S bacterial ribosomes, metabolic enzymes, and is susceptible to antibacterial antibiotics (e.g., macrolides, tetracyclines), while viruses are unaffected by antibacterials."
    },
    {
        "type": "QROC",
        "stem": "Enumerate four parasites that clinically affect the human urinary system.",
        "options": [],
        "correct": "-",
        "exp": "1. Schistosoma haematobium (urinary bilharziasis, causing hematuria and bladder cancer).\n2. Trichomonas vaginalis (causes vaginitis and urethritis in females and nongonococcal urethritis in males).\n3. Echinococcus granulosus (hydatid disease with cysts in renal parenchyma).\n4. Wuchereria bancrofti (causes lymphatic filariasis with lymphatic rupture leading to chyluria) or Enterobius vermicularis (causes nocturnal enuresis and ectopic urethritis)."
    },
    {
        "type": "QROC",
        "stem": "Explain the pathological changes in the urinary bladder wall caused by Schistosoma haematobium infection.",
        "options": [],
        "correct": "-",
        "exp": "Deposition of terminal-spined Schistosoma haematobium eggs in the submucosa of the urinary bladder evokes a granulomatous reaction composed of eosinophils, lymphocytes, histiocytes, and multinucleated foreign-body giant cells. Pathological sequelae include:\n1. Bilharzial polyps (fleshy hyperplastic mucosal projections containing dense egg clusters).\n2. Sandy patches (calcified, dead ova visible beneath atrophic, scarred epithelium appearing as granular yellowish-brown mucosa).\n3. Ulcerations and trabeculation of the bladder wall.\n4. Squamous metaplasia of urothelium, which predisposes to squamous cell carcinoma of the bladder."
    },
    {
        "type": "QROC",
        "stem": "Outline the clinical and medical treatment options for Hydatid disease (Echinococcus granulosus).",
        "options": [],
        "correct": "-",
        "exp": "1. Medical Antiparasitic Therapy: Albendazole (or mebendazole) administered pre- and post-procedure to sterilize cysts, reduce cyst size, and prevent secondary peritoneal seeding.\n2. PAIR Procedure: Minimally invasive percutaneous technique (Puncture of cyst, Aspiration of fluid, Injection of scolicidal agent like hypertonic saline or ethanol, Re-aspiration).\n3. Surgical Intervention: Total cystectomy or unroofing and capitonnage with scolicidal agent coverage for large, complicated, or superficial cysts at risk of rupture."
    },
    {
        "type": "QROC",
        "stem": "Describe the histological structure and functions of intraglomerular mesangial cells.",
        "options": [],
        "correct": "-",
        "exp": "Structure: Stellate-shaped cells located in the mesangium between glomerular capillaries, surrounded by an amorphous extracellular mesangial matrix, sharing the glomerular basement membrane with endothelial cells. They possess contractile microfilaments (actin and myosin), prominent cytoplasmic processes, and cell-surface receptors.\nFunctions:\n1. Structural support: Provide central structural anchoring for the glomerular capillary loops.\n2. Phagocytosis: Endocytose and clear trapped immune complexes, proteins, and cellular debris from the filtration barrier.\n3. Regulation of GFR: Contract in response to vasoconstrictors (angiotensin II, endothelin), reducing glomerular capillary surface area and modulating GFR.\n4. Synthesis of mesangial matrix and secretion of vasoactive prostaglandins and cytokines."
    },
    {
        "type": "QROC",
        "stem": "State the epithelial lining of: (a) Pelvis of the ureter, and (b) Female urethra.",
        "options": [],
        "correct": "-",
        "exp": "(a) Pelvis of the ureter: Lined by transitional epithelium (urothelium), composed of several layers of cells with umbrella-shaped superficial cells.\n(b) Female urethra: Lined by transitional epithelium near the bladder neck, which transitions to pseudostratified columnar epithelium in the middle part, and finally into non-keratinized stratified squamous epithelium near the external urethral orifice."
    },
    {
        "type": "QROC",
        "stem": "Describe the histological structure of the Malpighian renal corpuscle.",
        "options": [],
        "correct": "-",
        "exp": "The Malpighian renal corpuscle is a spherical vascular-epithelial filtration unit (~200 um diameter) consisting of:\n1. Glomerulus: A rounded network of anastomosing capillaries lined by fenestrated endothelium (pores 70-90 nm) lacking diaphragms, supplied by an afferent arteriole and drained by an efferent arteriole.\n2. Bowman's Capsule: A double-walled cup surrounding the glomerulus, featuring:\n   - Visceral layer: Formed of specialized epithelial cells (podocytes) that extend primary and secondary foot processes (pedicels) wrapping around capillary loops, forming filtration slits (25-30 nm) bridged by slit diaphragms.\n   - Parietal layer: Formed of simple squamous epithelium supported by a basal lamina.\n   - Bowman's space (Urinary space): The receptacle between visceral and parietal layers receiving the glomerular ultrafiltrate, continuous with the neck of the proximal convoluted tubule at the urinary pole."
    },
    {
        "type": "QROC",
        "stem": "Enumerate: (a) Major chemical types of urinary stones, and (b) Four benign tumors of the kidney.",
        "options": [],
        "correct": "-",
        "exp": "(a) Types of urinary stones:\n1. Calcium stones (~75-80%): Calcium oxalate and calcium phosphate.\n2. Triple phosphate / Struvite stones (~10-15%): Magnesium ammonium phosphate, associated with urease-producing bacteria (Proteus).\n3. Uric acid stones (~5-10%): Radiolucent stones in acidic urine.\n4. Cystine stones (~1-2%): Hexagonal crystals in genetic cystinuria.\n(b) Benign tumors of kidney:\n1. Renal papillary adenoma.\n2. Oncocytoma (derived from intercalated cells, mahogany-brown with central scar).\n3. Angiomyolipoma (associated with tuberous sclerosis).\n4. Medullary fibroma (renomedullary interstitial cell tumor)."
    },
    {
        "type": "QROC",
        "stem": "Compare between Wilms tumor (Nephroblastoma) and Renal Cell Carcinoma (RCC) regarding age of onset, histogenesis, microscopic picture, and clinical prognosis.",
        "options": [],
        "correct": "-",
        "exp": "1. Age of onset: Wilms tumor occurs almost exclusively in infants and young children (peak 2-5 years); RCC occurs predominantly in older adults (peak 50-70 years).\n2. Histogenesis: Wilms tumor originates from persistent embryonic metanephric blastema; RCC originates from mature renal tubular epithelial cells (mainly proximal convoluted tubule for clear cell RCC).\n3. Microscopic picture: Wilms tumor shows a classic triphasic pattern: blastemal sheets of small blue cells, epithelial primitive abortive tubules/glomeruloid structures, and mesenchymal stroma; RCC (clear cell) displays solid sheets and nests of large polygonal cells with clear, lipid- and glycogen-rich cytoplasm bounded by delicate sinusoidal fibrovascular network.\n4. Prognosis: Wilms tumor has an excellent cure rate (>90% 5-year survival) with combined nephrectomy and chemotherapy; RCC has variable, poorer prognosis if metastatic (~70% 5-year survival for localized clear cell RCC, highly resistant to conventional chemotherapy)."
    },
    {
        "type": "QROC",
        "stem": "Mention the light microscopic features of acute post-streptococcal glomerulonephritis (PSGN).",
        "options": [],
        "correct": "-",
        "exp": "Light microscopy of PSGN reveals diffuse, global proliferative glomerulonephritis characterized by:\n1. Marked hypercellularity of all glomeruli caused by intense proliferation of endothelial and mesangial cells.\n2. Prominent leukocytic infiltration of glomerular capillary tufts by neutrophils (exudative phase) and monocytes.\n3. Obliteration and compression of capillary lumens by swelling, proliferating cells and leukocytes, producing enlarged, bloodless glomeruli that fill Bowman's space.\n4. Red blood cell casts within tubular lumina."
    },
    {
        "type": "QROC",
        "stem": "State the definitive diagnosis for each of the following clinical presentations:\n(a) A neonate delivered with the right kidney located in the pelvis.\n(b) A 5-year-old child presenting with hematuria (smoky urine), mild proteinuria, periorbital edema, oliguria, hypertension, and azotemia two weeks after pharyngitis.\n(c) A neonate delivered with a congenitally small, undersized kidney containing a reduced number of normal calyces and nephrons.",
        "options": [],
        "correct": "-",
        "exp": "(a) Pelvic kidney (Renal ectopia due to failure of embryonic ascent from the pelvis).\n(b) Acute post-streptococcal glomerulonephritis (PSGN / Acute nephritic syndrome).\n(c) Renal hypoplasia."
    }
]

md = [
    '# Final 2026',
    '',
    '- **Source File**: `Final 2026.pdf`',
    '- **Tag**: `Exams, Final 2026`',
    '- **Year**: 2026',
    '- **Discipline / Subject**: `None`',
    f'- **Total Questions**: {len(questions)}',
    '',
    '---',
    ''
]

for idx, q in enumerate(questions, 1):
    md.append(f"### Question {idx}")
    md.append("")
    md.append(q['stem'])
    md.append("")
    if q['type'] == 'QCS':
        for o_i, opt in enumerate(q['options']):
            letter = chr(65 + o_i)
            md.append(f"- **{letter})** {opt}")
        md.append("")
        md.append(f"**Correct Answer**: {q['correct']}")
    else:
        md.append(f"**Correct Answer**: -")
        md.append(f"**EXP**: {q['exp']}")
    md.append("")
    md.append("---")
    md.append("")

with open('renal/Markdown_Questions/15_Final_2026.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md).strip() + '\n')

print(f"Wrote renal/Markdown_Questions/15_Final_2026.md: {len(questions)} clean questions!")
