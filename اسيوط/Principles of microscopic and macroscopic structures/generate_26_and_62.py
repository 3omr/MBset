import re

# We will build the verified list of questions for 26 & 62
questions = []

# P1: 22 Complete questions
p1_items = [
    ("The ……… acts as a packing and processing center in the cell to process proteins.", "Golgi apparatus"),
    ("…….. is an organelle that functions independently in eukaryotic cell.", "Mitochondria"),
    ("…….. is the most common GAG of connective tissue matrix.", "Hyaluronic acid"),
    ("In the wall of large arteries, elastin occurs as ……. sheets.", "Fenestrated"),
    ("Cartilage contains collagen type …….", "Type II collagen"),
    ("Collagen type …..... links fibrillar collagens to one another in the basement membrane.", "Type VII collagen"),
    ("……….. are the tubular folds of the inner membrane of mitochondria.", "Cristae"),
    ("Reticular fibers stain …… after impregnation with silver salts.", "Black"),
    ("Connective tissue proper is classified according to the amount and arrangement of …… fibres.", "Collagen"),
    ("…….. is a fixed connective tissue cell.", "Fibroblast"),
    ("A large phagocytic connective tissue cell is called ……", "Macrophage (Histiocyte)"),
    ("………. granules can be expected to be present in large numbers in non-dividing cells or cells with a long lifespan.", "Lipofuscin"),
    ("Cytoplasmic pigments are classified as either ………… or ………..", "Endogenous or exogenous"),
    ("With the E.M., ………. appears in the form of electron-dense granules with irregular outline usually associated with SER.", "Glycogen (or Ribosomes)"),
    ("With L.M., in specimens stained with H&E, ...… appear with a signet-ring appearance.", "Fat cell (Adipocyte)"),
    ("Multiple small …….. are found in the cytoplasm of steroid-secreting endocrine cells.", "Lipid droplets"),
    ("…………. is a fat-soluble exogenous pigment which gives adipose tissue its characteristic yellowish color and is converted into vitamin A in the skin.", "Carotene"),
    ("……….. is the loose connective tissue that underlies the epithelial lining of the digestive system.", "Lamina propria"),
    ("The outer layer of the nuclear envelope is continuous with the membrane of the ……. .", "Rough Endoplasmic Reticulum (RER)"),
    ("The structure that produces the initial organization of free double-stranded DNA into chromatin is the ………. .", "Nucleosome"),
    ("………… is the type of endocytosis which means the ingestion of large solid particles into the cell.", "Phagocytosis"),
    ("Lysosomes are considered the digestive apparatus of the cell because they are rich in ……… enzymes.", "Acid hydrolytic (hydrolases)")
]

for stem, ans in p1_items:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

# P2: 10 MCQs
p2_mcqs = [
    ("Epithelial cells that are adapted for absorption or secretion usually have …… at their free surface.",
     ["junctional complexes", "nuclei", "microvilli", "Golgi complexes"], "C"),
    ("A group of cells with similar structure and function is defined as a:",
     ["Organ system", "Organ", "Tissue", "Blood"], "C"),
    ("Which of the following is responsible for the production of lipofuscin pigment?",
     ["Ribosomes", "Lysosomes", "Microbodies (Peroxisomes)", "Mitochondria"], "B"),
    ("A eukaryotic cell is one which has:",
     ["A well defined nucleus with nuclear envelope", "A limiting plasma membrane only", "No definite nuclear membrane", "No membranous organelles"], "A"),
    ("Which of the following is a characteristic function of a tight junction (zonula occludens)?",
     ["Forms connection between desmosomes", "Stabilizes intermediate filaments", "Allows passage of ions and small molecules between adjacent cells", "Prevents the passage of material through the intercellular spaces"], "D"),
    ("……… are stains that enter cells either by diffusion or phagocytosis and stain cellular components without harming the living cell:",
     ["General histological stains", "Special histological stains", "Vital stains", "Histochemical and cytochemical methods"], "C"),
    ("Intercellular ionic and metabolic exchange is achieved by:",
     ["Nexus (gap junction)", "Zonula adherens", "Macula adherens (desmosome)", "Zonula occludens"], "A"),
    ("Rough endoplasmic reticulum:",
     ["Synthesizes proteins for export and membranes", "Is acidophilic", "Controls pigment migration", "Synthesizes lipids and steroids"], "A"),
    ("The organelle that contains enzymes concerned with the oxidation of food and ATP production is:",
     ["Golgi complex", "Lysosome", "Mitochondria", "RER"], "C"),
    ("The main function of lysosomes is:",
     ["Detoxification of drugs", "Converting H2O2 into water & O2", "Packaging of secretory proteins", "Intracellular digestion of materials entering the cell"], "D")
]

for stem, opts, ans in p2_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P3: 11 MCQs
p3_mcqs = [
    ("Which one of the following statements about the desmosome (macula adherens) is TRUE?",
     ["It is sometimes called a nexus", "It permits the passage of large proteins from one cell to an adjacent cell", "It facilitates electric coupling between adjacent cells", "It is connected to intermediate filaments (tonofilaments)"], "D"),
    ("Glycogen can be specifically demonstrated in cells by:",
     ["Its own natural color", "PAS (Periodic acid-Schiff) method", "Colouring with Sudan III/Sudan black", "The haematin test"], "B"),
    ("Wear and tear pigment (lipofuscin) is characterized by:",
     ["Membrane-bound yellowish-brown granules", "Residual bodies of lysosomal activity", "Endogenous pigment that increases with age", "All of the above"], "D"),
    ("The following is NOT a cytoplasmic inclusion:",
     ["Glycogen granules", "Melanin pigment", "Carotenoids", "Secretory vesicles"], "D"),
    ("The following is a pigment resulting from the breakdown of hemoglobin:",
     ["Myoglobin", "Haemosiderin", "Lipofuscin", "Melanin"], "B"),
    ("Microfilaments are composed mainly of a protein called:",
     ["Actin", "Tubulin", "Myosin", "Keratin"], "A"),
    ("Which of the following is NOT composed of intermediate filaments?",
     ["Centrioles (composed of microtubules)", "Desmin filaments", "Glial fibrillary filaments", "Keratin filaments"], "A"),
    ("All of the following structures are formed of microtubules EXCEPT:",
     ["Cilia", "Centrioles", "Mitotic spindle", "Microvilli (formed of actin microfilaments)"], "D"),
    ("Free polyribosomes (polysomes) are mainly concerned with:",
     ["Formation of steroids", "Synthesis of cytoplasmic/structural proteins", "Conduction of materials in cytoplasm", "Synthesis of secretory proteins for export"], "B"),
    ("The cell membrane (plasma membrane) thickness measures approximately:",
     ["1 - 5 nm", "7.5 - 10 nm", "25 - 30 nm", "50 - 100 nm"], "B"),
    ("A peripheral membrane protein is:",
     ["Deeply embedded across the lipid bilayer", "Loosely associated with one of the two membrane surfaces", "Composed strictly of cholesterol", "Found exclusively on the outer carbohydrate coat"], "B")
]

for stem, opts, ans in p3_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P4: MCQs & Enumerate
p4_mcqs = [
    ("Smooth endoplasmic reticulum:",
     ["Synthesizes proteins", "Is acidophilic", "Contains ribosomes on its surface", "Is intensely basophilic"], "B"),
    ("The Golgi apparatus is formed of:",
     ["Cisternae of smooth membrane only", "Cisternae, transfer vesicles, and secretory vesicles", "Tubules of rough membrane", "Centriolar triplets"], "B"),
    ("The inner membrane of mitochondria differs from the outer membrane in:",
     ["Containing more carbohydrates", "Containing more ribosomes", "Containing less integral proteins", "Being thrown into shelf-like folds called cristae"], "D"),
    ("Melanin pigments are classified as:",
     ["Endogenous inclusions", "Exogenous organelles", "Endogenous organelles", "Stored nutrient food"], "A")
]

for stem, opts, ans in p4_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

p4_enum = [
    ("Enumerate the types of non-membranous organelles in animal cells.",
     "1. Ribosomes (free and attached)\n2. Centrosome / Centrioles\n3. Microtubules\n4. Cytoskeletal filaments (Microfilaments, Intermediate filaments)"),
    ("Enumerate the types of intercellular junctions.",
     "1. Occluding junctions (Zonula occludens / Tight junction)\n2. Anchoring junctions (Zonula adherens, Desmosome / Macula adherens, Hemidesmosome)\n3. Communicating junctions (Gap junction / Nexus)"),
    ("Mention the main functions of plasma membrane proteins.",
     "1. Structural proteins\n2. Channel and transport proteins (pumps)\n3. Receptor proteins for signaling\n4. Cell-to-cell adhesion molecules (linkers)\n5. Membrane-bound enzymes"),
    ("Enumerate the types of mature lamellated bone.",
     "1. Compact (cortical) bone\n2. Spongy (cancellous or trabecular) bone"),
    ("Enumerate the main classes of cytoplasmic inclusions.",
     "1. Stored foods (Glycogen granules, Lipid droplets)\n2. Pigments (Endogenous e.g. melanin, lipofuscin, haemosiderin; Exogenous e.g. carotene, dust/carbon)\n3. Crystals"),
    ("Mention the two methods of bone formation (osteogenesis).",
     "1. Intramembranous ossification (directly within mesenchymal sheets)\n2. Endochondral (intracartilaginous) ossification (on a pre-existing hyaline cartilage model)"),
    ("Enumerate four essential characteristics of stem cells.",
     "1. Undifferentiated primitive cells\n2. Prolonged self-renewal capacity (asymmetric replication)\n3. Multipotency / pluripotency (ability to differentiate into specialized cell lineages)\n4. Ability to regenerate and repair damaged tissues"),
    ("Mention two primary functions of the basement membrane.",
     "1. Structural attachment and mechanical support for epithelial cells to underlying connective tissue\n2. Selective macromolecular filtration and diffusion barrier")
]

for stem, exp in p4_enum:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

# P5: MCQs
p5_mcqs = [
    ("Colour of the iris of the eye is primarily due to the presence of:",
     ["Hemoglobin", "Lipofuscin", "Melanin", "Carotene"], "C"),
    ("The common stored form of glucose in animal cells is:",
     ["Glycogen", "Starch", "Cellulose", "Amylose"], "A"),
    ("The following is NOT a cytoplasmic inclusion:",
     ["Carbohydrate granules", "Melanin granules", "Carotenoids", "Secretory vesicles"], "D"),
    ("Lipid/fat droplets can be demonstrated in histological sections by:",
     ["The PAS method", "Colouring with Sudan (Sudan III / Sudan black)", "Staining with orcein", "Its own natural yellow color"], "B"),
    ("The following is a breakdown pigment derived from hemoglobin in tissue macrophages:",
     ["Myoglobin", "Haemosiderin", "Lipofuscin", "Carotene"], "B"),
    ("The pigment that serves as an indicator of cellular wear and tear and increases in amount with age is:",
     ["Melanin", "Lipofuscin", "Hemoglobin", "Carotene"], "B")
]

for stem, opts, ans in p5_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P6: MCQs & Enumerate
p6_mcqs = [
    ("Which of the following cellular organelles is responsible for the production of lipofuscin granules?",
     ["Ribosomes", "Lysosomes (as residual bodies)", "Microbodies", "Mitochondria"], "B"),
    ("The following is NOT a characteristic feature of cytoplasmic inclusions:",
     ["Have little or no metabolic activity", "Actively involved in mitotic cell division", "Are usually transitory cytoplasmic components", "May or may not be enclosed by a membrane"], "B")
]

for stem, opts, ans in p6_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

p6_enum = [
    ("Enumerate the phases of the eukaryotic cell cycle.",
     "1. G1 phase (Gap 1)\n2. S phase (DNA Synthesis)\n3. G2 phase (Gap 2)\n4. M phase (Mitosis: Prophase, Metaphase, Anaphase, Telophase) and Cytokinesis"),
    ("Enumerate the stages of Interphase in the cell cycle.",
     "1. G1 phase (Pre-synthetic growth phase)\n2. S phase (DNA synthesis and centriole replication)\n3. G2 phase (Post-synthetic preparation for mitosis)"),
    ("Enumerate four major cellular changes that occur during necrosis.",
     "1. Cellular swelling (hydropic degeneration)\n2. Loss of plasma membrane integrity and rupture\n3. Lysis and destruction of organelles\n4. Nuclear breakdown (Pyknosis, Karyorrhexis, Karyolysis) provoking severe inflammatory reaction"),
    ("Enumerate four major cellular features that characterize apoptosis.",
     "1. Cell shrinkage and rounded cell contour\n2. Nuclear chromatin condensation and margination\n3. Cell membrane blebbing and formation of apoptotic bodies\n4. Intact cellular organelles and phagocytosis without an inflammatory response")
]

for stem, exp in p6_enum:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

# P7: MCQs
p7_mcqs = [
    ("Chromosome (DNA) replication occurs during which phase of the cell cycle?",
     ["Metaphase", "S-phase", "Anaphase", "G2-phase"], "B"),
    ("The irreversible cessation of vital cellular activities is defined as:",
     ["Cell death", "Cell growth", "Cell differentiation", "Cell cycle"], "A"),
    ("The centromere does not divide until the end of metaphase. This is important because the centromere:",
     ["Is connected with nuclear envelope", "Produces spindle fibres", "Contains genes that control prophase and metaphase", "Holds the replicated sister chromatids together"], "D"),
    ("Cell death in which the cell swells, chromatin clumps irregularly, the cytoplasm becomes weakly stained, and organelles are destroyed is:",
     ["Apoptosis", "Necrosis", "Autophagy", "Senescence"], "B"),
    ("Integral membrane proteins:",
     ["Are peripheral only", "Extend across the entire lipid bilayer (transmembrane proteins)", "Are completely soluble proteins in cytoplasm", "Lack hydrophobic amino acids"], "B")
]

for stem, opts, ans in p7_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P8: Complete questions
p8_items = [
    ("……….. is the longest part of the complete cell cycle (during which DNA replicates, centrioles duplicate, and proteins are actively produced) between two mitoses.", "Interphase"),
    ("……….. is the non-membranous organelle found in animal cells to which spindle fibers attach and organize during cell division.", "Centrosome (Centrioles)"),
    ("……….. (Progressive specialization) is the developmental process by which cells achieve new morphological features and specialized functions.", "Cell differentiation"),
    ("………… is the mitotic stage when chromosomes shorten, align at the equatorial plate, and then separate into two identical sets.", "Metaphase"),
    ("………… are surveillance mechanisms present in each phase of the cell cycle where the quality and completion of cell cycle events are monitored.", "Checkpoints"),
    ("Cell death means 'the ………. cessation of vital activities inside the cell'.", "Irreversible"),
    ("The epithelium that is highly specialized in secretion is called ………. epithelium.", "Glandular")
]

for stem, ans in p8_items:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

# P9: MCQs
p9_mcqs = [
    ("What is the role of stem cells with regard to the function of adult tissues and organs?",
     ["Stem cells are undifferentiated cells that divide asymmetrically, giving rise to one daughter that remains a stem cell and one daughter that differentiates to replace worn out cells",
      "Stem cells are fully differentiated cells that can divide when needed for organ growth",
      "Stem cells reside strictly under the epithelial surface to take over the function when overlying cells die",
      "Stem cells secrete the extracellular matrix of all organs"], "A"),
    ("Adult stem cells residing in mature tissues are usually:",
     ["Totipotent", "Pluripotent", "Multipotent", "Incapable of replication"], "C")
]

for stem, opts, ans in p9_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P10: Written & MCQs
p10_items = [
    ("………. is a type of modified epithelium formed of branched cells with multiple processes containing contractile elements (actin and myosin) located around acini.", "Myoepithelial cells (Myoepithelium)"),
    ("Match cell types with their renewal rate: (1) Cells of skin, blood and gut epithelium; (2) Cells of connective tissue; (3) Cells of nervous tissue and cardiac muscle.",
     "(1) Cells of skin, blood and gut: Renew rapidly (labile cells)\n(2) Cells of connective tissue: Renew slowly (stable cells)\n(3) Cells of nervous tissue and cardiac muscle: Never renew (permanent cells)")
]

for stem, ans in p10_items:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

p10_mcqs = [
    ("Barr body (sex chromatin):",
     ["Represents one of the active Y chromosomes", "Represents transcriptionally active euchromatin", "Is frequently detected in normal male nuclei", "Represents an inactivated condensed X-chromosome attached to the nuclear envelope in females"], "D"),
    ("Chromatin is chemically composed of:",
     ["DNA and histone proteins", "RNA and DNA only", "Messenger RNA and lipid", "Polysaccharides and DNA"], "A"),
    ("The post-mitotic growth phase of the cell cycle is designated as:",
     ["G1 phase", "S phase", "G2 phase", "G0 phase"], "A")
]

for stem, opts, ans in p10_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P11: MCQs
p11_mcqs = [
    ("A lysosome differs biochemically from a microbody (peroxisome) in:",
     ["Containing catalase and urate oxidase", "Containing acid hydrolases", "Being bounded by a double membrane", "Lacking enzymatic activity"], "B"),
    ("Reticular fibers are characterized by:",
     ["Forming large thick unbranched bundles", "Being acidophilic with H&E stain", "Staining intensely black by silver impregnation (argyrophilic)", "Being composed of Type I collagen"], "C"),
    ("The basal surface of epithelial cells adheres directly to:",
     ["Basement membrane (Basal lamina)", "Reticular layer of dermis", "Hypodermis", "Perichondrium"], "A"),
    ("The primary histological function of apical microvilli is to:",
     ["Move secretions along epithelial surfaces", "Increase the absorptive surface area of the cell", "Act as sensory mechanoreceptors", "Form intercellular occluding barriers"], "B")
]

for stem, opts, ans in p11_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P12: MCQs
p12_mcqs = [
    ("Elementary particles (ATP synthase complexes) are located on the:",
     ["Outer mitochondrial membrane", "Inner surface of the inner mitochondrial membrane (facing the matrix)", "Outer surface of the rough endoplasmic reticulum", "Limiting membrane of lysosomes"], "B"),
    ("The greatest attainable resolving power of a standard bright-field light microscope used in laboratory is approximately:",
     ["10 Angstrom", "0.2 micrometer (200 nm)", "0.1 nanometer", "2.0 micrometers"], "B"),
    ("The core structure of a motile cilium (axoneme) is formed of microtubules arranged as:",
     ["9 peripheral doublets and 2 central single microtubules (9+2 pattern)", "9 peripheral triplets with no central tubules (9+0 pattern)", "9 peripheral singlets and 1 central singlet", "Random bundles of microfilaments"], "A"),
    ("The organelle responsible for degradation of hydrogen peroxide (H2O2) via catalase is the:",
     ["Lysosome", "Peroxisome (Microbody)", "Golgi complex", "Centrosome"], "B")
]

for stem, opts, ans in p12_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P13: MCQs
p13_mcqs = [
    ("Ribosomal RNA transcription and ribosome subunit assembly are associated with which structure?",
     ["Rough endoplasmic reticulum", "Golgi apparatus", "Smooth endoplasmic reticulum", "Nucleolus"], "D"),
    ("Which of the following statements is INCORRECT regarding the smooth endoplasmic reticulum (SER)?",
     ["Involved in detoxification of drugs and toxins in hepatocytes", "Abundant in steroid-producing endocrine cells", "Forms the sarcoplasmic reticulum in striated muscle fibers", "Directly responsible for the synthesis and export of secretory proteins"], "D"),
    ("Desmin intermediate filaments are characteristically associated with:",
     ["Epithelial cells", "Endothelial cells", "Muscle cells (smooth, skeletal, and cardiac)", "Nerve axons"], "C"),
    ("All of the following statements regarding centrioles are correct EXCEPT:",
     ["Occur in orthogonal pairs inside the centrosome", "Duplicate prior to mitosis during S phase", "Are located within the centrosphere", "Are comprised of actin microfilaments (they are composed of 9 microtubule triplets!)"], "D"),
    ("Which one of the following statements about the desmosome (macula adherens) is TRUE?",
     ["It is sometimes called a nexus", "It permits passage of large proteins between adjacent cells", "It is an anchoring junction connected to tonofilaments via intracellular attachment plaques", "It facilitates direct metabolic coupling via connexons"], "C")
]

for stem, opts, ans in p13_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P14: MCQs & Enumerate
p14_mcqs = [
    ("Which one of the following statements about epithelial tissues is TRUE?",
     ["They exhibit distinct structural and functional polarity", "They are highly vascularized tissues", "They contain wide intercellular spaces filled with matrix", "They are never found lining blood vessels"], "A"),
    ("Which one of the following statements about exocrine glands is TRUE?",
     ["Exocrine glands lack excretory ducts", "Simple glands possess branched excretory ducts", "Endocrine glands secrete directly into ducts", "Serous secretions are watery and protein-rich"], "D")
]

for stem, opts, ans in p14_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

p14_enum = [
    ("Enumerate two anatomical sites where fibrocartilage is normally found in the human body.",
     "1. Intervertebral discs (annulus fibrosus)\n2. Pubic symphysis (also articular discs of TMJ and knee menisci)"),
    ("Enumerate two anatomical sites where elastic cartilage is found.",
     "1. Auricle (pinna) of the external ear\n2. Epiglottis (also external acoustic meatus and auditory tube)"),
    ("Enumerate four general functions of connective tissue proper.",
     "1. Structural support and binding of other tissues\n2. Physical and immune defense (macrophages, mast cells, plasma cells)\n3. Medium for nutrient diffusion, exchange of metabolites, and waste elimination\n4. Storage of fat and energy (adipose tissue)")
]

for stem, exp in p14_enum:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

# P15: Enumerate & True/False
p15_enum = [
    ("Enumerate three examples of endogenous cytoplasmic pigments.",
     "1. Melanin\n2. Lipofuscin\n3. Haemosiderin (or Bilirubin)"),
    ("Enumerate three essential functions of the smooth endoplasmic reticulum (SER).",
     "1. Synthesis of lipids, phospholipids, and steroid hormones\n2. Detoxification of potentially harmful drugs and metabolic wastes in the liver\n3. Storage and regulated release of calcium ions (sarcoplasmic reticulum in muscle)"),
    ("Enumerate the two primary types of cell death.",
     "1. Apoptosis (programmed physiological cell death)\n2. Necrosis (accidental/pathological cell death due to severe acute injury)")
]

for stem, exp in p15_enum:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': exp,
        'correct': '-',
        'opts': []
    })

p15_tf = [
    ("The outer nuclear membrane is continuous with the rough endoplasmic reticulum.", "True"),
    ("Hepatocytes typically contain a vesicular, spherical nucleus.", "True"),
    ("With EM and LM, cells rich in SER display intense cytoplasmic basophilia.", "False (Cells rich in SER are acidophilic/eosinophilic)"),
    ("Mitochondria have their own circular DNA and undergo self-replication by binary fission.", "True"),
    ("Peripheral membrane proteins are deeply incorporated into the hydrophobic lipid bilayer core.", "False (Integral proteins are embedded; peripheral proteins are loosely attached to surfaces)"),
    ("DNA replication occurs predominantly in the Gap 2 (G2) phase of the cell cycle.", "False (DNA replication occurs during S phase)"),
    ("The centrosome is composed of two perpendicularly oriented cylindrical rodlets called centrioles.", "True"),
    ("Gap junctions represent low-resistance regions of intercellular ionic and electrical coupling.", "True"),
    ("Eukaryotic cells are defined by possessing a membrane-bound nucleus containing their genome.", "True"),
    ("Pseudostratified columnar epithelium consists of multiple true anatomical layers of cells.", "False (All cells rest on the basement membrane, forming a single true cell layer)")
]

for stem, ans in p15_tf:
    questions.append({
        'type': 'QROC',
        'stem': f"State whether True or False: {stem}",
        'exp': ans,
        'correct': '-',
        'opts': []
    })

# P16: Matching & MCQs
p16_match = [
    ("Match each organelle/structure with its primary function:\n1. Mitochondria\n2. Free polysomes\n3. Smooth endoplasmic reticulum\n4. Lipofuscin pigment\n5. Lysosomes\n6. Apoptosis\n7. Golgi apparatus\n8. Microvilli\n9. Rough endoplasmic reticulum\n10. Cilia",
     "1. Mitochondria: Energy production (ATP synthesis via oxidative phosphorylation)\n2. Free polysomes: Formation of cytoplasmic/structural proteins\n3. Smooth endoplasmic reticulum: Lipid and steroid synthesis\n4. Lipofuscin pigment: Endogenous wear-and-tear pigment\n5. Lysosomes: Digestion of intracellular and foreign materials\n6. Apoptosis: Normal programmed cell death\n7. Golgi apparatus: Packaging, modification, and sorting of proteins\n8. Microvilli: Increase surface area for absorption\n9. Rough endoplasmic reticulum: Synthesis of proteins for export\n10. Cilia: Motility and transportation of fluids/particles")
]

for stem, ans in p16_match:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

p16_mcqs = [
    ("Which of the following cells is a true connective tissue cell?",
     ["Keratinocyte", "Fibroblast", "Parietal cell", "Langerhans cell"], "B"),
    ("Glycosaminoglycans (GAGs) are chemically composed of:",
     ["Simple globular proteins", "Polysaccharide chains formed of repeating disaccharide units", "Lipid-protein complexes", "Pure branched polypeptides"], "B")
]

for stem, opts, ans in p16_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P17: MCQs
p17_mcqs = [
    ("The cell grows in size and synthesizes enzymes and RNA during which phase of the cell cycle?",
     ["Interphase", "Prophase", "Metaphase", "Anaphase"], "A"),
    ("Steroid-forming endocrine cells are characteristically rich in:",
     ["Lipid droplets", "Smooth endoplasmic reticulum (SER)", "Abundant rough endoplasmic reticulum", "Both lipid droplets and SER"], "D"),
    ("Which of the following connective tissue cells synthesizes and secretes histamine and heparin?",
     ["Fibroblasts", "Neutrophils", "Monocytes", "Mast cells"], "D"),
    ("The most common and abundant cell type found in connective tissue proper is the:",
     ["Mast cell", "Macrophage", "Fibroblast", "Mesenchymal cell"], "C"),
    ("Which cells exhibit a classic 'signet-ring' appearance in routine H&E paraffin sections under LM?",
     ["Unilocular adipocytes (white fat cells)", "Macrophages", "Plasma cells", "Mesenchymal cells"], "A"),
    ("All of the following cell populations are rapidly renewing (labile) cells EXCEPT:",
     ["Smooth muscle cells", "Hematopoietic blood cells", "Epidermal skin cells", "Epithelium lining the gastrointestinal tract"], "A"),
    ("Euchromatin represents the portion of nuclear chromatin that is:",
     ["Transcriptionally inactive and condensed", "The inactive Barr body", "Dense and deeply basophilic", "Transcriptionally active and dispersed"], "D"),
    ("Which of the following organelles is surrounded by a limiting unit membrane?",
     ["Lysosome", "Ribosome", "Centrosome", "Microtubule"], "A")
]

for stem, opts, ans in p17_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P18: MCQs
p18_mcqs = [
    ("Regarding adult stem cells, all of the following statements are true EXCEPT:",
     ["They are isolated from the inner cell mass of the blastocyst (that is embryonic stem cells!)", "They can multiply to replenish dying cells", "They can regenerate damaged tissues", "They are found throughout the body in adult tissues"], "A"),
    ("The nucleolus is characteristically:",
     ["Bounded by a unit membrane", "Intensely basophilic due to high rRNA content", "Not essential for protein synthesis", "Acidophilic with H&E"], "B"),
    ("Regarding the Golgi apparatus, all of the following statements are true EXCEPT:",
     ["It appears as a negative Golgi image with H&E staining in plasma cells", "It is formed of flattened cisternae and vesicular transport vesicles", "Secretory condensing vesicles are larger than transfer vesicles", "It is the primary site of cellular aerobic respiration"], "D"),
    ("A non-membranous organelle that plays an essential role in spindle formation during cell division is the:",
     ["Mitochondrion", "Ribosome", "Lysosome", "Centriole"], "D"),
    ("All of the following are true regarding the Gap 1 (G1) phase of the cell cycle EXCEPT:",
     ["It occurs between mitosis and the initiation of DNA replication", "The nucleus does not exhibit an increase in DNA content", "Chromosomes are formed of two sister chromatids (double chromatids form after S phase!)", "It is a period of active RNA and protein synthesis"], "C"),
    ("Integral membrane proteins:",
     ["May occupy part of the cell membrane thickness", "Can extend completely across the membrane (transmembrane)", "Are loosely attached to the cytosolic surface only", "Both a and b are correct"], "D"),
    ("The total amount of DNA in a somatic cell at the Gap 2 (G2) phase is:",
     ["Similar to that at G1 phase", "Double that at S phase", "Double that at G1 phase (4C vs 2C)", "Half that at G1 phase"], "C")
]

for stem, opts, ans in p18_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P19: MCQs
p19_mcqs = [
    ("Which of the following is a characteristic function of a tight junction (zonula occludens)?",
     ["Forms mechanical anchors between desmosomes", "Stabilizes intermediate filaments", "Allows passage of ions and metabolites between cells", "Prevents the passage of materials through the intercellular space"], "D"),
    ("Regarding the plasma membrane, all of the following statements are true EXCEPT:",
     ["It cannot be visualized as a distinct bilayer with the light microscope", "With the transmission EM, it displays a classic trilaminar appearance", "It is organized according to the fluid mosaic model", "Its dry weight is composed of 20% protein, 5% lipid and 75% carbohydrate (proteins comprise ~50-60%!)"], "D"),
    ("Which of the following organelles is responsible for the formation of lipofuscin pigment granules?",
     ["Ribosomes", "Lysosomes (residual bodies)", "Peroxisomes", "Mitochondria"], "B"),
    ("Melanin granules in melanocytes and keratinocytes are classified as:",
     ["Endogenous inclusions", "Exogenous organelles", "Membranous organelles", "Stored energetic nutrients"], "A"),
    ("Microtubules are structural components of all the following EXCEPT:",
     ["Cilia", "Centrioles", "Mitotic spindle", "Microvilli"], "D"),
    ("Which nuclear structure is directly responsible for ribosomal RNA transcription and ribosomal subunit assembly?",
     ["Nuclear lamina", "Nuclear envelope", "Nucleolus", "Nuclear pore complex"], "C")
]

for stem, opts, ans in p19_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P20: MCQs & Complete
p20_mcqs = [
    ("The basement membrane serves which of the following essential functions?",
     ["Acts as a selective diffusion and filtration barrier", "Provides structural support for the overlying epithelium", "Anchors epithelial layers securely to underlying connective tissue", "All of the above"], "D"),
    ("Structural and functional cellular polarity is a characteristic feature found in:",
     ["Simple epithelium", "Stratified epithelium", "Pseudostratified epithelium", "All of the above"], "D"),
    ("The basement membrane can be specially demonstrated under light microscopy using:",
     ["Orcein stain", "Periodic acid-Schiff (PAS) reaction", "Silver impregnation stain", "Both PAS and silver stains"], "D"),
    ("Following the completion of normal mitosis, the number of chromosomes in each daughter cell is:",
     ["One fourth of parent cell", "One half of parent cell", "Double the parent cell", "The exact same diploid number as the parent cell (2n)"], "D")
]

for stem, opts, ans in p20_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

p20_items = [
    ("All components of the basal lamina (except fibronectin) are synthesized and secreted by the basal surface of ………. cells.", "Epithelial"),
    ("Components of the reticular lamina of the basement membrane are synthesized by cells of the underlying ………. tissue.", "Connective tissue (Fibroblasts)"),
    ("………. refers to the uneven distribution of organelles, proteins, and membrane domains between the apical and basal poles of epithelial cells.", "Cell polarity"),
    ("With the electron microscope, the basement membrane is demonstrated to consist of two parts: the basal lamina and the ………. lamina.", "Reticular"),
    ("The cilia present in the respiratory trachea are of the ……… type, while stereocilia in the epididymis are of the ……….. type.", "Motile; Immotile (absorptive microvilli)")
]

for stem, ans in p20_items:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

# P21: MCQs
p21_mcqs = [
    ("Which of the following statements is NOT true regarding the plasma membrane?",
     ["Fluid mosaic model of proteins and lipids", "Trilaminar unit membrane appearance under EM", "Freely permeable to all hydrophilic solutes and macromolecules", "Average thickness is approximately 7.5 to 10 nm"], "C"),
    ("Which of the following statements is TRUE regarding cartilage tissue?",
     ["It is classified into four distinct types", "It possesses an abundant intrinsic vascular network", "It has a mineralized rigid bone-like matrix", "It is a specialized form of supportive connective tissue"], "D"),
    ("The perichondrium covering cartilage is histologically composed of:",
     ["Yellow elastic connective tissue", "Loose areolar connective tissue", "Reticular connective tissue", "Dense irregular collagenous connective tissue"], "D"),
    ("The articular cartilage lining synovial joints:",
     ["Is formed of hyaline cartilage devoid of a perichondrium", "Is composed predominantly of dense elastic fibers", "Is covered by a thick fibrous perichondrium", "Receives direct arterial blood supply from the joint cavity"], "A"),
    ("A histological section in a tendon reveals all of the following features EXCEPT:",
     ["Minimal ground substance and packed parallel collagen bundles", "Abundant macrophages and mast cells (tendons contain primarily rows of inactive tenocytes!)", "Dense regular white fibrous connective tissue", "Parallel rows of flattened fibroblasts (tendon cells)"], "B"),
    ("Which of the following statements regarding proteoglycans in connective tissue matrix is CORRECT?",
     ["Stain intensely blue with silver impregnation", "Consist of a core protein to which GAG chains are covalently attached", "Possess intrinsic contractile properties similar to myosin", "Are synthesized exclusively by red blood cells"], "B"),
    ("Which of the following statements is TRUE regarding fibroblasts?",
     ["They are derived directly from mature endothelial cells", "They synthesize and secrete collagen, elastic, and reticular fibers as well as ground substance", "They are primarily fat-storing cells", "They line blood and lymphatic capillaries"], "B")
]

for stem, opts, ans in p21_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P22: MCQs
p22_mcqs = [
    ("Vital staining (e.g. Trypan blue injection) is used in vivo to specifically demonstrate which connective tissue cell?",
     ["Plasma cell", "Reticular cell", "Macrophage (Histiocyte)", "Mast cell"], "C"),
    ("Which of the following is EXCLUDED as a true connective tissue fiber?",
     ["Myosin filament (intracellular contractile protein)", "Reticular fiber", "Elastic fiber", "Collagen fiber"], "A"),
    ("A tendon is histologically classified as which type of connective tissue?",
     ["Dense regular collagenous connective tissue", "Dense irregular connective tissue", "Mucoid connective tissue", "Mesenchymal connective tissue"], "A"),
    ("Dense connective tissue proper is characterized by having:",
     ["Abundant, densely packed collagen bundles with relatively few cells", "Predominance of ground substance over fibers", "High density of blood capillaries with few fibers", "Absence of fibroblasts"], "A"),
    ("Which special histological stain is best suited to selectively demonstrate elastic fibers in connective tissue?",
     ["Orcein stain", "Routine H&E stain", "PAS stain", "Mucicarmine stain"], "A")
]

for stem, opts, ans in p22_mcqs:
    questions.append({
        'type': 'QCS',
        'stem': stem,
        'exp': None,
        'correct': ans,
        'opts': opts
    })

# P23: Complete questions
p23_items = [
    ("In the basement membrane, anchoring fibrils composed of collagen type ……… link the basal lamina to the underlying reticular lamina.", "Type VII collagen"),
    ("Reticular fibers stain characteristically ……… after silver impregnation.", "Black (Argyrophilic)"),
    ("Connective tissue proper is classified primarily according to the proportion and arrangement of ……… fibres.", "Collagen"),
    ("………. is the circulating granular leukocyte that migrates into tissues and secretes histamine and heparin.", "Basophil"),
    ("The eccentric nucleus of ……… is characterized by a distinctive 'clock-face' or 'cartwheel' chromatin pattern.", "Plasma cell")
]

for stem, ans in p23_items:
    questions.append({
        'type': 'QROC',
        'stem': stem,
        'exp': ans,
        'correct': '-',
        'opts': []
    })

print(f"Total reconstructed questions for 26 & 62: {len(questions)}")

# Now generate Markdown
md_blocks = []
for i, q in enumerate(questions, 1):
    q_str = f"### Question {i}\n\n{q['stem']}\n\n"
    if q['type'] == 'QCS':
        for j, opt in enumerate(q['opts']):
            letter = chr(ord('A') + j)
            q_str += f"- **{letter})** {opt}\n"
        q_str += f"\n**Correct Answer**: {q['correct']}\n"
    else:
        q_str += f"**Correct Answer**: -\n**Explanation**: {q['exp']}\n"
    md_blocks.append(q_str)

header_26 = """# Histology Bank Questions.pdf

- **Source File**: `Histology Bank Questions.pdf`
- **File Type**: Text PDF
- **Total Pages / Slides**: 23
- **Assiut Tag**: Department, QBank, Histology
- **Discipline**: Histology
- **Total Questions**: """ + str(len(questions)) + """

---

"""

header_62 = """# histology department.pdf

- **Source File**: `histology department.pdf`
- **File Type**: Text PDF
- **Total Pages / Slides**: 23
- **Assiut Tag**: Department, QBank, Histology
- **Discipline**: Histology
- **Total Questions**: """ + str(len(questions)) + """

---

"""

content_26 = header_26 + '\n---\n\n'.join(md_blocks) + '\n'
content_62 = header_62 + '\n---\n\n'.join(md_blocks) + '\n'

with open('Markdown_Questions/26_Histology_Bank_Questions.md', 'w') as f:
    f.write(content_26)

with open('Markdown_Questions/62_histology_department.md', 'w') as f:
    f.write(content_62)

print("Both 26 and 62 generated and saved successfully!")
