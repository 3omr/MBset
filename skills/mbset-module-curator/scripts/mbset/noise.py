"""Line-level noise removal and notation repair (never touches answer keys).

Two layers:
* `is_noise_line()` drops whole lines that are chrome: Moodle/LMS UI, phone status
  bars, scanner watermarks, DocReader headers, page footers.
* `clean_text()` cleans the text that survives: Arabic, bubble artefacts, trailing
  answer-grid dumps, leading numbering (stems only), and conservative notation
  repair. Anything ambiguous (`B1` could be vitamin B1) is left for the auditor
  to flag rather than guessed.
"""

from __future__ import annotations

import re

from .common import ARABIC, clean_inline

NOISE_LINES = [re.compile(p, re.I) for p in (
    r"^\s*(?:page\s*)?\d{1,3}\s*(?:of|/)\s*\d{1,3}\s*$",
    r"^\s*-?\s*\d{1,3}\s*-?\s*$",                       # bare page number (only dropped at page edges)
    r"Home\s*»\s*My courses",
    r"^\s*(?:Quick Links|About Us|Contact us)\b",
    r"Lorem Ipsum",
    r"^\s*(?:Started on|Completed on|Time taken|State|Grade|Marks)\b.*(?:\d{4}|out of|Finished|\d+\.\d+/)",
    r"^\s*(?:Flag question|Clear my choice|Finish (?:attempt|review)|Next page|Previous page)\b",
    r"^\s*Question\s+\d+\s*(?:Correct|Incorrect|Not answered|Answer saved|Complete)\b",
    r"^\s*Mark(?:ed)?\s+[\d.]+\s+out\s+of\s+[\d.]+",
    r"^\s*(?:Not yet answered|Answer saved)\s*$",
    r"^\s*(?:Scanned|Created)\s+(?:with|by)\s+\w*\s*(?:CamScanner|AnyScanner|Adobe Scan)",
    r"CamScanner|AnyScanner",
    r"^\s*DocReader Guide\s*$",
    r"Solve it online at:\s*https?://",
    r"^\s*@\w*bot\b|^\s*t\.me/",
    r"^\s*\d{1,2}:\d{2}\s*(?:AM|PM)?\s*(?:[\W_]|LTE|4G|5G|wifi|Vo)*\s*\d{0,3}%?\s*$",
)]

EDGE_ONLY = {1}  # indexes of NOISE_LINES that only apply at the first/last line of a page

GRID_DUMP = re.compile(
    r"(?i)\s*(?:answers?\s+(?:key|of)\b|answer\s+key|model\s+answer\s+key)?\s*(?:\b\d{1,3}\s+){4,}[A-E](?:\s+[A-E]){4,}.*$")
TABLE_HDR = re.compile(r"(?i)\s*TABLE\s+\d+\s+A\s+B\b.*$")
BUBBLES = re.compile(r"[@©®]{2,}|(?<=\s)[@©®](?=\s)|^[@©®\s.,\-)]+")
# "12." "12)" "Q3:" but never an age or dose: "44-y female", "1.5 mg", "12-year-old"
LEADING_NUM = re.compile(r"^\s*(?:#+\s*)?(?:Q(?:uestion)?\s*)?\d{1,3}\s*(?:[.):](?!\d)|-(?!\w))\s*", re.I)
MARKERS = re.compile(r"^\s*\[(?:MCQ|Written|QROC)\]\s*[:\-]?\s*", re.I)
# "( 1 mark )", "(2.5 marks)." and the residue of Arabic point labels such as ")نقطة 1(" → ")1("
MARK_NOTES = re.compile(r"\(\s*[\d.]+\s*(?:marks?|degrees?|points?)\s*\)\.?|\)\s*[\d.]*\s*\(|^\s*\*\s*$", re.I)
SELECT_ONE = re.compile(r"\bSelect\s+one(?:\s+or\s+more)?\s*:?", re.I)

NOTATION = [
    (re.compile(r"\bCa\s*(?:\*\*|\+\+|2\+)(?!\w)"), "Ca²⁺"),
    (re.compile(r"\bMg\s*(?:\*\*|\+\+|2\+)(?!\w)"), "Mg²⁺"),
    (re.compile(r"\bFe\s*(?:\*\*|\+\+|2\+)(?!\w)"), "Fe²⁺"),
    (re.compile(r"\bFe\s*(?:\*\*\*|\+\+\+|3\+)(?!\w)"), "Fe³⁺"),
    (re.compile(r"\b(Na|K|H)\s*(?:\*|\+)(?![\w+*])"), r"\1⁺"),
    (re.compile(r"\bCl\s*-(?=[\s,.;)]|$)"), "Cl⁻"),
    (re.compile(r"\bHCO3\s*-(?=[\s,.;)]|$)"), "HCO₃⁻"),
    (re.compile(r"(?<=\d)\s?um\b"), " µm"),
    (re.compile(r"(?<=\d)\s?ug\b"), " µg"),
    (re.compile(r"(?<=\d)\s?uL\b"), " µL"),
    (re.compile(r"\s(?:->|-->|=>)\s"), " → "),
    (re.compile(r"\b(?:B|beta)[\s-]?([12])(?=[\s-]*(?:receptors?|adrenergic|blockers?|agonists?|antagonists?))", re.I), r"β\1"),
    (re.compile(r"\b(?:alpha)[\s-]?([12])(?=[\s-]*(?:receptors?|adrenergic|blockers?|agonists?|antagonists?))", re.I), r"α\1"),
]
QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "•": "", "\uf0b7": "", "\uf0a7": ""})


def is_noise_line(text: str, at_page_edge: bool = False, extra: list[re.Pattern] | None = None) -> bool:
    for i, rx in enumerate(NOISE_LINES):
        if i in EDGE_ONLY and not at_page_edge:
            continue
        if rx.search(text):
            return True
    return any(rx.search(text) for rx in extra or [])


def repair_notation(text: str) -> str:
    for rx, repl in NOTATION:
        text = rx.sub(repl, text)
    return text


def clean_text(text: str, stem: bool = False) -> str:
    text = clean_inline(text).translate(QUOTES)
    text = ARABIC.sub("", text)
    text = GRID_DUMP.sub("", text)
    text = TABLE_HDR.sub("", text)
    text = BUBBLES.sub(" ", text)
    text = SELECT_ONE.sub("", text)
    text = MARK_NOTES.sub(" ", text)
    text = re.sub(r"^(?:\.\s*)+(?=[A-Za-z(])", "", text)          # RTL-moved full stops
    text = re.sub(r"^\s*\d{0,2}\s*[()]*\s*\*\s+", "", text)       # Google Forms "required" star residue
    if stem:
        text = MARKERS.sub("", LEADING_NUM.sub("", text))
        text = re.sub(r"^\s*[*•:]+\s*|\s*\*+\s*$", "", text)
    text = repair_notation(text)
    text = re.sub(r"\s\.(?=[a-z])", " ", text)                       # RTL full stop moved to a line start
    text = re.sub(r"\s+([,.;:?])(?=\s|$)", r"\1", text)
    text = re.sub(r"\(\s*\)", "", text)
    return re.sub(r"\s{2,}", " ", text).strip(" -–|_")
