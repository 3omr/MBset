# Parallel workflow — packets, Codex workers, locks

Large modules (40+ sources, 1 000+ pages) are split into packets. The deterministic steps
(inventory, OCR, parse) are already fast and run once, by the orchestrator; parallelism pays off for
the **judgement loop** — flag triage, answer sheets of pen-marked scans, spot checks and QROC /
derived answers — which is delegated to Codex **gpt-6-luna** at effort **max**, one run per packet
(see [`model-routing.md`](./model-routing.md)).

## Orchestrator (main agent)
```bash
S=.agents/skills/mbset-module-curator/scripts/mbset.py
python $S inventory "$M"
python $S ocr "$M" --jobs 3 --workers 4        # once, before splitting: the cache is shared
python $S parse "$M"
python $S packets "$M" --n 4                   # .mbset/packets/packet_k.md + packet_k_brief.txt
```
`packets` writes, per packet, `packet_k.md` (human-readable) and `packet_k_brief.txt`: a
**self-contained** Codex brief. Codex sees only that text — no chat history, no skill, no AGENTS.md —
so the brief carries the module path, the script path, its NN list, the lock/review loop below
verbatim, the rules and the report contract. Dispatch every packet at once, each in the background:

```bash
for k in 1 2 3 4; do
  node ~/.agents/skills/codex-delegate/scripts/relay.mjs \
    --brief "$M/.mbset/packets/packet_${k}_brief.txt" --cd /home/omar/MBset \
    --model gpt-6-luna --effort max &
done; wait
```
Never `gpt-5.6`; never one Codex run for several packets.

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
map or the Excel, never retypes question text, and never commits.

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
