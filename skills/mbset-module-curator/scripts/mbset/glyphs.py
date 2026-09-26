"""Repair text layers whose font lost some glyphs (profile `glyph_repair: [f, fi, ff, fl, ffi, Th]`).

Some exported books (e.g. a Schwartz review) have no Unicode mapping for `f`, the `fi/ff/fl/ffi`
ligatures and `Th`: the glyph comes out as a space — "T e undamental principles o  leadership",
"e ective", "Pro essor". The repair is deterministic and dictionary-checked: a missing glyph is put
back only where the joined word is a real word (hunspell en_US, the system word list, and every word
already in this repository's question banks) and the split pieces are not. Nothing else changes.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

WORD = re.compile(r"[A-Za-z]+")
EDGE = re.compile(r"^([^A-Za-z]*)(.*?)([^A-Za-z]*)$", re.S)


@lru_cache(maxsize=1)
def _system() -> frozenset[str]:
    words: set[str] = set()
    for dic in ("/usr/share/dict/american-english", "/usr/share/dict/british-english", "/usr/share/dict/words"):
        p = Path(dic)
        if p.exists():
            words.update(w.strip().lower() for w in p.read_text(errors="ignore").splitlines() if w.strip().isalpha())
    return frozenset(words)


@lru_cache(maxsize=1)
def _vocab() -> frozenset[str]:
    """System words + medical words already in the question banks (only ever used for the JOINED word:
    banks extracted from broken books contain fragments like 'ective', which must never count as a
    word on their own)."""
    words = set(_system())
    repo = Path(__file__).resolve().parents[5]            # …/MBset
    for md in repo.glob("*/*/Markdown_Questions/*.md"):
        try:
            words.update(w.lower() for w in WORD.findall(md.read_text(errors="ignore")) if len(w) >= 3)
        except OSError:
            pass
    return frozenset(words)


@lru_cache(maxsize=1)
def _enchant():
    try:
        import enchant
        return enchant.Dict("en_US")
    except Exception:
        return None


@lru_cache(maxsize=200_000)
def is_word(w: str, strict: bool = False) -> bool:
    """strict: system dictionaries only (for judging the split pieces)."""
    core = EDGE.match(w).group(2)
    if not core or not core.isalpha():
        return False
    low = core.lower()
    if low in (_system() if strict else _vocab()):
        return True
    d = _enchant()
    return bool(d and len(core) > 1 and (d.check(core) or d.check(low)))


def piece(w: str) -> bool:
    return is_word(w, strict=True)


def best(cands: list[str]) -> str | None:
    """A system-dictionary word first; a word known only from the banks as a fallback."""
    return next((c for c in cands if piece(c)), None) or next((c for c in cands if is_word(c)), None)


class GlyphRepair:
    def __init__(self, fillers: list[str]):
        self.lower = [f for f in fillers if f and f[0].islower()]
        self.th = any(f.lower() == "th" for f in fillers)

    def _join(self, a: str, b: str) -> str | None:
        """a + <missing glyph> + b, when that is a word and a or b alone is not."""
        if a == "T" and self.th and b[:1].islower():
            if is_word("Th" + b):
                return "Th" + b
        if a[-1:].isalpha() and b[:1].isalpha() and (not (piece(a) and piece(b)) or min(len(a), len(b)) == 1):
            return best([a + x + b for x in sorted(self.lower, key=len)])
        return None

    def _suffix(self, a: str) -> str | None:
        """'o' + missing 'f' before a real space → 'of'; 'Chie' → 'Chief'."""
        if not a[-1:].isalpha():
            return None
        if piece(a) and a.lower() not in ("o", "i"):
            return None
        return best([a + x for x in sorted(self.lower, key=len)])

    def _prefix(self, b: str) -> str | None:
        """missing glyph at the start of a word: ' undamental' → 'fundamental'."""
        if not b[:1].isalpha() or piece(b):
            return None
        cands = [(x.capitalize() if b[:1].isupper() else x) + b for x in sorted(self.lower, key=len)]
        if self.th and b[:1].islower():                  # "ime management" → "Time", " is" stays
            cands += ["T" + b, "Th" + b]
        return best(cands)

    @staticmethod
    def _inner(tok: str) -> str:
        """'afer', 'fuid', 'frst', 'defciency': the ligature kept only its 'f' (ft, fl, fi, ff)."""
        pre, core, post = EDGE.match(tok).groups()
        if not core or "f" not in core.lower() or piece(core) or not core.isalpha():
            return tok
        cands = [core[:i + 1] + extra + core[i + 1:] for i, ch in enumerate(core) if ch.lower() == "f"
                 for extra in ("i", "l", "t", "f")]
        w = best(cands)
        return pre + w + post if w else tok

    def repair(self, text: str) -> str:
        return " ".join(self._inner(t) for t in self._spaces(text).split(" "))

    @staticmethod
    def dehyphenate(text: str) -> str:
        """'stan- dards', 'po- tassium' (a line-break hyphen inside a wrapped stem) → one word, when the
        joined word is in the system dictionary and the pieces are not both words ('anti- inflammatory' stays)."""
        def join(m: re.Match) -> str:
            a, b = m.group(1), m.group(2)
            return a + b if piece(a + b) and not (piece(a) and piece(b)) else m.group(0)
        return re.sub(r"\b([A-Za-z]{2,})- ([a-z]{2,})\b", join, text)

    def _spaces(self, text: str) -> str:
        toks = text.split(" ")
        head = EDGE.match(toks[0]).group(2) if toks[0] else ""
        if head and not piece(head) and head.isalpha():         # "ime management": lost at the line start
            w = self._prefix(head)
            if w:
                toks[0] = toks[0].replace(head, w, 1)
        out: list[str] = []
        i = 0
        while i < len(toks):
            cur = toks[i]
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            if cur and nxt == "" and i + 2 < len(toks):             # "o  this": glyph lost before a real space
                w = self._suffix(cur)
                if w:
                    out.append(w)
                    i += 2
                    continue
            if cur and nxt:
                pre, a, _ = EDGE.match(cur).groups()
                _, b, post = EDGE.match(nxt).groups()
                if cur.endswith(a) and nxt.startswith(b) and a and b:
                    w = self._join(a, b)
                    if w:
                        toks[i + 1] = pre + w + post
                        i += 1
                        continue
            if cur == "" and nxt and (not out or out[-1] != ""):  # "  undamental": lost at a word start
                w = self._prefix(nxt)
                if w:
                    toks[i + 1] = w
                    i += 1
                    continue
            out.append(cur)
            i += 1
        return " ".join(out)
