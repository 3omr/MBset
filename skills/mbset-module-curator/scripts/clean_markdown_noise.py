#!/usr/bin/env python3
"""Deep noise removal for canonical question markdown (`### Qn:` blocks).

Uses the same cleaning rules as the parser (`mbset/noise.py`): Moodle / scanner /
phone chrome, leading numbering, bubble artifacts, answer-key dumps, invisible
unicode, Arabic, and medical-notation repair (Ca²⁺, β1, µm, →).

Safety rules (the old version broke both):
  * `Correct Answer` is never invented — an unknown answer stays `?`.
  * When empty options are removed and the rest are repacked to A.., the correct
    letter moves with its option; if the correct option itself is removed the
    answer becomes `?` and the question is reported.

Default is a dry run that prints what would change; pass --write to apply.
Legacy `### Question N` files are converted to the canonical layout.

    python clean_markdown_noise.py --dir "<Module>/Markdown_Questions"            # report
    python clean_markdown_noise.py --dir "<Module>/Markdown_Questions" --write    # apply
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mbset.common import ARABIC  # noqa: E402
from mbset.noise import clean_text, is_noise_line  # noqa: E402

HEAD = re.compile(r"^###\s*Q(?:uestion)?\s*(\d+)\s*[:.]?\s*(.*)$", re.M)
OPT = re.compile(r"^\s*-\s*\*\*([A-Fa-f])\)\*\*\s*(.*)$")
FIELD = re.compile(r"^\*\*([A-Za-z /]+?)(?::\*\*|\*\*:)\s*(.*)$")
FIELD_NAMES = {"correct answer": "Correct Answer", "answer source": "Answer Source", "image": "Image",
               "source pages": "Source Pages", "exp": "EXP", "explanation": "EXP", "model answer": "EXP",
               "year": "Year", "tag": "Tag", "tagsuggere": "tagSuggere", "note": "Note"}


def _clean(text: str, stem: bool = False) -> str:
    return ARABIC.sub("", clean_text(text, stem=stem)).strip()


def clean_block(num: int, first: str, body: str, problems: list[str]) -> str | None:
    stem_lines = [first] if first.strip() else []
    options: list[tuple[str, str]] = []
    fields: dict[str, str] = {}
    current = "stem"
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip() == "---":
            continue
        m = OPT.match(line)
        f = FIELD.match(line.strip())
        if m:
            options.append((m.group(1).upper(), m.group(2)))
            current = "opt"
        elif f and f.group(1).strip().lower() in FIELD_NAMES:
            current = FIELD_NAMES[f.group(1).strip().lower()]
            fields[current] = f.group(2)
        elif current == "stem":
            if not is_noise_line(line):
                stem_lines.append(line.strip())
        elif current == "opt":
            options[-1] = (options[-1][0], options[-1][1] + " " + line.strip())
        else:                                   # continuation of a field (multi-line EXP)
            fields[current] = fields.get(current, "") + "\n" + line
    stem = _clean(" ".join(stem_lines), stem=True)
    if len(stem) < 3:
        problems.append(f"Q{num}: stem empty after cleaning — block dropped, check the source")
        return None
    correct = (fields.get("Correct Answer") or "").strip().upper()
    kept: list[tuple[str, str]] = []
    for letter, text in options:
        t = _clean(text)
        if t:
            kept.append((letter, t))
        elif letter == correct:
            problems.append(f"Q{num}: the correct option {letter} was empty — answer reset to ?")
            correct = "?"
    new_correct = correct
    if correct and correct not in ("?", "-"):
        old = [x for x, _ in kept]
        if correct in old:
            new_correct = "ABCDEF"[old.index(correct)]
        else:
            problems.append(f"Q{num}: Correct {correct} is not among its options — reset to ?")
            new_correct = "?"
    out = [f"### Q{num}: {stem}", ""]
    for i, (_, text) in enumerate(kept):
        out.append(f"- **{'ABCDEF'[i]})** {text}")
    if kept:
        out.append("")
        out.append(f"**Correct Answer:** {new_correct or '?'}")
        out.append(f"**Answer Source:** {fields.get('Answer Source', '').strip() or 'none'}")
    else:
        out.append("**Correct Answer:** -")
        if fields.get("Answer Source"):
            out.append(f"**Answer Source:** {fields['Answer Source'].strip()}")
    for name in ("Image", "Source Pages", "Year", "Tag", "tagSuggere", "Note"):
        if fields.get(name, "").strip():
            out.append(f"**{name}:** {fields[name].strip()}")
    if fields.get("EXP", "").strip():
        # keep numbered lists in model answers: clean line by line
        exp_lines = [ARABIC.sub("", ln).rstrip() for ln in fields["EXP"].strip().splitlines()]
        out.append("**EXP:** " + "\n".join(ln for ln in exp_lines if ln.strip()))
    return "\n".join(out + ["", "---", ""])


def clean_markdown(text: str) -> tuple[str, list[str]]:
    heads = list(HEAD.finditer(text))
    if not heads:
        return text, ([] if re.search(r"EXCLUDED|DUPLICATE", text[:400]) else ["no question headings found"])
    head = ARABIC.sub("", text[:heads[0].start()])
    problems: list[str] = []
    blocks = []
    for j, m in enumerate(heads):
        body = text[m.end():heads[j + 1].start() if j + 1 < len(heads) else len(text)]
        b = clean_block(len(blocks) + 1, m.group(2), body, problems)
        if b:
            blocks.append(b)
    return head.rstrip() + "\n\n" + "\n".join(blocks).rstrip() + "\n", problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file")
    ap.add_argument("--dir")
    ap.add_argument("--pattern", default="*.md")
    ap.add_argument("--write", action="store_true", help="apply the changes (default: dry run)")
    ap.add_argument("--diff", action="store_true", help="print a unified diff per file")
    args = ap.parse_args()
    files = [Path(args.file)] if args.file else sorted(p for p in Path(args.dir).glob(args.pattern)
                                                       if not p.name.startswith("00_")) if args.dir else []
    if not files:
        ap.print_help()
        return 1
    changed = 0
    for p in files:
        old = p.read_text(encoding="utf-8", errors="replace")
        new, problems = clean_markdown(old)
        if new != old:
            changed += 1
            n = sum(1 for _ in difflib.unified_diff(old.splitlines(), new.splitlines(), n=0)) // 2
            print(f"[{'+' if args.write else '~'}] {p.name}: ~{n} changed line(s)")
            if args.diff:
                sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), p.name, p.name))
            if args.write:
                p.write_text(new, encoding="utf-8")
        for pr in problems:
            print(f"    ! {p.name}: {pr}")
    print(f"[=] {changed}/{len(files)} file(s) {'cleaned' if args.write else 'would change (dry run; --write to apply)'}")
    print("    note: a markdown written by mbset.py records its hash — run `mbset.py parse` again or accept it with --force")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
