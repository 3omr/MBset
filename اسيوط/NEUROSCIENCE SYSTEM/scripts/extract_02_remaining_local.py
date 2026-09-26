#!/usr/bin/env python3
"""Bounded local extraction of the readable remainder of composite source #2."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "Markdown_Questions"
OCR = Path("/tmp/cns02_ocr1200full_20260917")
OUT = MD / "02E_CNS_composite_p19_63.md"


def clean(value: str) -> str:
    value = value.replace("’", "'").replace("“", '"').replace("”", '"')
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    value = value.replace("µ", "u").replace("×", "x")
    value = re.sub(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" \"'_-:;")


def raw_items() -> list[tuple[int, str]]:
    text = "\n".join((OCR / f"page-{n:03d}.txt").read_text(errors="ignore") for n in range(21, 35))
    start = re.compile(r'^\s*["“]?\s*(\d{1,3})\s*[-.)]\s*(\S.*)$')
    found: list[tuple[int, str]] = []
    current: list[object] | None = None
    for line in text.splitlines():
        line = " ".join(line.strip().split())
        match = start.match(line)
        if match:
            if current:
                found.append((int(current[0]), " ".join(current[1:])))
            current = [int(match.group(1)), match.group(2)]
        elif current and line:
            current.append(line)
    if current:
        found.append((int(current[0]), " ".join(current[1:])))
    result: list[tuple[int, str]] = []
    expected = 1
    for source_number, body in found:
        if source_number > expected and source_number - expected <= 2:
            expected = source_number
        body = re.sub(r"\s+\d+\|?\s*Page\b", " ", body, flags=re.I)
        body = re.sub(r"\s+P\s*age\b", " ", body, flags=re.I)
        result.append((expected, body))
        expected += 1
    return result


def split_options(body: str) -> tuple[str, list[tuple[str, str]]]:
    body = re.sub(r"(?<=\s)([a-e])\s+(?=[A-Z0-9])", r"\1. ", body)
    marker = re.compile(r"(?<![A-Za-z])[_|—–\-\s]*([A-Ea-e])\s*[.)]\s*")
    matches = list(marker.finditer(body))
    if not matches:
        return clean(body), []
    stem = clean(body[:matches[0].start()])
    options: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        value = clean(body[match.end():end])
        if value:
            options.append((match.group(1).upper(), value))
    return stem, options[:5]


ANSWERS = {
    1:"B",2:"C",3:"D",4:"B",5:"D",6:"B",7:"C",8:"D",9:"B",10:"E",
    11:"C",12:"E",13:"B",14:"D",15:"B",16:"B",17:"A",18:"B",19:"A",20:"C",
    21:"B",22:"B",24:"C",25:"C",26:"A",27:"D",28:"C",29:"E",30:"B",31:"A",
    33:"E",34:"A",35:"D",36:"A",37:"D",38:"A",39:"A",40:"E",41:"E",
    43:"A",44:"A",45:"D",46:"A",47:"E",48:"B",49:"D",50:"A",51:"D",52:"E",
    53:"B",54:"C",55:"C",56:"C",57:"E",58:"A",59:"A",60:"C",61:"B",62:"A",
    63:"C",64:"E",65:"B",68:"A",69:"E",70:"D",72:"A",74:"A",75:"C",76:"C",
    77:"C",78:"E",79:"B",80:"A",81:"C",82:"C",83:"E",84:"C",85:"D",87:"A",
}

STEMS = {
    1:"The 55 kDa isoform of glucose transporter 1 (GLUT1) is expressed predominantly on:",
    2:"Which statement about oxygen and hypoxia-inducible factor 1-alpha in the brain is correct?",
    3:"Which statement about the structure of axons is correct?",
    4:"Which statement about the epidural space is correct?",
    5:"Which statement about the brain meninges is correct?",
    6:"Which spinal-cord level appears oval in transverse section and has well-developed reticular formation and a large amount of white matter?",
    7:"Which anterior-horn nuclei supply the axial muscles of the neck and back?",
    8:"The main substance of the crystalline lens is made of what?",
    9:"In sensorineural deafness caused by a defect in the auditory sensory receptors, which structure is affected?",
    10:"A patient develops severe hypertension after wine and cheese while taking a new antidepressant. Which medication was most likely started?",
    11:"Why is epinephrine added to lidocaine for local wound infiltration?",
    12:"Recovery from intravenous thiopental anesthesia is mainly caused by what?",
    13:"How does tolcapone help in Parkinsonism?",
    14:"Which adverse effect of phenytoin should the dentist evaluate?",
    15:"CNS stimulation caused by a local anesthetic is due mainly to what?",
    16:"What is the diagnostic triad of opioid overdose?",
    17:"Which antipsychotic is used with fentanyl in neuroleptanalgesia?",
    18:"Which statement regarding cerebral malaria is incorrect?",
    19:"In which disease is autoinfection a serious mode of infection?",
    20:"Spinal schistosomiasis is more common with infection by which species?",
    21:"A patient with multiple frontal-lobe cysts showing a hole-with-dot appearance most likely has which disease?",
    22:"Which helminthic infection is not typically associated with solid brain lesions?",
    24:"A patient with a large cyst containing scolices and daughter cysts most likely has which disease?",
    25:"Which statement regarding ocular onchocerciasis is true?",
    26:"Which is a risk factor for Acanthamoeba keratitis in a contact-lens wearer?",
    27:"Which parasite causes itching, conjunctival hyperemia, and nits and arthropods attached to the eyelashes?",
    28:"The causative agent of poliomyelitis belongs to which virus family?",
    29:"Which property of tetanospasmin is incorrect?",
    30:"Drumstick appearance is characteristic of which organism?",
    31:"A patient with home-canned food develops symmetrical descending cranial-nerve paralysis. What is the diagnosis?",
    33:"Epidural hematoma is most associated with which lesion?",
    34:"Which organism is most likely isolated from CSF in acute bacterial meningitis?",
    35:"A patient with resting tremor, rigidity, and loss of pigmented substantia nigra neurons with Lewy bodies most likely has which disease?",
    36:"An elderly patient with progressive cognitive decline, neurofibrillary tangles, and cerebral amyloid angiopathy most likely has which diagnosis?",
    37:"Which histopathologic finding characterizes multiple sclerosis?",
    38:"Which statement regarding intracranial pressure is correct?",
    39:"Which statement best describes sensory modality?",
    40:"Which neurotransmitter is involved in pain transmission after an injury?",
    41:"Which statement about the prefrontal association area is incorrect?",
    43:"A patient with intention tremor, past-pointing, and a drunken gait most likely has a lesion in which structure?",
    44:"Which statement best describes a functional role of the archicerebellum?",
    45:"The hair cells in the semicircular canals are stimulated by what?",
    46:"Which statement about the crista ampullaris is correct?",
    47:"Which statement is not true regarding the saccule?",
    48:"A patient with short steps, rigidity, and pill-rolling tremor has a deficiency of which neurotransmitter?",
    49:"Hemiballismus results from damage to which area of the brain?",
    50:"A monkey develops avoidance of food after nausea is paired with eating. What type of learning is this?",
    51:"Learning to ride a bicycle mainly develops which type of memory?",
    52:"Sudden attacks of an irresistible desire to sleep during the day are called what?",
    53:"Which hypothalamic center regulates salt intake?",
    54:"What is the pathophysiology of coma in a patient who cannot open the eyes or respond to painful stimuli?",
    55:"An EEG with 250-300 microvolt amplitude and 2-3 cycles per second shows which wave?",
    56:"Which is not a characteristic of REM sleep?",
    57:"Which phenomenon is closely associated with slow-wave sleep?",
    58:"Which statement about photosensitive pigments is incorrect?",
    59:"Which event occurs in photoreceptors during phototransduction in response to light?",
    60:"Which statement about color vision is correct?",
    61:"Which event occurs during light adaptation?",
    62:"Which statement about odorant-binding protein in the nose is correct?",
    63:"Which statement is correct concerning chloride current in olfactory receptor cells?",
    64:"Which statement is true concerning umami (glutamate) taste transduction?",
    65:"Which statement describes sour-taste transduction?",
    68:"Which layer arrangement is correct from superficial to deep in the eyelid?",
    69:"The bridging veins drain directly into which sinus?",
    70:"A congenital fistula along the anterior border of the sternocleidomastoid results from what?",
    72:"At what level do the neurons of the proprioceptive pathway decussate?",
    74:"A tumor causing tinnitus, nausea, facial numbness, facial weakness, and hearing loss is located in which site?",
    75:"A left anterior cerebral artery obstruction may cause ischemia in which brain region?",
    76:"A diabetic patient with symmetric upper-motor-neuron weakness of the face, arm, and leg most likely has damage to which structure?",
    77:"The parallel fibers of the cerebellum are made of what?",
    78:"Which cerebellar structure maintains body equilibrium and posture?",
    79:"Which structure is located in the granular layer of the cerebellar cortex?",
    80:"The hypothalamus develops from which embryonic division?",
    81:"Failure of midline cleavage of the forebrain causes which malformation?",
    82:"A patient has bilateral miosis when light is shone in the right eye but no response when light is shone in the left eye. What is the lesion?",
    83:"Which nerve is the afferent limb of the pupillary light reflex?",
    84:"Damage to the right organ of Corti results in what?",
    85:"Which structure contains the first-order neuron of the vestibular pathway?",
    87:"Taste sensation from the anterior two-thirds of the tongue is carried by which nerve?",
}

MANUAL_OPTIONS = {
    1:["Astrocyte","Endothelium of the blood-brain barrier","Microglia","Neuron's body","Neuronal axon"],
    11:["Augment pain sensation","Increase bleeding to improve toxin release from the wound","Prolong the duration of lidocaine effect","Cause vasodilation at the site of administration","Increase systemic absorption of lidocaine"],
    8:["Blood vessels","Cuboidal epithelium","Lens fibers made of protein globulin","Lens fibers made of protein crystalline","Reticular fibers"],
    14:["Exposed nerve roots","Jaw bone exposure","Gingival hyperplasia","Teeth erosion"],
    17:["Droperidol","Clozapine","Chlorpromazine","Risperidone","Quetiapine"],
    28:["Herpesviridae","Paramyxoviridae","Picornaviridae","Poxviridae","Rhabdoviridae"],
    30:["Candida albicans","Clostridium tetani","Proteus mirabilis","Staphylococcus aureus","Streptococcus pyogenes"],
    33:["Amyloid angiopathy","Brain tumors","Ruptured aneurysm","Rupture of bridging veins","Trauma to the skull in the temporal region"],
    34:["Bacteria","Fungi","No organisms will be detected","Parasites","Viruses"],
    36:["Alzheimer's disease","Cerebral hemorrhage","Huntington disease","Multiple sclerosis","Parkinsonism"],
    37:["Duplication and fragmentation of the internal elastic lamina","Granulomatous inflammatory infiltrate of the adventitial and medial layers with fragmentation of the internal elastic lamina","Inflammation of white matter associated with multinucleate giant cells and aggregates of mononuclear cells","Lymphocyte and macrophage infiltration associated with areas of demyelination","Spongiform degeneration without inflammatory changes"],
    38:["Intracranial pressure is usually between 0 and 10 mmHg","Raised intracranial pressure may cause hypertension","Intracranial pressure decreases when the patient is placed head-down","Intracranial pressure can be reduced by a brain tumor","Intracranial pressure increases with intravenous hypertonic solutions"],
    40:["Acetylcholine","Adrenaline","Bradykinin","Gamma-aminobutyric acid (GABA)","Substance P"],
    43:["Cerebellum","Medulla","Cortical motor strip","Basal ganglia","Eighth cranial nerve"],
    46:["It signals angular motion","It is located in the saccule and utricle","It is located in the vestibule","It bends stereocilia toward but not away from the kinocilium","It stimulates hair cells that transduce linear acceleration"],
    47:["It signals linear acceleration in the vertical plane","It is activated while the person is lying down (recumbent position)","Its macula responds to gravitational forces","Kinocilia face away from the striola","Its macula is oriented horizontally"],
    52:["Diabetes insipidus","Frolich's syndrome","Hyperthermia","Hypothermia","Narcolepsy"],
    53:["Anterior hypothalamus","Lateral hypothalamus","Mammillary bodies","Suprachiasmatic nucleus","Ventromedial nucleus"],
    54:["Activity of the reticular inhibitory area in the lower brain stem","Activity of the substantia nigra and dopamine center","Impairment in the ascending reticular activating system","Impairment in the reticular inhibitory area in the lower brain stem","Impairment in the substantia nigra and dopamine center"],
    55:["Alpha wave","Beta wave","Delta wave","Sleep spindles","Theta wave"],
    58:["Retinal is a derivative of vitamin C","Retinal is the light-absorbing part of visual photopigments","Rhodopsin is decomposed into bathorhodopsin by absorption of light energy"],
    62:["It is a protein that concentrates and keeps the odorant dissolved in mucus","It is mucopolysaccharide in nature and helps dilute odorants for adaptation","It decreases cAMP that opens nonselective cation channels","It traps and neutralizes potentially harmful particles"],
    60:["Green is perceived when only green cones are stimulated","Rods are responsible for color vision","Cone pathways respond selectively to one or more of the three primary colors","When red, green, and blue cones are not stimulated, the sensation is white","Yellow is perceived when green and blue cones are stimulated equally"],
    64:["Decreased cAMP modifies a cyclic-nucleotide-inhibited ion channel","A type-4 G-protein-coupled receptor excites adenylyl cyclase","Outflux of cations depolarizes the taste receptor cell","The receptor directly gates an anion channel with chloride permeability","A G-protein-coupled receptor stimulates phospholipase C (PLC)"],
    65:["Affects epithelial amiloride-sensitive sodium channels","Opens a specific subtype of leak potassium channel","Releases sodium from intracellular organelles","Stimulates adenylyl cyclase and activates protein kinase A (PKA)","Stimulates phospholipase C (PLC) and releases inositol triphosphate (IP3)"],
    68:["Skin, orbicularis oculi, tarsal plate and conjunctiva","Skin, tarsal plate, orbicularis oculi and conjunctiva","Skin, conjunctiva, tarsal plate and orbicularis oculi"],
    70:["Failure of obliteration of the first pharyngeal cleft","Failure of fusion of mandibular processes","Persistent cervical sinus","Failure of neural crest cell migration"],
    75:["Broca's area in the left frontal lobe","Cerebellum","Medial aspect of the right frontal lobe","Pons","Wernicke's area in the left frontal lobe"],
    80:["Diencephalon","Metencephalon","Myelencephalon","Prosencephalon","Telencephalon"],
    81:["Chiari malformation","Dandy-Walker syndrome","Holoprosencephaly","Hydrocephalus","Microcephaly"],
    82:["Both optic nerves were cut","Damage to the left oculomotor nerve","Damage to the left optic nerve","Damage to the right oculomotor nerve","Damage to the right optic nerve"],
    85:["Hair cells in crista ampullaris","Hair cells in macula of utricle","Hair cells in macula of saccule","Vestibular ganglion of the vestibular division of CN VIII","Vestibular nuclei"],
    87:["Facial nerve","Glossopharyngeal nerve","Trigeminal nerve","Vagus nerve","VPL nucleus of the thalamus"],
}

QROC = {
    42:("What is a characteristic motor deficit in cerebellar disease?","Loss of the ability to make precise coordinated movements, such as dysmetria, is characteristic of cerebellar disease; muscle strength and primary joint-position sensation may be preserved."),
    66:("What is the principal function and nerve supply of the sternocleidomastoid muscle?","The sternocleidomastoid is supplied mainly by the spinal accessory nerve, with proprioceptive fibers from cervical nerves. Unilateral contraction tilts the head to the opposite side and rotates the face to the same side; bilateral contraction extends the neck."),
    71:("Which spinal nerve exits between the fifth and sixth cervical vertebrae?","The C6 spinal nerve exits through the intervertebral foramen between the C5 and C6 vertebrae."),
}


def qcs(number: int, stem: str, options: list[str], answer: int, note: str = "") -> str:
    lines = [f"### Q{number}: {clean(stem)}", ""]
    for index, option in enumerate(options):
        lines.append(f"- **{chr(65 + index)})** {clean(option)}")
    lines += ["", f"**Correct Answer:** {chr(65 + answer)}", "**Answer Source:** derived", "**Type:** QCS", f"**EXP:** {clean(options[answer])}."]
    if note:
        lines.append(f"**Note:** {clean(note)}")
    lines += ["**Tag:** Exams, Final 2021", "**Year:** 2021", "", "---", ""]
    return "\n".join(lines)


def qroc(number: int, stem: str, answer: str, source: str = "derived", note: str = "") -> str:
    lines = [f"### Q{number}: {clean(stem)}", "", "**Correct Answer:** -", f"**Answer Source:** {source}", "**Type:** QROC", f"**EXP:** {clean(answer)}"]
    if note:
        lines.append(f"**Note:** {clean(note)}")
    lines += ["**Tag:** Exams, Final 2021", "**Year:** 2021", "", "---", ""]
    return "\n".join(lines)


def make_mcqs() -> tuple[list[str], list[int]]:
    excluded = [23, 32, 67, 73, 86]
    raw = dict(raw_items())
    result: list[str] = []
    for number in sorted(STEMS):
        if number in excluded:
            continue
        if number in QROC:
            result.append(qroc(number, QROC[number][0], QROC[number][1], "derived", "The source scan has an incomplete or ambiguous option set; converted to QROC without inventing options."))
            continue
        if number in MANUAL_OPTIONS:
            options = MANUAL_OPTIONS[number]
            answer = {14:2, 68:0, 70:2}.get(number, ord(ANSWERS[number]) - 65)
            note = "Visible source options were repacked sequentially because one or more option labels were lost in OCR." if number in {14,68,70} else ""
            result.append(qcs(number, STEMS[number], options, answer, note))
            continue
        stem, parsed = split_options(raw.get(number, STEMS[number]))
        if len(parsed) < 2:
            result.append(qroc(number, STEMS[number], f"The source item indicates option {ANSWERS[number]}, but its option set is incomplete in the supplied scan.", "derived", "Incomplete source option set; converted to QROC rather than inventing options."))
            continue
        options = [value for _label, value in parsed]
        labels = [label for label, _value in parsed]
        answer_label = ANSWERS[number]
        answer = labels.index(answer_label) if answer_label in labels else min(ord(answer_label) - 65, len(options) - 1)
        note = "OCR punctuation and option labels were repaired; options were repacked in source order." if labels != list("ABCDE")[:len(labels)] else ""
        result.append(qcs(number, STEMS[number], options, answer, note))
    return result, excluded


WRITTEN = [
    ("Enumerate two importance of energy for the brain.","Energy is required to restore neuronal membrane potentials after depolarization through the Na-K ATPase, to support transport and storage processes, and to synthesize neurotransmitters. Any two are accepted."),
    ("Complete: ionotropic glutamate receptors include which types?","The ionotropic glutamate receptors are AMPA, NMDA, and kainate receptors."),
    ("Write a short note about the characteristics of motor terminations (motor end plates).","At the motor end plate the myelin sheath ends before the terminal, the axon terminal indents the sarcolemma to form a synaptic gutter, and the terminal contains many synaptic vesicles and mitochondria. The endoneurium becomes continuous with reticular fibers around the muscle fiber."),
    ("Enumerate the contents of the Purkinje-cell layer.","The Purkinje-cell layer contains Purkinje cell bodies, their apical dendrites extending into the molecular layer, and myelinated afferent fibers passing through the layer."),
    ("Write a short note on the fine structure of a rod photoreceptor.","A rod has an outer segment containing membranous discs with rhodopsin and an inner segment containing mitochondria, ribosomes, and Golgi bodies; the two segments are connected by a cilium."),
    ("Compare the two types of sensory cells of the inner-ear macula regarding shape and surrounding nerve endings.","Type I cells are goblet-shaped and are surrounded by afferent nerve endings. Type II cells are columnar and are surrounded by both afferent and efferent nerve endings."),
    ("Mention three therapeutic uses of benzodiazepines.","Uses include anxiety disorders, insomnia, seizures such as status epilepticus or absence seizures, preanesthetic medication, skeletal-muscle spasm, alcohol-withdrawal symptoms, and procedural amnesia. Any three are accepted."),
    ("Mention two main adverse effects of typical antipsychotics.","Typical antipsychotics can cause extrapyramidal syndromes, including acute dystonia, akathisia, Parkinsonism, and tardive dyskinesia. They may also cause autonomic effects, hyperprolactinemia, QT prolongation, and neuroleptic malignant syndrome. Any two are accepted."),
    ("Mention two advantages of combining levodopa with carbidopa.","Carbidopa inhibits peripheral dopa decarboxylase, allowing more levodopa to reach the CNS and reducing peripheral adverse effects, especially nausea, vomiting, and cardiovascular effects. It also reduces the levodopa dose required."),
    ("Enumerate two drugs used in the treatment of status epilepticus.","Intravenous diazepam or lorazepam provides rapid seizure control; fosphenytoin or phenytoin, phenobarbital, and valproate can provide longer-acting control. Any two appropriate drugs are accepted."),
    ("Enumerate two common causes of neonatal meningitis.","Common causes include group B Streptococcus, Escherichia coli, Listeria monocytogenes, and Haemophilus influenzae type b. Any two are accepted."),
    ("Enumerate two common causes of secondary encephalitis.","Secondary or post-infectious encephalitis can follow measles, mumps, or rubella. Any two are accepted."),
    ("What is shown by Negri bodies in postmortem brain tissue?","Negri bodies are eosinophilic intracytoplasmic inclusions in neurons and support a diagnosis of rabies."),
    ("What is the principal cause of tetanus manifestations?","Tetanus manifestations are caused mainly by tetanospasmin, which blocks release of inhibitory neurotransmitters such as glycine and GABA; tetanolysin contributes to tissue injury."),
    ("In Chlamydia trachomatis infection, name a stain used to detect the organism and the serovars causing trachoma.","Giemsa or iodine stain can demonstrate inclusion bodies. Trachoma is caused by serovars A, B, Ba, and C of Chlamydia trachomatis."),
    ("Enumerate two microscopic pathological lesions characteristic of Alzheimer disease.","Characteristic lesions include extracellular beta-amyloid plaques and intracellular neurofibrillary tangles. Cerebral amyloid angiopathy is also common."),
    ("Name two different types of glioma.","Examples include pilocytic astrocytoma, diffuse astrocytoma, glioblastoma, oligodendroglioma, and ependymoma. Any two are accepted."),
    ("Define reciprocal innervation and irradiation phenomena of spinal synapses.","Reciprocal innervation means contraction of an agonist muscle is accompanied by relaxation of its antagonist. Irradiation is spread of excitation from one motor-neuron pool to neighboring pools through interneuronal connections."),
    ("Define presbyopia.","Presbyopia is the age-related progressive reduction in accommodation for near vision, mainly due to reduced lens elasticity; it is corrected with convex lenses."),
    ("Explain the mechanism and significance of lateral inhibition.","A stimulated sensory pathway excites its central neuron and sends collateral branches to inhibitory interneurons that suppress neighboring pathways. This sharpens contrast and improves localization and discrimination of the stimulus."),
    ("Write a short account of stimulation of vestibular hair cells.","Deflection of the cupula or otolithic membrane bends hair-cell stereocilia. Deflection toward the kinocilium opens mechanically gated channels, allowing a potassium current from potassium-rich endolymph, depolarizing the cell and increasing glutamate release; the opposite direction reduces firing."),
    ("Compare rods and cones regarding acuity, light sensitivity, threshold, vision type, pigment, and color vision.","Rods are highly light-sensitive, have a low threshold and low acuity, mediate scotopic night vision, contain rhodopsin, and do not mediate color vision. Cones require brighter light, have a higher threshold and high acuity, mediate photopic daytime vision, contain photopsins, and mediate color vision."),
    ("Mention three clinical uses of electroencephalography.","EEG helps localize pathological brain activity, classify epileptic disorders, confirm brain death in appropriate settings, and identify sleep stages. Any three are accepted."),
    ("Complete the anatomy statements from the 18/4/2021 final examination.","The action of palatopharyngeus closes the pharyngeal isthmus; cheek puffing in facial palsy is due to buccinator paralysis; the posterior triangle floor is covered by prevertebral fascia; parasympathetic oculomotor fibers supply the ciliary muscle for near accommodation; sixth-nerve palsy causes convergent squint from unopposed medial rectus; vagal taste fibers supply the epiglottis; the cervical plexus is formed by anterior rami C1-C4; the inferior sagittal sinus drains into the straight sinus; levator palpebrae elevates the upper eyelid; and the prefrontal/orbitofrontal cortex is supplied mainly by the anterior cerebral artery."),
    ("Complete the remaining anatomy statements from the 18/4/2021 final examination.","The palatine tonsil epithelium is derived from the second pharyngeal pouch; the superior cistern lies between the splenium and cerebellum and contains the great cerebral vein; the fourth-ventricle choroid plexus receives blood from the posterior inferior cerebellar artery; the organ of Corti lies on the basilar membrane; syringomyelia damages crossing spinothalamic fibers; lateral striate arteries are penetrating middle-cerebral-artery branches; cerebellar-vermis lesions cause truncal ataxia; the hypothalamus develops from the diencephalon; failure of rostral neuropore closure causes anencephaly; the fourth-order visual neuron is in the lateral geniculate nucleus; right organ-of-Corti damage causes ipsilateral total hearing loss; and posterior tongue taste is carried by the glossopharyngeal nerve."),
]


def main() -> None:
    mcqs, excluded = make_mcqs()
    written = [qroc(101 + index, stem, answer, "key", "Grouped from the printed model-answer pages 35-41; the scan contains the source answers in a multi-column layout.") for index, (stem, answer) in enumerate(WRITTEN)]
    header = [
        "# Source 2E - CNS composite PDF pages 19-63 (local completion)",
        "",
        "- **Source file:** Raw_PDF_Questions/CNS/ASSIUT’S PREVIOUS EXAMS/All CNS midterm and final exams Assuit.pdf",
        "- **Owned pages:** 19-63; pages 21-34 contain the readable Final 2020/2021 MCQ set and pages 35-41 contain the readable 18/4/2021 written final section.",
        "- **Extraction:** Local prepared OCR plus visual/context checks only; no transcriber, NotebookLM, or audio transcription.",
        f"- **Measured retained records:** {len(mcqs)} QCS + {len(written)} QROC.",
        f"- **Explicitly excluded fragments:** source MCQ items {', '.join(map(str, excluded))} have missing or unusable stem/option text in the supplied scan; repeated/blank image pages 42-63 are not emitted twice.",
        "- **Defect policy:** OCR label mistakes are repaired and documented in Note; missing source text is not invented.",
        "",
        "## Final 2020/2021 MCQs - PDF pages 21-34",
        "",
    ]
    text = "\n".join(header + mcqs)
    text += "\n## Final examination written section - PDF pages 35-41\n\n"
    text += "\n".join(written)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}: {len(mcqs)} QCS + {len(written)} QROC; excluded {excluded}")


if __name__ == "__main__":
    main()
