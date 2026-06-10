#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_package_v1_summary.csv"
)
SOURCE_SIDE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_partial_scope_replay_authorization_review_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_partial_W_path_replay_not_validation"
EXPECTED_RESPONSES = {
    "Q1_source_side_review_closure": {"yes"},
    "Q2_partial_scope_replay_scope": {"yes", "caveated_yes"},
    "Q3_no_leakage": {"yes"},
    "Q4_authorization": {"GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY"},
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate completed V2 partial W_path replay authorization response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    response_path = Path(args.response)
    if not response_path.is_absolute():
        response_path = ROOT / response_path
    summary_out = Path(args.summary_out)
    if not summary_out.is_absolute():
        summary_out = ROOT / summary_out

    package_summary = read_one(PACKAGE_SUMMARY)
    source_side = read_one(SOURCE_SIDE_SUMMARY)
    rows = read_rows(response_path)
    require(package_summary["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package_summary["zip_sha256"] == "03f4a7d801e0987df6797fa4a8d321d8af1d6ee7b04201bb6cbe81cca2b08b4a", "reviewed package checksum mismatch")
    require(package_summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(source_side["final_verdict"] == "ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE", "bad source-side verdict")
    require(source_side["endpoint_replay_allowed"] == "false", "source-side review must not authorize replay")
    require(source_side["endpoint_validation_claimed"] == "false", "source-side review must not claim validation")
    require(source_side["physical_lensing_path_weight_claimed"] == "false", "source-side review must not claim path physics")
    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly the required rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")
    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        require(row["review_completed"] == "true", f"{question_id} must be completed")
        require(row["reviewer_response"] in allowed, f"bad response for {question_id}")
        require(row["forbidden_inputs_used"] == "false", f"{question_id} must keep forbidden_inputs_used=false")
        require(row["endpoint_replay_allowed"] == "true", f"{question_id} must authorize replay permission")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id} must keep validation false")
        require(row["physical_lensing_path_weight_claimed"] == "false", f"{question_id} must keep path physics false")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")

    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "decision": "GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY",
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "source_side_review_verdict": source_side["verdict"],
            "strict_path_scope_candidate_count": "5",
            "caveated_path_scope_candidate_count": "7",
            "total_path_scope_candidate_count": "12",
            "remaining_lowz_rows_full_W_path_disabled": "412",
            "partial_path_values_computed": "true",
            "full_lowz_path_values_computed": "false",
            "nonzero_partial_path_value_count": "12",
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "run_only_one_separate_predeclared_12_row_partial_W_path_replay_without_validation_or_physical_path_weight_claim",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_RESPONSE_V1_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
