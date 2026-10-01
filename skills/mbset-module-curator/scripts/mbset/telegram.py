"""`mbset.py telegram` — fetch a module's sources from Telegram posts, for anyone.

Course material is usually shared as files in Telegram channels and groups. The t.me web page is only a
preview, so files come through Telegram's client API (Telethon) with the user's own account:

    mbset.py telegram setup                     # once per person, run BY THE USER in their own terminal
    mbset.py telegram status                    # credentials saved? session logged in? (no secrets shown)
    mbset.py telegram download "$M" URL…        # posts → $M/Raw_PDF_Questions/, then `inventory`
    mbset.py telegram download "$M" --links-file links.md   # every t.me link in a text/markdown file

Supported links: public posts `https://t.me/<channel>/<id>`, ranges `https://t.me/<channel>/100-140`,
and posts of private channels/groups the account has joined `https://t.me/c/<internal id>/<id>`.

Credentials and the login session live in `~/.config/mbset/` (mode 600), never in the module or the
repository. An agent never types the user's API hash, phone number, login code or 2FA password: the user
runs `setup` themselves, in their own terminal window (references/setup-guide.md).
Downloads are resumable: posts already recorded in `$M/.mbset/telegram_downloads.json` are skipped.
"""

from __future__ import annotations

import asyncio
import getpass
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .common import CONFIG_DIR as CONFIG, Module, now

ENV_FILE = CONFIG / "telegram.env"
SESSION = CONFIG / "telegram"            # Telethon adds .session
HOSTS = {"t.me", "www.t.me", "telegram.me", "www.telegram.me"}
URL_RX = re.compile(r"https?://(?:www\.)?(?:t\.me|telegram\.me)/[^\s)\]>},'\"]+", re.I)
INSTALL = "python3 -m pip install -r <skill>/scripts/requirements-telegram.txt"


# ------------------------------------------------------------------------------------------ links
def parse_url(url: str) -> list[tuple[str | int, int]]:
    """(channel username or internal id, message id) for every post a link names (ranges expand)."""
    p = urlparse(url.strip())
    if p.scheme not in ("http", "https") or p.netloc.lower() not in HOSTS:
        raise ValueError(f"not a Telegram link: {url}")
    parts = [x for x in p.path.split("/") if x]
    if parts and parts[0].lower() == "s":
        parts = parts[1:]
    if parts and parts[0].lower() == "c":               # private channel / group: t.me/c/<id>/<msg>
        if len(parts) < 3 or not parts[1].isdigit():
            raise ValueError(f"private link needs t.me/c/<id>/<post>: {url}")
        chat: str | int = int(f"-100{parts[1]}")
        post = parts[-1]
    else:
        if len(parts) < 2 or not re.fullmatch(r"[A-Za-z0-9_]{3,}", parts[0]):
            raise ValueError(f"Telegram link has no channel/post: {url}")
        chat, post = parts[0], parts[-1]
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", post)
    if not m:
        raise ValueError(f"invalid post id in {url}")
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    if b < a or b - a > 2000:
        raise ValueError(f"invalid post range in {url}")
    return [(chat, i) for i in range(a, b + 1)]


def collect(urls: list[str], links_file: Path | None) -> list[tuple[str, str | int, int]]:
    raw = list(urls)
    if links_file:
        raw += [u.rstrip(".,;:") for u in URL_RX.findall(links_file.read_text(encoding="utf-8"))]
    out: list[tuple[str, str | int, int]] = []
    seen: set[tuple[str | int, int]] = set()
    for u in raw:
        for chat, mid in parse_url(u):
            if (chat, mid) not in seen:
                seen.add((chat, mid))
                out.append((u, chat, mid))
    return out


# ------------------------------------------------------------------------------------ credentials
def _load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            k, _, v = line.partition("=")
            if k.strip() and not k.startswith("#"):
                env[k.strip()] = v.strip().strip('"')
    for k in ("TG_API_ID", "TG_API_HASH"):                 # the environment wins over the file
        alt = os.environ.get(k) or os.environ.get(k.replace("TG_", "TELEGRAM_"))
        if alt:
            env[k] = alt
    return env


def _client():
    try:
        from telethon import TelegramClient
    except ImportError:
        raise SystemExit(f"[-] Telethon is not installed: {INSTALL}")
    env = _load_env()
    if not env.get("TG_API_ID") or not env.get("TG_API_HASH"):
        raise SystemExit("[-] no Telegram API credentials — the user runs `mbset.py telegram setup` once")
    CONFIG.mkdir(parents=True, exist_ok=True)
    return TelegramClient(str(SESSION), int(env["TG_API_ID"]), env["TG_API_HASH"])


def cmd_setup(args) -> int:
    if not sys.stdin.isatty():
        raise SystemExit("[-] `telegram setup` is interactive: the user runs it in their own terminal window "
                         "(guide: references/setup-guide.md)")
    print("Telegram setup for mbset (once per person).\n"
          "1. Open https://my.telegram.org → log in → 'API development tools' → create an app (any name).\n"
          "2. Copy its api_id and api_hash here. They are saved only in " + str(ENV_FILE) + " (mode 600).\n")
    env = _load_env()
    api_id = input(f"api_id{' [keep saved]' if env.get('TG_API_ID') else ''}: ").strip() or env.get("TG_API_ID", "")
    api_hash = getpass.getpass(f"api_hash{' [keep saved]' if env.get('TG_API_HASH') else ''} (hidden): ").strip() \
        or env.get("TG_API_HASH", "")
    if not api_id.isdigit() or not re.fullmatch(r"[0-9a-f]{32}", api_hash):
        raise SystemExit("[-] api_id must be a number and api_hash 32 hex characters")
    CONFIG.mkdir(parents=True, exist_ok=True)
    os.chmod(CONFIG, 0o700)
    fd = os.open(ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"TG_API_ID={api_id}\nTG_API_HASH={api_hash}\n")
    print("\n3. Logging in: Telegram asks for your phone number and sends a code to your Telegram app "
          "(and your 2FA password if you set one).")

    async def login():
        client = _client()
        await client.start()                            # Telethon's own interactive login prompts
        try:
            return await client.get_me()
        finally:
            await client.disconnect()
    me = asyncio.run(login())
    for f in CONFIG.glob("telegram.session*"):
        os.chmod(f, 0o600)
    print(f"[+] logged in as {getattr(me, 'first_name', '') or 'your account'} — session saved in {CONFIG}")
    return 0


def cmd_status(args) -> int:
    env = _load_env()
    try:
        import telethon  # noqa: F401
        print("[+] Telethon installed")
    except ImportError:
        print(f"[-] Telethon missing: {INSTALL}")
        return 1
    if not env.get("TG_API_ID") or not env.get("TG_API_HASH"):
        print("[-] no API credentials — the user runs `mbset.py telegram setup`")
        return 1
    print(f"[+] API credentials saved ({ENV_FILE})")

    async def check() -> bool:
        client = _client()
        await client.connect()
        try:
            return await client.is_user_authorized()
        finally:
            await client.disconnect()
    ok = asyncio.run(check())
    print("[+] session logged in" if ok else "[-] session not logged in — the user runs `mbset.py telegram setup`")
    return 0 if ok else 1


# --------------------------------------------------------------------------------------- download
def _safe(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name).strip(" .") or "telegram_file"
    return name[:180]


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


async def _download(posts, out_dir: Path, manifest: dict[str, Any], save) -> tuple[int, int, int]:
    from telethon.errors import FileReferenceExpiredError, FloodWaitError, RPCError

    client = _client()
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        raise SystemExit("[-] Telegram session not logged in — the user runs `mbset.py telegram setup`")
    got = skipped = failed = 0
    entities: dict[Any, Any] = {}
    have = {r.get("sha256") for r in manifest["files"].values() if r.get("sha256")}
    try:
        for url, chat, mid in posts:
            key = f"{chat}/{mid}"
            if manifest["files"].get(key, {}).get("status") in ("downloaded", "duplicate", "no_media"):
                skipped += 1
                continue
            rec: dict[str, Any] = {"url": url, "at": now()}
            try:
                if chat not in entities:
                    entities[chat] = await client.get_entity(chat)
                msg = await client.get_messages(entities[chat], ids=mid)
                if not msg or not msg.media or not getattr(msg, "file", None):
                    rec["status"] = "no_media"
                    manifest["files"][key] = rec
                    continue
                name = msg.file.name or f"telegram_{str(chat).lstrip('-')}_{mid}{msg.file.ext or ''}"
                target = out_dir / _safe(name)
                n = 1
                while target.exists():
                    target = target.with_name(f"{Path(_safe(name)).stem} ({n}){target.suffix}")
                    n += 1
                part = target.with_name(target.name + ".part")
                for _ in range(3):
                    try:
                        await client.download_media(msg, file=str(part))
                        break
                    except FileReferenceExpiredError:
                        msg = await client.get_messages(entities[chat], ids=mid)
                    except FloodWaitError as e:
                        print(f"   Telegram asks to wait {e.seconds}s…")
                        await asyncio.sleep(int(e.seconds) + 2)
                else:
                    raise RuntimeError("download retries exhausted")
                digest = _sha(part)
                if digest in have:                      # the same file posted twice: keep one copy
                    part.unlink()
                    rec.update(status="duplicate", sha256=digest)
                else:
                    part.replace(target)
                    have.add(digest)
                    rec.update(status="downloaded", path=str(target.relative_to(out_dir.parent)),
                               sha256=digest, size=target.stat().st_size)
                    got += 1
                    print(f"[+] {key} → {target.name}")
            except (OSError, RuntimeError, ValueError, RPCError) as exc:
                rec.update(status="error", error=f"{type(exc).__name__}: {exc}")
                failed += 1
                print(f"[-] {key}: {rec['error']}", file=sys.stderr)
            manifest["files"][key] = rec
            save()
    finally:
        await client.disconnect()
    return got, skipped, failed


def cmd_download(args) -> int:
    module = Module(args.module)
    posts = collect(args.urls or [], Path(args.links_file) if args.links_file else None)
    posts = posts[args.offset:]
    if args.limit:
        posts = posts[:args.limit]
    if not posts:
        raise SystemExit("[-] no Telegram links given (URLs or --links-file)")
    print(f"[*] {len(posts)} post(s) → {module.raw}")
    if args.dry_run:
        for url, chat, mid in posts:
            print(f"    {chat}/{mid}  ({url})")
        return 0
    module.raw.mkdir(parents=True, exist_ok=True)
    mpath = module.meta / "telegram_downloads.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {"files": {}}

    def save() -> None:
        mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    got, skipped, failed = asyncio.run(_download(posts, module.raw, manifest, save))
    save()
    print(f"[=] {got} downloaded, {skipped} already done, {failed} failed — manifest {mpath}")
    if got:
        print(f'[=] next: mbset.py inventory "{module.root}"')
    return 0 if not failed else 2


def register(sub) -> None:
    p = sub.add_parser("telegram", help="fetch sources from Telegram posts (setup / status / download)")
    tsub = p.add_subparsers(dest="tcmd", required=True)
    s = tsub.add_parser("setup", help="once per person, run by the user: API credentials + login")
    s.set_defaults(fn=cmd_setup)
    s = tsub.add_parser("status", help="credentials saved / session logged in (no secrets shown)")
    s.set_defaults(fn=cmd_status)
    s = tsub.add_parser("download", help="download post files into <Module>/Raw_PDF_Questions")
    s.add_argument("module")
    s.add_argument("urls", nargs="*", help="t.me links (public, t.me/c/… private, or ranges …/100-140)")
    s.add_argument("--links-file", help="any text/markdown file: every t.me link in it, in order")
    s.add_argument("--offset", type=int, default=0)
    s.add_argument("--limit", type=int)
    s.add_argument("--dry-run", action="store_true", help="list the posts without logging in")
    s.set_defaults(fn=cmd_download)
