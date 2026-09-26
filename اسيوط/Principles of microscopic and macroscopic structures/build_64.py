# -*- coding: utf-8 -*-
"""
Build certified, noise-free 64_q_bank_anatomy.md
Contains Part 1 (Bones, Skin, Terms: 54 MCQs + 4 Essay Qs)
and Part 2 (Joints, Muscles, Serous: 75 MCQs + 6 Essay Qs)
Visually verified from q bank anatomy.pdf with authentic printed model answers and explanations.
"""

part1_mcqs = [
    {
        "stem": "The plane that divides the body into a large right part & a small left part is:",
        "options": [
            "A) Median.",
            "B) Right parasagittal.",
            "C) Left parasagittal.",
            "D) Coronal.",
            "E) Transverse."
        ],
        "correct": "C",
        "exp": "Left parasagittal plane."
    },
    {
        "stem": "Which of the following is responsible for the growth of the bone in length?",
        "options": [
            "A) Periosteum.",
            "B) Endosteum.",
            "C) Epiphysis.",
            "D) Epiphyseal plate.",
            "E) Diaphysis."
        ],
        "correct": "D",
        "exp": "Epiphyseal plate."
    },
    {
        "stem": "What is the type of the lunate (carpal) bone?",
        "options": [
            "A) Long.",
            "B) Flat.",
            "C) Irregular.",
            "D) Sesamoid.",
            "E) Short."
        ],
        "correct": "E",
        "exp": "Short bones include carpal & tarsal bones."
    },
    {
        "stem": "The parasagittal plane divides the body into:",
        "options": [
            "A) Right & left equal parts.",
            "B) Right & left unequal parts.",
            "C) Anterior & posterior parts.",
            "D) Upper & lower parts.",
            "E) Right anterior & left posterior parts."
        ],
        "correct": "B",
        "exp": "Parasagittal plane divides body into right & left unequal halves."
    },
    {
        "stem": "Adduction of toes occurs in which direction?",
        "options": [
            "A) Away from the 2nd toe.",
            "B) Away from the big toe.",
            "C) Towards the big toe.",
            "D) Towards the 2nd toe.",
            "E) Towards the middle line of body."
        ],
        "correct": "D",
        "exp": "Adduction of toes is towards 2nd toe."
    },
    {
        "stem": "Which of the following is a long bone?",
        "options": [
            "A) Clavicle.",
            "B) Sternum.",
            "C) Scapula.",
            "D) Rib.",
            "E) Sphenoid."
        ],
        "correct": "A",
        "exp": "Clavicle."
    },
    {
        "stem": "Which part of the bone is responsible for its growth in diameter (breadth)?",
        "options": [
            "A) Epiphysis.",
            "B) Periosteum.",
            "C) Epiphyseal plate.",
            "D) Endosteum.",
            "E) Nutrient artery."
        ],
        "correct": "B",
        "exp": "Periosteum."
    },
    {
        "stem": "The epidermis of the skin is thick in:",
        "options": [
            "A) Eyelids.",
            "B) Scrotum.",
            "C) Back.",
            "D) Palm of hand.",
            "E) Abdomen."
        ],
        "correct": "D",
        "exp": "Palm of hand."
    },
    {
        "stem": "A bone that ossifies from a membrane:",
        "options": [
            "A) Radius.",
            "B) Femur.",
            "C) Clavicle.",
            "D) Scapula.",
            "E) Sternum."
        ],
        "correct": "C",
        "exp": "Clavicle."
    },
    {
        "stem": "Inversion means:",
        "options": [
            "A) Sole of foot faces laterally.",
            "B) Palm of hand faces anteriorly.",
            "C) Sole of foot faces medially.",
            "D) Palm of hand faces posteriorly.",
            "E) Dorsum of foot faces upwards."
        ],
        "correct": "C",
        "exp": "In inversion, the sole faces medially."
    },
    {
        "stem": "Superficial fascia is devoid of fat at:",
        "options": [
            "A) Eyelids.",
            "B) Anterior abdominal wall.",
            "C) Palm of hand.",
            "D) Sole of foot.",
            "E) Buttocks."
        ],
        "correct": "A",
        "exp": "Eyelids."
    },
    {
        "stem": "Which of the following is a short bone?",
        "options": [
            "A) Radius.",
            "B) Sternum.",
            "C) Vertebra.",
            "D) Maxilla.",
            "E) Tarsal bone."
        ],
        "correct": "E",
        "exp": "Tarsal bone."
    },
    {
        "stem": "Which type of bone is the pisiform?",
        "options": [
            "A) Long.",
            "B) Sesamoid.",
            "C) Irregular.",
            "D) Pneumatic.",
            "E) Flat."
        ],
        "correct": "B",
        "exp": "Pisiform is considered as a short bone & sesamoid bone."
    },
    {
        "stem": "Thick skin is present in:",
        "options": [
            "A) Face.",
            "B) Dorsum of hand.",
            "C) Abdomen.",
            "D) Palm of hand.",
            "E) Back."
        ],
        "correct": "D",
        "exp": "Palm of hand."
    },
    {
        "stem": "Thick cleavage (Langer's) lines of skin represent:",
        "options": [
            "A) Skin creases over joints.",
            "B) Direction of elastin fibers in the epidermis.",
            "C) Direction of elastin fibers in the dermis.",
            "D) Direction of collagen fibers in the dermis.",
            "E) Direction of collagen fibers in the hypodermis."
        ],
        "correct": "D",
        "exp": "Langer's lines represent direction of collagen fibers."
    },
    {
        "stem": "Regarding sesamoid bones, all the following statements are true EXCEPT:",
        "options": [
            "A) Develop inside tendons.",
            "B) Have no periosteum.",
            "C) Resist friction.",
            "D) Maintain blood supply of joints.",
            "E) The patella is an example."
        ],
        "correct": "D",
        "exp": "Sesamoid bones have nothing to do with blood supply of joints."
    },
    {
        "stem": "In which one of the following cavities is yellow bone marrow present?",
        "options": [
            "A) Sphenoidal air sinus.",
            "B) Maxillary air sinus.",
            "C) Medullary cavity of long bone.",
            "D) Subarachnoid space.",
            "E) Epidural space."
        ],
        "correct": "C",
        "exp": "Bone marrow lies in medullary cavity."
    },
    {
        "stem": "The presence of epiphyseal plate indicates that the bone is:",
        "options": [
            "A) Increasing in length.",
            "B) Increasing in diameter.",
            "C) Decreasing in diameter.",
            "D) Dead.",
            "E) Stopped increasing in length."
        ],
        "correct": "A",
        "exp": "Epiphyseal plate increases bone in length."
    },
    {
        "stem": "Tarsal bones are classified as:",
        "options": [
            "A) Long bones.",
            "B) Short bones.",
            "C) Flat bones.",
            "D) Sesamoid bones.",
            "E) Irregular bones."
        ],
        "correct": "B",
        "exp": "Tarsal bones are short bones."
    },
    {
        "stem": "Primary center of ossification of a long bone:",
        "options": [
            "A) Lies at metaphysis.",
            "B) Appears after birth.",
            "C) Causes ossification of epiphysis.",
            "D) Increases breadth of bone.",
            "E) Changes cartilaginous shaft into bone."
        ],
        "correct": "E",
        "exp": "1ry center of ossification appears before birth in shaft to change its cartilage into bone."
    },
    {
        "stem": "What is the name of the vertical plane that divides the body into anterior & posterior parts?",
        "options": [
            "A) Median.",
            "B) Right parasagittal.",
            "C) Left parasagittal.",
            "D) Coronal.",
            "E) Transverse."
        ],
        "correct": "D",
        "exp": "Coronal plane."
    },
    {
        "stem": "What is the structure that never exists in superficial fascia?",
        "options": [
            "A) Tendons.",
            "B) Fat.",
            "C) Blood vessels.",
            "D) Nerves.",
            "E) Muscles."
        ],
        "correct": "A",
        "exp": "Superficial fascia contains fat, blood vessels, nerves & sometimes muscles. It never contains tendons."
    },
    {
        "stem": "Concerning the deep fascia, all the following are true EXCEPT:",
        "options": [
            "A) Forms retinaculae.",
            "B) Forms fibrous flexor sheaths.",
            "C) Is present in face.",
            "D) Covers the muscles.",
            "E) Divides limbs into compartments."
        ],
        "correct": "C",
        "exp": "Face has no deep fascia."
    },
    {
        "stem": "Which one of the following is not a part of the axial skeleton?",
        "options": [
            "A) Scapula.",
            "B) Sternum.",
            "C) Vertebrae.",
            "D) Ribs.",
            "E) Skull."
        ],
        "correct": "A",
        "exp": "Scapula is a part of the appendicular skeleton."
    },
    {
        "stem": "Which one of the following is a flat bone?",
        "options": [
            "A) Vertebra.",
            "B) Humerus.",
            "C) Carpal bone.",
            "D) Clavicle.",
            "E) Scapula."
        ],
        "correct": "E",
        "exp": "Scapula is a flat bone."
    },
    {
        "stem": "The metaphysis of the long bone is:",
        "options": [
            "A) The part of the epiphysis near the epiphyseal plate.",
            "B) The part of the epiphysis away from the epiphyseal plate.",
            "C) The part of the diaphysis near the epiphyseal plate.",
            "D) The part of the diaphysis near the center of the bone.",
            "E) The place of the epiphyseal plate."
        ],
        "correct": "C",
        "exp": "The metaphysis is the part of the diaphysis near the epiphyseal plate."
    },
    {
        "stem": "Which of the following is a characteristic of the long bone?",
        "options": [
            "A) Increases in length by periosteum.",
            "B) Its shaft has a medullary cavity.",
            "C) It is covered from outside by endosteum.",
            "D) Its metaphysis is a part of its epiphysis.",
            "E) Its primary center of ossification appears after birth."
        ],
        "correct": "B",
        "exp": "The shaft has a medullary cavity."
    },
    {
        "stem": "The skeleton of the hand includes all the following EXCEPT:",
        "options": [
            "A) Three phalanges in index finger.",
            "B) Five metacarpal bones.",
            "C) Seven carpal bones.",
            "D) Two phalanges in thumb.",
            "E) Three phalanges in middle finger."
        ],
        "correct": "C",
        "exp": "Carpal bones are 8 in number."
    },
    {
        "stem": "Which of the following is an irregular bone?",
        "options": [
            "A) Humerus.",
            "B) Vertebra.",
            "C) Rib.",
            "D) Clavicle.",
            "E) Patella."
        ],
        "correct": "B",
        "exp": "The vertebra is an irregular bone."
    },
    {
        "stem": "The primary center of ossification of the long bone:",
        "options": [
            "A) Changes the cartilaginous shaft into bone.",
            "B) Appears in the epiphysis.",
            "C) Appears immediately after birth.",
            "D) Appears at site of epiphyseal cartilage.",
            "E) Helps in growth of bone in width."
        ],
        "correct": "A",
        "exp": "1ry center of ossification appears before birth & changes cartilaginous shaft into bone."
    },
    {
        "stem": "Axial skeleton includes:",
        "options": [
            "A) Femur.",
            "B) Tibia.",
            "C) Sternum.",
            "D) Clavicle.",
            "E) Hip bone."
        ],
        "correct": "C",
        "exp": "Axial skeleton includes sternum."
    },
    {
        "stem": "The medial structure is the structure that lies:",
        "options": [
            "A) Closer to the upper end of the body.",
            "B) Closer to the lower end of the body.",
            "C) Closer to the front of the body.",
            "D) Closer to the back of the body.",
            "E) Closer to the median plane of the body."
        ],
        "correct": "E",
        "exp": "Medial = closer to median plane."
    },
    {
        "stem": "Adduction means:",
        "options": [
            "A) Moving a part away from the midline.",
            "B) Moving a part towards the midline.",
            "C) Moving a part forwards.",
            "D) Moving a part backwards.",
            "E) Rotating a part medially."
        ],
        "correct": "B",
        "exp": "Adduction = moving a part towards midline."
    },
    {
        "stem": "Pronation means:",
        "options": [
            "A) Medial rotation of thumb.",
            "B) Lateral rotation of thumb.",
            "C) Medial rotation of forearm.",
            "D) Lateral rotation of forearm.",
            "E) Rotation of trunk."
        ],
        "correct": "C",
        "exp": "Pronation = medial rotation of forearm."
    },
    {
        "stem": "Which one of the following is a part of the axial skeleton?",
        "options": [
            "A) Humerus.",
            "B) Radius.",
            "C) Vertebral column.",
            "D) Femur.",
            "E) Fibula."
        ],
        "correct": "C",
        "exp": "Vertebral column is a part of the axial skeleton."
    },
    {
        "stem": "The number of the lumbar vertebrae is:",
        "options": [
            "A) Five.",
            "B) Seven.",
            "C) Eight.",
            "D) Ten.",
            "E) Twelve."
        ],
        "correct": "A",
        "exp": "Lumbar vertebrae are 5 in number."
    },
    {
        "stem": "The anterior structure is the structure that lies:",
        "options": [
            "A) Closer to the upper end of the body.",
            "B) Closer to the lower end of the body.",
            "C) Closer to the front of the body.",
            "D) Closer to the back of the body.",
            "E) Closer to the median plane of the body."
        ],
        "correct": "C",
        "exp": "Anterior = closer to front of body."
    },
    {
        "stem": "Abduction means:",
        "options": [
            "A) Moving a part away from the midline.",
            "B) Moving a part towards the midline.",
            "C) Moving a part forwards.",
            "D) Moving a part backwards.",
            "E) Rotating a part medially."
        ],
        "correct": "A",
        "exp": "Abduction = moving a part away from midline."
    },
    {
        "stem": "Which one of the following is a part of the axial skeleton?",
        "options": [
            "A) Humerus.",
            "B) Scapula.",
            "C) Tibia.",
            "D) Fibula.",
            "E) Sternum."
        ],
        "correct": "E",
        "exp": "Sternum is a part of the axial skeleton."
    },
    {
        "stem": "The number of the cervical vertebrae is:",
        "options": [
            "A) Five.",
            "B) Seven.",
            "C) Eight.",
            "D) Ten.",
            "E) Twelve."
        ],
        "correct": "B",
        "exp": "Cervical vertebrae are 7 in number."
    },
    {
        "stem": "The shoulder girdle is formed of:",
        "options": [
            "A) Clavicle and humerus.",
            "B) Scapula and humerus.",
            "C) Clavicle and Scapula.",
            "D) Clavicle and sternum.",
            "E) Scapula and sternum."
        ],
        "correct": "C",
        "exp": "Shoulder girdle = clavicle & scapula."
    },
    {
        "stem": "The diaphysis:",
        "options": [
            "A) Has a medullary cavity.",
            "B) Forms the ends of the long bone.",
            "C) Is covered by articular cartilage.",
            "D) Develops by 2ry center of ossification.",
            "E) Is formed of cancellous bone."
        ],
        "correct": "A",
        "exp": "Diaphysis (shaft) has a medullary cavity."
    },
    {
        "stem": "Bones increase in thickness by:",
        "options": [
            "A) Epiphyseal cartilage.",
            "B) Nutrient artery.",
            "C) Metaphysis.",
            "D) Epiphysis.",
            "E) Periosteum."
        ],
        "correct": "E",
        "exp": "Bone increases in thickness by periosteum."
    },
    {
        "stem": "Which one of the following structures is the most proximal?",
        "options": [
            "A) Elbow joint.",
            "B) Arm.",
            "C) Shoulder joint.",
            "D) Hand.",
            "E) Wrist joint."
        ],
        "correct": "C",
        "exp": "Shoulder joint is the most proximal."
    },
    {
        "stem": "Which one of the following bones shares in the formation of a girdle?",
        "options": [
            "A) Humerus.",
            "B) Scapula.",
            "C) Tibia.",
            "D) Femur.",
            "E) Sternum."
        ],
        "correct": "B",
        "exp": "Scapula shares in the formation of shoulder girdle."
    },
    {
        "stem": "The epiphysis:",
        "options": [
            "A) Has a medullary cavity.",
            "B) Forms the shaft of the long bone.",
            "C) Is covered by periosteum.",
            "D) Develops by 2ry center of ossification.",
            "E) Is formed of compact bone."
        ],
        "correct": "D",
        "exp": "Epiphysis develops from 2ry center of ossification."
    },
    {
        "stem": "The number of the thoracic vertebrae is:",
        "options": [
            "A) Five.",
            "B) Seven.",
            "C) Eight.",
            "D) Ten.",
            "E) Twelve."
        ],
        "correct": "E",
        "exp": "Thoracic vertebrae are 12 in number."
    },
    {
        "stem": "Which one of the following is a rotatory movement?",
        "options": [
            "A) Protraction.",
            "B) Inversion.",
            "C) Abduction.",
            "D) Flexion.",
            "E) Pronation."
        ],
        "correct": "E",
        "exp": "Pronation is medial rotation of forearm."
    },
    {
        "stem": "Abduction of fingers means movement of fingers away from:",
        "options": [
            "A) Thumb.",
            "B) Index.",
            "C) Middle finger.",
            "D) Ring finger.",
            "E) Little finger."
        ],
        "correct": "C",
        "exp": "Abduction = moving fingers away from middle finger."
    },
    # 50-54 matching
    {
        "stem": "Match the bone with its type: Skull cap is a:",
        "options": [
            "A) Long bone.",
            "B) Short bone.",
            "C) Flat bone.",
            "D) Irregular bone.",
            "E) Sesamoid bone."
        ],
        "correct": "C",
        "exp": "Skull cap is a flat bone."
    },
    {
        "stem": "Match the bone with its type: Facial bones are:",
        "options": [
            "A) Long bone.",
            "B) Short bone.",
            "C) Flat bone.",
            "D) Irregular bone.",
            "E) Sesamoid bone."
        ],
        "correct": "D",
        "exp": "Facial bones are irregular bones."
    },
    {
        "stem": "Match the bone with its type: Radius is a:",
        "options": [
            "A) Long bone.",
            "B) Short bone.",
            "C) Flat bone.",
            "D) Irregular bone.",
            "E) Sesamoid bone."
        ],
        "correct": "A",
        "exp": "Radius is a long bone."
    },
    {
        "stem": "Match the bone with its type: Patella is a:",
        "options": [
            "A) Long bone.",
            "B) Short bone.",
            "C) Flat bone.",
            "D) Irregular bone.",
            "E) Sesamoid bone."
        ],
        "correct": "E",
        "exp": "Patella is a sesamoid bone."
    },
    {
        "stem": "Match the bone with its type: Carpal bone is a:",
        "options": [
            "A) Long bone.",
            "B) Short bone.",
            "C) Flat bone.",
            "D) Irregular bone.",
            "E) Sesamoid bone."
        ],
        "correct": "B",
        "exp": "Carpal bone is a short bone."
    }
]

part1_essays = [
    {
        "stem": "Name the parts of the growing long bones. Mention how it increases in length & breadth.",
        "exp": "Parts of growing long bone: Diaphysis (shaft), Epiphysis (ends), Metaphysis (part of diaphysis adjacent to epiphyseal cartilage), and Epiphyseal cartilage plate.\nIncrease in length: By proliferation of cartilage cells in the epiphyseal plate.\nIncrease in breadth (thickness): By appositional bone deposition by osteoblasts in the periosteum."
    },
    {
        "stem": "Describe ossification of long bones.",
        "exp": "Long bones ossify predominantly via intracartilaginous (endochondral) ossification from a hyaline cartilage model. Primary ossification center appears in the diaphysis before birth (around 8th week IUL) forming periosteal collar and central calcification. Secondary ossification centers appear in the epiphyses usually after birth. Epiphyseal cartilage plate persists between diaphysis and epiphysis until full skeletal maturity when it undergoes synostosis."
    },
    {
        "stem": "Describe types of ossification giving examples.",
        "exp": "1. Intramembranous ossification: Bone develops directly within condensed mesenchymal connective tissue membranes (e.g. bones of skull vault, facial bones, clavicle).\n2. Intracartilaginous (endochondral) ossification: Mesenchyme first forms a hyaline cartilage model which is later replaced by bone (e.g. long bones of limbs, vertebrae, ribs, sternum)."
    },
    {
        "stem": "Define the anatomical position. Name the 3 different planes of the body.",
        "exp": "Anatomical position: Standing erect, facing forward, eyes looking to the horizon, upper limbs hanging at sides with palms facing forward (thumbs pointing laterally), and lower limbs together with feet flat and toes pointing forward.\nPlanes of the body:\n1. Median (sagittal) plane: Vertical anteroposterior plane dividing body into right and left equal halves.\n2. Coronal (frontal) plane: Vertical plane perpendicular to sagittal plane, dividing body into anterior and posterior parts.\n3. Transverse (horizontal) plane: Horizontal plane perpendicular to sagittal and coronal planes, dividing body into superior and inferior parts."
    }
]

part2_mcqs = [
    {
        "stem": "An example of secondary cartilaginous joint:",
        "options": [
            "A) Symphysis pubis.",
            "B) Sternocostal joint.",
            "C) Costochondral joint.",
            "D) Sacroiliac joint.",
            "E) Sternoclavicular joint."
        ],
        "correct": "A",
        "exp": "Symphysis pubis."
    },
    {
        "stem": "An example of unipennate muscle:",
        "options": [
            "A) Sartorius.",
            "B) Flexor pollicis longus.",
            "C) Dorsal interosseous.",
            "D) Rectus femoris.",
            "E) Deltoid."
        ],
        "correct": "B",
        "exp": "Flexor pollicis longus."
    },
    {
        "stem": "Which one of the following muscles is a bipennate muscle?",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Subscapularis.",
            "C) 2nd dorsal interosseous.",
            "D) 3rd palmar interosseous.",
            "E) Deltoid."
        ],
        "correct": "C",
        "exp": "All dorsal interosseii are bipennate."
    },
    {
        "stem": "What is the type of the ankle joint?",
        "options": [
            "A) Condyloid joint.",
            "B) Plane joint.",
            "C) Hinge joint.",
            "D) Pivot joint.",
            "E) Saddle joint."
        ],
        "correct": "C",
        "exp": "Ankle & elbow joints are synovial hinge joints."
    },
    {
        "stem": "What is the joint that contains a cartilaginous disc?",
        "options": [
            "A) Superior radioulnar joint.",
            "B) Ankle joint.",
            "C) Metacarpophalangeal joints.",
            "D) Temporo-mandibular joint.",
            "E) Carpometacarpal joint of thumb."
        ],
        "correct": "D",
        "exp": "Temporo-mandibular joint contains a disc."
    },
    {
        "stem": "Which one of the following joints is the most moveable?",
        "options": [
            "A) Suture.",
            "B) Syndesmosis.",
            "C) Hinge.",
            "D) Gomphosis.",
            "E) Primary cartilaginous."
        ],
        "correct": "C",
        "exp": "Hinge joint is a synovial joint which is the most moveable. Other joints are either fibrous or cartilaginous joints that show little or no movement."
    },
    {
        "stem": "The function of the tendon is to link:",
        "options": [
            "A) A muscle to a bone.",
            "B) A bone to a cartilage.",
            "C) A muscle to skin.",
            "D) A cartilage to skin.",
            "E) A bone to a bone."
        ],
        "correct": "A",
        "exp": "Tendons of muscles fix them to bones."
    },
    {
        "stem": "Which one of the following muscles is a multipennate muscle?",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Rectus femoris.",
            "C) Dorsal interosseii.",
            "D) Temporalis.",
            "E) Deltoid."
        ],
        "correct": "E",
        "exp": "Deltoid is a Multipennate muscle."
    },
    {
        "stem": "An example of a triangular muscle is:",
        "options": [
            "A) Sartorius.",
            "B) External abdominal oblique muscle.",
            "C) Temporalis.",
            "D) Rectus femoris.",
            "E) Dorsal interosseous."
        ],
        "correct": "C",
        "exp": "Temporalis is a triangular muscle."
    },
    {
        "stem": "Match each joint with its type: Inferior tibiofibular joint is a:",
        "options": [
            "A) Plane.",
            "B) Hinge.",
            "C) Fibrous.",
            "D) 2ry cartilaginous.",
            "E) Pivot."
        ],
        "correct": "C",
        "exp": "Inferior tibiofibular joint is a fibrous joint (syndesmosis)."
    },
    {
        "stem": "Match each joint with its type: Intervertebral disc is a:",
        "options": [
            "A) Plane.",
            "B) Hinge.",
            "C) Fibrous.",
            "D) 2ry cartilaginous.",
            "E) Pivot."
        ],
        "correct": "D",
        "exp": "Intervertebral disc is a secondary cartilaginous joint (symphysis)."
    },
    {
        "stem": "Match each joint with its type: Elbow joint is a:",
        "options": [
            "A) Plane.",
            "B) Hinge.",
            "C) Fibrous.",
            "D) 2ry cartilaginous.",
            "E) Pivot."
        ],
        "correct": "B",
        "exp": "Elbow joint is a synovial hinge joint."
    },
    {
        "stem": "Match each joint with its type: Radioulnar joints are:",
        "options": [
            "A) Plane.",
            "B) Hinge.",
            "C) Fibrous.",
            "D) 2ry cartilaginous.",
            "E) Pivot."
        ],
        "correct": "E",
        "exp": "Radioulnar joints are synovial pivot joints."
    },
    {
        "stem": "Match each joint with its type: Acromioclavicular joint is a:",
        "options": [
            "A) Plane.",
            "B) Hinge.",
            "C) Fibrous.",
            "D) 2ry cartilaginous.",
            "E) Pivot."
        ],
        "correct": "A",
        "exp": "Acromioclavicular joint is a synovial plane joint."
    },
    {
        "stem": "The 2ry cartilaginous joint unites bones by:",
        "options": [
            "A) Synovial fluid.",
            "B) White fibrocartilage.",
            "C) Fibrous tissue.",
            "D) Yellow elastic cartilage.",
            "E) Hyaline cartilage."
        ],
        "correct": "B",
        "exp": "2ry cartilaginous joints bind bones by white fibrocartilage."
    },
    {
        "stem": "The joints between the bones of the skull vault (cap) belong to:",
        "options": [
            "A) Synovial joint.",
            "B) Syndesmosis.",
            "C) Sutures.",
            "D) Symphysis.",
            "E) Gomphosis."
        ],
        "correct": "C",
        "exp": "Sutures bind bones of skull cap."
    },
    {
        "stem": "Which one of the following muscles is a unipennate muscle?",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Dorsal interosseous.",
            "D) Temporalis.",
            "E) Deltoid."
        ],
        "correct": "A",
        "exp": "Flexor pollicis longus is a unipennate muscle."
    },
    {
        "stem": "Which one of the following joints is a hinge synovial?",
        "options": [
            "A) Superior radioulnar joint.",
            "B) Shoulder joint.",
            "C) Wrist joint.",
            "D) Elbow joint.",
            "E) Acromioclavicular joint."
        ],
        "correct": "D",
        "exp": "Elbow joint is a hinge synovial joint."
    },
    {
        "stem": "Primary cartilaginous joints:",
        "options": [
            "A) Are usually temporary.",
            "B) Allow wide range of movement.",
            "C) Are present between teeth & jaw.",
            "D) Unite bones by fibrous tissue.",
            "E) Unite lower ends of tibia & fibula."
        ],
        "correct": "A",
        "exp": "1ry cartilaginous joints ossify at a certain age."
    },
    {
        "stem": "Which one of the following joints is ellipsoid?",
        "options": [
            "A) Superior radioulnar joint.",
            "B) Ankle joint.",
            "C) Wrist joint.",
            "D) Interphalangeal joint.",
            "E) Sternoclavicular joint."
        ],
        "correct": "C",
        "exp": "Wrist joint is an ellipsoid joint."
    },
    {
        "stem": "The example of the muscle that is inserted in a raphe is:",
        "options": [
            "A) Digastric.",
            "B) Biceps.",
            "C) Popliteus.",
            "D) Pharyngeal muscles.",
            "E) Facial muscles."
        ],
        "correct": "D",
        "exp": "Pharyngeal muscles."
    },
    {
        "stem": "Match each joint with its type: Inferior tibiofibular is:",
        "options": [
            "A) Condyloid synovial.",
            "B) Hinge synovial.",
            "C) Syndesmosis.",
            "D) 1ry cartilaginous.",
            "E) Saddle synovial."
        ],
        "correct": "C",
        "exp": "Syndesmosis is a fibrous joint."
    },
    {
        "stem": "Match each joint with its type: Carpometacarpal joint of thumb is:",
        "options": [
            "A) Condyloid synovial.",
            "B) Hinge synovial.",
            "C) Syndesmosis.",
            "D) 1ry cartilaginous.",
            "E) Saddle synovial."
        ],
        "correct": "E",
        "exp": "Carpometacarpal joint of thumb is a saddle synovial joint."
    },
    {
        "stem": "Match each joint with its type: Elbow is:",
        "options": [
            "A) Condyloid synovial.",
            "B) Hinge synovial.",
            "C) Syndesmosis.",
            "D) 1ry cartilaginous.",
            "E) Saddle synovial."
        ],
        "correct": "B",
        "exp": "Elbow is a hinge synovial joint."
    },
    {
        "stem": "Match each joint with its type: Epiphyseal plate is:",
        "options": [
            "A) Condyloid synovial.",
            "B) Hinge synovial.",
            "C) Syndesmosis.",
            "D) 1ry cartilaginous.",
            "E) Saddle synovial."
        ],
        "correct": "D",
        "exp": "Epiphyseal plate is a primary cartilaginous joint."
    },
    {
        "stem": "Match each joint with its type: Metacarpophalangeal is:",
        "options": [
            "A) Condyloid synovial.",
            "B) Hinge synovial.",
            "C) Syndesmosis.",
            "D) 1ry cartilaginous.",
            "E) Saddle synovial."
        ],
        "correct": "A",
        "exp": "Metacarpophalangeal joint is a condyloid synovial joint."
    },
    {
        "stem": "All the following are types of muscle attachments EXCEPT:",
        "options": [
            "A) Tendon.",
            "B) Raphe.",
            "C) Ligament.",
            "D) Aponeurosis.",
            "E) Fleshy fibers."
        ],
        "correct": "C",
        "exp": "Ligaments are not a type of muscle attachment."
    },
    {
        "stem": "Match each muscle action: Muscle producing opposite action is:",
        "options": [
            "A) Synergist.",
            "B) Agonist.",
            "C) Antagonist.",
            "D) Fixator."
        ],
        "correct": "C",
        "exp": "Antagonist produces opposite action."
    },
    {
        "stem": "Match each muscle action: Muscle preventing movement of another joint is:",
        "options": [
            "A) Synergist.",
            "B) Agonist.",
            "C) Antagonist.",
            "D) Fixator."
        ],
        "correct": "D",
        "exp": "Fixator prevents movement of another joint."
    },
    {
        "stem": "Match each muscle action: Muscle initiating a particular movement is:",
        "options": [
            "A) Synergist.",
            "B) Agonist.",
            "C) Antagonist.",
            "D) Fixator."
        ],
        "correct": "B",
        "exp": "Agonist initiates a particular movement."
    },
    {
        "stem": "Match each muscle action: Muscle aiding another in the same movement is:",
        "options": [
            "A) Synergist.",
            "B) Agonist.",
            "C) Antagonist.",
            "D) Fixator."
        ],
        "correct": "A",
        "exp": "Synergist aids another in the same movement."
    },
    {
        "stem": "An example of parallel type of muscle is:",
        "options": [
            "A) Rectus femoris.",
            "B) Sartorius.",
            "C) Dorsal interosseous.",
            "D) Deltoid.",
            "E) Flexor pollicis longus."
        ],
        "correct": "B",
        "exp": "Sartorius has parallel fibers."
    },
    {
        "stem": "Symphysis pubis is:",
        "options": [
            "A) Pivot synovial joint.",
            "B) Primary cartilaginous joint.",
            "C) Hinge synovial joint.",
            "D) Secondary cartilaginous joint.",
            "E) Fibrous joint."
        ],
        "correct": "D",
        "exp": "Symphysis pubis is a 2ry cartilaginous joint."
    },
    {
        "stem": "Match muscle fiber arrangement: Unipennate is:",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Sartorius.",
            "D) Deltoid.",
            "E) Dorsal interosseous."
        ],
        "correct": "A",
        "exp": "Flexor pollicis longus is unipennate."
    },
    {
        "stem": "Match muscle fiber arrangement: Bipennate is:",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Sartorius.",
            "D) Deltoid.",
            "E) Dorsal interosseous."
        ],
        "correct": "E",
        "exp": "Dorsal interosseous is bipennate."
    },
    {
        "stem": "Match muscle fiber arrangement: Multipennate is:",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Sartorius.",
            "D) Deltoid.",
            "E) Dorsal interosseous."
        ],
        "correct": "D",
        "exp": "Deltoid is multipennate."
    },
    {
        "stem": "Match muscle fiber arrangement: Circumpennate is:",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Sartorius.",
            "D) Deltoid.",
            "E) Dorsal interosseous."
        ],
        "correct": "B",
        "exp": "Tibialis anterior is circumpennate."
    },
    {
        "stem": "Match muscle fiber arrangement: Parallel fibers is:",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Tibialis anterior.",
            "C) Sartorius.",
            "D) Deltoid.",
            "E) Dorsal interosseous."
        ],
        "correct": "C",
        "exp": "Sartorius has parallel fibers."
    },
    {
        "stem": "Most of the joints that lie in the median plane of the body are:",
        "options": [
            "A) Syndesmosis.",
            "B) Primary cartilaginous joints.",
            "C) Gomphosis.",
            "D) Secondary cartilaginous joints.",
            "E) Plane synovial joints."
        ],
        "correct": "D",
        "exp": "Most midline joints are 2ry cartilaginous joints."
    },
    {
        "stem": "Which one of the following muscles has spiralized fibers?",
        "options": [
            "A) Flexor pollicis longus.",
            "B) Subscapularis.",
            "C) 2nd dorsal interosseous.",
            "D) 3rd palmar interosseous.",
            "E) Trapezius."
        ],
        "correct": "E",
        "exp": "Trapezius is a Spiralized muscle."
    },
    {
        "stem": "All are characters of synovial joint EXCEPT:",
        "options": [
            "A) It has a joint cavity.",
            "B) A capsule binds its articulating bones.",
            "C) May contain intra-articular disc.",
            "D) The articular surfaces are covered by synovial membrane.",
            "E) They are freely mobile joints."
        ],
        "correct": "D",
        "exp": "Articular surfaces of synovial joints are not covered by synovial membrane but are covered by hyaline articular cartilages."
    },
    {
        "stem": "Which of the following is a uniaxial joint?",
        "options": [
            "A) Metacarpophalangeal joints.",
            "B) Intervertebral disc.",
            "C) Atlanto-axial joint.",
            "D) Hip joint.",
            "E) Wrist joint."
        ],
        "correct": "C",
        "exp": "Median atlanto-axial joint is a uniaxial (pivot) joint."
    },
    {
        "stem": "As regards the cartilaginous joints, choose INCORRECT statement:",
        "options": [
            "A) Secondary cartilaginous joints allow limited movement.",
            "B) Syndesmosis is a type of primary cartilaginous joint.",
            "C) Primary cartilaginous joints are usually temporary.",
            "D) Secondary cartilaginous joints lie usually in median plane.",
            "E) In secondary cartilaginous joints, articular surfaces are connected by fibrocartilage."
        ],
        "correct": "B",
        "exp": "Syndesmosis is a fibrous joint."
    },
    {
        "stem": "Primary cartilaginous joints:",
        "options": [
            "A) Allow free movement.",
            "B) Usually ossifies with age.",
            "C) Unite two pubic bones.",
            "D) Unite lower end of tibia & fibula.",
            "E) Occur between the tooth & socket in the jaw."
        ],
        "correct": "B",
        "exp": "1ry cartilaginous joints usually ossify with age."
    },
    {
        "stem": "Match joint with its type: Elbow is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "B",
        "exp": "Elbow is a hinge joint."
    },
    {
        "stem": "Match joint with its type: Carpometacarpal of thumb is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "E",
        "exp": "Carpometacarpal of thumb is a saddle joint."
    },
    {
        "stem": "Match joint with its type: Hip joint is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "C",
        "exp": "Hip joint is a ball & socket joint."
    },
    {
        "stem": "Match joint with its type: Wrist is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "D",
        "exp": "Wrist is an ellipsoid joint."
    },
    {
        "stem": "Match joint with its type: Shoulder is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "C",
        "exp": "Shoulder is a ball & socket joint."
    },
    {
        "stem": "Match joint with its type: Gomphosis is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "A",
        "exp": "Gomphosis is a fibrous joint."
    },
    {
        "stem": "Match joint with its type: Sutures is:",
        "options": [
            "A) Fibrous.",
            "B) Hinge.",
            "C) Ball & socket.",
            "D) Ellipsoid.",
            "E) Saddle."
        ],
        "correct": "A",
        "exp": "Sutures are fibrous joints."
    },
    {
        "stem": "As regards the muscles, choose the INCORRECT statement:",
        "options": [
            "A) A bipennate muscle looks like a complete feather.",
            "B) The most moveable part of the muscle is its origin.",
            "C) A raphe is a mixture of fleshy & tendinous fibers.",
            "D) The muscle may be inserted into the skin.",
            "E) Most muscles have tendons attached to bones."
        ],
        "correct": "B",
        "exp": "The origin is the most fixed part of the muscle."
    },
    {
        "stem": "As regards the skeletal muscles, choose the INCORRECT statement:",
        "options": [
            "A) The origin is the most moveable end of the muscle.",
            "B) Contraction means approximation of origin & insertion.",
            "C) Septa from deep fascia divide them into groups.",
            "D) They are mostly under voluntary control.",
            "E) They are innervated by motor, sensory & autonomic nerve fibers."
        ],
        "correct": "A",
        "exp": "The origin is the most fixed part of the muscle."
    },
    {
        "stem": "Match muscle with appropriate definition: Trapezius is:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "E",
        "exp": "Trapezius has spiral fibers."
    },
    {
        "stem": "Match muscle with appropriate definition: Rectus femoris is:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "B",
        "exp": "Rectus femoris is bipennate."
    },
    {
        "stem": "Match muscle with appropriate definition: Sternocleidomastoid is:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "D",
        "exp": "Sternocleidomastoid is cruciate."
    },
    {
        "stem": "Match muscle with appropriate definition: Dorsal interosseii are:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "B",
        "exp": "Dorsal interosseii are bipennate."
    },
    {
        "stem": "Match muscle with appropriate definition: Deltoid is:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "C",
        "exp": "Deltoid is multipennate."
    },
    {
        "stem": "Match muscle with appropriate definition: Flexor pollicis longus is:",
        "options": [
            "A) Unipennate.",
            "B) Bipennate.",
            "C) Multipennate.",
            "D) Cruciate.",
            "E) Spiral."
        ],
        "correct": "A",
        "exp": "Flexor pollicis longus is unipennate."
    },
    {
        "stem": "Which one of the following structures never lies inside synovial cavity?",
        "options": [
            "A) Articular cartilage.",
            "B) Menisci.",
            "C) Synovial fluid.",
            "D) Fibrous capsule.",
            "E) Ligaments."
        ],
        "correct": "D",
        "exp": "The fibrous capsule surrounds the joint from outside but never lies inside the joint."
    },
    {
        "stem": "Secondary cartilaginous joints:",
        "options": [
            "A) Are formed partly by fibrocartilage.",
            "B) Ossify with age.",
            "C) Show no movements.",
            "D) Include epiphyseal plate of long bones.",
            "E) Appear between bones in base of skull."
        ],
        "correct": "A",
        "exp": "2ry cartilaginous joints are formed by fibrocartilage."
    },
    {
        "stem": "Which one of the following is an ellipsoid joint?",
        "options": [
            "A) Shoulder.",
            "B) Elbow.",
            "C) Wrist.",
            "D) Hip.",
            "E) Knee."
        ],
        "correct": "C",
        "exp": "Wrist joint."
    },
    {
        "stem": "The joints between the parts of the sternum are:",
        "options": [
            "A) Synovial plane.",
            "B) Synovial hinge.",
            "C) Primary cartilaginous.",
            "D) Secondary cartilaginous.",
            "E) Fibrous."
        ],
        "correct": "D",
        "exp": "2ry cartilaginous joint."
    },
    {
        "stem": "Menisci are present in:",
        "options": [
            "A) Shoulder.",
            "B) Elbow.",
            "C) Wrist.",
            "D) Ankle.",
            "E) Knee."
        ],
        "correct": "E",
        "exp": "Menisci are present in knee joint."
    },
    {
        "stem": "Which of the following is (are) not striated:",
        "options": [
            "A) Skeletal muscle and cardiac muscle.",
            "B) Skeletal muscle and smooth muscle.",
            "C) Smooth muscle and cardiac muscle.",
            "D) Smooth muscle only.",
            "E) Cardiac muscle only."
        ],
        "correct": "D",
        "exp": "Smooth muscles only are non-striated. Skeletal & cardiac muscles are striated."
    },
    {
        "stem": "The long fibrous cord for attachment of muscles is called:",
        "options": [
            "A) Aponeurosis.",
            "B) Tendon.",
            "C) Bipennate.",
            "D) Raphe.",
            "E) Cruciate."
        ],
        "correct": "B",
        "exp": "The tendon is a long fibrous cord."
    },
    {
        "stem": "The articular surface of the synovial joint is covered by:",
        "options": [
            "A) Synovial membrane.",
            "B) Fibrous capsule.",
            "C) Hyaline cartilage.",
            "D) Capsular ligament.",
            "E) Extracapsular ligament."
        ],
        "correct": "C",
        "exp": "Articular surfaces are covered by hyaline cartilage."
    },
    {
        "stem": "Primary cartilaginous joints:",
        "options": [
            "A) Are formed by fibrocartilage.",
            "B) Do not ossify with age.",
            "C) Show no movements.",
            "D) Include intervertebral disc.",
            "E) Appear between parts of sternum."
        ],
        "correct": "C",
        "exp": "1ry cartilaginous joints usually show no movement."
    },
    {
        "stem": "Which one of the following is a ball and socket joint?",
        "options": [
            "A) Shoulder.",
            "B) Elbow.",
            "C) Wrist.",
            "D) Ankle.",
            "E) Knee."
        ],
        "correct": "A",
        "exp": "Shoulder joint."
    },
    {
        "stem": "The fibrous band that separates flesh muscles from each other is called:",
        "options": [
            "A) Aponeurosis.",
            "B) Tendon.",
            "C) Bipennate.",
            "D) Raphe.",
            "E) Cruciate."
        ],
        "correct": "D",
        "exp": "Raphe."
    },
    {
        "stem": "Match each serous membrane: Tunica vaginalis surrounds:",
        "options": [
            "A) Abdominal viscera.",
            "B) Between muscles & bones.",
            "C) Lungs.",
            "D) Testis.",
            "E) Tendons of muscles."
        ],
        "correct": "D",
        "exp": "Tunica vaginalis surrounds testis."
    },
    {
        "stem": "Match each serous membrane: Pleura surrounds:",
        "options": [
            "A) Abdominal viscera.",
            "B) Between muscles & bones.",
            "C) Lungs.",
            "D) Testis.",
            "E) Tendons of muscles."
        ],
        "correct": "C",
        "exp": "Pleura surrounds lungs."
    },
    {
        "stem": "Match each serous membrane: Synovial sheath surrounds:",
        "options": [
            "A) Abdominal viscera.",
            "B) Between muscles & bones.",
            "C) Lungs.",
            "D) Testis.",
            "E) Tendons of muscles."
        ],
        "correct": "E",
        "exp": "Synovial sheath surrounds tendons of muscles."
    },
    {
        "stem": "Match each serous membrane: Peritoneum surrounds:",
        "options": [
            "A) Abdominal viscera.",
            "B) Between muscles & bones.",
            "C) Lungs.",
            "D) Testis.",
            "E) Tendons of muscles."
        ],
        "correct": "A",
        "exp": "Peritoneum surrounds abdominal viscera."
    },
    {
        "stem": "Match each serous membrane: Bursae are located:",
        "options": [
            "A) Abdominal viscera.",
            "B) Between muscles & bones.",
            "C) Lungs.",
            "D) Testis.",
            "E) Tendons of muscles."
        ],
        "correct": "B",
        "exp": "Bursae lie between muscles & bones."
    }
]

part2_essays = [
    {
        "stem": "Classify the types of synovial joints; give one example for each.",
        "exp": "1. Plane synovial joint: e.g. Acromioclavicular joint, intercarpal joints.\n2. Uniaxial joints:\n   - Hinge joint: e.g. Elbow joint, ankle joint, interphalangeal joints.\n   - Pivot joint: e.g. Superior & inferior radioulnar joints, median atlanto-axial joint.\n3. Biaxial joints:\n   - Condyloid joint: e.g. Metacarpophalangeal joints, wrist joint.\n   - Ellipsoid joint: e.g. Wrist joint.\n   - Saddle joint: e.g. Carpometacarpal joint of thumb.\n4. Polyaxial (multiaxial) joint:\n   - Ball and socket joint: e.g. Shoulder joint, hip joint."
    },
    {
        "stem": "Classify synovial uniaxial joints; mentioning the axis, movements & 2 examples of each.",
        "exp": "1. Hinge joint:\n   - Axis: Transverse axis.\n   - Movements: Flexion and extension.\n   - Examples: Elbow joint, ankle joint, interphalangeal joints.\n2. Pivot joint:\n   - Axis: Longitudinal (vertical) axis.\n   - Movements: Rotation (e.g. pronation/supination, medial/lateral rotation).\n   - Examples: Superior radioulnar joint, median atlanto-axial joint."
    },
    {
        "stem": "Compare primary & secondary cartilaginous joints.",
        "exp": "1. Primary cartilaginous joint (Synchondrosis):\n   - Articular surfaces united by hyaline cartilage.\n   - No movement allowed.\n   - Usually temporary (ossifies with age).\n   - Examples: Epiphyseal plate of long bone, first sternocostal joint, spheno-occipital synchondrosis.\n2. Secondary cartilaginous joint (Symphysis):\n   - Articular surfaces covered by hyaline cartilage and united by a plate of white fibrocartilage.\n   - Limited movement allowed.\n   - Permanent (does not ossify with age).\n   - Located in the median plane of the body.\n   - Examples: Symphysis pubis, intervertebral discs, manubriosternal joint."
    },
    {
        "stem": "Classify fibrous joints giving one example for each.",
        "exp": "1. Sutures: Bones united by sutural ligament (dense connective tissue); immovable; e.g. Sutures of the skull cap (coronal, sagittal, lambdoid sutures).\n2. Syndesmosis: Bones united by an interosseous membrane or ligament; slight movement; e.g. Inferior tibiofibular joint, middle radioulnar joint.\n3. Gomphosis (peg-and-socket): Tooth root fitted into its alveolar socket and united by periodontal ligament; no movement; e.g. Dentoalveolar joint."
    },
    {
        "stem": "Classify types of skeletal muscles according to the arrangement of its fibers, giving one example for each type.",
        "exp": "1. Parallel fibers: Fibers run parallel to the line of pull (e.g. Sartorius, strap muscles).\n2. Pennate (feather-like) fibers:\n   - Unipennate: Tendon on one side, fibers oblique on one side (e.g. Flexor pollicis longus, extensor digitorum longus).\n   - Bipennate: Central tendon, fibers converge from both sides (e.g. Rectus femoris, dorsal interossei).\n   - Multipennate: Multiple central tendons with diagonal fibers (e.g. Deltoid, subscapularis).\n   - Circumpennate: Cylindrical tendon with circular oblique fibers (e.g. Tibialis anterior).\n3. Triangular (convergent) fibers: Broad origin converging to a narrow tendon (e.g. Temporalis, pectoralis major).\n4. Spiralized / Cruciate fibers: Fibers twist or cross (e.g. Trapezius, sternocleidomastoid, latissimus dorsi).\n5. Circular fibers: Sphincters surrounding orifices (e.g. Orbicularis oris, orbicularis oculi)."
    },
    {
        "stem": "Describe the structure of a synovial joint.",
        "exp": "A synovial joint is characterized by:\n1. Articular surfaces: Covered by a thin layer of smooth hyaline cartilage (articular cartilage), devoid of perichondrium, blood vessels, or nerves.\n2. Joint cavity: A potential space between the articulating bones filled with synovial fluid.\n3. Fibrous capsule: Dense fibrous sheath completely enclosing the joint and attached to bones beyond the articular margins.\n4. Synovial membrane: Vascular connective tissue lining the inner aspect of capsule and all non-articular surfaces, secreting viscous synovial fluid for lubrication and nutrition.\n5. Supporting structures (accessories): Intracapsular/extracapsular ligaments, articular discs/menisci (fibrocartilage), labra (e.g. glenoid labrum), and bursae/fat pads."
    }
]

print(f"Part 1: {len(part1_mcqs)} MCQs, {len(part1_essays)} Essays")
print(f"Part 2: {len(part2_mcqs)} MCQs, {len(part2_essays)} Essays")
total_q = len(part1_mcqs) + len(part1_essays) + len(part2_mcqs) + len(part2_essays)
print(f"Total Questions: {total_q}")

header = f"""# q bank anatomy.pdf

- **Source File**: `q bank anatomy.pdf`
- **File Type**: Scanned PDF Booklet
- **Total Pages / Slides**: 21
- **Assiut Tag**: Department, QBank, Anatomy
- **Discipline**: Anatomy
- **Total Questions**: {total_q}

---

"""

body = []
q_counter = 1

# Part 1 MCQs
for q in part1_mcqs:
    q_str = f"### Question {q_counter}\n\n{q['stem']}\n\n"
    for opt in q['options']:
        q_str += f"- **{opt[:2]}** {opt[3:].strip()}\n"
    q_str += f"\n**Correct Answer**: {q['correct']}\n\n"
    if q.get('exp'):
        q_str += f"**Explanation**: {q['exp']}\n\n"
    q_str += "---\n"
    body.append(q_str)
    q_counter += 1

# Part 1 Essays
for q in part1_essays:
    q_str = f"### Question {q_counter}\n\n{q['stem']}\n\n"
    q_str += f"**Correct Answer**: -\n\n"
    q_str += f"**Explanation**: {q['exp']}\n\n---\n"
    body.append(q_str)
    q_counter += 1

# Part 2 MCQs
for q in part2_mcqs:
    q_str = f"### Question {q_counter}\n\n{q['stem']}\n\n"
    for opt in q['options']:
        q_str += f"- **{opt[:2]}** {opt[3:].strip()}\n"
    q_str += f"\n**Correct Answer**: {q['correct']}\n\n"
    if q.get('exp'):
        q_str += f"**Explanation**: {q['exp']}\n\n"
    q_str += "---\n"
    body.append(q_str)
    q_counter += 1

# Part 2 Essays
for q in part2_essays:
    q_str = f"### Question {q_counter}\n\n{q['stem']}\n\n"
    q_str += f"**Correct Answer**: -\n\n"
    q_str += f"**Explanation**: {q['exp']}\n\n---\n"
    body.append(q_str)
    q_counter += 1

full_content = header + "\n".join(body)

output_path = "Markdown_Questions/64_q_bank_anatomy.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Successfully generated {output_path} with {total_q} verified questions!")
