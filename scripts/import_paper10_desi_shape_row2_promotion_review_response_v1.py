#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_paper10_desi_shape_row2_promotion_review_response_v1.py"
CANONICAL_RESPONSE = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_response_v1_summary.csv"
CANONICAL_NOTES = ROOT / "docs/paper10_desi_shape_row2_promotion_review_notes_v1.md"
CANONICAL_LOG = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_validation_log_v1.txt"

ZIP_RESPONSE = "paper10_desi_shape_row2_promotion_review_response_v1.csv"
ZIP_TEMPLATE_RESPONSE = "paper10_desi_shape_row2_promotion_review_response_template_v1.csv"
ZIP_NOTES = "paper10_desi_shape_row2_promotion_review_notes_v1.md"
ZIP_LOG = "paper10_desi_shape_row2_promotion_review_validation_log_v1.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import a completed Row2 promotion-review ZIP after validation succeeds.")
    parser.add_argument("completed_review_zip", help="Path to completed reviewer response ZIP.")
    return parser.parse_args()


def run_validator(response: Path, summary_out: Path) -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR.relative_to(ROOT)), str(response), "--summary-out", str(summary_out)],
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

    with tempfile.TemporaryDirectory(prefix="desi_row2_promotion_review_import_") as tmp:
        tmpdir = Path(tmp)
        with zipfile.ZipFile(package) as zf:
            names = set(zf.namelist())
            response_name = ZIP_RESPONSE if ZIP_RESPONSE in names else ZIP_TEMPLATE_RESPONSE
            if response_name not in names:
                raise SystemExit(
                    "completed review ZIP missing response CSV: "
                    f"expected {ZIP_RESPONSE} or {ZIP_TEMPLATE_RESPONSE}"
                )
            zf.extract(response_name, tmpdir)
            response = tmpdir / response_name
            notes = None
            log = None
            if ZIP_NOTES in names:
                zf.extract(ZIP_NOTES, tmpdir)
                notes = tmpdir / ZIP_NOTES
            if ZIP_LOG in names:
                zf.extract(ZIP_LOG, tmpdir)
                log = tmpdir / ZIP_LOG

        validated_summary = tmpdir / "validated_summary.csv"
        run_validator(response, validated_summary)

        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        CANONICAL_NOTES.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        run_validator(CANONICAL_RESPONSE, CANONICAL_SUMMARY)
        if notes is not None:
            shutil.copy2(notes, CANONICAL_NOTES)
        else:
            CANONICAL_NOTES.write_text(
                "# Paper10 DESI Shape Row2 Promotion Review Notes\n\n"
                "No separate notes file was included in the completed reviewer ZIP.\n"
            )
        if log is not None:
            shutil.copy2(log, CANONICAL_LOG)
        else:
            CANONICAL_LOG.write_text("No separate validation log was included in the completed reviewer ZIP.\n")

    print(
        "PAPER10_DESI_SHAPE_ROW2_PROMOTION_REVIEW_RESPONSE_IMPORTED "
        f"response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
