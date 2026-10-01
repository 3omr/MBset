"""Regression tests for the mbset.py parser, answers, overrides and cleaner.

Synthetic lines only (source PDFs are not in git), one test per format rule that once broke.
Run:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".agents/skills/mbset-module-curator/scripts"
sys.path.insert(0, str(SCRIPTS))

from mbset import answers, overrides  # noqa: E402
from mbset.common import Module  # noqa: E402
from mbset.document import Line  # noqa: E402
from mbset.noise import clean_text  # noqa: E402
from mbset.parser import Parser, finish  # noqa: E402
from mbset.profiles import DEFAULT  # noqa: E402
from mbset.writer import render  # noqa: E402

import clean_markdown_noise  # noqa: E402


def lines(text: str, page: int = 0) -> list[Line]:
    out = []
    for i, t in enumerate(t for t in text.strip("\n").splitlines()):
        indent = len(t) - len(t.lstrip())
        out.append(Line(text=t.strip(), page=page, bbox=(72 + indent * 6, 72 + i * 14, 500, 84 + i * 14)))
    return out


def parse(text: str, profile=None, lenient=False):
    prof = copy.deepcopy(profile or DEFAULT)
    ls = lines(text)
    p = Parser(prof, lenient=lenient)
    recs = finish(p.parse(ls), prof)
    return recs, p, ls, prof


class ParserTests(unittest.TestCase):
    def test_basic_mcq(self):
        recs, p, _, _ = parse("""
1. Which hormone is secreted by the posterior pituitary?
  a. ACTH
  b. ADH
  c. TSH
2. A 12-year-old boy presents with polyuria. The most likely cause is
  a) Diabetes insipidus
  b) Hypercalcaemia
""")
        self.assertEqual([r["number"] for r in recs], [1, 2])
        self.assertEqual([o["text"] for o in recs[0]["options"]], ["ACTH", "ADH", "TSH"])
        self.assertIn("12-year-old", recs[1]["stem"])          # "12-" inside a stem is not a number
        self.assertEqual(p.gaps, [])

    def test_inline_options_and_dose_not_a_number(self):
        recs, *_ = parse("""
1. The usual dose is 1.5 mg of
a. Levothyroxine b. Carbimazole c. Propranolol d. Iodine
""")
        self.assertEqual(len(recs), 1)
        self.assertEqual([o["letter"] for o in recs[0]["options"]], list("ABCD"))

    def test_section_restart_and_gap(self):
        recs, p, _, _ = parse("""
1. First question here
a. x1
b. y1
2. Second question here
a. x2
b. y2
1. Chapter two first question
a. x3
b. y3
3. Chapter two third question
a. x4
b. y4
""")
        self.assertEqual([r["section"] for r in recs], [1, 1, 2, 2])
        self.assertTrue(any("missing [2]" in g for g in p.gaps))

    def test_option_grid_sorted(self):
        recs, *_ = parse("""
1. Adrenal crisis is characterized by
a- profound asthma
c- vascular collapse
b- severe abdominal pain
d- low Na & high K
""")
        self.assertEqual([o["text"] for o in recs[0]["options"]],
                         ["profound asthma", "severe abdominal pain", "vascular collapse", "low Na & high K"])

    def test_rtl_numbers(self):
        recs, *_ = parse("""
All the following are causes of goitre except .4
.A. Iodine deficiency
.B. Graves disease
""")
        self.assertEqual(recs[0]["number"], 4)
        self.assertEqual(recs[0]["options"][0]["text"], "Iodine deficiency")

    def test_stem_prefix_cut(self):
        recs, *_ = parse("""
1. First question here
a. x1
b. y1
Explanation of the first one follows here. 2. All the following are true except
a. x2
b. y2
""", lenient=True)
        self.assertTrue(recs[-1]["stem"].startswith("All the following"))


class AnswerTests(unittest.TestCase):
    def test_grid_key_at_end(self):
        text = "\n".join(f"{i}. Question number {i} text\na. opt a{i}\nb. opt b{i}\nc. opt c{i}" for i in range(1, 7))
        text += "\n1-a 2-b 3-c\n4-a 5-b 6-c\n"
        recs, _, ls, prof = parse(text)
        with tempfile.TemporaryDirectory() as d:
            mod = Module(d)
            rep = answers.attach(mod, {"nn": "01", "pages": 1}, recs, ls, prof)
        self.assertEqual(len(recs), 6)                       # key lines are not glued to Q6
        self.assertEqual([r["correct"] for r in recs], list("ABCABC"))
        self.assertTrue(all(r["answer_source"] == "key" for r in recs))
        self.assertEqual(rep["answered"], 6)

    def test_marked_needs_exactly_one(self):
        recs, _, ls, prof = parse("1. Stem text here\na. one\nb. two\nc. three\n")
        for ln in ls:
            if ln.text.startswith("b."):
                ln.marks.append("highlight")
        recs = finish(Parser(prof).parse(ls), prof)
        with tempfile.TemporaryDirectory() as d:
            answers.attach(Module(d), {"nn": "01", "pages": 1}, recs, ls, prof)
        self.assertEqual((recs[0]["correct"], recs[0]["answer_source"]), ("B", "marked"))

    def test_no_answer_is_never_defaulted(self):
        recs, _, ls, prof = parse("1. Stem text here\na. one\nb. two\n")
        with tempfile.TemporaryDirectory() as d:
            answers.attach(Module(d), {"nn": "01", "pages": 1}, recs, ls, prof)
        self.assertIsNone(recs[0]["correct"])
        md = render({"rel": "x.pdf", "nn": "01"}, recs)
        self.assertIn("**Correct Answer:** ?", md)
        self.assertIn("**Answer Source:** none", md)


class OverrideTests(unittest.TestCase):
    def test_override_survives_reparse_by_option_text(self):
        recs, *_ = parse("1. Stem text here\na. one\nb. two\nc. three\n")
        src = {"nn": "01"}
        overrides.record(src, recs[0]["stem"], answer="three", source="marked")
        fresh, *_ = parse("1. Stem text here\na. one\nb. two\nc. three\n")
        rep = overrides.apply(src, fresh)
        self.assertEqual((fresh[0]["correct"], fresh[0]["answer_source"]), ("C", "marked"))
        self.assertEqual(rep["applied"], 1)

    def test_override_drop(self):
        recs, *_ = parse("1. Stem text here\na. one\nb. two\n2. Not a question banner\na. x\nb. y\n")
        src = {"nn": "01"}
        overrides.record(src, recs[1]["stem"], drop="banner")
        rep = overrides.apply(src, recs)
        self.assertEqual(len(recs), 1)
        self.assertEqual(len(rep["dropped"]), 1)


class CleanerTests(unittest.TestCase):
    def test_cleaner_never_invents_answer_and_moves_correct(self):
        md = """# t

### Q1: 1. Which is correct ?

- **A)**
- **B)** alpha
- **C)** beta

**Correct Answer:** C
**Answer Source:** key

---

### Q2: Second stem

- **A)** x
- **B)** y

**Correct Answer:** ?
**Answer Source:** none

---
"""
        out, problems = clean_markdown_noise.clean_markdown(md)
        self.assertIn("- **B)** beta", out)
        self.assertIn("**Correct Answer:** B", out)          # C moved with its option
        self.assertIn("**Correct Answer:** ?", out)          # unknown stays unknown
        self.assertNotIn("Correct Answer:** A", out)

    def test_leading_number_keeps_ages_and_doses(self):
        self.assertEqual(clean_text("44-y female pt", stem=True), "44-y female pt")
        self.assertEqual(clean_text("1.5 mg is given", stem=True), "1.5 mg is given")
        self.assertEqual(clean_text("12. Which hormone", stem=True), "Which hormone")

    def test_notation_and_arabic(self):
        self.assertEqual(clean_text("Serum Ca** is high"), "Serum Ca²⁺ is high")
        self.assertNotRegex(clean_text("Thyroid الغدة gland"), r"[؀-ۿ]")


class PenMarkedOptionTests(unittest.TestCase):
    """OCR of pen-marked exams: the tick eats the option's '.', or the whole letter."""

    def ocr_parse(self, text):
        recs, p, ls, prof = parse(text, lenient=True)
        return recs

    def setUp(self):
        global lines
        self._lines = lines

        def ocr_lines(text, page=0):
            out = self._lines(text, page)
            for ln in out:
                ln.conf = 0.95
            return out
        globals()["lines"] = ocr_lines

    def tearDown(self):
        globals()["lines"] = self._lines

    def letters(self, rec):
        return [o["letter"] for o in rec["options"]], [o["text"] for o in rec["options"]]

    def test_bare_glued_and_y_tick_markers(self):
        recs = self.ocr_parse("""
5. A patient with a localized wound infection should be treated with:
A. Antibiotics and warm soaks
By Antibiotics alone
C7 days of antibiotics
DIncision and drainage alone
""")
        L, T = self.letters(recs[0])
        self.assertEqual(L, list("ABCD"))
        self.assertEqual(T[1:], ["Antibiotics alone", "7 days of antibiotics", "Incision and drainage alone"])
        self.assertTrue(any("possible_mark" in f for f in recs[0]["flags"]))

    def test_orphan_row_between_options_is_kept(self):
        recs = self.ocr_parse("""
10. The major cause of impaired wound healing is:
A. Anemia
B. Diabetes mellitus
Local tissue infection
D. Malnutrition
""")
        L, T = self.letters(recs[0])
        self.assertEqual(L, list("ABCD"))
        self.assertEqual(T[2], "Local tissue infection")

    def test_first_and_last_marker_lost(self):
        recs = self.ocr_parse("""
18. The most common presenting symptom of acute arterial occlusion is:
Pain
B. Pallor
C. Paresthesia
D. Pulselessness
""")
        self.assertEqual(self.letters(recs[0]), (list("ABCD"), ["Pain", "Pallor", "Paresthesia", "Pulselessness"]))
        self.assertNotIn("Pain", recs[0]["stem"])


class FormsAndCompoundTests(unittest.TestCase):
    def test_c_reactive_is_not_an_option(self):
        from mbset.parser import INLINE_OPT
        self.assertEqual([m.group(1) for m in INLINE_OPT.finditer("Raised C-reactive protein is seen")], [])
        self.assertEqual([m.group(1) for m in INLINE_OPT.finditer("a-Insulin b-Glucagon")], ["a", "b"])

    def test_forms_unlabeled_choices_get_letters(self):
        from mbset.document import letter_unlabeled_options
        rows = [("In a bleeding patient, the most important parameter to assess fluid", 13.6, 0),
                (":replacement is", 13.6, 17), ("(\u0646\u0642\u0637\u0629 1) *", 13.6, 35),
                (".Pulse rate", 12.8, 74), (".Blood pressure", 12.8, 114), ("Urine output", 12.8, 154),
                (":Neurogenic shock is characterized by", 13.6, 220), ("Cool, moist skin", 12.8, 260),
                ("Increased cardiac output", 12.8, 300)] * 3
        ls = [Line(text=t, page=0, bbox=(72, y, 500, y + 14), size=z) for t, z, y in rows]
        out = [ln.text for ln in letter_unlabeled_options(ls, {"options_unlabeled": True})]
        self.assertEqual(out[:8], ["In a bleeding patient, the most important parameter to assess fluid",
                                   "replacement is:", "a. Pulse rate", "b. Blood pressure", "c. Urine output",
                                   "Neurogenic shock is characterized by:", "a. Cool, moist skin",
                                   "b. Increased cardiac output"])       # the points badge row is gone


class TextFixTests(unittest.TestCase):
    def test_visual_text_fix_survives_reparse_and_keeps_answer(self):
        recs, *_ = parse("1. Stem text here with noise \u00a2\na. one\nb. two\n")
        src = {"nn": "01"}
        overrides.record(src, recs[0]["stem"], stem_fix="Stem text here", options_fix={"C": "three"},
                         text_before={"stem": recs[0]["stem"]})
        overrides.record(src, "Stem text here", answer="three", source="marked")   # keyed via the fix
        fresh, *_ = parse("1. Stem text here with noise \u00a2\na. one\nb. two\n")
        overrides.apply(src, fresh)
        self.assertEqual(fresh[0]["stem"], "Stem text here")
        self.assertEqual([o["text"] for o in fresh[0]["options"]], ["one", "two", "three"])
        self.assertEqual((fresh[0]["correct"], fresh[0]["answer_source"]), ("C", "marked"))
        self.assertEqual(len(src["overrides"]), 1)


class ModelAnswerAndFlagTests(unittest.TestCase):
    def test_written_question_gets_model_answer_field(self):
        recs = [{"type": "QROC", "stem": "Define: ketolysis", "options": [], "exp": "Breakdown of ketone bodies",
                 "exp_source": "key", "pages": [0]},
                {"type": "QCS", "stem": "Pick one", "options": [{"letter": "A", "text": "x"}, {"letter": "B", "text": "y"}],
                 "correct": "B", "answer_source": "key", "exp": "because", "pages": [0]}]
        text = render({"rel": "Raw_PDF_Questions/s.pdf", "nn": "01"}, recs)
        self.assertIn("**Model Answer:** Breakdown of ketone bodies", text)
        self.assertIn("**EXP:** because", text)
        import build_module_template as b
        with tempfile.TemporaryDirectory() as tmp:
            for name, body in (("new.md", text), ("old.md", text.replace("**Model Answer:**", "**EXP:**"))):
                (Path(tmp) / name).write_text(body, encoding="utf-8")
                qs = b.parse_markdown(str(Path(tmp) / name))
                self.assertEqual(qs[0]["Type"], "QROC")
                self.assertEqual(qs[0]["EXP"], "Breakdown of ketone bodies")   # → ModelAnswer column

    def test_info_flags_do_not_need_review(self):
        from mbset.common import review_flags
        self.assertEqual(review_flags(["added_from_page_image", "unnumbered", "number_corrected_from_3",
                                       "text_corrected_visual", "letters_not_sequential"]),
                         ["letters_not_sequential"])


class TranscribeTests(unittest.TestCase):
    def test_chunks_split_big_files(self):
        from mbset.transcribe import chunks_for
        self.assertEqual(chunks_for(14, 6), [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14]])
        self.assertEqual(len(chunks_for(60, 6)), 10)
        self.assertEqual(chunks_for(3, 6), [[1, 2, 3]])

    def test_ingest_checks_keys_gaps_and_missing_chunks(self):
        import json
        from mbset import transcribe
        with tempfile.TemporaryDirectory() as tmp:
            module = Module(tmp)
            src = {"nn": "01", "rel": "Raw_PDF_Questions/s.pdf", "md": "01_S.md", "triage": {}}
            d = transcribe.tdir(module, src)
            d.mkdir(parents=True)
            chunks = [{"k": 1, "pages": [1, 2], "out": str(d / "chunk_01.json")},
                      {"k": 2, "pages": [3, 4], "out": str(d / "chunk_02.json")}]
            (d / "manifest.json").write_text(json.dumps({"pages": 4, "chunks": chunks}), encoding="utf-8")
            (d / "chunk_01.json").write_text(json.dumps({"questions": [
                {"page": 1, "number": 1, "stem": "First stem here", "options": {"A": "a", "B": "b"},
                 "answer": "B", "answer_source": "marked"},
                {"page": 2, "number": 2, "stem": "Second stem", "options": {"A": "a", "B": "b"},
                 "answer": "E", "answer_source": "key"},
                {"page": 2, "number": 5, "stem": "Define: x", "options": {},
                 "model_answer": "y", "model_answer_source": "key"}],
                "skipped_numbers": [4]}), encoding="utf-8")
            t = transcribe.load(module, src, copy.deepcopy(DEFAULT))
            r = t["records"]
            self.assertEqual([x["correct"] for x in r], ["B", None, None])
            self.assertIn("key_letter_not_among_options", r[1]["flags"])
            self.assertEqual((r[2]["type"], r[2]["exp"], r[2]["exp_source"]), ("QROC", "y", "key"))
            self.assertTrue(any("missing 3" in g for g in t["gaps"]))           # 4 is declared skipped
            self.assertFalse(any("missing 4" in g for g in t["gaps"]))
            self.assertEqual(len(t["counters"]["missing_chunks"]), 1)


class ExtractionV3Tests(unittest.TestCase):
    def _module(self, tmp, chunks, manifest_extra=None):
        import json
        from mbset import transcribe
        module = Module(tmp)
        src = {"nn": "01", "rel": "Raw_PDF_Questions/s.pdf", "md": "01_S.md", "triage": {}}
        d = transcribe.tdir(module, src)
        d.mkdir(parents=True)
        man = {"pages": 10, "chunks": []}
        for k, (pages, data) in enumerate(chunks, 1):
            out = d / f"chunk_{k:02d}.json"
            man["chunks"].append({"k": k, "pages": pages, "out": str(out)})
            if data is not None:
                out.write_text(json.dumps(data), encoding="utf-8")
        man.update(manifest_extra or {})
        (d / "manifest.json").write_text(json.dumps(man), encoding="utf-8")
        return module, src, d

    def test_chunks_follow_runs_of_pages(self):
        from mbset.transcribe import chunks_for
        self.assertEqual(chunks_for([3, 4, 5, 9, 10], 6), [[3, 4, 5], [9, 10]])
        self.assertEqual(chunks_for(list(range(1, 15)), 6), [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14]])

    def test_case_count_mismatch_and_key_job(self):
        import json
        from mbset import transcribe
        q = lambda n, case="": {"page": 1, "number": n, "case": case, "stem": f"Stem number {n} here",
                                "options": {"A": "x", "B": "y"}, "answer": None, "answer_source": None}
        with tempfile.TemporaryDirectory() as tmp:
            module, src, d = self._module(tmp, [([1, 2], {"printed_count": 3, "questions": [q(1, "A man of 40"), q(2, "A man of 40")]})],
                                          {"key": {"out": str(Path(tmp) / ".mbset/transcripts/01/key.json")}})
            (d / "key.json").write_text(json.dumps({"sections": [{"1": "B", "2": "Z"}]}), encoding="utf-8")
            t = transcribe.load(module, src, copy.deepcopy(DEFAULT))
            r = t["records"]
            self.assertEqual(r[0]["case"], "A man of 40")
            self.assertEqual((r[0]["correct"], r[0]["answer_source"]), ("B", "key"))
            self.assertIn("key_letter_not_among_options", r[1]["flags"])
            self.assertEqual(len(t["counters"]["chunk_count_mismatch"]), 1)

    def test_mix_keeps_parsed_pages_in_page_order(self):
        from mbset import transcribe
        base = [{"i": 1, "number": 1, "page": 0, "type": "QCS", "stem": "parsed one", "options": [], "flags": []},
                {"i": 2, "number": 3, "page": 2, "type": "QCS", "stem": "parsed three", "options": [], "flags": []}]
        tq = {"page": 2, "number": 2, "stem": "transcribed two", "options": {"A": "x", "B": "y"},
              "answer": "A", "answer_source": "marked"}
        with tempfile.TemporaryDirectory() as tmp:
            module, src, _ = self._module(tmp, [([2], {"printed_count": 1, "questions": [tq]})], {"pages_only": [2]})
            t = transcribe.load(module, src, copy.deepcopy(DEFAULT), base=base)
            self.assertEqual([x["number"] for x in t["records"]], [1, 2, 3])
            self.assertEqual(t["gaps"], [])

    def test_case_reaches_the_cas_column_and_dedupe_keeps_both(self):
        import build_module_template as b
        recs = [{"type": "QCS", "stem": "What is the diagnosis?", "case": case, "pages": [0],
                 "options": [{"letter": "A", "text": "x"}, {"letter": "B", "text": "y"}], "correct": "A",
                 "answer_source": "key"} for case in ("A child with fever", "An old man with chest pain")]
        text = render({"rel": "Raw_PDF_Questions/s.pdf", "nn": "01"}, recs)
        self.assertIn("**Case:** A child with fever", text)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.md").write_text(text, encoding="utf-8")
            qs = b.parse_markdown(str(Path(tmp) / "a.md"))
            self.assertEqual([q["Cas"] for q in qs], ["A child with fever", "An old man with chest pain"])
            self.assertEqual(qs[0]["Text"], "What is the diagnosis?")

    def test_folder_convention_tags(self):
        from mbset import taxonomy
        tax = taxonomy.load("folders")
        s = taxonomy.suggest(tax, "Raw_PDF_Questions/Department/[Physiology] {2024}/_x.pdf")
        self.assertEqual((s["tag"], s["tagSuggere"], s["year"]), ("Department 2024", "Physiology", 2024))
        self.assertEqual(taxonomy.suggest(tax, "Raw_PDF_Questions/Final 2022.pdf")["tag"], "Exams, Final 2022")


class DispatchTests(unittest.TestCase):
    def test_runs_pending_briefs_and_retries_missing_ones(self):
        import argparse, io, contextlib, json
        from mbset import dispatch, transcribe
        with tempfile.TemporaryDirectory() as tmp:
            module = Module(tmp)
            module.save({"sources": [{"nn": "01", "rel": "Raw_PDF_Questions/s.pdf", "md": "01_S.md"}]})
            d = transcribe.tdir(module, {"nn": "01"})
            d.mkdir(parents=True)
            chunks = []
            for k in (1, 2):
                b = d / f"chunk_0{k}.brief.txt"
                b.write_text("brief", encoding="utf-8")
                chunks.append({"k": k, "pages": [k], "brief": str(b), "out": str(d / f"chunk_0{k}.json")})
            (d / "chunk_01.json").write_text("{}", encoding="utf-8")            # chunk 1 already done
            (d / "manifest.json").write_text(json.dumps({"pages": 2, "chunks": chunks}), encoding="utf-8")
            # a fake worker: fails the first time (no JSON), succeeds on the retry
            flag = Path(tmp) / "tried"
            cmd = (f"if [ -f {flag} ]; then echo '{{}}' > $(dirname {{brief}})/chunk_02.json; "
                   f"else touch {flag}; fi")
            args = argparse.Namespace(module=tmp, only=None, parallel=2, retries=1, effort="high", dispatch=cmd)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = dispatch.cmd_dispatch(args)
            self.assertEqual(rc, 0, out.getvalue())
            self.assertIn("round 2: 1 brief", out.getvalue())
            self.assertTrue((d / "chunk_02.json").exists())


class WorklistSplitTests(unittest.TestCase):
    def test_big_file_is_split_into_question_ranges(self):
        from mbset import worklist
        w = {"nn": "01", "file": "f.pdf", "md": "m.md", "gaps": ["g"],
             "text": [(n, "x") for n in range(1, 21)], "answer": list(range(1, 41)), "model": []}
        parts = worklist.split(w, 30)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(worklist.cost(p) <= 30 for p in parts))
        self.assertEqual(sum(len(p["answer"]) for p in parts), 40)
        self.assertEqual([p["gaps"] for p in parts][1:], [[]] * (len(parts) - 1))
        self.assertEqual(worklist.split(dict(w, text=[], answer=[1]), 30)[0]["part"], None)


if __name__ == "__main__":
    unittest.main()
