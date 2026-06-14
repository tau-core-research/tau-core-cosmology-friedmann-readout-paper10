#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
DOC = ROOT / "docs/joint_symbolic_statistic_binding_status_v1.md"
CLAIM_BOUNDARY = "joint_symbolic_statistic_binding_status_not_scoring_not_validation"
VERDICT = "SYMBOLIC_SAME_STATISTIC_BINDING_PASSED_NUMERIC_VALIDATION_BINDING_BLOCKED"


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
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == int(summary["criteria_total"]), "criteria count mismatch")
    require(summary["verdict"] == VERDICT, "unexpected verdict")
    require(summary["symbolic_joint_statistic"] == "T_joint = sum_i q_i z_i", "bad symbolic statistic")
    require(summary["symbolic_binding_passed"] == "true", "symbolic binding should pass")
    require(summary["numeric_executable_binding_passed"] == "false", "numeric validation binding must remain blocked")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{field} must remain false")
    blocked_ids = {row["criterion_id"] for row in rows if row["status"] == "blocked"}
    require("JSSB_05_NUMERIC_EXECUTABLE_STATISTIC" in blocked_ids, "numeric statistic blocker missing")
    require("JSSB_06_CROSS_PROBE_COVARIANCE" in blocked_ids, "covariance blocker missing")
    text = DOC.read_text()
    for marker in ["symbolic binding passed", "numeric executable binding passed", VERDICT, CLAIM_BOUNDARY]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_SYMBOLIC_STATISTIC_BINDING_STATUS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
