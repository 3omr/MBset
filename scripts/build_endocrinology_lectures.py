#!/usr/bin/env python3
"""Build Endocrinology lecture PDFs with an explicit source priority.

Priority for every official subcategory:

1. A manually audited page range from the local book.
2. A matching file already downloaded from Telegram.
3. A qualifying DocReader Telegram link, downloaded automatically when
   ``--download-missing`` is supplied.
4. No source (the lecture is left absent and recorded as ``missing``).

The book ranges are deliberately explicit.  This prevents a fuzzy title match
from silently assigning the wrong book pages to a lecture.  Add a range only
after checking the section boundary in the scanned book.

Examples
--------
Build the first ten source-order lectures from the current book and Downloads::

    python3 scripts/build_endocrinology_lectures.py \
      --module-root 'أزهر دمياط/Endocrinology' \
      --max-order 11

Build all available lectures and download missing DocReader fallbacks::

    python3 scripts/build_endocrinology_lectures.py \
      --module-root 'أزهر دمياط/Endocrinology' \
      --download-missing \
      --env-file /home/omar/Documents/antigravity/wise-nobel/.env
"""

from __future__ import annotations

import argparse
import asyncio
import fnmatch
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# These are the only book ranges currently trusted for this scanned source.
# Page numbers are 1-based PDF pages.
BOOK_RANGES: dict[int, tuple[int, int]] = {
    2: (31, 32),   # Hashimoto / thyroiditis section
    3: (19, 26),   # Hyperthyroidism / thyrotoxicosis
    4: (27, 30),   # Hypothyroidism
    5: (37, 40),   # Hyperparathyroidism
    6: (41, 42),   # Hypoparathyroidism
    18: (7, 15),   # Delayed and precocious puberty
    20: (3, 6),    # Hirsutism / CAH
    23: (43, 44),  # Diabetes and glucose homeostasis
    24: (45, 54),  # Different types of diabetes
    39: (35, 36),  # Calcium homeostasis
    44: (56, 64),  # Diabetes pharmacotherapy
}


# Qualifying links from College_data_links.md.  Record/video links are not
# included.  Empty entries are intentional: they remain missing if the book
# has no audited range either.
TELEGRAM_LINKS: dict[int, list[str]] = {
    1: ["https://t.me/DocReader_Guide_4_Data/1767"],
    2: ["https://t.me/DocReader_Guide_4_Data/1762"],
    3: [],
    4: ["https://t.me/DocReader_Guide_4_Data/1785"],
    5: ["https://t.me/DocReader_Guide_4_Data/1786"],
    6: ["https://t.me/DocReader_Guide_4_Data/1787"],
    7: ["https://t.me/DocReader_Guide_4_Data/1796"],
    8: ["https://t.me/DocReader_Guide_4_Data/1800"],
    9: ["https://t.me/DocReader_Guide_4_Data/1802"],
    10: ["https://t.me/DocReader_Guide_4_Data/1813"],
    11: ["https://t.me/DocReader_Guide_4_Data/1840"],
    12: [],
    13: [
        "https://t.me/DocReader_Guide_4_Data/1893",
        "https://t.me/DocReader_Guide_4_Data/1894",
    ],
    14: ["https://t.me/DocReader_Guide_4_Data/1841"],
    15: ["https://t.me/DocReader_Guide_4_Data/1842"],
    16: ["https://t.me/DocReader_Guide_4_Data/1834"],
    17: ["https://t.me/DocReader_Guide_4_Data/1833"],
    18: ["https://t.me/DocReader_Guide_4_Data/1864"],
    19: [
        "https://t.me/DocReader_Guide_4_Data/1843",
        "https://t.me/DocReader_Guide_4_Data/1844",
    ],
    20: [
        "https://t.me/DocReader_Guide_4_Data/1875",
        "https://t.me/DocReader_Guide_4_Data/1876",
    ],
    21: ["https://t.me/DocReader_Guide_4_Data/419?single"],
    22: ["https://t.me/DocReader_Guide_4_Data/1871"],
    23: [],
    24: ["https://t.me/DocReader_Guide_4_Data/429?single"],
    25: [],
    26: ["https://t.me/DocReader_Guide_4_Data/1862"],
    27: [],
    28: ["https://t.me/DocReader_Guide_4_Data/1867"],
    29: ["https://t.me/DocReader_Guide_4_Data/1925"],
    30: [],
    31: [],
    32: [],
    33: [],
    34: ["https://t.me/DocReader_Guide_4_Data/323?single"],
    35: [],
    36: [],
    37: [],
    38: [],
    39: ["https://t.me/DocReader_Guide_4_Data/1780"],
    40: [],
    41: ["https://t.me/DocReader_Guide_4_Data/1764"],
    42: [],
    44: [],
    45: ["https://t.me/DocReader_Guide_4_Data/1901"],
    46: ["https://t.me/DocReader_Guide_4_Data/1903"],
}


# Telegram Desktop does not preserve the DocReader post id in the filename.
# These aliases handle the first downloaded batch, including the common typos.
LOCAL_PATTERNS: dict[int, list[str]] = {
    1: ["*intro to endocrinology*.pdf", "*تفريغ*intro*.pdf"],
    7: ["*bonevdiseseses*.pptx", "*bone*mineral*.pptx"],
    8: ["*adrenal hypersecretion*.pptx"],
    9: ["*endocrine htn*.pptx"],
    10: ["*cushing*.pptx"],
    11: ["*adrenal hypofunction*.pptx"],
}


@dataclass
class LectureResult:
    order_index: int
    subcategory_id: str
    name: str
    status: str
    source: str | None = None
    source_files: list[str] | None = None
    page_range: list[int] | None = None
    telegram_urls: list[str] | None = None
    output: str | None = None
    note: str | None = None


def load_rows(export_path: Path) -> list[dict[str, Any]]:
    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError("openpyxl is required to read the official export") from exc

    workbook = load_workbook(export_path, read_only=True, data_only=True)
    try:
        sheet = workbook["Subcategories"]
        headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
        rows = [dict(zip(headers, row)) for row in sheet.iter_rows(min_row=2, values_only=True)]
    finally:
        workbook.close()
    return sorted(rows, key=lambda row: int(row["orderIndex"]))


def find_export(module_root: Path) -> Path:
    exports = sorted(module_root.glob("subcategories_Endocrinology_*.xlsx"))
    if not exports:
        raise FileNotFoundError(f"official Endocrinology export not found under {module_root}")
    return exports[-1]


def find_book(module_root: Path, explicit: Path | None) -> Path | None:
    if explicit:
        book_path = explicit.expanduser().resolve()
        if not book_path.exists():
            raise FileNotFoundError(book_path)
        return book_path
    books = sorted((module_root / "Book").glob("*.pdf"))
    return books[0] if len(books) == 1 else None


def find_local_files(download_dir: Path, order_index: int) -> list[Path]:
    patterns = LOCAL_PATTERNS.get(order_index, [])
    if not patterns or not download_dir.exists():
        return []
    files = [path for path in download_dir.iterdir() if path.is_file() and not path.name.endswith(".part")]
    for pattern in patterns:
        matches = sorted(
            [path for path in files if fnmatch.fnmatch(path.name.casefold(), pattern.casefold())],
            key=lambda path: (path.stat().st_mtime, path.name),
            reverse=True,
        )
        if matches:
            return matches[:1]
    return []


def convert_to_pdf(source: Path, workdir: Path) -> Path:
    if source.suffix.casefold() == ".pdf":
        return source
    conversion = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(workdir),
            str(source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    converted = workdir / f"{source.stem}.pdf"
    if conversion.returncode != 0 or not converted.exists():
        detail = (conversion.stderr or conversion.stdout).strip()
        raise RuntimeError(f"LibreOffice could not convert {source.name}: {detail}")
    return converted


def merge_pdfs(inputs: list[Path], output: Path) -> None:
    try:
        import pymupdf as fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required to create lecture PDFs") from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".part")
    if temporary.exists():
        temporary.unlink()
    destination = fitz.open()
    try:
        for path in inputs:
            source = fitz.open(path)
            try:
                destination.insert_pdf(source)
            finally:
                source.close()
        destination.save(temporary)
    finally:
        destination.close()
    temporary.replace(output)


def extract_book_range(book: Path, start: int, end: int, output: Path) -> None:
    try:
        import pymupdf as fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required to extract book pages") from exc

    source = fitz.open(book)
    try:
        if start < 1 or end < start or end > source.page_count:
            raise ValueError(f"book page range {start}-{end} is outside 1-{source.page_count}")
        destination = fitz.open()
        try:
            destination.insert_pdf(source, from_page=start - 1, to_page=end - 1)
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = output.with_name(output.name + ".part")
            if temporary.exists():
                temporary.unlink()
            destination.save(temporary)
        finally:
            destination.close()
    finally:
        source.close()
    temporary.replace(output)


def resolve_env(env_file: Path | None) -> None:
    if not env_file:
        return
    try:
        from dotenv import load_dotenv
    except ImportError as exc:
        raise RuntimeError("python-dotenv is required when --env-file is used") from exc
    if not env_file.exists():
        raise FileNotFoundError(env_file)
    load_dotenv(env_file.expanduser(), override=False)


def download_fallbacks(
    links: list[str],
    download_dir: Path,
    session: Path,
    api_id: int,
    api_hash: str,
) -> dict[str, Path]:
    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    from download_telegram_files import TelegramLink, download_links

    selected = [TelegramLink(label="DocReader fallback", url=url) for url in links]
    records = asyncio.run(
        download_links(
            selected,
            out_dir=download_dir,
            session=session,
            api_id=api_id,
            api_hash=api_hash,
            overwrite=False,
            non_interactive=False,
        )
    )
    return {
        record.url: Path(record.path)
        for record in records
        if record.status == "downloaded" and record.path
    }


def build(args: argparse.Namespace) -> list[LectureResult]:
    module_root = args.module_root.expanduser().resolve()
    export_path = args.export or find_export(module_root)
    book = find_book(module_root, args.book)
    download_dir = args.download_dir.expanduser().resolve()
    lecture_dir = module_root / "Lectures"
    lecture_dir.mkdir(parents=True, exist_ok=True)
    rows = load_rows(export_path)
    if args.max_order is not None:
        rows = [row for row in rows if int(row["orderIndex"]) <= args.max_order * 10]

    # Identify all fallback files already present before downloading anything.
    local_inputs = {
        int(row["orderIndex"]) // 10: find_local_files(download_dir, int(row["orderIndex"]) // 10)
        for row in rows
    }
    missing_links: list[str] = []
    for row in rows:
        order = int(row["orderIndex"]) // 10
        book_available = book is not None and order in BOOK_RANGES
        if not book_available and not local_inputs[order]:
            missing_links.extend(TELEGRAM_LINKS.get(order, []))
    missing_links = list(dict.fromkeys(missing_links))

    downloaded_by_url: dict[str, Path] = {}
    if args.download_missing and missing_links:
        api_id_raw = args.api_id or os.environ.get("TG_API_ID") or os.environ.get("TELEGRAM_API_ID")
        api_hash = args.api_hash or os.environ.get("TG_API_HASH") or os.environ.get("TELEGRAM_API_HASH")
        if api_id_raw and api_hash:
            downloaded_by_url = download_fallbacks(
                missing_links,
                download_dir,
                args.session.expanduser().resolve(),
                int(api_id_raw),
                api_hash,
            )
        else:
            print("[INFO] No Telegram credentials; fallback links will remain missing.")

    results: list[LectureResult] = []
    temp_kwargs: dict[str, Any] = {"prefix": "mbset_endo_"}
    scratch_dir = module_root / "scratch"
    if scratch_dir.exists():
        temp_kwargs["dir"] = str(scratch_dir)
    with tempfile.TemporaryDirectory(**temp_kwargs) as temporary_directory:
        temp_dir = Path(temporary_directory)
        for row in rows:
            order = int(row["orderIndex"]) // 10
            name = str(row["name"])
            subcategory_id = str(row["subcategoryId"])
            output = lecture_dir / f"{subcategory_id}.pdf"

            # 1) Book is always authoritative when an audited range exists.
            if book and order in BOOK_RANGES:
                start, end = BOOK_RANGES[order]
                if not args.dry_run:
                    extract_book_range(book, start, end, output)
                result = LectureResult(
                    order_index=order,
                    subcategory_id=subcategory_id,
                    name=name,
                    status="ready",
                    source="book",
                    page_range=[start, end],
                    output=str(output),
                )
                print(f"[BOOK] {order:02d} {name} -> pages {start}-{end}")
                results.append(result)
                continue

            # 2) A file already downloaded by Telegram Desktop is next.
            inputs = local_inputs.get(order, [])
            source = "local_download"
            if not inputs:
                inputs = [downloaded_by_url[url] for url in TELEGRAM_LINKS.get(order, []) if url in downloaded_by_url]
                if inputs:
                    source = "docreader_download"

            if inputs:
                if not args.dry_run:
                    converted = [convert_to_pdf(path, temp_dir) for path in inputs]
                    merge_pdfs(converted, output)
                result = LectureResult(
                    order_index=order,
                    subcategory_id=subcategory_id,
                    name=name,
                    status="ready",
                    source=source,
                    source_files=[str(path) for path in inputs],
                    telegram_urls=TELEGRAM_LINKS.get(order) or None,
                    output=str(output),
                )
                print(f"[{source.upper()}] {order:02d} {name} -> {', '.join(path.name for path in inputs)}")
                results.append(result)
                continue

            # 3) No book range and no usable fallback.
            urls = TELEGRAM_LINKS.get(order, [])
            note = "no audited book range and no local/downloaded qualifying source"
            if urls and not args.download_missing:
                note += "; rerun with --download-missing to fetch DocReader"
            results.append(
                LectureResult(
                    order_index=order,
                    subcategory_id=subcategory_id,
                    name=name,
                    status="missing",
                    telegram_urls=urls or None,
                    note=note,
                )
            )
            print(f"[MISSING] {order:02d} {name}")

    manifest = module_root / "lecture_source_manifest.json"
    if not args.dry_run:
        manifest.write_text(
            json.dumps(
                {
                    "generatedAt": datetime.now(timezone.utc).isoformat(),
                    "export": str(export_path),
                    "book": str(book) if book else None,
                    "priority": ["book", "local_download", "docreader_download", "missing"],
                    "lectures": [asdict(result) for result in results],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Manifest: {manifest}")
    return results


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--module-root", type=Path, required=True)
    p.add_argument("--export", type=Path, help="official subcategories export")
    p.add_argument("--book", type=Path, help="book PDF; auto-detected when Book contains one PDF")
    p.add_argument(
        "--download-dir",
        type=Path,
        default=Path.home() / "Downloads" / "Telegram Desktop",
    )
    p.add_argument("--session", type=Path, default=Path.home() / ".config" / "mbset" / "telegram_download_session")
    p.add_argument("--env-file", type=Path)
    p.add_argument("--api-id", type=int)
    p.add_argument("--api-hash")
    p.add_argument("--download-missing", action="store_true")
    p.add_argument("--max-order", type=int, help="process only source-order lectures up to this number")
    p.add_argument("--dry-run", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        resolve_env(args.env_file)
        results = build(args)
        ready = sum(result.status == "ready" for result in results)
        missing = sum(result.status == "missing" for result in results)
        print(f"Finished: {ready} ready, {missing} missing")
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
