#!/usr/bin/env bash
# Mirror the workspace skill (.agents/skills/…) to skills/… — AGENTS.md requires both to stay in sync.
# Usage: scripts/sync_skill.sh [--check]   (--check: exit 1 if they differ, change nothing)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=.agents/skills/mbset-module-curator/
DST=skills/mbset-module-curator/
if [[ "${1:-}" == "--check" ]]; then
  if diff -rq --exclude=__pycache__ "$SRC" "$DST"; then echo "[+] skill mirror in sync"; else echo "[-] run scripts/sync_skill.sh"; exit 1; fi
  exit 0
fi
rsync -a --delete --exclude=__pycache__ "$SRC" "$DST"
echo "[+] synced $SRC → $DST"
