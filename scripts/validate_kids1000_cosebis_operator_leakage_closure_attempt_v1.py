#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_operator_leakage_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_operator_leakage_closure_attempt_not_validation"
EXPECTED_ITEMS = [
    "C1_uniform_limit",
    "C2_domain_decomposition",
    "C3_mask_quotient_triviality",
    "C4_projection_criterion",
    "C5_gauge_quotient_descent",
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
    require(len(rows) == 5, "expected five closure items")
    require([row["closure_item"] for row in rows] == EXPECTED_ITEMS, "unexpected closure item order")
    require(summary["status"] == "OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN", "bad status")
    require(
        summary["verdict"] == "OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "bad verdict",
    )
    require(summary["parent_joint_blocker"] == "B2_operator_leakage_theorem_open", "bad parent blocker")
    require(summary["closure_items"] == "5", "bad closure item count")
    require(summary["available_limit_checks"] == "1", "expected one available limit check")
    require(summary["open_blocker_count"] == "2", "expected two open blockers")
    require(summary["uniform_limit_available"] == "true", "uniform limit should be available")
    require(summary["domain_decomposition_declared"] == "true", "domain decomposition should be declared")
    require(summary["operator_leakage_theorem_proven"] == "false", "leakage theorem must remain open")
    require(summary["mask_quotient_triviality_proven"] == "false", "mask quotient triviality must remain open")
    require(summary["null_projection_condition_proven"] == "false", "null projection condition must remain open")
    require(summary["control_routing_condition_proven"] == "false", "control routing condition must remain open")
    require(summary["single_operator_consistency_proven"] == "false", "single operator consistency must remain open")
    require(summary["gauge_quotient_descent_proven"] == "false", "gauge quotient descent must remain open")
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

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_new_scores",
            "uses_kids_data_vector_values",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['closure_item']} {field} must be false")
        require(row["dimension_check"], f"{row['closure_item']} missing dimension check")
        require(row["known_limit_check"], f"{row['closure_item']} missing known-limit check")
        require(row["remaining_gap"], f"{row['closure_item']} missing remaining gap")
    by_item = {row["closure_item"]: row for row in rows}
    require(by_item["C1_uniform_limit"]["status"] == "AVAILABLE_AS_LIMIT_CHECK", "C1 status mismatch")
    require(by_item["C2_domain_decomposition"]["status"] == "DECLARED_NOT_PROVEN", "C2 status mismatch")
    require(by_item["C3_mask_quotient_triviality"]["status"] == "OPEN_BLOCKER", "C3 status mismatch")
    require(by_item["C4_projection_criterion"]["status"] == "FROZEN_NOT_PROVEN", "C4 status mismatch")
    require(by_item["C5_gauge_quotient_descent"]["status"] == "OPEN_BLOCKER", "C5 status mismatch")

    text = DOC.read_text()
    for marker in [
        "theorem not proven",
        "Minimal target theorem",
        "mask quotient triviality",
        "same statistic",
        "gauge/quotient descent",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
