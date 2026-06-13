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
CANONICAL_RESPONSE = ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/joint_block_diagonal_independence_review_response_v1_summary.csv"
VALIDATOR = ROOT / "scripts/validate_joint_block_diagonal_independence_review_response_v1.py"
EXPECTED_NAME = "joint_block_diagonal_independence_review_response_template_v1.csv"
EXPECTED_REVIEW_ID = "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_PACKAGE_V1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import a completed external joint block-diagonal independence "
            "review response only after validation succeeds. Accepts either a "
            "CSV response or a zip containing the completed response CSV."
        )
    )
    parser.add_argument("response", help="Path to completed reviewer response CSV or zip.")
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require_completed_response(path: Path) -> None:
    rows = read_rows(path)
    if len(rows) != 4:
        raise SystemExit("completed response must contain exactly four rows")
    for row in rows:
        if row.get("review_id") != EXPECTED_REVIEW_ID:
            raise SystemExit("response review_id mismatch")
        if row.get("review_completed", "").strip().lower() != "true":
            raise SystemExit("refusing to import incomplete review response")
        if not row.get("reviewer_response", "").strip():
            raise SystemExit("completed response row is missing reviewer_response")
        if not row.get("reviewer_id_or_role", "").strip():
            raise SystemExit("completed response row is missing reviewer_id_or_role")
        if not row.get("reviewer_rationale", "").strip():
            raise SystemExit("completed response row is missing reviewer_rationale")
        if row.get("forbidden_inputs_used", "").strip().lower() != "false":
            raise SystemExit("refusing response with forbidden_inputs_used=true")


def find_response_in_zip(zip_path: Path, tmp_dir: Path) -> Path:
    with zipfile.ZipFile(zip_path) as zf:
        names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        candidate_names = [name for name in names if Path(name).name == EXPECTED_NAME]
        if not candidate_names and len(names) == 1:
            candidate_names = names
        if len(candidate_names) != 1:
            raise SystemExit(f"zip must contain exactly one completed response CSV; found {names}")
        zf.extract(candidate_names[0], tmp_dir)
        return tmp_dir / candidate_names[0]


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
    source = resolve(args.response)
    if not source.exists():
        raise SystemExit(f"response path does not exist: {source}")

    with tempfile.TemporaryDirectory(prefix="joint_block_diagonal_independence_import_") as tmp_text:
        tmp = Path(tmp_text)
        if source.suffix.lower() == ".zip":
            response = find_response_in_zip(source, tmp)
        elif source.suffix.lower() == ".csv":
            response = source
        else:
            raise SystemExit(f"response must be a CSV or zip file: {source}")

        require_completed_response(response)
        tmp_summary = tmp / "validated_summary.csv"
        run_validator(response, tmp_summary)
        summary_rows = read_rows(tmp_summary)
        if len(summary_rows) != 1:
            raise SystemExit("validator summary must contain exactly one row")
        decision = summary_rows[0]["decision"]
        if decision == "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_RESPONSE_TEMPLATE_READY_NOT_COMPLETED":
            raise SystemExit("refusing to import a blank template response")

        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(response, CANONICAL_RESPONSE)
        shutil.copy2(tmp_summary, CANONICAL_SUMMARY)

    print(
        "JOINT_BLOCK_DIAGONAL_INDEPENDENCE_REVIEW_RESPONSE_IMPORTED "
        f"decision={decision} response={CANONICAL_RESPONSE.relative_to(ROOT)} "
        f"summary={CANONICAL_SUMMARY.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
