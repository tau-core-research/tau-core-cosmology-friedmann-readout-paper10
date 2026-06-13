#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv"
)
COMPLETED_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_review_completed_summary_v1.csv"
)
CLAIM_BOUNDARY = "v2_observer_basis_replay_authorization_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_W_path_x_sky_x_x_zcenter_replay_not_validation"
EXPECTED_RESPONSES = {
    "Q1_replay_scope": {"yes"},
    "Q2_family_freeze": {"yes"},
    "Q3_controls": {"yes"},
    "Q4_authorization": {"GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY"},
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate completed observer-basis replay authorization response.")
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
    package = read_one(PACKAGE_SUMMARY)
    completed = read_one(COMPLETED_SUMMARY)
    rows = read_rows(response_path)

    require(package["status"] == "V2_OBSERVER_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package["candidate_family"] == "W_path_x_sky_x_x_zcenter", "bad candidate")
    require(completed["reviewed_package_zip_sha256_current"].strip(), "completed review must record reviewed package checksum")
    require(package["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(completed["decision"] == "GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY", "bad decision")
    require(completed["endpoint_replay_allowed"] == "true", "completed response must authorize permission-only replay")
    require(completed["endpoint_validation_claimed"] == "false", "completed response must not claim validation")
    require(completed["physical_lensing_path_weight_claimed"] == "false", "completed response must not claim path physics")
    require(completed["authorization_scope"] == AUTH_SCOPE, "authorization scope mismatch")
    require(completed["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(len(rows) == len(EXPECTED_RESPONSES), "completed response row count mismatch")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")
    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        require(row["candidate_family"] == package["candidate_family"], f"{question_id}: candidate mismatch")
        require(row["review_completed"] == "true", f"{question_id}: review incomplete")
        require(row["reviewer_response"] in allowed, f"{question_id}: bad response")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing rationale")
        require(row["forbidden_inputs_used"] == "false", f"{question_id}: forbidden inputs")
        require(row["endpoint_replay_allowed"] == "true", f"{question_id}: replay permission mismatch")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: validation claim")
        require(row["physical_lensing_path_weight_claimed"] == "false", f"{question_id}: path physics claim")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_BASIS_REPLAY_AUTHORIZATION_POLICY",
            "status": "V2_OBSERVER_BASIS_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "candidate_family": package["candidate_family"],
            "decision": completed["decision"],
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_zip_sha256_current": package["zip_sha256"],
            "reviewed_package_zip_sha256_from_completed_review": completed["reviewed_package_zip_sha256_current"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "run_one_predeclared_permission_only_12_row_W_path_x_sky_x_x_zcenter_replay_with_frozen_controls",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_OBSERVER_BASIS_REPLAY_AUTH_RESPONSE_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
