#!/usr/bin/env python3
"""Download files from public Telegram post links.

The public t.me web page is only a preview; the file itself is delivered by
Telegram's client API.  This script uses Telethon, asks for a one-time Telegram
login on the first run, and then reuses the local session on later runs.

Examples
--------
Download the first ten links from the Endocrinology link report::

    python3 scripts/download_telegram_files.py \
      --links-file 'أزهر دمياط/Endocrinology/College_data_links.md' \
      --limit 10

Download one or more links directly::

    python3 scripts/download_telegram_files.py \
      https://t.me/DocReader_Guide_4_Data/1762

Credentials are read from TG_API_ID/TG_API_HASH (the same names used by the
existing wise-nobel recovery script) or TELEGRAM_API_ID/TELEGRAM_API_HASH.  The first
non-dry run also asks Telegram for the phone number, login code, and 2FA
password if the saved session is not authorized.  The session is stored under
~/.config/mbset and is never written into the repository.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
except ImportError:  # dry-run mode does not need python-dotenv
    load_dotenv = None


TELEGRAM_HOSTS = {"t.me", "www.t.me", "telegram.me", "www.telegram.me"}
TELEGRAM_URL_RE = re.compile(
    r"https?://(?:t\.me|telegram\.me)/[^\s)\]>},]+",
    re.IGNORECASE,
)
LINK_LINE_RE = re.compile(
    r"^\s*\d+\.\s+\*\*(?P<label>.+?)\*\*:\s+\[[^\]]+\]\((?P<url>https?://[^)]+)\)"
)


@dataclass(frozen=True)
class TelegramLink:
    label: str
    url: str


@dataclass
class DownloadRecord:
    url: str
    label: str
    channel: str
    message_id: int
    status: str
    path: str | None = None
    error: str | None = None
    sha256: str | None = None
    size: int | None = None


def parse_post_url(url: str) -> tuple[str, int]:
    """Return (public channel username, message id) from a Telegram URL."""

    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in TELEGRAM_HOSTS:
        raise ValueError(f"not a supported public Telegram URL: {url}")

    parts = [part for part in parsed.path.split("/") if part]
    if parts and parts[0].lower() == "s":
        parts = parts[1:]
    if len(parts) < 2:
        raise ValueError(f"Telegram URL has no post id: {url}")

    channel = parts[0]
    if channel.lower() == "c":
        raise ValueError("private/internal /c/ Telegram links are not supported; use a public t.me link")
    if not re.fullmatch(r"[A-Za-z0-9_]{3,}", channel):
        raise ValueError(f"invalid public Telegram channel name: {channel}")
    try:
        message_id = int(parts[1])
    except ValueError as exc:
        raise ValueError(f"invalid Telegram post id in {url}") from exc
    if message_id <= 0:
        raise ValueError(f"invalid Telegram post id in {url}")
    return channel, message_id


def extract_links(markdown_path: Path) -> list[TelegramLink]:
    """Extract the ordered Telegram links from a Markdown report.

    The preferred format is the numbered bold list produced by
    College_data_links.md.  A URL-only fallback keeps the script useful for a
    plain text file or a copied Telegram link list.
    """

    text = markdown_path.read_text(encoding="utf-8")
    found: list[TelegramLink] = []
    seen: set[str] = set()

    for line in text.splitlines():
        match = LINK_LINE_RE.match(line)
        if not match:
            continue
        url = match.group("url").strip()
        if url not in seen:
            found.append(TelegramLink(label=match.group("label").strip(), url=url))
            seen.add(url)

    if found:
        return found

    for index, raw_url in enumerate(TELEGRAM_URL_RE.findall(text), start=1):
        url = raw_url.rstrip(".,;:")
        if url in seen:
            continue
        channel, message_id = parse_post_url(url)
        found.append(TelegramLink(label=f"{channel}/{message_id} ({index})", url=url))
        seen.add(url)
    return found


def clean_filename(name: str) -> str:
    """Make a Telegram-provided filename safe for a single output directory."""

    name = Path(name).name.strip()
    name = re.sub(r"[\x00-\x1f<>:\"/\\|?*]", "_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name or "telegram_file.bin"


def unique_target(path: Path, overwrite: bool) -> Path:
    if overwrite or not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for number in range(2, 10_000):
        candidate = path.with_name(f"{stem} ({number}){suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not find a free filename for {path.name}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_bytes(value: int | None) -> str:
    if not value:
        return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    number = float(value)
    for unit in units:
        if number < 1024 or unit == units[-1]:
            return f"{number:.1f} {unit}" if unit != "B" else f"{int(number)} B"
        number /= 1024
    return f"{value} B"


class DownloadProgress:
    """Small progress bar patterned after the existing wise-nobel script."""

    def __init__(self, filename: str, expected_size: int | None):
        self.filename = filename
        self.expected_size = expected_size or 0
        self.started = time.time()
        self.last_update = 0.0

    def callback(self, current: int, total: int) -> None:
        now = time.time()
        if now - self.last_update < 0.25 and current < total:
            return
        self.last_update = now
        total = total or self.expected_size
        ratio = current / total if total else 0
        elapsed = max(now - self.started, 0.001)
        speed = current / elapsed
        bar_len = 24
        filled = int(bar_len * ratio)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(
            f"\r   [{bar}] {ratio * 100:5.1f}% | "
            f"{format_bytes(current)}/{format_bytes(total)} | {format_bytes(int(speed))}/s",
            end="",
            flush=True,
        )


def media_size(message: object) -> int | None:
    file_info = getattr(message, "file", None)
    size = getattr(file_info, "size", None)
    return int(size) if size else None


def write_manifest(path: Path, records: list[DownloadRecord]) -> None:
    path.write_text(
        json.dumps(
            {
                "updatedAt": datetime.now(timezone.utc).isoformat(),
                "records": [asdict(record) for record in records],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", help="public t.me post URLs")
    parser.add_argument(
        "--links-file",
        type=Path,
        help="Markdown/text file containing Telegram links, in report order",
    )
    parser.add_argument("--offset", type=int, default=0, help="skip this many links from --links-file")
    parser.add_argument("--limit", type=int, help="download at most this many links")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path.home() / "Downloads" / "Telegram Desktop",
        help="destination directory (default: ~/Downloads/Telegram Desktop)",
    )
    parser.add_argument(
        "--session",
        type=Path,
        default=None,
        help="Telethon session path; keep this outside the repository",
    )
    parser.add_argument(
        "--session-name",
        default="telegram_download_session",
        help="session filename when --session is omitted",
    )
    parser.add_argument("--env-file", type=Path, help="optional .env file (supports TG_API_ID/TG_API_HASH)")
    parser.add_argument("--api-id", type=int, help="Telegram API ID; env: TG_API_ID or TELEGRAM_API_ID")
    parser.add_argument("--api-hash", help="Telegram API hash; env: TG_API_HASH or TELEGRAM_API_HASH")
    parser.add_argument(
        "--manifest",
        type=Path,
        help="JSON manifest path (default: <out-dir>/mbset_telegram_downloads.json)",
    )
    parser.add_argument("--overwrite", action="store_true", help="overwrite an existing destination filename")
    parser.add_argument("--dry-run", action="store_true", help="validate and print links without logging into Telegram")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="fail instead of prompting for first-time Telegram authorization",
    )
    return parser


def select_links(args: argparse.Namespace) -> list[TelegramLink]:
    links: list[TelegramLink] = []
    if args.links_file:
        if not args.links_file.exists():
            raise FileNotFoundError(args.links_file)
        links.extend(extract_links(args.links_file))
    links.extend(TelegramLink(label="direct", url=url) for url in args.urls)

    unique: list[TelegramLink] = []
    seen: set[str] = set()
    for link in links:
        if link.url in seen:
            continue
        parse_post_url(link.url)
        unique.append(link)
        seen.add(link.url)

    selected = unique[args.offset :]
    if args.limit is not None:
        if args.limit < 1:
            raise ValueError("--limit must be positive")
        selected = selected[: args.limit]
    if not selected:
        raise ValueError("no Telegram links selected")
    return selected


async def download_links(
    links: list[TelegramLink],
    *,
    out_dir: Path,
    session: Path,
    api_id: int,
    api_hash: str,
    overwrite: bool,
    non_interactive: bool,
) -> list[DownloadRecord]:
    try:
        from telethon import TelegramClient
        from telethon.errors import FileReferenceExpiredError, FloodWaitError, RPCError
    except ImportError as exc:
        raise RuntimeError(
            "Telethon is not installed. Run: python3 -m pip install -r requirements-telegram.txt"
        ) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    session.parent.mkdir(parents=True, exist_ok=True)
    client = TelegramClient(str(session), api_id, api_hash)
    records: list[DownloadRecord] = []

    await client.connect()
    try:
        if not await client.is_user_authorized():
            if non_interactive:
                raise RuntimeError("Telegram session is not authorized; run once without --non-interactive")
            await client.start()

        entity_cache: dict[str, object] = {}
        for link in links:
            channel, message_id = parse_post_url(link.url)
            record = DownloadRecord(
                url=link.url,
                label=link.label,
                channel=channel,
                message_id=message_id,
                status="pending",
            )
            records.append(record)
            try:
                entity = entity_cache.get(channel)
                if entity is None:
                    entity = await client.get_entity(channel)
                    entity_cache[channel] = entity
                message = await client.get_messages(entity, ids=message_id)
                if not message or not message.media:
                    raise RuntimeError("post has no downloadable media")

                telegram_name = getattr(getattr(message, "file", None), "name", None)
                if not telegram_name:
                    extension = getattr(getattr(message, "file", None), "ext", "") or ".bin"
                    telegram_name = f"telegram_{channel}_{message_id}{extension}"
                target = unique_target(out_dir / clean_filename(telegram_name), overwrite)
                if target.exists() and overwrite:
                    target.unlink()
                part = target.with_name(target.name + ".part")
                if part.exists():
                    part.unlink()

                # File references can expire while a large file is downloading.
                # Re-fetch the message and retry, just as wise-nobel does.
                for attempt in range(1, 4):
                    try:
                        progress = DownloadProgress(target.name, media_size(message))
                        downloaded = await client.download_media(
                            message,
                            file=str(part),
                            progress_callback=progress.callback,
                        )
                        print()
                        if not downloaded or not part.exists():
                            raise RuntimeError("Telegram returned no file")
                        break
                    except FileReferenceExpiredError:
                        print("   File reference expired; refreshing message...")
                        message = await client.get_messages(entity, ids=message_id)
                    except FloodWaitError as exc:
                        wait_seconds = int(exc.seconds) + 2
                        print(f"   Telegram FloodWait; sleeping {wait_seconds}s...")
                        await asyncio.sleep(wait_seconds)
                    except (OSError, RuntimeError, RPCError):
                        if part.exists():
                            part.unlink()
                        raise
                else:
                    raise RuntimeError("download retries exhausted")
                part.replace(target)

                record.status = "downloaded"
                record.path = str(target)
                record.size = target.stat().st_size
                record.sha256 = sha256_file(target)
                print(f"[OK] {link.label} -> {target}")
            except (OSError, RuntimeError, ValueError, RPCError) as exc:  # keep the batch moving
                record.status = "error"
                record.error = f"{type(exc).__name__}: {exc}"
                print(f"[ERROR] {link.url}: {record.error}", file=sys.stderr)
    finally:
        await client.disconnect()
    return records


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.env_file:
            if load_dotenv is None:
                raise RuntimeError("python-dotenv is required when --env-file is used")
            if not args.env_file.exists():
                raise FileNotFoundError(args.env_file)
            load_dotenv(args.env_file.expanduser(), override=False)
        links = select_links(args)
        print(f"Selected {len(links)} Telegram link(s):")
        for index, link in enumerate(links, start=1):
            channel, message_id = parse_post_url(link.url)
            print(f"  {index:02d}. {link.label} -> @{channel}/{message_id}")
        if args.dry_run:
            return 0

        api_id_raw = (
            args.api_id
            or os.environ.get("TG_API_ID")
            or os.environ.get("TELEGRAM_API_ID")
        )
        api_hash = (
            args.api_hash
            or os.environ.get("TG_API_HASH")
            or os.environ.get("TELEGRAM_API_HASH")
        )
        if not api_id_raw or not api_hash:
            raise RuntimeError(
                "set TG_API_ID and TG_API_HASH (or pass --api-id/--api-hash)"
            )
        try:
            api_id = int(api_id_raw)
        except ValueError as exc:
            raise RuntimeError("TELEGRAM_API_ID must be an integer") from exc

        session_path = args.session or (
            Path.home() / ".config" / "mbset" / args.session_name
        )
        records = asyncio.run(
            download_links(
                links,
                out_dir=args.out_dir.expanduser().resolve(),
                session=session_path.expanduser().resolve(),
                api_id=api_id,
                api_hash=api_hash,
                overwrite=args.overwrite,
                non_interactive=args.non_interactive,
            )
        )
        manifest = args.manifest or (args.out_dir / "mbset_telegram_downloads.json")
        manifest = manifest.expanduser().resolve()
        manifest.parent.mkdir(parents=True, exist_ok=True)
        write_manifest(manifest, records)
        ok = sum(record.status == "downloaded" for record in records)
        failed = len(records) - ok
        print(f"Finished: {ok} downloaded, {failed} failed")
        print(f"Manifest: {manifest}")
        return 0 if failed == 0 else 2
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
