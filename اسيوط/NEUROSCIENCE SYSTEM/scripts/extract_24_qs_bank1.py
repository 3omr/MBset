#!/usr/bin/env python3
"""Curate the 56-item CNS Physiology Part I question bank.

This scan has no dependable answer-key page.  The answers below are marked
``derived`` and are based on the lecture content; the source wording and
option order are retained, including the true/false items.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "24_Qs_bank_1.md"

ITEMS = [
    ("Slowly adapting receptors include all the following types, EXCEPT:", [
        "Golgi tendon organs", "Warmth receptors", "Free nerve endings", "Meissner corpuscles"], "D"),
    ("Slowly adapting receptors differ from rapidly adapting receptors in:", [
        "Stopping to discharge after a relatively longer period of constant stimulation",
        "Detecting the dynamic properties of stimuli", "Detecting velocity of stimuli",
        "Generating receptor potentials as long as stimulus is applied"], "D"),
    ("Detection of the stimulus modality depends upon:", [
        "The location of the receptors in the body", "The magnitude of the stimulus",
        "The anatomical connections between the receptors and specific sensory areas in the cerebral cortex",
        "The magnitude of the receptor potential"], "C"),
    ("Touch receptors:", [
        "Are found only in the skin", "Are all encapsulated receptors", "Include two-element receptors",
        "Are stimulated by heat"], "C"),
    ("Tactile receptors include all the following receptors, EXCEPT:", [
        "Organ of Corti", "Hair follicle receptors", "Hair cell receptors", "Ruffini nerve endings"], "A"),
    ("Fine touch:", [
        "Is detected by slowly adapting touch receptors", "Is transmitted by the spinothalamic tract",
        "Is characterized by its emotional affect", "Is not involved in feeling the texture of touched objects"], "A"),
    ("A more developed two-point tactile discrimination:", [
        "Indicates a greater threshold distance for feeling of two points of touch applied simultaneously",
        "Is seen in the proximal regions of the body compared with the distal regions",
        "Is inversely related to the size of the receptive fields of the stimulated sensory units",
        "Depends upon the type of the involved touch receptor"], "C"),
    ("Proprioceptors include all the following types of receptors, EXCEPT:", [
        "Muscle spindles", "Pressure receptors", "Baroreceptors", "Joint receptors"], "C"),
    ("Proprioceptive sensations are transmitted by all the following pathways, EXCEPT:", [
        "Spinothalamic tracts", "Spinocerebellar tract", "Gracile tract", "Cuneocerebellar tract"], "A"),
    ("Reaction to pain includes all the following, EXCEPT:", [
        "Increased heart rate", "Depression", "Withdrawal reflexes",
        "Stoppage of impulse discharge from nociceptors in chronic painful conditions"], "D"),
    ("Pain receptors:", [
        "Become more sensitive with prolonged stimulation", "Are directly stimulated by prostaglandins",
        "Are more numerous in viscera than other tissues", "Include different morphological types"], "A"),
    ("Fast pain differs from slow pain in:", [
        "Being transmitted in the dorsal column pathway", "Evoking a depressor autonomic reaction",
        "Having a sharp quality", "Arising from encapsulated pain receptors"], "C"),
    ("Which of the following is TRUE concerning the fast component of cutaneous pain?", [
        "It is usually sharp and localized", "It is transmitted by A beta sensory fibers",
        "It is carried by the paleospinothalamic tract", "It has maximal conduction velocity of 2 meters/s"], "A"),
    ("Primary cutaneous hyperalgesia:", [
        "Develops in the normal skin region around the area of flare",
        "Is an abnormal condition in the skin in which painful stimuli become more severe",
        "It is due to divergence at dorsal horn cell", "Is associated with throbbing type of pain"], "B"),
    ("Deep pain shows the following characteristics, EXCEPT:", [
        "Dull aching", "Throbbing", "Evokes flexor reflexes", "Diffuse"], "C"),
    ("Pain produced by muscle spasm results from:", [
        "Mechanical stimulation of pain receptor by muscle spasm",
        "Decreased release of lactic acid from the spastic muscle fibers",
        "Release of compounds from the spastic muscle which increase the threshold for stimulation of pain receptors",
        "Decreased oxygen supply to the muscle"], "D"),
    ("Visceral pain:", [
        "Is more common than the other types of pain", "Arises only from wall of the visceral organs",
        "Is often well localized", "Evokes depressor autonomic reactions"], "D"),
    ("Intracranial headache could result from painful stimuli applied on:", [
        "The dura lining the inner surface of the bones of cranial vault", "The brain tissue",
        "Wall of big intracranial veins", "Arachnoid mater"], "A"),
    ("Pain control system:", [
        "Is activated whenever a painful stimulus is applied to body tissues", "Is never activated naturally",
        "Is activated only by administration of opiate drugs",
        "Is activated naturally under conditions associated with strong emotional excitement"], "D"),
    ("All of the following are descending motor tracts, EXCEPT:", [
        "Rubrospinal tract", "Spinotectal tract", "Reticulospinal tract", "Corticobulbar tract"], "B"),
    ("Which of the following is correct concerning the origin of Rubrospinal tract?", [
        "Pontine reticular formation", "Medullary reticular formation", "Red nucleus", "Inferior olivary nuclei"], "C"),
    ("The reticulospinal tracts:", [
        "Are inhibitory to muscle tone", "Are excitatory to muscle tone",
        "Are either excitatory or inhibitory to muscle tone", "Have effect on muscle tone"], "C"),
    ("Vestibulospinal tracts:", [
        "Adjust the discharge of vestibular receptors", "Adjust muscle tone",
        "Antagonize the effects of rubrospinal tract", "Terminate on the lateral motor neurons in the spinal cord"], "B"),
    ("Tectospinal tract:", [
        "Originate mainly from the inferior colliculus", "Originate mainly from the medial geniculate body",
        "Connected with neocerebellum", "Terminate in the cervical segments of the cord"], "D"),
    ("Representation of the body in the primary motor area:", [
        "Is ipsilateral", "Is upright", "Is disproportionate to the actual anatomical size of the represented region",
        "All the above are correct"], "C"),
    ("The premotor area includes all the following, EXCEPT:", [
        "Broca's area", "Head rotation area", "Supplemental motor area", "Hand skills area"], "C"),
    ("Lower motor neuron lesions cause all the following, EXCEPT:", [
        "Decreased number of transmitter receptors in the denervated muscle",
        "Atrophy of the denervated muscle", "Flaccid paralysis of the denervated muscle",
        "Loss of flexion withdrawal reflex"], "A"),
    ("When compared to normal muscle, the response of the denervated muscle to electrical stimulation shows:", [
        "Decreased chronaxie", "Greater response to faradic stimulation", "Abnormal response to galvanic stimulation",
        "CCC becomes greater than ACC"], "C"),
    ("The most dramatic effects of an UMN lesion occurs with lesions at the level of:", [
        "The primary motor area", "Internal capsule", "Medullary pyramids", "Lateral column of spinal white matter"], "B"),
    ("Motor defects that result from an internal capsular lesion include:", [
        "Paralysis of all skeletal muscles on the opposite side of the body",
        "Paralysis of all skeletal muscles on the same side of the body",
        "Paresis of axial muscles on the same side of the body",
        "Paralysis of the distal muscles on the opposite side of the body"], "D"),
    ("In upper motor neuron (UMN) lesions the response to plantar reflex:", [
        "Becomes exaggerated", "Becomes inhibited", "Becomes modified", "Is absent"], "A"),
    ("In upper motor neuron (UMN) lesions the response of the paralyzed muscles to electrical stimulation is:", [
        "Exaggerated", "Inhibited", "Not changed", "Is absent"], "C"),
    ("Spasticity of the paralyzed muscles in upper motor neuron (UMN) lesions is associated with:", [
        "Inhibition of tendon jerks", "Remarkable wasting of the muscle", "Clonus", "None of the above"], "C"),
    ("Spinal shock is due to:", [
        "Severe pain felt at the site of the lesion", "Severe hypotensive shock",
        "Interruption of the ascending sensory pathways", "Interruption of the descending facilitatory tracts"], "D"),
    ("The stage of spinal shock is characterized by the following EXCEPT:", [
        "Failure of spinal reflexes below the level of the lesion",
        "Loss of sensations from the body below the level of the lesion",
        "Loss of voluntary movement from the body below the level of the lesion",
        "Exaggerated tendon jerks below lesion level"], "D"),
    ("In humans the usual duration of the stage of spinal shock is:", [
        "From 2-6 hours", "From 2-6 days", "From 2-6 weeks", "From 2-6 months"], "C"),
    ("Failure of spinal reflexes during the stage of spinal shock causes:", [
        "Automatic micturition", "Hypotension", "Babinski sign", "Spasticity of the paralyzed muscles"], "B"),
    ("Complete transection of the spinal cord produces all of the following effects, EXCEPT:", [
        "Permanent loss of all sensations mediated by the cord below level of lesion",
        "Permanent loss of voluntary movements by muscles innervated by the cord below level of lesion",
        "Permanent loss of reflexes mediated by the cord below level of lesion",
        "Temporary loss of micturition reflexes"], "C"),
    ("Spinal cord complete transection did not affect arterial blood pressure, when the lesion occurs at the level of:", [
        "Mid-cervical segments", "Upper thoracic segments", "Lower thoracic segments", "Mid-lumbar segments"], "D"),
    ("The earliest spinal reflex that recovers after the stage of spinal shock is:", [
        "The micturition reflex", "The scratch reflex", "The stretch reflex", "The flexor reflex"], "D"),
    ("With recovery of arterial blood pressure following spinal cord transection, the recovered blood pressure tends to:", [
        "Be higher than normal", "Be lower than normal", "Show abnormal oscillations", "Drop progressively"], "B"),
    ("Recovery of micturition reflexes following the stage of shock:", [
        "Is due to recovery of supraspinal facilitation to the micturition center in the sacral segments",
        "Is due to recovery of activity of the micturition center in the sacral segments",
        "Causes retention with overflow", "Causes normal micturition"], "C"),
    ("Failure of the spinal reflexes is manifested by:", [
        "Automatic micturition", "Appearance of Babinski sign",
        "Loss of sensations from regions innervated by the cord below the level of the lesion",
        "Disappearance of the tendon jerks"], "D"),
    ("Brown-Sequard syndrome is characterized by all the following, EXCEPT:", [
        "Loss of vibration sense on the opposite side below level of the lesion",
        "Loss of voluntary movements on the same side below the level of the lesion",
        "Loss of reflex movements on the same side at the level of the lesion",
        "Loss of pain sensation on the opposite side below the level of the lesion"], "A"),
    ("Sensory receptors act as transducers:", ["True", "False"], "A"),
    ("The cold receptors are inactive at 50 degrees C:", ["True", "False"], "A"),
    ("Muscle spindles are considered rapidly adaptive receptors:", ["True", "False"], "B"),
    ("Primary hyperalgesia is excessive sensitivity of pain receptors:", ["True", "False"], "A"),
    ("Visceral pain can be felt in an area away from its source:", ["True", "False"], "A"),
    ("Epicritic sensations can be perceived at the level of the thalamus:", ["True", "False"], "B"),
    ("The postero-ventral nucleus of the thalamus receives the spinal, medial and trigeminal lemnisci:", ["True", "False"], "A"),
    ("In thalamic syndrome, not all sensations are lost:", ["True", "False"], "A"),
    ("In somatic sensory area one, body representations are proportional to the size of each part of the body:", ["True", "False"], "B"),
    ("Lesion in somatic association area results in amorphosynthesis:", ["True", "False"], "A"),
    ("The primary motor area (area 4) and vestibular nucleus are facilitatory to muscle tone:", ["True", "False"], "B"),
    ("Hemisection of the spinal cord leads to loss of pain and temperature sensation on the opposite side below the level of the lesion:", ["True", "False"], "A"),
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
        "Source 24 — Qs bank (CNS Physiology Part I)",
        {
            "Source file": "Raw_PDF_Questions/CNS/Qs bank(1).pdf",
            "Type": "Department question bank, CNS Physiology Part I",
            "Pages": 13,
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
