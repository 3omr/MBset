#!/usr/bin/env python3
"""Curate the mixed departmental question scan (source #26)."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "26_department_Q.md"


def w(stem: str, answer: str, subject: str) -> Question:
    return Question(stem=stem, correct="-", source="key", exp=answer,
                    tag=f"Department, QBank, {subject}", tag_suggere=subject)


def m(stem: str, options: list[str], answer: str, subject: str = "Physiology", source: str = "derived") -> Question:
    return Question(stem=stem, options=options, correct=answer, source=source,
                    exp="Answer transcribed from the marked source or derived from the corresponding MBset course content; the source has no uniform answer-key page.",
                    tag=f"Department, QBank, {subject}", tag_suggere=subject)


ITEMS = [
    # Pages 1–4: mixed source cards.
    m("A patient has weakness of the left arm and leg, loss of fine touch on the left, and loss of pain and temperature on the right after an MVA. This is most consistent with:", ["Complete cord syndrome", "A central cord syndrome", "An anterior spinal cord syndrome", "A left spinal cord hemisection syndrome", "A right spinal cord hemisection syndrome"], "D", "Anatomy"),
    m("A unilateral infarct in the territory of the anterior spinal artery and medial vertebral branches produces inferior alternating hemiplegia. Which cranial nerve is involved?", ["Eighth vestibulocochlear", "Ninth glossopharyngeal", "Tenth vagus", "Eleventh accessory", "Twelfth hypoglossal"], "E", "Anatomy"),
    w("After occlusion of the right anterior cerebral artery, which listed deficit is expected?", "Weakness of the contralateral lower limb is expected. The other listed combinations are not the characteristic deficit of a right anterior cerebral artery infarct.", "Anatomy"),
    m("A hypertensive man has paralysis and complete sensory loss of the left arm, leg, and lower face. The most likely lesion is in:", ["Thalamus", "Medulla oblongata", "Right frontal lobe", "Right internal capsule"], "D", "Anatomy"),
    m("Which of the following agents is an opioid antagonist?", ["Amphetamine", "Naltrexone", "Morphine", "Chlorpromazine", "Disulfiram"], "B", "Pharmacology"),
    m("Which opioid analgesic is used in combination with droperidol in neuroleptanalgesia?", ["Morphine", "Buprenorphine", "Fentanyl", "Naltrexone", "Pentazocine"], "C", "Pharmacology"),
    # Pages 6–23: stretch-reflex question bank.
    m("Which characteristic distinguishes the stretch reflex from other reflexes in humans?", ["It involves multiple interneurons", "It is a polysynaptic reflex", "It is the only monosynaptic reflex in humans", "It is primarily mediated by the brainstem", "It does not involve muscle contraction"], "C"),
    m("What is the primary function of gamma motor neurons?", ["Directly contract extrafusal muscle fibers", "Inhibit muscle spindle activity", "Transmit pain signals from muscle", "Adjust the sensitivity of muscle spindles", "Initiate voluntary movements"], "D"),
    m("What is the main purpose of alpha-gamma coactivation during voluntary movement?", ["Prevent muscle fatigue", "Increase muscle strength", "Inhibit antagonist muscle activity", "Maintain muscle spindle sensitivity during contraction", "Initiate a relaxation response"], "D"),
    m("Which muscle-spindle afferent is most sensitive to the velocity of muscle stretch?", ["Ia fibers", "II fibers", "A fibers", "A-delta fibers", "C fibers"], "A"),
    m("What is the purpose of clenching the teeth and interlocking the fingers before testing the patellar reflex?", ["Keep the patient calm", "Increase muscle tension in the legs", "Enhance the stretch-reflex response", "Assess cognitive function", "Test for upper motor neuron lesions"], "C"),
    m("Which brain region is known to facilitate gamma motor-neuron activity?", ["Vestibular nucleus", "Red nucleus", "Basal ganglia", "Inhibitory reticular formation", "Area 4 of the cerebral cortex"], "B"),
    m("How does anxiety contribute to hyperactive tendon reflexes?", ["By inhibiting alpha motor-neuron activity", "By suppressing muscle-spindle input", "By increasing the threshold for spindle activation", "By increasing gamma motor-neuron activity", "By activating inhibitory reticular formation"], "D"),
    m("Which intrafusal fiber is primarily responsible for the dynamic stretch reflex?", ["Nuclear bag fibers", "Nuclear chain fibers", "Type Ia fibers", "Type II fibers", "Gamma motor neurons"], "A"),
    m("How do muscle spindles contribute to posture and balance?", ["Initiate voluntary movement", "Provide feedback about muscle length and its rate of change", "Inhibit antagonist activity", "Directly contract muscles against gravity", "Transmit pain signals"], "B"),
    m("What happens to the firing rate of muscle-spindle afferents when a muscle is shortened?", ["It increases", "It decreases", "It remains unchanged", "It becomes erratic", "It depends on the velocity of shortening"], "B"),
    m("What effect does activation of gamma motor neurons have on muscle-spindle sensitivity?", ["Decreases sensitivity", "Increases sensitivity", "No effect", "Varies with the type of gamma neuron", "Depends on alpha motor-neuron activity"], "B"),
    m("Which brain region is known to inhibit the stretch reflex?", ["Vestibular nucleus", "Area 4 of the cerebral cortex", "Inhibitory reticular formation", "Cerebellum", "Facilitatory reticular formation"], "C"),
    m("What is the primary aim of the stretch reflex?", ["Initiate voluntary movements", "Prevent muscle fatigue", "Protect muscles from injury", "Maintain posture and muscle length", "Control rhythmic walking movements"], "D"),
    m("What are the two main ways that muscle spindles can be stimulated?", ["Electrical stimulation and acetylcholine release", "Alpha motor-neuron and gamma motor-neuron activation", "Changes in temperature and pH", "Passive muscle stretch and gamma motor-neuron activation", "Contraction of surrounding muscles and relaxation of antagonists"], "D"),
    m("Hyperactive stretch reflexes, clonus, and spasticity are most likely associated with:", ["Lower motor-neuron lesion", "Peripheral neuropathy", "Cerebellar ataxia", "Upper motor-neuron lesion", "Myasthenia gravis"], "D"),
    m("What is the primary role of gamma motor-neuron activation in the stretch reflex?", ["Initiate muscle contraction", "Inhibit muscle contraction", "Maintain muscle-spindle sensitivity", "Activate Golgi tendon organs"], "C", source="marked"),
    m("An anxious student has tense muscles and prominent reflexes. How does anxiety affect the stretch reflex?", ["Suppresses gamma activity", "Enhances descending inhibition", "Increases muscle-spindle sensitivity", "Activates the inverse stretch reflex"], "C", source="marked"),
    m("During deep sleep, how does reduced muscle tone affect the stretch reflex?", ["Increases gamma activity", "Enhances descending facilitation", "Decreases muscle-spindle sensitivity", "Activates Renshaw cells"], "C"),
    m("Hyperactive reflexes, clonus, and spasticity indicate which disorder?", ["Lower motor-neuron lesion", "Peripheral neuropathy", "Cerebellar ataxia", "Upper motor-neuron lesion", "Myasthenia gravis"], "D", source="marked"),
    m("During the patellar reflex, contraction of quadriceps is accompanied by relaxation of hamstrings. Which mechanism is responsible?", ["Alpha-gamma coactivation", "Reciprocal inhibition", "Autogenic inhibition", "Renshaw-cell inhibition"], "B", source="marked"),
    m("Rapid elbow extension stretches the biceps and elicits a strong reflex contraction. Which type of stretch reflex is responsible?", ["Dynamic stretch reflex", "Static stretch reflex", "Golgi tendon reflex", "Flexor reflex"], "A", source="marked"),
    m("A patient has increased resistance to passive stretch that is not velocity-dependent and is present throughout the range. What is the diagnosis?", ["Spasticity", "Rigidity", "Hypotonia", "Myasthenia gravis"], "B", source="marked"),
    m("Which receptors provide awareness of muscle length and position during yoga postures?", ["Golgi tendon organs", "Pacinian corpuscles", "Muscle spindles", "Meissner corpuscles"], "C", source="marked"),
    m("A weightlifter suddenly relaxes back muscles when the load becomes excessive. Which receptors mediate this protective mechanism?", ["Muscle spindles", "Golgi tendon organs", "Free nerve endings", "Pacinian corpuscles"], "B", source="marked"),
    m("Velocity-dependent increased muscle tone in a patient with multiple sclerosis is:", ["Rigidity", "Spasticity", "Dystonia", "Hypotonia"], "B", source="marked"),
    m("Which descending pathway is most likely affected when a brainstem lesion causes profound hypotonia and absent reflexes?", ["Vestibulospinal tract", "Reticulospinal tract", "Rubrospinal tract", "Corticospinal tract"], "B"),
    m("What characteristic of antigravity muscles contributes to fatigue resistance and sustained stretch-reflex activity?", ["Fast-twitch fibers", "Low mitochondrial content", "Abundant blood supply", "High glycogen stores"], "C"),
    m("After prolonged hamstring stretch, sudden relaxation allows a greater range of motion. What is this phenomenon?", ["Stretch reflex", "Load reflex", "Lengthening reaction", "Crossed-extensor reflex"], "C"),
    m("How can understanding the stretch reflex be applied in rehabilitation?", ["Inhibit the stretch reflex and reduce muscle tone", "Enhance the stretch reflex and increase strength", "Activate Golgi tendon organs and promote relaxation", "Stimulate muscle spindles and improve proprioception"], "C"),
    # Pages 24–28: parasitology and microbiology.
    m("Kuru and Creutzfeldt-Jakob disease are thought to be caused by:", ["Slow viruses", "Prions", "Flagellates", "Cell-wall-deficient bacteria", "Environmental toxins"], "B", "Pathology"),
    m("The neurotoxin released by Clostridium tetani is:", ["Tetanolysin", "Bacteriocin", "Cyanotoxin", "Tetanospasmin", "Aflatoxin"], "D", "Microbiology"),
    m("One of the solitary cystic helminthic brain lesions is:", ["Hydatidosis", "Schistosomiasis", "Strongyloidiasis", "Toxocariasis", "Trichinosis"], "A", "Parasitology", source="marked"),
    m("A hole-with-dot appearance in imaging of helminthic CNS disease is seen in:", ["Neurocysticercosis", "Schistosomiasis", "Strongyloidiasis", "Toxocariasis", "Trichinosis"], "A", "Parasitology", source="marked"),
    m("The definitive diagnosis in neurohydatidosis is made by:", ["Finding eggs in urine", "Finding eggs in sputum", "Finding eggs in stool", "Finding encysted larvae in muscle", "Microscopic examination of surgical specimens"], "E", "Parasitology", source="marked"),
    m("Coenurosis occurs due to invasion of which form into brain tissue?", ["Egg of Echinococcus granulosus", "Egg of Taenia multiceps", "Larval stage of Echinococcus granulosus", "Larval stage of Taenia multiceps", "Larval stage of Taenia solium"], "D", "Parasitology", source="marked"),
    m("A farmer has Aspergillus keratitis after a corn-leaf injury. KOH mount should reveal:", ["Yeast cells and pseudohyphae", "Septate hyphae with few chlamydoconidia", "Encapsulated yeast cells", "Septate hyphae with rosettes of conidia", "Septate hyphae bearing conidiophores with terminal vesicles"], "E", "Microbiology"),
    m("A newborn with purulent eye discharge after untreated maternal gonorrhea has which organism on Gram stain?", ["Gram-positive septate hyphae", "Gram-positive budding yeast cells", "Gram-negative extracellular diplococci", "Gram-positive diplococci"], "C", "Microbiology"),
    # Pages 29–43: basal ganglia.
    m("A man has difficulty initiating movements, bradykinesia, and resting tremor. Which basal-ganglia function is most affected?", ["Regulation of muscle tone", "Control of voluntary saccadic eye movements", "Cognitive control of motor-pattern sequences", "Execution of subconscious learned movement patterns"], "D", "Physiology"),
    w("Mention the function of the caudate circuit.", "The caudate circuit provides cognitive control of sequences of movements and control of their timing and scaling.", "Physiology"),
    w("A subthalamic-nucleus lesion causes hemiballismus. Name the damaged circuit and its function.", "The indirect circuit is damaged. It normally inhibits the motor cortex as a brake on the direct circuit and suppresses unwanted movement.", "Physiology"),
    m("A drug that blocks dopamine receptors in the striatum would most likely result in:", ["Chorea", "Bradykinesia", "Hemiballismus", "Athetosis"], "B", "Physiology"),
    w("Name the disease with resting tremor, bradykinesia, and rigidity, and enumerate its three cardinal manifestations.", "Parkinson disease. Its cardinal manifestations are resting tremor, bradykinesia or akinesia, and rigidity. Resting tremor is a 4–6 cycles/second pill-rolling tremor that improves with voluntary movement and increases with emotion; bradykinesia causes difficulty initiating movement, shuffling gait, masked face, and slow monotonous speech; rigidity increases tone in agonists and antagonists and may be lead-pipe or cogwheel.", "Physiology"),
    m("A young woman with Huntington disease has sudden involuntary jerky movements. The likely lesion is in the:", ["Subthalamic nucleus", "Caudate nucleus", "Globus pallidus", "Substantia nigra pars compacta"], "B", "Physiology"),
    m("Athetosis, characterized by slow writhing movements, results from a lesion in the:", ["Subthalamic nucleus", "Caudate nucleus", "Globus pallidus", "Substantia nigra pars reticulata"], "C", "Physiology", source="marked"),
    w("What can impairment in the cognitive loop of the basal ganglia lead to?", "It can impair planning, sequencing, timing, and scaling of complex motor patterns and may produce cognitive or executive dysfunction. The source card has incomplete option text, so the prompt is retained as QROC.", "Physiology"),
    w("What is the primary role of the limbic loop of the basal ganglia?", "It participates in emotional and motivational behavior and links limbic processing to action selection. The source card has incomplete option text, so the prompt is retained as QROC.", "Physiology"),
    m("A lesion in the oculomotor loop of the basal ganglia may cause difficulty with:", ["Controlling limb movements", "Making voluntary saccadic eye movements", "Expressing emotions", "Learning new motor skills"], "B", "Physiology"),
    w("Explain the role of the basal ganglia in eye movement.", "At rest, substantia nigra pars reticulata sends sustained inhibitory input to the superior colliculus. Inhibition from the caudate nucleus inhibits the substantia nigra pars reticulata, disinhibits the superior colliculus, and permits a saccadic eye movement. The frontal eye field and cranial nerves III, IV, and VI complete the circuit.", "Physiology"),
    m("Dopamine released in the striatum:", ["Inhibits the direct pathway and excites the indirect pathway", "Excites the direct pathway and inhibits the indirect pathway", "Has no effect on the indirect pathway", "Is primarily involved in regulating muscle tone"], "B", "Physiology", source="marked"),
    w("Illustrate the functions of dopamine and its receptors in the basal ganglia.", "Dopamine from substantia nigra pars compacta excites the direct pathway through D1 receptors and inhibits the indirect pathway through D2 receptors. Both actions disinhibit the thalamus and facilitate excitation of the motor cortex.", "Physiology"),
    m("The thalamus in basal-ganglia circuits:", ["Inhibits the motor cortex", "Relays information from the basal ganglia to the motor cortex", "Is the primary source of dopamine in the brain", "Is involved in regulating muscle tone"], "B", "Physiology"),
    w("What is the effect of activating the direct pathway of the basal ganglia?", "Activation of the direct pathway inhibits the internal globus pallidus and substantia nigra pars reticulata, disinhibits the thalamus, and facilitates movement. The source card omits one option, so the prompt is retained as QROC.", "Physiology"),
    w("What movement disorder may result from a lesion in the putamen circuit?", "The source card lists resting tremor and rigidity, chorea, and hemiballismus. A putamen-related circuit lesion can produce abnormal involuntary movement; the exact option is not fully legible in the scan, so the prompt is retained as QROC.", "Physiology"),
    w("A patient cannot perform familiar learned movements such as brushing teeth or buttoning a shirt despite normal strength and sensation. Which area is likely affected and what is the condition called?", "Disruption of the motor-pattern or cognitive basal-ganglia loop can cause apraxia, an inability to perform learned purposeful movements despite adequate strength and comprehension.", "Physiology"),
    w("A patient cannot plan or execute a complex sequence such as making tea, including timing and scaling. Which basal-ganglia circuit is likely impaired?", "The cognitive loop of the basal ganglia is likely impaired because it plans, sequences, times, and scales complex motor programs.", "Physiology"),
    w("A patient has bradykinesia and resting tremor. Give the diagnosis and basal-ganglia pathophysiology.", "Parkinson disease caused by loss of dopaminergic neurons in substantia nigra pars compacta. Reduced dopamine decreases activity of the movement-facilitating direct pathway and increases activity of the movement-inhibiting indirect pathway.", "Physiology"),
    w("A patient no longer swings the arms naturally while walking. Which basal-ganglia function may be affected?", "Automatic associated or associative movements may be impaired.", "Physiology"),
    w("Describe the role of the basal ganglia in regulating muscle tone and name the structures involved.", "The lentiform nucleus, consisting of the putamen and globus pallidus, mainly exerts an inhibitory effect on muscle tone. The caudate nucleus can increase muscle tone.", "Physiology"),
    m("What is the competitive antagonist of benzodiazepine receptors?", ["Flumazenil", "Picrotoxin", "Zolpidem", "Temazepam", "Flurazepam"], "A", "Pharmacology", source="marked"),
    m("The mechanism of action of benzodiazepines is:", ["Activation of GABA-B receptors", "Antagonism of glycine receptors in the spinal cord", "Blockade of glutamic-acid action", "Increased GABA-A-mediated chloride conductance", "Inhibition of GABA release"], "D", "Pharmacology"),
]


def main() -> int:
    count = write_markdown(
        OUTPUT,
        "Source 26 — Department question bank",
        {
            "Source file": "Raw_PDF_Questions/CNS/department Q.pdf",
            "Type": "Assiut departmental mixed question bank",
            "Pages": 43,
            "Total questions": len(ITEMS),
            "Answer source": "key:15; marked:16; derived:35 (source contains mixed highlighted cards and incomplete option captures)",
            "Tag": "Department, QBank, subject-specific tags below",
            "Year": "None",
            "Note": "The scan contains four mixed clinical cards, a stretch-reflex question bank, parasitology/microbiology cards, and basal-ganglia cards. Several basal-ganglia cards have incomplete option text or no complete MCQ stem; those prompts are retained as QROC with full answers rather than inventing missing options. No Arabic characters remain.",
        },
        ITEMS,
    )
    print(f"wrote {count}; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
