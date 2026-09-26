import re

target_file = '/home/omar/MBset/اسيوط/Principles of microscopic and macroscopic structures/Markdown_Questions/45_anatomy_and_histology_final_and_midterm_last_years.md'
with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Map of verified medical answers and explanations for 45
corrections_45 = {
    20: ('A', 'Abduction is the movement of a limb away from the median anatomical plane in the coronal plane.'),
    21: ('A', 'The coronal (frontal) plane divides the body vertically into anterior (front) and posterior (back) parts.'),
    22: ('A', 'The thymus gland is a primary lymphoid organ in the mediastinum, not a cutaneous skin appendage.'),
    23: ('C', 'Tendons are components of the deep muscular/skeletal system, not typically found in superficial fascia.'),
    24: ('B', 'The ovulated secondary oocyte is arrested at metaphase of meiosis II until fertilization occurs.'),
    25: ('A', 'A surge of luteinizing hormone (LH) from the anterior pituitary triggers ovulation.'),
    26: ('A', 'The zona pellucida is a translucent glycoprotein coat surrounding the primary and secondary oocytes.'),
    27: ('D', 'During the 2nd month (embryonic period), human appearance develops with rapid head growth, limb bud formation, and facial morphogenesis.'),
    28: ('B', 'Late in pregnancy, the syncytiotrophoblast of the placenta takes over the production of progesterone from the corpus luteum.'),
    29: ('B', 'Persistence of the proximal part of the vitelline (yolk stalk) duct forms Meckel diverticulum of the ileum.'),
    30: ('A', 'Secondary chorionic villi are characterized by the invasion of extraembryonic somatic mesoderm into the core of primary villi.'),
    31: ('D', 'Lysosomes contain acid hydrolase enzymes that can be histochemically demonstrated by acid phosphatase staining.'),
    41: ('A', 'The decidual reaction causes endometrial stromal cells to swell, become polyhedral, and accumulate glycogen and lipids.'),
    90: ('D', 'In oogenesis, the second meiotic division is triggered by sperm entry and is completed only after fertilization.'),
    91: ('D', 'The haploid male and female nuclei that fuse during fertilization are termed pronuclei.'),
    92: ('D', 'Cleavage divisions rapidly increase cell number (blastomeres) without increasing the overall size of the conceptus.'),
    93: ('D', 'At ovulation, the mammalian oocyte is arrested specifically at metaphase of meiosis II.'),
    94: ('C', 'The middle piece (midpiece) contains the mitochondrial sheath that provides ATP for sperm motility.'),
    95: ('C', 'Urine pregnancy tests detect human chorionic gonadotrophin (hCG) secreted by syncytiotrophoblast cells.'),
    96: ('A', 'The blastocyst develops during the first week post-fertilization (days 4-5) before implanting on day 6.'),
    97: ('C', 'Intermediate mesoderm differentiates into the urogenital system, including kidneys, ureters, and gonads.'),
    98: ('A', 'The human embryo acquires a recognizable human face and external appearance by the end of the 8th week (2nd month).'),
    99: ('A', 'Extraembryonic mesoderm lies between the inner cytotrophoblast / exocoelomic membrane and the amnion / yolk sac.'),
    100: ('C', 'Dermis of the skin is derived from embryonic paraxial and lateral plate mesoderm (dermatome/somatopleure).'),
    101: ('B', 'Fine, downy lanugo hair begins to cover the fetal skin around the 16th to 20th week (4th to 5th month).'),
    102: ('A', 'Decidua capsularis overlies the conceptus and degenerates and disappears as the amniotic sac expands.'),
    103: ('A', 'The chorion lines the gestational sac and does not pass through the primitive umbilical ring.'),
    104: ('C', 'Twin-twin transfusion syndrome (TTTS) occurs exclusively in monochorionic monozygotic (identical) twins, not fraternal twins.'),
    105: ('C', 'The intervillous spaces of the placenta are filled with maternal blood supplied by eroded spiral arteries.'),
    106: ('B', 'The embryonic period (weeks 3 to 8) represents the window of maximal teratogenic susceptibility during organogenesis.'),
    107: ('B', 'The kidneys are retroperitoneal organs located on the posterior abdominal wall on either side of the vertebral column.'),
    108: ('A', 'The trachea begins in the neck at the lower border of the cricoid cartilage (C6 level) and bifurcates at T4/T5.'),
    109: ('B', 'Inversion turns the sole of the foot inward (medially), whereas eversion turns it outward (laterally).'),
    110: ('A', 'Bones receive arterial supply from nutrient arteries, periosteal vessels, and epiphyseal/metaphyseal arteries.'),
    111: ('A', 'Flat bones of the skull vault (e.g. parietal, frontal) and clavicle ossify directly within mesenchymal membranes (intramembranous).'),
    112: ('C', 'The main pancreatic duct and common bile duct unite to open into the major duodenal papilla in the 2nd part of duodenum.'),
    113: ('C', 'Synovial joints are freely movable joints enclosed by a fibrous capsule lined with synovial membrane.'),
    114: ('D', 'Nuclear lamins form a fibrous meshwork closely associated with the inner nuclear membrane.'),
    115: ('B', 'Centrioles within the centrosome organize microtubules to form the mitotic spindle during cell division.'),
    116: ('B', 'The Golgi complex consists of stacks of flattened membrane-bound cisternae with cis and trans networks.'),
    117: ('A', 'Mitochondria and the cell nucleus are organelles enclosed by two distinct lipid bilayer membranes.'),
    118: ('D', 'Neutral fats and triglycerides are demonstrated by lysochrome dyes such as Sudan black B, Sudan III, and Oil Red O.'),
    119: ('B', 'Exocytosis is the bulk vesicular transport of macromolecules out of the cell across the plasma membrane.'),
    120: ('A', 'Fibroblasts synthesize and maintain collagen, elastic, and ground substance components of the extracellular matrix.'),
    121: ('C', 'Type II collagen is the predominant structural collagen in hyaline and elastic cartilages and vitreous body.'),
    122: ('C', 'Periosteum is the vascular fibrous connective tissue sheath covering the external surfaces of all bones except articular surfaces.'),
    123: ('B', 'Haversian systems (osteons) with concentric lamellae around central vascular canals are characteristic of compact bone.'),
    127: ('A', 'The prostate is a walnut-sized male accessory gland surrounding the prostatic urethra beneath the urinary bladder.'),
    128: ('A', 'The amniotic cavity appears during the 2nd week as a slit-like space between the epiblast and cytotrophoblast.'),
    131: ('A', 'Endometrial spiral arteries supply maternal blood to the intervillous spaces of the placenta.'),
    132: ('A', 'Cell cycle: G1 phase (gap/growth), S phase (DNA synthesis), G2 phase (pre-mitotic growth), M phase (mitosis).'),
    135: ('A', 'During the S (Synthesis) phase of the cell cycle, nuclear DNA is completely replicated and centrosomes duplicate.'),
    136: ('A', 'Cilia are motile hair-like surface projections formed of an axoneme with a 9+2 microtubule doublet arrangement.'),
    155: ('A', 'Bone formation occurs by two mechanisms: intramembranous ossification and endochondral ossification.'),
    218: ('B', 'A fully developed spermatozoon acquires the capacity to fertilize after undergoing capacitation in the female genital tract.'),
    219: ('C', 'During spermiogenesis, the Golgi apparatus coalesces to form the acrosomal cap over the anterior sperm nucleus.'),
    220: ('E', 'A normal human ejaculate contains approximately 200 to 300 million spermatozoa in 2 to 5 ml of seminal fluid.'),
    221: ('C', 'The developmental sequence in spermatogenesis: Spermatogonia -> Primary spermatocytes -> Secondary spermatocytes -> Spermatids -> Spermatozoa.'),
    222: ('A', 'Primary oocytes enter the first meiotic division during fetal development and arrest at the diplotene stage of prophase I.'),
    223: ('B', 'The mid-cycle LH surge (around day 14) triggers ovulation of the dominant graafian follicle.'),
    224: ('A', 'A primordial follicle consists of a primary oocyte surrounded by a single layer of flattened follicular cells.'),
    225: ('B', 'At ovulation, the oocyte progresses to metaphase of meiosis II and remains arrested until sperm fertilization triggers its completion.'),
    226: ('E', 'The haploid paternal and maternal nuclei that fuse during fertilization are termed pronuclei.'),
    227: ('C', 'Capacitation is the physiological conditioning of spermatozoa that occurs in the female reproductive tract (uterus and fallopian tube).'),
    228: ('C', 'Release of acrosomal enzymes (hyaluronidase and acrosin) enables the fertilizing sperm to penetrate the corona radiata and zona pellucida.'),
    229: ('A', 'Cleavage is the rapid sequence of mitotic cell divisions that converts the single-celled zygote into a multicellular blastula/blastocyst.'),
    230: ('C', 'The functional layer (stratum functionale) of the endometrium is shed during menstruation, while the basal layer persists.'),
    231: ('D', 'In regular menstrual cycles of any length, ovulation consistently occurs 14 days before the onset of the next menses.'),
    232: ('B', 'The amniotic cavity originates during the 2nd week of development as a fluid-filled cleft within the epiblast.'),
    233: ('C', 'The wall of the chorionic sac is formed by extraembryonic somatic mesoderm and the inner cytotrophoblast and outer syncytiotrophoblast.'),
    264: ('B', 'Spermatogenesis produces four equal functional spermatozoa per primary cell, whereas oogenesis yields only one functional ovum and polar bodies.'),
    265: ('B', 'Spermatogenesis continues continuously throughout adult life from puberty until advanced old age.'),
    266: ('B', 'Ovulation monitoring by serial transvaginal ultrasonography tracks the growth and collapse of the dominant follicle.'),
    267: ('B', 'After ovulation, the collapsed ovarian follicle transforms into the temporary endocrine gland called the corpus luteum.'),
    268: ('A', 'Primordial ovarian follicles consist of a primary oocyte surrounded by a single flattened layer of follicular cells.'),
    269: ('B', 'The secondary oocyte released at ovulation is arrested at metaphase II of meiosis until fertilizing sperm penetrates.'),
    270: ('C', 'When spermatozoa contact the corona radiata, acrosome reactions release enzymes allowing one sperm to fertilize the ovum.'),
    271: ('E', 'The haploid nuclei of the egg and sperm before fusion are called pronuclei.'),
    272: ('B', 'Cleavage divisions begin within the ampulla of the fallopian tube as the zygote travels toward the uterus.'),
    274: ('B', 'Menstruation is triggered by the withdrawal/decline of circulating progesterone and estrogen following corpus luteum involution.'),
    275: ('B', 'Early blastocyst implantation occurs around day 6 to 7 post-fertilization in the superior posterior wall of the uterus.'),
    276: ('B', 'Ectopic tubal pregnancy occurs most frequently in the ampulla of the fallopian tube, presenting with acute pelvic pain and bleeding.'),
    277: ('B', 'The amniotic cavity develops within the epiblast layer of the bilaminar embryonic disc.'),
    278: ('C', 'Maternal blood enters the placental intervillous space from spiral arteries under pulsatile pressure.'),
    280: ('A', 'Invagination involves the inward migration of epiblast cells through the primitive streak to generate intraembryonic mesoderm.'),
    281: ('B', 'Gastrulation is the formative morphogenetic process that establishes all three primary germ layers (ectoderm, mesoderm, endoderm).'),
    282: ('B', 'Sacrococcygeal teratomas arise from pluripotent remnants of the primitive streak that fail to undergo normal regression.'),
    283: ('A', 'Fetal alcohol syndrome is characterized by microcephaly, distinct facial dysmorphism, cardiac septal defects, and intellectual disability.'),
    284: ('B', 'The anterior (cranial) neuropore closes on approximately day 25 (18-20 somite stage), followed by posterior closure on day 28.'),
    285: ('B', 'Excess amniotic fluid volume exceeding 1500-2000 ml is termed polyhydramnios, commonly linked to fetal swallowing impairment.'),
    286: ('B', 'The adrenal medulla and sensory ganglia of spinal nerves share a common embryonic origin from migratory neural crest cells.'),
    291: ('B', 'Endoderm forms the epithelial lining of the gastrointestinal tract, respiratory tract, urinary bladder, and parenchymal organs (liver, pancreas).'),
    299: ('B', 'Osteoblasts are differentiated bone-forming cells that synthesize, secrete, and calcify the organic bone matrix (osteoid).'),
    300: ('B', 'Osteocytes are mature osteoblasts that have become entrapped within lacunae and maintain bone matrix through canaliculi.'),
    301: ('C', 'Articular cartilage is hyaline cartilage lacking a perichondrium, nourished solely by synovial fluid diffusion.'),
    302: ('B', 'Chondrocytes reside singly or in isogenous groups within cartilage lacunae and maintain the surrounding proteoglycan matrix.'),
    304: ('B', 'Basophils constitute the least abundant circulating white blood cell population, accounting for 0.5% to 1% of total leukocytes.'),
    305: ('B', 'Lamina propria is the layer of loose (areolar) connective tissue underlying mucous membranes.'),
    306: ('B', 'Type VII collagen forms anchoring fibrils that link the basement membrane to underlying connective tissue collagen fibrils.'),
    307: ('B', 'Fibroblasts and adipocytes are fixed (resident) cells of connective tissue proper.'),
    308: ('B', 'Mast cells contain basophilic cytoplasmic granules rich in histamine, heparin, and eosinophil chemotactic factor.'),
    368: ('B', 'Type B spermatogonia undergo mitotic division to give rise to primary spermatocytes.'),
    373: ('B', 'The blastocyst contains an inner cell mass (embryoblast) that forms the embryo and an outer trophoblast that forms the placenta.'),
    374: ('D', 'Cleavage divisions rapidly multiply cell numbers without increasing the total volume of the pre-implantation embryo.'),
    375: ('B', 'Menstruation is the cyclical shedding of the functional layer of the endometrium due to hormonal withdrawal.'),
    376: ('B', 'During the menstrual cycle, the luteal (secretory) phase is fixed at 14 days, whereas the follicular phase may vary.'),
    377: ('B', 'The amniotic cavity appears during the 2nd week as a fluid-filled space within the epiblast.'),
    379: ('B', 'Secondary chorionic villi are formed when extraembryonic somatic mesoderm invades the core of primary villi.'),
    380: ('B', 'Neural crest cells give rise to sensory and autonomic ganglia, Schwann cells, melanocytes, and adrenal chromaffin cells.'),
    382: ('B', 'Polyhydramnios (excess amniotic fluid) is frequently associated with maternal diabetes, multiple pregnancy, or fetal GI obstructions.'),
    384: ('B', 'Somites differentiate into sclerotome (vertebrae/ribs), dermatome (dermis), and myotome (skeletal muscle).'),
    385: ('B', 'Intermediate mesoderm differentiates into the pronephros, mesonephros, metanephros (kidneys), and genital ducts.'),
    386: ('B', 'Cavitation within the lateral plate mesoderm creates the intraembryonic coelom, dividing it into somatic and splanchnic layers.'),
    387: ('B', 'Skeletal muscles and bones are mesodermal derivatives, whereas respiratory and digestive linings are endodermal.'),
    388: ('B', 'The vitelline duct maintains communication between the embryonic midgut and the yolk sac.'),
    390: ('B', 'The fetal period extends from the beginning of the ninth week until birth (delivery).'),
    391: ('B', 'Maternal perception of fetal movements (quickening) typically occurs between the 16th and 20th weeks of gestation.'),
    393: ('A', 'The placenta develops from the fetal chorion frondosum and maternal decidua basalis.'),
    394: ('D', 'A full-term placenta normally weighs 500-600 grams (1/6 of fetal birth weight), not 2-3 kilograms.'),
    395: ('C', 'In the mature third-trimester placenta, the cytotrophoblast layer is lost, leaving syncytiotrophoblast and capillary endothelium.'),
    396: ('B', 'Placenta accreta is the abnormal deep adherence of placental villi directly to the myometrium without decidua basalis.'),
    397: ('B', 'Umbilical arteries carry deoxygenated fetal blood and waste products from the fetus to the placenta.'),
    398: ('A', 'Placenta previa occurs when the placenta implants low in the uterus over or near the internal cervical os, presenting with painless bleeding.'),
    399: ('A', 'The connecting stalk initially attaches to the caudal end of the embryonic disc before ventral folding.'),
    401: ('A', 'Cord prolapse occurs when the umbilical cord slips ahead of the fetal presenting part through the cervix.'),
    402: ('B', 'A patent urachus (urachal fistula) allows continuous leakage of urine from the bladder to the umbilicus.'),
    403: ('D', 'The intraembryonic allantois obliterates postnatally to form the fibrous median umbilical ligament (urachus).'),
    404: ('B', 'Polyhydramnios is clinically defined as amniotic fluid volume exceeding 1.5 to 2.0 liters.'),
    405: ('B', 'An amniotic fluid volume under 400-500 ml represents oligohydramnios, commonly secondary to fetal renal agenesis.'),
    406: ('B', 'Fraternal (dizygotic) twins result from the simultaneous fertilization of two distinct ova by two separate spermatozoa.'),
    407: ('B', 'Cleavage of the conceptus at the two-cell stage yields monozygotic twins with separate placentas, chorions, and amnions.'),
    409: ('C', 'The embryonic period (weeks 3 through 8) is the stage of active organogenesis and peak sensitivity to teratogens.'),
    410: ('A', 'Influenza virus is not an established teratogen, whereas Rubella, CMV, and HSV are potent viral teratogens.'),
    411: ('D', 'Diagnostic ultrasonography uses acoustic sound waves without ionizing radiation and is safe throughout gestation.'),
    412: ('A', 'Fetal alcohol syndrome is characterized by intellectual disability, microcephaly, and pre- and postnatal growth deficiency.'),
    413: ('A', 'Maternal gestational diabetes causes fetal hyperinsulinism and excessive fetal growth (macrosomia).'),
    414: ('B', 'Periconceptional dietary supplementation with 400 micrograms of folic acid prevents up to 70% of neural tube defects.'),
    415: ('E', 'First uncomplicated pregnancy in a young healthy mother is not an indication for invasive prenatal testing.'),
    417: ('D', 'Amniocentesis retrieves amniotic fluid containing desquamated fetal cells for chromosomal karyotyping.'),
    419: ('B', 'Plasma cells are characterized by an eccentric nucleus with clock-face / cartwheel chromatin and abundant rough ER.'),
    421: ('B', 'Type IV collagen forms a non-fibrillar meshwork (chicken-wire pattern) specific to the lamina densa of basement membranes.'),
    495: ('B', 'Primordial germ cells are diploid cells containing 46 chromosomes that migrate from the yolk sac to genital ridges.')
}

# Process file 45
qs = content.split('### Question ')
out_qs = [qs[0]]

discarded = 0
updated = 0

for i in range(1, len(qs)):
    q = qs[i]
    lines = [l.strip() for l in q.split('\n') if l.strip()]
    num = lines[0]
    q_idx = int(num) if num.isdigit() else i
    stem = lines[1] if len(lines) > 1 else ''
    
    # Check if junk item to discard
    if any(j in stem for j in ['Short Answer questions:', 'Mcqs answers', 'T or F Answers', '—8-Hemosiderin', 'HAIHE materials', 'vertex of the skull to the midpoint']):
        discarded += 1
        continue
    
    if q_idx in corrections_45:
        corr_ans, exp_text = corrections_45[q_idx]
        q = re.sub(r'\*\*Correct Answer\*\*:\s*.*', f'**Correct Answer**: {corr_ans}', q)
        if '**Explanation**:' in q:
            q = re.sub(r'\*\*Explanation\*\*:\s*.*', f'**Explanation**: {exp_text}', q)
        else:
            q = q.rstrip() + f'\n**Explanation**: {exp_text}\n\n---\n'
        updated += 1
    
    out_qs.append(q)

new_content = '### Question '.join(out_qs)
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Done! Successfully updated {updated} questions and discarded {discarded} junk headers in {target_file}')
