"""`mbset.py` — one command line for the whole MBset question-bank pipeline."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .common import ARABIC, Module, dispatch_lines, dump_json, load_json, now, review_flags, safe_name

SCRIPT = "scripts/mbset.py"
SKILL_SCRIPTS = Path(__file__).resolve().parents[1]


def _mod(args) -> tuple[Module, dict[str, Any]]:
    module = Module(args.module)
    return module, module.load()


def _need_inventory(state: dict[str, Any]) -> None:
    if not state.get("sources"):
        raise SystemExit("[-] no inventory yet — run `mbset.py inventory <Module>` first")


# --------------------------------------------------------------------------- commands
def cmd_inventory(args) -> int:
    from . import inventory

    module = Module(args.module)
    state = inventory.run(module)
    print(inventory.summary(state))
    if not state.get("catalog_managed") and not (module.markdown / "00_CATALOG_OF_ALL_FILES.md").exists():
        from . import catalog
        print(f"[+] catalog skeleton: {catalog.write(module, state)}")
    return 0


def cmd_ocr(args) -> int:
    from . import ocr

    module, state = _mod(args)
    _need_inventory(state)
    return ocr.run(module, state, args.only, args.jobs, args.workers, args.force, args.all)


def cmd_profile(args) -> int:
    from .profiles import write_profile

    module, state = _mod(args)
    _need_inventory(state)
    for src in module.sources(state, args.only):
        if src.get("status") == "excluded":
            continue
        path = write_profile(module, src, force=args.force)
        if args.print:
            print(path.read_text(encoding="utf-8"))
        else:
            print(f"[+] {src['nn']} {path}")
    return 0


def cmd_parse(args) -> int:
    from .pipeline import describe, parse_source

    module, state = _mod(args)
    _need_inventory(state)
    code = 0
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing"):
            continue
        if src.get("kind") == "image" or not src.get("triage", {}).get("has_text"):
            if not module.ocr_path(src).exists():
                from . import ocr
                from .profiles import effective_profile
                print(f"[*] {src['nn']}: OCR first")
                ocr.ocr_source(module, src, effective_profile(module, src), workers=args.workers)
        try:
            res = parse_source(module, state, src, force=args.force, dry_run=args.dry_run)
        except SystemExit:
            raise
        except Exception as exc:
            code = 1
            print(f"[-] {src['nn']} {src['rel']}: {type(exc).__name__}: {exc}")
            continue
        print(("[=] " if args.dry_run else "[+] ") + describe(res))
    return code


def _show_block(text: str, n: int) -> str | None:
    m = re.search(rf"^### Q{n}:.*?(?=^### Q\d+:|\Z)", text, re.S | re.M)
    return m.group(0).split("\n---")[0].rstrip() if m else None


def cmd_show(args) -> int:
    from .writer import md_numbers_by_stem

    module, state = _mod(args)
    src = module.sources(state, args.nn)[0]
    parsed = load_json(module.parsed_path(src)) or {"questions": []}
    md = module.md_path(src)
    text = md.read_text(encoding="utf-8") if md.exists() else ""
    numbers = md_numbers_by_stem(md) if md.exists() else {}
    wanted = {int(x) for x in args.q.split(",")} if args.q else None
    shown = 0
    for r in parsed["questions"]:
        n = numbers.get(r["stem"], r["i"])
        if wanted is not None and n not in wanted:
            continue
        if args.flags and not review_flags(r["flags"]):
            continue
        block = _show_block(text, n) or f"### Q{n}: (not in markdown) {r['stem']}"
        opts = " ".join(f"{o['letter']}[b{o.get('bold', 0)} c{o.get('color', 0)} {','.join(o.get('marks', []))}]"
                        for o in r["options"])
        print(block)
        print(f"    ↳ source no. {r['number']} sec {r['section']} p{r['page'] + 1} | flags: {', '.join(r['flags']) or '-'}"
              f" | evidence: {r.get('answer_evidence') or '-'} | style: {opts}")
        if r.get("after"):
            print(f"    ↳ text after options: {r['after'][:300]}")
        print()
        shown += 1
    if args.flags:
        print(f"[=] {shown} flagged question(s) of {len(parsed['questions'])}")
        if parsed.get("gaps"):
            print(f"[!] numbering gaps: {parsed['gaps']}")
    if args.dropped:
        print("\n".join(f"  dropped: {d}" for d in parsed.get("dropped_lines", [])))
    return 0


def cmd_figures(args) -> int:
    from . import figures
    from .pipeline import refresh_hash

    module, state = _mod(args)
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing") or not module.parsed_path(src).exists():
            continue
        qs = [int(x) for x in args.q.split(",")] if args.q else None
        res = figures.run(module, src, qs)
        if res.get("cropped"):
            refresh_hash(module, state, src)
            print(f"[+] {src['nn']}: {res['cropped']} crop(s) → view {res['contact_sheet']}")
        elif res.get("skipped"):
            print(f"[=] {src['nn']}: {res['skipped']}")
    return 0


# content decisions are never cleared by `--clear-drops ocr`, whatever else their reason mentions
CONTENT_DROP = r"not (?:a )?(?:question|standalone)|explanation|lecture|note|stud(?:y|ies)|duplicate|table.of.contents|" \
               r"index|heading|placeholder|chapter|another|other subject|dermatology|pediatric|handwritten|timing"
OCR_DROP = r"\bocr\b|pars(?:er|ed)|merg|fus(?:ed|e)|garbl|unreadable|malformed|lost|shift|fragment|damag|split"


def cmd_fix(args) -> int:
    """Edit questions in place and record each decision so a re-parse re-applies it."""
    import json

    from . import overrides
    from .pipeline import refresh_hash
    from .writer import edit

    module, state = _mod(args)
    src = module.sources(state, args.nn)[0]
    from .profiles import effective_profile
    keep_ar = bool(effective_profile(module, src).get("keep_arabic"))   # Arabic sources kept by user decision
    kept_md = effective_profile(module, src).get("markdown") == "keep"  # never re-render a kept markdown
    if args.clear_drops:
        # after a better OCR / profile: drops made only because the old text was garbled must go, so the
        # questions come back on the next parse; content drops (not a question, other subject) stay
        rx = re.compile(OCR_DROP if args.clear_drops == "ocr" else args.clear_drops, re.I)
        keep = re.compile(CONTENT_DROP, re.I) if args.clear_drops == "ocr" else None
        gone = [k for k, v in src.get("overrides", {}).items() if v.get("drop") and rx.search(v["drop"])
                and (not keep or re.match(r"\W*(?:the\s+)?(?:ocr|pars)", v["drop"], re.I)
                     or not keep.search(v["drop"]))]
        for k in gone:
            entry = src["overrides"][k]
            entry.pop("drop")
            if set(entry) <= {"at"}:
                del src["overrides"][k]
        module.save(state)
        print(f"[+] {src['nn']}: {len(gone)} drop decision(s) cleared — run `parse --only {src['nn']} --force`")
        return 0
    path = module.md_path(src)
    qs = overrides.md_questions(path)
    items = list(args.answer or [])
    if args.answers:
        items += args.answers.replace(",", " ").split()
    answers: dict[int, tuple[str, str]] = {}
    for item in items:
        m = re.fullmatch(r"(\d+)=([A-Fa-f])(?::(key|marked|online|derived))?", item.strip())
        if not m:
            raise SystemExit(f"[-] answer {item!r}: use N=LETTER[:source], e.g. 12=B:marked")
        source = m.group(3) or args.source
        if not source:
            raise SystemExit(f"[-] answer {item!r}: the provenance label is required (:source or --source)")
        answers[int(m.group(1))] = (m.group(2).upper(), source)
    exps: dict[int, tuple[str, str]] = {}
    if args.exp_file:
        data = json.loads(Path(args.exp_file).read_text(encoding="utf-8"))
        for n, text in data.items():
            if text is not None and ARABIC.search(text) and not keep_ar:
                raise SystemExit(f"[-] exp Q{n}: Arabic characters")
            exps[int(n)] = (text, args.exp_source)          # null clears a wrong explanation
    texts: dict[int, dict[str, Any]] = {}
    if args.text_file:
        # {"7": {"stem": "…", "options": {"C": "…", "E": "…"}, "note": "C was lost under a pen mark"}}
        for n, fixd in json.loads(Path(args.text_file).read_text(encoding="utf-8")).items():
            blob = " ".join([fixd.get("stem") or "", *[t or "" for t in (fixd.get("options") or {}).values()]])
            if ARABIC.search(blob) and not keep_ar:
                raise SystemExit(f"[-] text Q{n}: Arabic characters")
            bad = [L for L in (fixd.get("options") or {}) if L not in "ABCDEF"]
            if bad:
                raise SystemExit(f"[-] text Q{n}: option letters must be A-F, got {bad}")
            texts[int(n)] = fixd
    images = {}
    for item in args.image or []:
        n, _, img = item.partition("=")
        images[int(n)] = img
    drop = {int(x) for x in args.drop.split(",")} if args.drop else set()
    if drop and not args.reason:
        raise SystemExit("[-] --drop needs --reason (it is logged in the catalog evidence)")
    for n in set(answers) | set(exps) | set(images) | set(texts) | drop:
        if n not in qs:
            raise SystemExit(f"[-] Q{n} does not exist in {path.name} (1..{len(qs)})")
    if args.add_file:
        # [{"after": 24, "stem": "…", "options": {"A": "…"}, "page": 5, "note": "…"}] — exact re-reads of
        # questions the parser lost; "after": markdown Q number it follows (0 = first)
        from .pipeline import parse_source
        adds = json.loads(Path(args.add_file).read_text(encoding="utf-8"))
        for a in adds:
            blob = " ".join([a.get("stem") or "", *(a.get("options") or {}).values()])
            if (ARABIC.search(blob) and not keep_ar) or not a.get("stem"):
                raise SystemExit(f"[-] add after Q{a.get('after')}: stem missing or Arabic characters")
            after = int(a.get("after") or 0)
            anchor = overrides.key_for(src, qs[after]["stem"], qs[after]["options"]) if after else ""
            src.setdefault("additions", []).append({"after": anchor, "stem": a["stem"].strip(),
                                                   "options": a.get("options") or {}, "page": a.get("page"),
                                                   "note": a.get("note"), "at": now()})
        module.save(state)
        if kept_md:
            from .writer import edit_kept
            edit_kept(path, adds=adds)
        else:
            parse_source(module, state, src, force=True)
        qs = overrides.md_questions(path)
        print(f"[+] {src['nn']}: {len(adds)} question(s) added — markdown renumbered; re-read numbers before "
              f"answering")
    if texts:
        # visual text fixes first (answers given in the same call may name a restored option);
        # the original text is kept beside the fix for audit, and the source is re-rendered
        from .pipeline import parse_source
        for n, fixd in texts.items():
            q = qs[n]
            # the answer is stored as its option's text: follow the option when its text is corrected
            prev = (src.get("overrides") or {}).get(overrides.key_for(src, q["stem"], q["options"])) or {}
            if prev.get("answer"):
                for letter, new_text in (fixd.get("options") or {}).items():
                    if new_text and overrides.norm_stem(q["options"].get(letter, "")) == overrides.norm_stem(prev["answer"]):
                        prev["answer"] = new_text
            overrides.record(src, q["stem"], q["options"], stem_fix=fixd.get("stem"), options_fix=fixd.get("options"),
                             text_note=fixd.get("note"), text_before={"stem": q["stem"], "options": q["options"]})
        module.save(state)
        if kept_md:
            from .writer import edit_kept
            edit_kept(path, texts=texts)
        else:
            parse_source(module, state, src, force=True)
        qs = overrides.md_questions(path)
    for n, (letter, source) in answers.items():
        if letter not in qs[n]["options"]:
            raise SystemExit(f"[-] Q{n}: {letter} is not among its options {sorted(qs[n]['options'])}")
        overrides.record(src, qs[n]["stem"], qs[n]["options"], answer=qs[n]["options"][letter], source=source)
    for n, (text, source) in exps.items():
        if text is None:
            overrides.record(src, qs[n]["stem"], qs[n]["options"], exp_clear=True)
        else:
            overrides.record(src, qs[n]["stem"], qs[n]["options"], exp=text, exp_source=source, exp_clear=False)
    for n, img in images.items():
        overrides.record(src, qs[n]["stem"], qs[n]["options"], image=img)
    for n in drop:
        overrides.record(src, qs[n]["stem"], qs[n]["options"], drop=args.reason)
    edit(path, answers=answers, images=images, drop=drop, exps=exps if kept_md else None)
    if exps and not kept_md:
        # re-render from the stored decisions: an MCQ explanation must not touch its Answer Source, and a
        # cleared explanation disappears
        from .pipeline import parse_source
        module.save(state)
        parse_source(module, state, src, force=True)
    if drop:
        # keep the parsed evidence in step so the counters account for the drop before a re-parse
        parsed_path = module.parsed_path(src)
        parsed = load_json(parsed_path)
        if parsed:
            ov = parsed.setdefault("overrides", {"applied": 0, "dropped": [], "stale": []})
            ov["dropped"] += [{"stem": qs[n]["stem"][:120], "reason": args.reason} for n in sorted(drop)]
            dump_json(parsed_path, parsed)
    refresh_hash(module, state, src)
    derived = sum(1 for _, s_ in answers.values() if s_ == "derived") + sum(1 for t_, s_ in exps.values() if t_ and s_ == "derived")
    print(f"[+] {src['md']}: {len(texts)} text fix(es), {len(answers)} answer(s), {len(exps)} model answer(s), {len(images)} image(s), "
          f"{len(drop)} dropped{f' · {derived} derived (report to the user)' if derived else ''}")
    return 0


def cmd_answersheet(args) -> int:
    from . import spotcheck

    module, state = _mod(args)
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing") or not module.parsed_path(src).exists():
            continue
        wanted = [int(x) for x in args.q.split(",")] if args.q else None
        outs, qs = spotcheck.answer_sheets(module, src, wanted, per=args.per)
        if outs:
            print(f"[+] {src['nn']}: {len(qs)} question(s) → view " + " ".join(str(o) for o in outs))
            print(f"    then: mbset.py fix <module> {src['nn']} --answers \"{' '.join(f'{n}=?' for n in qs[:6])} …\" "
                  f"--source marked")
    return 0


def cmd_spotcheck(args) -> int:
    from . import spotcheck

    module, state = _mod(args)
    for src in module.sources(state, args.only):
        if src.get("status") in ("excluded", "missing") or not module.parsed_path(src).exists():
            continue
        outs = spotcheck.render(module, src, args.flagged, args.n)
        print(f"[+] {src['nn']}: view " + " ".join(str(o) for o in outs))
    return 0


def cmd_review(args) -> int:
    module, state = _mod(args)
    src = module.sources(state, args.nn)[0]
    rev = src.setdefault("stages", {}).setdefault("review", {})
    if args.spot:
        rev["spot_check"] = args.spot
        rev["at"] = now()
        src["status"] = "reviewed"
    if args.note:
        rev.setdefault("notes", []).append({"note": args.note, "at": now()})
    module.save(state)
    print(f"[+] {src['nn']}: {rev}")
    return 0


def cmd_set(args) -> int:
    module, state = _mod(args)
    for src in module.sources(state, args.nn):
        tags = src.setdefault("tags", {})
        if args.tag is not None:
            tags["tag"] = args.tag
        if args.subject is not None:
            tags["tagSuggere"] = None if args.subject.lower() in ("none", "") else args.subject
        if args.year is not None:
            tags["year"] = None if str(args.year).lower() in ("none", "") else int(args.year)
        if args.tag is not None or args.subject is not None or args.year is not None or args.confirm:
            if "<" in (tags.get("tag") or ""):
                raise SystemExit(f"[-] {src['nn']}: tag still has a placeholder: {tags.get('tag')}")
            tags["confirmed"] = True
            tags["confidence"] = "confirmed"
        if args.exclude:
            src["status"] = "excluded"
            src["exclusion"] = args.exclude
        if args.include:
            src["status"] = "pending"
            src.pop("exclusion", None)
        if args.count_note:
            src["count_note"] = args.count_note
        print(f"[+] {src['nn']}: status={src.get('status')} tags={tags}")
    module.save(state)
    return 0


def cmd_renumber(args) -> int:
    """Give a duplicate NN a fresh index and carry everything that is clearly that source's with it:
    markdown, parsed/OCR evidence (sha-matched), and its figure crops `Images/<old>_*` together
    with every path that points at them (markdown, parsed JSON, stored `fix --image` decisions)."""
    from .common import text_hash

    module, state = _mod(args)
    seen: set[str] = set()
    top = max(int(s["nn"]) for s in state["sources"])
    img_ref = lambda nn: re.compile(rf"(?<![\w/])Images/{re.escape(nn)}_[^\s)\]\"'`|]+")  # noqa: E731
    for src in state["sources"]:
        if src["nn"] not in seen:
            seen.add(src["nn"])
            continue
        old = src["nn"]
        top += 1
        new = f"{top:02d}"
        old_md = module.md_path(src)
        new_md = re.sub(r"^\d+_", f"{new}_", src["md"])
        others = [s for s in state["sources"] if s is not src and s["nn"] == old]
        md_shared = any(s.get("md") == src["md"] for s in others)
        # ---- which images are this source's: linked from its own markdown / its overrides /
        # its sha-matched parsed evidence, and not linked from another source that shares the NN
        mine: set[str] = set()
        if old_md.exists() and not md_shared:
            mine |= set(img_ref(old).findall(old_md.read_text(encoding="utf-8")))
        for o in (src.get("overrides") or {}).values():
            if (o.get("image") or "").startswith(f"Images/{old}_"):
                mine.add(o["image"])
        parsed_old = module.meta / "parsed" / f"{old}.json"
        parsed = load_json(parsed_old) if parsed_old.exists() else None
        parsed_mine = bool(parsed) and parsed.get("sha256") == src.get("sha256")
        if parsed_mine:
            mine |= {r["image"] for r in parsed.get("questions", [])
                     if (r.get("image") or "").startswith(f"Images/{old}_")}
        theirs: set[str] = set()
        for s in others:
            p = module.md_path(s)
            if p.exists():
                theirs |= set(img_ref(old).findall(p.read_text(encoding="utf-8")))
            theirs |= {o["image"] for o in (s.get("overrides") or {}).values() if o.get("image")}
        clash = sorted(mine & theirs)
        if clash:
            print(f"[!] {old}: image(s) linked by both sources, left in place — relink by hand: {clash}")
        moves: dict[str, str] = {}
        for rel in sorted(mine - theirs):
            target = f"Images/{new}_" + rel[len(f"Images/{old}_"):]
            a, b = module.root / rel, module.root / target
            if b.exists():
                print(f"[!] {old}: {target} already exists — {rel} not moved")
                continue
            if a.exists():
                a.rename(b)
            moves[rel] = target

        def swap(path: str | None) -> str | None:
            return moves.get(path, path) if path else path

        # ---- evidence files (shared files belong to the first owner of the NN)
        for folder in ("parsed", "ocr"):
            p = module.meta / folder / f"{old}.json"
            data = parsed if folder == "parsed" else (load_json(p) if p.exists() else None)
            if not data or data.get("sha256") != src.get("sha256"):
                continue
            if folder == "parsed":
                for r in data.get("questions", []):
                    if r.get("image"):
                        r["image"] = swap(r["image"])
            dump_json(module.meta / folder / f"{new}.json", data)
            p.unlink()
        for o in (src.get("overrides") or {}).values():
            if o.get("image"):
                o["image"] = swap(o["image"])
        # ---- markdown
        if old_md.exists() and not md_shared:
            text = old_md.read_text(encoding="utf-8")
            if moves:
                text = img_ref(old).sub(lambda m: moves.get(m.group(0), m.group(0)), text)
            (module.markdown / new_md).write_text(text, encoding="utf-8")
            if old_md != module.markdown / new_md:
                old_md.unlink()
            parse_stage = src.get("stages", {}).get("parse")
            if parse_stage and parse_stage.get("md_hash"):
                parse_stage["md_hash"] = text_hash(text)
        elif md_shared:
            print(f"[!] {old}: markdown {src['md']} is shared with another source — not moved; re-parse {new}")
        print(f"[+] {old} → {new}: {src['md']} → {new_md}"
              + (f" · {len(moves)} image(s) renamed" if moves else ""))
        src["nn"], src["md"] = new, new_md
    state["duplicate_nn"] = []
    state["sources"].sort(key=lambda s: s["nn"])
    module.save(state)
    return 0


def _grouped(items: list[str]) -> list[str]:
    """'04 x.md: Q7: Answer Source none' ×9 → '04: Answer Source none ×9 (Q1,Q2,…)'."""
    groups: dict[tuple[str, str], list[str]] = {}
    for it in items:
        m = re.match(r"(\d+)(?: [^:]+\.md)?: (?:(Q\d+): )?(.*)", it)
        if not m:
            groups.setdefault(("", it), [])
            continue
        nn, q, what = m.groups()
        what = re.sub(r"\b(?:Correct [A-F?] not among options)", "Correct not among options", what)
        what = re.sub(r"options not sequential \[.*?\]", "options not sequential", what)
        what = re.sub(r"Images/\S+", "…", what)
        groups.setdefault((nn, what), []).append(q or "")
    out = []
    for (nn, what), qs in groups.items():
        qs = [q for q in qs if q]
        tail = f" ×{len(qs)} ({','.join(qs[:6])}{',…' if len(qs) > 6 else ''})" if len(qs) > 1 else (f" ({qs[0]})" if qs else "")
        out.append(f"{nn + ': ' if nn else ''}{what}{tail}")
    return out


def cmd_check(args) -> int:
    from . import check

    module, state = _mod(args)
    _need_inventory(state)
    res = check.check_module(module, state, args.only)
    report = check.write_report(module, res)
    for nn, r in res["per_source"].items():
        i = r["info"]
        if i.get("excluded"):
            continue
        mark = "FAIL" if r["hard"] else ("review" if r["review"] else "OK")
        print(f"  {nn} {mark:6} Q={i.get('questions', 0):<4} MCQ={i.get('mcq', 0):<4} "
              f"{i.get('sources', '')} {i.get('distribution', '')}")
    print(f"\n[{'-' if res['hard'] else '+'}] hard failures: {len(res['hard'])}")
    if args.all:
        for h in res["hard"]:
            print(f"    - {h}")
    else:
        for line in _grouped(res["hard"]):
            print(f"    - {line}")
    print(f"[!] review items: {len(res['review'])}")
    if not args.quiet:
        for line in (res["review"] if args.all else _grouped(res["review"])):
            print(f"    - {line}")
    print(f"[=] report: {report}")
    if args.json:
        Path(args.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if res["hard"] else 0


def cmd_catalog(args) -> int:
    from . import catalog

    module, state = _mod(args)
    print(f"[+] {catalog.write(module, state)}")
    print(f"[+] {catalog.tag_map(module, state)}")
    return 0


def cmd_packets(args) -> int:
    """Work packets for parallel workers, plus one self-contained worker brief per packet
    (`.mbset/packets/packet_k_brief.txt`; dispatch: references/parallel-workflow.md)."""
    from . import catalog

    module, state = _mod(args)
    script = str(SKILL_SCRIPTS / "mbset.py")
    for p in catalog.packets(module, state, args.n, script):
        print(f"[+] {p}")
    bins, load = catalog.packet_groups(state, args.n)
    repo = catalog.repo_root(module.root)
    for k, (group, pages) in enumerate(zip(bins, load), 1):   # same k as packet_k.md
        if not group:
            continue
        brief = module.meta / "packets" / f"packet_{k}_brief.txt"
        brief.write_text(catalog.packet_brief(module, k, len(bins), group, pages, script, repo), encoding="utf-8")
        print(f"[+] {brief}")
        print("\n".join(dispatch_lines([str(brief)], repo, "max", getattr(args, "dispatch", None))[-1:]))
    return 0


def cmd_lock(args) -> int:
    from . import catalog

    module, _ = _mod(args)
    nns = args.nns.split(",")
    if args.release:
        catalog.unlock(module, nns)
        print(f"[+] released {nns}")
        return 0
    taken = catalog.lock(module, nns, args.owner or f"{os.getenv('USER', 'agent')}:{os.getpid()}")
    if taken:
        print(f"[-] already locked: {taken}")
        return 1
    print(f"[+] locked {nns}")
    return 0


def cmd_build(args) -> int:
    from . import catalog, check

    module, state = _mod(args)
    res = check.check_module(module, state)
    if res["hard"] and not args.skip_check:
        print(f"[-] {len(res['hard'])} hard failure(s) — run `mbset.py check`; the Excel is not built")
        return 1
    cid, cname = args.category_id, args.category_name
    if not cid:
        cid, cname2 = catalog.category(module, state)
        cname = cname or cname2
    if not cid or not cname:
        print("[-] categoryId/categoryName unknown — pass --category-id/--category-name "
              "(from the platform subcategories export)")
        return 1
    state["category_id"], state["category_name"] = cid, cname
    module.save(state)
    catalog.write(module, state)
    tags = catalog.tag_map(module, state)
    out = args.out or str(catalog.excel_path(module))
    py = sys.executable
    # only the sources that are in the bank: excluded ones keep their markdown (placeholder or parser
    # output) in Markdown_Questions for the audit trail, but never reach the Excel
    import shutil
    import tempfile
    stage = Path(tempfile.mkdtemp(prefix="mbset_build_"))
    from .profiles import effective_profile
    keep_ar = any(effective_profile(module, s).get("keep_arabic") for s in state["sources"]
                  if s.get("status") not in ("excluded", "missing"))
    for src in state["sources"]:
        md = module.md_path(src)
        if src.get("status") not in ("excluded", "missing") and md.exists():
            shutil.copy(md, stage / md.name)
    steps = [
        [py, str(SKILL_SCRIPTS / "build_module_template.py"), "--markdown", str(stage),
         "--tag-map", str(tags), "--category-id", cid, "--category-name", cname, "--out", out],
        [py, str(SKILL_SCRIPTS / "validate_questions_excel.py"), out],
        [py, str(SKILL_SCRIPTS / "audit_question_bank.py"), "--excel", out, "--by-tag"],
    ]
    if keep_ar:      # Arabic sources kept in Arabic by user decision; `check` still gates every other source
        steps[1].append("--allow-arabic")
        steps[2].append("--allow-arabic")
    for step in steps:
        print(f"[*] {' '.join(Path(step[1]).name if i == 1 else s for i, s in enumerate(step[1:], 1))}")
        rc = subprocess.run(step).returncode
        if rc:
            print(f"[-] {Path(step[1]).name} failed (exit {rc})")
            return rc
    print(f"[+] {out} built and gated")
    return 0


def cmd_status(args) -> int:
    module, state = _mod(args)
    _need_inventory(state)
    counts: dict[str, int] = {}
    for s in state["sources"]:
        counts[s.get("status", "pending")] = counts.get(s.get("status", "pending"), 0) + 1
    print(f"{module.name}: {len(state['sources'])} sources · " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for s in state["sources"]:
        st = s.get("stages", {})
        p = st.get("parse", {})
        o = st.get("ocr", {})
        r = st.get("review", {})
        lock = (module.meta / "locks" / f"{s['nn']}.lock")
        print(f"  {s['nn']} {s.get('status', 'pending'):9} {s.get('triage', {}).get('class', '?'):18} "
              f"{str(s.get('pages') or ''):>3}p "
              f"{'ocr✓ ' if o.get('status') == 'done' else ''}"
              f"{('Q=' + str(p.get('questions')) + ' ans=' + str(p.get('answered')) + '/' + str(p.get('mcq'))) if p else ''}"
              f"{' spot=' + r['spot_check'] if r.get('spot_check') else ''}"
              f"{' 🔒' if lock.exists() else ''}  {Path(s['rel']).name[:50]}"
              f"{'  — ' + s['exclusion'] if s.get('exclusion') else ''}")
    return 0


def cmd_run(args) -> int:
    """Everything mechanical in one go: inventory → OCR → profiles → parse → check."""
    from . import inventory, ocr
    from .pipeline import describe, parse_source

    module = Module(args.module)
    state = inventory.run(module)
    print(inventory.summary(state))
    ocr.run(module, state, None, args.jobs, args.workers, False, False)
    for src in state["sources"]:
        if src.get("status") in ("excluded", "missing"):
            continue
        try:
            print("[+] " + describe(parse_source(module, state, src, force=False)))
        except Exception as exc:
            print(f"[-] {src['nn']} {src['rel']}: {type(exc).__name__}: {exc}")
    args.only, args.json, args.all, args.quiet = None, None, False, True
    return cmd_check(args)


# --------------------------------------------------------------------------- parser
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="mbset.py", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_, only=True):
        p = sub.add_parser(name, help=help_)
        p.add_argument("module", help="module folder, e.g. 'أزهر دمياط/Endocrinology'")
        if only:
            p.add_argument("--only", help="comma-separated NN / filenames")
        p.set_defaults(fn=fn)
        return p

    add("inventory", cmd_inventory, "Stage 0: archives, hashes, dedupe, triage, catalog skeleton", only=False)
    p = add("ocr", cmd_ocr, "Stage 0.5: OCR every scanned source (cached)")
    p.add_argument("--jobs", type=int, default=2, help="files in parallel")
    p.add_argument("--workers", type=int, default=4, help="pages in parallel per file")
    p.add_argument("--force", action="store_true")
    p.add_argument("--all", action="store_true", help="OCR sources with a text layer too")
    p = add("profile", cmd_profile, "write suggested parser profiles")
    p.add_argument("--force", action="store_true")
    p.add_argument("--print", action="store_true")
    p = add("parse", cmd_parse, "Stage 1+2: profile → markdown with answers and flags")
    p.add_argument("--force", action="store_true", help="replace a hand-edited markdown (backup kept)")
    p.add_argument("--dry-run", action="store_true", help="report counts without writing")
    p.add_argument("--workers", type=int, default=4)
    p = sub.add_parser("show", help="print questions (only flagged ones with --flags) with evidence")
    p.add_argument("module"); p.add_argument("nn")
    p.add_argument("--flags", action="store_true"); p.add_argument("--q"); p.add_argument("--dropped", action="store_true")
    p.set_defaults(fn=cmd_show)
    p = add("figures", cmd_figures, "crop figures for figure-dependent questions + contact sheet")
    p.add_argument("--q", help="markdown question numbers to crop (default: flagged figure questions)")
    p = sub.add_parser("fix", help="edit single questions in place without retyping")
    p.add_argument("module"); p.add_argument("nn")
    p.add_argument("--answer", action="append", help="N=LETTER:source (source: key|marked|online|derived)")
    p.add_argument("--answers", help='batch: "1=A 2=C 7=B" (use with --source, or N=L:source each)')
    p.add_argument("--source", choices=["key", "marked", "online", "derived"], help="provenance for --answers")
    p.add_argument("--exp-file", "--model-file", dest="exp_file",
                   help="JSON {\"N\": \"model answer\"} for written questions (→ **Model Answer:** / ModelAnswer column)")
    p.add_argument("--exp-source", default="derived", choices=["key", "derived"],
                   help="where the model answers came from (default derived → reported to the user)")
    p.add_argument("--image", action="append", help="N=Images/NN_QN.png")
    p.add_argument("--drop", help="comma-separated question numbers to remove")
    p.add_argument("--reason")
    p.add_argument("--text-file", help='JSON {"N": {"stem": "…", "options": {"C": "…"}, "note": "…"}}: '
                   'text re-read from the page image (exact wording, never paraphrased); null removes an option')
    p.add_argument("--add-file", help='JSON list [{"after": N, "stem": "…", "options": {"A": "…"}, "page": P, '
                   '"note": "…"}]: a question the parser lost, re-read exactly from the page')
    p.add_argument("--clear-drops", metavar="REGEX|ocr",
                   help="remove drop decisions whose reason matches (`ocr` = drops caused by bad OCR/parsing)")
    p.set_defaults(fn=cmd_fix)
    p = add("spotcheck", cmd_spotcheck, "source-vs-markdown sheets for max(5,10%%) sampled questions")
    p.add_argument("--flagged", action="store_true", help="include flagged questions in the sample")
    p.add_argument("--n", type=int)
    p = add("answersheet", cmd_answersheet, "crops of unanswered MCQs (6 per sheet) for a batch visual answer pass")
    p.add_argument("--q", help="markdown question numbers (default: every MCQ without an answer)")
    p.add_argument("--per", type=int, default=6)
    p = sub.add_parser("review", help="record the spot-check verdict")
    p.add_argument("module"); p.add_argument("nn"); p.add_argument("--spot"); p.add_argument("--note")
    p.set_defaults(fn=cmd_review)
    p = sub.add_parser("set", help="confirm tags, exclude/include a source, annotate counts")
    p.add_argument("module"); p.add_argument("nn", help="NN or comma list")
    p.add_argument("--tag"); p.add_argument("--subject"); p.add_argument("--year", help="integer, or `none` when the source gives no year")
    p.add_argument("--confirm", action="store_true", help="accept the suggested tag as is")
    p.add_argument("--exclude", metavar="REASON"); p.add_argument("--include", action="store_true")
    p.add_argument("--count-note", help="explain an accepted counter mismatch")
    p.set_defaults(fn=cmd_set)
    add("renumber", cmd_renumber, "give duplicate NN a fresh index and rename their markdown", only=False)
    p = add("check", cmd_check, "Stage 2+3 gate: problems only; exit 1 on hard failures")
    p.add_argument("--json"); p.add_argument("--all", action="store_true"); p.add_argument("--quiet", action="store_true")
    add("catalog", cmd_catalog, "regenerate 00_CATALOG_OF_ALL_FILES.md and tag_map.json from state", only=False)
    p = add("packets", cmd_packets, "split pending sources into N balanced packets for parallel agents", only=False)
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--dispatch", help="worker command chosen by the user, with {brief} {repo} {effort}")
    p = sub.add_parser("lock", help="claim (or --release) sources for one agent")
    p.add_argument("module"); p.add_argument("nns"); p.add_argument("--owner"); p.add_argument("--release", action="store_true")
    p.set_defaults(fn=cmd_lock)
    p = add("build", cmd_build, "Stage 4: check → catalog → Excel → validate → audit", only=False)
    p.add_argument("--category-id"); p.add_argument("--category-name"); p.add_argument("--out")
    p.add_argument("--skip-check", action="store_true", help="build even with hard failures (never for upload)")
    add("status", cmd_status, "one line per source", only=False)
    p = add("run", cmd_run, "inventory → OCR → parse → check in one go", only=False)
    p.add_argument("--jobs", type=int, default=2); p.add_argument("--workers", type=int, default=4)
    from . import crossdup, doctor, lectures, report, tidy, transcribe, worklist
    for extra in (tidy, report, doctor, crossdup, lectures, worklist, transcribe):
        extra.register(sub)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args) or 0
