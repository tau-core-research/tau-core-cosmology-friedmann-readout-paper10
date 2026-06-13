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
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv"
)
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_observer_orientation_kernel_v2_replay_not_validation"
EXPECTED_RESPONSES = {
    "Q1_kernel_freeze": {"yes"},
    "Q2_centering_rule": {"yes", "caveated_yes"},
    "Q3_control_scope": {"yes"},
    "Q4_authorization": {"GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY"},
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
        description="Validate completed V2 observer-orientation kernel replay authorization response."
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
        == "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(
        package_summary["zip_sha256"]
        == "747d73b85d9196a850e4651ac4871c672d5c9d41c1b3958980c013fa93d17f93",
        "reviewed package checksum mismatch",
    )
    require(package_summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
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
        require(row["primary_kernel"] == "W_path_times_centered_sky_z", f"{question_id}: primary kernel mismatch")
        require(row["reference_kernel"] == "W_path_times_raw_sky_z", f"{question_id}: reference kernel mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")

    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_POLICY",
            "status": "V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "decision": "GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY",
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
            "primary_kernel": "W_path_times_centered_sky_z",
            "reference_kernel": "W_path_times_raw_sky_z",
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "run_only_one_separate_predeclared_12_row_observer_orientation_kernel_v2_replay_without_validation_or_physical_path_weight_claim",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTH_RESPONSE_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
