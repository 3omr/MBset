"""`tidy` — standardize a module folder to the AGENTS.md §2.E deliverables layout.

Dry run by default: prints a plan (action, path, size, reason) and writes it to
``.mbset/reports/tidy_<date>.md``. ``--apply`` never deletes anything: items are moved into
``<Module>/_trash/<date>/<original relative path>`` (or into ``Raw_PDF_Questions/`` /
``.mbset/archive/``), and every move is written to ``_trash/<date>/MANIFEST.json`` (original
path, new path, sha256 per file, size) so ``tidy <Module> --restore <date>`` puts it all back.

Rules (in order):

* ``Raw_PDF_Questions``, ``Markdown_Questions`` (real files), ``Images``, ``.mbset`` and
  ``_trash`` are never touched; ``<Module>_Questions.xlsx`` is kept.
* ``--lectures-from DIR``: DIR is the official uploaded lecture set — the current
  ``Lectures/`` goes to the trash and DIR is renamed ``Lectures/``; every other
  ``Lecture*_…`` folder goes to the trash. Without the flag ``Lectures/`` is kept and another
  lecture folder is trashed only when every file in it is a byte-duplicate of ``Lectures/``
  or its name says ``PreOfficialNames`` / ``Staging`` (the reason says which).
* ``OCR_PDF/``, ``OCR_Text/`` → trash (legacy OCR; the pipeline keeps OCR in .mbset/ocr).
* ``Telegram_Staging/`` → ``.mbset/archive/`` unless it holds pdf/doc(x) not already in
  ``Raw_PDF_Questions`` by hash: those are listed as *needs decision* and the folder stays.
* Any other folder with source-like files (pdf/doc(x)/ppt(x)/images/archives): byte-duplicates
  of ``Raw_PDF_Questions`` → trash, unique sources → ``Raw_PDF_Questions/<folder>/``, other
  files → ``.mbset/archive/<folder>/``; a folder of duplicates only is trashed whole.
  Folders without source-like files → ``.mbset/archive/``.
* ``subcategories_*.xlsx``: the one with the latest ``YYYY-MM-DD`` in its name is kept, the
  rest (undated = oldest) → trash.
* Loose ``*.json`` / ``*.md`` / ``*.txt`` / ``*.csv`` / ``*.log`` at the top level → ``.mbset/archive/``;
  a loose source-like file is trashed when it duplicates a raw source, else *needs decision*.
* ``Markdown_Questions/*.md`` that are only an EXCLUDED / DUPLICATE placeholder are reported;
  they are trashed only with ``--apply --placeholders``.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .common import IMAGE_SUFFIXES, Module, now
from .crossdup import HashCache

SOURCE_LIKE = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".zip", ".rar", ".7z"} | IMAGE_SUFFIXES
QUESTION_SOURCES = {".pdf", ".docx", ".doc"}
META_SUFFIXES = {".json", ".md", ".txt", ".csv", ".log"}
PROTECTED = {"Raw_PDF_Questions", "Markdown_Questions", "Images", ".mbset", "_trash"}
LEGACY_OCR = {"OCR_PDF", "OCR_Text"}
LECTURE_LIKE = re.compile(r"(?i)^lectures?[_ -]")
STAGING_NAME = re.compile(r"(?i)PreOfficialNames|Staging")
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")

TRASH, TO_RAW, ARCHIVE, RENAME, KEEP, DECIDE, PLACEHOLDER = (
    "trash", "move→raw", "archive", "rename", "keep", "needs decision", "placeholder")
ORDER = {TRASH: 0, TO_RAW: 1, ARCHIVE: 2, RENAME: 3}   # the old Lectures/ leaves before DIR is renamed
MOVES = set(ORDER)


@dataclass
class Item:
    action: str
    rel: str
    size: int
    reason: str
    dest: str | None = None
    kind: str = "file"
    detail: bool = False        # a file listed under a folder row (not counted twice in the totals)


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return str(n)


def _files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*") if p.is_file())


def _size(path: Path) -> int:
    return sum(p.stat().st_size for p in _files(path))


def is_placeholder(path: Path) -> bool:
    """A markdown file that only records an exclusion (no `### Q` block)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if re.search(r"^###\s*Q\d+", text, re.M):
        return False
    named = re.search(r"_(EXCLUDED|DUPLICATE)\b", path.stem, re.I)
    marked = path.stat().st_size < 2000 and re.search(r"\b(EXCLUDED|DUPLICATE)\b", text)
    return bool(named or marked)


# --------------------------------------------------------------------------- plan
def plan(root: Path, lectures_from: str | None = None, placeholders: bool = False,
         cache: HashCache | None = None) -> list[Item]:
    root = Path(root).resolve()
    hc = cache or HashCache(root)
    items: list[Item] = []
    raw = root / "Raw_PDF_Questions"
    raw_hashes = {hc.get(p) for p in _files(raw)} if raw.is_dir() else set()
    rel = lambda p: str(p.relative_to(root))  # noqa: E731

    official: Path | None = None
    if lectures_from:
        official = Path(lectures_from)
        official = (official if official.is_absolute() else root / official).resolve()
        if not official.is_dir() or official.parent != root:
            raise SystemExit(f"[-] --lectures-from must be a folder directly inside the module: {official}")
        if official.name == "Lectures":
            raise SystemExit("[-] --lectures-from is already Lectures/")
    lectures = root / "Lectures"
    ref = official or lectures
    ref_hashes = {hc.get(p) for p in _files(ref)} if ref.is_dir() else set()

    def dup_count(path: Path, pool: set[str]) -> tuple[int, int]:
        fs = _files(path)
        return sum(hc.get(p) in pool for p in fs), len(fs)

    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    subcats = [p for p in entries if p.is_file() and re.fullmatch(r"(?i)subcategories_.*\.xlsx", p.name)]
    if subcats:
        best = max(subcats, key=lambda p: (DATE.search(p.name).group(1) if DATE.search(p.name) else "",
                                           p.stat().st_mtime))
    for p in entries:
        name = p.name
        if name.startswith(".") and name != ".mbset":
            continue
        if p.is_dir():
            if name in PROTECTED:
                items.append(Item(KEEP, name, 0, "pipeline deliverable / state — never touched", kind="dir"))
            elif name == "Lectures":
                if official:
                    k, n = dup_count(p, ref_hashes)
                    items.append(Item(TRASH, name, _size(p), f"replaced by the official upload set {official.name}/ "
                                      f"({k}/{n} files byte-identical to it)", kind="dir"))
                else:
                    items.append(Item(KEEP, name, _size(p), "lecture PDFs (Lectures/<subcategoryId>.pdf)", kind="dir"))
            elif official and p.resolve() == official:
                items.append(Item(RENAME, name, _size(p), "official uploaded lecture set → Lectures/",
                                  dest="Lectures", kind="dir"))
            elif LECTURE_LIKE.match(name):
                k, n = dup_count(p, ref_hashes)
                if official:
                    items.append(Item(TRASH, name, _size(p), f"superseded by the official set {official.name}/ "
                                      f"({k}/{n} files byte-identical to it)", kind="dir"))
                elif n and k == n:
                    items.append(Item(TRASH, name, _size(p), f"all {n} files byte-identical to Lectures/", kind="dir"))
                elif STAGING_NAME.search(name):
                    items.append(Item(TRASH, name, _size(p), f"folder name marks it pre-official/staging "
                                      f"({k}/{n} files byte-identical to Lectures/, {n - k} not)", kind="dir"))
                elif not n:
                    items.append(Item(TRASH, name, 0, "empty lecture folder", kind="dir"))
                else:
                    items.append(Item(DECIDE, name, _size(p), f"lecture folder with {n - k}/{n} files not in "
                                      "Lectures/ — pass --lectures-from if it is the official set", kind="dir"))
            elif name in LEGACY_OCR:
                items.append(Item(TRASH, name, _size(p), "legacy OCR output (pipeline OCR lives in .mbset/ocr)",
                                  kind="dir"))
            elif name == "Telegram_Staging":
                unique = [f for f in _files(p) if f.suffix.lower() in QUESTION_SOURCES and hc.get(f) not in raw_hashes]
                if unique:
                    items.append(Item(DECIDE, name, _size(p), f"{len(unique)} pdf/doc(x) not in Raw_PDF_Questions "
                                      "— folder left in place until they are sorted", kind="dir"))
                    items += [Item(DECIDE, rel(f), f.stat().st_size, "question source? not in Raw_PDF_Questions"
                                   + (" (byte-identical to a lecture PDF)" if hc.get(f) in ref_hashes else ""),
                                   detail=True) for f in unique]
                else:
                    items.append(Item(ARCHIVE, name, _size(p), "unsorted downloads; every pdf/doc(x) already in "
                                      "Raw_PDF_Questions", dest=f".mbset/archive/{name}", kind="dir"))
            else:
                items += _plan_other_dir(root, p, raw_hashes, hc)
        else:
            if name == f"{root.name}_Questions.xlsx":
                items.append(Item(KEEP, name, p.stat().st_size, "master question bank"))
            elif p in subcats:
                if p == best:
                    items.append(Item(KEEP, name, p.stat().st_size, "latest platform subcategories export"))
                else:
                    d = DATE.search(name)
                    items.append(Item(TRASH, name, p.stat().st_size, f"older subcategories export "
                                      f"({d.group(1) if d else 'undated'}); keeping {best.name}"))
            elif p.suffix.lower() in META_SUFFIXES:
                note = ""
                if "tag_map" in name:
                    note = " (inventory reads *tag_map*.json from the module root: run `inventory` first)"
                items.append(Item(ARCHIVE, name, p.stat().st_size, "loose metadata / legacy report" + note,
                                  dest=f".mbset/archive/{name}"))
            elif p.suffix.lower() in SOURCE_LIKE:
                if hc.get(p) in raw_hashes:
                    items.append(Item(TRASH, name, p.stat().st_size, "byte-identical copy of a raw source"))
                else:
                    items.append(Item(DECIDE, name, p.stat().st_size, "loose source not in Raw_PDF_Questions"))
            else:
                items.append(Item(DECIDE, name, p.stat().st_size, "unknown top-level file"))

    md = root / "Markdown_Questions"
    owners: dict[str, dict[str, Any]] = {}
    try:
        owners = {s.get("md"): s for s in json.loads((root / ".mbset" / "state.json").read_text(encoding="utf-8"))
                  .get("sources", [])}
    except (OSError, ValueError):
        pass
    if md.is_dir():
        for f in sorted(md.glob("*.md")):
            if not f.name.startswith("00_") and is_placeholder(f):
                owner = owners.get(f.name)
                note = (f"; it is the markdown of state source {owner['nn']} (status {owner.get('status')}) — "
                        "mark it `set --exclude` first" if owner and owner.get("status") != "excluded" else
                        f"; owned by excluded state source {owner['nn']}" if owner else
                        "; no state source owns it" if owners else "")
                live_owner = bool(owner) and owner.get("status") != "excluded"   # check needs this file
                items.append(Item(TRASH if placeholders and not live_owner else PLACEHOLDER, rel(f), f.stat().st_size,
                                  "EXCLUDED/DUPLICATE placeholder (trashed only with --apply --placeholders)" + note))
    hc.save()
    return items


def _plan_other_dir(root: Path, d: Path, raw_hashes: set[str], hc: HashCache) -> list[Item]:
    files = _files(d)
    name = d.name
    if not files:
        return [Item(TRASH, name, 0, "empty folder", kind="dir")]
    sources = [f for f in files if f.suffix.lower() in SOURCE_LIKE]
    if not sources:
        return [Item(ARCHIVE, name, _size(d), "unknown folder without question sources",
                     dest=f".mbset/archive/{name}", kind="dir")]
    dups = [f for f in sources if hc.get(f) in raw_hashes]
    if len(dups) == len(files):
        return [Item(TRASH, name, _size(d), f"all {len(files)} files byte-identical to Raw_PDF_Questions", kind="dir")]
    out = []
    for f in files:
        r = str(f.relative_to(root))
        inner = str(f.relative_to(d))
        if f in dups:
            out.append(Item(TRASH, r, f.stat().st_size, "byte-identical to a file in Raw_PDF_Questions"))
        elif f.suffix.lower() in SOURCE_LIKE:
            out.append(Item(TO_RAW, r, f.stat().st_size, "unique source → inventory it",
                            dest=f"Raw_PDF_Questions/{name}/{inner}"))
        else:
            out.append(Item(ARCHIVE, r, f.stat().st_size, "non-source file", dest=f".mbset/archive/{name}/{inner}"))
    return out


# --------------------------------------------------------------------------- output
def totals(items: list[Item]) -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for it in items:
        if it.action == KEEP or it.detail:
            continue
        c, b = out.get(it.action, (0, 0))
        out[it.action] = (c + 1, b + it.size)
    return out


def layout(root: Path, items: list[Item]) -> list[str]:
    """Top-level names after the plan (depth 1)."""
    root = Path(root)
    names = {p.name + ("/" if p.is_dir() else "") for p in root.iterdir() if not p.name.startswith(".")}
    names.add(".mbset/")
    moved: dict[str, int] = {}
    for it in items:
        if it.action not in MOVES:
            continue
        top = Path(it.rel).parts[0]
        if len(Path(it.rel).parts) == 1:
            names.discard(top + ("/" if it.kind == "dir" else ""))
        else:
            moved[top] = moved.get(top, 0) + 1
        if it.action == TRASH:
            names.add("_trash/")
        elif it.action == RENAME:
            names.add(it.dest + "/")
    for top, n in moved.items():
        if (root / top).is_dir() and n >= len(_files(root / top)):
            names.discard(top + "/")
    return sorted(names, key=lambda s: (not s.endswith("/"), s.lower()))


def render(root: Path, items: list[Item], applied: bool, date: str) -> str:
    lines = [f"# Tidy plan — {Path(root).name}", "", f"Generated {now()} · {'APPLIED' if applied else 'dry run'}", "",
             "| action | path | size | reason | destination |", "|---|---|---:|---|---|"]
    for it in items:
        if it.action == KEEP:
            continue
        dest = it.dest or (f"_trash/{date}/{it.rel}" if it.action == TRASH else "")
        lines.append(f"| {it.action} | `{it.rel}{'/' if it.kind == 'dir' else ''}` | {human(it.size)} | "
                     f"{it.reason} | {dest} |")
    lines += ["", "## Totals", ""]
    for action, (c, b) in sorted(totals(items).items()):
        lines.append(f"- {action}: {c} item(s), {human(b)}")
    freed = totals(items).get(TRASH, (0, 0))[1]
    lines += [f"- **bytes freed** (to `_trash/{date}`, reclaimable once emptied): {freed} ({human(freed)})", "",
              "## Resulting layout", "", "```", f"{Path(root).name}/"]
    lines += [f"├── {n}" for n in layout(root, items)]
    lines += ["```", ""]
    return "\n".join(lines)


def print_plan(root: Path, items: list[Item]) -> None:
    shown = [it for it in items if it.action != KEEP]
    w = max([len(it.action) for it in shown] + [6])
    print(f"{'action':{w}}  {'size':>9}  path  — reason")
    for it in shown:
        dest = f"  → {it.dest}" if it.dest else ""
        print(f"{it.action:{w}}  {human(it.size):>9}  {it.rel}{'/' if it.kind == 'dir' else ''}{dest}  — {it.reason}")
    print()
    for action, (c, b) in sorted(totals(items).items()):
        print(f"[=] {action:{w}} {c:4} item(s) {human(b):>10}")
    freed = totals(items).get(TRASH, (0, 0))[1]
    print(f"[=] bytes freed (moved to _trash): {freed} ({human(freed)})")
    print(f"\nresulting layout:\n{Path(root).name}/")
    for n in layout(root, items):
        print(f"├── {n}")


# --------------------------------------------------------------------------- apply / restore
def _unique(dest: Path) -> Path:
    if not dest.exists():
        return dest
    i = 1
    while (cand := dest.with_name(f"{dest.stem}.{i}{dest.suffix}")).exists():
        i += 1
    return cand


def _move(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.rename(src, dest)
    except OSError:
        shutil.move(str(src), str(dest))


def _prune_empty(path: Path, stop: Path) -> None:
    """Remove now-empty parent folders up to (not including) stop."""
    path = path.resolve()
    stop = stop.resolve()
    while path != stop and stop in path.parents and path.is_dir() and not any(path.iterdir()):
        if path.parent == stop and path.name in PROTECTED | {"Lectures"}:
            break
        path.rmdir()
        path = path.parent


def apply(root: Path, items: list[Item], date: str, cache: HashCache | None = None) -> Path | None:
    root = Path(root).resolve()
    hc = cache or HashCache(root)
    todo = sorted((it for it in items if it.action in MOVES), key=lambda it: ORDER[it.action])
    if not todo:
        return None
    trash = root / "_trash" / date
    manifest_path = trash / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else \
        {"module": str(root), "date": date, "entries": []}
    for it in todo:
        src = root / it.rel
        if not src.exists():
            print(f"[!] gone before apply: {it.rel}")
            continue
        dest = _unique(root / (it.dest or f"_trash/{date}/{it.rel}"))
        files = [{"rel": str(f.relative_to(src)) if src.is_dir() else "", "sha256": hc.get(f), "size": f.stat().st_size}
                 for f in _files(src)]
        entry: dict[str, Any] = {"from": it.rel, "to": str(dest.relative_to(root)), "action": it.action,
                                 "kind": it.kind, "size": it.size, "reason": it.reason, "at": now()}
        if it.kind == "file":
            entry["sha256"] = files[0]["sha256"]
        else:
            entry["files"] = files
        _move(src, dest)
        _prune_empty(src.parent, root)
        manifest["entries"].append(entry)
        trash.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[+] {it.action:8} {it.rel} → {entry['to']}")
    hc.save()
    return manifest_path


def restore(root: Path, date: str) -> int:
    from .common import sha256

    root = Path(root).resolve()
    trash = root / "_trash" / date
    manifest_path = trash / "MANIFEST.json"
    if not manifest_path.exists():
        raise SystemExit(f"[-] no manifest {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    problems = 0
    for e in reversed(manifest["entries"]):
        if e.get("restored"):
            continue
        src, dest = root / e["to"], root / e["from"]
        if not src.exists():
            print(f"[-] missing {e['to']} (cannot restore {e['from']})")
            problems += 1
            continue
        if dest.exists():
            print(f"[-] {e['from']} exists again — left {e['to']} in place")
            problems += 1
            continue
        _move(src, dest)
        _prune_empty(src.parent, root)
        if e["kind"] == "file" and sha256(dest) != e.get("sha256"):
            print(f"[!] {e['from']}: sha256 differs from the manifest")
            problems += 1
        elif e["kind"] == "dir":
            bad = [f["rel"] for f in e.get("files", []) if not (dest / f["rel"]).is_file()
                   or sha256(dest / f["rel"]) != f["sha256"]]
            if bad:
                print(f"[!] {e['from']}: {len(bad)} file(s) missing or changed, e.g. {bad[:3]}")
                problems += 1
        e["restored"] = now()
        print(f"[+] restored {e['to']} → {e['from']}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    if all(e.get("restored") for e in manifest["entries"]):
        keep = root / ".mbset" / "reports" / f"tidy_restored_{date}.json"
        keep.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(manifest_path), str(keep))
        _prune_empty(trash, root)
        print(f"[+] everything from {date} restored; manifest kept at {keep.relative_to(root)}")
    return 1 if problems else 0


# --------------------------------------------------------------------------- command
def cmd_tidy(args) -> int:
    module = Module(args.module)
    if args.restore:
        return restore(module.root, args.restore)
    date = today()
    cache = HashCache(module.root)
    items = plan(module.root, args.lectures_from, placeholders=args.placeholders, cache=cache)
    print_plan(module.root, items)
    report = module.meta / "reports" / f"tidy_{date}.md"
    report.write_text(render(module.root, items, False, date), encoding="utf-8")
    print(f"\n[=] plan: {report}")
    if not args.apply:
        print("[=] dry run — nothing moved; rerun with --apply (everything goes to _trash, restorable)")
        return 0
    manifest = apply(module.root, items, date, cache)
    if manifest:
        report.write_text(render(module.root, items, True, date), encoding="utf-8")
        print(f"[+] applied; manifest {manifest} · undo: tidy {args.module!r} --restore {date}")
    else:
        print("[=] nothing to move")
    return 0


def register(sub) -> None:
    p = sub.add_parser("tidy", help="standardize the module folder layout (dry run; --apply moves to _trash)")
    p.add_argument("module", help="module folder, e.g. 'أزهر دمياط/Endocrinology'")
    p.add_argument("--apply", action="store_true", help="move items (never deletes; writes _trash/<date>/MANIFEST.json)")
    p.add_argument("--lectures-from", metavar="DIR", help="folder holding the official uploaded lecture set")
    p.add_argument("--placeholders", action="store_true",
                   help="with --apply, also trash EXCLUDED/DUPLICATE placeholder markdown")
    p.add_argument("--restore", metavar="DATE", help="move everything from _trash/<DATE> back (YYYY-MM-DD)")
    p.set_defaults(fn=cmd_tidy)
