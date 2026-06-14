#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_joint_numeric_t_joint_control_suite_review_response_v1.py"
CANONICAL_RESPONSE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_v1.csv"
CANONICAL_SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_v1_summary.csv"
RECONCILIATION = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_response_reconciliation_v1.csv"
EXPECTED_DECISION = "ACCEPT_CONTROL_SUITE_REVIEW_FOR_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE_PREPARATION_NOT_ENDPOINT_SCORING_NOT_VALIDATION"
EXPECTED_NEXT = "prepare_separate_endpoint_scoring_authorization_package_if_needed; do_not_score_from_this_review"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile completed control-suite review response with reviewer summary.")
    parser.add_argument("response_csv")
    parser.add_argument("completed_summary_csv")
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_validator(response: Path, summary: Path) -> None:
    result = subprocess.run(
        ["python", str(VALIDATOR.relative_to(ROOT)), str(response), "--summary-out", str(summary)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit((result.stderr or result.stdout).strip())


def main() -> None:
    args = parse_args()
    response_path = resolve(args.response_csv)
    completed_summary_path = resolve(args.completed_summary_csv)
    rows = read_rows(response_path)
    completed = read_rows(completed_summary_path)
    if len(completed) != 1:
        raise SystemExit("completed summary must contain exactly one row")
    summary = completed[0]
    if summary["decision"] != EXPECTED_DECISION:
        raise SystemExit("completed summary does not authorize package-preparation-only route")
    if summary["next_required_action"] != EXPECTED_NEXT:
        raise SystemExit("completed summary next action mismatch")
    if summary["endpoint_scoring_allowed"].strip().lower() != "false":
        raise SystemExit("summary must not authorize endpoint scoring")
    if summary["endpoint_validation_claimed"].strip().lower() != "false":
        raise SystemExit("summary must not claim endpoint validation")
    if summary["completion_check"].strip().lower() != "pass":
        raise SystemExit("summary completion_check must be pass")
    if len(rows) != 4:
        raise SystemExit("response must contain four rows")

    changed_rows = 0
    reconciled = []
    for row in rows:
        old_value = row["endpoint_scoring_authorization_package_preparation_allowed"]
        if old_value.strip().lower() != "true":
            row["endpoint_scoring_authorization_package_preparation_allowed"] = "true"
            changed_rows += 1
        reconciled.append(row)

    if changed_rows != 4:
        raise SystemExit("expected all four template preparation fields to require reconciliation")

    with tempfile.TemporaryDirectory(prefix="control_suite_review_reconcile_") as tmp_text:
        tmp = Path(tmp_text)
        reconciled_response = tmp / "reconciled_response.csv"
        reconciled_summary = tmp / "reconciled_summary.csv"
        write_rows(reconciled_response, reconciled)
        run_validator(reconciled_response, reconciled_summary)
        CANONICAL_RESPONSE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(reconciled_response, CANONICAL_RESPONSE)
        run_validator(CANONICAL_RESPONSE, CANONICAL_SUMMARY)

    write_rows(
        RECONCILIATION,
        [
            {
                "reconciliation_id": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_RESPONSE_RECONCILIATION_V1",
                "source_response_path": str(response_path),
                "source_completed_summary_path": str(completed_summary_path),
                "reconciled_rows": str(changed_rows),
                "field_reconciled": "endpoint_scoring_authorization_package_preparation_allowed",
                "old_value": "False",
                "new_value": "true",
                "basis": "completed_summary_decision_and_next_required_action_authorize_package_preparation_only_not_scoring",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "review_response_reconciled_from_completed_summary_not_scoring_not_validation",
            }
        ],
    )
    print("JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_RESPONSE_RECONCILED_AND_IMPORTED")


if __name__ == "__main__":
    main()
