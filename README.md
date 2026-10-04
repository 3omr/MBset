# MBset — mbset-module-curator skill

An agent skill that turns medical exam sources (PDFs, scans, Word files, slides, screenshots) into verbatim
markdown and the 32-column MBset question-bank Excel, plus lecture subcategories. Works with Claude Code,
Codex, Antigravity and other agents that read `SKILL.md`.

## Install
Copy [`skills/mbset-module-curator/`](skills/mbset-module-curator/) into your agent's skills folder:

| Agent | Folder |
|---|---|
| Claude Code | `~/.claude/skills/mbset-module-curator/` |
| Codex / generic agents | `<project>/.agents/skills/mbset-module-curator/` |
| Antigravity | `~/.gemini/antigravity/skills/mbset-module-curator/` |

Then ask your agent to use it — the first run sets it up for you (faculty tag system, which worker runs the
briefs, optional Telegram with your own account, reply language). Full guide (English / العربي):
[`references/setup-guide.md`](skills/mbset-module-curator/references/setup-guide.md).

## Develop
`python3 -m unittest discover tests` — tests run against `.agents/skills/…` when present, else `skills/…`.
`scripts/sync_skill.sh` mirrors a working copy in `.agents/skills/` to `skills/` (`--check` to verify).
