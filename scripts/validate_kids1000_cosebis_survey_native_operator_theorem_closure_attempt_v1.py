#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_survey_native_operator_theorem_closure_attempt_not_validation"
EXPECTED_ITEMS = [
    "S1_factorized_skeleton_available",
    "S2_leakage_closure_required",
    "S3_gauge_quotient_descent_required",
    "S4_response_units_required",
    "S5_standard_null_required",
    "S6_single_operator_synthesis_required",
    "S7_no_endpoint_feedback",
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

    require(len(rows) == 7, "expected seven synthesis items")
    require([row["synthesis_item"] for row in rows] == EXPECTED_ITEMS, "unexpected synthesis item order")
    require(
        summary["status"] == "SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_SYNTHESIZES_BLOCKERS_NOT_PROVEN",
        "bad status",
    )
    require(
        summary["verdict"] == "SURVEY_NATIVE_OPERATOR_THEOREM_SYNTHESIS_HAS_SOURCE_SKELETON_BUT_PROOF_CHAIN_REMAINS_OPEN",
        "bad verdict",
    )
    require(summary["parent_joint_blocker"] == "B1_survey_native_operator_theorem_open", "bad parent blocker")
    require(summary["synthesis_items"] == "7", "bad synthesis item count")
    require(summary["available_source_skeletons"] == "1", "bad source skeleton count")
    require(summary["open_blocker_count"] == "5", "expected five open blockers")
    require(summary["operator_skeleton_constructed"] == "true", "operator skeleton must exist")
    for key in [
        "survey_native_operator_constructed",
        "operator_theorem_proven",
        "operator_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "response_unit_normalization_derived",
        "standard_lensing_null_amplitude_proven",
        "physical_promotion_ready",
        "can_promote_kids_block_to_clean_joint_support",
        "computes_new_scores",
        "uses_kids_data_vector_values",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
        "cosmological_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary {key} must remain false")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    by_item = {row["synthesis_item"]: row for row in rows}
    require(
        by_item["S1_factorized_skeleton_available"]["status"] == "AVAILABLE_AS_SOURCE_SKELETON",
        "S1 status mismatch",
    )
    for item in [
        "S2_leakage_closure_required",
        "S3_gauge_quotient_descent_required",
        "S4_response_units_required",
        "S5_standard_null_required",
        "S6_single_operator_synthesis_required",
    ]:
        require(by_item[item]["status"] == "OPEN_BLOCKER", f"{item} should remain open")
    require(by_item["S7_no_endpoint_feedback"]["status"] == "SATISFIED", "S7 no-feedback status mismatch")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_new_scores",
            "uses_kids_data_vector_values",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['synthesis_item']} {field} must be false")
        require(row["dimension_check"], f"{row['synthesis_item']} missing dimension check")
        require(row["known_limit_check"], f"{row['synthesis_item']} missing known-limit check")
        require(row["remaining_gap"], f"{row['synthesis_item']} missing remaining gap")

    text = DOC.read_text()
    for marker in [
        "survey-native physical operator theorem not proven",
        "Minimal target theorem",
        "There exists one survey-native operator O_tau",
        "B2--B5 remain open",
        "cannot yet be",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
