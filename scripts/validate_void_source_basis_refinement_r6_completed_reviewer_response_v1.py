#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_r6_completed_reviewer_response_policy_v1.csv"
HANDOFF_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv"

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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def norm(value: str) -> str:
    return value.strip().lower()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_response(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 4, "completed R6 response must contain exactly four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected R6 question set")
    by_question = {row["question_id"]: row for row in rows}
    for row in rows:
        require(norm(row["review_completed"]) == "true", "all reviewer rows must set review_completed=true")
        require(norm(row["forbidden_inputs_used"]) == "false", "reviewer response must keep forbidden_inputs_used=false")
        require(norm(row["endpoint_replay_allowed"]) == "false", "reviewer response must not authorize endpoint replay")
        require(norm(row["endpoint_validation_claimed"]) == "false", "reviewer response must not claim validation")
        require(row["reviewer_id_or_role"].strip(), "reviewer_id_or_role must be nonempty")
        require(row["reviewer_rationale"].strip(), "reviewer_rationale must be nonempty")
    require(norm(by_question["Q1_source_identity"]["reviewer_response"]) == "yes", "Q1 must be yes")
    require(norm(by_question["Q2_no_endpoint_fields"]["reviewer_response"]) == "yes", "Q2 must be yes")
    require(
        norm(by_question["Q3_r4_r5_gate_consistency"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q3 must be yes or caveated_yes",
    )
    require(
        by_question["Q4_r6_decision"]["reviewer_response"].strip() == "ACCEPT_AS_CAVEATED_SOURCE_SIDE_REVIEW",
        "Q4 must accept the source-side review as caveated",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a completed R6 void source-basis reviewer response.")
    parser.add_argument("response_csv", type=Path)
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT / "data" / "derived" / "void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv",
    )
    args = parser.parse_args()
    response_path = args.response_csv.resolve()
    require(response_path.exists(), f"missing completed reviewer response: {response_path}")

    policy = read_one(POLICY)
    handoff = read_one(HANDOFF_SUMMARY)
    rows = read_rows(response_path)
    require(policy["status"] == "VOID_SOURCE_BASIS_REFINEMENT_R6_COMPLETED_REVIEWER_RESPONSE_POLICY_FROZEN", "bad policy")
    require(handoff["verdict"] == "r6_reviewer_handoff_package_ready_not_completed", "completed response must derive from ready R6 handoff package")
    require(handoff["endpoint_replay_allowed"] == "false", "handoff package must not authorize endpoint replay")
    validate_response(rows)

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "VOID_SOURCE_BASIS_REFINEMENT_R6_COMPLETED_REVIEWER_RESPONSE_ACCEPTED_SOURCE_SIDE_ONLY",
            "response_path": display_path(response_path),
            "response_sha256": sha256(response_path),
            "review_completed": "true",
            "independent_reviewer_attestation_complete": "true",
            "leakage_review_complete": "true",
            "source_unique_ready": "true",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "r6_completed_reviewer_response_accepted_source_side_only_endpoint_replay_still_forbidden",
            "recommended_next_action": "human_review_before_any_separate_endpoint_replay_gate",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(args.summary_out, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R6_COMPLETED_REVIEWER_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
