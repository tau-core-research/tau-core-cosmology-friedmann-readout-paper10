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
    / "low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "w_time_uncertainty_basis_replay_authorization_review_not_validation"
AUTH_SCOPE = "single_permission_only_low_z_W_time_uncertainty_basis_replay_not_validation"
EXPECTED_PACKAGE_SHA256 = "2067b221b0309bb8fcc3a294fcebf5c8fddd6123d7d7d7a151615c992a2fd69f"
EXPECTED_RESPONSES = {
    "Q1_source_side_basis_closure": {"yes"},
    "Q2_candidate_scope": {"yes", "caveated_yes"},
    "Q3_no_leakage": {"yes"},
    "Q4_authorization": {"GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY"},
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
        description="Validate completed low-z W_time uncertainty-basis replay authorization response."
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
    rows = read_rows(response_path)
    require(
        package_summary["status"]
        == "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package_summary["zip_sha256"] == EXPECTED_PACKAGE_SHA256, "reviewed package checksum mismatch")
    require(package_summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package_summary["physical_validation_claimed"] == "false", "package must not claim physical validation")
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
        require(row["physical_validation_claimed"] == "false", f"{question_id} must keep physical validation false")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(row["source_side_basis_verdict"] == "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized", f"{question_id}: source basis verdict mismatch")
        require(row["basis_rows"] == "424", f"{question_id}: basis row count mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")

    summary = [
        {
            "policy_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "decision": "GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY",
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "source_side_basis_verdict": "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized",
            "basis_rows": "424",
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "run_only_one_separate_predeclared_low_z_W_time_uncertainty_basis_replay_without_validation_claim",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_RESPONSE_V1_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
