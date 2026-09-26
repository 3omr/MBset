"""Shared paths, state and text helpers for the MBset pipeline.

Every module keeps its machine state in ``<Module>/.mbset/``:

    state.json          inventory + per-source stage status (single source of truth)
    profiles/NN.yaml    parser profile per source (written by `profile`, edited by the agent)
    ocr/NN.json         cached OCR lines (keyed by the source sha256)
    parsed/NN.json      parser output: questions with page/bbox evidence and flags
    reports/            check reports, spot-check sheets, contact sheets
    packets/            work packets for parallel agents
    work/               scratch space (never versioned)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
INVISIBLE = re.compile(r"[​-‏‪-‮⁠-⁤﻿­]")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

SOURCE_SUFFIXES = {".pdf", ".docx", ".pptx", ".txt", ".md", ".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
ARCHIVE_SUFFIXES = {".zip", ".7z", ".rar"}
LETTERS = "ABCDEF"

SUBJECTS = ("Anatomy", "Physiology", "Histology", "Biochemistry", "Microbiology",
            "Parasitology", "Pathology", "Pharmacology")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_stem(text: str | None) -> str:
    """The Stage-4 dedupe key: lowercase ASCII alphanumerics only."""
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def clean_inline(text: str) -> str:
    """Normalize one extracted line without changing its wording."""
    text = unicodedata.normalize("NFC", text)
    text = CONTROL.sub("", INVISIBLE.sub("", text)).replace("\xa0", " ")
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    return re.sub(r"[ \t]+", " ", text).strip()


def safe_name(name: str, limit: int = 60) -> str:
    stem = ARABIC.sub("", Path(name).stem)
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_")
    return (stem or "source")[:limit].strip("_")


def _merge_state(base: dict[str, Any], mine: dict[str, Any], disk: dict[str, Any]) -> dict[str, Any]:
    """Apply my changes (base → mine) on top of what another process saved (disk)."""
    out = json.loads(json.dumps(disk))
    for k, v in mine.items():
        if k in ("sources", "updated"):
            continue
        if base.get(k) != v:
            out[k] = v
    key = lambda s: s.get("rel")  # noqa: E731
    base_src = {key(s): s for s in base.get("sources", [])}
    disk_idx = {key(s): i for i, s in enumerate(out.get("sources", []))}
    for s in mine.get("sources", []):
        if base_src.get(key(s)) == s:
            continue                                  # untouched by me: keep the disk version
        if key(s) in disk_idx:
            out["sources"][disk_idx[key(s)]] = s
        else:
            out.setdefault("sources", []).append(s)
    return out


class Module:
    """A module folder (e.g. `أزهر دمياط/Endocrinology`) and its `.mbset` state."""

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise SystemExit(f"[-] module folder not found: {self.root}")
        self.meta = self.root / ".mbset"
        self.raw = self.root / "Raw_PDF_Questions"
        self.markdown = self.root / "Markdown_Questions"
        self.images = self.root / "Images"
        for sub in ("profiles", "ocr", "parsed", "reports", "packets", "work", "locks", "cache"):
            (self.meta / sub).mkdir(parents=True, exist_ok=True)
        self.state_path = self.meta / "state.json"

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def university(self) -> str:
        path = str(self.root)
        return "Assiut" if "اسيوط" in path or "assiut" in path.lower() else "Damietta"

    # ---- state -----------------------------------------------------------------
    def load(self) -> dict[str, Any]:
        if self.state_path.exists():
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
        else:
            state = {"module": self.name, "sources": [], "archives": [], "created": now()}
        self._snapshot = json.loads(json.dumps(state))
        return state

    def save(self, state: dict[str, Any]) -> None:
        """Three-way merge under a file lock, so agents working on different sources in parallel
        never overwrite each other: only the sources / keys this process changed are written."""
        import fcntl

        base = getattr(self, "_snapshot", None)
        with open(self.meta / "state.lock", "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            merged = state
            if base is not None and self.state_path.exists():
                disk = json.loads(self.state_path.read_text(encoding="utf-8"))
                if disk != base:
                    merged = _merge_state(base, state, disk)
            merged["updated"] = now()
            tmp = self.state_path.with_suffix(f".{os.getpid()}.tmp")
            tmp.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, self.state_path)
            # the base of the next merge is *my* view, so only my later edits are written next time;
            # the in-memory state is never swapped out (callers hold references to its source dicts)
            self._snapshot = json.loads(json.dumps(state))

    def sources(self, state: dict[str, Any], selector: str | None = None) -> list[dict[str, Any]]:
        items = state.get("sources", [])
        if not selector:
            return items
        wanted: set[str] = set()
        for part in (s.strip() for s in selector.split(",")):
            m = re.fullmatch(r"(\d+)-(\d+)", part)
            if m:                                   # a range: 10-14
                wanted |= {f"{n:02d}" for n in range(int(m.group(1)), int(m.group(2)) + 1)}
            else:
                wanted.add(f"{int(part):02d}" if part.isdigit() else part)
        picked = [s for s in items if s["nn"] in wanted or s["rel"] in wanted
                  or Path(s["rel"]).name in wanted or (s.get("md") or "") in wanted]
        if not picked:
            raise SystemExit(f"[-] no source matches {selector!r}; see `mbset.py status {self.root}`")
        return picked

    def source_path(self, src: dict[str, Any]) -> Path:
        return self.root / src["rel"]

    def profile_path(self, src: dict[str, Any]) -> Path:
        return self.meta / "profiles" / f"{src['nn']}.yaml"

    def parsed_path(self, src: dict[str, Any]) -> Path:
        return self.meta / "parsed" / f"{src['nn']}.json"

    def ocr_path(self, src: dict[str, Any]) -> Path:
        return self.meta / "ocr" / f"{src['nn']}.json"

    def md_path(self, src: dict[str, Any]) -> Path:
        return self.markdown / src["md"]


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def parse_pages(spec: str | None, total: int) -> list[int]:
    """'1-3,7' → [0,1,2,6] (0-based); None → every page."""
    if not spec:
        return list(range(total))
    pages: list[int] = []
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start = int(a) if a else 1
            end = int(b) if b else total
            pages.extend(range(start - 1, min(end, total)))
        else:
            pages.append(int(part) - 1)
    return [p for p in pages if 0 <= p < total]
