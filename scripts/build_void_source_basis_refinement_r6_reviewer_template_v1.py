#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_r6_reviewer_template_policy_v1.csv"
R5_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_template_v1_summary.csv"

QUESTIONS = [
    {
        "question_id": "Q1_source_identity",
        "question_text": "Do the attached R1-R3 artifacts match the stated source-native void catalogue, host/SN-to-void geometry join, and fixed line-of-sight environment construction?",
        "required_response": "yes_or_no",
        "acceptance_condition": "yes_with_source_side_rationale",
    },
    {
        "question_id": "Q2_no_endpoint_fields",
        "question_text": "Did the review avoid endpoint scores, distance residuals, fit statistics, post-score residual shapes, and physical-validation claims?",
        "required_response": "yes_or_no",
        "acceptance_condition": "yes",
    },
    {
        "question_id": "Q3_r4_r5_gate_consistency",
        "question_text": "Do R4 and R5 consistently keep only low-correlation source candidates and frozen controls without reopening endpoint replay?",
        "required_response": "yes_or_caveated_yes_or_no",
        "acceptance_condition": "yes_or_caveated_yes_with_blockers_named",
    },
    {
        "question_id": "Q4_r6_decision",
        "question_text": "Can the R6 leakage review be accepted for caveated source-side purposes without authorizing endpoint replay or validation?",
        "required_response": "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW or REJECT or NEEDS_MORE_SOURCE_EVIDENCE",
        "acceptance_condition": "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW",
    },
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    r5 = read_one(R5_SUMMARY)
    if policy["status"] != "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_POLICY_FROZEN":
        raise SystemExit("unexpected R6 reviewer template policy status")
    if r5["status"] != "R5_CONTROL_RESISTANCE_PREFLIGHT_FROZEN_R6_STILL_OPEN":
        raise SystemExit("R6 template requires completed R5 control-resistance preflight")
    if r5["endpoint_replay_allowed"] != "false":
        raise SystemExit("R5 must not allow endpoint replay")
    if r5["leakage_review_complete"] != "false":
        raise SystemExit("R6 template must be built before completed leakage review")

    context = (
        "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1.csv;"
        "data/derived/void_source_basis_refinement_r4_independence_preflight_v1.csv;"
        "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv;"
        "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv"
    )
    rows = []
    for item in QUESTIONS:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "question_id": item["question_id"],
                "question_text": item["question_text"],
                "review_context_artifacts": context,
                "required_response": item["required_response"],
                "acceptance_condition": item["acceptance_condition"],
                "reviewer_response": "",
                "reviewer_rationale": "",
                "reviewer_id_or_role": "",
                "review_completed": "false",
                "forbidden_inputs_used": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_BUILT_NOT_COMPLETED",
            "question_count": str(len(rows)),
            "review_completed": "false",
            "independent_reviewer_attestation_complete": "false",
            "leakage_review_complete": "false",
            "source_unique_ready": "false",
            "computes_new_scores": "false",
            "uses_distance_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "r6_reviewer_template_ready_not_completed",
            "recommended_next_action": "send_template_to_independent_reviewer_then_validate_completed_response",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_TEMPLATE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
