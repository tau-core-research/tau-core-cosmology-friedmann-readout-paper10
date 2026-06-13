#!/usr/bin/env python3
from __future__ import annotations

import os
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "paper10_submission_source"
OUT = ROOT / "arxiv_submission_source.zip"
GENERATED_MANUSCRIPT_PDFS = {
    "main.pdf",
    "supplement_route_ledgers.pdf",
}

EXCLUDE_SUFFIXES = {
    ".aux",
    ".bbl",
    ".blg",
    ".bcf",
    ".log",
    ".out",
    ".run.xml",
    ".toc",
    ".xdv",
    ".fls",
    ".fdb_latexmk",
}


def main() -> None:
    if OUT.exists():
        OUT.unlink()
    files = []
    for path in sorted(SOURCE.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.relative_to(SOURCE).parts):
            continue
        if path.name in GENERATED_MANUSCRIPT_PDFS:
            continue
        if path.suffix in EXCLUDE_SUFFIXES:
            continue
        files.append(path)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(str(path.relative_to(SOURCE)))
            info.date_time = (2026, 6, 8, 0, 0, 0)
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    print(f"built {OUT} with {len(files)} files")


if __name__ == "__main__":
    main()
