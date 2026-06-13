#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_replay_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_rows(POLICY)
    rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require(len(policy) == 4, "policy must have four questions")
    require(len(rows) == 4, "template must have four response rows")
    require(summary["status"] == "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad status")
    require(summary["basis_rows"] == "424", "expected 424 basis rows")
    require(summary["review_completed"] == "false", "template must not be completed")
    require(summary["endpoint_replay_allowed"] == "false", "template must not pre-authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "template must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "template must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["review_completed"] == "false", "row must be blank")
        require(row["reviewer_response"] == "", "row response must be blank")
        require(row["forbidden_inputs_used"] == "false", "forbidden inputs must default false")
        require(row["endpoint_replay_allowed"] == "false", "row must not pre-authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["physical_validation_claimed"] == "false", "row must not claim physical validation")
        require(row["authorization_scope"] == "single_permission_only_low_z_W_time_uncertainty_basis_replay_not_validation", "bad scope")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
