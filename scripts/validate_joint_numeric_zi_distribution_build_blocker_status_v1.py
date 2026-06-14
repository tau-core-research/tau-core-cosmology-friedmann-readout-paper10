#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_zi_distribution_build_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_build_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_zi_distribution_build_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_zi_distribution_build_blocker_status_not_scoring_not_validation"


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
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    require(row["status"] == "JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_BLOCKED_NOT_SCORING_NOT_VALIDATION", "bad status")
    require(summary["status"] == row["status"], "summary status mismatch")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(row["numeric_t_joint_allowed"] == "false", "T_joint must not be allowed")
    require(summary["numeric_t_joint_allowed"] == "false", "summary T_joint must not be allowed")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(row[field] == "false", f"{field} must remain false")
        require(summary[field] == "false", f"summary {field} must remain false")
    require(
        row["current_blocker"]
        in {
            "numeric_zi_distribution_build_authorization_response_missing",
            "numeric_zi_distribution_build_authorized_but_not_run",
            "numeric_zi_distribution_build_authorization_rejected_or_incomplete",
            "numeric_zi_distribution_ledger_built_numeric_t_joint_authorization_missing",
        },
        "unexpected blocker",
    )
    if row["authorization_response_exists"] == "false":
        require(row["review_completed"] == "false", "missing response cannot be completed")
        require(row["numeric_zi_build_allowed"] == "false", "missing response cannot authorize z_i build")
        require(
            row["current_blocker"] == "numeric_zi_distribution_build_authorization_response_missing",
            "missing response blocker mismatch",
        )
    text = DOC.read_text()
    for marker in [
        "blocked",
        "not scoring",
        "not validation",
        "no completed reviewer response",
        row["current_blocker"],
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_NUMERIC_ZI_DISTRIBUTION_BUILD_BLOCKER_STATUS_V1_VALIDATED blocker={row['current_blocker']}")


if __name__ == "__main__":
    main()
