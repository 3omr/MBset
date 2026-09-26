"""Shared MBset Markdown helpers for the Assiut NEUROSCIENCE SYSTEM module."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ARABIC = re.compile(r"[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff\ufb50-\ufdff\ufe70-\ufeff]")
INVISIBLE = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff\u00ad]")

_NOTATION = (
    (re.compile(r"\bCa\s*(?:\*\*|\+\+)"), "Ca²⁺"),
    (re.compile(r"\bNa\s*\*(?!\*)"), "Na⁺"),
    (re.compile(r"\bNa\+(?!\w)"), "Na⁺"),
    (re.compile(r"\bK\+(?!\w)"), "K⁺"),
    (re.compile(r"\bCl-(?!\w)"), "Cl⁻"),
    (re.compile(r"\bHCO3-(?!\w)"), "HCO₃⁻"),
    (re.compile(r"\bH2O\b"), "H₂O"),
    (re.compile(r"\bCO2\b"), "CO₂"),
    (re.compile(r"\bO2\b"), "O₂"),
    (re.compile(r"(?<![A-Za-z])B(?=[12]\b)"), "β"),
    (re.compile(r"(?<![A-Za-z])a(?=[12]\b)"), "α"),
    (re.compile(r"\bum\b"), "µm"),
    (re.compile(r"(?:-->|->|=>)"), "→"),
)


def clean(value: object | None, *, strip_edges: bool = True) -> str | None:
    if value is None:
        return None
    text = unicodedata.normalize("NFKC", str(value))
    text = INVISIBLE.sub("", text).replace("\xa0", " ")
    text = text.replace("", " ").replace("", "").replace("", "")
    text = ARABIC.sub("", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"[ \t]{2,}", " ", text).strip()
    for pattern, replacement in _NOTATION:
        text = pattern.sub(replacement, text)
    if strip_edges:
        text = text.strip(" .;,\t")
    return text or None


def clean_stem(value: object | None) -> str | None:
    text = clean(value)
    if not text:
        return None
    text = re.sub(r"^\s*(?:\[MCQ\]\s*)?(?:###\s*)?Q?\s*\d{1,3}\s*[.):\-]\s*", "", text, flags=re.I)
    text = re.sub(r"\s*-\s*\*\*Source question:\*\*.*$", "", text, flags=re.I)
    text = text.replace("**", "")
    return text.strip()


def clean_option(value: object | None) -> str | None:
    text = clean(value)
    if not text:
        return None
    # Do not strip the leading B from medical terms such as B-carbolines.
    # A hyphen is treated as an option separator only when followed by
    # whitespace or the end of the value.
    return re.sub(r"^\s*[A-Fa-f]\s*(?:[.):]|-(?=\s|$))\s*", "", text).strip() or None


def has_arabic(value: object | None) -> bool:
    return bool(value and ARABIC.search(str(value)))


@dataclass
class Question:
    stem: str
    options: Sequence[str] | None = None
    correct: str = "-"
    source: str = "derived"
    exp: str | None = None
    tag: str | None = None
    tag_suggere: str | None = None
    year: int | None = None
    image: str | None = None
    qtype: str | None = None

    def __post_init__(self) -> None:
        self.stem = clean_stem(self.stem) or ""
        self.options = tuple(clean_option(option) or "" for option in (self.options or ()))
        self.correct = self.correct.upper() if self.correct else "-"
        self.exp = clean(self.exp)
        self.qtype = self.qtype or ("QCS" if self.options else "QROC")

    def render(self, number: int) -> str:
        lines = [f"### Q{number}: {self.stem}", ""]
        if self.qtype == "QCS":
            for index, option in enumerate(self.options):
                lines.append(f"- **{chr(65 + index)})** {option}")
            lines += ["", f"**Correct Answer:** {self.correct}", f"**Answer Source:** {self.source}"]
        else:
            lines += ["**Correct Answer:** -", f"**Answer Source:** {self.source}"]
        if self.image:
            lines.append(f"**Image:** {self.image}")
        if self.exp:
            lines.append(f"**EXP:** {self.exp}")
        if self.tag:
            lines.append(f"**Tag:** {self.tag}")
        if self.tag_suggere:
            lines.append(f"**tagSuggere:** {self.tag_suggere}")
        if self.year is not None:
            lines.append(f"**Year:** {self.year}")
        lines += ["", "---", ""]
        return "\n".join(lines)


def write_markdown(path: str | Path, title: str, metadata: dict[str, object], questions: Iterable[Question]) -> int:
    question_list = list(questions)
    lines = [f"# {title}", ""]
    for key, value in metadata.items():
        lines.append(f"- **{key}:** {value}")
    lines += ["", "---", ""]
    for index, question in enumerate(question_list, 1):
        lines.append(question.render(index))
    Path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return len(question_list)
