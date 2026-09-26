#!/usr/bin/env python3
"""Curate the visible questions from the Assiut End-of-Block exam, 24 Dec 2020."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "05_Mid_exam_2020.md"
TAG = "Exams, Midterm 2020"


def mcq(stem: str, options: list[str], answer: str, source: str = "derived") -> Question:
    return Question(
        stem=stem,
        options=options,
        correct=answer,
        source=source,
        exp="The scan has no legible printed answer key; answer derived from the source wording and standard neuroscience content. Handwritten circles were retained as review evidence where readable.",
        tag=TAG,
        year=2020,
    )


MCQS = [
    ("Regarding the multipolar neurons:", ["Golgi type I neurons have short axons", "Golgi type II neurons have long axons", "Pyramidal neurons are present in cerebellar cortex", "Purkinje neurons are present in cerebral cortex", "Stellate neurons make the majority of neurons"], "C"),
    ("Regarding neuroglia:", ["Astrocytes are present in the peripheral nervous system", "Ependymal cells are ciliated", "Microglia does not proliferate", "Oligodendrocytes form myelin sheath in the peripheral nervous system", "Schwann cells form myelin sheath in the central nervous system"], "E"),
    ("Regarding the choroid plexus:", ["It is formed of dense connective tissue", "It consists of arachnoid granulations", "It absorbs cerebrospinal fluid", "It contains continuous blood capillaries", "It is covered by ependyma connected by tight junctions"], "A"),
    ("Which of the following is NOT a monoamine neurotransmitter?", ["Dopamine", "Glutamate", "Histamine", "Noradrenaline", "Serotonin"], "B"),
    ("Which statement about ionotropic receptors is INCORRECT?", ["They are oligomeric proteins with transmembrane segments arranged around a central aqueous channel", "They are large proteins composed of five subunits that assemble in the membrane", "They operate with a long latency", "When continuously exposed to ligand, many show rapid desensitization", "When open, the ion channel is usually selective to one or more ions"], "C"),
    ("Which is the rate-limiting enzyme in serotonin synthesis?", ["Catechol-O-methyl transferase", "DOPA decarboxylase", "Monoamine oxidase", "Tryptophan hydroxylase", "Tyrosine hydroxylase"], "D"),
    ("Gray matter is chiefly made of:", ["Many glial cells but no nerve cell bodies", "Myelinated dendrites", "Myelinated nerve cell bodies", "Myelinated axons", "Nerve cell bodies and dendrites"], "E"),
    ("In vasogenic cerebral edema, in which part is the edema most severe?", ["Ependyma", "Meninges", "White matter", "Dura", "Skull"], "C"),
    ("Which histopathological finding is the most important indicator of CNS injury?", ["Astrocytosis", "Lipofuscin pigment", "Gliosis", "Red neuron", "Neuronophagia"], "C"),
    ("A sudden severe headache with subarachnoid hemorrhage at the brain base and bloody CSF most likely indicates:", ["Acute bacterial meningitis", "Ruptured berry aneurysm", "Alzheimer disease", "Hypertensive hemorrhage", "Amyloid angiopathy"], "B"),
    ("A temporal-parietal linear skull fracture after a blow to the head most likely causes:", ["Contusion of frontal lobes", "Epidural hematoma", "Ruptured berry aneurysm", "Sagittal sinus thrombosis", "Subdural hematoma"], "B"),
    ("The cells responsible for myelin formation in the CNS are:", ["Astrocytes", "Ependymal cells", "Oligodendrocytes", "Satellite cells", "Schwann cells"], "C"),
    ("Regarding the cerebral cortex or neocortex:", ["It consists of six layers", "It consists of two to three layers", "It contains only interstitial neurons", "It consists only of axons, glial cells, and blood vessels", "It is found in the deep portions of the cerebrum"], "A"),
    ("The most common route of spread of infection to the brain is:", ["Along nerves", "Direct implantation", "Via the arterial route", "Via lymphatics", "Via the venous route"], "C"),
    ("Which parasite can enter through the eyes, skin, or lungs?", ["Canthamoeba species", "Naegleria fowleri", "Trypanosoma cruzi", "Trypanosoma brucei gambiense", "Toxoplasma gondii"], "A"),
    ("A young man develops fever, myalgia, severe headache, and stiff neck after swimming in a water park. Motile trophozoites are seen. What is the diagnosis?", ["Cerebral malaria", "East African trypanosomiasis", "Granulomatous amoebic encephalitis", "Primary amoebic meningoencephalitis", "Sleeping sickness"], "D"),
    ("Diagnostic flagellated stages can be detected in CSF during infection with:", ["African trypanosomiasis", "Cerebral malaria", "Cerebral amoebic abscess", "Granulomatous amoebic encephalitis", "Neurotoxoplasmosis"], "A"),
    ("A pregnant woman with cat exposure has fetal mild hydrocephalus and lymphadenopathy. The possible diagnosis is:", ["Cerebral malaria", "Congenital toxoplasmosis", "East African trypanosomiasis", "Primary amoebic meningoencephalitis", "West African trypanosomiasis"], "B"),
    ("Which statement regarding cerebral amoebic abscess is INCORRECT?", ["It usually shows Entamoeba histolytica trophozoites", "It causes focal cystic brain lesions", "It is caused by direct spread of E. histolytica cysts into the CNS", "It is caused by hematogenous spread of E. histolytica trophozoites into the CNS", "The cerebral lesion is a single or multiple abscesses"], "D"),
    ("A febrile pilgrim who consumed unpasteurized milk develops meningitis. CSF is expected to show:", ["Encapsulated yeast demonstrated by India ink", "Gram-negative intracellular diplococci", "Gram-positive cocci in chains", "Gram-positive highly motile bacilli", "Viral antigens"], "D"),
    ("An unvaccinated child develops meningitis with other children at camp. Which vaccine was likely missed?", ["BCG vaccine", "DTaP vaccine", "Meningococcal conjugate vaccine MCV-4", "Rabies vaccine", "Salk vaccine"], "C"),
    ("An arthropod vector is involved in infection by:", ["Alphavirus", "Parainfluenza virus", "Parvovirus", "Reovirus", "Respiratory syncytial virus"], "A"),
    ("CSF with polymorphonuclear cells, low glucose, and gram-negative diplococci most likely indicates:", ["Echovirus", "Haemophilus influenzae", "Listeria monocytogenes", "Neisseria meningitidis", "Streptococcus pneumoniae"], "D"),
    ("Poliovirus is commonly transmitted by:", ["Blood", "Droplet inhalation", "Direct contact", "Fecal-oral route", "Sexual transmission"], "D"),
    ("A common adverse effect of fluoxetine in a young man is:", ["Abdominal pain", "Impotence", "Loss of taste", "Pancreatitis", "Peptic ulcers"], "B"),
    ("Which treatment should be avoided in a patient with narrow-angle glaucoma?", ["Bupropion", "Clomipramine", "Fluvoxamine", "Mirtazapine", "Sertraline"], "B"),
    ("Local anesthetics produce:", ["A stupor and somnolent state", "Alleviation of anxiety with altered consciousness", "Alleviation of pain with altered consciousness", "Analgesia, amnesia, and loss of consciousness", "Blocking pain sensation without loss of consciousness"], "E"),
    ("Which anesthetic produces dissociative anesthesia?", ["Etomidate", "Halothane", "Ketamine", "Midazolam", "Propofol"], "C"),
    ("A possible pathological finding after a prolonged halothane anesthesia is:", ["Cholelithiasis", "Hepatic necrosis", "Nephrolithiasis", "Steatorrhea", "Tinnitus"], "B"),
    ("Morphine is used in a patient suffering from:", ["Biliary colic", "Head injury", "Hypothyroidism", "Late stage of labor", "Pulmonary edema"], "E"),
    ("Morphine does not cause:", ["Analgesia", "Bronchiolar constriction", "Constipation", "Dilatation of the biliary duct", "Urinary retention"], "D"),
    ("Which is TRUE concerning autoregulation of cerebral blood flow?", ["CO2 is the primary chemical regulator", "It is inversely proportional to brain activity", "Increased extravascular H+ causes vasoconstriction", "Sympathetic stimulation causes vasodilation", "Cerebral arteriolar smooth muscle responds to stretch by vasodilation"], "A"),
    ("Which statement about CSF functions is INCORRECT?", ["Maintaining homeostasis in the brain", "Maintaining blood volume", "Protection of the brain and spinal cord", "Removal of metabolic wastes", "Supplying nutrients to the CNS"], "B"),
    ("Compared with chemical synapses, electrical synaptic transmission is:", ["Unidirectional", "More common in the CNS", "More easily modified", "More rapid", "Mediated by neurotransmitters"], "D"),
    ("Release of neurotransmitter at a chemical synapse depends on:", ["Hyperpolarization of the synaptic terminal", "Influx of calcium ions into the presynaptic terminal", "Opening of ligand-gated sodium channels", "Opening of ligand-gated potassium channels", "Synthesis of acetylcholinesterase"], "B"),
    ("Which statement about postsynaptic potentials is INCORRECT?", ["An inhibitory postsynaptic potential hyperpolarizes the postsynaptic neuron", "They are propagated down the postsynaptic neuron", "They undergo spatiotemporal summation", "They are analogous to generator and end-plate potentials", "They are proportional to the amount of transmitter released"], "B"),
    ("Which condition increases synaptic transmission?", ["Acidosis", "Alkalosis", "Anesthesia", "Hypoglycemia", "Hypoxia"], "B"),
    ("After-discharge in a neuronal pool is based mainly on:", ["After-discharge of individual neurons", "Convergence circuits", "Divergence circuits", "Reverberation circuits", "Occlusion"], "D"),
    ("Synaptic fatigue is caused by:", ["Activation of postsynaptic receptors", "Decrease in neurotransmitters in presynaptic terminals", "Depolarization of the postsynaptic membrane", "An increased postsynaptic discharge rate", "A mechanism that increases convulsions in epilepsy"], "B"),
    ("Regarding nociceptors in a diabetic patient with sensory loss, which is true?", ["Their afferents are A-alpha fibers", "They adapt rapidly to continuous stimulation", "They are distributed equally over all surfaces and internally", "They can be stimulated by any stimulus intensity", "They detect damaging stimuli regardless of the type"], "E"),
    ("Tactile discrimination:", ["Involves convergence on a single cortical neuron", "Is carried by the dorsal column medial lemniscal pathway", "Means only the sense of something touching the skin", "Reaches about 2 mm at the shoulder and 7 mm at the fingertips", "Requires stimulation of different points of the same surface"], "E"),
    ("Which comparison of slow and fast pain is correct?", ["Fast pain is transmitted through the paleospinothalamic pathway", "Fast pain fibers are C fibers", "Slow pain fibers are A-delta fibers", "Slow pain is produced by overstimulating touch receptors", "Slow pain is transmitted through the paleospinothalamic pathway"], "E"),
    ("Secondary hyperalgesia:", ["Can be explained by convergence-facilitation theory", "Does not extend beyond redness", "Has a lowered pain threshold", "Is explained by a local axon reflex", "Is localized to the injured area"], "C"),
    ("Which statement about referred pain is INCORRECT?", ["It can be explained by branching of single afferent fibers", "It is explained by convergence-projection theory", "It always accompanies cutaneous pain", "It is a major manifestation of visceral pain", "It is felt in a somatic structure innervated by the same dorsal root"], "C"),
    ("Stimulation of which brain area can modulate pain sensation?", ["Amygdala", "Cerebellum", "Locus coeruleus", "Periaqueductal gray", "Superior olivary complex"], "D"),
    ("Muscle contraction in response to maintained stretch is initiated by sensory input from:", ["A-delta fiber", "Gamma motor neuron", "Golgi tendon organ", "Nuclear bag fiber", "Nuclear chain fiber"], "E"),
    ("Which statement about the stretch reflex is INCORRECT?", ["Muscle tone and tendon jerk are monosynaptic", "Its afferent belongs to primary group Ib", "The initiating stimulus is muscle stretch", "The response is contraction of the stretched muscle", "The receptor is the muscle spindle"], "B"),
    ("Which statement is TRUE concerning the inverse myotatic reflex?", ["Its receptor is the Golgi tendon organ", "It produces positive feedback excitation of the homonymous muscle", "It causes relaxation of the antagonist muscle", "It excites neurons of synergistic muscles", "It is a monosynaptic reflex"], "A"),
    ("Which is the correct statement about speech centers?", ["The angular gyrus processes information and conducts it directly to Broca area", "The auditory association area understands spoken words", "Broca area understands written words", "Exner area is responsible for verbalization of words", "Visual sensory area 17 understands written words"], "B"),
    ("Regarding the face, which statement is correct?", ["Buccinator is supplied by the buccal branch of trigeminal nerve", "In Bell palsy the corner of the mouth goes to the nonparalyzed side on smiling", "The face has deep fascia", "Platysma lies in the cheeks", "Orbicularis oculi opens the eyelids"], "B"),
    ("Which is not a content of the anterior triangle of the neck?", ["Ansa cervicalis nerve", "External jugular vein", "Submandibular gland", "Hypoglossal nerve", "Roots of the brachial plexus"], "B"),
    ("The functional component of the olfactory nerve is:", ["General somatic afferent", "General visceral afferent", "Special somatic afferent", "Special visceral afferent", "Special visceral efferent"], "D"),
    ("Special visceral efferent fibers in the trigeminal nerve innervate:", ["Anterior belly of digastric", "Muscles of mastication", "Posterior belly of digastric", "Tensor palati", "A, B and D"], "E"),
    ("The only muscle supplied by the glossopharyngeal nerve is:", ["Hyoglossus", "Musculus uvulae", "Palatoglossus", "Palatopharyngeus", "Stylopharyngeus"], "E"),
    ("Which statement about dural venous sinuses is not true?", ["They lie between two layers of dura mater", "They drain veins from brain, eye, skull interior, and diploic veins", "The superior sagittal sinus runs in the attached margin of tentorium cerebelli", "The inferior sagittal sinus continues as the straight sinus", "The occipital sinus connects transverse and sigmoid sinuses"], "C"),
    ("Submandibular nodes do not receive afferents from:", ["Gums of upper and lower jaws", "Lateral part of lower lip", "Lower portion of nasal cavity", "The nose", "Tip of the tongue"], "E"),
    ("Which statement about the extraocular muscles is not true?", ["All recti arise from the common tendinous ring", "All recti insert into sclera behind the equator", "Oculomotor paralysis causes lateral squint", "Superior oblique depresses and abducts the eyeball", "They are voluntary and involuntary muscles"], "E"),
    ("Which is not a branch of the vertebrobasilar system?", ["Anterior and posterior spinal arteries", "Labyrinthine arteries", "Pontine arteries", "Posterior inferior cerebellar artery", "Posterior choroidal arteries"], "E"),
    ("Cleft lip is caused by failure of fusion of:", ["Lateral nasal swelling and maxillary process", "Medial nasal swelling and lateral nasal swelling", "Medial nasal swellings and maxillary process", "Lateral nasal swelling and mandibular process", "Medial nasal swelling and mandibular process"], "C"),
    ("Which dural venous sinus occupies the tentorium cerebelli?", ["Inferior petrosal sinus", "Inferior sagittal sinus", "Intercavernous sinus", "Occipital sinus", "Straight sinus"], "E"),
    ("The median and lateral apertures open into which cavity?", ["Cerebral aqueduct", "Fourth ventricle", "Left lateral ventricle", "Right lateral ventricle", "Third ventricle"], "B"),
    ("The lining of the tympanic cavity is supplied by:", ["Chorda tympani nerve", "Great auricular nerve", "Greater superficial petrosal nerve", "Lesser occipital nerve", "Tympanic plexus"], "E"),
    ("The lumbar enlargement of the spinal cord extends between:", ["L1-L5", "L2-L5", "L1-S2", "L3-S2", "L4-S1"], "A"),
    ("A hemisection-type cord syndrome with ipsilateral weakness and fine-touch loss and contralateral pain-temperature loss is most consistent with:", ["Complete cord syndrome", "Central cord syndrome", "Anterior spinal cord syndrome", "Left spinal cord hemisection syndrome", "Right spinal cord hemisection syndrome"], "D"),
    ("With respect to dermatomal nerve supply, which statement is correct?", ["Skin at the inguinal ligament is supplied by T10", "Skin at the umbilicus is supplied by T12", "Skin at the xiphoid process is supplied by T4", "Front of knee is supplied by S1", "Lateral forearm and thumb are supplied by C6"], "E"),
    ("Regarding the midbrain, which statement is correct?", ["Corticospinal and corticonuclear fibers occupy the medial half of crus cerebri", "They occupy the middle two-thirds of crus cerebri", "The midbrain contains seventh and eighth cranial nerve nuclei", "The oculomotor nerve is attached posteriorly", "Substantia nigra is present in the tectum posteriorly"], "D"),
    ("Weakness and numbness of the left arm and lower left face with other functions normal suggests a stroke involving a branch of the:", ["Left anterior cerebral artery", "Left middle cerebral artery", "Left posterior cerebral artery", "Right middle cerebral artery", "Right posterior cerebral artery"], "D"),
    ("A diabetic man has symmetric right-sided upper motor-neuron weakness of face, arm, and leg with preserved language. The damaged part is:", ["Amygdala", "Cerebellum", "Internal capsule", "Parietal lobe", "Thalamus"], "C"),
]


def main() -> int:
    questions = [mcq(stem, options, answer) for stem, options, answer in MCQS]
    count = len(questions)
    count = write_markdown(
        OUTPUT,
        "Source 5 — Assiut NEUROSCIENCE SYSTEM End-of-Block Exam 2020",
        {
            "Source file": "Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/Mid exam 2020.pdf",
            "Type": "Assiut End-of-Block MCQ examination, Form A",
            "Pages": 11,
            "Declared total": "75 MCQs on the cover; 68 visible question blocks were recoverable from the supplied scan",
            "Total questions": count,
            "Answer source": f"derived:{count} (handwritten circles are inconsistent and no printed key is present)",
            "Tag": TAG,
            "Year": 2020,
            "Note": "The visible scan contains Q1–Q48 and Q56–Q75. Source questions Q49–Q55 are absent from the supplied PDF image sequence; they are recorded as an explicit seven-question source gap and were not invented. Several marked circles conflict with the medically correct option, so derived answers are used and the source defect is retained.",
        },
        questions,
    )
    print(f"wrote {count}; QCS={count}; derived={count}; missing_source_questions=Q49-Q55; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
