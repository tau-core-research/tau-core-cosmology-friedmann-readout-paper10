#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv"
R6_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_endpoint_replay_authorization_review_template_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_r6_source_side_closure",
    "Q2_refined_replay_scope",
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
    r6 = read_one(R6_SUMMARY)
    template_rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)

    require({row["question_id"] for row in policy_rows} == EXPECTED_QUESTIONS, "unexpected policy questions")
    require({row["question_id"] for row in template_rows} == EXPECTED_QUESTIONS, "unexpected template questions")
    require(r6["leakage_review_complete"] == "true", "R6 leakage review must be complete")
    require(r6["source_unique_ready"] == "true", "R6 source_unique_ready must be true")
    require(r6["endpoint_replay_allowed"] == "false", "R6 must not authorize replay")
    require(r6["endpoint_validation_claimed"] == "false", "R6 must not claim validation")

    for row in policy_rows:
        for marker in [
            "distance_residuals",
            "fit_statistics",
            "endpoint_scores",
            "posthoc_void_catalog_choice",
            "posthoc_row_selection",
            "posthoc_void_thresholds",
            "posthoc_amplitude_tuning",
            "posthoc_covariance_reweighting",
        ]:
            require(marker in row["forbidden_inputs"], f"{row['question_id']}: missing forbidden marker {marker}")
        require(
            row["claim_boundary"] == "void_source_basis_refinement_endpoint_replay_authorization_review_not_validation",
            f"{row['question_id']}: claim boundary mismatch",
        )

    for row in template_rows:
        require(row["review_completed"] == "false", "template must not be completed")
        require(row["forbidden_inputs_used"] == "false", "template must default forbidden_inputs_used=false")
        require(row["endpoint_replay_allowed"] == "false", "template must not pre-authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "template must not claim validation")
        require(
            row["authorization_scope"]
            == "single_predeclared_refined_low_z_void_source_basis_replay_permission_only_not_validation",
            "authorization scope mismatch",
        )
        require(row["r6_source_side_verdict"] == r6["verdict"], "R6 verdict mismatch")
        require(row["claim_boundary"] == "void_source_basis_refinement_endpoint_replay_authorization_review_not_validation", "claim boundary mismatch")

    require(summary["status"] == "REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "summary status mismatch")
    require(summary["review_completed"] == "false", "summary must keep review_completed=false")
    require(summary["endpoint_replay_allowed"] == "false", "summary must keep endpoint_replay_allowed=false")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    print(
        "PAPER10_REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
