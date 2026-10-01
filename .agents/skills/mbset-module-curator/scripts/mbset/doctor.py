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
    # optional Telegram downloader (mbset.py telegram) — nothing secret is printed
    try:
        import telethon  # noqa: F401
        from .telegram import ENV_FILE, SESSION
        creds = ENV_FILE.exists()
        session = any(SESSION.parent.glob(SESSION.name + ".session*"))
        say("OK" if creds and session else "WARN",
            f"telegram: Telethon installed, credentials {'saved' if creds else 'missing'}, "
            f"login {'saved' if session else 'missing'}"
            + ("" if creds and session else " — the user runs `mbset.py telegram setup` (optional)"))
    except ImportError:
        say("WARN", "telegram: Telethon not installed (optional: pip install -r scripts/requirements-telegram.txt)")
    # optional external workers — the user picks one (or Claude subagents, which need nothing installed)
    found = [name for name in ("codex", "agy", "claude", "gemini", "cursor-agent", "opencode", "aider", "kimi")
             if shutil.which(name)]
    say("OK", f"worker CLIs found: {', '.join(found) or 'none'} — the user chooses the worker; Claude "
              f"subagents need no CLI")


def check_sync(say: Report) -> None:
    if REPO is None:
        say("OK", f"standalone install at {SKILL} (no repo mirror to check)")
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


def system_install_command() -> list[str] | None:
    """The package-manager command for the OCR / PDF / archive tools on this OS (None: unknown OS)."""
    import platform
    if platform.system() == "Darwin" and shutil.which("brew"):
        return ["brew", "install", "tesseract", "tesseract-lang", "poppler", "p7zip"]
    if platform.system() == "Linux" and shutil.which("apt-get"):
        return ["sudo", "apt-get", "install", "-y", "tesseract-ocr", "tesseract-ocr-ara", "tesseract-ocr-eng",
                "poppler-utils", "p7zip-full", "python3-venv"]
    if platform.system() == "Linux" and shutil.which("dnf"):
        return ["sudo", "dnf", "install", "-y", "tesseract", "tesseract-langpack-ara", "poppler-utils", "p7zip"]
    return None


def fix_system() -> None:
    """Install missing system tools when that needs no password; otherwise print the one command the user
    must run (an agent shows it and asks — it never types a sudo password)."""
    missing = [t for t in ("tesseract", "pdftotext", "pdftoppm") if not shutil.which(t)]
    if shutil.which("tesseract"):
        _, langs = _run(["tesseract", "--list-langs"])
        if "ara" not in langs.split():
            missing.append("tesseract-ara")
    if not missing:
        print("[+] system tools present")
        return
    cmd = system_install_command()
    if not cmd:
        print(f"[!] install manually: Tesseract (eng + ara) and Poppler — missing: {missing}. Windows: use WSL.")
        return
    import sys
    if cmd[0] == "sudo" and _run(["sudo", "-n", "true"], timeout=5)[0] != 0 and not sys.stdin.isatty():
        print(f"[!] needs administrator rights — ask the user to run, in their own terminal:\n    {' '.join(cmd)}")
        return
    print(f"[*] {' '.join(cmd)}")
    subprocess.run(cmd, check=False)


def cmd_doctor(args) -> int:
    say = Report()
    if getattr(args, "fix", False):
        print("fix:")
        fix_system()                     # Python packages were already installed by mbset.py's bootstrap
        if getattr(args, "telegram", False):
            print("[+] Telegram downloader installed — next, the user runs `mbset.py telegram setup` once")
        print()
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
    p.add_argument("--fix", action="store_true", help="install what is missing (Python packages automatically; "
                                                      "system tools when no password is needed)")
    p.add_argument("--telegram", action="store_true", help="with --fix: also install the Telegram downloader")
    p.set_defaults(fn=cmd_doctor)
