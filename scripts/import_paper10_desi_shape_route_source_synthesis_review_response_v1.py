#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_paper10_desi_shape_route_source_synthesis_review_response_v1.py"
CANONICAL_RESPONSE = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_response_v1_summary.csv"
CANONICAL_COMPLETED = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_completed_summary_v1.csv"
CANONICAL_NOTES = ROOT / "docs/paper10_desi_shape_route_source_synthesis_review_notes_v1.md"
CANONICAL_LOG = ROOT / "data/derived/paper10_desi_shape_route_source_synthesis_review_validation_log_v1.txt"

ZIP_RESPONSE = "paper10_desi_shape_route_source_synthesis_review_response_v1.csv"
ZIP_COMPLETED = "paper10_desi_shape_route_source_synthesis_review_completed_summary_v1.csv"
ZIP_NOTES = "paper10_desi_shape_route_source_synthesis_review_notes_v1.md"
ZIP_LOG = "paper10_desi_shape_route_source_synthesis_review_validation_log_v1.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a completed DESI shape-route source-synthesis review ZIP after validation succeeds."
    )
    parser.add_argument("zip_path")
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def require_member(names: set[str], member: str) -> None:
    if member not in names:
        raise SystemExit(f"completed review zip is missing {member}")


def main() -> None:
    args = parse_args()
    zip_path = resolve(args.zip_path)
    if not zip_path.exists():
        raise SystemExit(f"missing zip: {zip_path}")
    with tempfile.TemporaryDirectory(prefix="desi_shape_route_source_synthesis_review_import_") as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
            for member in [ZIP_RESPONSE, ZIP_COMPLETED, ZIP_NOTES, ZIP_LOG]:
                require_member(names, member)
            zf.extractall(tmp_path)
        response = tmp_path / ZIP_RESPONSE
        summary = tmp_path / "validated_summary.csv"
        subprocess.run(
            ["python", str(VALIDATOR), str(response), "--summary-out", str(summary)],
            cwd=ROOT,
            check=True,
        )
        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        CANONICAL_NOTES.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        shutil.copy2(tmp_path / ZIP_COMPLETED, CANONICAL_COMPLETED)
        shutil.copy2(tmp_path / ZIP_NOTES, CANONICAL_NOTES)
        shutil.copy2(tmp_path / ZIP_LOG, CANONICAL_LOG)
    subprocess.run(["python", str(VALIDATOR)], cwd=ROOT, check=True)
    print(f"imported {zip_path} into canonical DESI shape-route source-synthesis review artifacts")


if __name__ == "__main__":
    main()
