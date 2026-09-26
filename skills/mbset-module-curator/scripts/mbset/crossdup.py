"""`crossdup` — byte-identical sources shared by more than one module (report only).

Hashes every file under ``<module>/Raw_PDF_Questions/**`` for every module found under the
given roots and groups the ones whose sha256 appears in more than one module. Nothing is
moved. Hashes are cached per module in ``<module>/.mbset/cache/hashes.json`` keyed by the
path relative to the module root and validated by (size, mtime_ns), so reruns are instant.

``HashCache`` is shared with `tidy`.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .common import sha256

CACHE_REL = Path(".mbset") / "cache" / "hashes.json"


class HashCache:
    """sha256 per file of one module folder, cached by (relative path, size, mtime_ns)."""

    def __init__(self, root: Path, persist: bool = True):
        self.root = Path(root).resolve()
        self.path = self.root / CACHE_REL
        self.persist = persist
        self.dirty = False
        try:
            self.data: dict[str, list[Any]] = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.data = {}

    def get(self, path: Path) -> str:
        path = Path(path)
        st = path.stat()
        try:
            key = str(path.resolve().relative_to(self.root))
        except ValueError:
            key = str(path.resolve())
        hit = self.data.get(key)
        if hit and hit[0] == st.st_size and hit[1] == st.st_mtime_ns:
            return hit[2]
        digest = sha256(path)
        self.data[key] = [st.st_size, st.st_mtime_ns, digest]
        self.dirty = True
        return digest

    def save(self) -> None:
        if not (self.persist and self.dirty):
            return
        # drop entries for files that no longer exist so the cache does not grow forever
        self.data = {k: v for k, v in self.data.items() if (self.root / k).exists()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, self.path)
        self.dirty = False


def find_modules(roots: list[str]) -> list[Path]:
    """A root is a module itself (has Raw_PDF_Questions) or a university folder of modules."""
    mods: list[Path] = []
    for r in roots:
        root = Path(r).resolve()
        if not root.is_dir():
            raise SystemExit(f"[-] not a folder: {root}")
        if (root / "Raw_PDF_Questions").is_dir():
            mods.append(root)
            continue
        mods += sorted(p for p in root.iterdir() if p.is_dir() and (p / "Raw_PDF_Questions").is_dir())
    seen: set[Path] = set()
    return [m for m in mods if not (m in seen or seen.add(m))]


def scan(modules: list[Path], min_size: int = 0) -> dict[str, list[dict[str, Any]]]:
    """sha256 → [{module, rel, size}] for every raw file of at least min_size bytes."""
    by_hash: dict[str, list[dict[str, Any]]] = {}
    for mod in modules:
        cache = HashCache(mod)
        for p in sorted((mod / "Raw_PDF_Questions").rglob("*")):
            if not p.is_file() or p.name.startswith("."):
                continue
            size = p.stat().st_size
            if size < min_size:
                continue
            by_hash.setdefault(cache.get(p), []).append(
                {"module": str(mod), "rel": str(p.relative_to(mod)), "size": size})
        cache.save()
    return by_hash


def shared(by_hash: dict[str, list[dict[str, Any]]]) -> list[tuple[str, list[dict[str, Any]]]]:
    groups = [(h, items) for h, items in by_hash.items() if len({i["module"] for i in items}) > 1]
    return sorted(groups, key=lambda g: (-g[1][0]["size"], g[1][0]["rel"]))


def _label(module: str, roots: list[Path]) -> str:
    p = Path(module)
    return f"{p.parent.name}/{p.name}"


def cmd_crossdup(args) -> int:
    modules = find_modules(args.roots)
    if not modules:
        print("[-] no module with Raw_PDF_Questions under the given roots")
        return 1
    by_hash = scan(modules, args.min_size)
    files = sum(len(v) for v in by_hash.values())
    groups = shared(by_hash)
    print(f"[=] {len(modules)} module(s), {files} raw file(s), {len(by_hash)} distinct")
    if not groups:
        print("[+] no source is shared between modules")
        return 0
    wasted = sum(items[0]["size"] * (len(items) - 1) for _, items in groups)
    print(f"[!] {len(groups)} source(s) appear in more than one module ({wasted / 1e6:.1f} MB in extra copies)\n")
    for h, items in groups:
        print(f"  sha256 {h[:12]} · {items[0]['size'] / 1e6:.2f} MB · {len({i['module'] for i in items})} modules")
        for i in items:
            print(f"      {_label(i['module'], modules)}: {i['rel']}")
    if args.json:
        Path(args.json).write_text(json.dumps([{"sha256": h, "files": items} for h, items in groups],
                                              ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n[=] json: {args.json}")
    return 0


def register(sub) -> None:
    p = sub.add_parser("crossdup", help="report raw sources byte-identical across modules (never moves anything)")
    p.add_argument("roots", nargs="+", help="module folders or university folders of modules")
    p.add_argument("--min-size", type=int, default=0, help="ignore files smaller than this many bytes")
    p.add_argument("--json", help="also write the groups as JSON here")
    p.set_defaults(fn=cmd_crossdup)
