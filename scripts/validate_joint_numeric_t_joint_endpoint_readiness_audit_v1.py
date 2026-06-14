#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/derived/joint_numeric_t_joint_endpoint_readiness_audit_v1.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_endpoint_readiness_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_endpoint_readiness_audit_not_scoring_not_validation"


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
    row = read_one(AUDIT)
    require(row["audit_id"] == "JOINT_NUMERIC_T_JOINT_ENDPOINT_READINESS_AUDIT_V1", "bad audit id")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(row["control_suite_valid"] == "true", "control suite should be valid")
    require(row["zero_control_result"] == "true", "expected zero-control result")
    require(row["controls_beating_or_equal_candidate"] == "0", "expected 0 controls beating/equal candidate")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(row[field] == "false", f"{field} must be false")
    if row["review_response_exists"] == "false":
        require(row["endpoint_authorization_package_build_ready"] == "false", "cannot be build-ready without review response")
        require(row["readiness"] == "BLOCKED_BEFORE_ENDPOINT_AUTHORIZATION_PACKAGE", "bad blocked readiness")
        require(row["current_blocker"] == "control_suite_review_response_missing", "bad missing-review blocker")
    doc = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, row["readiness"], row["current_blocker"], "does not authorize endpoint scoring"]:
        require(marker in doc, f"doc missing marker: {marker}")
    print(f"JOINT_NUMERIC_T_JOINT_ENDPOINT_READINESS_AUDIT_V1_VALIDATED readiness={row['readiness']}")


if __name__ == "__main__":
    main()
