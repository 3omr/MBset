# Parallel workflow

Large modules (40+ sources, 1 000+ pages) are split across several agents. The deterministic steps
(inventory, OCR, parse) are already fast, so parallelism pays off for the **review loop** —
flag triage, answer sheets and spot checks.

## Coordinator
```bash
python $S inventory "$M"
python $S ocr "$M" --jobs 3 --workers 4        # once, before splitting: the cache is shared
python $S parse "$M"
python $S packets "$M" --n 4                   # .mbset/packets/packet_1.md … packet_4.md
```
Hand each agent one packet file. It lists its sources and the exact command loop.

## Each agent
1. `lock "$M" <its NNs> --owner <name>` — refuses sources held by someone else.
2. Run the review loop from `pipeline-v2.md` for each of its sources only.
3. Touch only: `.mbset/profiles/NN.yaml`, `Markdown_Questions/NN_*.md`, `Images/NN_*`, and state
   entries of its NNs (through `fix`, `review`, `set`). Never edit the catalog, the tag map or the Excel.
4. Finish when `check "$M" --only <its NNs>` prints 0 hard failures; `lock … --release`.
5. Report: questions per file, answer-source counts, derived counts, anything excluded and why.

`state.json` is saved under a file lock with a three-way merge (only the sources and keys a command
changed are written), so agents working on different sources never overwrite each other; still,
never run two commands on the *same* NN at once.

## Coordinator, at the end
```bash
python $S check "$M"          # whole module, including reconciliation and duplicate NN
python $S catalog "$M"
python $S build "$M"
```
Then report per-file counts and every `derived` answer count to the user.

## Packet sizing
Packets are balanced by page count. Scanned exams cost the most review time (visual answer pass);
digital files with keys cost almost none. With 4 agents a 40-source module is typically one
packet of large scanned books and three of mixed exams.
