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
    / "paper10_desi_time_level_endpoint_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "paper10_desi_time_level_endpoint_authorization_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_authorization_review_not_validation"
AUTH_SCOPE = "single_permission_only_desi_cc_5row_time_level_replay_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_scope_freeze",
    "Q2_source_side_freeze",
    "Q3_controls_required",
    "Q4_permission_only_replay",
    "Q5_forbidden_inputs",
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
        description="Validate a completed DESI/CC time-level endpoint authorization review response."
    )
    parser.add_argument("response", nargs="?", default=str(DEFAULT_RESPONSE))
    parser.add_argument("--summary-out", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def resolve_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    return path


def rel_or_abs(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    args = parse_args()
    response_path = resolve_path(args.response)
    summary_out = resolve_path(args.summary_out)

    package_summary = read_one(PACKAGE_SUMMARY)
    rows = read_rows(response_path)
    require(
        package_summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package_summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package_summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package_summary["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package_summary["contains_endpoint_residuals"] == "false", "package must not contain residuals")
    require(package_summary["contains_endpoint_scores"] == "false", "package must not contain scores")
    require(package_summary["contains_fit_statistics"] == "false", "package must not contain fit statistics")
    require(package_summary["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")

    require(len(rows) == len(EXPECTED_QUESTIONS), "completed response must contain exactly the required rows")
    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == EXPECTED_QUESTIONS, "completed response question ids mismatch")
    for question_id in sorted(EXPECTED_QUESTIONS):
        row = by_id[question_id]
        require(row["review_completed"] == "true", f"{question_id} must be completed")
        require(row["reviewer_response"] == "accept", f"{question_id} must be accepted")
        require(row["reviewer_rationale"].strip(), f"{question_id}: reviewer rationale required")
        require(row["forbidden_inputs_used"] == "false", f"{question_id}: forbidden inputs must remain false")
        require(row["endpoint_replay_allowed"] == "true", f"{question_id}: permission-only replay must be allowed")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", f"{question_id}: physical validation must remain false")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(
            row["readiness_verdict"]
            == "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing",
            f"{question_id}: readiness verdict mismatch",
        )
        require(row["desi_first_endpoint_rows"] == "5", f"{question_id}: DESI endpoint row count mismatch")
        require(row["desi_control_family_count"] == "7", f"{question_id}: control-family count mismatch")
        require(row["desi_control_seed_range"] == "41001;41007", f"{question_id}: control seed range mismatch")
        require(
            row["high_z_policy"] == "z2p33_excluded_as_holdout_or_future_independent_clock_support",
            f"{question_id}: high-z policy mismatch",
        )
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    summary = [
        {
            "policy_id": "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY",
            "decision": "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY",
            "question_count": str(len(rows)),
            "response_path": rel_or_abs(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package_summary["zip_sha256"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "desi_first_endpoint_rows": "5",
            "desi_control_family_count": "7",
            "desi_control_seed_range": "41001;41007",
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": "prepare_one_guarded_desi_cc_5row_time_level_replay_without_validation_claim",
        }
    ]
    write_csv(summary_out, summary)
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_RESPONSE_VALIDATED "
        f"decision={summary[0]['decision']}"
    )


if __name__ == "__main__":
    main()
