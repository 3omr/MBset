# Model routing — who does which step

With `mbset.py` the question text never passes through a model: the deterministic scripts extract,
answer from keys, count and gate. What is left is **judgement on flagged items**, and that is
delegated to Codex workers, one per packet, while the main agent orchestrates and re-verifies.

| Step | Needs | Who |
| :--- | :--- | :--- |
| `doctor`, `tidy`, `inventory`, `ocr`, `parse`, `check`, `catalog`, `build`, `report` | nothing — deterministic scripts | the orchestrator runs the commands |
| Confirming tags, exclusions, count notes (`set`) | filenames, source headers, the summary | orchestrator (or the packet worker for its own NNs) |
| Flag triage (`show --flags` → profile YAML or single `fix`) | reading evidence, editing YAML | **Codex gpt-6-luna, effort max** |
| Answer sheets of pen-marked scans (`answersheet` PNGs → `fix --answers … --source marked`) | reading ticks / circles reliably | **Codex gpt-6-luna, effort max** |
| Spot-check sheets (`spotcheck` PNGs → `review --spot`) | comparing a source crop with the markdown | **Codex gpt-6-luna, effort max** |
| QROC model answers and derived MCQ answers (`--exp-file`, `--source derived`) | medical knowledge, must be correct | **Codex gpt-6-luna, effort max**; always reported |
| Packets, dispatch, re-verification, final report | overview | the main agent (orchestrator) |

## Delegation command

Every judgement packet goes through the `codex-delegate` skill, **one Codex run per packet**, all
packets in parallel (background each call):

```bash
node ~/.agents/skills/codex-delegate/scripts/relay.mjs \
  --brief "$M/.mbset/packets/packet_k_brief.txt" --cd /home/omar/MBset \
  --model gpt-6-luna --effort max
```

- The model is **gpt-6-luna** and the effort **max** — never `gpt-5.6`, never a lower effort to save time.
- The brief is `packet_k_brief.txt`, written by `mbset.py packets`. Codex sees **nothing but the brief**
  (no chat, no skill, no AGENTS.md), so the brief is self-contained: module path, script path, its NN
  list, the exact command loop, the rules and the report contract. Do not hand Codex a brief you
  wrote by hand for a packet — regenerate it with `packets` so it carries the current rules.
- The relay never commits, and neither does the orchestrator unless the user asks.

## Rules for every worker (they are in the brief)
- Never transcribe, retype or paraphrase question text. A misread question is fixed through the
  profile + re-parse, or `fix` (answers, images, drops, model answers) — all keep the source wording.
- `fix --answers … --source marked` only when the mark is actually visible on the sheet. Unsure →
  leave the answer `?`; it is reported as unresolved, never guessed.
- Derived answers only via `--source derived` (MCQ) or `--exp-file` (QROC, `exp-source derived`),
  never mixed with read answers, and always listed in the report.
- Touch only the packet's own NNs; finish with `check --only <its NNs>`.
- Batch work: one answer sheet holds 6 questions, so a 30-question exam is 5 images and one
  `fix --answers` call.

## The orchestrator after each run
1. Read `result.json` (`finalMessage` is the worker's report); do not trust its gate claims.
2. Re-run `python $S check "$M" --only <NNs>` and `python $S report "$M"` and compare the per-file
   counts, answer-source counts and derived list with the worker's report.
3. Diff the markdown: no stem or option text may have changed except through a re-parse; any
   hand-typed wording is reverted and the packet re-dispatched with `--session <threadId>`.
4. Unresolved `?` answers go to a second, smaller packet (only those sheets) or to the user.
