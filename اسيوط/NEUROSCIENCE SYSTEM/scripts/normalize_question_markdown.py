#!/usr/bin/env python3
"""Small, explicit preflight repairs for legacy Markdown question blocks.

The source files are already manually extracted.  This script only fills
documented structural gaps that prevent the canonical payload from being
validated (missing evidence labels, short legacy stems, and missing model
answers for one-option QROC blocks).  It does not invent options or answer
keys.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "Markdown_Questions"
BLOCK_RE = re.compile(r"(^###\s*Q(?P<num>\d+)\s*:.*?)(?=^###\s*Q\d+\s*:|\Z)", re.S | re.M)


def update_blocks(path: Path, updates: dict[int, dict[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        number = int(match.group("num"))
        update = updates.get(number)
        if not update:
            return block

        heading = update.get("heading")
        if heading:
            block = re.sub(r"^###\s*Q\d+\s*:.*$", f"### Q{number}: {heading}", block, count=1, flags=re.M)

        answer_source = update.get("answer_source")
        if answer_source and "**Answer Source:**" not in block:
            marker = re.search(r"^\*\*Tag:\*\*.*$", block, flags=re.M)
            line = f"**Answer Source:** {answer_source}\n"
            if marker:
                block = block[: marker.start()] + line + block[marker.start() :]
            else:
                block = block.rstrip() + "\n" + line

        exp = update.get("exp")
        if exp and not re.search(r"^\*\*EXP:\*\*\s*\S", block, flags=re.M):
            marker = re.search(r"^\*\*Tag:\*\*.*$", block, flags=re.M)
            line = f"**EXP:** {exp}\n"
            if marker:
                block = block[: marker.start()] + line + block[marker.start() :]
            else:
                block = block.rstrip() + "\n" + line
        return block

    updated = BLOCK_RE.sub(repl, text)
    if updated == text:
        return
    path.write_text(updated, encoding="utf-8")


def add_source10_provenance() -> None:
    path = MD / "10_CNS_Gds.md"
    text = path.read_text(encoding="utf-8")
    blocks = []
    last = 0
    matches = list(re.finditer(r"^###\s*Q\d+\s*:.*?(?=^###\s*Q\d+\s*:|\Z)", text, re.S | re.M))
    for match in matches:
        blocks.append(text[last : match.start()])
        block = match.group(0)
        if "**Answer Source:**" not in block:
            marker = re.search(r"^\*\*Tag:\*\*.*$", block, flags=re.M)
            line = "**Answer Source:** derived\n"
            if marker:
                block = block[: marker.start()] + line + block[marker.start() :]
            else:
                block = block.rstrip() + "\n" + line
        blocks.append(block)
        last = match.end()
    blocks.append(text[last:])
    updated = "".join(blocks)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def main() -> None:
    add_source10_provenance()

    update_blocks(
        MD / "17_M3WAN_Final_30.md",
        {131: {"heading": "What is GABA?"}},
    )

    update_blocks(
        MD / "18_M3WAN_Final_32.md",
        {
            27: {
                "heading": "Which opioid is a full antagonist?",
                "exp": "Naloxone is a full competitive opioid receptor antagonist used to reverse opioid toxicity.",
            },
            40: {
                "heading": "Which statement about the third ventricle is true?",
                "exp": "The hypothalamus forms much of the floor of the third ventricle.",
            },
            62: {
                "heading": "What is the main reward center in the brain?",
                "exp": "The medial forebrain bundle is the principal reward pathway and a major brain reward center.",
            },
        },
    )

    update_blocks(
        MD / "19_M3WAN_Mid_Final_31.md",
        {
            63: {
                "heading": "Which structure is the most potent reward center?",
                "exp": "The medial forebrain bundle is the most potent reward pathway and a major brain reward center.",
            },
            64: {
                "heading": "Which structure facilitates recognition of words after prior exposure?",
                "exp": "Neocortical priming facilitates recognition of words after prior exposure to them.",
            },
            65: {
                "heading": "Which statement about visual acuity is true?",
                "exp": "Visual acuity is greatest at the fovea because cone pathways there have minimal convergence and provide high spatial resolution.",
            },
            66: {
                "heading": "Which structure is the analyzer of hearing?",
                "exp": "The auditory cortex is the cortical analyzer of hearing; the basilar membrane is the peripheral frequency-analyzing structure of the cochlea.",
            },
            67: {
                "heading": "Which statement about REM sleep is true?",
                "exp": "REM sleep is associated with rapid eye movements, skeletal muscle atonia, and increased cerebral blood flow and activity.",
            },
            68: {
                "heading": "What is the tuberomammillary nucleus (TMN)?",
                "exp": "The tuberomammillary nucleus is a histaminergic hypothalamic nucleus that releases histamine and promotes wakefulness.",
            },
            100: {
                "heading": "Which CSF finding indicates septic meningitis?",
                "exp": "Septic or acute bacterial meningitis typically causes neutrophilic pleocytosis, elevated CSF protein, and reduced CSF glucose.",
            },
        },
    )

    update_blocks(
        MD / "21_M3WAN_Mid_32.md",
        {
            1: {
                "heading": "Cheese reaction occurs with which combination?",
                "exp": "Selegiline combined with tyramine-rich food can cause a hypertensive cheese reaction because monoamine oxidase inhibition increases tyramine.",
            },
            2: {"heading": "Which statement about ketamine is correct?"},
            9: {
                "heading": "What is the key enzyme of acetylcholine synthesis?",
                "exp": "Choline acetyltransferase synthesizes acetylcholine from choline and acetyl-CoA.",
            },
            12: {
                "heading": "Which organism causes fungal meningitis?",
                "exp": "Cryptococcus neoformans is a major cause of fungal meningitis, particularly in immunocompromised patients.",
            },
            14: {"heading": "Which statement about astrocytes is correct?"},
            22: {
                "heading": "What does cutaneous hyperalgesia mean?",
                "exp": "Cutaneous hyperalgesia is an exaggerated painful response to a normally painful cutaneous stimulus; a painless stimulus becoming painful is allodynia.",
            },
            27: {
                "heading": "What is dysdiadochokinesia?",
                "exp": "Dysdiadochokinesia is the inability to perform rapid alternating opposite movements, suggesting cerebellar dysfunction.",
            },
            30: {
                "heading": "Which structure divides the neck into anterior and posterior triangles?",
                "exp": "The sternocleidomastoid muscle divides the neck into anterior and posterior triangles.",
            },
            31: {
                "heading": "Which nerve supplies cutaneous sensation to the forehead?",
                "exp": "The supratrochlear nerve supplies part of the cutaneous sensation of the forehead, with the supraorbital nerve supplying the remaining major area.",
            },
            33: {
                "heading": "Which muscle compresses the cheek against the molar teeth?",
                "exp": "The buccinator muscle compresses the cheek against the molar teeth.",
            },
        },
    )

    update_blocks(
        MD / "25_Qs_bank_2.md",
        {31: {"heading": "Which statement about glycine is correct?"}},
    )

    update_blocks(
        MD / "28_Physiology_Qs_bank_MCQ.md",
        {
            2: {"heading": "The cerebral blood flow (CBF) equals:"},
            3: {"heading": "Which statement about the blood-brain barrier (BBB) is correct?"},
            74: {
                "heading": "Which statement about glaucoma is correct?",
                "exp": "Glaucoma is a common cause of blindness due to progressive optic nerve damage, often associated with increased intraocular pressure.",
            },
            75: {
                "heading": "Which statement about cataract is correct?",
                "exp": "A cataract is a degenerative loss of transparency of the crystalline lens and is a major cause of visual impairment.",
            },
        },
    )


if __name__ == "__main__":
    main()
