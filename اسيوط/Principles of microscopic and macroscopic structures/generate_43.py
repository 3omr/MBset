questions_43 = []

# Section A: 10 Short Essay Questions
essay_items = [
    ("Define anatomical and functional end arteries.",
     "1. Anatomical end arteries: Arteries that have no anastomoses with neighboring arteries; complete occlusion results in ischemic infarction and tissue necrosis (e.g. central artery of retina, splenic artery).\n2. Functional end arteries: Arteries that possess potential micro-anastomoses with neighboring arteries, but these anastomoses are anatomically insufficient to maintain tissue viability upon sudden occlusion (e.g. coronary arteries, renal arteries)."),
    ("Define spermatogenesis.",
     "Spermatogenesis is the sequence of cellular events by which primitive male germ cells (spermatogonia) undergo mitotic proliferation and meiotic divisions to produce mature haploid motile spermatozoa in the seminiferous tubules of the testes."),
    ("Enumerate the three phases of fertilization.",
     "1. Phase 1: Penetration of the corona radiata\n2. Phase 2: Penetration of the zona pellucida (acrosomal reaction)\n3. Phase 3: Fusion of the oocyte and sperm cell membranes (cortical reaction and resumption of second meiotic division)."),
    ("Define gastrulation.",
     "Gastrulation is the fundamental morphogenetic process that establishes all three primary germ layers (ectoderm, intraembryonic mesoderm, and endoderm), transforming the bilaminar embryonic disc into a trilaminar embryonic disc."),
    ("Mention the cellular changes that occur in the endometrium during the decidual reaction.",
     "1. Endometrial stromal cells enlarge, become rounded/polyhedral, and accumulate abundant glycogen and lipid droplets (decidual cells).\n2. Endometrial stroma becomes highly vascular and edematous, prepared for blastocyst invasion and placental nourishment."),
    ("Mention three histological differences between cytotrophoblast and syncytiotrophoblast.",
     "1. Cytotrophoblast forms the inner cellular layer; syncytiotrophoblast forms the outer invasive layer.\n2. Cytotrophoblast cells are mononucleated with distinct cell membranes and undergo active mitotic divisions; syncytiotrophoblast is a multinucleated protoplasmic mass devoid of distinct cell boundaries and shows no mitotic figures (grows by fusion of underlying cytotrophoblasts)."),
    ("Enumerate two sources of amniotic fluid.",
     "1. Amnioblasts (cells of the amniotic membrane)\n2. Fetal urine (via embryo/fetal kidneys entering amniotic cavity in later pregnancy)\n3. Transudation of fluid across fetal capillaries from the placenta and umbilical cord."),
    ("Enumerate four types of intermediate filaments.",
     "1. Keratins (cytokeratins) in epithelial cells\n2. Vimentin in mesenchymal and connective tissue cells\n3. Desmin in muscle cells\n4. Neurofilaments in neurons\n5. Glial fibrillary acidic protein (GFAP) in glial cells\n6. Lamins (nuclear lamins) in the nuclear lamina."),
    ("Mention the key histological features and mechanism of apoptosis.",
     "Apoptosis is programmed, gene-directed physiological cell death characterized by:\n1. Cellular shrinkage without swelling; cell volume decreases while organelles remain structurally intact.\n2. Condensation and margination of nuclear chromatin followed by DNA fragmentation by endogenous endonucleases.\n3. Progressive cell membrane blebbing forming membrane-bound apoptotic bodies.\n4. Phagocytosis of apoptotic bodies by resident macrophages or adjacent epithelial cells without provoking an inflammatory reaction."),
    ("Define the basement membrane.",
     "The basement membrane is a thin, specialized extracellular sheet of macromolecules situated between the basal surface of epithelial cells and the underlying connective tissue stroma, composed of the basal lamina (secreted by epithelial cells) and the reticular lamina (secreted by connective tissue fibroblasts).")
]

for stem, exp in essay_items:
    questions_43.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

# Section B: 12 Complete Questions
complete_items = [
    ("Degeneration of ovarian follicles before reaching maturity is called follicular ……….", "Atresia (Corpus atreticum)"),
    ("The hormone responsible for the growth and maturation of ovarian follicles during the follicular phase is ……….", "FSH (Follicle-Stimulating Hormone)"),
    ("Following fertilization, cleavage divisions produce a solid ball of 16 blastomeres called the ……….", "Morula"),
    ("The blastocyst typically reaches the uterine cavity at approximately the ………. day after fertilization.", "5th day"),
    ("Gastrulation begins with the appearance of the primitive streak at the beginning of the ………. week of development.", "3rd week"),
    ("The fetal component of the placenta is formed by the chorion ………., while the smooth non-villous portion is the chorion ………..", "Chorion frondosum; Chorion laeve"),
    ("Steroid-secreting cells and drug-metabolizing liver cells are richly endowed with ………. endoplasmic reticulum.", "Smooth (SER)"),
    ("The golden-brown, iron-containing endogenous pigment resulting from hemoglobin breakdown in macrophages is ………..", "Haemosiderin"),
    ("Branched contractile cells located between the basal lamina and secretory cells of glands are ………. cells.", "Myoepithelial"),
    ("The antibody-producing cells derived from activated B lymphocytes with a clock-face eccentric nucleus are ………. cells.", "Plasma"),
    ("The principal cell responsible for synthesizing collagen, elastic fibers, and ground substance in connective tissue is the ………..", "Fibroblast"),
    ("Histochemical demonstration of tissue enzymes and lipids requires ………. sections rather than routine paraffin embedding.", "Frozen (Cryostat)")
]

for stem, exp in complete_items:
    questions_43.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

# Section C: 17 MCQs
mcqs_43 = [
    ("Regarding the small intestine, choose the CORRECT statement:",
     ["It is 4 meters long", "Has taeniae coli in its wall", "Includes the duodenum in which the common bile duct opens", "The anal canal forms its terminal part"], "C"),
    ("Movement of a limb away from the median plane of the body is termed:",
     ["Abduction", "Circumduction", "Extension", "Pronation"], "A"),
    ("A suture joint of the skull is classified as a:",
     ["Fibrous joint", "Primary cartilaginous joint", "Secondary cartilaginous joint", "Synovial joint"], "A"),
    ("A vertical plane that divides the human body into anterior and posterior parts is the:",
     ["Coronal plane", "Median plane", "Transverse plane", "Sagittal plane"], "A"),
    ("All the following structures are skin appendages EXCEPT:",
     ["Thymus gland", "Sweat gland", "Sebaceous gland", "Nails"], "A"),
    ("The superficial fascia may contain all of the following structures EXCEPT:",
     ["Subcutaneous fat", "Cutaneous blood and lymphatic vessels", "Cutaneous nerves and facial muscles", "Tendons of deep skeletal muscles"], "D"),
    ("The ovulated mammalian secondary oocyte is arrested at:",
     ["Prophase of meiosis I", "Metaphase of meiosis I", "Prophase of meiosis II", "Metaphase of meiosis II"], "D"),
    ("Ovulation occurs in direct response to a mid-cycle surge of which hormone?",
     ["FSH", "LH (Luteinizing Hormone)", "Progesterone", "Estrogen"], "B"),
    ("The early stages of embryonic cleavage divisions are characterized by:",
     ["Formation of a hollow ball of cells", "Formation of the zona pellucida", "Increase in the size of the whole zygote", "Increase in the number of cells within the unchanging zygote volume"], "D"),
    ("Under the light microscope, the zona pellucida appears as a translucent glycoprotein membrane surrounding the:",
     ["Primary oocyte", "Morula", "Very early blastocyst", "All of the above"], "D"),
    ("The primitive streak first appears on the dorsal surface of the epiblast at the beginning of the:",
     ["First week", "Second week", "Third week", "Fourth week"], "C"),
    ("During the second month of development (embryonic period), the external appearance of the embryo changes due to:",
     ["Significant increase in head size", "Formation and outgrowth of upper and lower limbs", "Development of the face, ears, nose, and eyes", "All of the above"], "D"),
    ("Which of the following structures produces the majority of progesterone late in human pregnancy?",
     ["Corpus luteum of ovary", "Syncytiotrophoblast of the placenta", "Fetal adenohypophysis", "Maternal liver"], "B"),
    ("Persistence of the proximal intra-abdominal portion of the vitelline (omphalomesenteric) duct results in:",
     ["Umbilical cord hernia", "Meckel's diverticulum", "Vitelline cyst", "Patent vitelline fistula"], "B"),
    ("Chorionic villi are designated as secondary chorionic villi when they:",
     ["Directly contact the decidua basalis", "Are covered exclusively by syncytiotrophoblast", "Develop an internal mesenchymal connective tissue core", "Give rise to anchoring branch villi"], "C"),
    ("Monozygotic (identical) twins:",
     ["Sometimes share a single common chorionic cavity", "Are covered only by cytotrophoblast", "Always have separate unconnected placentas", "Always arise from two separate morulae"], "A"),
    ("Which of the following cellular organelles can be demonstrated histochemically by staining for acid phosphatase and hydrolytic enzymes?",
     ["Golgi bodies", "Smooth endoplasmic reticulum", "Rough endoplasmic reticulum", "Lysosomes"], "D")
]

for stem, opts, ans in mcqs_43:
    questions_43.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# Section D: 9 True or False
tf_43 = [
    ("The pectoral (shoulder) girdle is formed of the clavicle anteriorly and the scapula posteriorly.", "True"),
    ("The filum terminale is a prolongation of the dura mater attached to the front of the coccyx.", "False (It is a prolongation of the pia mater)"),
    ("The functional unit of the human kidney is the nephron.", "True"),
    ("The trachea extends from the level of the sixth cervical vertebra (C6) to the lower border of the fourth / upper border of fifth thoracic vertebra (T4/T5).", "True"),
    ("Neural tube defects result from failure of normal closure of the embryonic neural tube.", "True"),
    ("The total number of somite pairs formed in human embryogenesis is 32-34 pairs.", "False (42 to 44 pairs of somites are formed)"),
    ("Neural crest cells give rise to the cortex of the suprarenal (adrenal) gland.", "False (They give rise to the adrenal medulla; the cortex arises from coelomic mesoderm)"),
    ("The human fetus is covered by fine downy lanugo hair starting in the second trimester.", "True"),
    ("A urachal sinus represents the persistence of the embryonic allantois throughout its entire length.", "False (Complete persistence is patent urachus; urachal sinus is persistence of only the umbilical end)")
]

for stem, ans in tf_43:
    questions_43.append({
        'type': 'QROC',
        'stem': f"State whether True or False: {stem}",
        'exp': ans,
        'correct': '-',
        'opts': []
    })

print(f"Total questions for 43: {len(questions_43)}")

md_blocks = []
for i, q in enumerate(questions_43, 1):
    q_str = f"### Question {i}\n\n{q['stem']}\n\n"
    if q['type'] == 'QCS':
        for j, opt in enumerate(q['opts']):
            letter = chr(ord('A') + j)
            q_str += f"- **{letter})** {opt}\n"
        q_str += f"\n**Correct Answer**: {q['correct']}\n"
    else:
        q_str += f"**Correct Answer**: -\n**Explanation**: {q['exp']}\n"
    md_blocks.append(q_str)

header_43 = f"""# anatomy Qs bank.pdf

- **Source File**: `anatomy Qs bank.pdf`
- **File Type**: Text PDF
- **Total Pages / Slides**: 7
- **Assiut Tag**: Department, QBank, Anatomy
- **Discipline**: Anatomy
- **Total Questions**: {len(questions_43)}

---

"""

with open('Markdown_Questions/43_anatomy_Qs_bank.md', 'w') as f:
    f.write(header_43 + '\n---\n\n'.join(md_blocks) + '\n')

print("43_anatomy_Qs_bank.md written successfully!")
