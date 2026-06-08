#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper10_submission_source" / "main.tex"


def run(cmd: list[str], cwd: Path = ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1780876800")
    print("+ tectonic paper10_submission_source/main.tex")
    subprocess.run(["tectonic", PAPER.name], cwd=PAPER.parent, env=env, check=True)
    run(["python", "scripts/validate_source_freeze.py"])
    run(["python", "scripts/build_arxiv_source.py"])
    run(["python", "-m", "pytest", "-q"])
    print("PAPER10_REPRODUCTION_COMPLETE")


if __name__ == "__main__":
    main()
