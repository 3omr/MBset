#!/usr/bin/env python3
"""Parse validated MBset Markdown into a canonical JSON payload.

This is the data/preflight half of the final Excel build.  It honors Tag,
tagSuggere, and Year inside each question block, which is required for mixed
quiz/exam sources.  A later artifact-tool builder can consume the JSON without
re-parsing Markdown or losing per-question provenance.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from lib_md import clean, clean_option, clean_stem  # noqa: E402


CANONICAL = [
    "id", "Cas", "Text", "Image", "explanationImage", "A", "B", "C", "D", "E", "F",
    "A_EXP", "B_EXP", "C_EXP", "D_EXP", "E_EXP", "F_EXP", "Correct", "Hint", "EXP",
    "Note", "Type", "categoryId", "categoryName", "subcategoryId", "subcategoryName",
    "tagSuggere", "Year", "Tag", "ImageMasks", "ExplanationImageMasks",
]
BLOCK_RE = re.compile(r"^###\s*Q(\d+)\s*:\s*(.*?)(?=^###\s*Q\d+\s*:|\Z)", re.S | re.M)
OPT_RE = re.compile(r"^\s*[-*]\s*\*\*([A-F])\)\*\*\s*(.+?)\s*$", re.M)
FIELD_RE = {
    name: re.compile(r"^\*\*" + re.escape(name) + r":\*\*\s*(.*?)\s*$", re.M)
    for name in ("Correct Answer", "Answer Source", "Image", "EXP", "Tag", "tagSuggere", "Year")
}
ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")


def field(body: str, name: str) -> str | None:
    match = FIELD_RE[name].search(body)
    return clean(match.group(1)) if match else None


def catalog_meta(catalog: Path) -> dict[str, dict[str, object]]:
    """Fallback metadata for older/simple files without block-level tags."""
    meta: dict[str, dict[str, object]] = {}
    if not catalog.is_file():
        return meta
    for line in catalog.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`*") for cell in line.strip("|").split("|")]
        filename = next((cell for cell in cells if cell.endswith(".md")), None)
        tag = next((cell for cell in cells if re.match(r"^(Department|Exams|Formative|Professor|External),", cell)), None)
        if not filename or not tag:
            continue
        subject = next((cell for cell in cells if cell in {"Anatomy", "Physiology", "Histology", "Biochemistry", "Microbiology", "Parasitology", "Pathology", "Pharmacology"}), None)
        year = next((cell for cell in reversed(cells) if re.fullmatch(r"(19|20)\d{2}", cell)), None)
        meta[filename] = {"Tag": tag, "tagSuggere": subject, "Year": int(year) if year else None}
    return meta


def parse_file(path: Path, fallback: dict[str, object]) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    output: list[dict[str, object]] = []
    for number, body in BLOCK_RE.findall(text):
        body = body.split("\n---", 1)[0]
        opt_matches = list(OPT_RE.finditer(body))
        boundaries = [match.start() for match in opt_matches]
        for name in ("Correct Answer", "Answer Source", "Image", "EXP", "Tag", "tagSuggere", "Year"):
            match = FIELD_RE[name].search(body)
            if match:
                boundaries.append(match.start())
        # Legacy formative blocks keep source numbering as a Markdown list
        # item before the real options.  It is metadata, not part of the stem.
        source_question = re.search(r"^\s*-\s*\*\*Source question:\*\*.*$", body, flags=re.M | re.I)
        if source_question:
            boundaries.append(source_question.start())
        stem = clean_stem(body[: min(boundaries)] if boundaries else body)
        options = {label: clean_option(value) for label, value in OPT_RE.findall(body)}
        correct = (field(body, "Correct Answer") or "-").upper()
        source = (field(body, "Answer Source") or "").lower()
        tag = field(body, "Tag") or fallback.get("Tag")
        tag_suggere = field(body, "tagSuggere") or fallback.get("tagSuggere")
        year_raw = field(body, "Year")
        if year_raw and re.fullmatch(r"\d{4}", year_raw):
            year: int | None = int(year_raw)
        else:
            year = fallback.get("Year") if isinstance(fallback.get("Year"), int) else None
        filled = [label for label in "ABCDEF" if options.get(label)]
        qtype = "QCS" if len(filled) >= 2 and correct != "-" else "QROC"
        # Preserve the evidence label in Note because the platform schema has
        # no dedicated provenance column.
        note = f"Answer Source: {source or 'missing'}"
        if qtype == "QROC":
            correct = "-"
            options = {label: None for label in "ABCDEF"}
        output.append(
            {
                "id": None,
                "Cas": None,
                "Text": stem,
                "Image": field(body, "Image"),
                "explanationImage": None,
                **{label: options.get(label) for label in "ABCDEF"},
                **{f"{label}_EXP": None for label in "ABCDEF"},
                "Correct": correct,
                "Hint": None,
                "EXP": field(body, "EXP"),
                "Note": note,
                "Type": qtype,
                "categoryId": "AssiutUniv_NEUROSCIENCE_SYSTEM",
                "categoryName": "NEUROSCIENCE SYSTEM",
                "subcategoryId": None,
                "subcategoryName": None,
                "tagSuggere": tag_suggere,
                "Year": year,
                "Tag": tag,
                "ImageMasks": None,
                "ExplanationImageMasks": None,
                "_source_file": path.name,
                "_source_question": int(number),
                "_answer_source": source,
            }
        )
    return output


def normalized_stem(text: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


REVIEWED_CONFLICT_STEMS = {
    normalized_stem("Active cells during inflammation of CNS is ?"),
    normalized_stem("Primary cutaneous hyperalgesia:"),
    normalized_stem("Visceral pain:"),
    normalized_stem("Temporal summation:"),
    normalized_stem("Temporal Summation:"),
    normalized_stem("Spatial summation:"),
    normalized_stem("Epinephrine added to local anesthetics to:"),
    normalized_stem("Intracranial headache could result from painful stimuli applied on :-"),
    normalized_stem("Which of the following is not part of the analgesia system:"),
    normalized_stem("Cerebral autoregulation is correctly described by:"),
    normalized_stem("Allodynia means:"),
    normalized_stem("Regarding unmyelinated fibers:"),
}


def normalized_answer(text: object) -> str:
    """Normalize answer text so reordered options are not false conflicts."""
    value = str(text or "").lower()
    value = re.sub(r"\b(does|is|are|the|a|an)\b", " ", value)
    return re.sub(r"[^a-z0-9]+", "", value)


def correct_answer_text(row: dict[str, object]) -> str:
    correct = str(row.get("Correct") or "-")
    if correct == "-":
        return ""
    return normalized_answer(row.get(correct))


def merge_questions(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    seen: dict[str, dict[str, object]] = {}
    conflicts: list[dict[str, object]] = []
    hard_conflicts: list[dict[str, object]] = []
    for row in rows:
        key = normalized_stem(row["Text"])
        if not key:
            continue
        previous = seen.get(key)
        if previous is None:
            seen[key] = row
            continue
        old_correct, new_correct = previous["Correct"], row["Correct"]
        if old_correct != new_correct and old_correct != "-" and new_correct != "-":
            conflict = {
                "stem": row["Text"],
                "left": {"file": previous["_source_file"], "correct": old_correct},
                "right": {"file": row["_source_file"], "correct": new_correct},
            }
            # A duplicated source often changes option order.  Compare the
            # answer text before treating the letter change as a conflict.
            same_answer_text = correct_answer_text(previous) == correct_answer_text(row)
            if not same_answer_text:
                conflicts.append(conflict)
                if key not in REVIEWED_CONFLICT_STEMS:
                    hard_conflicts.append(conflict)
        # Preserve the strongest answer provenance and any useful evidence.
        rank = {"key": 4, "marked": 4, "online": 4, "derived": 2, "": 0}
        if rank.get(str(row["_answer_source"]), 0) > rank.get(str(previous["_answer_source"]), 0):
            previous.update({label: row[label] for label in "ABCDEF"})
            previous["Correct"] = row["Correct"]
            previous["Type"] = row["Type"]
            previous["EXP"] = row["EXP"] or previous["EXP"]
            previous["_answer_source"] = row["_answer_source"]
        tags = [value.strip() for value in f"{previous.get('Tag') or ''}, {row.get('Tag') or ''}".split(",") if value.strip()]
        previous["Tag"] = ", ".join(dict.fromkeys(tags)) or None
        previous["tagSuggere"] = previous.get("tagSuggere") or row.get("tagSuggere")
        previous["Image"] = previous.get("Image") or row.get("Image")
    return list(seen.values()), conflicts, hard_conflicts


def validate(rows: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(rows, start=2):
        blob = " ".join(str(row.get(key) or "") for key in ("Text", *"ABCDEF", "EXP", "Tag"))
        if ARABIC_RE.search(blob):
            errors.append(f"row {index}: Arabic character")
        if not row.get("Text") or len(str(row["Text"])) < 10:
            errors.append(f"row {index}: short stem")
        if not row.get("Tag"):
            errors.append(f"row {index}: missing Tag")
        if row["Type"] == "QCS":
            filled = [label for label in "ABCDEF" if row.get(label)]
            if filled != list("ABCDEF"[: len(filled)]):
                errors.append(f"row {index}: option gap")
            if row["Correct"] not in filled:
                errors.append(f"row {index}: Correct not among options")
        elif row["Type"] == "QROC":
            if row["Correct"] != "-" or not row.get("EXP"):
                errors.append(f"row {index}: incomplete QROC")
        else:
            errors.append(f"row {index}: invalid Type")
        if row.get("_answer_source") not in {"key", "marked", "online", "derived"}:
            errors.append(f"row {index}: missing/invalid Answer Source")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    fallback = catalog_meta(args.catalog)
    rows: list[dict[str, object]] = []
    files = sorted(path for path in args.markdown.glob("*.md") if not path.name.startswith("00_"))
    for path in files:
        rows.extend(parse_file(path, fallback.get(path.name, {})))
    deduped, conflicts, hard_conflicts = merge_questions(rows)
    errors = validate(deduped)
    if hard_conflicts:
        errors.append(f"{len(hard_conflicts)} unresolved hard duplicate answer conflict(s)")
    payload = {
        "headers": CANONICAL,
        "categoryId": "AssiutUniv_NEUROSCIENCE_SYSTEM",
        "categoryName": "NEUROSCIENCE SYSTEM",
        "sourceMarkdownFiles": [path.name for path in files],
        "inputQuestionCount": len(rows),
        "deduplicatedQuestionCount": len(deduped),
        "duplicateCount": len(rows) - len(deduped),
        "provenance": Counter(str(row["_answer_source"]) for row in deduped),
        "conflicts": conflicts,
        "reviewConflictCount": len(conflicts) - len(hard_conflicts),
        "hardConflictCount": len(hard_conflicts),
        "errors": errors,
        "questions": deduped,
    }
    # Counter is not JSON serializable by default.
    payload["provenance"] = dict(payload["provenance"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("inputQuestionCount", "deduplicatedQuestionCount", "duplicateCount", "provenance", "reviewConflictCount", "hardConflictCount", "errors")}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
