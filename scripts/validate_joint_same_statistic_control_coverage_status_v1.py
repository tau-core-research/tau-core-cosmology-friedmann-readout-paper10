#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_same_statistic_control_coverage_status_v1_summary.csv"
DOC = ROOT / "docs/joint_same_statistic_control_coverage_status_v1.md"
CLAIM_BOUNDARY = "joint_same_statistic_control_coverage_status_not_scoring_not_validation"
VERDICT = "SAME_STATISTIC_CONTROL_COVERAGE_SYMBOLIC_PROGRESS_NUMERIC_BLOCKED"
EXPECTED_FAMILIES = [
    "sign_flip_controls",
    "leave_one_probe_or_block_drop",
    "shuffled_channel_labels",
    "wrong_channel_or_wrong_family_controls",
    "scope_and_forbidden_input_controls",
    "null_readout_controls",
]


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
    require(len(rows) == 6, "expected six tracked control families")
    require([row["control_family"] for row in rows] == EXPECTED_FAMILIES, "unexpected control family order")
    require(summary["tracked_control_families"] == "6", "summary family count mismatch")
    require(summary["symbolic_complete_families"] == "2", "expected two symbolic-complete families")
    require(summary["symbolic_partial_families"] == "1", "expected one symbolic-partial family")
    require(summary["design_ready_numeric_blocked_families"] == "3", "expected three design-ready blocked families")
    require(summary["symbolic_binding_passed"] == "true", "symbolic binding must pass")
    require(summary["numeric_executable_binding_passed"] == "false", "numeric binding must remain blocked")
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
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["same_symbolic_statistic_required"] == "true", "symbolic statistic requirement missing")
        require(row["numeric_executable_statistic_required"] == "true", "numeric binding requirement missing")
        require(row["cross_probe_covariance_required"] == "true", "covariance requirement missing")
        require(row["remaining_blocker"], f"{row['control_family']} missing blocker")
        for field in [
            "computes_numeric_statistic_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['control_family']} {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "symbolic progress only",
        "not scoring",
        "not validation",
        VERDICT,
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_SAME_STATISTIC_CONTROL_COVERAGE_STATUS_V1_VALIDATED verdict={VERDICT}")


if __name__ == "__main__":
    main()
