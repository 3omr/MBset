# Parallel workflow — chunks, worklist parts, packets

## Default: JSON-only workers, big files always split
Two kinds of parallel unit, both safe without locks because the worker writes **only JSON** and the
coordinator ingests/applies it:

| Unit | Made by | Worker writes | Coordinator |
| :--- | :--- | :--- | :--- |
| transcription chunk (6 pages) | `transcribe "$M" --only NN` | `.mbset/transcripts/NN/chunk_KK.json` | `transcribe --status` → `parse --only NN` → `check` |
| worklist part (≤ 60 cost, question range) | `worklist "$M"` | `.mbset/packets/worklist/out/<NN[_pK]>/{text,answers,model,drop,add}.json` | `worklist --apply` → `check` |

```bash
python $S route "$M"                                # which sources go to transcribe
python $S transcribe "$M" --only 07,09,12 [--dispatch '<worker cmd with {brief}>']
#   → one brief (or one ready command) per chunk; dispatch them all at once to the worker the user chose
python $S transcribe "$M" --status && python $S parse "$M" --only 07,09,12
python $S worklist "$M" [--dispatch …]              # what is left anywhere, big files in parts
#   → one brief per worklist; dispatch them all at once
python $S worklist "$M" --apply && python $S check "$M"
```
With Claude subagents: one background `Agent` call per brief ("Read <brief> and do exactly what it says").
With a delegate CLI: `--dispatch` (or `MBSET_DISPATCH`) makes the scripts print one ready line per brief.
A chunk whose worker died is simply re-dispatched (its JSON is missing; `--status` lists it). The split is
stable once made, so a re-run of `transcribe` never moves pages between chunks.

## Legacy: whole-source packets (small parse-route files only)

Large modules (40+ sources, 1 000+ pages) are split into packets. The deterministic steps
(inventory, OCR, parse) are already fast and run once, by the orchestrator; parallelism pays off for
the **judgement loop** — flag triage, answer sheets of pen-marked scans, spot checks and QROC /
derived answers — which is delegated to the worker the user chose, effort **max**, one run per packet
(see [`model-routing.md`](./model-routing.md)).

## Orchestrator (main agent)
```bash
S=<skill>/scripts/mbset.py
python $S inventory "$M"
python $S ocr "$M" --jobs 3 --workers 4        # once, before splitting: the cache is shared
python $S parse "$M"
python $S packets "$M" --n 4                   # .mbset/packets/packet_k.md + packet_k_brief.txt
```
`packets` writes, per packet, `packet_k.md` (human-readable) and `packet_k_brief.txt`: a
**self-contained** worker brief. The worker sees only that text — no chat history, no skill, no AGENTS.md —
so the brief carries the module path, the script path, its NN list, the lock/review loop below
verbatim, the rules and the report contract. Dispatch every packet at once, each in the background:

`packets` prints one ready line per packet when `--dispatch` / `MBSET_DISPATCH` is set; otherwise
dispatch each `packet_k_brief.txt` to the chosen worker (Claude subagent: one `Agent` call each).
Never one worker run for several packets.

## Each worker (the loop in the brief)
```bash
python $S lock "$M" <NNs> --owner packet_k        # refuses sources held by someone else
python $S parse "$M" --only NN                    # profile → markdown + flags
python $S show "$M" NN --flags                    # read only the flagged questions
python $S show "$M" NN --dropped                  # the noise filter must not have eaten a question
#   profile problem → edit .mbset/profiles/NN.yaml, then parse --only NN again
python $S fix "$M" NN --drop 7 --reason "…"       # single questions (also --image N=Images/NN_QN.png)
python $S answersheet "$M" --only NN              # unanswered MCQs: view the PNGs, read the marks
python $S fix "$M" NN --answers "3=B 4=D" --source marked       # only marks you can see; else leave ?
python $S fix "$M" NN --answers "9=C" --source derived          # only when the source has no answer
python $S fix "$M" NN --exp-file answers.json     # QROC model answers {"N": "…"} (derived)
python $S figures "$M" --only NN                  # if figure-dependent questions exist
python $S spotcheck "$M" --only NN                # view the PNG sheets it prints
python $S review "$M" NN --spot "6/6 OK"
python $S check "$M" --only <NNs>                 # must print 0 hard failures
python $S lock "$M" <NNs> --release
```
A worker touches only `.mbset/profiles/NN.yaml`, `Markdown_Questions/NN_*.md`, `Images/NN_*` and
the state entries of its NNs (through `fix`, `review`, `set`). It never edits the catalog, the tag
map or the Excel, never paraphrases question text (corrections only as exact re-reads of the page
through `fix --text-file`), and never commits.

**Report contract** (the worker's final message): per file — questions, MCQ, QROC, answered;
answer-source counts (key / marked / online / derived / `?`); every derived answer as `NN Qn`;
unresolved flags and `?` answers with the reason; the last `check --only` summary line.

`state.json` is saved under a file lock with a three-way merge (only the sources and keys a command
changed are written), so workers on different sources never overwrite each other; still, never run
two commands on the *same* NN at once.

## Orchestrator, after the runs
```bash
python $S check "$M" --only <packet NNs>      # per packet: re-verify, never trust the self-report
python $S report "$M"                         # compare counts / answer sources / derived with each report
python $S check "$M"                          # whole module, including reconciliation and duplicate NN
python $S catalog "$M"
python $S build "$M"
```
Diff the markdown of each packet: stem and option wording changes only through a re-parse. Re-send
a delta brief with `--session <threadId>` (from `result.json`) for anything left. Then report per-file
counts and every `derived` answer count to the user.

## Packet sizing
Packets are balanced by page count. Scanned exams cost the most review time (visual answer pass);
digital files with keys cost almost none. With 4 workers a 40-source module is typically one packet
of large scanned books and three of mixed exams.
