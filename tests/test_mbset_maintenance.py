"""Tests for renumber (images move with their source), year-less tag suggestions + check, Codex
packet briefs, and the renal DocReader answer index (never defaults to A).

Run:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / ".agents/skills/mbset-module-curator/scripts"
sys.path.insert(0, str(SCRIPTS))

from mbset import catalog, check, inventory  # noqa: E402
from mbset.cli import main  # noqa: E402
from mbset.common import text_hash  # noqa: E402


def run_cli(*argv: str) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = main(list(argv))
    assert rc == 0, out.getvalue()
    return out.getvalue()


def md(stem: str, image: str | None = None) -> str:
    img = f"**Image:** {image}\n" if image else ""
    return (f"### Q1: {stem}\n\n- **A)** one\n- **B)** two\n\n**Correct Answer:** A\n"
            f"**Answer Source:** key\n{img}\n---\n")


class RenumberTests(unittest.TestCase):
    def test_images_and_paths_follow_the_renumbered_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Mod"
            (root / "Markdown_Questions").mkdir(parents=True)
            (root / "Images").mkdir()
            meta = root / ".mbset"
            (meta / "parsed").mkdir(parents=True)
            first = {"nn": "05", "rel": "Raw_PDF_Questions/a.pdf", "md": "05_A.md", "sha256": "aaa"}
            second = {"nn": "05", "rel": "Raw_PDF_Questions/b.pdf", "md": "05_B.md", "sha256": "bbb",
                      "overrides": {"stemkey": {"image": "Images/05_Q1.png"}},
                      "stages": {"parse": {"md_hash": "old"}}}
            (meta / "state.json").write_text(json.dumps({"sources": [first, second], "duplicate_nn": ["05"]}),
                                             encoding="utf-8")
            (root / "Markdown_Questions/05_A.md").write_text(md("First source", "Images/05_Q2.png"), encoding="utf-8")
            (root / "Markdown_Questions/05_B.md").write_text(md("Second source", "Images/05_Q1.png"), encoding="utf-8")
            (root / "Images/05_Q1.png").write_bytes(b"second")
            (root / "Images/05_Q2.png").write_bytes(b"first")
            (meta / "parsed/05.json").write_text(json.dumps(
                {"sha256": "bbb", "questions": [{"stem": "Second source", "image": "Images/05_Q1.png"}]}),
                encoding="utf-8")

            run_cli("renumber", str(root))

            self.assertEqual((root / "Images/06_Q1.png").read_bytes(), b"second")
            self.assertFalse((root / "Images/05_Q1.png").exists())
            self.assertEqual((root / "Images/05_Q2.png").read_bytes(), b"first")      # the first owner's crop stays
            new_md = (root / "Markdown_Questions/06_B.md").read_text(encoding="utf-8")
            self.assertIn("**Image:** Images/06_Q1.png", new_md)
            self.assertFalse((root / "Markdown_Questions/05_B.md").exists())
            self.assertIn("Images/05_Q2.png", (root / "Markdown_Questions/05_A.md").read_text(encoding="utf-8"))
            parsed = json.loads((meta / "parsed/06.json").read_text(encoding="utf-8"))
            self.assertEqual(parsed["questions"][0]["image"], "Images/06_Q1.png")
            self.assertFalse((meta / "parsed/05.json").exists())
            state = json.loads((meta / "state.json").read_text(encoding="utf-8"))
            moved = next(s for s in state["sources"] if s["rel"].endswith("b.pdf"))
            self.assertEqual(moved["nn"], "06")
            self.assertEqual(moved["md"], "06_B.md")
            self.assertEqual(moved["overrides"]["stemkey"]["image"], "Images/06_Q1.png")
            self.assertEqual(moved["stages"]["parse"]["md_hash"], text_hash(new_md))  # still re-parseable

    def test_image_linked_by_both_sources_is_not_moved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Mod"
            (root / "Markdown_Questions").mkdir(parents=True)
            (root / "Images").mkdir()
            (root / ".mbset").mkdir()
            srcs = [{"nn": "03", "rel": "Raw_PDF_Questions/a.pdf", "md": "03_A.md", "sha256": "a"},
                    {"nn": "03", "rel": "Raw_PDF_Questions/b.pdf", "md": "03_B.md", "sha256": "b"}]
            (root / ".mbset/state.json").write_text(json.dumps({"sources": srcs}), encoding="utf-8")
            for name in ("03_A.md", "03_B.md"):
                (root / "Markdown_Questions" / name).write_text(md(name, "Images/03_Q1.png"), encoding="utf-8")
            (root / "Images/03_Q1.png").write_bytes(b"x")
            out = run_cli("renumber", str(root))
            self.assertIn("left in place", out)
            self.assertTrue((root / "Images/03_Q1.png").exists())
            self.assertIn("Images/03_Q1.png", (root / "Markdown_Questions/04_B.md").read_text(encoding="utf-8"))


class TagSuggestionTests(unittest.TestCase):
    damietta = SimpleNamespace(university="Damietta")
    assiut = SimpleNamespace(university="Assiut")

    def test_unknown_year_gives_no_placeholder(self):
        t = inventory.suggest_tags(self.damietta, "Raw_PDF_Questions/Dr Morshdy questions.pdf")
        self.assertEqual(t["tag"], "Professor, Dr Morshdy")
        self.assertIsNone(t["year"])
        self.assertEqual(t["confidence"], "low")
        self.assertTrue(t["needs_year"])
        for rel in ("Final exam.pdf", "Formative.pdf", "Physiology book.pdf", "random notes.pdf"):
            t = inventory.suggest_tags(self.damietta, f"Raw_PDF_Questions/{rel}")
            self.assertNotIn("<", t["tag"], rel)
            self.assertNotIn("None", t["tag"], rel)
            self.assertTrue(t["needs_year"], rel)

    def test_known_year_is_in_the_tag(self):
        t = inventory.suggest_tags(self.damietta, "Raw_PDF_Questions/Dr Morshdy 2025.pdf")
        self.assertEqual(t["tag"], "Professor, Dr Morshdy 2025")
        self.assertEqual(t["year"], 2025)
        self.assertFalse(t["needs_year"])
        t = inventory.suggest_tags(self.damietta, "Raw_PDF_Questions/Final 2023.pdf")
        self.assertEqual((t["tag"], t["tagSuggere"]), ("Exams, Final 2023", None))

    def test_assiut_quizzes_and_formatives_need_no_year(self):
        t = inventory.suggest_tags(self.assiut, "Raw_PDF_Questions/Quiz week 3.pdf")
        self.assertEqual(t["tag"], "Department, Quizzes, Week 3")
        self.assertIsNone(t["year"])
        self.assertFalse(t["needs_year"])
        t = inventory.suggest_tags(self.assiut, "Raw_PDF_Questions/Formative week 2.pdf")
        self.assertEqual(t["tag"], "Department, Formative, Week 2")
        self.assertFalse(t["needs_year"])
        t = inventory.suggest_tags(self.assiut, "Raw_PDF_Questions/Midterm exam.pdf")
        self.assertEqual(t["tag"], "Exams, Midterm")
        self.assertTrue(t["needs_year"])


class TagCheckTests(unittest.TestCase):
    def src(self, tag, confirmed=False, **extra):
        return {"nn": "07", "tags": {"tag": tag, "confirmed": confirmed, **extra}}

    def test_placeholder_is_hard_even_when_confirmed(self):
        hard, _ = check.check_tags(self.src("Professor, Dr X <Year>", confirmed=True))
        self.assertTrue(any("placeholder" in h for h in hard))
        hard, _ = check.check_tags(self.src("Department, GDs, <Subject> GD 1 2024", confirmed=True))
        self.assertTrue(any("placeholder" in h for h in hard))

    def test_unconfirmed_without_year_warns(self):
        hard, review = check.check_tags(self.src("Professor, Dr X", needs_year=True))
        self.assertTrue(any("not confirmed" in h for h in hard))
        self.assertTrue(any("WARN tag has no year" in r for r in review))
        _, review = check.check_tags(self.src("Exams, Final"))          # older state: no needs_year key
        self.assertTrue(review)

    def test_no_warning_for_year_free_or_dated_tags(self):
        for tag in ("Department, Quizzes, Week 3", "Department, Formative, Week 1", "Exams, End 2025"):
            hard, review = check.check_tags(self.src(tag))
            self.assertEqual(review, [], tag)
            self.assertEqual(len(hard), 1, tag)                          # only "not confirmed"
        self.assertEqual(check.check_tags(self.src("Exams, End 2025", confirmed=True)), ([], []))


class PacketBriefTests(unittest.TestCase):
    def test_every_packet_gets_a_self_contained_brief(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Mod"
            (root / ".mbset").mkdir(parents=True)
            srcs = [{"nn": f"{i:02d}", "rel": f"Raw_PDF_Questions/s{i}.pdf", "md": f"{i:02d}_S{i}.md",
                     "pages": p, "status": "parsed", "triage": {"class": "scanned"}}
                    for i, p in ((1, 40), (2, 10), (3, 25), (4, 5))]
            srcs.append({"nn": "05", "rel": "Raw_PDF_Questions/x.pdf", "md": "05_X.md", "status": "excluded"})
            (root / ".mbset/state.json").write_text(json.dumps({"sources": srcs}), encoding="utf-8")
            out = run_cli("packets", str(root), "--n", "2")
            self.assertIn("worker not set: ask the user", out)          # the worker is the user's choice
            self.assertNotIn("gpt-6-luna", out)
            out = run_cli("packets", str(root), "--n", "2", "--dispatch", 'wk --brief "{brief}" --effort {effort}')
            self.assertIn('wk --brief "', out)
            self.assertIn("--effort max", out)
            briefs = sorted((root / ".mbset/packets").glob("packet_*_brief.txt"))
            self.assertEqual([b.name for b in briefs], ["packet_1_brief.txt", "packet_2_brief.txt"])
            texts = [b.read_text(encoding="utf-8") for b in briefs]
            bins, _ = catalog.packet_groups(json.loads((root / ".mbset/state.json").read_text()), 2)
            script = str(SCRIPTS / "mbset.py")
            for text, group in zip(texts, bins):
                nns = ",".join(sorted(s["nn"] for s in group))
                self.assertIn(str(root.resolve()), text)
                self.assertIn(script, text)
                self.assertIn(f"Your sources (NN list): {nns}", text)
                self.assertIn(f"--owner packet_", text)
                self.assertIn(f'check "$M" --only {nns}', text)
                self.assertIn('--source marked       # only marks you can see; else leave ?', text)
                self.assertIn("--source derived", text)
                self.assertIn("never paraphrase, shorten, reword", text)
                self.assertIn("Report contract", text)
                self.assertIn("Do NOT commit", text)
                self.assertNotIn("05", nns)                             # excluded sources are not packeted
            self.assertEqual(sorted(",".join(sorted(s["nn"] for s in g)) for g in bins), ["01", "02,03,04"])


class DocReaderAnswerTests(unittest.TestCase):
    def test_missing_index_is_never_answer_a(self):
        path = REPO / "أزهر دمياط/renal/scripts/build_docreader_files.py"
        spec = importlib.util.spec_from_file_location("renal_docreader", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        opts = ["one", "two", "three"]
        self.assertEqual(mod.answer_letter(opts, None), "?")
        self.assertEqual(mod.answer_letter(opts, 5), "?")
        self.assertEqual(mod.answer_letter(opts, -1), "?")
        self.assertEqual(mod.answer_letter(opts, True), "?")
        self.assertEqual(mod.answer_letter(opts, 0), "A")
        self.assertEqual(mod.answer_letter(opts, "2"), "C")
        self.assertEqual(mod.answer_letter(["one", "", "three"], 2), "B")   # empty option dropped before lettering
        self.assertEqual(mod.answer_letter(["one", "", "three"], 1), "?")


class TelegramLinkTests(unittest.TestCase):
    def test_public_private_and_range_links(self):
        from mbset.telegram import collect, parse_url
        self.assertEqual(parse_url("https://t.me/somechan/12"), [("somechan", 12)])
        self.assertEqual(parse_url("https://t.me/somechan/10-12"), [("somechan", 10), ("somechan", 11), ("somechan", 12)])
        self.assertEqual(parse_url("https://t.me/c/123456/7"), [(-100123456, 7)])
        self.assertEqual(parse_url("https://t.me/s/somechan/5"), [("somechan", 5)])
        for bad in ("https://example.com/x/1", "https://t.me/somechan", "https://t.me/c/abc/1", "https://t.me/ch/9-3"):
            with self.assertRaises(ValueError, msg=bad):
                parse_url(bad)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "links.md"
            f.write_text("1. **Lec 1**: [x](https://t.me/somechan/3)\nsee https://t.me/somechan/3, https://t.me/c/99/1.",
                         encoding="utf-8")
            self.assertEqual([(c, m) for _, c, m in collect([], f)], [("somechan", 3), (-10099, 1)])

    def test_setup_refuses_without_a_terminal(self):
        from unittest import mock
        with mock.patch("sys.stdin") as stdin:              # an agent's shell: no terminal to type into
            stdin.isatty.return_value = False
            with self.assertRaises(SystemExit) as ctx:
                main(["telegram", "setup"])
        self.assertIn("interactive", str(ctx.exception))


class UniversityTests(unittest.TestCase):
    def test_saved_university_wins_over_the_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "Assiut" / "Mod"
            root.mkdir(parents=True)
            from mbset.common import Module as M
            mod = M(root)
            self.assertEqual(mod.university, "Assiut")
            mod.state_path.write_text(json.dumps({"sources": [], "university": "Damietta"}), encoding="utf-8")
            self.assertEqual(mod.university, "Damietta")


class TaxonomyTests(unittest.TestCase):
    CASES = {
        "Damietta": {"Raw_PDF_Questions/Final 2023.pdf": "Exams, Final 2023",
                     "Raw_PDF_Questions/formative 2 2025.pdf": "Exams, Formative 2025",
                     "Raw_PDF_Questions/end 24.pdf": "Exams, End 2024",
                     "Raw_PDF_Questions/Dr elmorshdy questions(MCQ) 2025.pdf": "Professor, Dr Elmorshdy 2025",
                     "Raw_PDF_Questions/Physiology book 2026.pdf": "Department, Physiology 2026"},
        "Assiut": {"Raw_PDF_Questions/quiz week 3.pdf": "Department, Quizzes, Week 3",
                   "Raw_PDF_Questions/mid term 2022.pdf": "Exams, Midterm 2022",
                   "Raw_PDF_Questions/CBF GD 2 2023.pdf": "Department, GDs, <Subject> GD 2 2023"},
    }

    def test_builtin_taxonomies_keep_the_known_tags(self):
        from mbset import taxonomy
        for uni, cases in self.CASES.items():
            tax = taxonomy.load(uni)
            self.assertEqual(taxonomy.validate(tax), [])
            for rel, tag in cases.items():
                self.assertEqual(taxonomy.suggest(tax, rel)["tag"], tag, rel)
        s = taxonomy.suggest(taxonomy.load("Damietta"), "Raw_PDF_Questions/random notes.pdf")
        self.assertTrue(s["needs_year"])                                   # a year is never guessed
        self.assertIsNone(taxonomy.suggest(taxonomy.load("Assiut"), "Raw_PDF_Questions/quiz.pdf")["year"])

    def test_first_run_init_saves_settings_and_a_new_faculty(self):
        import importlib
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"MBSET_CONFIG_DIR": tmp}):
            from mbset import common, taxonomy, init
            for mod in (common, taxonomy, init):
                importlib.reload(mod)
            try:
                f = Path(tmp) / "new.yaml"
                f.write_text("name: Tanta\nrules:\n  - {match: 'final', tag: 'Exams, Final'}\n"
                             "default: {tag: 'Bank, {label}'}\n", encoding="utf-8")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    init.cmd_init(init_args(taxonomy_file=str(f), worker="Claude subagents", telegram="no"))
                cfg = common.load_config()
                self.assertEqual((cfg["university"], cfg["worker"], cfg["telegram"]), ("tanta", "Claude subagents", False))
                self.assertEqual(taxonomy.suggest(taxonomy.load("tanta"), "Raw_PDF_Questions/Final 2020.pdf")["tag"],
                                 "Exams, Final 2020")
                bad = Path(tmp) / "bad.yaml"
                bad.write_text("name: X\nrules:\n  - {match: '(', tag: 'Y'}\n", encoding="utf-8")
                with self.assertRaises(SystemExit):
                    init.cmd_init(init_args(taxonomy_file=str(bad)))
            finally:
                os.environ.pop("MBSET_CONFIG_DIR", None)
                for mod in (common, taxonomy, init):
                    importlib.reload(mod)


def init_args(**kw):
    import argparse
    base = dict(show=False, list=False, test=None, university=None, taxonomy_file=None, worker=None,
                dispatch=None, telegram=None, language=None)
    return argparse.Namespace(**{**base, **kw})


if __name__ == "__main__":
    unittest.main()


class TagHeuristicTests(unittest.TestCase):
    def test_arabic_letter_inside_word_is_not_a_professor(self):
        import os
        from mbset.inventory import suggest_tags
        from mbset.common import Module
        with tempfile.TemporaryDirectory() as d:
            root = os.path.join(d, "أزهر دمياط", "X")
            os.makedirs(root)
            m = Module(root)
            cairo = suggest_tags(m, "Raw_PDF_Questions/اسئله الجراحه كتاب القاهره شابتر الاندوكرين.pdf")
            self.assertNotIn("Professor", cairo["tag"])
            khaled = suggest_tags(m, "Raw_PDF_Questions/أسئلة MCQ د. خالد.pdf")
            self.assertEqual(khaled["tag"], "Professor, Dr <Name>")      # English only; agent transliterates
            self.assertEqual(suggest_tags(m, "Raw_PDF_Questions/Endocrine summtive 2025.pdf")["tag"], "Exams, End 2025")
            self.assertEqual(suggest_tags(m, "Raw_PDF_Questions/Final 26.pdf")["year"], 2026)


class WriterTests(unittest.TestCase):
    def test_more_than_six_options_does_not_crash_and_is_visible(self):
        from mbset.writer import render
        opts = [{"letter": L, "text": f"opt {L}"} for L in "ABCDEFGH"]
        md = render({"rel": "x.pdf", "nn": "01"},
                    [{"type": "QCS", "stem": "Glued stem", "options": opts, "correct": "H", "answer_source": "key"}])
        self.assertIn("**Extra Options (split or drop):** opt G | opt H", md)
        self.assertIn("**Correct Answer:** ?", md)                # never a wrong in-range letter
