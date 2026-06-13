#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_route_replay_authorization_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "paper10_desi_shape_route_replay_authorization_review_not_validation"
AUTH_SCOPE = "one_permission_only_DESI_shape_route_replay_later_not_validation"
ALLOWED_AUTH_SCOPES = {
    AUTH_SCOPE,
    "single_permission_only_DESI_shape_route_CLOCK_SLOPE_SHAPE_replay_later_not_validation",
}
EXPECTED_RESPONSES = {
    "Q1_shape_route_scope": {"yes"},
    "Q2_control_binding": {"yes", "caveated_yes"},
    "Q3_no_leakage": {"yes"},
    "Q4_authorization": {
        "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY",
        "NO_GO_NEEDS_MORE_PROTOCOL_WORK",
        "NO_GO_LEAKAGE_OR_SCOPE_RISK",
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
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
        description="Validate a completed DESI shape-route replay-authorization review response."
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
        package["status"] == "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be the uncompleted handoff")
    require(package["shape_observable_candidate_available"] == "true", "shape candidate must be available")
    require(package["primary_candidate"] == "CLOCK_SLOPE_SHAPE", "primary candidate mismatch")
    require(package["shape_bound_control_count"] == "5", "shape controls must be fully bound")
    require(package["unbound_control_families"] == "none", "unbound controls remain")
    require(package["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY", "CC-window policy changed")
    require(package["multi_clock_support_endpoint_ready"] == "false", "multi-clock blocker must be preserved")
    require(package["high_z_row_can_enter_replay"] == "false", "high-z row must remain excluded")
    require(package["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")
    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly four rows")

    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")
    decision = by_id["Q4_authorization"]["reviewer_response"]
    accepted = decision == "GO_DESI_SHAPE_ROUTE_REPLAY_PERMISSION_ONLY"

    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        expected_replay_flag = (
            "true"
            if accepted and question_id == "Q4_authorization"
            else "false"
        )
        require(row["review_completed"] == "true", f"{question_id}: review must be completed")
        require(row["reviewer_response"] in allowed, f"{question_id}: bad reviewer response")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")
        require(row["forbidden_inputs_used"] == "false", f"{question_id}: forbidden inputs used")
        require(row["shape_observable_candidate_available"] == "true", f"{question_id}: shape availability changed")
        require(row["primary_candidate"] == "CLOCK_SLOPE_SHAPE", f"{question_id}: primary candidate changed")
        require(row["shape_bound_control_count"] == "5", f"{question_id}: control count changed")
        require(row["unbound_control_families"] == "none", f"{question_id}: unbound controls changed")
        require(
            row["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY",
            f"{question_id}: CC-window policy changed",
        )
        require(row["multi_clock_support_endpoint_ready"] == "false", f"{question_id}: multi-clock flag changed")
        require(row["high_z_row_can_enter_replay"] == "false", f"{question_id}: high-z flag changed")
        require(row["endpoint_replay_allowed"] == expected_replay_flag, f"{question_id}: bad replay flag")
        require(row["endpoint_validation_claimed"] == "false", f"{question_id}: validation claimed")
        require(row["physical_validation_claimed"] == "false", f"{question_id}: physical validation claimed")
        require(row["authorization_scope"] in ALLOWED_AUTH_SCOPES, f"{question_id}: authorization scope mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    status = (
        "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY"
        if accepted
        else "DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_NOT_ACCEPTED_NO_REPLAY"
    )
    next_action = (
        "run_one_separate_predeclared_DESI_shape_route_replay_without_validation_claim"
        if accepted
        else "do_not_run_replay_return_to_protocol_or_source_work"
    )
    summary = [
        {
            "policy_id": "PAPER10_DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_REVIEW_V1",
            "status": status,
            "decision": decision,
            "question_count": str(len(rows)),
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package["zip_sha256"],
            "review_completed": "true",
            "forbidden_inputs_used": "false",
            "shape_observable_candidate_available": "true",
            "primary_candidate": "CLOCK_SLOPE_SHAPE",
            "shape_bound_control_count": "5",
            "unbound_control_families": "none",
            "cc_window_stress_release_policy": "SOURCE_REOPEN_ONLY_NO_REPLAY",
            "multi_clock_support_endpoint_ready": "false",
            "high_z_row_can_enter_replay": "false",
            "endpoint_replay_allowed": "true" if accepted else "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "authorization_scope": AUTH_SCOPE,
            "claim_boundary": CLAIM_BOUNDARY,
            "recommended_next_action": next_action,
        }
    ]
    write_csv(summary_out, summary)
    print(f"PAPER10_DESI_SHAPE_ROUTE_REPLAY_AUTHORIZATION_RESPONSE_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()
