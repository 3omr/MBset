#!/usr/bin/env python3
"""Write confidence- and position-aware OCR drafts with PaddleOCR 3.x."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def json_safe_value(ocr_value: Any) -> Any:
    if hasattr(ocr_value, "tolist"):
        return json_safe_value(ocr_value.tolist())
    if isinstance(ocr_value, dict):
        return {str(key): json_safe_value(child) for key, child in ocr_value.items()}
    if isinstance(ocr_value, (list, tuple)):
        return [json_safe_value(child) for child in ocr_value]
    if hasattr(ocr_value, "item"):
        return ocr_value.item()
    return ocr_value


def extract_page_json(ocr_page: Any) -> dict[str, Any]:
    page_json = getattr(ocr_page, "json", None)
    page_json = page_json() if callable(page_json) else page_json
    page_json = json_safe_value(page_json)
    if isinstance(page_json, str):
        page_json = json.loads(page_json)
    if not isinstance(page_json, dict):
        raise ValueError("PaddleOCR returned an unexpected page result")
    return page_json


def detection_bounds(index: int, rectangles: list, polygons: list) -> list[float] | None:
    if index < len(rectangles) and len(rectangles[index]) >= 4:
        return [float(coordinate) for coordinate in rectangles[index][:4]]
    if index >= len(polygons):
        return None
    points = [point for point in polygons[index] if len(point) >= 2]
    if not points:
        return None
    xs = [float(point[0]) for point in points]
    ys = [float(point[1]) for point in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def extract_ocr_lines(page_json: dict[str, Any], review_below: float) -> list[dict[str, Any]]:
    page_fields = page_json.get("res", page_json)
    texts = page_fields.get("rec_texts", [])
    scores = page_fields.get("rec_scores", [])
    rectangles = page_fields.get("rec_boxes", [])
    polygons = page_fields.get("rec_polys", [])
    lines = []
    for index, text in enumerate(texts):
        score = float(scores[index]) if index < len(scores) else None
        lines.append({"text": str(text), "confidence": score,
                      "bbox": detection_bounds(index, rectangles, polygons),
                      "review": score is not None and score < review_below})
    return sorted(lines, key=reading_position)


def reading_position(line: dict[str, Any]) -> tuple[float, float]:
    bounds = line["bbox"]
    return (bounds[1], bounds[0]) if bounds else (float("inf"), float("inf"))


def format_ocr_line(line: dict[str, Any]) -> str:
    score = line["confidence"]
    score_text = f"{score:.3f}" if score is not None else "unknown"
    review = "[review] " if line["review"] else ""
    return f"{review}[confidence={score_text}; bbox={line['bbox']}] {line['text']}"


def write_page_files(output_dir: Path, page_name: str, page_index: Any, lines: list[dict[str, Any]]) -> None:
    text_path = output_dir / f"{page_name}.txt"
    json_path = output_dir / f"{page_name}.json"
    text_path.write_text("\n".join(map(format_ocr_line, lines)) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps({"page": page_name, "page_index": page_index, "lines": lines},
                                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def page_summary(page_name: str, page_index: Any, lines: list[dict[str, Any]], output_dir: Path) -> dict[str, Any]:
    return {"page": page_name, "page_index": page_index, "line_count": len(lines),
            "low_confidence_lines": sum(line["review"] for line in lines),
            "text_file": str(output_dir / f"{page_name}.txt"),
            "json_file": str(output_dir / f"{page_name}.json")}


def scan_source(ocr_engine: Any, source: Path, output_dir: Path, review_below: float) -> list[dict[str, Any]]:
    page_records = []
    for page_number, ocr_page in enumerate(ocr_engine.predict(str(source)), start=1):
        page_json = extract_page_json(ocr_page)
        lines = extract_ocr_lines(page_json, review_below)
        page_name = f"page_{page_number:04d}" if source.suffix.casefold() == ".pdf" else "image_0001"
        page_index = page_json.get("res", page_json).get("page_index")
        write_page_files(output_dir, page_name, page_index, lines)
        page_records.append(page_summary(page_name, page_index, lines, output_dir))
    if not page_records:
        raise RuntimeError(f"PaddleOCR returned no pages for {source}")
    return page_records


def safe_source_name(source: Path) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", source.stem).strip("._") or "source"


def create_ocr_engine() -> Any:
    try:
        from paddleocr import PaddleOCR
    except ImportError as exc:
        raise SystemExit("Install PaddlePaddle and PaddleOCR 3.x; see legacy/smart-ocr-workflow.md") from exc
    return PaddleOCR(text_detection_model_name="PP-OCRv5_mobile_det",
                     text_recognition_model_name="en_PP-OCRv5_mobile_rec",
                     use_doc_orientation_classify=True,
                     use_doc_unwarping=False, use_textline_orientation=True,
                     device="cpu", enable_mkldnn=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path, help="PDF or image source files")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--review-below", type=float, default=0.85,
                        help="flag lines below this confidence for review (default: 0.85)")
    args = parser.parse_args()
    if not 0 <= args.review_below <= 1:
        parser.error("--review-below must be between 0 and 1")
    for source in args.sources:
        if not source.is_file():
            parser.error(f"source file not found: {source}")
        if source.suffix.casefold() != ".pdf" and source.suffix.casefold() not in IMAGE_SUFFIXES:
            parser.error(f"unsupported source type: {source}")
    return args


def source_record(source: Path, output_dir: Path, pages: list[dict[str, Any]]) -> dict[str, Any]:
    return {"source": str(source), "output_dir": str(output_dir), "page_count": len(pages),
            "low_confidence_lines": sum(page["low_confidence_lines"] for page in pages), "pages": pages}


def write_manifest(output_dir: Path, records: list[dict[str, Any]], review_below: float) -> None:
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps({"review_below": review_below, "sources": records},
                                        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    ocr_engine = create_ocr_engine()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_records = []
    for index, source in enumerate(args.sources, start=1):
        output_dir = args.output_dir / f"{index:02d}_{safe_source_name(source)}"
        output_dir.mkdir(parents=True, exist_ok=True)
        pages = scan_source(ocr_engine, source, output_dir, args.review_below)
        source_records.append(source_record(source, output_dir, pages))
        flagged_lines = source_records[-1]["low_confidence_lines"]
        print(f"{source}: {len(pages)} page(s), {flagged_lines} line(s) flagged")
    write_manifest(args.output_dir, source_records, args.review_below)
    print(f"Manifest: {args.output_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
