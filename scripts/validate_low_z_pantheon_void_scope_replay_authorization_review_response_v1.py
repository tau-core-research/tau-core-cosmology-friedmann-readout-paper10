#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_scope_replay_authorization_review_policy_v1.csv"
PACKAGE_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_package_v1_summary.csv"
SCOPE_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_scope_integrity",
    "Q2_low_z_rationale",
    "Q3_no_leakage",
    "Q4_authorization",
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


def validate_response(rows: list[dict[str, str]], scope: dict[str, str]) -> None:
    require(len(rows) == 4, "authorization response must contain exactly four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected authorization question set")
    by_question = {row["question_id"]: row for row in rows}

    for row in rows:
        require(norm(row["review_completed"]) == "true", "all authorization rows must set review_completed=true")
        require(row["reviewer_id_or_role"].strip(), "reviewer_id_or_role must be nonempty")
        require(row["reviewer_rationale"].strip(), "reviewer_rationale must be nonempty")
        require(norm(row["forbidden_inputs_used"]) == "false", "authorization response must keep forbidden_inputs_used=false")
        require(norm(row["endpoint_run_allowed"]) == "true", "accepted response must set endpoint_run_allowed=true")
        require(norm(row["physical_validation_claimed"]) == "false", "authorization response must not claim validation")
        require(
            row["authorization_scope"]
            == "single_predeclared_low_z_pantheon_void_replay_permission_only_not_validation",
            "authorization_scope must remain low-z replay permission-only",
        )
        require(row["included_rows"] == scope["included_rows"], "included_rows must match frozen low-z scope")
        require(row["z_support_max"] == scope["z_support_max"], "z_support_max must match frozen low-z scope")
        require(
            row["claim_boundary"] == "low_z_void_scope_replay_authorization_review_not_validation",
            "claim boundary must remain authorization review, not validation",
        )

    require(norm(by_question["Q1_scope_integrity"]["reviewer_response"]) == "yes", "Q1 must be yes")
    require(
        norm(by_question["Q2_low_z_rationale"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q2 must be yes or caveated_yes",
    )
    require(norm(by_question["Q3_no_leakage"]["reviewer_response"]) == "yes", "Q3 must be yes")
    require(
        by_question["Q4_authorization"]["reviewer_response"].strip()
        == "GO_LOW_Z_VOID_REPLAY_PERMISSION_ONLY",
        "Q4 must grant low-z void replay permission only",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a completed low-z Pantheon void replay authorization review response."
    )
    parser.add_argument("response_csv", type=Path)
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT
        / "data"
        / "derived"
        / "low_z_pantheon_void_scope_replay_authorization_review_response_v1_summary.csv",
    )
    args = parser.parse_args()

    response_path = args.response_csv.resolve()
    if not response_path.exists():
        raise SystemExit(f"missing authorization response: {response_path}")

    policy_rows = read_rows(POLICY)
    package = read_one(PACKAGE_SUMMARY)
    scope = read_one(SCOPE_SUMMARY)
    rows = read_rows(response_path)

    require(len(policy_rows) == 4, "authorization policy must contain four rows")
    require(
        package["status"] == "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "review package must be the clean uncompleted handoff package",
    )
    require(package["endpoint_run_allowed"] == "false", "handoff package must not pre-authorize replay")
    require(package["contains_endpoint_residuals"] == "false", "handoff package must not include endpoint residuals")
    require(package["contains_endpoint_scores"] == "false", "handoff package must not include endpoint scores")
    require(package["contains_fit_statistics"] == "false", "handoff package must not include fit statistics")
    require(scope["candidate_endpoint_run_allowed_now"] == "false", "scope candidate must not pre-authorize replay")
    require(scope["endpoint_scoring_allowed"] == "false", "scope candidate must keep scoring disabled")
    validate_response(rows, scope)

    summary = [
        {
            "policy_id": "LOW_Z_PANTHEON_VOID_SCOPE_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "response_path": display_path(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package["zip_sha256"],
            "review_completed": "true",
            "scope_candidate_id": scope["scope_id"],
            "included_rows": scope["included_rows"],
            "z_support_max": scope["z_support_max"],
            "forbidden_inputs_used": "false",
            "endpoint_run_allowed": "true",
            "physical_validation_claimed": "false",
            "authorization_scope": "single_predeclared_low_z_pantheon_void_replay_permission_only_not_validation",
            "verdict": "low_z_void_replay_authorized_permission_only_not_validation",
            "recommended_next_action": "run_only_the_separate_predeclared_low_z_void_replay_without_validation_claim",
            "claim_boundary": "low_z_void_scope_replay_authorization_review_not_validation",
        }
    ]
    write_csv(args.summary_out, summary)
    print(
        "PAPER10_LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION_REVIEW_RESPONSE_V1_VALIDATED "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
