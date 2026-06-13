#!/usr/bin/env python3
"""Validate a completed ACT caveated K_path replay-authorization response."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
RESPONSE = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_v1_summary.csv"


EXPECTED_QS = {
    "Q1_source_design_acceptance",
    "Q2_controls_required",
    "Q3_old_branch_quarantine",
    "Q4_forbidden_inputs",
    "Q5_permission_only_replay",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def is_false(value: str) -> bool:
    return value.strip().lower() in {"false", "0", "no", "n"}


def main() -> None:
    if not RESPONSE.exists():
        raise SystemExit("missing imported replay-authorization response")
    if not SUMMARY.exists():
        raise SystemExit("missing replay-authorization response summary")
    rows = read_rows(RESPONSE)
    summary = read_one(SUMMARY)
    if len(rows) != 5:
        raise SystemExit(f"expected five response rows, found {len(rows)}")
    if {row["question_id"] for row in rows} != EXPECTED_QS:
        raise SystemExit("unexpected question set in response")
    if any(not row.get("reviewer_answer", "") for row in rows):
        raise SystemExit("all reviewer_answer fields must be completed")
    if any(not is_false(row.get("forbidden_inputs_used", "")) for row in rows):
        raise SystemExit("forbidden_inputs_used must remain false on every response row")

    q5 = {row["question_id"]: row["reviewer_answer"] for row in rows}["Q5_permission_only_replay"]
    expected_verdict = (
        "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_ALLOWED_NOT_SCORING"
        if q5 == "authorize_permission_only_replay_package"
        else "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_NOT_ALLOWED"
    )
    expected_allowed = "true" if q5 == "authorize_permission_only_replay_package" else "false"
    expected_summary = {
        "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_REVIEW_RESPONSE_V1",
        "review_completed": "true",
        "review_rows": "5",
        "q5_answer": q5,
        "forbidden_inputs_used": "false",
        "permission_only_guarded_replay_package_preparation_allowed": expected_allowed,
        "endpoint_replay_allowed_by_this_review": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": "replay_authorization_response_import_not_scoring",
        "verdict": expected_verdict,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            raise SystemExit(f"{key}: expected {expected!r}, got {summary.get(key)!r}")
    print("ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_RESPONSE_VALIDATED")


if __name__ == "__main__":
    main()
