#!/usr/bin/env python3
"""Create searchable OCR copies and text sidecars for an MBset module.

Original sources are never overwritten.  PDFs are copied through OCRmyPDF into
``OCR_PDF/<group>/`` and their reading-order text is written to
``OCR_Text/<group>/``.  Files with a healthy native text layer keep that layer;
image-only or unusable PDFs are force-OCRed page by page by OCRmyPDF.

The output manifest is the gate for the next extraction stage.  A source is
``ok`` only when its searchable PDF/text sidecar was produced and contains
text; failures stay visible instead of being silently skipped.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class OcrRecord:
    group: str
    source: str
    source_path: str
    searchable_pdf: str | None
    text_path: str | None
    pages: int | None
    method: str
    text_chars: int
    status: str
    error: str | None = None


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def pdf_page_count(path: Path) -> int:
    probe = run_command(["pdfinfo", str(path)])
    if probe.returncode != 0:
        raise RuntimeError(probe.stderr.strip() or "pdfinfo failed")
    for line in probe.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("pdfinfo did not report a page count")


def native_probe(path: Path, pages: int) -> str:
    end_page = min(pages, 2)
    probe = run_command(["pdftotext", "-layout", "-f", "1", "-l", str(end_page), str(path), "-"])
    if probe.returncode != 0:
        return ""
    return re.sub(r"\s+", "", probe.stdout)


def safe_stem(path: Path) -> str:
    stem = path.stem.strip()
    return re.sub(r"[\\/:*?\"<>|]", "_", stem) or "source"


def searchable_copy(source: Path, destination: Path, force_ocr: bool, jobs: int, fast: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    if temporary.exists():
        temporary.unlink()
    command = ["ocrmypdf", "--output-type", "pdf"]
    if fast:
        command.extend(["--oversample", "200"])
    else:
        command.extend(["--deskew", "--rotate-pages"])
    command.extend(["--jobs", str(jobs), "-l", "eng"])
    command.append("--force-ocr" if force_ocr else "--skip-text")
    command.extend([str(source), str(temporary)])
    result = run_command(command)
    if result.returncode != 0 or not temporary.exists():
        temporary.unlink(missing_ok=True)
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(detail[-2000:] or "ocrmypdf failed")
    temporary.replace(destination)


def text_from_pdf(path: Path) -> str:
    result = run_command(["pdftotext", "-layout", str(path), "-"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "pdftotext failed")
    return result.stdout


def text_from_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("python-docx is required for DOCX sources") from exc
    document = Document(path)
    blocks = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables:
        for row in table.rows:
            blocks.append("\t".join(cell.text for cell in row.cells))
    return "\n".join(blocks) + "\n"


def process_pdf(source: Path, group: str, pdf_root: Path, text_root: Path, jobs: int, fast: bool) -> OcrRecord:
    pages = pdf_page_count(source)
    usable_native_text = len(native_probe(source, pages)) >= 100
    method = "native-text+OCR-copy" if usable_native_text else "force-ocr"
    searchable = pdf_root / group / f"{safe_stem(source)}.pdf"
    text_path = text_root / group / f"{safe_stem(source)}.txt"
    if searchable.exists() and text_path.exists():
        text = text_path.read_text(encoding="utf-8")
        return OcrRecord(
            group=group,
            source=source.name,
            source_path=str(source),
            searchable_pdf=str(searchable),
            text_path=str(text_path),
            pages=pdf_page_count(searchable),
            method="existing-ocr",
            text_chars=len(re.sub(r"\s+", "", text)),
            status="ok",
        )
    searchable_copy(source, searchable, force_ocr=not usable_native_text, jobs=jobs, fast=fast)
    text = text_from_pdf(searchable)
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(text, encoding="utf-8")
    chars = len(re.sub(r"\s+", "", text))
    if chars < 20:
        raise RuntimeError("OCR completed but produced fewer than 20 non-space characters")
    return OcrRecord(
        group=group,
        source=source.name,
        source_path=str(source),
        searchable_pdf=str(searchable),
        text_path=str(text_path),
        pages=pages,
        method=method,
        text_chars=chars,
        status="ok",
    )


def process_docx(source: Path, group: str, text_root: Path) -> OcrRecord:
    text = text_from_docx(source)
    text_path = text_root / group / f"{safe_stem(source)}.txt"
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(text, encoding="utf-8")
    chars = len(re.sub(r"\s+", "", text))
    if chars < 20:
        raise RuntimeError("DOCX extraction produced fewer than 20 non-space characters")
    return OcrRecord(
        group=group,
        source=source.name,
        source_path=str(source),
        searchable_pdf=None,
        text_path=str(text_path),
        pages=None,
        method="docx-native",
        text_chars=chars,
        status="ok",
    )


def process_source(source: Path, group: str, pdf_root: Path, text_root: Path, jobs: int, fast: bool) -> OcrRecord:
    try:
        if source.suffix.casefold() == ".pdf":
            return process_pdf(source, group, pdf_root, text_root, jobs, fast)
        if source.suffix.casefold() == ".docx":
            return process_docx(source, group, text_root)
        raise RuntimeError(f"unsupported source extension: {source.suffix}")
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as exc:
        return OcrRecord(
            group=group,
            source=source.name,
            source_path=str(source),
            searchable_pdf=None,
            text_path=None,
            pages=None,
            method="failed",
            text_chars=0,
            status="failed",
            error=f"{type(exc).__name__}: {exc}",
        )


def discover_sources(module_root: Path, scope: str) -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    if scope in {"raw", "all"}:
        roots.append(("Raw_PDF_Questions", module_root / "Raw_PDF_Questions"))
    if scope in {"lectures", "all"}:
        roots.append(("Lectures", module_root / "Lectures"))
    sources: list[tuple[str, Path]] = []
    for group, root in roots:
        if not root.exists():
            continue
        for path in sorted(root.iterdir(), key=lambda candidate: candidate.name.casefold()):
            if path.is_file() and path.suffix.casefold() in {".pdf", ".docx"}:
                sources.append((group, path))
    return sources


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module-root", type=Path, required=True)
    parser.add_argument("--scope", choices=["raw", "lectures", "all"], default="all")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--ocr-jobs", type=int, default=1)
    parser.add_argument("--fast", action="store_true", help="use 200-DPI OCR without deskew/rotation; suitable for lecture upload copies")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.workers < 1 or args.ocr_jobs < 1:
        raise SystemExit("--workers and --ocr-jobs must be positive")
    module_root = args.module_root.expanduser().resolve()
    pdf_root = module_root / "OCR_PDF"
    text_root = module_root / "OCR_Text"
    sources = discover_sources(module_root, args.scope)
    if not sources:
        raise SystemExit("no PDF/DOCX sources found")
    records: list[OcrRecord] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process_source, path, group, pdf_root, text_root, args.ocr_jobs, args.fast): (group, path)
            for group, path in sources
        }
        for index, future in enumerate(as_completed(futures), start=1):
            record = future.result()
            records.append(record)
            marker = "OK" if record.status == "ok" else "FAIL"
            print(f"[{index}/{len(futures)}] {marker} {record.group}/{record.source} ({record.method})")
            if record.error:
                print(f"  {record.error}")
    records.sort(key=lambda record: (record.group, record.source.casefold()))
    manifest = module_root / "OCR_MANIFEST.json"
    manifest.write_text(
        json.dumps(
            {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "scope": args.scope,
                "sourceCount": len(records),
                "okCount": sum(record.status == "ok" for record in records),
                "failedCount": sum(record.status == "failed" for record in records),
                "records": [asdict(record) for record in records],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest}")
    return 0 if all(record.status == "ok" for record in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
