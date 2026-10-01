# Model routing — who does which step

With `mbset.py` the question text passes through a model only where the page must be read: the
deterministic scripts extract, answer from keys, count and gate. The judgement and reading work is
written into **self-contained briefs** and handed to workers; **which worker is the user's choice**
(SKILL.md, "Choosing the worker"). The main agent orchestrates and re-verifies.

| Step | Needs | Who | Effort |
| :--- | :--- | :--- | :--- |
| `doctor`, `tidy`, `inventory`, `ocr`, `parse`, `route`, `check`, `catalog`, `build`, `report`, `worklist --apply` | nothing — deterministic scripts | the main agent runs the commands | — |
| Confirming tags, exclusions, count notes (`set`) | filenames, source headers, the summary | main agent | — |
| Transcription chunks (`transcribe` briefs → `chunk_KK.json`: verbatim questions + answers + model answers) | reading page images exactly | chosen worker, one per chunk, all at once | high |
| Worklist parts (`worklist` briefs → JSON) | re-reading crops, reading marks | chosen worker, one per part | high; max for parts with MODEL items or files with no key |
| Flag triage, packets (`packets` briefs) | reading evidence, editing YAML | chosen worker | max |
| QROC model answers and derived MCQ answers | medical knowledge, must be correct | chosen worker; always reported | max |
| Dispatch, re-verification, final report | overview | main agent | — |

## Dispatching

Ask the user first (once per module/session), offering what exists: Claude subagents (always), the
delegate CLIs `mbset.py doctor` found, or the main agent alone. Then:

- **Claude subagents**: one background `Agent` call per brief, prompt: `Read <brief path> and do exactly
  what it says. Your final message is the report the brief asks for.`
- **A delegate CLI** (Codex, Antigravity, Cursor, OpenCode, …): pass its command once and every
  `transcribe` / `worklist` / `packets` run prints a ready line per brief:
  ```bash
  python $S transcribe "$M" --only 07,09 --dispatch '<cli> … --brief "{brief}" --cd "{repo}" --effort {effort}'
  # or: export MBSET_DISPATCH='<same template>'
  ```
  Use the model the user named. Run every line in the background, all at once.
- **No workers**: the main agent follows the briefs one by one.

Rules for every choice:
- A brief is all the worker sees (no chat, no skill, no AGENTS.md). Regenerate briefs with the script —
  never hand-write one — so they carry the current rules.
- Big files are never one run: transcription is split into page chunks and worklists into question
  ranges, so a timeout costs one chunk, not hours. A failed chunk is simply re-dispatched.
- If a worker runs out of credits or fails repeatedly, ask the user which worker to continue with.
- Workers never commit.

## Rules for every worker (they are in the brief)
- Question text is copied **exactly as printed** — never paraphrased, shortened or completed from
  knowledge; corrections are re-reads of the page image, logged with the original.
- `marked` only when the mark is actually visible; `key` only when printed; `derived` only when the source
  has no answer for that question, and always listed in the report.
- Write only the files the brief names.

## The main agent after each run
1. Read the worker's final message as a claim, not a result.
2. `transcribe --status` / `worklist --apply`, then `check` and `report`; compare per-file counts,
   answer-source counts and the derived list with the worker's report.
3. Spot-check (`spotcheck` → `review --spot`); `transcript_not_in_page_text` and large text corrections
   are reviewed against the page. Anything hand-typed or paraphrased is re-dispatched.
4. Report per-file counts and every `derived` answer count to the user.
