# Workers — who reads the pages, and how briefs are dispatched

Scripts do everything they can (inventory, OCR, parse, gates, build). What needs eyes is written into
**self-contained briefs**; a worker sees only its brief and writes only the JSON file the brief names. The
main agent dispatches, then ingests/applies and re-verifies with the gates.

## The briefs

| Brief | Made by | Worker writes | Then | Effort |
| :--- | :--- | :--- | :--- | :--- |
| transcription chunk (6 pages) | `transcribe "$M" --only NN` | `.mbset/transcripts/NN/chunk_KK.json` | `transcribe --status` → `parse --only NN` | high |
| answer-key job | `transcribe … --key-pages P` | `.mbset/transcripts/NN/key.json` | same | high |
| worklist part (question range) | `worklist "$M"` | `.mbset/packets/worklist/out/<NN[_pK]>/*.json` | `worklist --apply` | high; max with model answers |

Big files are never one run: a timeout costs one chunk, which is simply re-dispatched (`--status` lists it).
Chunk splits are stable once made.

## Who runs them — the user's choice

Asked at first-run setup (SKILL.md §0) and saved (`init --show`); never assumed. If it fails or runs out of
credits, ask again.

- **Claude subagents** (always available): one background `Agent` call per brief, all at once —
  `Read <brief path> and do exactly what it says. Your final message is the report the brief asks for.`
- **A delegate CLI** (Codex, Antigravity/Gemini, Cursor, OpenCode… — `doctor` lists what is installed): save
  its command once (`init --dispatch '<cmd with {brief} {repo} {effort}>'`) and `transcribe` / `worklist`
  print one ready line per brief. `mbset.py dispatch "$M" [--only NN] [--parallel 3] [--retries 2]` runs every
  pending brief with it and retries the ones whose JSON is still missing — keep parallelism low: 9 parallel
  Antigravity runs lost their shared login (401) mid-run, 3 at a time did not. Use `transcribe --format png` (page
  image + its OCR text) unless the worker's file tool reads PDFs; Antigravity's reads images only.
  Example (Antigravity): `node <agy-delegate>/scripts/relay.mjs --brief "{brief}" --cd "$(dirname {brief})"
  --model gemini-3.8-flash-high --timeout 25m`
- **None**: the main agent works through the briefs itself, one after another (slowest).

## After every run — never trust the self-report

1. `transcribe --status` / `worklist --apply`, then `check` and `report`.
2. Hard failures name the chunk or question (missing chunk, chunk count mismatch, gap, key not among the
   options, bias) → re-dispatch that chunk or fix that question.
3. `transcript_not_in_page_text` and large text corrections are compared with the page; anything
   paraphrased is re-dispatched.
4. Spot-check every file (`spotcheck` → `review --spot`), then report per-file counts and every `derived`
   count to the user.
