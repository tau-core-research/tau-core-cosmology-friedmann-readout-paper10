#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_not_validation"
EXPECTED_ITEMS = [
    "N1_null_controls_available",
    "N2_zero_tau_source_statement",
    "N3_operator_null_safety",
    "N4_response_unit_dependency",
    "N5_leakage_and_gauge_dependency",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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
    require(len(rows) == 5, "expected five null-amplitude items")
    require([row["null_item"] for row in rows] == EXPECTED_ITEMS, "unexpected null item order")
    require(summary["status"] == "STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN", "bad status")
    require(
        summary["verdict"] == "STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "bad verdict",
    )
    require(summary["parent_joint_blocker"] == "B5_standard_lensing_null_amplitude_theorem_open", "bad parent blocker")
    require(summary["null_items"] == "5", "bad item count")
    require(summary["available_control_limits"] == "1", "expected one control-limit item")
    require(summary["specified_not_derived_items"] == "1", "expected one specified-not-derived item")
    require(summary["open_blocker_count"] == "3", "expected three open blockers")
    require(summary["null_controls_available_as_control_limit"] == "true", "null controls should be available as controls")
    require(summary["zero_tau_source_amplitude_statement_specified"] == "true", "zero-source statement should be specified")
    for key in [
        "standard_lensing_null_amplitude_proven",
        "operator_null_safety_proven",
        "response_unit_normalization_derived",
        "operator_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
    ]:
        require(summary[key] == "false", f"{key} must remain false")
    for field in [
        "computes_new_scores",
        "uses_kids_data_vector_values",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
        "cosmological_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must be false")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    by_item = {row["null_item"]: row for row in rows}
    require(by_item["N1_null_controls_available"]["status"] == "AVAILABLE_AS_CONTROL_LIMIT", "N1 status mismatch")
    require(by_item["N2_zero_tau_source_statement"]["status"] == "SPECIFIED_NOT_DERIVED", "N2 status mismatch")
    for item in ["N3_operator_null_safety", "N4_response_unit_dependency", "N5_leakage_and_gauge_dependency"]:
        require(by_item[item]["status"] == "OPEN_BLOCKER", f"{item} should remain open")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_new_scores",
            "uses_kids_data_vector_values",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['null_item']} {field} must be false")
        require(row["dimension_check"], f"{row['null_item']} missing dimension check")
        require(row["known_limit_check"], f"{row['null_item']} missing known-limit check")
        require(row["remaining_gap"], f"{row['null_item']} missing remaining gap")

    text = DOC.read_text()
    for marker in [
        "null-amplitude theorem not proven",
        "Minimal target theorem",
        "standard-lensing",
        "no-Tau-source",
        "null-control class",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
