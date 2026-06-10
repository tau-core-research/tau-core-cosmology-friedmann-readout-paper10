#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv"
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_endpoint_replay_authorization_review_package_v1_summary.csv"
)
R6_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv"

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


def validate_response(rows: list[dict[str, str]], r6: dict[str, str]) -> None:
    require(len(rows) == 4, "authorization response must contain exactly four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected authorization question set")
    by_question = {row["question_id"]: row for row in rows}

    for row in rows:
        require(norm(row["review_completed"]) == "true", "all authorization rows must set review_completed=true")
        require(row["reviewer_id_or_role"].strip(), "reviewer_id_or_role must be nonempty")
        require(row["reviewer_rationale"].strip(), "reviewer_rationale must be nonempty")
        require(norm(row["forbidden_inputs_used"]) == "false", "authorization response must keep forbidden_inputs_used=false")
        require(norm(row["endpoint_replay_allowed"]) == "true", "accepted response must set endpoint_replay_allowed=true")
        require(norm(row["endpoint_validation_claimed"]) == "false", "authorization response must not claim validation")
        require(
            row["authorization_scope"]
            == "single_predeclared_refined_low_z_void_source_basis_replay_permission_only_not_validation",
            "authorization_scope must remain refined low-z void replay permission-only",
        )
        require(row["r6_source_side_verdict"] == r6["verdict"], "R6 verdict must match frozen source-side summary")
        require(
            row["claim_boundary"] == "void_source_basis_refinement_endpoint_replay_authorization_review_not_validation",
            "claim boundary must remain authorization review, not validation",
        )

    require(norm(by_question["Q1_r6_source_side_closure"]["reviewer_response"]) == "yes", "Q1 must be yes")
    require(
        norm(by_question["Q2_refined_replay_scope"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q2 must be yes or caveated_yes",
    )
    require(norm(by_question["Q3_no_leakage"]["reviewer_response"]) == "yes", "Q3 must be yes")
    require(
        by_question["Q4_authorization"]["reviewer_response"].strip() == "GO_REFINED_VOID_REPLAY_PERMISSION_ONLY",
        "Q4 must grant refined void replay permission only",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a completed refined void endpoint replay authorization review response."
    )
    parser.add_argument("response_csv", type=Path)
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT
        / "data"
        / "derived"
        / "void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv",
    )
    args = parser.parse_args()

    response_path = args.response_csv.resolve()
    if not response_path.exists():
        raise SystemExit(f"missing authorization response: {response_path}")

    policy_rows = read_rows(POLICY)
    package = read_one(PACKAGE_SUMMARY)
    r6 = read_one(R6_SUMMARY)
    rows = read_rows(response_path)

    require({row["question_id"] for row in policy_rows} == EXPECTED_QUESTIONS, "unexpected policy question set")
    require(
        package["status"] == "REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "handoff package must be the clean uncompleted authorization package",
    )
    require(package["review_completed"] == "false", "handoff package must not be pre-completed")
    require(package["endpoint_replay_allowed"] == "false", "handoff package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "handoff package must not claim validation")
    require(package["contains_endpoint_residuals"] == "false", "handoff package must not include endpoint residuals")
    require(package["contains_endpoint_scores"] == "false", "handoff package must not include endpoint scores")
    require(package["contains_fit_statistics"] == "false", "handoff package must not include fit statistics")
    require(r6["review_completed"] == "true", "R6 source-side review must be complete before replay authorization")
    require(r6["leakage_review_complete"] == "true", "R6 leakage review must be complete")
    require(r6["source_unique_ready"] == "true", "R6 source_unique_ready must be true")
    require(r6["endpoint_replay_allowed"] == "false", "R6 must not itself authorize replay")
    require(r6["endpoint_validation_claimed"] == "false", "R6 must not claim validation")

    validate_response(rows, r6)

    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "response_path": display_path(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package["zip_sha256"],
            "review_completed": "true",
            "r6_source_side_verdict": r6["verdict"],
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "authorization_scope": "single_predeclared_refined_low_z_void_source_basis_replay_permission_only_not_validation",
            "verdict": "refined_void_replay_authorized_permission_only_not_validation",
            "recommended_next_action": "run_only_the_separate_predeclared_refined_void_replay_without_validation_claim",
            "claim_boundary": "void_source_basis_refinement_endpoint_replay_authorization_review_not_validation",
        }
    ]
    write_csv(args.summary_out, summary)
    print(
        "PAPER10_REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
