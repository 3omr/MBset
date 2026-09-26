import re, os

def clean_text(s):
    if not s:
        return ""
    s = re.sub(r'[\u0600-\u06FF]+', '', s)
    s = s.replace('\u200b', '').replace('\ufeff', '').replace('\xa0', ' ')
    s = re.sub(r'^\s*(?:\d+[\.\-\)]|[A-Z][\.\)]|\- \*\*[A-F]\*\*)\s*', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def build_anatomy():
    with open('renal/markdown_output/Anatomy_Urinary_System_MCQ_Bank.md', 'r', encoding='utf-8') as f:
        text = f.read()

    blocks = re.split(r'####\s*\d+\.\s*', text)[1:]
    md = [
        '# Anatomy_Urinary_System_MCQ_Bank.md',
        '',
        '- **Source File**: `Anatomy_Urinary_System_MCQ_Bank.md`',
        '- **Tag**: `Department, Anatomy 2026`',
        '- **Year**: 2026',
        '- **Discipline / Subject**: `Anatomy`',
        f'- **Total Questions**: {len(blocks)}',
        '',
        '---',
        ''
    ]

    for idx, b in enumerate(blocks, 1):
        lines = [l.strip() for l in b.strip().splitlines() if l.strip()]
        stem = clean_text(lines[0])
        options = []
        correct_letter = 'A'
        explanation = ''
        
        for l in lines[1:]:
            m_opt = re.match(r'-\s*\[([ xX])\]\s*([a-fA-F])\.\s*(.+)', l)
            if m_opt:
                checked, letter, otext = m_opt.groups()
                opt_l = letter.upper()
                options.append(clean_text(otext))
                if checked.lower() == 'x':
                    correct_letter = opt_l
            elif l.startswith('> **Explanation:**'):
                explanation = clean_text(l.replace('> **Explanation:**', ''))
                
        md.append(f'### Question {idx}')
        md.append('')
        md.append(stem)
        md.append('')
        for o_i, o_t in enumerate(options):
            md.append(f'- **{chr(65+o_i)})** {o_t}')
        md.append('')
        md.append(f'**Correct Answer**: {correct_letter}')
        if explanation:
            md.append(f'**Explanation**: {explanation}')
        md.append('')
        md.append('---')
        md.append('')

    out_p = 'renal/Markdown_Questions/01_Anatomy_Urinary_System_MCQ_Bank.md'
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'Wrote {out_p}: {len(blocks)} Qs')

def build_biochem_written():
    biochem_qs = [
        ("Define buffers with examples", "Buffers are solutions that resist changes in pH when small amounts of acid or alkali are added. Examples include acidic buffers (e.g., acetic acid/sodium acetate, carbonic acid/bicarbonate) and basic buffers (e.g., ammonium hydroxide/ammonium chloride)."),
        ("Define acidosis", "Acidosis is a clinical state characterized by increased hydrogen ion concentration in blood, resulting in a blood pH < 7.35."),
        ("Define alkalosis", "Alkalosis is a clinical state characterized by decreased hydrogen ion concentration in blood, resulting in a blood pH > 7.45."),
        ("Enumerate mechanisms of regulation of blood pH", "1. First line of defense: Blood chemical buffers (bicarbonate, phosphate, hemoglobin, plasma proteins). 2. Second line of defense: Respiratory regulation (controlling CO2 elimination). 3. Third line of defense: Renal regulation (controlling H+ excretion and HCO3- reabsorption/regeneration)."),
        ("Explain: Why is the bicarbonate-carbonic acid system the most important buffer in plasma?", "It is the most important buffer because: 1. It is present in the highest concentration in plasma (24-28 mmol/L, accounting for 40-50% of buffering capacity). 2. Its components are independently and physiologically regulated: the base component (HCO3-) is regulated by the kidneys, and the acid component (CO2/H2CO3) is regulated by the lungs."),
        ("Enumerate the major renal mechanisms for regulation of pH", "1. Reabsorption of filtered bicarbonate (mainly in PCT). 2. Excretion of hydrogen ions (H+ secretion). 3. Excretion of titratable acid (mainly as NaH2PO4). 4. Excretion of ammonium ions (NH4+) via glutamine deamination."),
        ("Explain: Why may metabolic alkalosis develop during prolonged vomiting and gastric suction?", "Prolonged vomiting and gastric suction cause loss of gastric HCl, leading to hypochloremia and metabolic alkalosis. Loss of fluid also leads to volume depletion, stimulating aldosterone, which enhances H+ and K+ secretion and increases HCO3- reabsorption in the kidneys."),
        ("Explain: Why may sudden hypokalemia develop during rapid correction of metabolic acidosis?", "In metabolic acidosis, excess H+ ions move into cells in exchange for K+ moving out into ECF. When acidosis is rapidly corrected with bicarbonate or insulin, H+ moves out of cells and K+ rapidly shifts back into intracellular space, causing acute hypokalemia."),
        ("Explain: Why does morphine poisoning lead to respiratory acidosis?", "Morphine acts on the respiratory center in the brainstem to cause severe respiratory depression, leading to hypoventilation, CO2 retention, elevated PaCO2 (hypercapnia), and respiratory acidosis."),
        ("Describe the metabolic origin of atoms in the purine ring structure", "- N1: Aspartate. - C2 & C8: Formyl-tetrahydrofolate (Formyl-THF). - N3 & N9: Amide group of Glutamine. - C4, C5, and N7: Glycine. - C6: Respiratory CO2 (HCO3-)."),
        ("What are the metabolic causes of primary gout?", "1. Hyperactivity or increased activity of PRPP synthetase (overproduction of PRPP). 2. Partial deficiency of HGPRTase (decreased salvage pathway leading to accumulation of PRPP and accelerated de novo synthesis). 3. Glucose-6-phosphatase deficiency (Von Gierke disease)."),
        ("What is secondary gout and mention its causes?", "Secondary gout results from underlying medical conditions or drugs causing hyperuricemia: 1. Increased uric acid production due to increased cell turnover and lysis (e.g., leukemia, lymphoma, polycythemia, chemotherapy/radiation - tumor lysis syndrome). 2. Decreased renal uric acid excretion (e.g., chronic renal failure, use of thiazide or loop diuretics, lead poisoning, ketoacidosis, lactic acidosis)."),
        ("Explain: Why is the salvage pathway essential for some tissues?", "Tissues such as the brain and bone marrow have very low or absent de novo purine synthesis pathways, making them completely dependent on the salvage pathway (HGPRTase and APRTase) for nucleotide formation."),
        ("Explain: How does Glucose-6-phosphatase deficiency (Von Gierke's disease) lead to hyperuricemia?", "1. Glucose-6-phosphate cannot be converted to free glucose, so it accumulates and is diverted into the HMP shunt pathway, generating excess Ribose-5-phosphate. 2. Excess Ribose-5-P increases PRPP synthesis, stimulating de novo purine synthesis and degradation to uric acid. 3. Concomitant lactic acidosis competitively inhibits renal tubular secretion of uric acid, reducing its clearance."),
        ("What is the difference between a nucleotide and a nucleoside?", "- Nucleoside: Consists of a nitrogenous base (purine or pyrimidine) attached to a pentose sugar (ribose or deoxyribose) via a glycosidic bond. - Nucleotide: Consists of a nucleoside plus one or more phosphate groups attached by an ester bond (nitrogenous base + pentose sugar + phosphate)."),
        ("Explain the mechanism of action of Allopurinol", "Allopurinol is a structural analog of hypoxanthine. It competitively inhibits the enzyme xanthine oxidase and is converted by it into alloxanthine (oxypurinol), which is a non-competitive suicide inhibitor of xanthine oxidase. This reduces the synthesis of insoluble uric acid and leads to accumulation of hypoxanthine and xanthine, which are more water-soluble and easily excreted in urine."),
        ("Explain the effect of Methotrexate on purine synthesis", "Methotrexate is a folate analog that competitively inhibits the enzyme dihydrofolate reductase (DHFR). This prevents the regeneration of tetrahydrofolate (THF). Without THF, formyl-THF cannot be provided to donate carbons C2 and C8 to the purine ring, halting purine and thymidylate synthesis, thereby arresting DNA replication and cell division."),
        ("What are the types of dehydration and the difference between osmolarity and osmolality?", "Types of dehydration: 1. Isotonic dehydration: Proportional loss of water and electrolytes (normal serum osmolality). 2. Hypertonic dehydration: Water loss exceeds electrolyte loss (increased serum osmolality, e.g., diabetes insipidus, excessive sweating). 3. Hypotonic dehydration: Electrolyte loss exceeds water loss (decreased serum osmolality, e.g., chronic diuretic use, Addison's disease). Difference: - Osmolarity: Number of osmoles of solute per liter of solution (Osm/L). - Osmolality: Number of osmoles of solute per kilogram of solvent (Osm/kg H2O).")
    ]
    md = [
        '# Biochemistry Important written questions 2026.md',
        '',
        '- **Source File**: `Biochemistry Important written questions 2026.md`',
        '- **Tag**: `Department, Biochemistry 2026`',
        '- **Year**: 2026',
        '- **Discipline / Subject**: `Biochemistry`',
        f'- **Total Questions**: {len(biochem_qs)}',
        '',
        '---',
        ''
    ]
    for idx, (stem, ans) in enumerate(biochem_qs, 1):
        md.append(f'### Question {idx}')
        md.append('')
        md.append(stem)
        md.append('')
        md.append('**Type**: QROC')
        md.append('**Correct Answer**: -')
        md.append(f'**Explanation**: {ans}')
        md.append('')
        md.append('---')
        md.append('')

    out_p = 'renal/Markdown_Questions/03_Biochemistry_Important_Written_questions_2026.md'
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'Wrote {out_p}: {len(biochem_qs)} Qs')

def build_elmorshdy_written():
    el_qs = [
        ("Mention one causative organism of Weil's disease", "Leptospira interrogans."),
        ("Mention one causative organism of Lymphogranuloma venereum (LGV)", "Chlamydia trachomatis (serovars L1, L2, L3)."),
        ("Mention causative viruses of viral UTI", "Adenovirus (causes hemorrhagic cystitis), BK polyomavirus, JC polyomavirus, Herpes simplex virus (HSV)."),
        ("Mention causative organism of Psittacosis", "Chlamydia psittaci."),
        ("Mention causative organisms of Pyelonephritis", "Escherichia coli (UPEC - most common), Klebsiella pneumoniae, Proteus mirabilis, Enterococcus faecalis."),
        ("Enumerate 3 organisms that cause non-gonococcal urethritis (NGU)", "1. Chlamydia trachomatis (serovars D-K, most common). 2. Ureaplasma urealyticum. 3. Mycoplasma genitalium (or Mycoplasma hominis, Trichomonas vaginalis)."),
        ("Enumerate 2 risk factors of UTI", "1. Female gender (short straight urethra close to anus). 2. Urinary tract obstruction or instrumentation (e.g., prostatic hypertrophy, stones, urinary catheterization)."),
        ("Enumerate 2 virulence factors for E. coli and Pseudomonas aeruginosa", "- E. coli: P fimbriae (pyelonephritis-associated pili for urothelial adherence), K capsular antigen, endotoxin (LPS), hemolysin. - Pseudomonas aeruginosa: Exotoxin A (inhibits protein synthesis), Alginate slime capsule (biofilm formation), elastase, endotoxin."),
        ("Mention one Gram-negative bacillus without fermentation of sugars (non-fermenter)", "Pseudomonas aeruginosa (or Acinetobacter baumannii)."),
        ("Give reason: Females are more liable to UTI than males", "Females have a shorter urethra (approx. 4 cm vs 20 cm in males), which is straight, uncurved, and in close anatomical proximity to the perianal area and vagina, facilitating ascending colonization of fecal flora."),
        ("Give reason: Mycoplasma doesn't respond to penicillin", "Mycoplasma species naturally lack a peptidoglycan cell wall, which is the specific target of beta-lactam antibiotics like penicillin."),
        ("Give reason: Chlamydia was historically considered as a virus", "Because Chlamydia are obligate intracellular organisms that cannot synthesize their own ATP (energy parasites), are filterable through bacteriological filters due to small size, and only replicate inside host cells."),
        ("Give reason: Leptospira cannot be visualized by standard Gram staining", "Leptospira are extremely thin, delicate spirochetes with tight coils that fall below the resolving power of brightfield light microscopy and do not retain Gram stain reagents well; they require dark-field microscopy, silver impregnation (Fontana stain), or immunofluorescence."),
        ("Classify Chlamydia according to biphasic forms", "1. Elementary Body (EB): Small, extracellular, metabolically inactive, infectious, and resistant to environmental stress. 2. Reticulate Body (RB): Larger, intracellular, metabolically active, non-infectious, replicative form that divides by binary fission inside inclusion bodies."),
        ("Classify Gram-negative bacilli on MacConkey's agar as aetiological agents of UTI", "1. Lactose Fermenters (pink colonies): Escherichia coli, Klebsiella pneumoniae, Enterobacter. 2. Non-Lactose Fermenters (pale/colorless colonies): Proteus mirabilis, Pseudomonas aeruginosa."),
        ("Classify Urethritis regarding Neisseria gonorrhoeae", "1. Gonococcal Urethritis (GU): Caused by Neisseria gonorrhoeae (purulent discharge, Gram-negative intracellular diplococci). 2. Non-Gonococcal Urethritis (NGU): Caused by organisms other than N. gonorrhoeae (mainly Chlamydia trachomatis, Ureaplasma urealyticum, Mycoplasma genitalium)."),
        ("The most common causative agent of community-acquired UTI is", "Escherichia coli (Uropathogenic E. coli / UPEC, causing 80-90% of cases)."),
        ("The enzyme produced by Proteus that allows it to break down urea and invade the urinary tract is", "Urease (splits urea into ammonia and CO2, alkalinizing urine and precipitating struvite/triple phosphate stones)."),
        ("A Gram-negative pathogen that causes a characteristic 'swarming' pattern on culture", "Proteus mirabilis (or Proteus vulgaris)."),
        ("The infectious form of Chlamydia is ..., while the intracellular replicative form is ...", "The Elementary body (EB) is the infectious form, while the Reticulate body (RB) is the intracellular replicative form.")
    ]
    md = [
        '# Dr elmorshdy questions(Written).md',
        '',
        '- **Source File**: `Dr elmorshdy questions(Written).md`',
        '- **Tag**: `Department, Microbiology 2026`',
        '- **Year**: 2026',
        '- **Discipline / Subject**: `Microbiology`',
        f'- **Total Questions**: {len(el_qs)}',
        '',
        '---',
        ''
    ]
    for idx, (stem, ans) in enumerate(el_qs, 1):
        md.append(f'### Question {idx}')
        md.append('')
        md.append(stem)
        md.append('')
        md.append('**Type**: QROC')
        md.append('**Correct Answer**: -')
        md.append(f'**Explanation**: {ans}')
        md.append('')
        md.append('---')
        md.append('')

    out_p = 'renal/Markdown_Questions/04_Dr_Elmorshdy_questions_Written.md'
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'Wrote {out_p}: {len(el_qs)} Qs')

def build_histo_written():
    with open('renal/markdown_output/HistologyDepartmentbookQuestions(Written)2026.md', 'r', encoding='utf-8') as f:
        text = f.read()

    blocks = re.split(r'\n(?=\d+[\.\،]\s*)', text)[1:]
    md = [
        '# HistologyDepartmentbookQuestions(Written)2026.md',
        '',
        '- **Source File**: `HistologyDepartmentbookQuestions(Written)2026.md`',
        '- **Tag**: `Department, Histology 2026`',
        '- **Year**: 2026',
        '- **Discipline / Subject**: `Histology`',
        f'- **Total Questions**: {len(blocks)}',
        '',
        '---',
        ''
    ]

    for idx, b in enumerate(blocks, 1):
        lines = [l.strip() for l in b.strip().splitlines() if l.strip()]
        stem = clean_text(lines[0])
        ans = ' '.join(lines[1:]).replace('\u200b', '').strip()
        ans = clean_text(ans)
        
        md.append(f'### Question {idx}')
        md.append('')
        md.append(stem)
        md.append('')
        md.append('**Type**: QROC')
        md.append('**Correct Answer**: -')
        md.append(f'**Explanation**: {ans}')
        md.append('')
        md.append('---')
        md.append('')

    out_p = 'renal/Markdown_Questions/21_Histology_Department_Book_Questions_Written_2026.md'
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    print(f'Wrote {out_p}: {len(blocks)} Qs')

if __name__ == '__main__':
    build_anatomy()
    build_biochem_written()
    build_elmorshdy_written()
    build_histo_written()
