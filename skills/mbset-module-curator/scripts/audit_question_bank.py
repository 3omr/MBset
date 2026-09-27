#!/usr/bin/env python3
"""
MBset Forensic Question Bank Auditor
====================================

Goes beyond schema validation (`validate_questions_excel.py`) and catches the
defects that a schema check passes: fabricated answer keys, surviving duplicates,
residual OCR/web noise, figure-dependent questions with no image, and mangled
medical notation.

Usage
-----
    python audit_question_bank.py --excel CVS/CVS_Questions.xlsx
    python audit_question_bank.py --excel CVS/CVS_Questions.xlsx --by-tag
    python audit_question_bank.py --markdown CVS/Markdown_Questions
    python audit_question_bank.py --excel a.xlsx --json report.json

Exit code 0 when clean, 1 when any hard failure is found.
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

try:
    import openpyxl
except ImportError:
    openpyxl = None

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
FIGURE = re.compile(r"(?i)\b(figure|fig\.|diagram|shown below|this slide|arrow|labell?ed|"
                    r"photomicrograph|following image|following picture|the picture)\b")
MANGLED = re.compile(r"(?:Ca|Na|K|Cl|Mg|HCO3|H)\s*\*{1,2}(?!\w)")
NOISE = {
    "moodle/LMS chrome": r"(?i)moodle|my courses|quick links|lorem ipsum|flag question|"
                         r"clear my choice|select one|finish attempt",
    "quiz metrics": r"(?i)\bmarks?\s*=|time taken|state\s+finished|grade\s+\d+[\.\d]*\s+out\s+of",
    "phone clock": r"\b\d{1,2}:\d{2}\s*(AM|PM)\b",
    "source watermark": r"(?i)docreader|doc-reader-guide",
    "url": r"https?://",
    "markdown markers": r"\*\*|^\s*[-•]\s*\*\*[A-F]\)",
    "leading numbering": r"^\s*(Q\s*)?\d{1,3}\s*[\.\)\-]\s+\S",
    "answer-key grid": r"(?:\b[A-E]\s+){5,}[A-E]\b",
}
BIAS_INVESTIGATE = 0.45
BIAS_FAIL = 0.60

CANON = ['id', 'Cas', 'Text', 'Image', 'explanationImage', 'A', 'B', 'C', 'D', 'E', 'F',
         'A_EXP', 'B_EXP', 'C_EXP', 'D_EXP', 'E_EXP', 'F_EXP', 'Correct', 'Hint', 'EXP',
         'Note', 'Type', 'categoryId', 'categoryName', 'subcategoryId', 'subcategoryName',
         'tagSuggere', 'Year', 'Tag', 'ImageMasks', 'ExplanationImageMasks', 'ModelAnswer']


def norm_stem(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


# --------------------------------------------------------------------------- Excel

def read_excel(path):
    if openpyxl is None:
        sys.exit("openpyxl is required: pip install openpyxl")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        sys.exit(f"{path}: empty sheet")
    hdr = [str(h).strip() if h is not None else "" for h in rows[0]]
    data = [r for r in rows[1:] if r and any(c is not None and str(c).strip() for c in r)]
    return hdr, data


def bias_table(pairs):
    """pairs: [(group, correct_letter)] -> {group: (n, Counter)}"""
    per = collections.defaultdict(collections.Counter)
    for g, c in pairs:
        per[g][c] += 1
    return per


def report_bias(per, min_n=15):
    hard, soft = [], []
    lines = []
    for g, c in sorted(per.items(), key=lambda x: -sum(x[1].values())):
        n = sum(c.values())
        if n < min_n:
            continue
        letter, cnt = c.most_common(1)[0]
        share = cnt / n
        dist = "  ".join(f"{L}{100*c[L]/n:3.0f}%" for L in "ABCDEF" if c[L])
        flag = ""
        if share > BIAS_FAIL:
            flag = "  <== FAIL (placeholder key)"
            hard.append(f"{g}: {letter}={100*share:.0f}% over {n} MCQs")
        elif share > BIAS_INVESTIGATE:
            flag = "  <-- investigate"
            soft.append(f"{g}: {letter}={100*share:.0f}% over {n} MCQs")
        lines.append(f"    {g[:44]:44} n={n:5}  {dist}{flag}")
    return lines, hard, soft


def audit_excel(path, by_tag):
    hdr, data = read_excel(path)
    H = {h: i for i, h in enumerate(hdr) if h}
    g = lambda r, k: (r[H[k]] if k in H and H[k] < len(r) else None)
    hard, soft, info = [], [], []

    print("=" * 78)
    print(f"EXCEL AUDIT: {path}")
    print(f"  rows: {len(data)}   columns: {len(hdr)}")

    if hdr[:len(CANON)] != CANON:
        diff = [f"col {i}: '{hdr[i] if i < len(hdr) else ''}' != '{CANON[i]}'"
                for i in range(len(CANON)) if i >= len(hdr) or hdr[i] != CANON[i]]
        hard.append("header is not the canonical 32-column layout")
        print("  [-] HEADER MISMATCH (legacy layout?):")
        for d in diff[:6]:
            print(f"        {d}")
        if len(diff) > 6:
            print(f"        ... and {len(diff)-6} more")
    else:
        print("  [+] canonical 32-column header")

    types = collections.Counter(g(r, "Type") for r in data)
    print(f"  Type: {dict(types)}")

    # --- answer distribution
    pairs = []
    for r in data:
        if g(r, "Type") != "QCS":
            continue
        tag = str(g(r, "Tag") or "")
        parts = [p.strip() for p in tag.split(",")]
        group = (parts[1] if by_tag and len(parts) > 1 else (parts[0] if by_tag else "ALL"))
        pairs.append((group or "(untagged)", str(g(r, "Correct") or "?")))
    per = bias_table(pairs)
    print("  Answer distribution:")
    lines, h, s = report_bias(per)
    for ln in lines:
        print(ln)
    hard += h
    soft += s

    # --- per-row defects
    probs = collections.Counter()
    examples = {}

    def note(key, row_i, snippet=""):
        probs[key] += 1
        examples.setdefault(key, (row_i, snippet[:90]))

    for i, r in enumerate(data, start=2):
        t = g(r, "Type")
        text = str(g(r, "Text") or "")
        opts = {L: str(g(r, L) or "").strip() for L in "ABCDEF"}
        filled = [L for L in "ABCDEF" if opts[L]]
        blob = " ".join(str(g(r, c) or "") for c in ("Text", "A", "B", "C", "D", "E", "F", "EXP") if c in H)

        if ARABIC.search(blob):
            note("Arabic characters", i, text)
        if len(text.strip()) < 10:
            note("stem under 10 chars", i, text)
        if MANGLED.search(blob):
            note("mangled super/subscript (Ca**, Na*)", i, text)
        if FIGURE.search(text) and not str(g(r, "Image") or "").strip():
            note("figure-dependent question without Image", i, text)
        if g(r, "id") is not None and str(g(r, "id")).strip():
            note("id not empty", i)
        for col in ("subcategoryId", "subcategoryName"):
            if g(r, col) is not None and str(g(r, col)).strip():
                note(f"{col} not empty", i)
        if not str(g(r, "Tag") or "").strip():
            note("empty Tag", i, text)
        if g(r, "Year") in (None, ""):
            note("empty Year", i, text)

        if t == "QCS":
            if len(filled) < 2:
                note("MCQ with fewer than 2 options", i, text)
            elif filled != list("ABCDEF"[:len(filled)]):
                note("option letter gap", i, text)
            c = str(g(r, "Correct") or "").strip()
            if c not in filled:
                note("Correct not among options", i, text)
            if len(set(opts[L].lower() for L in filled)) < len(filled):
                note("duplicate options", i, text)
            if any(len(opts[L]) < 2 for L in filled):
                note("option under 2 chars", i, text)
        elif t == "QROC":
            if filled:
                note("QROC carries options", i, text)
            if str(g(r, "Correct") or "").strip():
                note("QROC Correct is not empty", i, text)
            if str(g(r, "EXP") or "").strip():
                note("QROC EXP is not empty", i, text)
            if not str(g(r, "ModelAnswer") or "").strip():
                note("QROC without model answer", i, text)
        else:
            note("invalid Type", i, text)

        for name, pat in NOISE.items():
            if name == "markdown markers" and t == "QROC":
                continue  # model answers may legitimately use lists
            target = text if name in ("leading numbering",) else blob
            if re.search(pat, target, re.M):
                note(f"noise: {name}", i, text)
                break

    dup = collections.Counter(norm_stem(g(r, "Text")) for r in data)
    ndup = sum(v - 1 for v in dup.values() if v > 1)
    if ndup:
        probs["duplicate normalized stems"] = ndup

    HARD_KEYS = {"Arabic characters", "Correct not among options", "option letter gap",
                 "MCQ with fewer than 2 options", "QROC Correct is not empty", "QROC EXP is not empty", "invalid Type",
                 "id not empty", "duplicate normalized stems",
                 "figure-dependent question without Image", "empty Tag"}
    print("  Row defects:" if probs else "  Row defects: none")
    for k, v in probs.most_common():
        ex = examples.get(k)
        loc = f"  e.g. row {ex[0]}: {ex[1]!r}" if ex else ""
        mark = "[-]" if k in HARD_KEYS else "[!]"
        print(f"    {mark} {k}: {v}{loc}")
        (hard if k in HARD_KEYS else soft).append(f"{k}: {v}")

    return hard, soft, {"rows": len(data), "types": {str(k): v for k, v in types.items()},
                        "defects": dict(probs)}


# ------------------------------------------------------------------------ Markdown

Q_RE = re.compile(r"^###\s*Q(\d+)\b", re.M)
CORRECT_RE = re.compile(r"^\*\*Correct Answer:\*\*\s*(\S+)", re.M)
SRC_RE = re.compile(r"^\*\*Answer Source:\*\*\s*(\w+)", re.M)


def audit_markdown(dirpath):
    hard, soft = [], []
    files = sorted(f for f in glob.glob(os.path.join(dirpath, "*.md"))
                   if not os.path.basename(f).startswith("00_"))
    print("=" * 78)
    print(f"MARKDOWN AUDIT: {dirpath}  ({len(files)} files)")
    grand = collections.Counter()
    for fp in files:
        txt = open(fp, encoding="utf-8").read()
        nums = [int(n) for n in Q_RE.findall(txt)]
        answers = CORRECT_RE.findall(txt)
        sources = collections.Counter(SRC_RE.findall(txt))
        mcq = [a for a in answers if a not in ("-", "", "None")]
        name = os.path.basename(fp)
        issues, warnings = [], []
        if nums and nums != list(range(1, len(nums) + 1)):
            issues.append("numbering not continuous 1..N")
            hard.append(f"{name}: numbering not continuous")
        if len(answers) != len(nums):
            issues.append(f"{len(nums)} questions but {len(answers)} answers")
            hard.append(f"{name}: questions/answers mismatch")
        if ARABIC.search(txt):
            issues.append("Arabic characters")
            hard.append(f"{name}: Arabic characters")
        missing_src = len(mcq) - sum(sources.values())
        if missing_src > 0:
            warnings.append(f"{missing_src} MCQs without **Answer Source:**")
            soft.append(f"{name}: {missing_src} MCQs without provenance")
        dist = collections.Counter(mcq)
        bias = ""
        if len(mcq) >= 15:
            L, c = dist.most_common(1)[0]
            share = c / len(mcq)
            if share > BIAS_FAIL:
                bias = f"  <== FAIL {L}={100*share:.0f}%"
                hard.append(f"{name}: {L}={100*share:.0f}% of {len(mcq)} MCQs")
            elif share > BIAS_INVESTIGATE:
                bias = f"  <-- {L}={100*share:.0f}%"
                soft.append(f"{name}: {L}={100*share:.0f}% of {len(mcq)} MCQs")
        grand.update(sources)
        srcs = " ".join(f"{k}={v}" for k, v in sorted(sources.items())) or "no provenance"
        print(f"  {name[:46]:46} Q={len(nums):4} MCQ={len(mcq):4}  {srcs}{bias}")
        for i in issues:
            print(f"      [-] {i}")
        for w in warnings:
            print(f"      [!] {w}")
    if grand:
        print(f"  Provenance totals: {dict(grand)}")
        if grand.get("derived"):
            soft.append(f"{grand['derived']} answers are 'derived' — report to the user")
    return hard, soft, {"files": len(files), "provenance": dict(grand)}


def main():
    ap = argparse.ArgumentParser(description="Forensic audit of an MBset question bank")
    ap.add_argument("--excel", help="path to <Module>_Questions.xlsx")
    ap.add_argument("--markdown", help="path to <Module>/Markdown_Questions directory")
    ap.add_argument("--by-tag", action="store_true",
                    help="break the answer distribution down by source tag (recommended)")
    ap.add_argument("--json", help="write a machine-readable report here")
    args = ap.parse_args()
    if not args.excel and not args.markdown:
        ap.error("give --excel and/or --markdown")

    hard, soft, payload = [], [], {}
    if args.markdown:
        h, s, p = audit_markdown(args.markdown)
        hard += h; soft += s; payload["markdown"] = p
    if args.excel:
        h, s, p = audit_excel(args.excel, args.by_tag or True)
        hard += h; soft += s; payload["excel"] = p

    print("=" * 78)
    if hard:
        print(f"RESULT: FAIL — {len(hard)} hard finding(s)")
        for x in hard[:25]:
            print(f"  [-] {x}")
    else:
        print("RESULT: PASS — no hard findings")
    if soft:
        print(f"  {len(soft)} warning(s):")
        for x in soft[:25]:
            print(f"  [!] {x}")

    if args.json:
        payload["hard"] = hard
        payload["soft"] = soft
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        print(f"  report written to {args.json}")

    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
