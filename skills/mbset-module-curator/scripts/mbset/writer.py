"""Canonical markdown writer and small in-place editors.

The written format is exactly what `build_module_template.py` parses:

    ### Q1: <stem>

    - **A)** option
    - **B)** option

    **Correct Answer:** B
    **Answer Source:** key
    **Image:** Images/05_Q1.png
    **Source Pages:** 3
    **EXP:** explanation / model answer

    ---

Unanswered MCQs are written as `**Correct Answer:** ?` / `**Answer Source:** none`
so every gate fails loudly until the agent resolves them. A markdown file that was
edited after the parser wrote it is never overwritten without --force (a backup
is kept in .mbset/work/backup/).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

from .common import Module, now, text_hash


def render(src: dict[str, Any], records: list[dict[str, Any]], title: str | None = None) -> str:
    mcq = [r for r in records if r["type"] == "QCS"]
    srcs: dict[str, int] = {}
    for r in mcq:
        key = r.get("answer_source") or "none"
        srcs[key] = srcs.get(key, 0) + 1
    title = title or Path(src["rel"]).stem
    out = [f"# {title} — extracted questions", "",
           f"> Source: `{Path(src['rel']).name}` · index {src['nn']} · parsed {now()[:10]} by mbset.py",
           f"> Questions: {len(records)} ({len(mcq)} MCQ / {len(records) - len(mcq)} written) · answers: "
           + ", ".join(f"{k} {v}" for k, v in sorted(srcs.items())), ""]
    for n, r in enumerate(records, 1):
        out.append(f"### Q{n}: {r['stem']}")
        out.append("")
        if r["type"] == "QCS":
            for i, o in enumerate(r["options"][:6]):
                out.append(f"- **{'ABCDEF'[i]})** {o['text']}")
            if len(r["options"]) > 6:
                # more than A-F is almost always two questions glued together: keep the text visible
                # for the reviewer (split with a profile fix or drop); `check` fails while it is here
                extra = " | ".join(o["text"] for o in r["options"][6:])
                out.append(f"**Extra Options (split or drop):** {extra}")
            out.append("")
            correct = r.get("correct")
            letters = [o["letter"] for o in r["options"]]
            if correct in letters:
                # options are repacked to A.. in order, so map the letter by position
                pos = letters.index(correct)
                correct = "ABCDEF"[pos] if pos < 6 else None
            else:
                correct = None
            out.append(f"**Correct Answer:** {correct or '?'}")
            out.append(f"**Answer Source:** {r.get('answer_source') or 'none'}")
        else:
            out.append("**Correct Answer:** -")
            if r.get("exp_source"):
                out.append(f"**Answer Source:** {r['exp_source']}")
        if r.get("image"):
            out.append(f"**Image:** {r['image']}")
        pages = ", ".join(str(p + 1) for p in r.get("pages", []))
        if pages:
            out.append(f"**Source Pages:** {pages}")
        if r.get("exp"):
            out.append(f"**EXP:** {r['exp']}")
        out += ["", "---", ""]
    return "\n".join(out).rstrip() + "\n"


def write(module: Module, src: dict[str, Any], text: str, force: bool = False) -> tuple[bool, str]:
    path = module.md_path(src)
    path.parent.mkdir(parents=True, exist_ok=True)
    last = src.get("stages", {}).get("parse", {}).get("md_hash")
    if path.exists():
        current = text_hash(path.read_text(encoding="utf-8"))
        edited = last is None or current != last
        if edited and not force:
            return False, (f"{path.name} exists and was edited after the last parse "
                           f"(or predates mbset.py) — keeping it; pass --force to replace (a backup is kept)")
        backup = module.meta / "work" / "backup" / f"{path.stem}.{now().replace(':', '')}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    path.write_text(text, encoding="utf-8")
    return True, str(path)


# --------------------------------------------------------------------------- editing
def md_numbers_by_stem(path: Path) -> dict[str, int]:
    """Markdown Q number of every stem (numbers shift after --drop; stems do not)."""
    out: dict[str, int] = {}
    for m in re.finditer(r"^### Q(\d+):\s*(.*)$", path.read_text(encoding="utf-8"), re.M):
        out.setdefault(m.group(2).strip(), int(m.group(1)))
    return out


BLOCK = re.compile(r"^### Q(\d+):.*?(?=^### Q\d+:|\Z)", re.S | re.M)


def _blocks(text: str) -> tuple[str, list[str]]:
    blocks = [m.group(0) for m in BLOCK.finditer(text)]
    head = text[:BLOCK.search(text).start()] if blocks else text
    return head, blocks


def _renumber(blocks: list[str]) -> list[str]:
    return [re.sub(r"^### Q\d+:", f"### Q{i}:", b, count=1, flags=re.M) for i, b in enumerate(blocks, 1)]


def _set_field(block: str, name: str, value: str) -> str:
    rx = re.compile(rf"^\*\*{re.escape(name)}:\*\*.*$", re.M)
    if rx.search(block):
        return rx.sub(f"**{name}:** {value}", block, count=1)
    anchor = re.search(r"^\*\*(?:Source Pages|EXP):\*\*", block, re.M) or re.search(r"^---\s*$", block, re.M)
    line = f"**{name}:** {value}\n"
    if anchor:
        return block[:anchor.start()] + line + block[anchor.start():]
    return block.rstrip() + "\n" + line


def _set_exp(block: str, value: str) -> str:
    """EXP may span several lines (numbered model answers): replace up to the block separator."""
    value = value.strip()
    rx = re.compile(r"^\*\*EXP:\*\*.*?(?=^---\s*$|\Z)", re.S | re.M)
    if rx.search(block):
        return rx.sub(lambda _: f"**EXP:** {value}\n\n", block, count=1)
    sep = re.search(r"^---\s*$", block, re.M)
    line = f"**EXP:** {value}\n\n"
    return block[:sep.start()].rstrip() + "\n" + line + block[sep.start():] if sep else block.rstrip() + "\n" + line


def edit(path: Path, answers: dict[int, tuple[str, str]] | None = None, images: dict[int, str] | None = None,
         drop: set[int] | None = None, exps: dict[int, tuple[str, str]] | None = None) -> str:
    """answers {n: (letter, source)}, images {n: path}, exps {n: (text, source)}, drop {n} — n = markdown Q number."""
    text = path.read_text(encoding="utf-8")
    head, blocks = _blocks(text)
    for n, (letter, source) in (answers or {}).items():
        b = blocks[n - 1]
        letters = re.findall(r"^\s*-\s*\*\*([A-F])\)\*\*", b, re.M)
        if letter != "-" and letter not in letters:
            raise SystemExit(f"[-] Q{n}: {letter} is not among its options {letters}")
        b = _set_field(b, "Correct Answer", letter)
        blocks[n - 1] = _set_field(b, "Answer Source", source)
    for n, (exp, source) in (exps or {}).items():
        b = _set_exp(blocks[n - 1], exp)
        blocks[n - 1] = _set_field(b, "Answer Source", source) if source else b
    for n, img in (images or {}).items():
        blocks[n - 1] = _set_field(blocks[n - 1], "Image", img)
    if drop:
        blocks = [b for i, b in enumerate(blocks, 1) if i not in drop]
        blocks = _renumber(blocks)
    new = head + "".join(b if b.endswith("\n") else b + "\n" for b in blocks)
    path.write_text(new, encoding="utf-8")
    return new
