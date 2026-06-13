#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/pantheon_clock_slope_route_replay_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "clock_slope_route_replay_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_rows(POLICY)
    rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require(len(policy) == 4, "policy must have four rows")
    require(len(rows) == 4, "template must have four rows")
    require(summary["status"] == "CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad status")
    require(summary["selected_route_candidate_family"] == "clock_slope", "template must target clock_slope")
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
        require(
            row["authorization_scope"] == "single_permission_only_pantheon_clock_slope_route_replay_candidate_not_validation",
            "bad authorization scope",
        )
        require(row["route_status"] == "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL", "bad route status")
        require(row["selected_route_candidate_family"] == "clock_slope", "bad family")
        require(row["local_controls_pass"] == "true", "local control status mismatch")
        require(row["global_controls_pass"] == "false", "global control blocker must remain explicit")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_TEMPLATE_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
