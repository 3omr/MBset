"""`mbset.py telegram` — fetch a module's sources from Telegram posts, for anyone.

Course material is usually shared as files in Telegram channels and groups. The t.me web page is only a
preview, so files come through Telegram's client API (Telethon) with the user's own account:

    mbset.py telegram setup                     # once per person, run BY THE USER in their own terminal
    mbset.py telegram status                    # credentials saved? session logged in? (no secrets shown)
    mbset.py telegram download "$M" URL…        # posts → $M/Raw_PDF_Questions/, then `inventory`
    mbset.py telegram download "$M" --links-file links.md   # every t.me link in a text/markdown file
    mbset.py telegram scan "$M" URL… [--depth 2] [--comments]  # explore, download NOTHING → summary
    mbset.py telegram download "$M" --from-scan [--pick 1,3-7] [--skip-types video,audio]

`scan` follows a post, its album, every Telegram link in its text / hidden behind words / on its buttons
(and optionally its comments), and the posts those link to, down to --depth, never visiting a post twice.
It writes `.mbset/telegram_scan.json` + `telegram_scan.md`: a tree of where each file came from and a
numbered table (name, type, size, post, duplicates, already in Raw_PDF_Questions). The agent shows that
summary to the user and downloads only after the user says which files (`download --from-scan`).

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
    if getattr(args, "from_scan", False):
        sp = module.meta / "telegram_scan.json"
        if not sp.exists():
            raise SystemExit("[-] no scan yet: `mbset.py telegram scan \"$M\" <links>` first")
        posts = from_scan(json.loads(sp.read_text(encoding="utf-8")), args.pick, args.skip_types)
    else:
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


# ------------------------------------------------------------------------------------------- scan
KINDS = {"pdf": "pdf", "doc": "word", "docx": "word", "ppt": "slides", "pptx": "slides", "xls": "excel",
         "xlsx": "excel", "zip": "archive", "rar": "archive", "7z": "archive", "jpg": "image", "jpeg": "image",
         "png": "image", "webp": "image", "heic": "image", "mp4": "video", "mkv": "video", "mov": "video",
         "mp3": "audio", "m4a": "audio", "ogg": "audio", "oga": "audio", "txt": "text", "md": "text"}
NOT_QUESTIONS = ("video", "audio")


def kind_of(name: str, mime: str | None = None) -> str:
    ext = Path(name or "").suffix.lower().lstrip(".")
    if ext in KINDS:
        return KINDS[ext]
    mime = (mime or "").lower()
    for k in ("pdf", "image", "video", "audio"):
        if k in mime:
            return k
    return "other"


def links_in(text: str, extra: list[str] | None = None) -> list[str]:
    """Every link of a post, in order, once: the ones written in the text, plus `extra` (links hidden behind
    words — text-url entities — and on inline buttons)."""
    out: list[str] = []
    for u in re.findall(r"https?://[^\s)\]>},'\"]+", text or "") + [x for x in (extra or []) if x]:
        u = u.rstrip(".,;:!?")
        if u not in out:
            out.append(u)
    return out


def classify_link(url: str) -> tuple[str, Any]:
    """('post', [(chat, mid)…]) for a post link, else ('skip', reason) — channel/invite/outside links are only
    listed, never opened (a scan never joins anything)."""
    p = urlparse(url)
    if p.netloc.lower() not in HOSTS:
        return "skip", "outside Telegram — listed, not opened"
    parts = [x for x in p.path.split("/") if x]
    if parts and (parts[0].startswith("+") or parts[0].lower() == "joinchat"):
        return "skip", "invite link — the account would have to join; not opened"
    if parts and parts[0].lower() == "addlist":
        return "skip", "folder link — not opened"
    try:
        posts = parse_url(url)
    except ValueError:
        return "skip", "channel/profile link without a post — not opened"
    if len(posts) > 50:
        return "skip", f"range of {len(posts)} posts — download it explicitly if wanted"
    return "post", posts


async def crawl(roots: list[tuple[str, str | int, int]], fetch, depth: int = 2, max_posts: int = 300
                ) -> dict[str, Any]:
    """Breadth-first over posts. `fetch(chat, mid)` (async) returns {"chat", "mid", "text", "links", "files",
    "error"?}; files are {"name", "size", "mime", "media_id", "chat", "mid", "via"} (the post itself, its album,
    its comments). Each post is fetched once; links deeper than `depth` are listed, not opened."""
    queue: list[tuple[str | int, int, int, str | None, str]] = [(c, m, 0, None, u) for u, c, m in roots]
    seen: set[tuple[str, int]] = set()
    posts: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    unopened: list[dict[str, Any]] = []
    while queue:
        chat, mid, d, parent, url = queue.pop(0)
        key = (str(chat), int(mid))
        if key in seen:
            continue
        if len(posts) >= max_posts:
            unopened.append({"url": url, "from": parent, "reason": f"--max-posts {max_posts} reached"})
            continue
        seen.add(key)
        node = await fetch(chat, mid)
        pkey = f"{chat}/{mid}"
        post = {"key": pkey, "url": url, "depth": d, "parent": parent,
                "text": " ".join((node.get("text") or "").split())[:160], "files": 0}
        if node.get("error"):
            post["error"] = node["error"]
        posts.append(post)
        for f in node.get("files") or []:
            fk = (str(f.get("chat", chat)), int(f.get("mid", mid)), f.get("media_id") or f.get("name"))
            if any((str(x["chat"]), int(x["mid"]), x.get("media_id") or x.get("name")) == fk for x in files):
                continue                                  # an album member already reached from its sibling
            seen.add(fk[:2])
            files.append({**f, "chat": f.get("chat", chat), "mid": f.get("mid", mid), "post": pkey})
            post["files"] += 1
        for link in node.get("links") or []:
            what, val = classify_link(link)
            if what == "skip":
                unopened.append({"url": link, "from": pkey, "reason": val})
            elif d + 1 > depth:
                unopened.append({"url": link, "from": pkey, "reason": f"deeper than --depth {depth}"})
            else:
                queue += [(c, m, d + 1, pkey, link) for c, m in val]
    return {"posts": posts, "files": files, "unopened": unopened}


def summarize(result: dict[str, Any], raw_dir: Path) -> dict[str, Any]:
    """Number the files, mark kinds, duplicates (same Telegram media, or same name + size) and files already in
    Raw_PDF_Questions (same name + size)."""
    have = {(p.name.lower(), p.stat().st_size) for p in raw_dir.rglob("*") if p.is_file()} \
        if raw_dir.exists() else set()
    first: dict[Any, int] = {}
    for n, f in enumerate(result["files"], 1):
        f["n"] = n
        f["kind"] = kind_of(f.get("name") or "", f.get("mime"))
        ids = [k for k in (("m", f.get("media_id")) if f.get("media_id") else None,
                           ("ns", (f.get("name") or "").lower(), f.get("size")) if f.get("name") else None) if k]
        dup = next((first[k] for k in ids if k in first), None)
        if dup:
            f["dup_of"] = dup
        for k in ids:
            first.setdefault(k, n)
        if f.get("name") and ((f["name"].lower(), f.get("size")) in have):
            f["have"] = True
    files = result["files"]
    new = [f for f in files if not f.get("dup_of") and not f.get("have")]
    result["totals"] = {"posts": len(result["posts"]), "files": len(files),
                        "duplicates": sum(1 for f in files if f.get("dup_of")),
                        "already_have": sum(1 for f in files if f.get("have")),
                        "to_download": len(new), "to_download_bytes": sum(f.get("size") or 0 for f in new),
                        "unopened_links": len(result["unopened"])}
    return result


def _size(b: int | None) -> str:
    if not b:
        return "?"
    for unit in ("B", "KB", "MB", "GB"):
        if b < 1024 or unit == "GB":
            return f"{b:.0f} {unit}" if unit == "B" else f"{b:.1f} {unit}"
        b /= 1024
    return "?"


def render_scan(result: dict[str, Any]) -> str:
    t = result["totals"]
    out = [f"# Telegram scan — {result.get('module', '')}", "",
           f"Scanned {t['posts']} post(s): **{t['files']} file(s)** — {t['duplicates']} duplicate(s), "
           f"{t['already_have']} already in Raw_PDF_Questions → **{t['to_download']} to download "
           f"({_size(t['to_download_bytes'])})**. Nothing has been downloaded.", "", "## Where the files are", ""]
    kids: dict[Any, list[dict[str, Any]]] = {}
    for p in result["posts"]:
        kids.setdefault(p["parent"], []).append(p)
    by_post: dict[str, list[dict[str, Any]]] = {}
    for f in result["files"]:
        by_post.setdefault(f["post"], []).append(f)

    def walk(parent: Any, level: int) -> None:
        for p in kids.get(parent, []):
            nums = ", ".join(f"#{f['n']}" for f in by_post.get(p["key"], []))
            note = f" — ERROR: {p['error']}" if p.get("error") else ""
            out.append(f"{'  ' * level}- `{p['key']}` {p['text'][:80]!r}" + (f" → files {nums}" if nums else "")
                       + note)
            walk(p["key"], level + 1)
    walk(None, 0)
    out += ["", "## Files", "", "| # | file | type | size | post | note |", "|---|---|---|---|---|---|"]
    for f in result["files"]:
        notes = []
        if f.get("dup_of"):
            notes.append(f"duplicate of #{f['dup_of']}")
        if f.get("have"):
            notes.append("already in Raw_PDF_Questions")
        if f["kind"] in NOT_QUESTIONS:
            notes.append("probably not questions")
        if f.get("via") and f["via"] != "post":
            notes.append(f"from {f['via']}")
        out.append(f"| {f['n']} | {(f.get('name') or '?').replace('|', '/')} | {f['kind']} | {_size(f.get('size'))} | "
                   f"`{f['chat']}/{f['mid']}` | {'; '.join(notes)} |")
    if result["unopened"]:
        out += ["", "## Links not opened", ""]
        out += [f"- {u['url']} (in `{u['from']}`): {u['reason']}" for u in result["unopened"]]
    out += ["", "Next: ask the user which files to import, then "
            "`mbset.py telegram download \"$M\" --from-scan [--pick 1,3-7] [--skip-types video,audio]`."]
    return "\n".join(out) + "\n"


def _media_id(msg) -> Any:
    for attr in ("document", "photo"):
        obj = getattr(msg, attr, None)
        if obj is not None and getattr(obj, "id", None):
            return f"{attr}:{obj.id}"
    return None


def _file_of(msg, chat, via: str) -> dict[str, Any] | None:
    if not getattr(msg, "media", None) or not getattr(msg, "file", None):
        return None
    f = msg.file
    return {"name": f.name or f"telegram_{str(chat).lstrip('-')}_{msg.id}{f.ext or ''}", "size": f.size,
            "mime": f.mime_type, "media_id": _media_id(msg), "chat": chat, "mid": msg.id, "via": via}


def _hidden_links(msg) -> list[str]:
    urls = [getattr(e, "url", None) for e in (getattr(msg, "entities", None) or [])]
    markup = getattr(msg, "reply_markup", None)
    for row in getattr(markup, "rows", None) or []:
        for b in getattr(row, "buttons", []):          # older layers: button.url; newer: button.type.url
            urls.append(getattr(b, "url", None) or getattr(getattr(b, "type", None), "url", None))
    return [u for u in urls if u]


async def _scan(roots, depth: int, max_posts: int, comments: bool) -> dict[str, Any]:
    from telethon.errors import FloodWaitError, RPCError

    client = _client()
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        raise SystemExit("[-] Telegram session not logged in — the user runs `mbset.py telegram setup`")
    entities: dict[Any, Any] = {}

    async def call(fn, *a, **k):
        for _ in range(3):
            try:
                return await fn(*a, **k)
            except FloodWaitError as e:
                print(f"   Telegram asks to wait {e.seconds}s…")
                await asyncio.sleep(int(e.seconds) + 2)
        raise RuntimeError("Telegram kept asking to wait")

    async def fetch(chat, mid) -> dict[str, Any]:
        node: dict[str, Any] = {"chat": chat, "mid": mid, "text": "", "links": [], "files": []}
        try:
            if chat not in entities:
                entities[chat] = await call(client.get_entity, chat)
            ent = entities[chat]
            msg = await call(client.get_messages, ent, ids=mid)
            if not msg:
                node["error"] = "post not found (deleted, or not visible to this account)"
                return node
            node["text"] = msg.message or ""
            node["links"] = links_in(msg.message or "", _hidden_links(msg))
            group = [msg]
            if getattr(msg, "grouped_id", None):          # an album: its siblings sit next to it
                near = await call(client.get_messages, ent, ids=list(range(max(1, mid - 10), mid + 11)))
                group = [m for m in near if m and getattr(m, "grouped_id", None) == msg.grouped_id]
                for m in group:
                    if m.id != mid:
                        node["links"] += [u for u in links_in(m.message or "", _hidden_links(m))
                                          if u not in node["links"]]
            node["files"] = [f for f in (_file_of(m, chat, "post" if m.id == mid else "album") for m in group) if f]
            if comments and getattr(getattr(msg, "replies", None), "comments", False):
                async for c in client.iter_messages(ent, reply_to=mid, limit=200):
                    f = _file_of(c, c.chat_id, "comments")
                    if f:
                        node["files"].append(f)
                    node["links"] += [u for u in links_in(c.message or "", _hidden_links(c)) if u not in node["links"]]
        except (RPCError, ValueError, RuntimeError, TypeError) as exc:
            node["error"] = f"{type(exc).__name__}: {exc}"
        return node

    try:
        return await crawl(roots, fetch, depth=depth, max_posts=max_posts)
    finally:
        await client.disconnect()


def cmd_scan(args) -> int:
    module = Module(args.module)
    roots = collect(args.urls or [], Path(args.links_file) if args.links_file else None)
    if not roots:
        raise SystemExit("[-] no Telegram links given (URLs or --links-file)")
    result = asyncio.run(_scan(roots, args.depth, args.max_posts, args.comments))
    result = summarize(result, module.raw)
    result.update(module=module.name, at=now(), roots=args.urls or [], depth=args.depth)
    module.meta.mkdir(parents=True, exist_ok=True)
    (module.meta / "telegram_scan.json").write_text(json.dumps(result, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")
    md = render_scan(result)
    (module.meta / "telegram_scan.md").write_text(md, encoding="utf-8")
    print(md)
    print(f"[=] summary: {module.meta / 'telegram_scan.md'} — nothing downloaded; show it to the user and ask "
          f"which files to import")
    return 0


def picks(spec: str | None, total: int) -> set[int]:
    if not spec:
        return set(range(1, total + 1))
    out: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if not m:
            raise SystemExit(f"[-] --pick: not a number or range: {part!r}")
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        out |= set(range(min(a, b), max(a, b) + 1))
    return {n for n in out if 1 <= n <= total}


def from_scan(scan: dict[str, Any], pick: str | None, skip_types: str | None) -> list[tuple[str, str | int, int]]:
    """(url, chat, mid) of the chosen files: duplicates and files already in Raw_PDF_Questions left out."""
    skip = {s.strip().lower() for s in (skip_types or "").split(",") if s.strip()}
    want = picks(pick, len(scan["files"]))
    return [(f"scan #{f['n']}", f["chat"], int(f["mid"])) for f in scan["files"]
            if f["n"] in want and not f.get("dup_of") and not f.get("have") and f["kind"] not in skip]


def register(sub) -> None:
    p = sub.add_parser("telegram", help="fetch sources from Telegram posts (setup / status / scan / download)")
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
    s.add_argument("--from-scan", action="store_true", help="download the files listed by the last `scan`")
    s.add_argument("--pick", help="with --from-scan: file numbers from the summary, e.g. 1,3,5-9 (default all)")
    s.add_argument("--skip-types", help="with --from-scan: kinds to leave out, e.g. video,audio")
    s.set_defaults(fn=cmd_download)
    s = tsub.add_parser("scan", help="follow a post, its album and every Telegram link in it (to --depth) and "
                                     "summarize the files — downloads nothing")
    s.add_argument("module")
    s.add_argument("urls", nargs="*", help="t.me post links")
    s.add_argument("--links-file", help="any text/markdown file: every t.me link in it")
    s.add_argument("--depth", type=int, default=2, help="link levels to follow (default 2)")
    s.add_argument("--max-posts", type=int, default=300, help="stop after this many posts (default 300)")
    s.add_argument("--comments", action="store_true", help="also read the files/links in the post's comments")
    s.set_defaults(fn=cmd_scan)
