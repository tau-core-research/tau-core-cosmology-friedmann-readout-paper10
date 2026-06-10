#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_policy_v1.csv"
)
COMPLETED_REVIEW_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv"
)
TEMPLATE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_partial_scope_replay_authorization_review_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_source_side_review_closure",
    "Q2_partial_scope_replay_scope",
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
    completed = read_one(COMPLETED_REVIEW_SUMMARY)
    template_rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require({row["question_id"] for row in policy_rows} == EXPECTED_QUESTIONS, "unexpected policy questions")
    require({row["question_id"] for row in template_rows} == EXPECTED_QUESTIONS, "unexpected template questions")
    require(completed["review_completed"] == "true", "source-side review must be complete")
    require(completed["final_verdict"] == "ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE", "bad source-side verdict")
    require(completed["endpoint_replay_allowed"] == "false", "source-side review must not authorize replay")
    require(completed["endpoint_validation_claimed"] == "false", "source-side review must not claim validation")
    require(completed["physical_lensing_path_weight_claimed"] == "false", "source-side review must not claim path physics")
    for row in policy_rows:
        for marker in [
            "distance_residuals",
            "lensing_residuals",
            "fit_statistics",
            "endpoint_scores",
            "kids_data_vector_values",
            "posterior_chains",
            "posthoc_path_weight_tuning",
            "physical_lensing_path_weight_claims",
        ]:
            require(marker in row["forbidden_inputs"], f"{row['question_id']}: missing forbidden marker {marker}")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{row['question_id']}: claim boundary mismatch")
    for row in template_rows:
        require(row["review_completed"] == "false", "template must not be completed")
        require(row["forbidden_inputs_used"] == "false", "template must default forbidden_inputs_used=false")
        require(row["endpoint_replay_allowed"] == "false", "template must not pre-authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "template must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "template must not claim path physics")
        require(
            row["authorization_scope"] == "single_permission_only_12_row_partial_W_path_replay_not_validation",
            "authorization scope mismatch",
        )
        require(row["source_side_review_verdict"] == completed["verdict"], "source-side verdict mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(summary["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad summary status")
    require(summary["review_completed"] == "false", "summary must keep review_completed=false")
    require(summary["endpoint_replay_allowed"] == "false", "summary must keep endpoint_replay_allowed=false")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
