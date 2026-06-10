#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv"
PACKAGE_SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv"
RESPONSE = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_v1_summary.csv"

EXPECTED_QUESTIONS = {
    "Q1_protocol_integrity",
    "Q2_readiness_caveat",
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    return value.strip().lower()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(RESPONSE)
    summary = read_one(SUMMARY)

    require(len(policy_rows) == 4, "authorization policy must contain four rows")
    require(len(rows) == 4, "completed authorization response must contain four rows")
    require({row["question_id"] for row in rows} == EXPECTED_QUESTIONS, "unexpected question set")
    require(
        package["status"] == "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "review package must be the clean uncompleted handoff package",
    )
    require(package["endpoint_run_allowed"] == "false", "handoff package must not pre-authorize endpoint runs")
    require(package["contains_endpoint_residuals"] == "false", "handoff package must not include endpoint residuals")
    require(package["contains_endpoint_scores"] == "false", "handoff package must not include endpoint scores")
    require(package["contains_fit_statistics"] == "false", "handoff package must not include fit statistics")
    require(summary["input_zip_sha256"] == package["zip_sha256"], "completed review must reference the reviewed package hash")
    require(summary["manifest_hash_check"] == "pass", "manifest hash check must pass")
    require(summary["package_forbidden_endpoint_flags_check"] == "pass", "package forbidden flag check must pass")
    require(summary["template_validator_precompletion_check"] == "pass", "precompletion template validation must pass")
    require(summary["decision"] == "GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY", "unexpected review decision")
    require(summary["review_completed"] == "true", "review must be completed")
    require(summary["forbidden_inputs_used"] == "false", "review must not use forbidden endpoint inputs")
    require(summary["endpoint_run_allowed"] == "true", "completed review must allow the single endpoint run")
    require(summary["physical_validation_claimed"] == "false", "completed review must not claim physical validation")
    require(
        summary["authorization_scope"] == "single_predeclared_combined_void_web_endpoint_run_permission_only_not_validation",
        "authorization scope must stay permission-only",
    )
    require(
        summary["claim_boundary"] == "combined_multiblock_endpoint_authorization_review_not_validation",
        "claim boundary must remain authorization review, not validation",
    )

    by_question = {row["question_id"]: row for row in rows}
    for row in rows:
        require(norm(row["review_completed"]) == "true", "all review rows must be completed")
        require(row["reviewer_id_or_role"].strip(), "reviewer identity/role must be nonempty")
        require(row["reviewer_rationale"].strip(), "review rationale must be nonempty")
        require(norm(row["forbidden_inputs_used"]) == "false", "forbidden inputs must remain unused")
        require(norm(row["endpoint_run_allowed"]) == "true", "every completed row must allow endpoint run")
        require(norm(row["physical_validation_claimed"]) == "false", "no row may claim physical validation")
        require(
            row["authorization_scope"] == "single_predeclared_combined_void_web_endpoint_run_permission_only_not_validation",
            "row authorization scope must stay permission-only",
        )
        require(
            row["claim_boundary"] == "combined_multiblock_endpoint_authorization_review_not_validation",
            "row claim boundary must remain review-only",
        )

    require(norm(by_question["Q1_protocol_integrity"]["reviewer_response"]) == "yes", "Q1 must be yes")
    require(
        norm(by_question["Q2_readiness_caveat"]["reviewer_response"]) in {"yes", "caveated_yes", "yes_caveated"},
        "Q2 must be yes or caveated_yes",
    )
    require(norm(by_question["Q3_no_leakage"]["reviewer_response"]) == "yes", "Q3 must be yes")
    require(
        by_question["Q4_authorization"]["reviewer_response"] == "GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY",
        "Q4 must grant combined endpoint permission only",
    )
    require(summary["input_zip_sha256"] == package["zip_sha256"], "reviewed package hash mismatch")
    require(sha256(RESPONSE), "response hash must be computable")

    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_AUTHORIZATION_REVIEW_RESPONSE_V1_VALIDATED "
        "decision=GO_COMBINED_VOID_WEB_ENDPOINT_PERMISSION_ONLY "
        "claim_boundary=authorization_review_not_validation"
    )


if __name__ == "__main__":
    main()
