#!/usr/bin/env python3
"""Curate the 48-item CNS Physiology Part II question bank.

The scan has no dependable answer-key page.  All answers are therefore marked
``derived`` and remain traceable to the source question and lecturer heading.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "25_Qs_bank_2.md"

ITEMS = [
    ("All of the following are correct concerning chemical synapses in the central nervous system EXCEPT:", [
        "They play an important role in processing information", "They are the junctional areas between two neurons",
        "They allow unidirectional transport of nerve impulses", "Synaptic knobs end by communication only with the body of postsynaptic neurons"], "D"),
    ("All the following are TRUE concerning excitatory postsynaptic potentials (EPSPs) EXCEPT:", [
        "Are depolarizing response in the postsynaptic membrane", "Have a latency of about 0.5 msec",
        "Are produced by sodium influx", "Are associated with decreased excitability of the neuron to other stimuli"], "D"),
    ("Concerning chemical synaptic transmission, all are true EXCEPT:", [
        "It is one-way conduction", "It is fatigued by repeated stimulation", "It is increased by acidosis", "It is decreased by hypoxia"], "C"),
    ("Motor tetanus:", [
        "Has a longer latent period than reflex tetanus", "Results from stimulation of afferent nerve",
        "Shows the phenomenon of after-discharge", "Is characterized by rapid rise of tension to the maximum"], "C"),
    ("Concerning Renshaw cells, all are true EXCEPT:", [
        "Its axon releases acetylcholine to inhibit anterior horn cells", "It is an inhibitory interneuron in the ventral horn of the spinal cord",
        "It inhibits over-excitation of anterior horn cells", "It has a role in sharpening motor activity"], "A"),
    ("Inhibitory postsynaptic potential (IPSP) is due to:", ["Cl- influx", "K+ influx", "Na+ influx", "Ca2+ influx"], "A"),
    ("Concerning synaptic transmission:", [
        "Can be suppressed by alkalosis", "Spatial summation occurs when an input fibre is repetitively stimulated",
        "Synaptic sensitization occurs upon repeated application of a benign stimulus",
        "Postsynaptic inhibition is caused by increased permeability of postsynaptic neuron to Cl-"], "D"),
    ("Long-term potentiation as a supplement of CNS learning resulting in long-lasting enhancement of synaptic transmission following persistent synaptic stimulation in the hippocampus:", ["True", "False"], "A"),
    ("Ionotropic receptors: binding of neurotransmitter opens ionic channels that create a current which can cause depolarization in the postsynaptic cell; fast changes in membrane potential; effects are produced directly:", ["True", "False"], "A"),
    ("Long-term potentiation (LTP) results in long-lasting enhancement of synaptic transmission following intense brief tetanic stimulation:", ["True", "False"], "A"),
    ("Excitatory postsynaptic potential (EPSP) is hyperpolarization of the cell as a result of a stimulus that drives the membrane potential away from threshold potential:", ["True", "False"], "B"),
    ("At a neuromuscular junction, after the action potential occurs, acetylcholine binds to receptors on the postsynaptic muscle membrane and causes sodium and potassium channels to open:", ["True", "False"], "A"),
    ("Inhibitory postsynaptic potential (IPSP) permeability is the ability to change the functional properties and strength of synapses over time:", ["True", "False"], "B"),
    ("Sensitization is prolonged enhancement of a reflex response to a stimulus that is novel or noxious:", ["True", "False"], "A"),
    ("Temporal summation is the ability of a neuron to summate several EPSPs or IPSPs occurring within a short period of time due to repetitive firing of a single presynaptic terminal:", ["True", "False"], "A"),
    ("Electrical synapse:", [
        "Current flows instantaneously directly between two neighboring neuron cells via low-resistance gap junctions",
        "Decrease in amplitude of PSPs in response to repeated action potentials",
        "Binding of neurotransmitter opens ionic channels that cause fast depolarization in the postsynaptic cell",
        "Current flow stimulates calcium influx into the presynaptic cell and release of neurotransmitter into the synaptic cleft"], "A"),
    ("Which of the following sentences is correct regarding change in the permeability of the synaptic membrane and the postsynaptic potential (IPSP)?", [
        "It is produced by increased permeability of calcium", "It is produced by increased permeability of sodium",
        "It is produced by increased permeability of potassium", "It is produced by increased permeability of chloride"], "D"),
    ("GABA or glycine:", [
        "Postsynaptic response to the release of a quantum", "Graded change in the resting membrane potential",
        "Common neurotransmitters in IPSPs", "Graded depolarizations in the motor neurons"], "C"),
    ("Spatial summation is:", [
        "Summation of EPSPs from several different presynaptic terminals firing simultaneously",
        "Repetitive firing of a single presynaptic neuron that leads to the postsynaptic neuron reaching threshold",
        "Depolarization of the axon terminal of the motor neuron by action potential",
        "Activity of a G-protein-coupled receptor in the postsynaptic membrane by norepinephrine"], "A"),
    ("Long-term potentiation (LTP) is a:", [
        "Decrease in amplitude of PSPs in response to repeated action potentials",
        "Increase in amplitude of PSPs in response to repeated action potentials",
        "Long-lasting enhancement of synaptic transmission following intense stimulation (tetanic)",
        "Postsynaptic response to the release of a quantum"], "C"),
    ("Temporal summation:", [
        "Continuous firing of a single presynaptic neuron that leads to the postsynaptic neuron reaching threshold and firing an action potential",
        "Influx of calcium in the presynaptic cell stimulates vesicle fusion and release of acetylcholine",
        "Excitatory potentials from many different presynaptic neurons cause the postsynaptic neuron to reach threshold",
        "Area on the presynaptic membrane where synaptic vesicles bind to release their neurotransmitter"], "A"),
    ("Graded change in the resting membrane potential is a synaptic potential:", ["True", "False"], "A"),
    ("The amount of neurotransmitter released from presynaptic neuronal terminals is directly proportional to the degree of depolarization and the amount of calcium influx:", ["True", "False"], "A"),
    ("Which of the following is correct concerning a chemical synapse?", [
        "Vesicles filled with neurotransmitter are found in the postsynaptic cell",
        "Most neurotransmitter receptors are found in the presynaptic membrane",
        "Influx of calcium in the presynaptic cell inhibits release into the synaptic cleft",
        "Influx of calcium into the presynaptic cell excites release"], "D"),
    ("As you record neuronal activity and observe multiple EPSPs and IPSPs of various sizes mixed together, this is an example of:", [
        "Probably temporal summation only", "Probably spatial summation only", "Probably algebraic summation only",
        "Probably both spatial and temporal summation"], "D"),
    ("Which of the following statements correctly describes an inhibitory postsynaptic potential (IPSP)?", [
        "They are hyperpolarizing the postsynaptic cell", "They drive the membrane potential towards threshold potential",
        "They drive the membrane potential away from zero", "They are depolarizing change of the postsynaptic neuron"], "A"),
    ("Which of the following is TRUE concerning electrical synapses?", [
        "Transmission of information is unidirectional", "Chemical transmitter is needed", "Transmission is fast through gap junctions", "Synaptic cleft is wide"], "C"),
    ("Which of the following is TRUE concerning neuronal habituation?", [
        "It is an increase in amplitude of postsynaptic potentials in response to repeated stimulation",
        "It is due to sensory adaptation or motor fatigue", "It is prolonged enhancement of a response to a novel or noxious stimulus",
        "It is the decrease of a response to a stimulus after repeated presentations"], "D"),
    ("Inhibitory postsynaptic potentials result from an increase in chloride permeability rather than sodium and potassium permeability:", ["True", "False"], "A"),
    ("Inhibitory postsynaptic potentials are caused by:", ["Influx of calcium into postsynaptic membrane", "Influx of sodium into postsynaptic membrane", "Influx of potassium into postsynaptic membrane", "Influx of chloride into postsynaptic membrane"], "D"),
    ("Glycine:", ["Blocks the AMPA/kainate receptors", "Causes hyperpolarization of postsynaptic membrane", "Causes depolarization of postsynaptic membrane", "Blocks NMDA receptors"], "B"),
    ("Which of the following is CORRECT concerning IPSPs?", ["It is due to increased calcium conductance", "It is due to increased sodium conductance", "It is due to increased chloride or potassium conductance", "It is due to increased sodium and calcium conductance"], "C"),
    ("Which of the following sentences is CORRECT regarding neural sensitization?", [
        "It results from sensory adaptation or motor fatigue", "It is decreased responses to a stimulus after repeated presentation",
        "It is learned behavior to stop responding to a stimulus that is no longer biologically relevant",
        "It is prolonged enhancement of a response to a stimulus that is novel or noxious"], "D"),
    ("Temporal summation is the ability to summate several EPSPs or IPSPs due to successive firing from a single presynaptic terminal within a short period of time:", ["True", "False"], "A"),
    ("Synaptic potential is a graded change in the potential of the postsynaptic membrane that may bring the membrane nearer or away from the threshold of action potential initiation:", ["True", "False"], "A"),
    ("Long-term potentiation (LTP):", ["Is caused by activation of glycine receptors", "Is caused by activation of GABAA receptors", "Is caused by activation of NMDA receptors", "Is caused by activation of GABAB receptors"], "C"),
    ("SNARE mechanism for neurotransmitter release includes all of the following EXCEPT:", [
        "Mobilization of vesicles from storage site to release site", "Binding of neurotransmitter with its receptor on the postsynaptic membrane",
        "Docking of vesicles at the active zone", "Fusion of vesicle membrane and target membrane"], "B"),
    ("Spatial summation is summation of several EPSPs or IPSPs or both that are:", [
        "Applied simultaneously from a single neuronal terminal", "Applied successively within a short period of time",
        "Applied simultaneously from several neuronal terminals", "Applied repeatedly from a single neuronal terminal"], "C"),
    ("Chemical synapses:", ["Are rare in the central nervous system", "Allow unidirectional flow of information", "Allow coordination of response in groups of neurons", "Are faster than electrical synapses"], "B"),
    ("Which of the following is correct concerning the GABAA neurotransmitter receptor?", [
        "It causes conductance increase of EPSPs", "It causes conductance increase of IPSPs",
        "It causes conductance decrease of EPSPs", "It causes conductance decrease of IPSPs"], "B"),
    ("Which of the following is TRUE concerning cerebellar long-term depression (LTD)?", [
        "It results from simultaneous firing of the climbing and parallel fibers", "It results from simultaneous firing of the climbing fiber only",
        "It results from simultaneous firing of the parallel fiber only", "It results from successive firing of the climbing and parallel fibers"], "A"),
    ("Synaptic facilitation is:", [
        "Decrease in amplitude of PSPs in response to repeated action potentials",
        "Increase in amplitude of PSPs in response to repeated action potentials",
        "An abrupt change in the resting membrane potential", "Caused by potassium efflux"], "B"),
    ("Which of the following is correct concerning electrical synapses?", [
        "They need chemical transmitter", "They are frequently seen in the CNS", "They allow coordinated firing of a group of neurons", "They connect pyramidal neurons in the neocortex"], "C"),
    ("A graded change in the resting membrane potential is an excitatory postsynaptic potential (EPSP):", ["True", "False"], "A"),
    ("Purkinje cells are the most common types of neurons in the cerebral cortex:", ["True", "False"], "B"),
    ("Influx of calcium in the presynaptic cell stimulates vesicle fusion to the presynaptic membrane and release of acetylcholine into the synaptic cleft:", ["True", "False"], "A"),
    ("Aspartate is the neurotransmitter of climbing fibers of the cerebellum:", ["True", "False"], "B"),
    ("Metabotropic receptors:", ["They are voltage-gated ion channels", "They are ligand-gated ion channels", "They are G-protein-coupled receptors", "They are chemically gated ion channels"], "C"),
]


def main() -> int:
    questions = [
        Question(
            stem=stem,
            options=options,
            correct=answer,
            source="derived",
            exp="No reliable answer key is embedded in this source; answer derived from the corresponding CNS physiology content and requires final spot-check.",
            tag="Department, QBank, Physiology",
            tag_suggere="Physiology",
        )
        for stem, options, answer in ITEMS
    ]
    count = write_markdown(
        OUTPUT,
        "Source 25 — Qs bank (CNS Physiology Part II)",
        {
            "Source file": "Raw_PDF_Questions/CNS/Qs bank.pdf",
            "Type": "Department question bank, CNS Physiology Part II",
            "Pages": 30,
            "Total questions": len(questions),
            "Answer source": f"derived:{len(questions)} (no dependable answer-key page)",
            "Tag": "Department, QBank, Physiology",
            "tagSuggere": "Physiology",
            "Year": "None",
            "Note": "Scan/OCR normalized; true/false statements retained as two-option QCS items.",
        },
        questions,
    )
    print(f"wrote {count}; derived={count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
