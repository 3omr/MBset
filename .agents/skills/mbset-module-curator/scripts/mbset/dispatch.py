"""`mbset.py dispatch` — run every pending brief with the worker command the user chose, N at a time.

    mbset.py dispatch "$M" [--only NN] [--parallel 3] [--retries 2] [--dispatch '<cmd {brief} {repo} {effort}>']

Pending = transcription chunks / key jobs without their JSON (and worklists without output). Each brief
runs as one shell command (the template saved at `init --dispatch`, or --dispatch, or MBSET_DISPATCH); a
brief whose JSON is still missing afterwards is retried. Delegate CLIs that share one login can lose it
when many processes refresh it at once (seen with Antigravity: 401 mid-run at 9 parallel), so keep
--parallel small (3) and let the retries pick up the rest. Claude subagents are dispatched by the main
agent with its Agent tool instead (one call per brief) — this command is for shell workers.
"""

from __future__ import annotations

import os
import shlex
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .common import Module, fill_template, load_config, load_json


def pending(module: Module, state: dict[str, Any], selector: str | None) -> list[tuple[str, Path]]:
    """(brief, expected output) for every transcription chunk / key job whose JSON is missing."""
    from .transcribe import tdir
    out: list[tuple[str, Path]] = []
    for src in module.sources(state, selector):
        m = load_json(tdir(module, src) / "manifest.json")
        if not m:
            continue
        for c in m["chunks"]:
            if not Path(c["out"]).exists():
                out.append((c["brief"], Path(c["out"])))
        for k in m.get("keys") or []:
            if not Path(k["out"]).exists():
                out.append((k["brief"], Path(k["out"])))
    return out


def cmd_dispatch(args) -> int:
    from .catalog import repo_root
    template = args.dispatch or os.environ.get("MBSET_DISPATCH") or load_config().get("dispatch")
    if not template:
        raise SystemExit("[-] no worker command: ask the user which worker runs the briefs (SKILL.md §0), then "
                         "`init --dispatch '<cmd with {brief}>'` — Claude subagents are dispatched with the Agent tool")
    module = Module(args.module)
    state = module.load()
    repo = repo_root(module.root)
    logs = module.meta / "work" / "dispatch"
    logs.mkdir(parents=True, exist_ok=True)

    import threading
    gate = threading.Lock()
    last = [0.0]

    def run(item: tuple[str, Path]) -> tuple[str, bool, float]:
        brief, out = item
        with gate:                           # stagger the starts: simultaneous logins refresh one token at once
            wait = last[0] + getattr(args, "stagger", 0) - time.time()
            if wait > 0:
                time.sleep(wait)
            last[0] = time.time()
        t0 = time.time()
        cmd = fill_template(template, brief=shlex.quote(brief), repo=shlex.quote(str(repo)), effort=args.effort)
        with open(logs / (Path(brief).stem + ".log"), "a", encoding="utf-8") as log:
            subprocess.run(cmd, shell=True, stdout=log, stderr=subprocess.STDOUT)
        return brief, out.exists(), time.time() - t0

    from .consensus import pending as consensus_pending
    todo = pending(module, state, args.only) + consensus_pending(module)
    if not todo:
        print("[=] nothing pending")
        return 0
    for attempt in range(1, args.retries + 2):
        print(f"[*] round {attempt}: {len(todo)} brief(s), {args.parallel} at a time")
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            for brief, ok, secs in pool.map(run, todo):
                print(f"    {'OK ' if ok else 'NO '} {Path(brief).name}  {secs / 60:.1f} min")
        todo = [t for t in todo if not t[1].exists()]
        if not todo:
            break
    if todo:
        print(f"[-] still missing after {args.retries + 1} round(s): {[Path(b).name for b, _ in todo]} "
              f"(logs in {logs})")
        return 1
    print('[=] all briefs done — next: parse "$M" --only NN')
    return 0


def register(sub) -> None:
    p = sub.add_parser("dispatch", help="run pending briefs with the chosen worker command, N at a time, retrying")
    p.add_argument("module")
    p.add_argument("--only", help="NN list")
    p.add_argument("--parallel", type=int, default=3, help="briefs at once (shared logins dislike many)")
    p.add_argument("--retries", type=int, default=2, help="extra rounds for briefs whose JSON is still missing")
    p.add_argument("--effort", default="high")
    p.add_argument("--stagger", type=float, default=20, help="seconds between two starts (default 20)")
    p.add_argument("--dispatch", help="worker command with {brief} {repo} {effort} (default: saved at init)")
    p.set_defaults(fn=cmd_dispatch)
