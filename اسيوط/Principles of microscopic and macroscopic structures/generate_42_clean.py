import re

qs_42 = [
    (1, "In anatomical position, all the following statements are true EXCEPT:",
     {"A": "The person is standing erect.", "B": "The arms are straight by sides.", "C": "Palms are facing forward.", "D": "Legs are crossed."}, "D"),
    
    (2, "The sagittal plane:",
     {"A": "Is a horizontal plane.", "B": "Lies parallel to the median plane.", "C": "Divides the body into upper and lower parts.", "D": "Divides the body into anterior and posterior parts."}, "B"),
    
    (3, "A structure present towards the front of the body is described as:",
     {"A": "Anterior.", "B": "Posterior.", "C": "Superior.", "D": "Inferior."}, "A"),
    
    (4, "A structure present in the sole of the foot is described as:",
     {"A": "Ventral.", "B": "Dorsal.", "C": "Palmar.", "D": "Plantar."}, "D"),
    
    (5, "A structure present in the palm of the hand is described as:",
     {"A": "Ventral.", "B": "Dorsal.", "C": "Palmar.", "D": "Plantar."}, "C"),
    
    (6, "Nearer to the point of origin or attachment is termed:",
     {"A": "Distal.", "B": "Proximal.", "C": "Lateral.", "D": "Medial."}, "B"),
    
    (7, "Abduction of the fingers is movement away from the ... finger:",
     {"A": "Little", "B": "Ring", "C": "Middle", "D": "Index", "E": "Thumb"}, "C"),
    
    (8, "Which of the following is NOT a rotatory movement?",
     {"A": "Pronation.", "B": "Supination.", "C": "Retrusion.", "D": "Medial rotation."}, "C"),
    
    (9, "Rotation of foot to make the sole facing medially is called:",
     {"A": "Inversion.", "B": "Eversion.", "C": "Abduction.", "D": "Adduction."}, "A"),
    
    (10, "Which of the following is a combined movement consisting of flexion, abduction, extension, and adduction?",
     {"A": "Rotation.", "B": "Circumduction.", "C": "Supination.", "D": "Pronation."}, "B"),
    
    (11, "One of the following is an axial bone:",
     {"A": "Clavicle.", "B": "Scapula.", "C": "Sternum.", "D": "Humerus."}, "C"),
    
    (12, "The shoulder girdle is formed by:",
     {"A": "Clavicle and scapula.", "B": "Scapula and sternum.", "C": "Clavicle and humerus.", "D": "Humerus and scapula."}, "A"),
    
    (13, "Regarding ossification of bones, choose the correct statement:",
     {"A": "Clavicle ossifies in a connective tissue membrane.", "B": "Skull vault bones ossify in cartilage models.", "C": "Primary centers of ossification appear in the epiphyses.", "D": "Secondary centers of ossification appear before birth."}, "A"),
    
    (14, "A sesamoid bone is:",
     {"A": "Patella.", "B": "Femur.", "C": "Scapula.", "D": "Sternum."}, "A"),
    
    (15, "Regarding the two ends of a growing long bone, choose the correct statement:",
     {"A": "They are called diaphysis.", "B": "They don't have medullary cavities.", "C": "They are covered by periosteum at the articular surface.", "D": "They contain only yellow marrow."}, "B"),
    
    (16, "A bone gets its primary blood supply through:",
     {"A": "Periosteal vessels only.", "B": "Epiphyseal vessels only.", "C": "Nutrient artery.", "D": "Muscular attachments only."}, "C"),
    
    (17, "One of the following is NOT a cartilaginous joint:",
     {"A": "Intervertebral disc.", "B": "Symphysis pubis.", "C": "Inferior tibio-fibular joint.", "D": "First sternocostal joint."}, "C"),
    
    (18, "A pivot synovial joint is:",
     {"A": "Superior radio-ulnar joint.", "B": "Sternoclavicular joint.", "C": "Shoulder joint.", "D": "Hip joint."}, "A"),
    
    (19, "An example of hinge synovial joint:",
     {"A": "Elbow joint.", "B": "Wrist joint.", "C": "Shoulder joint.", "D": "Carpometacarpal joint of thumb."}, "A"),
    
    (20, "All the following combinations are true EXCEPT:",
     {"A": "Middle radio-ulnar joint - fibrous joint", "B": "Inferior tibio-fibular joint - fibrous syndesmosis", "C": "Symphysis pubis - primary cartilaginous joint", "D": "Sternoclavicular joint - synovial joint"}, "C"),
    
    (21, "Cardiac muscles are described as:",
     {"A": "Striated, branched, and involuntary.", "B": "Non-striated, branched, and involuntary.", "C": "Striated, unbranched, and voluntary.", "D": "Non-striated, unbranched, and involuntary."}, "A"),
    
    (22, "Regarding skeletal muscles, choose the correct statement:",
     {"A": "They are involuntary.", "B": "They are striated, voluntary, and not branched.", "C": "They are innervated by the autonomic nervous system.", "D": "They lack striations."}, "B"),
    
    (23, "A bi-pennate muscle is:",
     {"A": "Rectus abdominis.", "B": "Deltoid.", "C": "Rectus femoris.", "D": "Tibialis anterior."}, "C"),
    
    (24, "One of the following is a parallel arrangement of muscle fibers:",
     {"A": "Rectus abdominis.", "B": "Deltoid.", "C": "Tibialis anterior.", "D": "Pectoralis major."}, "A"),
    
    (25, "The muscle that opposes the action of prime mover is called:",
     {"A": "Synergist.", "B": "Antagonist.", "C": "Fixator.", "D": "Agonist."}, "B"),
    
    (26, "The muscle which initiates the movement is called:",
     {"A": "Antagonist.", "B": "Fixator.", "C": "Prime mover (agonist).", "D": "Synergist."}, "C"),
    
    (27, "Skin appendages include all the following structures EXCEPT:",
     {"A": "Nails.", "B": "Hair follicles.", "C": "Sweat glands.", "D": "Deep fascia."}, "D"),
    
    (28, "The epidermis of the skin contains:",
     {"A": "Blood vessels.", "B": "Stratified squamous keratinized epithelium.", "C": "Abundant adipose tissue.", "D": "Loose connective tissue."}, "B"),
    
    (29, "All the following statements are true about cleavage lines of the skin (Langer's lines) EXCEPT:",
     {"A": "They run longitudinally in the limbs.", "B": "They run circumferentially in the neck and trunk.", "C": "Incisions made along them heal with minimal scarring.", "D": "Incisions made along them heal with wide, prominent scars."}, "D"),
    
    (30, "Regarding the deep fascia, choose the incorrect statement:",
     {"A": "It is an inelastic dense fibrous membrane.", "B": "It forms retinacula at the wrist and ankle.", "C": "It is rich in fat deposits.", "D": "It forms intermuscular septa."}, "C"),
    
    (31, "Regarding the nerve cell, all the following statements are true EXCEPT:",
     {"A": "It consists of a cell body and processes.", "B": "Axon carries impulses away from the cell body.", "C": "Dendrites carry impulses toward the cell body.", "D": "Mature neurons divide actively by mitosis."}, "D"),
    
    (32, "The number of cervical spinal cord segments is:",
     {"A": "7", "B": "8", "C": "12", "D": "5"}, "B"),
    
    (33, "The cerebrospinal fluid (CSF) circulates in:",
     {"A": "Epidural space.", "B": "Subdural space.", "C": "Subarachnoid space.", "D": "Central canal only."}, "C"),
    
    (34, "One of the following is NOT a part of the brain stem:",
     {"A": "Midbrain.", "B": "Pons.", "C": "Medulla oblongata.", "D": "Cerebellum."}, "D"),
    
    (35, "Regarding the spinal nerve, choose the incorrect statement:",
     {"A": "It is formed by the union of dorsal and ventral roots.", "B": "It divides into dorsal and ventral rami.", "C": "Dorsal rami are larger than ventral rami.", "D": "It is a mixed nerve containing motor and sensory fibers."}, "C"),
    
    (36, "In adults, the spinal cord ends at the level of the lower border of:",
     {"A": "L1 vertebra.", "B": "L3 vertebra.", "C": "S2 vertebra.", "D": "T12 vertebra."}, "A"),
    
    (37, "The preganglionic parasympathetic fibers arise with:",
     {"A": "Thoracolumbar outflow.", "B": "Craniosacral outflow (CN III, VII, IX, X and S2-S4).", "C": "Cervical nerves.", "D": "Sympathetic trunk."}, "B"),
    
    (38, "One of the following is NOT a function of the parasympathetic nervous system:",
     {"A": "Constriction of the pupil.", "B": "Stimulation of salivary secretion.", "C": "Dilatation of bronchi and acceleration of heart rate.", "D": "Stimulation of intestinal peristalsis."}, "C"),
    
    (39, "The bicuspid (mitral) valve lies between:",
     {"A": "Right atrium and right ventricle.", "B": "Left atrium and left ventricle.", "C": "Right ventricle and pulmonary artery.", "D": "Left ventricle and aorta."}, "B"),
    
    (40, "The valve lying between the right ventricle and the pulmonary trunk is:",
     {"A": "Tricuspid valve.", "B": "Mitral valve.", "C": "Pulmonary valve.", "D": "Aortic valve."}, "C"),
    
    (41, "Blood vessels that carry blood away from the heart are:",
     {"A": "Veins.", "B": "Arteries.", "C": "Capillaries.", "D": "Lymphatics."}, "B"),
    
    (42, "Regarding the veins, choose the correct statement:",
     {"A": "They always carry oxygenated blood.", "B": "Pulmonary veins carry oxygenated blood to the left atrium.", "C": "Veins have thicker muscular walls than corresponding arteries.", "D": "Veins lack valves."}, "B"),
    
    (43, "The heart gets its arterial blood supply through:",
     {"A": "Pulmonary arteries.", "B": "Coronary arteries.", "C": "Internal thoracic arteries.", "D": "Bronchial arteries."}, "B"),
    
    (44, "The circulation of the blood from the intestine to the liver is called:",
     {"A": "Systemic circulation.", "B": "Pulmonary circulation.", "C": "Portal circulation.", "D": "Coronary circulation."}, "C"),
    
    (45, "All the following statements are true about capillaries EXCEPT:",
     {"A": "They connect arterioles to venules.", "B": "Their walls consist of a single layer of endothelial cells.", "C": "They are the site of gas and nutrient exchange.", "D": "They have thick muscular walls with valves."}, "D"),
    
    (46, "The thoracic duct begins in the abdomen as a dilated sac called:",
     {"A": "Cisterna chyli.", "B": "Spleen.", "C": "Thymus.", "D": "Lymph node."}, "A"),
    
    (47, "All the following structures are rich in lymphatic vessels EXCEPT:",
     {"A": "Dermis of the skin.", "B": "Mucosa of the digestive tract.", "C": "Central nervous system and cornea.", "D": "Lymph nodes."}, "C"),
    
    (48, "All the following statements are true about lymphatic drainage EXCEPT:",
     {"A": "Right lymphatic duct drains right side of head, neck, thorax, and right upper limb.", "B": "Thoracic duct drains both lower limbs and abdomen.", "C": "Right lymphatic duct drains the whole body below the diaphragm.", "D": "Thoracic duct opens into the junction of left internal jugular and subclavian veins."}, "C"),
    
    (49, "Which of the following minimizes friction between a tendon and an underlying bone?",
     {"A": "Synovial bursa.", "B": "Deep fascia.", "C": "Fibrous membrane.", "D": "Ligament."}, "A"),
    
    (50, "The serous sac surrounding the lung is:",
     {"A": "Pericardium.", "B": "Peritoneum.", "C": "Pleura.", "D": "Tunica vaginalis."}, "C"),
    
    (51, "According to muscle shape, pronator quadratus is classified as:",
     {"A": "Quadrilateral muscle.", "B": "Fusiform muscle.", "C": "Triangular muscle.", "D": "Circumpennate muscle."}, "A"),
    
    (52, "According to muscle shape, biceps brachii is classified as:",
     {"A": "Fusiform muscle.", "B": "Strap muscle.", "C": "Multipennate muscle.", "D": "Unipennate muscle."}, "A"),
    
    (53, "The lateral bone of the forearm is the:",
     {"A": "Radius.", "B": "Ulna.", "C": "Humerus.", "D": "Fibula."}, "A")
]

md_lines = [
    '# anatomy Qs bank(2).pdf\n',
    '- **Source File**: `anatomy Qs bank(2).pdf`',
    '- **File Type**: Scanned PDF',
    '- **Total Pages / Slides**: 12',
    '- **Assiut Tag**: Department, QBank, Anatomy',
    '- **Discipline**: Anatomy',
    f'- **Total Questions**: {len(qs_42)}\n',
    '---\n'
]

for num, stem, opts, ans in qs_42:
    md_lines.append(f'### Question {num}\n')
    md_lines.append(f'{stem}\n')
    for l in sorted(opts.keys()):
        md_lines.append(f'- **{l})** {opts[l]}')
    md_lines.append(f'\n**Correct Answer**: {ans}\n')
    md_lines.append('---\n')

with open('Markdown_Questions/42_anatomy_Qs_bank_2.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f'Wrote {len(qs_42)} clean questions to Markdown_Questions/42_anatomy_Qs_bank_2.md!')
