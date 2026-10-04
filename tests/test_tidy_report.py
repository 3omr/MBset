"""Tests for `tidy`, `report`, `crossdup` and `doctor` on synthetic temp modules.

Run:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = next(p for p in (Path(__file__).resolve().parents[1] / d / "mbset-module-curator/scripts"
                for d in (".agents/skills", "skills")) if p.exists())
sys.path.insert(0, str(SCRIPTS))

from mbset import crossdup, doctor, report, tidy  # noqa: E402
from mbset.common import Module  # noqa: E402

MD_REAL = """# Real — extracted questions

### Q1: Which hormone is secreted by the posterior pituitary?

- **A)** ACTH
- **B)** ADH
- **C)** TSH

**Correct Answer:** B
**Answer Source:** key

---

### Q2: Name the hormone deficient in Addison disease.

**Correct Answer:** -
**Answer Source:** derived
**EXP:** Cortisol (and aldosterone).

---

### Q3: The structure shown in the figure is

- **A)** Thyroid
- **B)** Adrenal

**Correct Answer:** A
**Answer Source:** derived
**Image:** Images/01_Q3.png

---
"""

PLACEHOLDER = """# Excluded source record

**Status:** EXCLUDED — unreadable scan.

No question rows were created from this source.
"""


def write(path: Path, data: bytes | str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.write_bytes if isinstance(data, bytes) else path.write_text)(data)
    return path


def snapshot(root: Path) -> dict[str, str]:
    """relative path → sha256 of every file outside .mbset/ and _trash/."""
    out = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if p.is_file() and rel.parts[0] not in (".mbset", "_trash"):
            out[str(rel)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def make_module(base: Path, name: str = "Endo") -> Path:
    m = base / name
    write(m / "Raw_PDF_Questions/a.pdf", b"%PDF raw a")
    write(m / "Raw_PDF_Questions/b.pdf", b"%PDF raw b")
    write(m / "Book/a copy.pdf", b"%PDF raw a")                       # all duplicates → trash whole
    write(m / "Questions/a.pdf", b"%PDF raw a")                       # mixed folder
    write(m / "Questions/new source.pdf", b"%PDF unique c")
    write(m / "Questions/notes.xlsx", b"xlsx bytes")
    write(m / "Lectures/L1.pdf", b"%PDF lecture 1 old")
    write(m / "Lectures_OCR_Upload/L1.pdf", b"%PDF lecture 1")
    write(m / "Lectures_OCR_Upload/L2.pdf", b"%PDF lecture 2")
    write(m / "Lectures_PreOfficialNames_2026-09-18/x.pdf", b"%PDF something else")
    write(m / "Lecture_PowerPoint_PDF_Staging/y.pdf", b"%PDF lecture 1 old")
    write(m / "Lectures_Other/z.pdf", b"%PDF not a lecture dup")
    write(m / "OCR_PDF/a_ocr.pdf", b"%PDF ocr")
    write(m / "OCR_Text/a.txt", "ocr text")
    write(m / "Telegram_Staging/dl/a.pdf", b"%PDF raw a")
    write(m / "Telegram_Staging/dl/slides.pptx", b"pptx")
    write(m / "Table/t.xlsx", b"table")
    write(m / f"{name}_Questions.xlsx", b"bank")
    write(m / f"subcategories_{name}.xlsx", b"undated")
    write(m / f"subcategories_{name}_2026-09-17.xlsx", b"older")
    write(m / f"subcategories_{name}_2026-09-18.xlsx", b"latest")
    write(m / "OCR_MANIFEST.json", "{}")
    write(m / "lecture_upload_summary.md", "# summary")
    write(m / "Markdown_Questions/00_CATALOG_OF_ALL_FILES.md",
          "| # | src | md |\n|---|---|---|\n| 1 | `a.pdf` | `01_Real.md` |\n| 2 | `b.pdf` | `02_B_EXCLUDED.md` |\n")
    write(m / "Markdown_Questions/01_Real.md", MD_REAL)
    write(m / "Markdown_Questions/02_B_EXCLUDED.md", PLACEHOLDER)
    write(m / "Images/01_Q3.png", b"png")
    return m


def by_rel(items):
    return {it.rel: it for it in items}


class TidyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_module(Path(self.tmp.name))
        Module(self.root)                                              # creates .mbset/

    def tearDown(self):
        self.tmp.cleanup()

    def test_plan_rules_without_lecture_flag(self):
        items = by_rel(tidy.plan(self.root))
        self.assertEqual(items["Book"].action, tidy.TRASH)
        self.assertEqual(items["Questions/a.pdf"].action, tidy.TRASH)
        self.assertEqual(items["Questions/new source.pdf"].action, tidy.TO_RAW)
        self.assertEqual(items["Questions/new source.pdf"].dest, "Raw_PDF_Questions/Questions/new source.pdf")
        self.assertEqual(items["Questions/notes.xlsx"].action, tidy.ARCHIVE)
        self.assertEqual(items["Lectures"].action, tidy.KEEP)
        self.assertEqual(items["Lecture_PowerPoint_PDF_Staging"].action, tidy.TRASH)
        self.assertIn("byte-identical to Lectures/", items["Lecture_PowerPoint_PDF_Staging"].reason)
        self.assertEqual(items["Lectures_PreOfficialNames_2026-09-18"].action, tidy.TRASH)
        self.assertIn("pre-official/staging", items["Lectures_PreOfficialNames_2026-09-18"].reason)
        self.assertEqual(items["Lectures_OCR_Upload"].action, tidy.DECIDE)
        self.assertEqual(items["Lectures_Other"].action, tidy.DECIDE)
        self.assertEqual(items["OCR_PDF"].action, tidy.TRASH)
        self.assertEqual(items["OCR_Text"].action, tidy.TRASH)
        self.assertEqual(items["Telegram_Staging"].action, tidy.ARCHIVE)   # its only pdf is in Raw
        self.assertEqual(items["Telegram_Staging"].dest, ".mbset/archive/Telegram_Staging")
        self.assertEqual(items["Table"].action, tidy.ARCHIVE)
        self.assertEqual(items["Endo_Questions.xlsx"].action, tidy.KEEP)
        self.assertEqual(items["subcategories_Endo_2026-09-18.xlsx"].action, tidy.KEEP)
        self.assertEqual(items["subcategories_Endo_2026-09-17.xlsx"].action, tidy.TRASH)
        self.assertEqual(items["subcategories_Endo.xlsx"].action, tidy.TRASH)
        self.assertEqual(items["OCR_MANIFEST.json"].action, tidy.ARCHIVE)
        self.assertEqual(items["lecture_upload_summary.md"].action, tidy.ARCHIVE)
        self.assertEqual(items["Markdown_Questions/02_B_EXCLUDED.md"].action, tidy.PLACEHOLDER)
        self.assertNotIn("Markdown_Questions/01_Real.md", items)
        for rel in items:
            self.assertFalse(rel.startswith(("Raw_PDF_Questions/", "Images/", ".mbset/")), rel)

    def test_lectures_from(self):
        items = by_rel(tidy.plan(self.root, "Lectures_OCR_Upload"))
        self.assertEqual(items["Lectures"].action, tidy.TRASH)
        self.assertEqual(items["Lectures_OCR_Upload"].action, tidy.RENAME)
        self.assertEqual(items["Lectures_OCR_Upload"].dest, "Lectures")
        for name in ("Lectures_PreOfficialNames_2026-09-18", "Lecture_PowerPoint_PDF_Staging", "Lectures_Other"):
            self.assertEqual(items[name].action, tidy.TRASH, name)
        with self.assertRaises(SystemExit):
            tidy.plan(self.root, "Nope")

    def test_telegram_unique_source_needs_decision(self):
        write(self.root / "Telegram_Staging/dl/unique.pdf", b"%PDF new question file")
        items = by_rel(tidy.plan(self.root))
        self.assertEqual(items["Telegram_Staging"].action, tidy.DECIDE)
        self.assertEqual(items["Telegram_Staging/dl/unique.pdf"].action, tidy.DECIDE)
        self.assertEqual(tidy.totals(list(items.values()))[tidy.DECIDE][0], 3)  # folder + Lectures_OCR_Upload + Lectures_Other

    def test_dry_run_changes_nothing(self):
        before = snapshot(self.root)
        args = argparse.Namespace(module=str(self.root), apply=False, lectures_from="Lectures_OCR_Upload",
                                  placeholders=True, restore=None)
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(tidy.cmd_tidy(args), 0)
        self.assertEqual(snapshot(self.root), before)
        self.assertIn("bytes freed", out.getvalue())
        self.assertIn("resulting layout", out.getvalue())
        self.assertTrue(list((self.root / ".mbset/reports").glob("tidy_*.md")))
        self.assertFalse((self.root / "_trash").exists())

    def test_apply_then_restore_round_trip(self):
        before = snapshot(self.root)
        items = tidy.plan(self.root, "Lectures_OCR_Upload", placeholders=True)
        with redirect_stdout(io.StringIO()):
            manifest = tidy.apply(self.root, items, "2026-01-02")
        top = sorted(p.name for p in self.root.iterdir())
        self.assertEqual(top, sorted([".mbset", "_trash", "Images", "Lectures", "Markdown_Questions",
                                      "Raw_PDF_Questions", "Endo_Questions.xlsx",
                                      "subcategories_Endo_2026-09-18.xlsx"]))
        self.assertEqual(sorted(p.name for p in (self.root / "Lectures").iterdir()), ["L1.pdf", "L2.pdf"])
        self.assertTrue((self.root / "Raw_PDF_Questions/Questions/new source.pdf").is_file())
        self.assertTrue((self.root / ".mbset/archive/Telegram_Staging/dl/slides.pptx").is_file())
        self.assertTrue((self.root / "_trash/2026-01-02/Lectures/L1.pdf").is_file())
        self.assertTrue((self.root / "_trash/2026-01-02/Markdown_Questions/02_B_EXCLUDED.md").is_file())
        self.assertTrue((self.root / "Markdown_Questions/01_Real.md").is_file())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        files = [e for e in data["entries"] if e["kind"] == "file"]
        self.assertTrue(all(len(e["sha256"]) == 64 and "size" in e for e in files))
        self.assertTrue(all("files" in e for e in data["entries"] if e["kind"] == "dir"))
        # nothing is ever deleted: every byte is still somewhere under the module
        after = {h for p, h in snapshot(self.root).items()}
        after |= {hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.root / "_trash").rglob("*") if p.is_file()}
        after |= {hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.root / ".mbset/archive").rglob("*")
                  if p.is_file()}
        self.assertLessEqual(set(before.values()), after)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(tidy.restore(self.root, "2026-01-02"), 0)
        self.assertEqual(snapshot(self.root), before)
        self.assertFalse((self.root / "_trash/2026-01-02").exists())

    def test_placeholder_owned_by_pending_source_is_kept(self):
        (self.root / ".mbset/state.json").write_text(json.dumps(
            {"sources": [{"nn": "02", "rel": "Raw_PDF_Questions/b.pdf", "md": "02_B_EXCLUDED.md", "status": "pending"}]}))
        items = by_rel(tidy.plan(self.root, placeholders=True))
        self.assertEqual(items["Markdown_Questions/02_B_EXCLUDED.md"].action, tidy.PLACEHOLDER)
        self.assertIn("set --exclude", items["Markdown_Questions/02_B_EXCLUDED.md"].reason)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = make_module(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_markdown_only(self):
        data = report.collect(Module(self.root))
        self.assertEqual(data["mode"], "markdown only")
        (row,) = data["rows"]
        self.assertEqual((row["questions"], row["mcq"], row["qroc"], row["answered"]), (3, 2, 1, 3))
        self.assertEqual(row["derived"], [2, 3])
        self.assertEqual(row["figures"], 1)
        self.assertEqual(row["source"], "a.pdf")
        self.assertEqual([e["md"] for e in data["excluded"]], ["02_B_EXCLUDED.md"])
        self.assertIn("unreadable scan", data["excluded"][0]["reason"])
        text = report.render(data)
        self.assertIn("derived answers: 2", text)
        self.assertIn("Q2, Q3", text)

    def test_state_and_bias(self):
        blocks = "".join(f"### Q{i}: Stem number {i} about hormones?\n\n- **A)** x\n- **B)** y\n\n"
                         f"**Correct Answer:** {'A' if i <= 12 else 'B'}\n**Answer Source:** key\n\n---\n\n"
                         for i in range(1, 17))
        write(self.root / "Markdown_Questions/03_Biased.md", "# b\n\n" + blocks)
        write(self.root / "Raw_PDF_Questions/c.pdf", b"%PDF c")
        (self.root / ".mbset").mkdir(exist_ok=True)
        (self.root / ".mbset/state.json").write_text(json.dumps({"sources": [
            {"nn": "01", "rel": "Raw_PDF_Questions/a.pdf", "md": "01_Real.md", "status": "reviewed",
             "triage": {"class": "digital_single"}, "tags": {"tag": "Exams, End 2024"},
             "stages": {"review": {"spot_check": "5/5 ok"}}},
            {"nn": "02", "rel": "Raw_PDF_Questions/b.pdf", "md": "02_B_EXCLUDED.md", "status": "excluded",
             "exclusion": "unreadable"},
            {"nn": "03", "rel": "Raw_PDF_Questions/c.pdf", "md": "03_Biased.md", "status": "parsed"}]}))
        data = report.collect(Module(self.root))
        rows = {r["nn"]: r for r in data["rows"]}
        self.assertEqual(rows["01"]["spot"], "5/5 ok")
        self.assertEqual(rows["01"]["tag"], "Exams, End 2024")
        self.assertEqual(rows["03"]["bias"][0], "A")
        self.assertEqual(rows["03"]["bias"][3], "FAIL")                 # 12/16 = 75 %
        self.assertEqual(data["excluded"][0]["reason"], "unreadable")
        buf = io.StringIO()
        out = Path(self.tmp.name) / "r.md"
        with redirect_stdout(buf):
            self.assertEqual(report.cmd_report(argparse.Namespace(module=str(self.root), out=str(out))), 0)
        self.assertIn("A = 75% of 16 — FAIL", out.read_text(encoding="utf-8"))


class CrossdupTests(unittest.TestCase):
    def test_shared_sources_and_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            uni = Path(tmp) / "Uni"
            write(uni / "M1/Raw_PDF_Questions/x.pdf", b"%PDF shared")
            write(uni / "M1/Raw_PDF_Questions/only1.pdf", b"%PDF one")
            write(uni / "M2/Raw_PDF_Questions/sub/x copy.pdf", b"%PDF shared")
            write(uni / "M2/Raw_PDF_Questions/dup-in-same.pdf", b"%PDF one2")
            write(uni / "M2/Raw_PDF_Questions/dup-in-same2.pdf", b"%PDF one2")
            mods = crossdup.find_modules([str(uni)])
            self.assertEqual([m.name for m in mods], ["M1", "M2"])
            groups = crossdup.shared(crossdup.scan(mods))
            self.assertEqual(len(groups), 1)                           # same-module copies are not reported
            self.assertEqual(sorted(i["rel"] for i in groups[0][1]),
                             ["Raw_PDF_Questions/sub/x copy.pdf", "Raw_PDF_Questions/x.pdf"])
            self.assertTrue((uni / "M1/.mbset/cache/hashes.json").is_file())
            with redirect_stdout(io.StringIO()) as out:
                self.assertEqual(crossdup.cmd_crossdup(argparse.Namespace(roots=[str(uni)], min_size=0, json=None)), 0)
            self.assertIn("1 source(s) appear in more than one module", out.getvalue())


class RegisterTests(unittest.TestCase):
    def test_register_all(self):
        ap = argparse.ArgumentParser()
        sub = ap.add_subparsers(dest="cmd", required=True)
        for m in (tidy, report, doctor, crossdup):
            m.register(sub)
        a = ap.parse_args(["tidy", "X", "--lectures-from", "L", "--apply"])
        self.assertIs(a.fn, tidy.cmd_tidy)
        self.assertTrue(a.apply)
        self.assertIs(ap.parse_args(["report", "X"]).fn, report.cmd_report)
        self.assertIsNone(ap.parse_args(["doctor"]).module)
        self.assertEqual(ap.parse_args(["crossdup", "a", "b", "--min-size", "10"]).min_size, 10)

    def test_doctor_module_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "M"
            (root / "Raw_PDF_Questions").mkdir(parents=True)
            (root / ".mbset/locks").mkdir(parents=True)
            (root / ".mbset/state.json").write_text("{not json")
            say = doctor.Report()
            with redirect_stdout(io.StringIO()) as out:
                doctor.check_module(say, str(root))
            self.assertEqual(say.fails, 1)
            self.assertIn("state.json unreadable", out.getvalue())


if __name__ == "__main__":
    unittest.main()
