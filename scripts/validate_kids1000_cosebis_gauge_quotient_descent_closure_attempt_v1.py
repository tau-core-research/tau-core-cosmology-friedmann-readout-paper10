#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_gauge_quotient_descent_closure_attempt_not_validation"
EXPECTED_ITEMS = [
    "D1_equivalence_relation",
    "D2_uniform_offset_limit",
    "D3_normalization_invariance",
    "D4_tile_relabeling_invariance",
    "D5_pure_mask_control_compatibility",
    "D6_single_operator_dependency",
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
    require(len(rows) == 6, "expected six descent items")
    require([row["descent_item"] for row in rows] == EXPECTED_ITEMS, "unexpected descent item order")
    require(summary["status"] == "GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN", "bad status")
    require(
        summary["verdict"] == "GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "bad verdict",
    )
    require(summary["parent_joint_blocker"] == "B3_gauge_quotient_descent_open", "bad parent blocker")
    require(summary["descent_items"] == "6", "bad item count")
    require(summary["available_limit_checks"] == "1", "expected one available limit check")
    require(summary["open_blocker_count"] == "4", "expected four open descent blockers")
    require(summary["equivalence_classes_declared"] == "true", "equivalence classes should be declared")
    require(summary["uniform_mask_offset_limit_available"] == "true", "uniform offset limit should be available")
    for key in [
        "normalization_invariance_proven",
        "tile_relabeling_invariance_proven",
        "pure_mask_control_compatibility_proven",
        "gauge_quotient_descent_proven",
        "survey_native_operator_constructed",
        "operator_leakage_theorem_proven",
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

    by_item = {row["descent_item"]: row for row in rows}
    require(by_item["D1_equivalence_relation"]["status"] == "DECLARED_NOT_PROVEN", "D1 status mismatch")
    require(by_item["D2_uniform_offset_limit"]["status"] == "AVAILABLE_AS_LIMIT_CHECK", "D2 status mismatch")
    for item in [
        "D3_normalization_invariance",
        "D4_tile_relabeling_invariance",
        "D5_pure_mask_control_compatibility",
        "D6_single_operator_dependency",
    ]:
        require(by_item[item]["status"] == "OPEN_BLOCKER", f"{item} should remain open")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_new_scores",
            "uses_kids_data_vector_values",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['descent_item']} {field} must be false")
        require(row["dimension_check"], f"{row['descent_item']} missing dimension check")
        require(row["known_limit_check"], f"{row['descent_item']} missing known-limit check")
        require(row["remaining_gap"], f"{row['descent_item']} missing remaining gap")

    text = DOC.read_text()
    for marker in [
        "theorem not proven",
        "Minimal target theorem",
        "tile relabeling",
        "admissible normalization",
        "Pure-mask representatives",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
