#!/usr/bin/env python3
"""Extract the nine declared written questions from the 9 Jan 2024 model answer."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "03_CNS_Final_2024_Model.md"

ITEMS = [
    (
        "Question I — Pharmacology. Answer the following: (1) compare buspirone and diazepam using three differences; (2) compare haloperidol and clozapine using three differences; (3) enumerate three therapeutic uses of valproic acid; (4) list three adverse effects that occur with long-term levodopa–carbidopa use.",
        "(1) Buspirone is a selective 5-HT1A partial agonist and anxiolytic with little abuse potential, no clinically important tolerance, and no withdrawal syndrome; diazepam is a benzodiazepine receptor agonist with anxiolytic, hypnotic, skeletal-muscle-relaxant, and anticonvulsant effects, and chronic use risks dependence, abuse, residual drowsiness, delayed reaction time, incoordination, confusion, anterograde amnesia, and paradoxical disinhibition. (2) Haloperidol is a typical competitive D2 blocker with frequent extrapyramidal effects and hyperprolactinemia, mainly treating positive schizophrenia symptoms; clozapine is atypical, mainly inhibits 5-HT2A and affects D1/D4 more than D2, has fewer extrapyramidal effects and less hyperprolactinemia, and treats positive and negative symptoms. (3) Valproic acid: partial and generalized seizures including absence seizures; mood stabilization in bipolar affective disorder; migraine prophylaxis. (4) Long-term levodopa–carbidopa: dyskinesias, behavioral disturbances with hallucinations and confusion, on-off phenomenon, and a malignant neuroleptic-like syndrome after abrupt withdrawal; any three are accepted.",
    ),
    (
        "Question II — Anatomy. Answer the twelve source items: one structure passing between superior and middle pharyngeal constrictors; origin level of the right common carotid; terminal end of the spinal cord; decussation of the second-order dorsal-column neuron; muscles supplied by the branchial efferent column in pons; surface marking of the frontal middle meningeal branch; artery supplying the fourth-ventricle choroid plexus; embryological origin of tongue muscles; structure separated from the orbit by its floor; muscle in the middle ear; order of the medial geniculate neuron in the auditory pathway; and one parietal cortical area.",
        "Stylopharyngeus muscle or glossopharyngeal nerve. The right common carotid arises from the brachiocephalic trunk at the right sternoclavicular joint. The terminal spinal-cord segment is the conus medullaris. The second-order dorsal-column neuron decussates in the medulla oblongata. The pontine branchial efferent column supplies muscles of the face and muscles of mastication. The frontal branch of the middle meningeal artery is approached through a burr hole at the pterion, about 3 cm above the midpoint of the zygomatic arch (about 3.5 cm behind and 1.2 cm above the frontozygomatic suture). The fourth-ventricle choroid plexus is supplied by the posterior inferior cerebellar artery. Tongue muscles develop from occipital somites. The orbital floor separates the orbit from the maxillary sinus. The middle ear contains tensor tympani. The medial geniculate relay is the fourth-order neuron in the source model answer. A parietal cortical area may be the primary sensory cortex (areas 3, 1, and 2) or the secondary sensory association area.",
    ),
    (
        "Question III — Anatomy. Answer the ten source items: largest brain commissure; internal-capsule part carrying corticobulbar fibers; regions supplied by proximal middle-cerebral deep branches; destination of bridging veins; cerebellar lobe controlling balance; thalamic nucleus receiving dentate efferents; parent artery of the anterior inferior cerebellar artery; derivatives of metencephalon and myelencephalon; two types of spina bifida; and the nerve and ganglion carrying taste from the epiglottis and tongue root.",
        "The corpus callosum is the largest commissure. Corticobulbar fibers descend through the genu of the internal capsule. Lateral and medial striate arteries supply the striatum and internal-capsule regions. Bridging veins drain into the superior sagittal sinus. Balance is controlled by the flocculonodular lobe. Dentate efferents relay to the lateral ventral nucleus of the thalamus. The anterior inferior cerebellar artery is a branch of the basilar artery. The metencephalon develops into the pons and cerebellum, while the myelencephalon develops into the medulla. Types of spina bifida include spina bifida occulta, meningocele, and meningomyelocele; any two are accepted. Taste from the epiglottis and tongue root is carried by the superior laryngeal nerve, whose cells are in the inferior ganglion of the vagus.",
    ),
    (
        "Question IV — Microbiology. Answer the three source clinical questions: stain supporting cryptococcal meningitis; causative agent and family when Negri bodies are found; and diagnosis plus blocked neurotransmitter in descending paralysis after home-canned food.",
        "India ink stain supports cryptococcal meningitis. Negri bodies indicate rabies virus of the family Rhabdoviridae. The home-canned-food illness is botulism, in which acetylcholine release is blocked.",
    ),
    (
        "Question V — Pathology. Answer the three source items: characteristic histopathology of the most common cause of dementia; diagnosis of a cerebellar malignant small-round-cell tumor and two other common childhood CNS tumors; and three differences between epidural and subdural intracranial hemorrhage.",
        "The characteristic findings of Alzheimer disease are neuritic plaques, neurofibrillary tangles, and amyloid angiopathy. A malignant small-round-cell cerebellar tumor in a child is a medulloblastoma; other common childhood CNS tumors include pilocytic astrocytoma and ependymoma. Epidural hemorrhage is usually trauma with skull fracture, lies at the trauma site, is arterial, and produces a short lucid interval followed by sudden loss of consciousness. Subdural hemorrhage is usually trauma without fracture due to inertia, lies opposite the trauma site, is venous, and causes delayed loss of consciousness after one to three days or weeks.",
    ),
    (
        "Question VI — Biochemistry. Answer the two source items: enumerate two functions of glucose for the brain other than energy production; and, in the serotonin-depletion case, enumerate the enzymes used in serotonin synthesis and name the product of serotonin degradation by monoamine oxidase.",
        "Glucose contributes to glycogen formation, the structure of important macromolecules such as glycolipids and glycoproteins, and synthesis of neurotransmitters including GABA, glutamate, and acetylcholine; any two are accepted. Serotonin synthesis uses tryptophan hydroxylase, the rate-limiting tetrahydrobiopterin-dependent enzyme converting tryptophan to 5-hydroxytryptophan, followed by aromatic L-amino-acid decarboxylase converting it to serotonin (5-hydroxytryptamine). MAO degradation produces 5-hydroxy-3-indoleacetaldehyde (5-HIAL).",
    ),
    (
        "Question VII — Physiology. Discuss the source items: two differences between slow-wave and paradoxical sleep; three characteristics of theta waves; the cause of the short latency of the stretch reflex; functions of the thalamus and Wernicke area; basal-ganglia control of voluntary saccadic eye movement; two learning and memory processes; three characteristics of cerebellar ataxia; two conditions associated with hypertonia and hyperreflexia; and the two case studies.",
        "Slow-wave sleep occupies about 75–80% of sleep, averages 90 minutes per cycle, begins sleep, has upward-deviated eyes with miosis, and is associated with medullary reticular formation; paradoxical sleep occupies about 20–25%, averages 20 minutes, follows the fourth slow-wave stage, has rapid eye movements, and is associated with pontine reticular formation. Theta waves are large and regular at 4–7 cycles/s with 100–150 microvolts, occur in children, emotional stress, light sleep, frustration, or brain disorders, and are recorded over temporal and parietal regions. Stretch-reflex latency is short because the reflex is monosynaptic and both afferent and efferent fibers conduct rapidly. Thalamic functions include relaying epicritic and crude sensations, visual and auditory pathways, cerebello-thalamo-cortical and basal-ganglia feedback, autonomic, memory and emotional signals, reticular-activating input, and higher cortical functions. Wernicke area receives somatic, visual, and auditory association input; links sensory and motor speech centers; comprehends spoken and written language; selects words for expression; and stores language memories. For saccades, substantia nigra pars reticulata tonically inhibits the superior colliculus; caudate inhibition of the SNr disinhibits the superior colliculus and permits a saccadic movement. Learning and memory processes include encoding, storage, and retrieval; any two are accepted. Cerebellar ataxia includes dysmetria, dysarthria, decomposition of movement, adiadochokinesia, asynergia, kinetic or intention tremor, nystagmus, rebound, and zigzag gait; any three are accepted. Hypertonia and hyperreflexia may occur with excessive facilitatory supraspinal control such as UMN lesions, tetany, or hyperthyroidism; any two are accepted. In Case study 1, presbyopia is an age-related reduction in accommodation and is corrected with convex lenses; aqueous-humor formation and outflow affect intraocular pressure; and scotopic vision uses rods with low acuity and no color, whereas photopic vision uses cones with high acuity and color. In Case study 2, vestibular equilibrium is maintained by lateral vestibulospinal control of antigravity muscles, medial vestibulospinal control of head position, and coordination of eye movements with the head. Auditory transduction uses mechanically gated channels in ciliated hair cells, potassium-rich endolymph, calcium-dependent glutamate release, and altered afferent firing. Interaural intensity differences, useful mainly for sounds above 3000 Hz, compare ipsilateral excitation in the lateral superior olive with contralateral inhibition through the medial nucleus of the trapezoid body.",
    ),
    (
        "Question VIII — Histology. Answer the six source items: structure of the macula; structure of the lens; structure of the blood–CSF barrier; comparison of protoplasmic and fibrous astrocytes by site and cytoplasm; histological structures of the molecular layer of the cerebellar cortex; and taste-bud cell types seen by electron microscopy.",
        "The macula contains sensory hair cells and supporting (sustentacular) cells covered by a thick gelatinous glycoprotein layer bearing calcium-carbonate otoliths. The lens is biconvex, transparent, and elastic; attached to the ciliary body by zonules; surrounded by a homogeneous capsule; covered anteriorly by a single subcapsular cell layer; and composed mainly of transparent crystalline lens fibers. The blood–CSF barrier includes choroidal epithelial cells joined by tight junctions, a basement membrane, and fenestrated endothelial capillaries. Protoplasmic astrocytes are in gray matter with granular cytoplasm and few glial filaments; fibrous astrocytes are in white matter with numerous glial filaments. The molecular cerebellar layer contains granule-cell axons or parallel fibers, Purkinje-cell dendrites, stellate cells, and basket cells; any four are accepted. Taste buds contain glial-like supporting cells (type I), receptor cells (type II), presynaptic cells (type III), and basal cells; any four are accepted.",
    ),
    (
        "Question IX — Parasitology. Answer the following: (1) enumerate two helminthic diseases causing cystic brain lesions; (2) identify the parasite and larval form in a patient with multiple frontal-lobe cysts showing a hole-with-dot appearance; and (3) confirm the diagnosis and appropriate specimen time in a Cameroonian patient with an African eye worm and migratory forearm swelling.",
        "Helminthic diseases causing cystic brain lesions include hydatidosis, cysticercosis, and coenurosis; any two are accepted. Multiple small frontal-lobe cysts with a hole-with-dot appearance indicate neurocysticercosis, caused by Cysticercus cellulosae larvae. Loiasis is confirmed by a thick blood smear stained with Giemsa, collected during daytime, approximately 10 AM to 12 PM, because of diurnal periodicity.",
    ),
]


def main() -> int:
    questions = [
        Question(
            stem=stem,
            options=None,
            correct="-",
            source="key",
            exp=answer,
            tag="Exams, Final 2024",
            year=2024,
        )
        for stem, answer in ITEMS
    ]
    count = write_markdown(
        OUTPUT,
        "Source 03 — CNS Final 2024 model answer",
        {
            "Source file": "Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/CNS FINAL 2024.pdf",
            "Type": "Assiut final examination model answer, nine written questions",
            "Pages": 9,
            "Declared questions": 9,
            "Answer source": "key:9 (model answers printed in source)",
            "Tag": "Exams, Final 2024",
            "Year": 2024,
            "Note": "Top-level exam numbering is retained; each QROC includes all source subparts and the complete model answer.",
        },
        questions,
    )
    print(f"wrote {count}; QROC={count}; key={count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
