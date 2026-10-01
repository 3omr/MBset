"""`doctor` — environment (and optionally module) health check. OK / WARN / FAIL lines; exit 1 on FAIL."""

from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]              # .../mbset-module-curator
REPO = SKILL.parents[2] if SKILL.parent.name == "skills" and SKILL.parents[1].name == ".agents" else None
PY_MODULES = [  # (import name, pip name, required)
    ("fitz", "PyMuPDF", True), ("yaml", "PyYAML", True), ("openpyxl", "openpyxl", True),
    ("PIL", "Pillow", True), ("rapidfuzz", "rapidfuzz", True),
    ("docx", "python-docx", False), ("pptx", "python-pptx", False),
]
STALE_LOCK_HOURS = 12


class Report:
    def __init__(self):
        self.fails = self.warns = 0

    def __call__(self, level: str, what: str) -> None:
        self.fails += level == "FAIL"
        self.warns += level == "WARN"
        print(f"  {level:4}  {what}")


def _run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, str(exc)


def check_env(say: Report) -> None:
    tess = shutil.which("tesseract")
    if not tess:
        say("FAIL", "tesseract not found (apt install tesseract-ocr tesseract-ocr-ara)")
    else:
        _, out = _run([tess, "--version"])
        say("OK", f"tesseract {out.splitlines()[0] if out else ''}".strip())
        _, langs = _run([tess, "--list-langs"])
        have = {ln.strip() for ln in langs.splitlines()[1:]}
        for lang in ("eng", "ara"):
            say("OK" if lang in have else "FAIL", f"tesseract language '{lang}'"
                + ("" if lang in have else f" missing (apt install tesseract-ocr-{lang})"))
    for tool in ("pdftotext", "pdftoppm"):
        say("OK" if shutil.which(tool) else "FAIL", f"{tool}" + ("" if shutil.which(tool) else " not found (poppler-utils)"))
    arch = [t for t in ("unrar", "7z") if shutil.which(t)]
    say("OK" if arch else "WARN", f"archive tools: {', '.join(arch) or 'none (rar/7z sources cannot be expanded)'}")
    for mod, pip, required in PY_MODULES:
        try:
            m = importlib.import_module(mod)
            ver = getattr(m, "__version__", None) or getattr(m, "VersionBind", None) or "?"
            say("OK", f"python {mod} ({pip} {ver})")
        except Exception as exc:  # noqa: BLE001 — any import failure is a finding
            say("FAIL" if required else "WARN", f"python {mod}: {type(exc).__name__} (pip install {pip})")
    req = SKILL / "scripts" / "requirements.txt"
    if req.exists():
        listed = {ln.split(">")[0].split("=")[0].strip().lower() for ln in req.read_text().splitlines()
                  if ln.strip() and not ln.startswith("#")}
        unchecked = listed - {p.lower() for _, p, _ in PY_MODULES}
        if unchecked:
            say("WARN", f"requirements.txt lists packages doctor does not check: {sorted(unchecked)}")
    check_sync(say)
    # optional external workers — the user picks one (or Claude subagents, which need nothing installed)
    found = [name for name in ("codex", "agy", "claude", "gemini", "cursor-agent", "opencode", "aider", "kimi")
             if shutil.which(name)]
    say("OK", f"worker CLIs found: {', '.join(found) or 'none'} — the user chooses the worker; Claude "
              f"subagents need no CLI")


def check_sync(say: Report) -> None:
    if REPO is None:
        say("WARN", f"skill mirror check skipped (skill not under <repo>/.agents/skills: {SKILL})")
        return
    mirror = REPO / "skills" / SKILL.name
    script = REPO / "scripts" / "sync_skill.sh"
    if not mirror.is_dir():
        say("FAIL", f"skill mirror missing: {mirror}")
        return
    if script.exists():
        rc, out = _run(["bash", str(script), "--check"], timeout=60)
    else:
        rc, out = _run(["diff", "-rq", "--exclude=__pycache__", str(SKILL), str(mirror)], timeout=60)
    if rc == 0:
        say("OK", "skill mirror .agents/skills ↔ skills in sync")
    else:
        diffs = [ln for ln in out.splitlines() if ln.startswith(("Only in", "Files"))]
        say("FAIL", f"skill mirror out of sync ({len(diffs)} difference(s)) — run scripts/sync_skill.sh")
        for ln in diffs[:8]:
            print(f"          {ln}")
        if len(diffs) > 8:
            print(f"          … {len(diffs) - 8} more")


def check_module(say: Report, path: str) -> None:
    root = Path(path).resolve()
    if not root.is_dir():
        say("FAIL", f"module folder not found: {root}")
        return
    say("OK" if (root / "Raw_PDF_Questions").is_dir() else "FAIL", "Raw_PDF_Questions/ exists")
    state = root / ".mbset" / "state.json"
    if not state.exists():
        say("WARN", "no .mbset/state.json yet (run `mbset.py inventory`)")
    else:
        try:
            data = json.loads(state.read_text(encoding="utf-8"))
            say("OK", f"state.json readable ({len(data.get('sources', []))} sources)")
        except (OSError, ValueError) as exc:
            say("FAIL", f"state.json unreadable: {exc}")
    tmp = list((root / ".mbset").glob("state.*.tmp"))
    if tmp:
        say("WARN", f"{len(tmp)} leftover state temp file(s) (interrupted save?)")
    locks = root / ".mbset" / "locks"
    stale = []
    for lk in sorted(locks.glob("*.lock")) if locks.is_dir() else []:
        age = (time.time() - lk.stat().st_mtime) / 3600
        if age > STALE_LOCK_HOURS:
            stale.append(f"{lk.stem} ({age:.0f}h)")
    say("WARN" if stale else "OK", f"stale locks > {STALE_LOCK_HOURS}h: {', '.join(stale)} — `mbset.py lock <m> NN --release`"
        if stale else "no stale locks")
    say("OK" if (root / "Markdown_Questions").is_dir() else "WARN", "Markdown_Questions/ exists")


def cmd_doctor(args) -> int:
    say = Report()
    print("environment:")
    check_env(say)
    if args.module:
        print(f"module {args.module}:")
        check_module(say, args.module)
    print(f"\n[{'-' if say.fails else '+'}] {say.fails} FAIL · {say.warns} WARN")
    return 1 if say.fails else 0


def register(sub) -> None:
    p = sub.add_parser("doctor", help="check tools, python modules, skill mirror sync (and a module's state/locks)")
    p.add_argument("module", nargs="?", help="optional module folder")
    p.set_defaults(fn=cmd_doctor)
