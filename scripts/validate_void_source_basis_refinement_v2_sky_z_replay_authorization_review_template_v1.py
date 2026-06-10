#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_policy_v1.csv"
)
TEMPLATE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_template_v1.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_sky_z_replay_authorization_review_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_W_path_x_sky_z_replay_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_followup_closure",
    "Q2_sky_z_replay_scope",
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
    template_rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require({row["question_id"] for row in policy_rows} == EXPECTED_QUESTIONS, "unexpected policy questions")
    require({row["question_id"] for row in template_rows} == EXPECTED_QUESTIONS, "unexpected template questions")
    for row in policy_rows:
        for marker in [
            "distance_residuals",
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
        require(row["authorization_scope"] == AUTH_SCOPE, "authorization scope mismatch")
        require(row["followup_family"] == "W_path_x_sky_z", "followup family mismatch")
        require(row["sky_z_family_survives_controls"] == "true", "sky-z family control status mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(summary["status"] == "V2_SKY_Z_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad summary status")
    require(summary["followup_family"] == "W_path_x_sky_z", "summary followup family mismatch")
    require(summary["family_survives_controls"] == "true", "summary family control status mismatch")
    require(summary["controls_better_than_candidate_chi2"] == "0", "summary control count mismatch")
    require(summary["review_completed"] == "false", "summary must keep review_completed=false")
    require(summary["endpoint_replay_allowed"] == "false", "summary must keep endpoint_replay_allowed=false")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print(
        "PAPER10_V2_SKY_Z_REPLAY_AUTHORIZATION_TEMPLATE_V1_VALIDATED "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
