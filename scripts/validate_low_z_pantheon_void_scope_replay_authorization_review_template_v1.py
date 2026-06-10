#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_scope_replay_authorization_review_policy_v1.csv"
SCOPE_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_template_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_scope_integrity",
    "Q2_low_z_rationale",
    "Q3_no_leakage",
    "Q4_authorization",
}


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
    policy_rows = read_rows(POLICY)
    scope = read_one(SCOPE_SUMMARY)
    template_rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)

    require({row["question_id"] for row in policy_rows} == EXPECTED_QUESTIONS, "unexpected policy questions")
    require({row["question_id"] for row in template_rows} == EXPECTED_QUESTIONS, "unexpected template questions")
    require(scope["candidate_endpoint_run_allowed_now"] == "false", "scope must not pre-authorize endpoint")
    require(scope["endpoint_scoring_allowed"] == "false", "scope must keep scoring disabled")
    require(int(scope["included_rows"]) > 0, "scope must include rows")

    for row in policy_rows:
        for marker in [
            "residuals",
            "chi2",
            "AIC",
            "BIC",
            "endpoint_rank",
            "fit_improvement_flags",
            "posthoc_row_selection",
            "posthoc_amplitude_tuning",
        ]:
            require(marker in row["forbidden_inputs"], f"{row['question_id']}: missing forbidden marker {marker}")
        require(
            row["claim_boundary"] == "low_z_void_scope_replay_authorization_review_not_validation",
            f"{row['question_id']}: claim boundary mismatch",
        )

    for row in template_rows:
        require(row["review_completed"] == "false", "template must not be pre-completed")
        require(row["forbidden_inputs_used"] == "false", "template must default forbidden_inputs_used=false")
        require(row["endpoint_run_allowed"] == "false", "template must not pre-authorize replay")
        require(row["physical_validation_claimed"] == "false", "template must not claim validation")
        require(
            row["authorization_scope"]
            == "single_predeclared_low_z_pantheon_void_replay_permission_only_not_validation",
            "authorization scope mismatch",
        )
        require(row["included_rows"] == scope["included_rows"], "included row mismatch")
        require(row["z_support_max"] == scope["z_support_max"], "z support mismatch")

    require(summary["status"] == "AUTHORIZATION_REVIEW_TEMPLATE_READY_NOT_COMPLETED", "summary status mismatch")
    require(summary["review_completed"] == "false", "summary must keep review_completed=false")
    require(summary["endpoint_run_allowed"] == "false", "summary must keep endpoint_run_allowed=false")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim validation")
    require(
        summary["claim_boundary"] == "low_z_void_scope_replay_authorization_review_not_validation",
        "summary claim boundary mismatch",
    )
    print(
        "PAPER10_LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION_REVIEW_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_run_allowed=false"
    )


if __name__ == "__main__":
    main()
