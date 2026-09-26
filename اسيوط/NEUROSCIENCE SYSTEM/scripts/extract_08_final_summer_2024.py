#!/usr/bin/env python3
"""Curate the Assiut Final CNS summer 2024 model-answer scan."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "08_Final_CNS_summer_2024.md"
TAG = "Exams, Final 2024"


def q(stem: str, answer: str, discipline: str) -> Question:
    return Question(stem=stem, correct="-", source="key", exp=answer, tag=TAG,
                    tag_suggere=discipline, year=2024)


ITEMS = [
    # Anatomy, Question II.
    q("What is the motor nerve supply of the sternocleidomastoid muscle?",
      "Spinal accessory nerve.", "Anatomy"),
    q("Where does the lateral corticospinal tract terminate?",
      "Motor neurons in the ventral horn of the spinal cord.", "Anatomy"),
    q("What are the groups of muscles innervated by the branchial efferent column in the medulla oblongata?",
      "Muscles of the pharynx, muscles of the palate, and muscles of the larynx.", "Anatomy"),
    q("The superior cistern occupies the interval between the splenium of the corpus callosum and the superior surface of the cerebellum. What does it contain?",
      "The great cerebral vein.", "Anatomy"),
    q("The Reichert cartilage develops into what structure?",
      "The stapes.", "Anatomy"),
    q("The floor of the middle ear cavity is a thin plate of bone separating the tympanic cavity from what structure?",
      "The superior bulb of the internal jugular vein.", "Anatomy"),
    q("The auditory radiation is located in which part of the internal capsule?",
      "The sublenticular part.", "Anatomy"),
    q("Name one cortical area located in the occipital lobe of the cerebral hemisphere.",
      "The visual area or the visual association area.", "Anatomy"),
    q("Define commissural fibers.",
      "Commissural fibers connect corresponding regions of the two cerebral hemispheres.", "Anatomy"),
    q("In which part of the internal capsule does the corticospinal tract descend?",
      "The posterior limb.", "Anatomy"),
    q("The prefrontal and orbitofrontal cortex is supplied by which artery?",
      "The anterior cerebral artery.", "Anatomy"),
    q("The bridging veins drain venous blood from the cerebral cortex into what structure?",
      "The superior sagittal sinus.", "Anatomy"),
    # Anatomy, Question III.
    q("Posterior inferior cerebellar artery supplies the medulla and posterior inferior cerebellum. Hypoperfusion manifests with which syndrome?",
      "Lateral medullary (Wallenberg) syndrome.", "Anatomy"),
    q("The rubrocerebellar tract is located in which peduncle?",
      "The superior cerebellar peduncle.", "Anatomy"),
    q("What is the second neuron in the vestibular pathway?",
      "Vestibular nuclei.", "Anatomy"),
    q("To which nucleus of the thalamus do the efferents from the dentate nuclei send their output?",
      "The lateral ventral nucleus of the thalamus.", "Anatomy"),
    q("The posterior inferior cerebellar artery is a branch of which artery?",
      "The vertebral artery.", "Anatomy"),
    q("The midbrain is developed from which embryonic vesicle?",
      "The mesencephalon.", "Anatomy"),
    q("The myelencephalon develops into what structures?",
      "The medulla oblongata.", "Anatomy"),
    q("Injury of the optic nerve results in what visual defect?",
      "Ipsilateral anopsia.", "Anatomy"),
    q("The optic radiations are formed by the cells of which nucleus?",
      "The lateral geniculate nucleus.", "Anatomy"),
    q("What is the type of spina bifida in which vertebral arches fail to close with herniation of meninges but not the spinal cord?",
      "Meningocele.", "Anatomy"),
    q("In which condition is the occipital bone most commonly missing with herniation of meninges and part of the brain?",
      "Meningoencephalocele.", "Anatomy"),
    q("Lingual branches of the glossopharyngeal nerve mediate taste from which part of the tongue?",
      "The posterior one-third of the tongue.", "Anatomy"),
    q("What is the second neuron in the olfactory pathway?",
      "Mitral and tufted cells.", "Anatomy"),
    # Microbiology, Question IV.
    q("An elderly man has fever, confusion, and right temporal lobe necrosis. What is the most likely causative agent?",
      "Herpes simplex virus type 1 (HSV-1).", "Microbiology"),
    q("A patient develops encephalitis after an animal bite. Bullet-shaped viral antigens are demonstrated. To which virus family does the causative agent belong?",
      "Rhabdoviridae.", "Microbiology"),
    q("What is the most appropriate postexposure prophylaxis after exposure to rabies virus?",
      "Passive-active immunization: human rabies immunoglobulin for passive immunization plus inactivated rabies vaccine for active immunization.", "Microbiology"),
    q("A homeless man has fever, neck stiffness, muscle spasms, and gangrenous feet. What is the most probable diagnosis?",
      "Tetanus.", "Microbiology"),
    q("What is the main virulence factor responsible for tetanus?",
      "Tetanospasmin, a neurotoxin.", "Microbiology"),
    # Pathology, Question V.
    q("Mention the grades of astrocytoma.",
      "Grade I: pilocytic astrocytoma; Grade II: diffuse astrocytoma; Grade III: anaplastic astrocytoma; Grade IV: glioblastoma multiforme.", "Pathology"),
    q("Compare schwannoma and neurofibroma.",
      "Both are benign nerve-fiber tumors. Schwannoma is usually a single, encapsulated mass arising from Schwann cells, may involve cranial or spinal nerves, displaces the nerve fibers, shows Antoni A and Antoni B areas with Verocay bodies, and is sporadic or associated with NF2. Neurofibroma may be multiple or plexiform, involves spinal or peripheral nerves, is non-encapsulated and incorporates axons, contains elongated spindle cells with wavy nuclei, collagen, and residual nerve fibers, and is sporadic or associated with NF1; plexiform lesions carry a risk of malignant transformation.", "Pathology"),
    # Biochemistry, Question VI.
    q("Enumerate two important functions of energy for the brain.",
      "Energy restores neuronal membrane potentials after depolarization through Na⁺-K⁺ ATPase, supports transport and storage processes, and supports synthesis of neurotransmitters.", "Biochemistry"),
    q("Enumerate three basic features of conventional (classical) neurotransmitters.",
      "They are synthesized before they are needed, sequestered in secretory vesicles, released when Ca²⁺ enters the axon terminal in response to an action potential, bind postsynaptic receptors to produce a response, and are either taken back into the presynaptic cell or degraded by extracellular enzymes.", "Biochemistry"),
    # Physiology, Question VII.
    q("Compare upper motor neuron and lower motor neuron lesions. Give four differences.",
      "Upper motor neuron lesions cause widespread paralysis, increased muscle tone, hyperactive deep reflexes, absent superficial reflexes, a positive Babinski sign, clonus, and mild muscle atrophy. Lower motor neuron lesions cause limited paralysis, decreased muscle tone, hypoactive deep reflexes, decreased superficial reflexes, fasciculation and fibrillation, and severe muscle atrophy.", "Physiology"),
    q("List three clinical uses of human EEG.",
      "EEG helps determine the sites of pathological lesions in the brain, diagnose different types of epilepsy, diagnose brain death and certain psychopathic disturbances, and determine stages of sleep.", "Physiology"),
    q("Define the stretch reflex.",
      "It is a reflex contraction of a skeletal muscle, with an intact nerve, when the muscle is passively stretched.", "Physiology"),
    q("Name two necessary processes in learning and memory and mention their meanings.",
      "Encoding is the initial learning of information by perceiving it and relating it to past knowledge. Storage is maintaining information over time. Retrieval is the ability to access information when needed; any two of these processes are acceptable.", "Physiology"),
    q("Mention three characteristics of cerebellar ataxia and explain each.",
      "Dysmetria is inability to perform movement over the correct distance because of loss of predictive function. Dysarthria is interrupted, scanning speech caused by asynergy of speech muscles. Decomposition of movement is performance of a complex movement in steps because of failure of progression. Other accepted characteristics include adiadochokinesia, intention tremor, cerebellar nystagmus, rebound phenomenon, asynergia, and a zigzag gait.", "Physiology"),
    q("Mention two conditions associated with hypertonia and hyperreflexia.",
      "Tetany and hyperthyroidism are examples. Hypertonia and hyperreflexia may also result when facilitatory supraspinal control exceeds inhibitory control of spinal centers, such as in an upper motor neuron lesion.", "Physiology"),
    q("Define presbyopia and state its correction.",
      "Presbyopia is a physiological reduction of accommodation with age, accompanied by recession of the near point. It is corrected with convex lenses.", "Physiology"),
    q("Explain how aqueous humor can affect intraocular pressure.",
      "Increased formation of aqueous humor increases intraocular pressure. Decreased formation decreases pressure. Decreased aqueous outflow increases pressure because of increased resistance in the trabecular meshwork or increased episcleral venous pressure.", "Physiology"),
    q("Enumerate two differences between scotopic and photopic vision.",
      "Scotopic vision is rod-mediated peripheral vision with low acuity, poorly seen detail, and absent color vision. Photopic vision is cone-mediated central vision with high acuity, clear detail, and color vision.", "Physiology"),
    q("List three mechanisms by which the vestibular system maintains equilibrium.",
      "It regulates antigravity muscle tone of the trunk and limbs through lateral vestibulospinal pathways to extensor lower motor neurons, maintains head position and a constant plane of vision through the medial vestibulospinal tract to neck muscles, and coordinates eye movements with head movement to maintain the visual field through vestibular connections with extraocular motor nuclei in the brainstem.", "Physiology"),
    q("Mention the mechanism of auditory transduction by a hair cell.",
      "The apical membrane is ciliated and the stereocilia are polarized in high-potassium, low-sodium endolymph. Bending toward the tallest stereocilium opens mechanically gated channels, allowing K⁺ entry and depolarizing the hair cell. Depolarization opens voltage-gated Ca²⁺ channels, Ca²⁺ triggers glutamate exocytosis, and the afferent fiber firing rate increases. Bending away hyperpolarizes the cell and decreases transmitter release and afferent firing.", "Physiology"),
    q("Explain the interaural intensity difference mechanism of sound localization.",
      "It is the horizontal localization mechanism useful for high-frequency sounds above about 3000 Hz. A sound from straight ahead reaches both ears with equal intensity; a sound from one side is reduced at the opposite ear by the sound shadow of the head. The circuit compares excitation and inhibition through the lateral superior olive and the medial nucleus of the trapezoid body, producing greater output on the side of the louder ear.", "Physiology"),
    # Histology, Question VIII.
    q("Enumerate the types of neurons according to the number of fibers.",
      "Unipolar or pseudounipolar neurons, bipolar neurons, multipolar neurons, Golgi type I neurons, Golgi type II neurons, stellate neurons, pyramidal cells, and Purkinje cells.", "Histology"),
    q("Compare histologically the two types of intrafusal muscle fibers in a muscle spindle.",
      "Nuclear bag fibers are larger and have a central expanded region containing many nuclei in a bag-like arrangement. Nuclear chain fibers are thinner and have a row of nuclei along the central part. Both are enclosed by the spindle capsule and are supplied by sensory and motor endings.", "Histology"),
    q("Enumerate the histological structures of the molecular layer of the cerebellar cortex.",
      "The molecular layer contains the axons of granule cells forming parallel fibers, dendrites of Purkinje cells, stellate cells, and basket cells.", "Histology"),
    q("Mention two refractive media of the eye.",
      "Any two of the cornea, aqueous humor, lens, and vitreous humor.", "Histology"),
    q("What is the lining epithelium of the cornea?",
      "Stratified squamous non-keratinizing epithelium.", "Histology"),
    q("Enumerate the types of cells of taste buds seen by electron microscopy.",
      "Glial-like supporting cells (type I), receptor cells (type II), presynaptic cells (type III), and basal cells.", "Histology"),
    # Parasitology, Questions IX-X.
    q("Enumerate two helminthic diseases causing cystic brain lesions.",
      "Hydatidosis, cysticercosis, and coenurosis are accepted examples.", "Parasitology"),
    q("A patient has multiple small frontal-lobe cysts with a hole-with-dot appearance. What parasitic disease causes this manifestation?",
      "Neurocysticercosis.", "Parasitology"),
    q("What is the name of the larva found in the brain in neurocysticercosis?",
      "Cysticercus cellulosae.", "Parasitology"),
    q("A woman from Cameroon sees a worm moving in the sclera and has painless forearm swelling. How do you confirm African eye worm disease?",
      "Examine a thick blood smear stained with Giemsa for microfilariae.", "Parasitology"),
    q("What is the suitable time to take the specimen for confirmation of African eye worm disease?",
      "During daytime, approximately 10 a.m. to 12 p.m., because of diurnal periodicity.", "Parasitology"),
]


def main() -> int:
    count = write_markdown(
        OUTPUT,
        "Source 8 — Final CNS summer 2024 model answer",
        {
            "Source file": "Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/final CNS summer 2024.pdf",
            "Type": "Assiut written model-answer examination",
            "Pages": 9,
            "Total questions": len(ITEMS),
            "Answer source": f"key:{len(ITEMS)} (printed model answers)",
            "Tag": TAG,
            "Year": 2024,
            "Note": "The first PDF page is a phone status-bar capture with no declared question. Pages 2–9 contain the printed model answers. Section subparts are retained as individual QROC records; no MCQ answer key is present in this source.",
        },
        ITEMS,
    )
    print(f"wrote {count}; QROC={count}; key={count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
