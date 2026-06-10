#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_observer_dependence_followup_policy_v1.csv"
TEMPLATE = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_dependence_followup_response_template_v1.csv"
)
SUMMARY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_dependence_followup_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_observer_dependence_followup_not_endpoint_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_no_endpoint_leakage",
    "Q2_source_basis_identity",
    "Q3_screen_interpretation",
    "Q4_next_action",
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
            "lensing_residuals",
            "fit_statistics",
            "endpoint_scores",
            "posthoc_sky_direction_selection",
            "posthoc_path_projection_labels",
            "posthoc_path_weight_tuning",
            "physical_validation_claims",
        ]:
            require(marker in row["forbidden_inputs"], f"{row['question_id']}: missing forbidden marker {marker}")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "policy claim boundary mismatch")
    for row in template_rows:
        require(row["review_completed"] == "false", "template must be blank")
        require(row["forbidden_inputs_used"] == "false", "template must default forbidden_inputs_used=false")
        require(row["endpoint_replay_allowed"] == "false", "template must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "template must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "template must not claim path physics")
        require(row["followup_family"] == "W_path_x_sky_z", "follow-up family mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "template claim boundary mismatch")
    require(summary["status"] == "V2_OBSERVER_DEPENDENCE_FOLLOWUP_TEMPLATE_READY_NOT_COMPLETED", "bad status")
    require(summary["followup_family"] == "W_path_x_sky_z", "summary follow-up family mismatch")
    require(summary["family_survives_controls"] == "true", "family control survival must be true")
    require(summary["review_completed"] == "false", "summary must not be completed")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print(
        "PAPER10_V2_OBSERVER_DEPENDENCE_FOLLOWUP_TEMPLATE_V1_VALIDATED "
        "followup_family=W_path_x_sky_z"
    )


if __name__ == "__main__":
    main()
