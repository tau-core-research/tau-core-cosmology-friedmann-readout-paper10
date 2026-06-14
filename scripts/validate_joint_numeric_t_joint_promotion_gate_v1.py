#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_promotion_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_promotion_gate_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_promotion_gate_not_scoring_not_validation"
VERDICT = "NUMERIC_T_JOINT_LEDGER_BUILT_PROMOTION_STILL_BLOCKED_FOR_ENDPOINT_SCORING"
EXPECTED_BLOCKED = {
    "NTJ_07_NUMERIC_CONTROL_EXECUTION_BINDING",
    "NTJ_08_CROSS_PROBE_COVARIANCE_CLOSURE",
    "NTJ_09_NO_ENDPOINT_SCORING_AUTHORIZATION_YET",
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
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 9, "expected nine numeric-promotion criteria")
    require(summary["criteria_total"] == "9", "summary total mismatch")
    require(summary["criteria_passed"] == "6", "expected six passed prerequisites including numeric ledgers")
    require(summary["criteria_blocked"] == "3", "expected three blocked endpoint-scoring criteria")
    require(summary["numeric_t_joint_promotion_ready"] == "false", "numeric promotion must remain blocked")
    require(summary["numeric_zi_defined"] == "true", "numeric z_i ledger must be defined")
    require(summary["numeric_t_joint_ledger_built"] == "true", "numeric T_joint ledger must be built")
    require(float(summary["numeric_t_joint"]) > 0, "numeric T_joint must be positive in current ledger")
    require(summary["same_statistic_control_numeric_ready"] == "false", "numeric controls must remain blocked")
    require(summary["cross_probe_covariance_closed"] == "false", "covariance must remain open")
    require(summary["verdict"] == VERDICT, "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "computes_numeric_statistic_now",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must remain false")
    blocked = {row["criterion_id"] for row in rows if row["status"] == "blocked"}
    require(blocked == EXPECTED_BLOCKED, f"blocked criteria mismatch: {blocked}")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["required_before_numeric_promotion"] == "true", "criterion must be required")
        for field in [
            "computes_numeric_statistic_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['criterion_id']} {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "numeric-promotion gate",
        "numeric T_joint ledger built",
        "not scoring",
        "not validation",
        VERDICT,
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_NUMERIC_T_JOINT_PROMOTION_GATE_V1_VALIDATED verdict={VERDICT}")


if __name__ == "__main__":
    main()
