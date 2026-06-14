#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_same_statistic_execution_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_execution_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_same_statistic_execution_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_same_statistic_execution_blocker_status_not_execution_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    require(row["status"] == "JOINT_SAME_STATISTIC_EXECUTION_BLOCKED_NOT_SCORING_NOT_VALIDATION", "bad status")
    require(summary["status"] == row["status"], "summary status mismatch")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(row[field] == "false", f"{field} must remain false")
        require(summary[field] == "false", f"summary {field} must remain false")
    require(
        row["execution_authorization_response_exists"] in {"true", "false"},
        "bad response existence flag",
    )
    if row["execution_authorization_response_exists"] == "false":
        require(
            row["current_blocker"] == "same_statistic_execution_authorization_response_missing",
            "missing-response blocker mismatch",
        )
        require(
            row["permission_only_execution_allowed"] == "false",
            "missing response cannot allow execution",
        )
    if row["execution_authorization_response_exists"] == "true":
        require(
            row["current_blocker"]
            in {
                "same_statistic_execution_authorized_but_replay_not_run",
                "same_statistic_execution_authorization_rejected_or_not_accepted",
                "permission_only_replay_completed_not_validation",
            },
            "unexpected post-response blocker",
        )
    text = DOC.read_text()
    for marker in [
        "not a replay",
        "not endpoint scoring",
        "not cosmological validation",
        row["current_blocker"],
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_SAME_STATISTIC_EXECUTION_BLOCKER_STATUS_V1_VALIDATED blocker={row['current_blocker']}")


if __name__ == "__main__":
    main()
