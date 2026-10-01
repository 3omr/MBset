"""`mbset.py init` — first-run setup of the skill for one person (SKILL.md §0).

The agent asks the user (faculty and its tag system, who runs the briefs, Telegram, reply language), then
saves the answers with flags; a person at a terminal can run `init` alone and answer the prompts.

    mbset.py init --show                       # current settings, or NOT INITIALIZED
    mbset.py init --list                       # faculties with a ready tag taxonomy
    mbset.py init --test "Final 2023.pdf" …    # the tag each filename would get under a taxonomy
    mbset.py init --university Damietta --worker "Claude subagents" --telegram no --language ar
    mbset.py init --university "Mansoura" --taxonomy-file mansoura.yaml …   # a faculty not built in

Settings go to `~/.config/mbset/config.yaml`; a new faculty's taxonomy to
`~/.config/mbset/taxonomies/<name>.yaml`. Nothing is written into modules or the repository.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

from .common import CONFIG_FILE, load_config, now, save_config
from . import taxonomy

FIELDS = ("university", "worker", "dispatch", "telegram", "language")


def show(cfg: dict[str, Any]) -> None:
    if not cfg:
        print("NOT INITIALIZED — run first-run setup (SKILL.md §0): ask the user, then `mbset.py init --university …`")
        return
    print(f"settings ({CONFIG_FILE}):")
    for k in FIELDS + ("initialized",):
        if cfg.get(k) not in (None, ""):
            print(f"  {k}: {cfg[k]}")
    tax = taxonomy.load(cfg.get("university"))
    print(f"  taxonomy: {tax['name']} — {tax.get('description', '')}")


def list_taxonomies() -> None:
    for name, f in taxonomy.available().items():
        tax = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        where = "yours" if f.parent == taxonomy.USER else "built-in"
        print(f"  {tax.get('name', name):<12} {where:<9} {tax.get('description', '')}")
        for r in tax.get("rules") or []:
            print(f"      {r.get('match') or 'has ' + str(r.get('has')):<22} → {r['tag']}")
        print(f"      {'(otherwise)':<22} → {(tax.get('default') or {}).get('tag')}"
              + (f"   · no year: {', '.join(tax['year_free'])}" if tax.get("year_free") else ""))


def test(tax: dict[str, Any], names: list[str]) -> None:
    for n in names:
        s = taxonomy.suggest(tax, n if "/" in n else f"Raw_PDF_Questions/{n}")
        extra = " (needs a year: not in the filename)" if s["needs_year"] else ""
        print(f"  {n:<45} → {s['tag']}   [tagSuggere: {s['tagSuggere']}]{extra}")


def install_taxonomy(path: Path, name: str) -> str:
    tax = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    tax["name"] = tax.get("name") or name
    errs = taxonomy.validate(tax)
    if errs:
        raise SystemExit("[-] taxonomy not saved:\n    " + "\n    ".join(errs))
    taxonomy.USER.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", tax["name"].lower()).strip("-") or "faculty"
    out = taxonomy.USER / f"{slug}.yaml"
    out.write_text(yaml.safe_dump(tax, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"[+] taxonomy saved: {out}")
    return slug


def interactive(cfg: dict[str, Any]) -> dict[str, Any]:
    print("mbset first-run setup (answers are saved in ~/.config/mbset/config.yaml)\n")
    names = list(taxonomy.available())
    list_taxonomies()
    uni = input(f"\nYour faculty [{'/'.join(names)}, or a new name] ({cfg.get('university') or 'damietta'}): ").strip()
    cfg["university"] = uni or cfg.get("university") or "Damietta"
    if cfg["university"].lower() not in names:
        print(f"'{cfg['university']}' has no taxonomy yet: the generic one is used until your agent writes one "
              f"with you (`init --taxonomy-file`).")
    cfg["worker"] = input("Who runs transcription/review briefs [Claude subagents / Codex / Antigravity / none]: ").strip() \
        or cfg.get("worker") or "Claude subagents"
    cfg["telegram"] = (input("Download sources from Telegram? [y/N]: ").strip().lower() or "n").startswith("y")
    cfg["language"] = input("Reply language [ar/en] (ar): ").strip() or cfg.get("language") or "ar"
    return cfg


def cmd_init(args) -> int:
    cfg = load_config()
    if args.list:
        list_taxonomies()
        return 0
    if args.test:
        test(taxonomy.load(args.university or cfg.get("university")), args.test)
        return 0
    given = {k: getattr(args, k) for k in FIELDS if getattr(args, k) is not None}
    if args.show or (not given and not args.taxonomy_file and not sys.stdin.isatty()):
        show(cfg)
        return 0
    if args.taxonomy_file:
        given["university"] = install_taxonomy(Path(args.taxonomy_file), given.get("university") or "faculty")
    if given:
        if "telegram" in given:
            given["telegram"] = str(given["telegram"]).lower() in ("y", "yes", "true", "1")
        cfg.update(given)
    else:
        cfg = interactive(cfg)
    cfg["initialized"] = cfg.get("initialized") or now()[:10]
    save_config(cfg)
    print(f"[+] saved {CONFIG_FILE}")
    show(cfg)
    return 0


def register(sub) -> None:
    p = sub.add_parser("init", help="first-run setup: faculty & tag taxonomy, worker, Telegram, language")
    p.add_argument("--show", action="store_true", help="print the current settings (NOT INITIALIZED if none)")
    p.add_argument("--list", action="store_true", help="faculties with a ready tag taxonomy, and their rules")
    p.add_argument("--test", nargs="+", metavar="FILENAME", help="the tag these filenames would get")
    p.add_argument("--university", help="faculty / taxonomy name (built-in: Damietta, Assiut, Generic)")
    p.add_argument("--taxonomy-file", help="YAML taxonomy for a faculty that is not built in (see taxonomy.py)")
    p.add_argument("--worker", help="who runs briefs: Claude subagents / a delegate CLI name / none")
    p.add_argument("--dispatch", help="worker command with {brief} {repo} {effort} (delegate CLIs)")
    p.add_argument("--telegram", help="yes / no")
    p.add_argument("--language", help="reply language, e.g. ar or en")
    p.set_defaults(fn=cmd_init)
