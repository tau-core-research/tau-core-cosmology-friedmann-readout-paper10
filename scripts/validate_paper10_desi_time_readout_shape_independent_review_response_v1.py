#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/paper10_desi_time_readout_shape_independent_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "paper10_desi_time_readout_shape_independent_review_not_validation"
AUTH_SCOPE = "retain_caveated_source_side_shape_candidate_only_not_replay"
EXPECTED_RESPONSES = {
    "Q1_source_side_derivation": {"yes"},
    "Q2_no_leakage": {"yes"},
    "Q3_caveat_acceptance": {"yes", "caveated_yes"},
    "Q4_next_action_limit": {"yes", "caveated_yes"},
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
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
        description="Validate completed DESI time-readout shape independent review response."
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

    package = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    require(
        package["status"] == "DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["zip_sha256"].strip(), "reviewed package checksum missing")
    require(package["review_completed"] == "false", "package must be the uncompleted handoff")
    require(package["shape_observable_candidate_available"] == "true", "shape candidate must be available")
    require(package["endpoint_ready_shape_observable"] == "false", "shape candidate must remain endpoint-blocked")
    require(package["multi_clock_support_endpoint_ready"] == "false", "multi-clock blocker must be preserved")
    require(package["high_z_row_can_enter_replay"] == "false", "high-z blocker must be preserved")
    require(package["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly the required rows")

    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")
    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        require(row["review_completed"] == "true", f"{question_id}: review must be completed")
        require(row["reviewer_response"] in allowed, f"{question_id}: bad reviewer response")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")
        require(row["forbidden_inputs_used"] == "false", f"{question_id}: forbidden inputs used")
        require(row["shape_observable_candidate_available"] == "true", f"{question_id}: shape availability changed")
        require(row["endpoint_ready_shape_observable"] == "false", f"{question_id}: endpoint-ready flag changed")
        require(row["multi_clock_support_endpoint_ready"] == "false", f"{question_id}: multi-clock blocker changed")
        require(row["high_z_row_can_enter_replay"] == "false", f"{question_id}: high-z blocker changed")
        require(row["endpoint_replay_allowed"] == "false", f"{question_id}: review must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: review must not claim validation")
        require(row["physical_validation_claimed"] == "false", f"{question_id}: review must not claim physical validation")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    summary = [
        {
            "policy_id": "PAPER10_DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_POLICY_V1",
            "status": "DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_ACCEPTED_CAVEATED_SOURCE_SIDE_NOT_REPLAY",
            "decision": "RETAIN_CAVEATED_SOURCE_SIDE_SHAPE_CANDIDATE_ONLY",
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package["zip_sha256"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "shape_observable_candidate_available": "true",
            "endpoint_ready_shape_observable": "false",
            "multi_clock_support_endpoint_ready": "false",
            "high_z_row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "retain_shape_as_caveated_source_side_candidate_or_fetch_new_clock_compilation",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_DESI_TIME_READOUT_SHAPE_INDEPENDENT_REVIEW_RESPONSE_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
