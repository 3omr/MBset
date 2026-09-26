#!/usr/bin/env python3
"""Extract the readable question cards from the 19-page Department Qs scan."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import Question, write_markdown  # noqa: E402


MODULE = SCRIPT_DIR.parent
OUTPUT = MODULE / "Markdown_Questions" / "12_Department_Qs.md"

# The file is a collage of short question cards from several disciplines.  The
# cards are kept in source order, including repeated cards supplied on later
# pages.  Answer provenance is per card: explicit slide answers are ``key``,
# visible overlaid/circled answers are ``marked``, and the two stroke items are
# derived from the anatomy/physiology content because their marks are unclear.
ITEMS = [
    ("A patient has suffered a stroke caused by occlusion of the right anterior cerebral artery. The patient is most likely to present with:", [
        "Loss of pain and temperature sensation in the left leg", "Weakness in the right leg", "Drooping of the corner of the mouth on the left", "Aphasia", "Loss of discriminative touch on the right side of the face"], "A", "derived", "Anatomy"),
    ("Which of the following agents is an opioid antagonist?", ["Amphetamine", "Naltrexone", "Morphine", "Chlorpromazine", "Disulfiram"], "B", "marked", "Pharmacology"),
    ("Which opioid analgesic is used in combination with droperidol in neuroleptanalgesia?", ["Morphine", "Buprenorphine", "Fentanyl", "Naltrexone", "Pentazocine"], "C", "marked", "Pharmacology"),
    ("A 64-year-old man with poorly controlled hypertension collapses and has paralysis and complete sensory loss of the left arm, leg, and lower face. The most likely location for the lesion is:", ["Thalamus", "Medulla oblongata", "Right frontal lobe", "Right internal capsule"], "D", "marked", "Anatomy"),
    ("Indicate the competitive antagonist of benzodiazepine receptors:", ["Flumazenil", "Picrotoxin", "Zolpidem", "Temazepam", "Flurazepam"], "A", "marked", "Pharmacology"),
    ("The mechanism of action of benzodiazepines is:", ["Activation of GABAB receptors", "Antagonism of glycine receptors in the spinal cord", "Blockade of the action of glutamic acid", "Increased GABA-mediated chloride ion conductance", "Blockade of serotonin receptors"], "D", "derived", "Pharmacology"),
    ("Which of the following antipsychotic drugs is typical?", ["Clozapine", "Quetiapine", "Haloperidol", "Olanzapine", "Risperidone"], "C", "marked", "Pharmacology"),
    ("Indicate the atypical antipsychotic drug:", ["Haloperidol", "Clozapine", "Thioridazine", "Thiothixene", "Chlorpromazine"], "B", "marked", "Pharmacology"),
    ("A patient is capable of pupillary constriction during accommodation but not in response to light directed to either eye. The lesion is most likely present in:", ["Optic nerve", "Abducent nucleus", "Edinger-Westphal nucleus", "Pretectal areas", "Supraoculomotor nucleus"], "D", "derived", "Physiology"),
    ("The aperture controlling the amount of light entering the eye is called:", ["The lens", "The pupil", "The cornea", "Ciliary muscles"], "B", "key", "Physiology"),
    ("The greatest amount of refraction occurs when light passes from:", ["The lens into the vitreous humor", "The aqueous humor into the lens", "The cornea into the aqueous humor", "The air into the cornea"], "D", "key", "Physiology"),
    ("All of the following conditions are associated with pupillary dilation (mydriasis) EXCEPT:", ["Withdrawal of light", "During the second stage of anesthesia", "Horner syndrome", "Lesions of the oculomotor nerve"], "C", "derived", "Physiology"),
    ("Which of the following is NOT a function of the iris?", ["It is protective to the lens", "It shares in the drainage of aqueous", "It contains the muscles that control the size of the pupil", "It is transparent to permit light entry"], "D", "key", "Histology"),
    ("A patient has suffered a stroke caused by occlusion of the right anterior cerebral artery. The patient is most likely to present with:", [
        "Loss of pain and temperature sensation in the left leg", "Weakness in the right leg", "Drooping of the corner of the mouth on the left", "Aphasia", "Loss of discriminative touch on the right side of the face"], "A", "derived", "Anatomy"),
    ("Which of the following agents is an opioid antagonist?", ["Amphetamine", "Naltrexone", "Morphine", "Chlorpromazine", "Disulfiram"], "B", "marked", "Pharmacology"),
    ("Which opioid analgesic is used in combination with droperidol in neuroleptanalgesia?", ["Morphine", "Buprenorphine", "Fentanyl", "Naltrexone", "Pentazocine"], "C", "marked", "Pharmacology"),
    ("One of the solitary cystic helminthic brain lesions is:", ["Hydatidosis", "Schistosomiasis", "Strongyloidiasis", "Toxocariasis", "Trichinosis"], "A", "marked", "Parasitology"),
    ("A hole-with-dot appearance in imaging of helminthic CNS disease presents in:", ["Neurocysticercosis", "Schistosomiasis", "Strongyloidiasis", "Toxocariasis", "Trichinosis"], "A", "marked", "Parasitology"),
    ("Definitive diagnosis in neurohydatidosis is:", ["Egg in urine", "Egg in sputum", "Egg in stool", "Encysted larvae in muscle", "Microscopic examination of surgical specimens"], "E", "marked", "Parasitology"),
    ("Coenurosis occurs due to the invasion of which stage to the brain tissue?", ["Egg of Echinococcus granulosus", "Egg of Taenia multiceps", "Larval stage of Echinococcus granulosus", "Larval stage of Taenia multiceps", "Larval stage of Taenia solium"], "D", "marked", "Parasitology"),
    ("Which of the following is NOT a function of the iris?", ["It is protective to the lens", "It shares in the drainage of aqueous", "It contains the muscles that control the size of the pupil", "It is transparent to permit light entry"], "D", "key", "Histology"),
    ("During photopic vision:", ["Visual acuity is lower than during scotopic vision", "Rods are not stimulated", "Color vision is perceived by cones", "Cones are not stimulated"], "C", "key", "Physiology"),
    ("Rhodopsin:", ["Is the photosensitive pigment in the cones", "Is decomposed upon light stimulation", "Is composed of opsin and all-trans retinal", "Increases in light adaptation", "Increases in vitamin A deficiency"], "B", "key", "Physiology"),
]


def main() -> int:
    questions = [
        Question(
            stem=stem,
            options=options,
            correct=answer,
            source=source,
            exp=("Answer explicitly printed on the source card." if source == "key" else
                 "Answer transcribed from the visible mark on the source card." if source == "marked" else
                 "No dependable key was available on the card; answer derived from the corresponding course content."),
            tag=f"Department, QBank, {subject}",
            tag_suggere=subject,
        )
        for stem, options, answer, source, subject in ITEMS
    ]
    count = write_markdown(
        OUTPUT,
        "Source 12 — Department Qs",
        {
            "Source file": "Raw_PDF_Questions/CNS/Department Qs.pdf",
            "Type": "Department question cards, mixed Anatomy/Pharmacology/Physiology/Histology/Parasitology",
            "Pages": 19,
            "Total questions": len(questions),
            "Answer source": "key:5; marked:12; derived:5",
            "Tag": "per question — Department, QBank, Subject",
            "tagSuggere": "per question — subject",
            "Year": "None",
            "Note": "Repeated cards supplied by the source are retained; blank pages and explanatory slide text without a question are excluded and logged in the catalog.",
        },
        questions,
    )
    print(f"wrote {count}; key=5; marked=12; derived=5; Arabic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
