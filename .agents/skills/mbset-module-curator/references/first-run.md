# First run — set the skill up for this person

SKILL.md §0 points here. `$S` = `<skill>/scripts/mbset.py`.
Run `python3 $S init --show` at the start of every session. If it prints **NOT INITIALIZED**, run this
onboarding before any module work. Its answers are saved in `~/.config/mbset/` and never asked again; the
user can change them later with `init`.

**Step 1 — ask the user** (one AskUserQuestion with up to 4 questions; use their language):
1. **Faculty / university.** Offer the faculties listed by `init --list` (Damietta, Assiut) plus *Other*.
   For *Other*, ask its name.
2. **Who runs the heavy work** (transcription / review briefs): *Claude subagents* (always available), each
   delegate CLI that `doctor` finds (Codex, Antigravity, Cursor, OpenCode…), or *none* (the main agent works
   alone). If they pick a CLI, ask which model.
3. **Telegram:** do their sources come from Telegram channels or groups?
4. **Reply language** (Arabic / English).

**Step 2 — tag system for their faculty.**
- **Built-in faculty:** show `init --list`'s rules for it in plain words and ask if that matches how their
  faculty labels sources.
- **Other (or rules that don't fit):** show the generic families (`init --list`, *Generic*). Ask how their
  faculty names its sources: exam rounds (final / midterm / formative / quiz…), department or subject
  books, professor collections, external banks, and which families carry no year. Write a taxonomy YAML
  (format in `scripts/mbset/taxonomy.py`; examples in `references/taxonomies/`) and preview it on their
  real filenames: `init --test "<file 1>" "<file 2>" … --university <name>`. Adjust until they agree.
  Then save it with `--taxonomy-file`.
- Also ask for their platform `categoryId` prefix, if they know it. Otherwise it comes from the platform
  export later.

**Step 3 — save:**
`python3 $S init --university <name> [--taxonomy-file f.yaml] --worker "<choice>" [--dispatch '<cmd {brief}>'] --telegram yes|no --language ar|en`

**Step 4 — tools:**
- Run `python3 $S doctor --fix` (add `--telegram` if they use Telegram). Missing Python packages go into
  `<skill>/.venv` automatically, and later `mbset.py` calls use it. Missing OCR/PDF tools are installed
  with apt/brew/dnf when that needs no password.
- If it prints `[!] needs administrator rights`, show the user the printed command and ask them to run it
  in their own terminal. Never type a sudo password.
- If they use Telegram and `doctor` says credentials or login are missing, the user connects **their own
  account** once with `mbset.py telegram setup`:
  - if the host lets you start a command in the user's own terminal (e.g. the Terminal panel of the Claude
    desktop app), start `python3 $S telegram setup` there and tell them to type the answers there;
  - otherwise give them the command and [`references/setup-guide.md`](./references/setup-guide.md).
  Never ask for, read back, type or store their api_hash, phone number, login code or password, and do
  not read that terminal while they type.
- Re-run `doctor` until it shows 0 FAIL.

**After setup:**
- Modules use the saved faculty's taxonomy. A module from another faculty (e.g. an Assiut folder for a
  Damietta user) takes `inventory --university <name>`.
- The saved worker is used for every dispatch (`--dispatch` / `MBSET_DISPATCH` override it). If it fails
  or runs out of credits, ask again.
