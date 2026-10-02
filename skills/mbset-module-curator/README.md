# MBset Medical Module Curator Skill Package

Standard Operating Procedure (SOP) and automated toolkit for curating, extracting, verifying and building **MBset** medical question banks and lecture curricula.

One procedure (SKILL.md §2): scripts read every page they can for free (text layer, OCR, parser), parallel
workers read only the pages scripts cannot (verbatim questions + answers + model answers in one pass), and
deterministic gates decide when a module is done. First run sets the skill up for the person (faculty tag
system, worker, Telegram, language).

---

## 📦 Package Contents

```text
mbset-module-curator/
├── SKILL.md                     # the SOP: §0 first run · §1 hard rules · §2 extraction procedure · tags · lectures
├── README.md
├── references/
│   ├── first-run.md             # the onboarding the agent runs the first time
│   ├── setup-guide.md           # install + connect your own Telegram (EN / AR)
│   ├── commands.md              # every mbset.py command and flag
│   ├── workers.md               # briefs, who runs them, re-verification
│   ├── profiles.md              # per-source parser profiles
│   ├── schema-31-columns.md     # canonical 32-column schema + legacy migration map
│   ├── tagging-and-naming.md    # tag families
│   ├── subcategories-and-lectures.md
│   ├── taxonomies/              # tag systems per faculty (damietta, assiut, generic, folders)
│   └── profiles/                # profile templates
└── scripts/
    ├── mbset.py + mbset/        # the CLI (self-installing)
    ├── install.sh · requirements.txt · requirements-telegram.txt
    ├── build_module_template.py · validate_questions_excel.py · audit_question_bank.py
    └── clean_markdown_noise.py
```

---

## 🚀 Installation (anyone)

1. Copy this folder to `~/.claude/skills/mbset-module-curator/` (Claude Code), `<project>/.agents/skills/`
   (Codex and other agents) or `~/.gemini/antigravity/skills/` (Antigravity).
2. That's it — the skill sets itself up: the first `mbset.py doctor --fix` (the agent runs it) installs the
   Python packages into `<skill>/.venv` and the OCR/PDF tools (apt / brew / dnf; Windows: WSL). To do it
   ahead of time: `bash scripts/install.sh [--telegram]`.
3. Optional — Telegram: run `python3 scripts/mbset.py telegram setup` **yourself** once, with your own
   account (API id/hash from my.telegram.org).

Full guide in English and Arabic: [`references/setup-guide.md`](references/setup-guide.md).

---

## 🛠️ In commands

See SKILL.md §2 (the procedure) and `references/commands.md` (every flag).
