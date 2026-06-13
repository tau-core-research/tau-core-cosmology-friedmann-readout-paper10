#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1.csv"
)
DEFAULT_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_v1_summary.csv"
)
PACKAGE_SUMMARY = (
    ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv"
)
CLAIM_BOUNDARY = "paper10_desi_shape_validation_permission_replay_authorization_not_validation"
AUTH_SCOPE = "one_future_frozen_DESI_shape_route_permission_only_diagnostic_replay_not_validation"
EXPECTED_RESPONSES = {
    "Q1_scope_frozen": {"yes"},
    "Q2_caveats_retained": {"yes"},
    "Q3_no_leakage": {"yes"},
    "Q4_authorization": {
        "GO_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_ONLY",
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


def truthy(value: str) -> str:
    return str(value).strip().lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a completed DESI shape validation-permission replay authorization response."
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
        package["status"] == "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
        "bad package status",
    )
    require(package["review_completed"] == "false", "package must be the uncompleted handoff")
    require(package["future_permission_only_replay_preparation_allowed"] == "true", "future replay preparation missing")
    require(package["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(package["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(package["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(package["claim_boundary"] == CLAIM_BOUNDARY, "package claim boundary mismatch")
    require(len(rows) == len(EXPECTED_RESPONSES), "completed response must contain exactly four rows")

    by_id = {row["question_id"]: row for row in rows}
    require(set(by_id) == set(EXPECTED_RESPONSES), "completed response question ids mismatch")
    decision = by_id["Q4_authorization"]["reviewer_response"]
    accepted = decision == "GO_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_ONLY"

    for question_id, allowed in EXPECTED_RESPONSES.items():
        row = by_id[question_id]
        require(truthy(row["review_completed"]) == "true", f"{question_id}: review must be completed")
        require(row["reviewer_response"] in allowed, f"{question_id}: bad reviewer response")
        require(row["reviewer_rationale"].strip(), f"{question_id}: missing reviewer rationale")
        require(truthy(row["forbidden_inputs_used"]) == "false", f"{question_id}: forbidden inputs used")
        require(row["route_candidate_score"] == package["route_candidate_score"], f"{question_id}: route candidate changed")
        require(row["route_best_control_score"] == package["route_best_control_score"], f"{question_id}: best control changed")
        require(row["route_margin"] == package["route_margin"], f"{question_id}: route margin changed")
        require(row["robustness_verdict"] == package["robustness_verdict"], f"{question_id}: robustness verdict changed")
        require(truthy(row["narrow_margin_caveat_retained"]) == "true", f"{question_id}: narrow caveat removed")
        require(truthy(row["row_sensitive_caveat_retained"]) == "true", f"{question_id}: row-sensitive caveat removed")
        require(truthy(row["row2_negative_diagnostic_retained"]) == "true", f"{question_id}: Row2 caveat removed")
        require(truthy(row["future_permission_only_replay_preparation_allowed"]) == "true", f"{question_id}: future prep flag changed")
        require(truthy(row["endpoint_replay_allowed"]) == "false", f"{question_id}: response must not claim endpoint replay as validation")
        require(truthy(row["endpoint_validation_claimed"]) == "false", f"{question_id}: validation claimed")
        require(truthy(row["physical_validation_claimed"]) == "false", f"{question_id}: physical validation claimed")
        require(row["authorization_scope"] == AUTH_SCOPE, f"{question_id}: authorization scope mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{question_id}: claim boundary mismatch")

    status = (
        "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY_NOT_VALIDATION"
        if accepted
        else "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_NOT_ACCEPTED_NO_REPLAY"
    )
    summary = [
        {
            "policy_id": "PAPER10_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_REVIEW_V1",
            "status": status,
            "decision": decision,
            "response_path": str(response_path.relative_to(ROOT)) if response_path.is_relative_to(ROOT) else str(response_path),
            "response_sha256": sha256(response_path),
            "reviewed_package_sha256": package["zip_sha256"],
            "package_manifest_pass": "true",
            "review_completed": "true",
            "question_count": str(len(rows)),
            "accepted_question_count": str(sum(1 for q, r in by_id.items() if r["reviewer_response"] in EXPECTED_RESPONSES[q])),
            "future_permission_only_replay_preparation_allowed": "true",
            "permission_only_replay_authorized": "true" if accepted else "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "forbidden_inputs_used": "false",
            "route_candidate_score": package["route_candidate_score"],
            "route_best_control_score": package["route_best_control_score"],
            "route_margin": package["route_margin"],
            "robustness_verdict": package["robustness_verdict"],
            "narrow_margin_caveat_retained": "true",
            "row_sensitive_caveat_retained": "true",
            "row2_negative_diagnostic_retained": "true",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": (
                "one_future_frozen_DESI_shape_route_permission_only_diagnostic_replay_authorized_by_completed_response_not_validation"
                if accepted
                else "no_permission_only_replay_authorized"
            ),
            "recommended_next_action": (
                "run_only_the_single_frozen_permission_only_diagnostic_replay_in_a_separate_execution_context; do_not_claim_endpoint_or_physical_validation"
                if accepted
                else "do_not_run_replay_return_to_protocol_or_source_work"
            ),
        }
    ]
    write_csv(summary_out, summary)
    print(f"PAPER10_DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_RESPONSE_VALIDATED decision={decision}")


if __name__ == "__main__":
    main()
