#!/usr/bin/env python3
"""MBset question-bank pipeline — one command line for Stages 0-4.

    python mbset.py run        <Module>        # inventory → OCR → parse → check (mechanical part)
    python mbset.py inventory  <Module>        # Stage 0
    python mbset.py ocr        <Module>        # Stage 0.5 (cached, parallel)
    python mbset.py parse      <Module> [--only NN]
    python mbset.py show       <Module> NN --flags
    python mbset.py fix        <Module> NN --answer 12=B:marked --drop 7 --reason "..."
    python mbset.py figures    <Module> [--only NN]
    python mbset.py spotcheck  <Module> [--only NN]
    python mbset.py review     <Module> NN --spot "6/6 OK"
    python mbset.py check      <Module> [--only NN]
    python mbset.py packets    <Module> --n 4
    python mbset.py build      <Module>
    python mbset.py status     <Module>

See ../SKILL.md and ../references/pipeline-v2.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mbset.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
