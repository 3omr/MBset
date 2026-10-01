#!/usr/bin/env python3
"""MBset question-bank pipeline — one command line for Stages 0-4.

    python mbset.py doctor     [<Module>] [--fix] [--telegram]  # health check; --fix installs what is missing
    python mbset.py telegram   setup|status|download …
    python mbset.py run        <Module>        # inventory → OCR → parse → check (mechanical part)
    python mbset.py inventory  <Module>        # Stage 0
    python mbset.py ocr        <Module>        # Stage 0.5 (cached, parallel)
    python mbset.py parse      <Module> [--only NN]
    python mbset.py route      <Module>        # parse or transcribe, per source
    python mbset.py transcribe <Module> --only NN
    python mbset.py worklist   <Module> [--apply]
    python mbset.py show       <Module> NN --flags
    python mbset.py fix        <Module> NN --answer 12=B:marked --drop 7 --reason "..."
    python mbset.py figures    <Module> [--only NN]
    python mbset.py spotcheck  <Module> [--only NN]
    python mbset.py review     <Module> NN --spot "6/6 OK"
    python mbset.py check      <Module> [--only NN]
    python mbset.py build      <Module>
    python mbset.py status     <Module>
    python mbset.py report     <Module>        # final per-file report (answer sources, derived)
    python mbset.py tidy       <Module> [--apply] [--lectures-from DIR]   # dry run unless --apply
    python mbset.py lectures   <Module> plan|match|apply|check
    python mbset.py crossdup   <UniversityRoot>...

Self-setup: on a machine without the Python packages, the first run creates `<skill>/.venv`, installs
`requirements.txt` into it (and `requirements-telegram.txt` for `telegram`) and re-runs itself there;
later runs use that environment automatically. Set MBSET_NO_BOOTSTRAP=1 to turn this off.

See ../SKILL.md, ../references/setup-guide.md and ../references/pipeline-v2.md.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV = HERE.parent / ".venv"
VENV_PY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
REQUIRED = ("fitz", "yaml", "openpyxl", "PIL", "rapidfuzz")


def _missing(names) -> list:
    return [n for n in names if importlib.util.find_spec(n) is None]


def bootstrap() -> None:
    """Make the packages this command needs importable, without touching the system Python."""
    if os.environ.get("MBSET_NO_BOOTSTRAP"):
        return
    want_tg = (len(sys.argv) > 1 and sys.argv[1] == "telegram") or "--telegram" in sys.argv
    need = _missing(REQUIRED) + (_missing(("telethon",)) if want_tg else [])
    in_venv = Path(sys.prefix).resolve() == VENV.resolve()
    if not need:
        return
    if VENV_PY.exists() and not in_venv:            # set up earlier: just use it
        os.execv(str(VENV_PY), [str(VENV_PY), __file__, *sys.argv[1:]])
    if os.environ.get("MBSET_BOOTSTRAPPED"):
        return                                      # one install attempt per invocation, never a loop
    os.environ["MBSET_BOOTSTRAPPED"] = "1"
    print(f"[*] first run: installing the toolkit's Python packages into {VENV} (once)…", file=sys.stderr)
    try:
        if not VENV_PY.exists():
            subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
        reqs = ["-r", str(HERE / "requirements.txt")]
        if want_tg:
            reqs += ["-r", str(HERE / "requirements-telegram.txt")]
        subprocess.run([str(VENV_PY), "-m", "pip", "install", "-q", "--upgrade", "pip"], check=False)
        subprocess.run([str(VENV_PY), "-m", "pip", "install", "-q", *reqs], check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        sys.exit(f"[-] automatic setup failed ({exc}). On Debian/Ubuntu install python3-venv first "
                 f"(sudo apt-get install python3-venv), or run: bash {HERE / 'install.sh'}")
    os.execv(str(VENV_PY), [str(VENV_PY), __file__, *sys.argv[1:]])


bootstrap()
sys.path.insert(0, str(HERE))

from mbset.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
