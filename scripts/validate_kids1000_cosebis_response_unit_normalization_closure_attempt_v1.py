#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_response_unit_normalization_closure_attempt_not_validation"
EXPECTED_ITEMS = [
    "U1_codomain_domain_match",
    "U2_dimensionless_kernel_identified",
    "U3_covariance_metric_separation",
    "U4_response_unit_map",
    "U5_null_limit_compatibility",
    "U6_dependency_on_B2_B3",
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
    require(len(rows) == 6, "expected six unit items")
    require([row["unit_item"] for row in rows] == EXPECTED_ITEMS, "unexpected unit item order")
    require(summary["status"] == "RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_DERIVED", "bad status")
    require(
        summary["verdict"] == "RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_UNITS_REMAIN_OPEN",
        "bad verdict",
    )
    require(summary["parent_joint_blocker"] == "B4_response_unit_normalization_open", "bad parent blocker")
    require(summary["unit_items"] == "6", "bad item count")
    require(summary["available_domain_or_source_checks"] == "2", "expected two available checks")
    require(summary["open_blocker_count"] == "3", "expected three open blockers")
    require(summary["cosebis_row_domain_available"] == "true", "row domain should be available")
    require(summary["dimensionless_kernel_and_source_amplitude_available"] == "true", "dimensionless kernel should be available")
    require(summary["covariance_metric_available"] == "true", "covariance metric should be available")
    for key in [
        "covariance_metric_used_as_units_derivation",
        "response_unit_normalization_derived",
        "physical_operator_units_derived",
        "standard_lensing_null_compatibility_proven",
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

    by_item = {row["unit_item"]: row for row in rows}
    require(by_item["U1_codomain_domain_match"]["status"] == "AVAILABLE_AS_DOMAIN_LIMIT", "U1 status mismatch")
    require(by_item["U2_dimensionless_kernel_identified"]["status"] == "AVAILABLE_AS_SOURCE_LIMIT", "U2 status mismatch")
    require(by_item["U3_covariance_metric_separation"]["status"] == "REQUIREMENT_FROZEN", "U3 status mismatch")
    for item in ["U4_response_unit_map", "U5_null_limit_compatibility", "U6_dependency_on_B2_B3"]:
        require(by_item[item]["status"] == "OPEN_BLOCKER", f"{item} should remain open")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_new_scores",
            "uses_kids_data_vector_values",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['unit_item']} {field} must be false")
        require(row["dimension_check"], f"{row['unit_item']} missing dimension check")
        require(row["known_limit_check"], f"{row['unit_item']} missing known-limit check")
        require(row["remaining_gap"], f"{row['unit_item']} missing remaining gap")

    text = DOC.read_text()
    for marker in [
        "unit map not derived",
        "Minimal target theorem",
        "dimensionless",
        "covariance metric",
        "standard-lensing/no-Tau-source null limit",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
