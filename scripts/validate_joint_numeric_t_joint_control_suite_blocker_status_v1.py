#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_blocker_status_not_scoring_not_validation"
EXPECTED_BLOCKERS = {
    "control_suite_authorization_response_missing",
    "control_suite_authorization_response_incomplete",
    "control_suite_authorization_rejected_or_incomplete",
    "control_suite_authorized_numeric_control_build_missing",
    "control_suite_built_endpoint_scoring_authorization_missing",
}


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
    require(DOC.exists(), "missing doc")
    for item, label in [(row, "row"), (summary, "summary")]:
        require(item["claim_boundary"] == CLAIM_BOUNDARY, f"{label}: claim boundary mismatch")
        require(item["numeric_control_suite_exists"] in {"true", "false"}, f"{label}: bad numeric_control_suite_exists")
        require(item["control_suite_authorization_allowed"] in {"true", "false"}, f"{label}: bad control_suite_authorization_allowed")
        require(item["current_blocker"] in EXPECTED_BLOCKERS, f"{label}: unexpected blocker")
        require(float(item["frozen_numeric_t_joint"]) > 0.0, f"{label}: bad frozen T_joint")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(item[field] == "false", f"{label}: unsafe field {field}")
    text = DOC.read_text()
    for marker in [row["current_blocker"], CLAIM_BOUNDARY, "not scoring", "not validation"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_BLOCKER_STATUS_V1_VALIDATED blocker={row['current_blocker']}")


if __name__ == "__main__":
    main()
