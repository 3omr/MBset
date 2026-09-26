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


if __name__ == "__main__":
    unittest.main()
