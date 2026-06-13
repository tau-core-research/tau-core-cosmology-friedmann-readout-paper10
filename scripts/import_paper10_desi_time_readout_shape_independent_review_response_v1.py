#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_RESPONSE = (
    ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_v1.csv"
)
CANONICAL_SUMMARY = (
    ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_v1_summary.csv"
)
VALIDATOR = ROOT / "scripts/validate_paper10_desi_time_readout_shape_independent_review_response_v1.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import a completed external DESI time-readout shape independent review "
            "response only after validation succeeds."
        )
    )
    parser.add_argument("response_csv", help="Path to completed reviewer response CSV.")
    return parser.parse_args()


def run_validator(response: Path, summary: Path) -> None:
    result = subprocess.run(
        [
            "python",
            str(VALIDATOR.relative_to(ROOT)),
            str(response),
            "--summary-out",
            str(summary),
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
    response = Path(args.response_csv).expanduser()
    if not response.is_absolute():
        response = (Path.cwd() / response).resolve()
    if not response.exists():
        raise SystemExit(f"response CSV does not exist: {response}")
    if response.suffix.lower() != ".csv":
        raise SystemExit(f"response must be a CSV file: {response}")

    with tempfile.TemporaryDirectory(prefix="desi_shape_review_import_") as tmp:
        tmp_summary = Path(tmp) / "validated_summary.csv"
        run_validator(response, tmp_summary)
        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        shutil.copy2(tmp_summary, CANONICAL_SUMMARY)

    print(
        "PAPER10_DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_RESPONSE_IMPORTED "
        f"response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
