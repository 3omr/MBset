"""Stage 1 — profile-driven question parser.

Reads reading-order `Line`s (document.py), executes the source's profile and
produces question records that keep the source wording verbatim, the page/bbox
evidence of every line, and a list of review flags. Answers are attached by
answers.py; markdown is written by writer.py.

Design rules
* Text is copied from the source, never re-typed. Cleaning is limited to noise
  removal and notation repair (noise.py).
* A question number is accepted only when it continues the sequence (n+1), opens
  a new section (1), or skips at most a few numbers (flagged as a gap). Any other
  number-like line is treated as text, so "5. mg" inside a stem cannot split it.
* Option letters must advance (a→b→c…). A fresh "a" after a finished option run
  with stem-like text in between opens an unnumbered question (flagged).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .common import AR_LETTERS, ARABIC, LETTERS, arabic_markers
from .document import Line
from .noise import clean_text as _clean_text, is_noise_line

FIGURE = re.compile(r"(?i)\b(figure|fig\.|diagram|shown (?:below|above|here)|this slide|arrows?|labell?ed|"
                    r"photomicrograph|following image|(?<!clinical )(?<!blood )picture|the image|micrograph|X-ray shown|ECG shown)\b")


@dataclass
class Option:
    letter: str
    parts: list[Line] = field(default_factory=list)
    text: str = ""

    def style(self) -> dict[str, Any]:
        n = sum(max(len(p.text), 1) for p in self.parts) or 1
        return {
            "bold": round(sum(p.bold * max(len(p.text), 1) for p in self.parts) / n, 2),
            "color": round(sum(p.color * max(len(p.text), 1) for p in self.parts) / n, 2),
            "marks": sorted({m for p in self.parts for m in p.marks}),
        }


@dataclass
class Question:
    number: int | None
    section: int
    stem_parts: list[Line] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)
    after: list[Line] = field(default_factory=list)       # text after the options (explanation/answer)
    exp_parts: list[Line] = field(default_factory=list)
    inline_answer: str | None = None
    answer_text: str | None = None                        # 'The correct answer is: Arginine'
    flags: list[str] = field(default_factory=list)
    stem_prefix: str = ""


RTL_CHARS = re.compile(r"[\u0600-\u06ff]")


def _edge_gap(a: Line, b: Line) -> float:
    """Distance between the starting edges of two lines: left for LTR text, right for Arabic (RTL)."""
    rtl = len(RTL_CHARS.findall(a.text + b.text)) > len(re.findall(r"[A-Za-z]", a.text + b.text))
    return abs(a.bbox[2] - b.bbox[2]) if rtl else abs(a.bbox[0] - b.bbox[0])


def qnum(match: re.Match) -> int:
    """The question number: the first group that matched (profiles may use alternatives)."""
    return int(next(g for g in match.groups() if g is not None))


def _compile(patterns: list[str] | None) -> list[re.Pattern]:
    return [re.compile(p, re.I) for p in patterns or []]


TIGHT_DASH_OPT = re.compile(r"^\s*([a-fA-F])\s*-(?=[A-Za-z(\d])")   # "A-Glipizide", trusted only inside a run
QUESTION_HEADER = re.compile(r"^\s*Q(?:uestion)?\s*(?:No\.?\s*)?(\d{1,3})\s*[:.)-]?\s*$", re.I)
RTL_NUMBER = re.compile(r"(?:^|\s)[-*]?\s*\.(\d{1,3})\s*[*]?\s*$")   # "… except .4" from right-to-left PDFs
# "C-reactive protein", "B-lymphocytes": an upper-case letter + dash + lower-case word is a compound,
# not an option; "c-reactive" (lower-case marker) and "C- text" / "C-Text" still are options
INLINE_OPT = re.compile(r"(?:(?<=\s)|^)[(\[]?([a-fA-F])\s*(?:[.)\]]|-(?=\s)|-(?=[A-Z(\d])|(?<=[a-f])-(?=[a-z]))\s*(?=\S)")


def split_inline_options(text: str, mode: Any) -> list[str]:
    """'Stem? a. x b. y c. z' → ['Stem?', 'a. x', 'b. y', 'c. z'].

    Letters must increase (a,b,c… or a,c for 2×2 option grids) and share one case.
    In auto mode a run is split only when it starts the line, or starts with "a"
    and has at least three markers — "vitamin a) and b)" inside a sentence stays.
    """
    if mode is False or mode == "false":
        return [text]
    hits = list(INLINE_OPT.finditer(text))
    if len(hits) < 2:
        return [text]
    best: list[re.Match] = []
    for i, h in enumerate(hits):
        run = [h]
        for h2 in hits[i + 1:]:
            prev = run[-1].group(1)
            cur = h2.group(1)
            if cur.isupper() == prev.isupper() and 0 < ord(cur.lower()) - ord(prev.lower()) <= 3:
                run.append(h2)
        if len(run) > len(best):
            best = run
    if len(best) < 2:
        return [text]
    if mode == "auto" and best[0].start() != 0 and not (best[0].group(1).lower() == "a" and len(best) >= 3):
        return [text]
    pieces = []
    if best[0].start() > 0:
        pieces.append(text[:best[0].start()].strip())
    for i, h in enumerate(best):
        end = best[i + 1].start() if i + 1 < len(best) else len(text)
        pieces.append(text[h.start():end].strip())
    return [p for p in pieces if p]


GRID_LINE = re.compile(r"(?<![\d.])(\d{1,3})\s*[-.:)=|]?\s*\(?([A-Fa-f])\)?(?:\s*/\s*[A-Fa-f])*(?![A-Za-z\d])")


KEY_LABEL = re.compile(r"^[\W_]*(?:(?:the\s+)?(?:correct\s+)?(?:ans(?:wers?)?|key|answer\s*key|model\s+answers?)\s*"
                       r"(?:key)?\s*[:.\-=]?\s*)", re.I)


def is_grid_line(text: str) -> bool:
    """A line that is only answer-key pairs: '1 D 12 C 23 E', '1-a 2-c', a table row '1 E 21 C', '41 C'."""
    text = KEY_LABEL.sub("", text)
    hits = GRID_LINE.findall(text)
    if not hits:
        return False
    rest = re.sub(r"[\W_]", "", GRID_LINE.sub("", text))
    return not rest and (len(hits) >= 2 or re.fullmatch(r"\s*\d{1,3}\s*[-.:)=|]?\s*[A-Fa-f]\s*", text) is not None)


OCR_NUMBER = re.compile(r"^\s*[\\/|'`‘’]?\s*([0-9lIOSZ|]{1,3})\s*[.)]\s+(?=[A-Za-z(])")
OCR_DIGITS = str.maketrans({"l": "1", "I": "1", "|": "1", "O": "0", "S": "5", "Z": "2"})
def BARE_MARKER(letter: str) -> re.Pattern:
    """The expected option letter after a pen tick ate its "." — "D Incision", "DIncision", "By Infected"."""
    return re.compile(rf"^\s*{letter}(?:[y/\\|'`’]?\s+(?=[A-Za-z(\d])|(?=[A-Z][a-z])|(?=\d+\s+[a-z]))")


OCR_MARKER = re.compile(r"^\s*(?:[^\sA-Za-z]{1,2}|[a-fA-F][,;:]|\S{1,2}[.,:;])\s+(?=\S)")   # "4.", "&", "c,", "«."


class Parser:
    def __init__(self, profile: dict[str, Any], lenient: bool = False):
        self.p = profile
        self.lenient = lenient          # OCR text: repair option markers from layout
        self.q_rx = re.compile(profile["question_start"], re.I)
        self.o_rx = re.compile(profile["option_pattern"])
        self.ans_rx = re.compile(profile["answers"]["inline_pattern"], re.I)
        tp = profile["answers"].get("text_pattern")
        self.ans_text_rx = re.compile(tp, re.I) if tp else None
        self.written_ans = re.compile(profile["written"]["answer_marker"], re.I)
        self.skip = _compile(profile.get("skip_patterns"))
        self.stop = _compile(profile.get("stop_patterns"))
        self.keep_ar = bool(profile.get("keep_arabic"))
        self.q_end = re.compile(profile["question_end"]) if profile.get("question_end") else None
        self.questions: list[Question] = []
        self.sections: list[int] = []        # highest number seen per section
        self.starts: list[int] = []          # first number of each section
        self.gaps: list[str] = []
        self.dropped: list[str] = []

    # ------------------------------------------------------------------ helpers
    def _running_lines(self, lines: list[Line], n_pages: int) -> set[str]:
        """Running headers / footers: the same short line on many pages ('INTERNAL MEDICINE DEPARTMENT')."""
        if n_pages < 3:
            return set()
        pages: dict[str, set[int]] = {}
        by_page: dict[int, list[int]] = {}
        for i, ln in enumerate(lines):
            by_page.setdefault(ln.page, []).append(i)
        edge = {i for idx in by_page.values() for i in idx[:2] + idx[-2:]}   # headers/footers sit at the edges
        for i, ln in enumerate(lines):
            if i not in edge:
                continue
            k = _running_key(ln.text)
            if len(k) >= 10 and not self.q_rx.match(ln.text) and not self.o_rx.match(ln.text):
                pages.setdefault(k, set()).add(ln.page)
        return {k for k, pg in pages.items() if len(pg) >= max(3, 0.4 * n_pages)}

    def _key_column(self, lines: list[Line]) -> list[Line]:
        """`answers.key_column: 520` — a lone letter at x >= 520 is the key of the question whose stem
        shares its row ("Which … proteins?   C"); it is attached to that row and removed."""
        col = self.p.get("answers", {}).get("key_column")
        if not col:
            return lines
        keep: list[Line] = []
        for ln in lines:
            m = re.fullmatch(r"\s*\(?([A-Fa-f])\)?\s*", ln.text)
            mt = re.search(r"\s([A-F])\s*$", ln.text)
            if not m and mt and ln.bbox[2] >= col and ln.bbox[0] < col and len(ln.text) > 12:
                # the key letter merged onto the end of its stem row ("… surgical intervention   E")
                ln.text = ln.text[:mt.start()].rstrip()
                ln.key = mt.group(1)
                keep.append(ln)
                continue
            if m and ln.bbox[0] >= col:
                h = ln.bbox[3] - ln.bbox[1]
                row = [x for x in keep if x.page == ln.page and x.bbox[0] < col
                       and min(x.bbox[3], ln.bbox[3]) - max(x.bbox[1], ln.bbox[1]) > 0.5 * h]
                if row:
                    row[-1].key = m.group(1).upper()
                    continue
            keep.append(ln)
        return keep

    def _expand(self, lines: list[Line]) -> list[Line]:
        """Drop noise lines and split inline option runs into separate lines."""
        lines = self._key_column(lines)
        out: list[Line] = []
        by_page: dict[int, list[int]] = {}
        for i, ln in enumerate(lines):
            by_page.setdefault(ln.page, []).append(i)
        edges = {idx[0] for idx in by_page.values()} | {idx[-1] for idx in by_page.values()}
        self._edge2 = {i for idx in by_page.values() for i in idx[:2] + idx[-2:]}
        running = self._running_lines(lines, len(by_page))
        for i, ln in enumerate(lines):
            if any(rx.search(ln.text) for rx in self.stop):
                break
            if is_noise_line(ln.text, i in edges, self.skip) or (running and i in self._edge2
                                                                  and _running_key(ln.text) in running):
                self.dropped.append(ln.text)
                continue
            if self.keep_ar and len(re.findall(r"[A-Za-z]", ln.text)) > 3 * len(ARABIC.findall(ln.text)):
                text = re.sub(r"[\u0660-\u0669]", "", ARABIC.sub("", ln.text)).strip()   # English line: OCR strays
            elif self.keep_ar:
                text = arabic_markers(ln.text).strip()
            else:
                text = ARABIC.sub("", ln.text).strip()
            if is_grid_line(text):
                self.dropped.append(ln.text)
                continue
            if not re.search(rf"[A-Za-z0-9{AR_LETTERS if self.keep_ar else ''}]", text):
                if ln.text.strip():
                    self.dropped.append(ln.text)
                continue
            pieces = split_inline_options(text, self.p.get("options_inline", "auto"))
            if len(pieces) == 1:
                ln.text = text
                out.append(ln)
                continue
            for piece in pieces:
                out.append(Line(text=piece, page=ln.page, col=ln.col, bbox=ln.bbox, bold=ln.bold,
                                color=ln.color, marks=list(ln.marks), conf=ln.conf, size=ln.size,
                                split_option=bool(INLINE_OPT.match(piece))))
        return out

    def _accept_number(self, n: int) -> str | None:
        """'next' | 'section' | 'gap' | None."""
        if not self.sections:
            return "next" if n == 1 else ("gap" if n <= 3 else "start")   # "start": an excerpt from Q121 on
        # unnumbered questions since the last number (OCR lost their numbers) still advance the count
        base = self.sections[-1]
        last = base + self._unnumbered_since()
        if n == last + 1 or n == base + 1:
            return "next"
        if n == 1 and self.p.get("sections_restart", True) and last >= 2:
            return "section"
        if base + 1 < n <= last + 4:
            return "gap"
        return None

    def _unnumbered_since(self) -> int:
        k = 0
        for x in reversed(self.questions):
            if x.number is not None:
                break
            k += 1
        return k

    def _new_question(self, n: int | None, kind: str, line: Line, rest: str) -> Question:
        if kind == "start" and n is not None:
            self.sections.append(n - 1)
            self.starts.append(n)
        if kind == "section":
            self.sections.append(0)
            self.starts.append(1)
        if not self.sections:
            self.sections.append(0)
            self.starts.append(1)
        if kind == "gap" and n is not None:
            start = min(self.sections[-1] + self._unnumbered_since(), n - 1) + 1
            missing = list(range(start, n))
            if missing:
                self.gaps.append(f"section {len(self.sections)}: missing {missing}")
            else:
                kind = "next"      # the unnumbered questions before it fill the gap
        q = Question(number=n, section=len(self.sections))
        if n is not None:
            self.sections[-1] = n
        if kind == "gap":
            q.flags.append("numbering_gap_before")
        if rest.strip():
            q.stem_parts.append(Line(text=rest, page=line.page, col=line.col, bbox=line.bbox, bold=line.bold,
                                     color=line.color, marks=line.marks, conf=line.conf))
            if getattr(line, "key", None):
                q.stem_parts[-1].key = line.key
        else:
            q.stem_parts.append(Line(text="", page=line.page, col=line.col, bbox=line.bbox))
        self.questions.append(q)
        return q

    @staticmethod
    def _close(a: Line, b: Line) -> bool:
        """Is b the next visual line after a (same column, no paragraph gap)?"""
        if a.page != b.page or a.col != b.col:
            return b.page == a.page + 1 or (b.page == a.page and b.col == a.col + 1)
        h = max(a.bbox[3] - a.bbox[1], 6)
        return -2 <= b.bbox[1] - a.bbox[3] <= 1.1 * h

    def _wraps(self, last: Line, ln: Line, opt: Option) -> bool:
        """Is ln the wrapped continuation of option line `last` (not a new stem)?"""
        if not self._close(last, ln) or len(opt.parts) >= 4:
            return False
        if abs(ln.bold - last.bold) > 0.5:
            return False                       # bold stem after plain options (or the reverse)
        first = ln.text.lstrip()[:1]
        if ln.page != last.page and not first.islower():
            return False                       # a new page starts a new block unless the sentence runs on
        if first.islower() or first in "(,-/&" or first.isdigit():
            return True
        if ln.bbox[0] > last.bbox[0] + 6:
            return True                        # indented wrap
        right = self.margins.get((last.page, last.col), last.bbox[2])
        width = max(right - self.lefts.get((last.page, last.col), 0), 1)
        return last.bbox[2] >= right - 0.12 * width and not re.search(r"[.?:]$", last.text.strip())

    def _stem_block(self, pending: list[Line]) -> tuple[list[Line], list[Line]]:
        """Split buffered lines into (dropped head, stem) — the stem is the last paragraph."""
        if not pending:
            return [], []
        k = len(pending) - 1
        while k > 0 and self._close(pending[k - 1], pending[k]) and pending[k - 1].page == pending[k].page:
            k -= 1
        return pending[:k], pending[k:]

    def _keep_orphans(self, q: Question, letter: str) -> None:
        """Rows between two options that are not a wrap: never drop them.

        'b. …' / 'Local tissue infection' / 'd. …' — the pen covered the 'c.'; the orphan is option c and
        its tick is a strong hint of the marked answer. Anything else is kept as a wrap of the last option.
        """
        orphans, q.after[:] = q.after[:], []
        missing = LETTERS.index(letter) - len(q.options)
        if q.options and missing == 1 and self.lenient:
            new = LETTERS[len(q.options)]
            q.options.append(Option(letter=new, parts=orphans))
            q.flags.append(f"option_marker_repaired_{new}_from_orphan_possible_mark")
        elif q.options:
            q.options[-1].parts.extend(orphans)
            q.flags.append("orphan_rows_joined_to_option")
        else:
            q.stem_parts.extend(orphans)

    @staticmethod
    def _opt(letter: str, rest: str, ln: Line) -> Option:
        return Option(letter, [Line(text=rest, page=ln.page, col=ln.col, bbox=ln.bbox, bold=ln.bold,
                                    color=ln.color, marks=ln.marks, conf=ln.conf)])

    def _number(self, text: str) -> tuple[int, str] | None:
        """A question number at the start ('12.'), as a 'Question 12' header, or RTL at the end (' .12')."""
        if self.p.get("numbering") == "none":
            return None
        mq = self.q_rx.match(text)
        if mq:
            return qnum(mq), text[mq.end():]
        if self.lenient:
            # OCR confusions in the number itself: "L." → 1, "S." → 5, "\16)" → 16; only the expected next number
            mo = OCR_NUMBER.match(text)
            if mo:
                digits = mo.group(1).translate(OCR_DIGITS)
                if digits.isdigit() and self._accept_number(int(digits)) == "next":
                    return int(digits), text[mo.end():]
        mh = QUESTION_HEADER.match(text)
        if mh:
            return int(mh.group(1)), ""
        mr = RTL_NUMBER.search(text)
        if mr and self._accept_number(int(mr.group(1))) in ("next", "section", "start"):
            return int(mr.group(1)), text[:mr.start()]
        return None

    # ------------------------------------------------------------------ main
    def parse(self, lines: list[Line]) -> list[Question]:
        written = self.p.get("type") == "written"
        unnumbered_written = written and self.p.get("numbering") == "none"
        lines = self._expand(lines)
        self.margins: dict[tuple[int, int], float] = {}
        self.lefts: dict[tuple[int, int], float] = {}
        for ln in lines:
            key = (ln.page, ln.col)
            self.margins[key] = max(self.margins.get(key, 0), ln.bbox[2])
            self.lefts[key] = min(self.lefts.get(key, 1e9), ln.bbox[0])
        q: Question | None = None
        pending: list[Line] = []          # lines before the first question
        in_exp = False
        NUMOPT = re.compile(r"^\s*[(]?\s*([1-6])\s*[)(.\-]\s*(?=\S)")
        for li, ln in enumerate(lines):
            text = ln.text
            mnum = NUMOPT.match(text) if self.p.get("numeric_options") and q is not None else None
            if mnum and int(mnum.group(1)) == len(q.options) + 1 and not (self.q_end and self.q_end.search(text)):
                # numbered options "1) صح" / "2( خطأ": an option unless a stem ending ("؟", ":") follows
                # before the next numbered line (then it is a multi-line question stem)
                stem_like = False
                for nxt in lines[li + 1:li + 6]:
                    if NUMOPT.match(nxt.text) or self.o_rx.match(nxt.text):
                        break
                    if self.q_end and self.q_end.search(nxt.text):
                        stem_like = True
                        break
                if not stem_like:
                    text = ln.text = f"{'abcdef'[int(mnum.group(1)) - 1]}) {text[mnum.end():]}"
            num = self._number(text)
            if self.q_end and q is not None and len(q.options) >= 2 and self.q_end.search(text) \
                    and not self.o_rx.match(text) and not (num and self._accept_number(num[0]) == "next"):
                # profile question_end: a stem line ("…:" / "…؟") after an option run opens the next
                # question even when OCR destroyed its number ('"- من أمثلة …:')
                ln.text = re.sub(r"^(?:[^\u0600-\u06ffA-Za-z(]+|[VvIl]{1,2}\s)+", "", text).strip() or text
                q = Question(number=None, section=q.section, stem_parts=[ln], flags=["unnumbered", "stem_by_question_end"])
                self.questions.append(q)
                in_exp = False
                continue
            if num and self.lenient and q is not None and q.options and len(q.options) < 6 \
                    and self._accept_number(num[0]) == "gap":
                first = q.options[0].parts[0]
                if first.page == ln.page and first.col == ln.col and _edge_gap(ln, first) <= 8:
                    letter = LETTERS[len(q.options)]
                    q.options.append(self._opt(letter, num[1], ln))
                    q.flags.append(f"option_marker_repaired_{letter}")
                    continue
            if num and self.lenient and q is not None and len(q.options) >= 2 and not self._accept_number(num[0]):
                stems = [x.stem_parts[0] for x in self.questions[-4:] if x.stem_parts]
                if stems and all(_edge_gap(ln, st) <= 10 for st in stems[-2:]):
                    fixed = self.sections[-1] + self._unnumbered_since() + 1
                    q = self._new_question(fixed, "next", ln, num[1])
                    q.flags.append(f"number_corrected_from_{num[0]}")
                    in_exp = False
                    continue
            if num:
                kind = self._accept_number(num[0])
                if kind:
                    if q is None and pending:
                        self.dropped += [p.text for p in pending]
                        pending = []
                    q = self._new_question(num[0], kind, ln, num[1])
                    in_exp = False
                    continue
            if unnumbered_written:
                prev = q.stem_parts[-1] if q is not None and q.stem_parts else None
                new_item = prev is not None and not in_exp and not self.written_ans.match(text) and (
                    (re.search(r"[.?)]\s*$", prev.text) and text[:1].isupper()) or not self._close(prev, ln))
                if q is None or new_item:
                    q = Question(number=None, section=1, stem_parts=[ln], flags=["unnumbered"])
                    self.questions.append(q)
                    in_exp = False
                    continue
            if not written:
                ma = self.ans_rx.match(text)
                if ma and q is not None and (q.options or q.inline_answer is None):
                    q.inline_answer = ma.group(1).upper()
                    tail = text[ma.end():].strip(" .:-")
                    if tail:
                        q.exp_parts.append(Line(text=tail, page=ln.page, col=ln.col, bbox=ln.bbox))
                    in_exp = True
                    continue
                mt = self.ans_text_rx.match(text) if self.ans_text_rx else None
                if mt and q is not None and q.options and q.answer_text is None:
                    # the key given as the option's text; continuation rows follow in exp_parts
                    q.answer_text = mt.group(1).strip()
                    q.exp_parts.append(Line(text=mt.group(1).strip(), page=ln.page, col=ln.col, bbox=ln.bbox))
                    in_exp = True
                    continue
                mo = self.o_rx.match(text) or (TIGHT_DASH_OPT.match(text) if ln.split_option else None)
                if not mo and self.lenient and q is not None and q.options and len(q.options) < 6:
                    first = q.options[0].parts[0]
                    mg = OCR_MARKER.match(text)
                    letter = LETTERS[len(q.options)]
                    aligned = first.page == ln.page and first.col == ln.col and not q.after
                    if mg and aligned and _edge_gap(ln, first) <= 8:
                        q.options.append(self._opt(letter, text[mg.end():], ln))
                        q.flags.append(f"option_marker_repaired_{letter}")
                        continue
                    # "D Incision and drainage": the expected letter with its "." eaten by a pen tick —
                    # the option is real, and the tick is a strong hint that it is the marked answer
                    bare = BARE_MARKER(letter).match(text)
                    if bare and aligned and _edge_gap(ln, first) <= 14:
                        q.options.append(self._opt(letter, text[bare.end():], ln))
                        q.flags.append(f"option_marker_repaired_{letter}_bare_possible_mark")
                        continue
                if mo:
                    letter = mo.group(1).upper()
                    rest = text[mo.end():]
                    if q is None:
                        if letter != "A":
                            pending.append(ln)
                            continue
                        head, stem = self._stem_block(pending)
                        self.dropped += [p.text for p in head]
                        pending = []
                        q = Question(number=None, section=1, stem_parts=stem, flags=["unnumbered"])
                        self.questions.append(q)
                        if not self.sections:
                            self.sections.append(0)
                            self.starts.append(1)
                        q.options.append(self._opt(letter, rest, ln))
                        continue
                    expected = LETTERS[len(q.options)] if len(q.options) < len(LETTERS) else None
                    used = {o.letter for o in q.options}
                    reach = LETTERS.index(letter) <= len(q.options) + 2
                    restart = letter == "A" and len(q.options) >= 2
                    if letter == expected or (letter not in used and reach and not restart):
                        if not q.options and letter != "A":
                            q.flags.append(f"options_start_at_{letter}")
                        if q.after:
                            self._keep_orphans(q, letter)
                        q.options.append(self._opt(letter, rest, ln))
                        in_exp = False
                        continue
                    if restart:
                        # an unnumbered question: its stem is the text since the last option, or the
                        # lines that were taken as a wrap of the last option
                        stem = q.after[:]
                        q.after.clear()
                        flags = ["unnumbered"]
                        if not stem and len(q.options[-1].parts) > 1:
                            stem = q.options[-1].parts[1:]
                            q.options[-1].parts = q.options[-1].parts[:1]
                            flags.append("stem_recovered_from_option_wrap")
                        nq = Question(number=None, section=q.section, stem_parts=stem, flags=flags)
                        nq.options.append(self._opt("A", rest, ln))
                        self.questions.append(nq)
                        q = nq
                        in_exp = False
                        continue
                    q.flags.append(f"option_out_of_order_{letter}")
            elif q is not None and self.written_ans.match(text):
                in_exp = True
                tail = self.written_ans.sub("", text).strip()
                if tail:
                    q.exp_parts.append(Line(text=tail, page=ln.page, col=ln.col, bbox=ln.bbox))
                continue
            if q is None:
                pending.append(ln)
                continue
            # continuation text
            if in_exp:
                q.exp_parts.append(ln)
            elif q.options:
                opt = q.options[-1]
                if not q.after and self._wraps(opt.parts[-1], ln, opt):
                    opt.parts.append(ln)
                else:
                    q.after.append(ln)
            elif written and self.p.get("written", {}).get("answer_follows") and q.stem_parts \
                    and any(p.text for p in q.stem_parts) and not self._close(q.stem_parts[-1], ln):
                in_exp = True
                q.exp_parts.append(ln)
            else:
                q.stem_parts.append(ln)
        self.dropped += [p.text for p in pending]
        # form fields (name, seat number, college …) and Arabic-only items are not questions
        self.skipped: list[dict[str, Any]] = []
        keep = []
        for x in self.questions:
            raw = " ".join(p.text for p in x.stem_parts) + " " + " ".join(p.text for o in x.options for p in o.parts)
            if not re.search(rf"[A-Za-z{AR_LETTERS if self.keep_ar else ''}]{{3,}}",
                             raw if self.keep_ar else ARABIC.sub("", raw)):
                self.skipped.append({"number": x.number, "reason": "no English text (form field or Arabic-only item)"})
                continue
            keep.append(x)
        self.questions = keep
        # OCR dropped a number: unnumbered questions exactly filling a gap get the missing numbers
        i = 0
        qs = self.questions
        while i < len(qs):
            if qs[i].number is None:
                j = i
                while j < len(qs) and qs[j].number is None:
                    j += 1
                before = qs[i - 1].number if i > 0 else 0
                after = qs[j].number if j < len(qs) else None
                if after is not None and before is not None and qs[j].section == (qs[i - 1].section if i else qs[j].section) \
                        and after - before - 1 == j - i:
                    for k in range(i, j):
                        qs[k].number = before + (k - i) + 1
                        qs[k].flags = [f for f in qs[k].flags if f != "unnumbered"] + ["number_inferred"]
                    self.gaps = [g for g in self.gaps if not g.endswith(str(list(range(before + 1, after))))]
                i = j
            else:
                i += 1
        # an unnumbered first question followed by "2." is question 1
        numbered = [x for x in self.questions if x.number is not None]
        if self.questions and self.questions[0].number is None and numbered and numbered[0].number == 2:
            self.questions[0].number = 1
            self.questions[0].flags.remove("unnumbered")
        return self.questions


def _running_key(text: str) -> str:
    return re.sub(r"[^a-z]", "", re.sub(r"\d+", "", text.lower()))[:60] if len(text) <= 90 else ""


# --------------------------------------------------------------------------- finishing
def _repair_lost_marker(q: Question) -> None:
    """OCR only: 'a. …' / '<marker lost under a pen stroke> …' / 'c. …' — the lone wrap line is option b."""
    opts = q.options
    if opts and opts[0].letter == "B" and len(q.stem_parts) >= 2:
        # "…burn is:" / "A Early excision" (pen tick on the A) / "B. …": the last stem row is option A
        last, before = q.stem_parts[-1], q.stem_parts[-2]
        m = BARE_MARKER("A").match(last.text)
        # no letter at all ("…occlusion is:" / "Pain" / "B. Pallor"): the stem ended with ":" or "?"
        if not m and before.text.rstrip().endswith((":", "?")) and not last.text.rstrip().endswith((":", "?")):
            m = re.match(r"^\s*", last.text)
        if m and last.conf is not None and abs(last.bbox[0] - opts[0].parts[0].bbox[0]) <= 14:
            q.stem_parts.pop()
            opts.insert(0, Option(letter="A", parts=[Line(text=last.text[m.end():], page=last.page, col=last.col,
                                                          bbox=last.bbox, conf=last.conf, marks=last.marks)]))
            q.flags.append("option_marker_repaired_A_bare_possible_mark")
    if 2 <= len(opts) < 5 and 1 <= len(q.after) <= 3 and q.after[0].conf is not None:
        # "c. …" / "The metatarsophalangeal joint" (+ its wrap rows) / next question: the pen covered
        # the last marker
        tail, ref = q.after[0], opts[-1].parts[-1]
        if tail.page == ref.page and abs(tail.bbox[0] - opts[-1].parts[0].bbox[0]) <= 14 \
                and 0 <= tail.bbox[1] - ref.bbox[3] < 40:
            new = LETTERS[len(opts)]
            opts.append(Option(letter=new, parts=q.after[:]))
            q.after.clear()
            q.flags.append(f"option_marker_repaired_{new}_from_tail_possible_mark")
    for k in range(len(opts) - 1):
        a, b = opts[k], opts[k + 1]
        if ord(b.letter) - ord(a.letter) != 2 or len(a.parts) != 2:
            continue
        first, extra = a.parts
        if first.conf is None or extra.page != first.page or extra.bbox[1] - first.bbox[3] < -2:
            continue
        # the orphan starts where the option texts start (right of the markers) — or, when the tick
        # covered the whole marker, where the markers start; either way on its own row, between a and c
        if extra.bbox[0] > first.bbox[0] + 8 or abs(extra.bbox[0] - first.bbox[0]) <= 14:
            new = Option(letter=chr(ord(a.letter) + 1), parts=[extra])
            a.parts = [first]
            opts.insert(k + 1, new)
            q.flags.append(f"option_marker_repaired_{new.letter}_from_wrap_possible_mark")
            return


def finish(questions: list[Question], profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Clean texts, compute type and flags, and return JSON-able records."""
    out = []
    dehy = (lambda t: t)
    ar = bool(profile.get("keep_arabic"))
    clean_text = (lambda t, stem=False: _clean_text(t, stem=stem, keep_arabic=ar))
    if profile.get("glyph_repair"):
        from .glyphs import GlyphRepair
        dehy = GlyphRepair.dehyphenate
    for i, q in enumerate(questions, 1):
        if not q.inline_answer:                  # answers.key_column: the key printed beside the stem
            keys = [getattr(p, "key", None) for p in q.stem_parts if getattr(p, "key", None)]
            if len(keys) == 1:
                q.inline_answer = keys[0]
            elif len(set(keys)) > 1:
                q.flags.append("several_key_column_letters")
        _repair_lost_marker(q)                  # before the stem text: it may take the stem's last row
        stem = dehy(clean_text(" ".join(p.text for p in q.stem_parts if p.text), stem=True))
        cut = ""
        prev = next((x.number for x in reversed(questions[:i - 1]) if x.number is not None), 0)
        expected = q.number if q.number is not None else prev + 1
        if expected:
            # "<header / previous explanation> 9. All the following …": the real stem starts at its own number
            alias = r"[1lIL|]" if expected == 1 else str(expected)
            m = None
            for m in re.finditer(rf"(?:^|\s)\W?{alias}\s*[.),]\s+(?=[A-Z\"'(])", stem):
                pass
            if m and m.start() >= 15:
                cut, stem = stem[:m.start()].strip(), stem[m.end():].strip()
                q.flags.append("stem_prefix_cut")
                if q.number is None:
                    q.number = expected
                    q.flags = [f for f in q.flags if f != "unnumbered"] + ["number_from_stem"]
        _repair_lost_marker(q)
        if [o.letter for o in q.options] != sorted(o.letter for o in q.options):
            q.options.sort(key=lambda o: o.letter)   # 2×2 option grids arrive as a, c, b, d
        options = []
        for opt in q.options:
            text = dehy(clean_text(" ".join(p.text for p in opt.parts if p.text)))
            options.append({"letter": opt.letter, "text": text, **opt.style(),
                            "page": opt.parts[0].page, "bbox": list(opt.parts[0].bbox)})
        after = clean_text(" ".join(p.text for p in q.after))
        exp = dehy(clean_text(" ".join(p.text for p in q.exp_parts)))
        flags = list(dict.fromkeys(q.flags))
        forced = profile.get("type")
        qtype = "QCS" if len(options) >= 2 else "QROC"
        if forced == "written":
            qtype = "QROC"
        if forced == "mcq" and qtype == "QROC":
            flags.append("expected_mcq_but_no_options")
        if qtype == "QCS":
            letters = [o["letter"] for o in options]
            if letters != list(LETTERS[:len(letters)]):
                flags.append("letters_not_sequential")
            texts = [o["text"].lower() for o in options]
            if len(set(texts)) != len(texts):
                flags.append("duplicate_option_text")
            if any(len(o["text"]) < 2 for o in options):
                flags.append("empty_option")
            if any(len(o["text"]) > 300 for o in options):
                flags.append("very_long_option")
            if after:
                flags.append("text_after_options")
        elif len(options) == 1:
            flags.append("single_option")
        if not stem:
            flags.append("empty_stem")
        if len(stem) > 700:
            flags.append("very_long_stem")
        nxt = (q.number or 0) + 1
        if q.number is not None and re.search(rf"(?:^|\s){nxt}\s*[.)]\s+[A-Z]", stem):
            flags.append("possible_chimera")
        confs = [p.conf for p in q.stem_parts + [x for o in q.options for x in o.parts] if p.conf is not None]
        if confs and min(confs) < 0.60:
            flags.append("low_ocr_confidence")
        if FIGURE.search(stem):
            flags.append("figure_dependent")
        if qtype == "QROC" and not exp and not after:
            flags.append("written_without_model_answer")
        first = q.stem_parts[0] if q.stem_parts else None
        last_parts = [x for o in q.options for x in o.parts] or q.stem_parts
        y1 = max((x.bbox[3] for x in last_parts if x.page == (first.page if first else 0)), default=0)
        out.append({
            "i": i, "number": q.number, "section": q.section, "type": qtype, "stem": stem,
            "options": options, "after": after, "exp": exp or (after if qtype == "QROC" else ""),
            "inline_answer": q.inline_answer, "answer_text": exp if q.answer_text else None, "flags": flags, "cut_prefix": cut,
            "page": first.page if first else 0,
            "bbox": [first.bbox[0], first.bbox[1], max(x.bbox[2] for x in q.stem_parts + last_parts), y1]
            if first else None,
            "pages": sorted({x.page for x in q.stem_parts + last_parts}),
        })
    return out
