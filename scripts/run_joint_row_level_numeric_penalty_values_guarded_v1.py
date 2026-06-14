#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOCKER = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1_summary.csv"
AUTH_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_values_guarded_runner_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"BLOCKED: missing required authorization artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"BLOCKED: {path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], field: str, label: str) -> None:
    if row[field] != "false":
        raise SystemExit(f"BLOCKED: {label} unsafe field {field}={row[field]}")


def main() -> None:
    blocker = read_one(BLOCKER)
    for field in [
        "lambda_row_numeric_value_allowed",
        "t_joint_rescoring_allowed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
        "penalty_values_computed",
    ]:
        require_false(blocker, field, "blocker")

    if blocker["numeric_penalty_computation_allowed"] != "true":
        raise SystemExit(
            "BLOCKED: numeric row-level penalty values are not authorized. "
            f"verdict={blocker['verdict']} next={blocker['next_required_action']} "
            f"claim_boundary={CLAIM_BOUNDARY}"
        )

    auth = read_one(AUTH_SUMMARY)
    if auth["decision"] != "AUTHORIZE_SEPARATE_NUMERIC_PENALTY_VALUE_PACKAGE_NOT_RESCORING_NOT_VALIDATION":
        raise SystemExit(f"BLOCKED: unexpected authorization decision: {auth['decision']}")
    if auth["numeric_penalty_computation_authorized"] != "true":
        raise SystemExit("BLOCKED: authorization summary does not allow numeric penalty computation")
    for field in [
        "lambda_row_numeric_value_authorized",
        "t_joint_rescoring_authorized",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
    ]:
        require_false(auth, field, "authorization")

    print(
        "READY_FOR_SEPARATE_NUMERIC_PACKAGE: authorization is present, but this guard "
        "does not compute values. Build a separate numeric penalty value package next. "
        f"claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()
