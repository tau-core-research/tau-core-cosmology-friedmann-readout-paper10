#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_paper10_desi_clock_support_blocker_external_review_response_v1.py"
CANONICAL_RESPONSE = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_response_v1.csv"
CANONICAL_COMPLETED_SUMMARY = (
    ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_completed_summary_v1.csv"
)
CANONICAL_SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_response_v1_summary.csv"
CANONICAL_NOTES = ROOT / "docs/paper10_desi_clock_support_blocker_external_review_notes_v1.md"
CANONICAL_LOG = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_validation_log_v1.txt"

ZIP_RESPONSE = "paper10_desi_clock_support_blocker_external_review_response_v1.csv"
ZIP_COMPLETED_SUMMARY = "paper10_desi_clock_support_blocker_external_review_completed_summary_v1.csv"
ZIP_NOTES = "paper10_desi_clock_support_blocker_external_review_notes_v1.md"
ZIP_LOG = "paper10_desi_clock_support_blocker_external_review_validation_log_v1.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import a completed DESI clock-support blocker external review ZIP after validation succeeds."
    )
    parser.add_argument("completed_review_zip", help="Path to completed reviewer response ZIP.")
    return parser.parse_args()


def run_validator(response: Path, completed_summary: Path, summary_out: Path) -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR.relative_to(ROOT)),
            str(response),
            "--completed-summary",
            str(completed_summary),
            "--summary-out",
            str(summary_out),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "validator rejected response").strip()
        raise SystemExit(f"response validation failed; canonical artifacts were not modified: {detail}")


def main() -> None:
    args = parse_args()
    package = Path(args.completed_review_zip).expanduser()
    if not package.is_absolute():
        package = (Path.cwd() / package).resolve()
    if not package.exists():
        raise SystemExit(f"completed review ZIP does not exist: {package}")
    if package.suffix.lower() != ".zip":
        raise SystemExit(f"completed review must be a ZIP: {package}")

    with tempfile.TemporaryDirectory(prefix="desi_clock_blocker_review_import_") as tmp:
        tmpdir = Path(tmp)
        with zipfile.ZipFile(package) as zf:
            names = set(zf.namelist())
            required = {ZIP_RESPONSE, ZIP_COMPLETED_SUMMARY, ZIP_NOTES, ZIP_LOG}
            missing = required - names
            if missing:
                raise SystemExit(f"completed review ZIP missing required files: {sorted(missing)}")
            zf.extract(ZIP_RESPONSE, tmpdir)
            zf.extract(ZIP_COMPLETED_SUMMARY, tmpdir)
            zf.extract(ZIP_NOTES, tmpdir)
            zf.extract(ZIP_LOG, tmpdir)

        response = tmpdir / ZIP_RESPONSE
        completed_summary = tmpdir / ZIP_COMPLETED_SUMMARY
        notes = tmpdir / ZIP_NOTES
        log = tmpdir / ZIP_LOG
        validated_summary = tmpdir / "validated_summary.csv"
        run_validator(response, completed_summary, validated_summary)

        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        CANONICAL_NOTES.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        shutil.copy2(completed_summary, CANONICAL_COMPLETED_SUMMARY)
        shutil.copy2(validated_summary, CANONICAL_SUMMARY)
        shutil.copy2(notes, CANONICAL_NOTES)
        shutil.copy2(log, CANONICAL_LOG)

    print(
        "PAPER10_DESI_CLOCK_SUPPORT_BLOCKER_EXTERNAL_REVIEW_RESPONSE_IMPORTED "
        f"response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
