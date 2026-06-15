#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_RESPONSE = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_v1_summary.csv"
VALIDATOR = ROOT / "scripts/validate_joint_row_level_aligned_control_value_authorization_response_v1.py"
EXPECTED_RESPONSE_NAME = "joint_row_level_aligned_control_value_authorization_response_v1.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import completed aligned-control value authorization response CSV or zip.")
    parser.add_argument("response", help="Path to completed response CSV or zip.")
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find_response_in_zip(zip_path: Path, tmp_dir: Path) -> Path:
    with zipfile.ZipFile(zip_path) as zf:
        names = [name for name in zf.namelist() if Path(name).name == EXPECTED_RESPONSE_NAME]
        if len(names) != 1:
            raise SystemExit(f"zip must contain exactly one {EXPECTED_RESPONSE_NAME}; found {zf.namelist()}")
        zf.extract(names[0], tmp_dir)
        return tmp_dir / names[0]


def run_validator(response: Path, summary: Path) -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR.relative_to(ROOT)), str(response), "--summary-out", str(summary)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "validator rejected response").strip()
        raise SystemExit(f"response validation failed; canonical artifacts were not modified: {detail}")


def main() -> None:
    args = parse_args()
    source = resolve(args.response)
    if not source.exists():
        raise SystemExit(f"response path does not exist: {source}")

    with tempfile.TemporaryDirectory(prefix="jrl_acv_import_") as tmp_text:
        tmp = Path(tmp_text)
        if source.suffix.lower() == ".zip":
            response = find_response_in_zip(source, tmp)
        elif source.suffix.lower() == ".csv":
            response = source
        else:
            raise SystemExit(f"response must be CSV or zip: {source}")

        rows = read_rows(response)
        if len(rows) != 4:
            raise SystemExit("completed aligned-control value authorization response must contain exactly four rows")
        tmp_summary = tmp / "validated_summary.csv"
        run_validator(response, tmp_summary)
        decision = read_rows(tmp_summary)[0]["decision"]

        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        run_validator(CANONICAL_RESPONSE, CANONICAL_SUMMARY)

        if source.suffix.lower() == ".zip":
            with zipfile.ZipFile(source) as zf:
                for name in zf.namelist():
                    base = Path(name).name
                    if base in {
                        "joint_row_level_aligned_control_value_authorization_completed_summary_v1.csv",
                        "joint_row_level_aligned_control_value_authorization_validation_log_v1.txt",
                    }:
                        zf.extract(name, tmp)
                        shutil.copy2(tmp / name, ROOT / "data/derived" / base)
                    elif base == "joint_row_level_aligned_control_value_authorization_review_notes_v1.md":
                        zf.extract(name, tmp)
                        shutil.copy2(tmp / name, ROOT / "docs" / base)

    print(
        "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_RESPONSE_IMPORTED "
        f"decision={decision} response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
