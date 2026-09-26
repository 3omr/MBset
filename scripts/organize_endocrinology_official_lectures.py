#!/usr/bin/env python3
"""Organize Endocrinology lecture PDFs using the uploaded official IDs.

The old filename-based folders are moved to dated backups.  Nothing is
deleted.  Only PDFs already present locally (including the merged surgery
lecture) are copied into the official-ID folders; unavailable DocReader
lectures remain explicit ``missing`` records.

Source selection is deliberate and ordered: PowerPoint/College material
first, then the book, then a DocReader summary/PDF, then ``missing``.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "أزهر دمياط/Endocrinology"
EXPORT = MODULE / "subcategories_Endocrinology_2026-09-18.xlsx"
LECTURES = MODULE / "Lectures"
UPLOAD = MODULE / "Lectures_OCR_Upload"
OLD_MANIFEST = MODULE / "lecture_source_manifest.json"

MANIFEST_OUT = MODULE / "lecture_source_manifest_official.json"
SUMMARY_OUT = MODULE / "lecture_upload_summary.md"
POWERPOINT_DIR = MODULE / "Lecture_PowerPoint_PDF_Staging"

# This order is part of the module's source-of-truth metadata. The first
# available source wins for each official subcategory.
SOURCE_PRIORITY = ["powerpoint", "book", "docreader_summary", "missing"]

OFFICIAL_MERGED = (
    "DamiettaFa_ENDOCRINOLOGY_2_APPLIED_ANATOMY_OF_THYROID_PARATHYROID_GLANDS_"
    "SURGICAL_MANAGEMENT_OF_THYROID_PARATHYROID_DISORDERS.pdf"
)


def norm(value: str) -> str:
    value = value.casefold().replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "", value)


ALIASES = {
    norm("Laboratory Diagnosis of Diabetes"): norm(
        "Clinical Pathology: Laboratory Diagnosis of Diabetes & Endocrine Diseases"
    ),
    norm("Structural & Functional Imaging of Endocrine Gland"): norm(
        "Radiology: Structural & Functional Imaging of Endocrine Gland"
    ),
    norm("Calcium homeostasis"): norm("Bio: Calcium homeostasis"),
    norm("Diabetes Pharmacotherapy"): norm("Pharma: Diabetes Pharmacotherapy"),
    norm("Posterior pituitary (Diabetes Insipidus, SIADH)"): norm(
        "Posterior pituitary disorders (Diabetes Insipidus, SIADH)"
    ),
    norm("Prolactinoma & Galactorrhea, Non-Functioning Adenomas"): norm(
        "Prolactinoma & Galactorrhea, Non-Functioning Adenomas and Pituitary Apoplexy"
    ),
}


def rows() -> list[dict[str, object]]:
    workbook = load_workbook(EXPORT, read_only=True, data_only=True)
    sheet = workbook["Subcategories"]
    headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    result = [dict(zip(headers, row)) for row in sheet.iter_rows(min_row=2, values_only=True)]
    workbook.close()
    return sorted(result, key=lambda row: int(row["orderIndex"]))


def old_sources() -> dict[str, dict[str, object]]:
    data = json.loads(OLD_MANIFEST.read_text(encoding="utf-8"))
    result: dict[str, dict[str, object]] = {}
    for item in data.get("lectures", []):
        path = Path(item.get("output") or "")
        if item.get("status") == "ready":
            result[item["name"]] = {
                "path": path,
                "kind": item.get("source") or "existing",
            }
    return result


def find_legacy_source(
    official_name: str, legacy: dict[str, dict[str, object]]
) -> dict[str, object] | None:
    target = norm(official_name)
    for old_name, source in legacy.items():
        old = norm(old_name)
        expected = ALIASES.get(old, old)
        if expected == target or old == target:
            return source
    candidates = [
        source
        for old_name, source in legacy.items()
        if norm(old_name) in target or target in norm(old_name)
    ]
    return candidates[0] if len(candidates) == 1 else None


POWERPOINT_FILES = {
    "DamiettaFa_ENDOCRINOLOGY_2_HASHIMOTO_S_THYROIDITIS": "0000000292__Hashimoto thyrodisis.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_HYPOTHYROIDISM": "0000000315__Hypothyroidism.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_HYPERPARATHYROIDISM": "0000000316__Hyperparathyroidism.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_HYPOPARATHYROIDISM": "0000000317__Hypoparathyroidism.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_BONE_MINERAL_DISORDERS": "0000000326__bonevdiseseses_013727.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_ADRENAL_HYPERSECRETION": "0000000330__adrenal hypersecretion.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_ENDOCRINE_HYPERTENSION": "0000000332__endocrine htn.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_CUSHING_S_SYNDROME": "0000000345__cushing-syndrome1.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_ADRENAL_HYPOFUNCTION": "0000000373__Adrenal hypofunction.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_ACROMEGALY": "0000000374__Acromegaly.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_PANHYPOPITUITARISM": "0000000375__Panhypopituitarism.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_POSTERIOR_PITUITARY_DISORDERS_DIABETES_INSIPIDUS_SIADH": "0000000376_0377__Posterior_pituitary_disorders.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_MICROVASCULAR_DIABETIC_COMPLICATIONS": "0000000406__Microvascular DM ds..pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_CONGENITAL_HYPOTHYROIDISM_CRETINISM": "0000000294__Congenital Hypothyroidism.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_CLINICAL_PATHOLOGY_LABORATORY_DIAGNOSIS_OF_DIABETES_ENDOCRINE_DISEASES": "0000000442__Laboratory Diagnosis of Endocrine Diseases.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_RADIOLOGY_STRUCTURAL_FUNCTIONAL_IMAGING_OF_ENDOCRINE_GLAND": "0000000444__slidesaver.app_oabovdمعدل.pdf",
    "DamiettaFa_ENDOCRINOLOGY_2_APPLIED_ANATOMY_OF_THYROID_PARATHYROID_GLANDS_SURGICAL_MANAGEMENT_OF_THYROID_PARATHYROID_DISORDERS": "merged_applied_anatomy_thyroid_parathyroid.pdf",
}


def powerpoint_sources() -> dict[str, Path]:
    return {
        subcategory_id: POWERPOINT_DIR / filename
        for subcategory_id, filename in POWERPOINT_FILES.items()
        if (POWERPOINT_DIR / filename).exists()
    }


def page_count(path: Path) -> int | None:
    probe = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=False)
    match = re.search(r"^Pages:\s+(\d+)", probe.stdout, re.M)
    return int(match.group(1)) if match else None


def text_chars(path: Path) -> int:
    probe = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=False)
    return len(re.sub(r"\s+", "", probe.stdout)) if probe.returncode == 0 else 0


def backup_and_reset() -> tuple[Path, Path]:
    stamp = "2026-09-18"
    old_backup = MODULE / f"Lectures_PreOfficialNames_{stamp}"
    upload_backup = MODULE / f"Lectures_OCR_PreOfficialNames_{stamp}"
    old_backup.mkdir(parents=True, exist_ok=True)
    upload_backup.mkdir(parents=True, exist_ok=True)
    for source_dir, backup_dir in ((LECTURES, old_backup), (UPLOAD, upload_backup)):
        if not source_dir.exists():
            continue
        for path in source_dir.iterdir():
            if path.is_file():
                destination = backup_dir / path.name
                if destination.exists():
                    destination = backup_dir / f"{path.stem}_copy{path.suffix}"
                shutil.move(str(path), str(destination))
    LECTURES.mkdir(parents=True, exist_ok=True)
    UPLOAD.mkdir(parents=True, exist_ok=True)
    return old_backup, upload_backup


def build() -> None:
    lecture_rows = rows()
    legacy = old_sources()
    ppt_sources = powerpoint_sources()
    old_backup, upload_backup = backup_and_reset()
    legacy = {
        name: {
            **source,
            "path": (
                source["path"]
                if Path(source["path"]).exists()
                else old_backup / Path(source["path"]).name
            ),
        }
        for name, source in legacy.items()
    }

    records: list[dict[str, object]] = []
    for row in lecture_rows:
        name = str(row["name"])
        subcategory_id = str(row["subcategoryId"])
        official_path = LECTURES / f"{subcategory_id}.pdf"
        upload_path = UPLOAD / f"{subcategory_id}.pdf"

        source = ppt_sources.get(subcategory_id)
        source_kind = "powerpoint" if source else None
        if not source:
            legacy_source = find_legacy_source(name, legacy)
            if legacy_source:
                source = Path(legacy_source["path"])
                legacy_kind = str(legacy_source.get("kind") or "existing")
                source_kind = {
                    "book": "book",
                    "local_download": "docreader_summary",
                    "docreader_download": "docreader_summary",
                }.get(legacy_kind, "existing")
        # The merged surgery file existed before the reset; recover it from the
        # dated backup after the reset.
        if (
            not source
            and subcategory_id.endswith(
                "APPLIED_ANATOMY_OF_THYROID_PARATHYROID_GLANDS_SURGICAL_MANAGEMENT_OF_THYROID_PARATHYROID_DISORDERS"
            )
        ):
            candidate = old_backup / OFFICIAL_MERGED
            if candidate.exists():
                source = candidate
                source_kind = "powerpoint_merged"

        if source and source.exists():
            shutil.copy2(source, official_path)
            upload_source = upload_backup / source.name
            shutil.copy2(upload_source if upload_source.exists() else source, upload_path)
            records.append({
                "subcategoryId": subcategory_id,
                "name": name,
                "tag": row["tag"],
                "orderIndex": row["orderIndex"],
                "status": "ready",
                "sourceKind": source_kind,
                "sourcePriorityUsed": (
                    "powerpoint"
                    if source_kind in {"powerpoint", "powerpoint_merged"}
                    else source_kind
                ),
                "source": str(source),
                "output": str(official_path),
                "uploadOutput": str(upload_path),
                "pages": page_count(official_path),
                "textChars": text_chars(official_path),
            })
        else:
            records.append({
                "subcategoryId": subcategory_id,
                "name": name,
                "tag": row["tag"],
                "orderIndex": row["orderIndex"],
                "status": "missing",
                "sourcePriorityUsed": "missing",
                "source": None,
                "output": None,
                "uploadOutput": None,
                "pages": None,
                "textChars": 0,
            })

    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "export": str(EXPORT),
        "lectureCount": len(records),
        "readyCount": sum(r["status"] == "ready" for r in records),
        "missingCount": sum(r["status"] == "missing" for r in records),
        "sourcePriority": SOURCE_PRIORITY,
        "sourcePriorityRule": (
            "PowerPoint/College first; then book; then DocReader summary/PDF; "
            "otherwise missing"
        ),
        "backupLectures": str(old_backup),
        "backupUpload": str(upload_backup),
        "lectures": records,
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Endocrinology — official lecture upload summary",
        "",
        f"- Official rows: **{len(records)}**",
        f"- Ready PDFs: **{manifest['readyCount']}**",
        f"- Missing source: **{manifest['missingCount']}**",
        "- Source priority: **PowerPoint/College → Book → DocReader summary/PDF → Missing**",
        f"- Old names preserved in: `{old_backup}`",
        "",
        "| Order | Group | Lecture | Subcategory ID | Status | Source used | Pages | Text chars |",
        "|---:|---|---|---|---|---|---:|---:|",
    ]
    for item in records:
        pages = item["pages"] if item["pages"] is not None else "—"
        lines.append(
            f"| {item['orderIndex']} | {item['tag']} | {item['name']} | `{item['subcategoryId']}` | {item['status']} | {item['sourcePriorityUsed']} | {pages} | {item['textChars']} |"
        )
    SUMMARY_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Official lecture PDFs: {manifest['readyCount']} ready, {manifest['missingCount']} missing")
    print(f"Manifest: {MANIFEST_OUT}")
    print(f"Summary: {SUMMARY_OUT}")


if __name__ == "__main__":
    build()
