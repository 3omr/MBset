import re

qs_data = [
    # Written Questions P1-3
    (1, "Brief the proliferative phase of the uterine cycle.", 
     "QROC", "-", {}, 
     "From 5th to 14th day. It follows the menstrual flow, lasts for about 10 days, and ends by the time of ovulation. It is characterized by repair and growth of the endometrium following menstruation. This phase is also called the estrogenic phase because it is controlled by estrogen secreted by theca interna surrounding growing ovarian follicles. The basal layer containing basal ends of endometrial glands remains to regenerate the epithelium. Glands elongate into loose stroma to become straight tubular glands. Endometrium thickens (>3 mm) and blood vessels reform and elongate."),
    
    (2, "Give a short account of the progestational (secretory) phase of the uterine cycle.", 
     "QROC", "-", {}, 
     "Called secretory phase (15th to 28th day). It begins after ovulation, lasts 14 days, and is under the influence of progesterone secreted by the corpus luteum. Endometrial glands become wide, elongated, tortuous, and distended with glycogen- and lipid-rich secretions. Spiral arteries become elongated and coiled, reaching the surface mucosa. Endometrium becomes thickened (>5 mm), edematous, and congested, ready to receive and nourish a fertilized ovum."),
    
    (3, "What about the menstrual phase of the uterine endometrium?", 
     "QROC", "-", {}, 
     "Menstruation is the first phase of the uterine cycle (lasting 3-5 days). The functional layer (compact layer and most of spongy layer) is sloughed off and discarded due to progesterone withdrawal. The basal layer remains intact to regenerate the endometrium during the subsequent proliferative phase."),
    
    (4, "Complete the missed hormones and phases of the menstrual/uterine cycle: H1, H2, H3, H4 and Phase 1, Phase 2, Phase 3.", 
     "QROC", "-", {}, 
     "H1: FSH; H2: LH; H3: Estrogen; H4: Progesterone. Phase 1: Menstrual phase; Phase 2: Proliferative phase; Phase 3: Secretory (luteal) phase."),

    # Digestive MCQs P4-5
    (5, "Regarding the small intestine, choose the CORRECT answer:", 
     "QCS", "C", 
     {"A": "It is 4 meters long", "B": "Has taeniae coli in its wall", "C": "Includes the duodenum in which the common bile duct opens", "D": "The anal canal forms its terminal part", "E": "The distal 2/5 is formed by the jejunum"}, None),
    
    (6, "Which of the following opens in the second part of duodenum:", 
     "QCS", "B", 
     {"A": "Appendix", "B": "Common bile duct and pancreatic duct", "C": "Gall bladder", "D": "Spleen"}, None),
    
    (7, "Regarding anatomy of the pharynx, choose the incorrect statement:", 
     "QCS", "E", 
     {"A": "It begins at the base of skull", "B": "It is formed mainly of 3 constrictor muscles", "C": "It ends at the level of C6", "D": "It shares as part of respiratory and digestive functions", "E": "It has complete anterior and posterior walls"}, None),
    
    (8, "Which of the following is TRUE about anatomy of the stomach?", 
     "QCS", "B", 
     {"A": "It has a narrow lesser curvature on the left border", "B": "It is connected to the esophagus by a sphincter", "C": "It is formed of inner circular and outer longitudinal muscles only", "D": "Its proximal end shows the pyloric sphincter", "E": "It has a narrow greater curvature on the right border"}, None),
    
    (9, "Which of the following is NOT a character of the large intestine?", 
     "QCS", "A", 
     {"A": "Hepato-pancreatic ampulla", "B": "Tenia coli", "C": "Appendices epiploicae", "D": "Ileo-cecal junction", "E": "Sacculations"}, None),

    # Reproduction Lectures 38-41 MCQs P6-9
    (10, "Fertilization normally takes place in the:", 
     "QCS", "E", 
     {"A": "Cervical canal", "B": "Peritoneal cavity", "C": "Uterine cavity", "D": "Isthmus of oviduct", "E": "Ampulla of oviduct"}, None),
    
    (11, "In how many days after fertilization does the fertilized ovum enter the uterine cavity?", 
     "QCS", "B", 
     {"A": "1 day", "B": "3 days", "C": "7 days", "D": "8 days", "E": "14 days"}, None),
    
    (12, "The ovulated mammalian oocyte is arrested at:", 
     "QCS", "D", 
     {"A": "prophase of meiosis I", "B": "prophase of meiosis II", "C": "metaphase of meiosis I", "D": "metaphase of meiosis II", "E": "none of the above"}, None),
    
    (13, "Haploid nuclei that fuse at fertilization are called:", 
     "QCS", "E", 
     {"A": "homunculi", "B": "mitotic figures", "C": "centrioles", "D": "nucleoli", "E": "pronuclei"}, None),
    
    (14, "Capacitation of the sperm:", 
     "QCS", "D", 
     {"A": "is caused by the zona pellucida", "B": "occurs in the male", "C": "prevents polyspermy", "D": "is essential for fertilization", "E": "removes the head of the sperm"}, None),
    
    (15, "The early stages of cleavage are characterized by:", 
     "QCS", "D", 
     {"A": "formation of a hollow ball of cells", "B": "formation of the zona pellucida", "C": "increase in the size of the cells in the zygote", "D": "increase in the number of cells in the zygote", "E": "none of the above"}, None),
    
    (16, "With the light microscope, the zona pellucida appears as a translucent membrane surrounding the:", 
     "QCS", "E", 
     {"A": "primary oocyte", "B": "zygote", "C": "morula", "D": "very early blastocyst", "E": "all of the above are correct"}, None),
    
    (17, "In humans, cleavage begins in the:", 
     "QCS", "B", 
     {"A": "ovary", "B": "oviduct", "C": "uterus", "D": "vagina", "E": "Cervical Canal"}, None),
    
    (18, "Increased glycogen and lipid deposits are part of the:", 
     "QCS", "C", 
     {"A": "menstrual phase", "B": "proliferative phase", "C": "secretory phase"}, None),
    
    (19, "Granulosa cells are the primary source of:", 
     "QCS", "C", 
     {"A": "FSH", "B": "LH", "C": "Oestrogen", "D": "Progesterone"}, None),
    
    (20, "In the corpus luteum:", 
     "QCS", "A", 
     {"A": "Granulosa and lutein cells secrete progesterone", "B": "Thecal and granulosa cells secrete progesterone", "C": "Thecal and lutein cells secrete progesterone"}, None),
    
    (21, "Ovulation is caused by:", 
     "QCS", "B", 
     {"A": "A surge in FSH levels", "B": "A surge in LH levels", "C": "A surge in progesterone levels"}, None),

    # Reproduction Written P7-9
    (22, "The stages of ovarian cycle are:", 
     "QROC", "-", {}, 
     "Follicular phase, Ovulation, and Luteal phase."),
    
    (23, "The secondary oocyte contains ... number of chromosomes:", 
     "QROC", "-", {}, 
     "23 chromosomes (haploid, 22 autosomes + 1 sex chromosome X)."),
    
    (24, "What is the duration of secretory phase of the uterine cycle, name the responsible ovarian hormone, and mention two characteristics occurring in the endometrium:", 
     "QROC", "-", {}, 
     "Duration: 14 days (from day 15 to day 28). Responsible hormone: Progesterone (secreted by corpus luteum). Characteristics: 1) Endometrial glands become wide, tortuous, and distended with glycogen/lipid secretion. 2) Spiral arteries become elongated, coiled, and extend to surface mucosa; endometrium thickens to >5 mm."),

    # Slide MCQs P11-29
    (25, "Which of the following is correct about mammalian testes?", 
     "QCS", "C", 
     {"A": "Graafian follicles, Sertoli cells, Leydig's cells", "B": "Graafian follicles, Sertoli cells, Seminiferous tubules", "C": "Sertoli cells, Seminiferous tubules, Leydig's cells", "D": "Graafian follicle, Leydig's cells, Seminiferous tubule"}, None),
    
    (26, "Temperature of the scrotum which is necessary for the functioning of testis is always around ... below body temperature:", 
     "QCS", "A", 
     {"A": "2°C", "B": "4°C", "C": "6°C", "D": "8°C"}, None),
    
    (27, "The nutritive cells found in seminiferous tubules are:", 
     "QCS", "C", 
     {"A": "Leydig's cells", "B": "atretic follicular cells", "C": "Sertoli cells", "D": "chromaffin cells"}, None),
    
    (28, "Sertoli cells are regulated by the pituitary hormone known as:", 
     "QCS", "B", 
     {"A": "LH", "B": "FSH", "C": "GH", "D": "prolactin"}, None),
    
    (29, "Spermatogenesis, reduction division of chromosome occurs during conversion of:", 
     "QCS", "B", 
     {"A": "spermatogonia to primary spermatocytes", "B": "primary spermatocytes to secondary spermatocytes", "C": "secondary spermatocytes to spermatids", "D": "spermatids to sperms"}, None),
    
    (30, "Which of the following groups of cells in the male gonad represent haploid cells?", 
     "QCS", "C", 
     {"A": "Spermatogonial cells", "B": "Germinal epithelial cells", "C": "Secondary spermatocytes", "D": "Primary spermatocytes"}, None),
    
    (31, "A single ejaculate contains approximately ... sperms:", 
     "QCS", "D", 
     {"A": "20 - 30 thousands", "B": "200 - 300 thousands", "C": "20 - 30 million", "D": "200 - 300 million", "E": "500 million at least"}, None),
    
    (32, "Which of the following parts of sperm is responsible for production of energy:", 
     "QCS", "A", 
     {"A": "Mitochondrial sheath", "B": "Nucleus", "C": "Acrosomal cap", "D": "Tail"}, None),
    
    (33, "Which of the following is not a feature of mature sperm cell?", 
     "QCS", "B", 
     {"A": "An acrosome containing digestive enzymes", "B": "A large amount of cytoplasm surrounding the nucleus", "C": "A midpiece and a long tail called a flagellum", "D": "A mitochondrial sheath around middle piece", "E": "A nucleus with 22 autosomes and 1 sex chromosome"}, None),
    
    (34, "Sperm cells must undergo ... before they can fertilize a secondary oocyte:", 
     "QCS", "A", 
     {"A": "Capacitation", "B": "Fertilization", "C": "Development", "D": "Differentiation"}, None),
    
    (35, "Sperms develop in the:", 
     "QCS", "A", 
     {"A": "Seminiferous tubules", "B": "Epididymis", "C": "Vas deferens", "D": "Prostate gland"}, None),
    
    (36, "Fusion of two haploid sex cells to produce a diploid zygote is:", 
     "QCS", "A", 
     {"A": "Fertilization", "B": "Ovulation", "C": "Cleavage", "D": "Implantation"}, None),
    
    (37, "All of a woman's primary oocytes are produced:", 
     "QCS", "C", 
     {"A": "between the ages of 16 and 24 years", "B": "within a year after she reaches puberty", "C": "before she is born", "D": "none of the above"}, None),
    
    (38, "A peak in ... triggers ovulation around the ... day of the 28 monthly cycle:", 
     "QCS", "A", 
     {"A": "LH ... 14th", "B": "FSH ... 7th", "C": "Estrogen ... 21st", "D": "Progesterone ... 1st"}, None),
    
    (39, "After ovulation Graafian follicle regresses into:", 
     "QCS", "A", 
     {"A": "Corpus luteum", "B": "Corpus albicans", "C": "Atretic follicle", "D": "Secondary follicle"}, None),
    
    (40, "Immediately after ovulation, the mammalian oocyte is surrounded by:", 
     "QCS", "A", 
     {"A": "Corona radiata and zona pellucida", "B": "Zona pellucida only", "C": "Theca interna only", "D": "Cumulus oophorus only"}, None),
    
    (41, "The vas deferens receives duct from the:", 
     "QCS", "A", 
     {"A": "Seminal vesicle", "B": "Bulbourethral gland", "C": "Prostate gland", "D": "Ureter"}, None),
    
    (42, "Mature Graafian follicle is generally present in the ovary of a healthy human female around:", 
     "QCS", "B", 
     {"A": "5-8 day of menstrual cycle", "B": "11-17 day of menstrual cycle", "C": "18-23 day of menstrual cycle", "D": "24-28 day of menstrual cycle"}, None),
    
    (43, "Which one of the following is not a male accessory gland?", 
     "QCS", "B", 
     {"A": "Seminal vesicle", "B": "Ampulla", "C": "Prostate", "D": "Bulbourethral gland"}, None),
    
    (44, "The oocyte finishes its second meiotic division:", 
     "QCS", "C", 
     {"A": "Immediately before ovulation", "B": "Immediately after ovulation", "C": "After entry of the spermatozoa", "D": "Prenatally", "E": "Before puberty"}, None),
    
    (45, "Concerning the luteinizing hormone (LH), choose the CORRECT statement:", 
     "QCS", "A", 
     {"A": "It is responsible for ovulation and corpus luteum formation", "B": "It is responsible for initial follicular growth", "C": "It is secreted by the posterior pituitary", "D": "It stimulates endometrial shedding"}, None),
    
    (46, "Regarding oogenesis, choose the FALSE statement:", 
     "QCS", "D", 
     {"A": "It starts during fetal life", "B": "It continues till menopause", "C": "The second meiotic division is completed only after fertilization", "D": "Primary oocytes are formed after birth"}, None)
]

md_lines = [
    '# anatomy department.pdf\n',
    '- **Source File**: `anatomy department.pdf`',
    '- **File Type**: Text PDF',
    '- **Total Pages / Slides**: 49',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(qs_data)}\n',
    '---\n'
]

for num, stem, q_type, ans, opts, exp in qs_data:
    md_lines.append(f'### Question {num}\n')
    md_lines.append(f'{stem}\n')
    if q_type == 'QCS':
        for l in sorted(opts.keys()):
            md_lines.append(f'- **{l})** {opts[l]}')
        md_lines.append(f'\n**Correct Answer**: {ans}\n')
    else:
        md_lines.append(f'\n**Correct Answer**: -')
        md_lines.append(f'**Explanation**: {exp}\n')
    md_lines.append('---\n')

with open('Markdown_Questions/48_anatomy_department.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f'Wrote {len(qs_data)} clean questions to Markdown_Questions/48_anatomy_department.md!')
