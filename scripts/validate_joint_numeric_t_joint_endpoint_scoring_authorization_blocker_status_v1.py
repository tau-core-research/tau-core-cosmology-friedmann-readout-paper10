#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_endpoint_scoring_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_endpoint_scoring_authorization_blocker_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    status = read_one(STATUS)
    summary = read_one(SUMMARY)
    require(status == summary, "status and summary rows must match exactly")
    require(status["status"] == "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_BLOCKED_NOT_SCORING_NOT_VALIDATION", "bad status")
    require(status["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(status["review_package_exists"] == "true", "review package should exist")
    require(status["controls_beating_or_equal_candidate"] == "0", "expected 0 controls beating/equal candidate")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(status[field] == "false", f"{field} must remain false")
    if status["review_response_exists"] == "false":
        require(status["current_blocker"] == "control_suite_review_response_missing", "missing response blocker mismatch")
        require(
            status["next_required_action"] == "send_control_suite_review_zip_to_reviewer_then_import_completed_response",
            "missing response next action mismatch",
        )
        require(status["endpoint_scoring_authorization_package_preparation_allowed"] == "false", "prep cannot be allowed without review response")
        require(status["endpoint_authorization_package_exists"] == "false", "endpoint package must not exist before review response")
    doc = DOC.read_text()
    for marker in [status["current_blocker"], status["next_required_action"], CLAIM_BOUNDARY, "does not authorize endpoint scoring"]:
        require(marker in doc, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_ENDPOINT_SCORING_AUTHORIZATION_BLOCKER_STATUS_V1_VALIDATED "
        f"blocker={status['current_blocker']}"
    )


if __name__ == "__main__":
    main()
