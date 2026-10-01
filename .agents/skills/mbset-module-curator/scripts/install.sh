#!/usr/bin/env bash
# Optional one-command setup. The skill also sets itself up on first use (mbset.py creates <skill>/.venv
# and installs its packages automatically); this script just does it ahead of time.
#
#   bash <skill>/scripts/install.sh              # Python packages + system tools (asks for sudo if needed)
#   bash <skill>/scripts/install.sh --telegram   # also the Telegram downloader
#
# It never touches your Telegram account: afterwards YOU run `telegram setup` yourself
# (references/setup-guide.md). Re-running is safe.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null || { echo "[-] python3 not found — install Python 3.10+ first"; exit 1; }
"$PY" -c 'import sys; sys.exit(sys.version_info < (3, 10))' || { echo "[-] Python 3.10+ is required"; exit 1; }
EXTRA=()
[[ " $* " == *" --telegram "* ]] && EXTRA+=(--telegram)
# doctor --fix: packages into <skill>/.venv, system tools via apt/brew/dnf (sudo prompts in YOUR terminal)
"$PY" "$HERE/mbset.py" doctor --fix ${EXTRA[@]+"${EXTRA[@]}"} || true
if [[ " $* " == *" --telegram "* ]]; then
  echo
  echo "Next (once, yourself — it uses YOUR Telegram account):"
  echo "    $PY \"$HERE/mbset.py\" telegram setup"
fi
