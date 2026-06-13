#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_rows(POLICY)
    rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require(len(policy) == 5, "policy must have five rows")
    require(len(rows) == 5, "template must have five rows")
    require(summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad status")
    require(summary["authorization_scope"] == "single_permission_only_desi_cc_5row_time_level_replay_not_validation", "bad scope")
    require(
        summary["readiness_verdict"]
        == "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing",
        "bad readiness verdict",
    )
    require(summary["desi_first_endpoint_rows"] == "5", "bad DESI endpoint row count")
    require(summary["desi_control_family_count"] == "7", "bad DESI control family count")
    require(summary["desi_control_seed_range"] == "41001;41007", "bad DESI control seed range")
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
            row["authorization_scope"] == "single_permission_only_desi_cc_5row_time_level_replay_not_validation",
            "bad row authorization scope",
        )
        require(row["desi_first_endpoint_rows"] == "5", "bad row endpoint scope")
        require(row["desi_control_family_count"] == "7", "bad row control count")
        require(row["desi_control_seed_range"] == "41001;41007", "bad row seed range")
        require(row["high_z_policy"] == "z2p33_excluded_as_holdout_or_future_independent_clock_support", "bad high-z policy")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_TEMPLATE_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
