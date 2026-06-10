#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_r6_reviewer_template_policy_v1.csv"
TEMPLATE = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_template_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_source_identity",
    "Q2_no_endpoint_fields",
    "Q3_r4_r5_gate_consistency",
    "Q4_r6_decision",
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    require(policy["status"] == "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_POLICY_FROZEN", "bad policy")
    require(summary["status"] == "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_BUILT_NOT_COMPLETED", "bad summary status")
    require(len(rows) == 4 and summary["question_count"] == "4", "R6 template must contain four questions")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected R6 question set")
    for key in [
        "review_completed",
        "independent_reviewer_attestation_complete",
        "leakage_review_complete",
        "source_unique_ready",
        "computes_new_scores",
        "uses_distance_residuals",
        "uses_fit_statistics",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    for row in rows:
        for empty_key in ["reviewer_response", "reviewer_rationale", "reviewer_id_or_role"]:
            require(row[empty_key] == "", f"template must leave {empty_key} blank")
        require(row["review_completed"] == "false", "template rows must not be completed")
        require(row["forbidden_inputs_used"] == "false", "template rows must not use forbidden inputs")
        require(row["endpoint_replay_allowed"] == "false", "template rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "template rows must not claim validation")
        require(row["claim_boundary"] == policy["claim_boundary"], "claim boundary mismatch")
    require(summary["verdict"] == "r6_reviewer_template_ready_not_completed", "unexpected verdict")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
