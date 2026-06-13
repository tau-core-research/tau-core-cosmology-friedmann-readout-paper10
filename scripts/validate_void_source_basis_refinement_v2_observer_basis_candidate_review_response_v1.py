#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_summary.csv"
)
PACKAGE_MANIFEST = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_package_v1_manifest.csv"
)
COMPLETED_SUMMARY = (
    ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_completed_summary_v1.csv"
)
CLAIM_BOUNDARY = "v2_observer_basis_candidate_review_not_validation"
EXPECTED_RESPONSES = {
    "Q1_candidate_predeclared": {"yes"},
    "Q2_source_side_inputs": {"yes"},
    "Q3_control_result": {"caveated_yes"},
    "Q4_next_action": {"caveated_yes"},
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
    parser = argparse.ArgumentParser(description="Validate completed observer-basis candidate review response.")
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
    manifest = read_rows(PACKAGE_MANIFEST)
    completed = read_one(COMPLETED_SUMMARY)
    rows = read_rows(response_path)
    require(package["status"] == "V2_OBSERVER_BASIS_CANDIDATE_REVIEW_PACKAGE_BUILT_NOT_COMPLETED", "bad package status")
    require(package["candidate_family"] == "W_path_x_sky_x_x_zcenter", "bad package candidate")
    expected_manifest = {
        "data/source_manifest/void_source_basis_refinement_v2_observer_basis_candidate_review_policy_v1.csv": "2ce16501782d48b4a35b7bdb6f67ca1ca42e18270ec805f5a633360fb3dd78db",
        "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv": "1f66c898b6b45914ade593b6236d32c0becb4962fa4b07b6b20e1a45d7e4097a",
        "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv": "f7897e758ff3bf927753cb9f0da0f657840cdbcaa2f3649bd7eb8cd097e4ab63",
        "docs/void_source_basis_refinement_v2_observer_basis_candidate_review_v1.md": "63fd070ce6125cb4d9c30f361c0eb2c563440a264da7104d44543f081e49aba0",
        "data/derived/void_source_basis_refinement_v2_observer_basis_candidate_review_response_template_v1.csv": "30ba07bc4217ec060ce90c58410e51df4ca6ea109d50a9ad4633a34c6817c9f7",
    }
    require({row["path"]: row["sha256"] for row in manifest} == expected_manifest, "reviewed package content checksum mismatch")
    require(package["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(completed["final_decision"] == "ACCEPT_OBSERVER_BASIS_CANDIDATE_FOR_SEPARATE_PERMISSION_ONLY_REPLAY_AUTHORIZATION_PACKAGE", "bad final decision")
    require(completed["candidate_family"] == package["candidate_family"], "completed candidate mismatch")
    require(completed["endpoint_replay_allowed"] == "false", "completed review must not authorize replay")
    require(completed["endpoint_validation_claimed"] == "false", "completed review must not claim validation")
    require(completed["physical_lensing_path_weight_claimed"] == "false", "completed review must not claim path physics")
    require(completed["claim_boundary"] == CLAIM_BOUNDARY, "completed claim boundary mismatch")
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
        require(row["endpoint_replay_allowed"] == "false", f"{question_id}: must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", f"{question_id}: must not claim path physics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_BASIS_CANDIDATE_REVIEW_POLICY",
            "status": "V2_OBSERVER_BASIS_CANDIDATE_REVIEW_ACCEPTED_FOR_SEPARATE_AUTHORIZATION_PACKAGE_NOT_REPLAY",
            "candidate_family": package["candidate_family"],
            "decision": completed["final_decision"],
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_zip_sha256_current": package["zip_sha256"],
            "reviewed_package_content_checksum_status": "matches_completed_review_log",
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "authorization_scope": completed["authorization_scope"],
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "build_separate_permission_only_replay_authorization_package_for_W_path_x_sky_x_x_zcenter",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_OBSERVER_BASIS_CANDIDATE_REVIEW_RESPONSE_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
