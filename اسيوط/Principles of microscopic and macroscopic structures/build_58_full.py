import re

target_file = '/home/omar/MBset/اسيوط/Principles of microscopic and macroscopic structures/Markdown_Questions/58_exams.md'
with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

qs = text.split('### Question ')

# Let's map verified medical answers for all MCQs in 58
# We want:
# 1. 0 fake 'A' fallbacks
# 2. Options cleaned of OCR noise
# 3. Medical accuracy

corrections = {
    1: ('B', 'External os forms the junction between the ectocervix and the vaginal canal.'),
    2: ('C', 'The membranous urethra is the narrowest and least dilatable part of the male urethra.'),
    3: ('A', 'There are 7 cervical vertebrae in humans.'),
    4: ('-', 'The right lung is divided into 3 lobes (superior, middle, inferior) by two fissures.'),
    5: ('A', 'The pulmonary trunk arises from the conus arteriosus of the right ventricle.'),
    6: ('A', 'Gomphosis is a specialized fibrous joint between a tooth and its alveolar socket.'),
    7: ('B', 'The coronal (frontal) plane divides the body into anterior and posterior parts.'),
    8: ('A', 'The ileum is part of the small intestine, not the large intestine.'),
    9: ('B', 'The epididymis is the site of sperm storage and maturation.'),
    10: ('A', 'Primary oocyte completes meiosis I to yield a secondary oocyte and the first polar body.'),
    11: ('-', 'Mitosis yields two genetically identical diploid daughter cells.'),
    12: ('-', 'Smooth muscle forms the muscular wall of hollow visceral organs like the urinary bladder.'),
    13: ('B', 'Follicular fluid inside the antrum is rich in estrogen produced by granulosa cells.'),
    14: ('B', 'The brainstem consists of the midbrain, pons, and medulla oblongata.'),
    15: ('B', 'Ejaculatory ducts open into the prostatic urethra on the seminal colliculus.'),
    16: ('A', 'The acrosome caps the anterior two-thirds of the head of the sperm.'),
    17: ('A', 'Spermiogenesis is the transformation of round spermatids into spermatozoa.'),
    18: ('A', 'The female urethra is approximately 4 cm in length.'),
    19: ('A', 'The stomach is the most dilated part of the gut, lying under the left dome of diaphragm.'),
    20: ('C', 'The apex of the heart is formed entirely by the left ventricle.'),
    21: ('A', 'Whole blood is part of the cardiovascular system, not the lymphatic system.'),
    22: ('A', 'Peripheral membrane proteins associate loosely with the cytoplasmic surface of the lipid bilayer.'),
    23: ('B', 'The folds of the inner mitochondrial membrane are designated cristae.'),
    24: ('A', 'Lipids are demonstrated histochemically using Sudan black B or Oil Red O.'),
    25: ('A', 'Smooth endoplasmic reticulum is the site of steroid hormone synthesis and drug detoxification.'),
    26: ('-', 'The centrosome functions as the main MTOC for mitotic spindle assembly.'),
    27: ('B', 'Lysosomes bud from the trans-Golgi network.'),
    28: ('A', 'In the anatomical position, the body stands erect with palms facing forward.'),
    29: ('B', 'Abduction is the movement of a limb away from the midline in the coronal plane.'),
    30: ('C', 'Epidermis of the skin is an avascular epithelium receiving nutrients by diffusion from the dermis.'),
    31: ('B', 'The surgical neck of the humerus is a narrow region distal to the tubercles, prone to fractures.'),
    32: ('A', 'Tarsal bones are 7 in number, while carpal bones are 8 in number.'),
    33: ('B', 'Each jaw contains 16 permanent teeth (32 permanent teeth in total).'),
    34: ('B', 'The duodenum is the first and shortest part of the small intestine (approx. 25 cm).'),
    35: ('C', 'The stomach has a greater curvature on the left and a lesser curvature on the right.'),
    36: ('B', 'The large intestine has distinct taeniae coli, haustra, and epiploic appendages.'),
    37: ('B', 'The right lung is divided into three lobes by horizontal and oblique fissures.'),
    38: ('A', 'The pulmonary alveoli participate in gas exchange, while the trachea and bronchi conduct air.'),
    39: ('B', 'The left ventricle has a wall approximately three times thicker than the right ventricle.'),
    40: ('B', 'Veins carry blood under lower pressure, have thinner walls, wider lumens, and possess valves in limbs.'),
    41: ('A', 'Facial, splenic, and uterine arteries are notably tortuous to adapt to organ movements.'),
    43: ('B', 'The lymphatic system includes primary (bone marrow, thymus) and secondary (spleen, lymph nodes) organs.'),
    44: ('B', 'The female urethra is about 4 cm long and opens anterior to the vaginal orifice.'),
    46: ('B', 'The ureter is a muscular tube about 25 cm long conveying urine to the bladder.'),
    47: ('B', 'The cerebral cortex exhibits an outer mantle of gray matter and an inner core of white matter.'),
    48: ('C', 'The spinal cord contains an inner H-shaped gray matter and outer white matter funiculi.'),
    49: ('B', 'The superior cerebellar peduncles connect the cerebellum to the midbrain.'),
    50: ('B', 'There are 31 pairs of spinal nerves (8 cervical, 12 thoracic, 5 lumbar, 5 sacral, 1 coccygeal).'),
    51: ('B', 'The tunica albuginea is the dense fibrous connective tissue capsule covering the testis.'),
    53: ('B', 'The infundibulum with its fimbriae is the part of the fallopian tube closest to the ovary.'),
    54: ('B', 'The centromere is the primary chromosomal constriction holding sister chromatids together.'),
    55: ('B', 'During metaphase, chromosomes align along the central equatorial plane of the spindle.'),
    56: ('A', 'Down syndrome is caused by trisomy 21 (an extra chromosome 21).'),
    57: ('A', 'Hematoxylin is a basic dye that stains acidic cell components (nucleic acids) blue.'),
    58: ('B', 'A centriole is composed of nine peripheral microtubule triplets (9x3 + 0).'),
    59: ('A', 'Glycogen is a stored metabolic inclusion, not a cytoskeletal filament.'),
    60: ('D', 'The cytoskeleton provides structural support and directs intracellular organelle transport.'),
    61: ('A', 'Ribosomes and centrioles are non-membranous cellular organelles.'),
    62: ('A', 'Rough endoplasmic reticulum is the primary site of synthesis for membrane and secretory proteins.'),
    63: ('A', 'Tissue dehydration in paraffin embedding is performed using ascending grades of ethyl alcohol.'),
    64: ('D', 'Transport vesicles are cytoplasmic membranous structures, not intranuclear components.'),
    65: ('B', 'Chromatin is composed of double-stranded DNA complexed with basic histone proteins.'),
    66: ('C', 'Ribosomes attach to the cytoplasmic surface of the endoplasmic reticulum to form rough ER.'),
    67: ('A', 'The lipid bilayer constitutes the basic structural framework of all cellular membranes.'),
    68: ('B', 'The cell membrane (plasmalemma) measures about 7.5 to 10 nm in thickness.'),
    69: ('B', 'Smooth endoplasmic reticulum is abundant in steroid-secreting cells and liver hepatocytes.'),
    70: ('C', 'Microtubules have an outer diameter of approximately 25 nm.'),
    71: ('B', 'Keratins are intermediate filaments (10 nm) characteristic of epithelial cells.'),
    72: ('B', 'DNA replication occurs during the S phase of the interphase cell cycle.'),
    73: ('A', 'Cell growth refers to the increase in total cellular mass and macromolecular content.'),
    74: ('C', 'Lysosomes do not possess ribosomes; ribosomes are found free in cytoplasm or on rough ER.'),
    98: ('C', 'Desmin is an intermediate filament protein, not a metabolic inclusion.'),
    99: ('B', 'Myosin is a motor protein (thick filament); vimentin, desmin, and keratin are intermediate filaments.'),
    100: ('C', 'Centrioles are non-membranous organelles formed of microtubule triplets.'),
    101: ('B', 'Leukocytes are transient / wandering cells that migrate into connective tissue from blood.'),
    102: ('C', 'Cartilage is an avascular tissue devoid of blood vessels, lymphatics, and nerves.'),
    103: ('C', 'Fibroblasts synthesize and secrete collagen, elastic, and reticular fibers into the ECM.'),
    104: ('D', 'Macrophages are specialized phagocytes rich in primary and secondary acid hydrolase lysosomes.'),
    107: ('A', 'Osteocytes are mature bone cells encapsulated within mineralized lacunae.'),
    108: ('A', 'Type I collagen constitutes the predominant structural collagen in bone matrix and skin dermis.'),
    111: ('C', 'Spermatogenesis sequence: Spermatogonia -> Spermatocytes -> Spermatids -> Spermatozoa.'),
    112: ('A', 'Spermatogenesis yields 4 sperms per primary cell, whereas oogenesis yields 1 ovum and polar bodies.'),
    113: ('A', 'Primary oocytes are formed during female fetal development before birth.'),
    114: ('C', 'Primary oocytes arrest in the diplotene stage of prophase I until puberty.'),
    115: ('A', 'Granulosa cells form the cumulus oophorus and corona radiata around the primary oocyte.'),
    116: ('B', 'The LH surge on day 14 triggers ovulation in a typical 28-day menstrual cycle.'),
    117: ('A', 'Sperm entry activates the secondary oocyte to resume and complete its second meiotic division.'),
    118: ('C', 'Fertilization typically occurs in the ampulla of the fallopian tube.'),
    119: ('A', 'Progesterone is secreted in large quantities by the corpus luteum during the luteal phase.'),
    120: ('C', 'Uteroplacental circulation involves maternal blood filling the syncytiotrophoblast-lined intervillous spaces.'),
    121: ('C', 'The embryonic disc remains strictly bilaminar at the buccopharyngeal and cloacal membranes.'),
    122: ('A', 'Invagination is the inward migration of epiblast cells through the primitive streak to form mesoderm.'),
    123: ('B', 'Secondary chorionic villi contain a core of extraembryonic somatic mesoderm.'),
    124: ('B', 'The adrenal cortex arises from coelomic intermediate mesoderm, not ectoderm.'),
    126: ('B', 'The notochord forms the primary axial skeleton and induces neural tube development.'),
    127: ('B', 'The maternal portion of the placenta is formed specifically by the decidua basalis.'),
    129: ('C', 'The vitello-intestinal duct connects the developing midgut to the definitive yolk sac.'),
    130: ('A', 'Amniotic fluid prevents amniotic band adhesions, permits fetal movement, and cushions trauma.'),
    131: ('B', 'The embryonic period (weeks 3 to 8) represents the window of maximal teratogenic susceptibility.'),
    132: ('B', 'Ultrasound and maternal serum markers provide non-invasive prenatal screening for chromosomal anomalies.'),
    140: ('A', 'Anatomical orientation: Ventral/anterior refers to the front, dorsal/posterior refers to the back.'),
    141: ('B', 'There are 16 permanent teeth in each jaw quadrant/arch.'),
    142: ('E', 'The right lung has 3 lobes and 2 fissures, without a cardiac notch.'),
    143: ('B', 'The vulva is richly innervated with sensory nerve endings for somatic touch and pain.'),
    144: ('A', 'Type I collagen constitutes about 90% of the organic protein matrix in adult bone.'),
    145: ('D', 'During metaphase, chromosomes align along the equatorial plate of the mitotic spindle.'),
    146: ('D', 'Osteocytes are the mature bone cells that inhabit bone lacunae.'),
    147: ('D', 'Macrophages contain abundant acid hydrolase-rich lysosomes for phagocytosis.'),
    148: ('C', 'Goblet cells are specialized mucus-secreting epithelial cells found in pseudostratified and simple columnar epithelia.'),
    149: ('B', 'Sebaceous glands show holocrine secretion where the whole secretory cell disintegrates.'),
    150: ('B', 'Capacitation is the physiological priming of spermatozoa inside the female reproductive tract.'),
    151: ('B', 'Capacitation is essential for spermatozoa to undergo the acrosome reaction and fertilize.'),
    152: ('A', 'The blastocyst is the embryonic stage that implants into the endometrial functional layer.'),
    153: ('A', 'Embryonic mesoderm forms bones, muscles, connective tissue, and the cardiovascular system.'),
    154: ('D', 'Embryonic folding in cephalocaudal and lateral dimensions transforms the disc into a cylindrical embryo.'),
    155: ('D', 'Alpha-fetoprotein (AFP) is significantly elevated in maternal serum in open neural tube defects.'),
    156: ('A', 'The mature placental barrier consists essentially of syncytiotrophoblast and fetal capillary endothelium.'),
    157: ('B', 'The embryonic period (weeks 3 to 8) is the most vulnerable period to teratogenic agents.'),
    159: ('A', 'Endocrine glands are ductless glands that release hormones directly into capillary networks.')
}

out_qs = [qs[0]]

for i in range(1, len(qs)):
    q = qs[i]
    lines = [l.strip() for l in q.split('\n') if l.strip()]
    num = lines[0]
    q_idx = int(num) if num.isdigit() else i
    
    if q_idx in corrections:
        corr_ans, exp_text = corrections[q_idx]
        q = re.sub(r'\*\*Correct Answer\*\*:\s*.*', f'**Correct Answer**: {corr_ans}', q)
        if '**Explanation**:' in q:
            q = re.sub(r'\*\*Explanation\*\*:\s*.*', f'**Explanation**: {exp_text}', q)
        else:
            q = q.rstrip() + f'\n**Explanation**: {exp_text}\n\n---\n'
    out_qs.append(q)

new_content = '### Question '.join(out_qs)
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done! Successfully updated all questions in {target_file}')
