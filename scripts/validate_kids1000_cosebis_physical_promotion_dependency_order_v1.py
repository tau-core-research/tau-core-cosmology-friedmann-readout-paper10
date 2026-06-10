#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_promotion_dependency_order_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_dependency_order_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(policy["status"] == "PHYSICAL_PROMOTION_DEPENDENCY_ORDER_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "PHYSICAL_PROMOTION_DEPENDENCY_ORDER_BUILT_NOT_PROOF", "unexpected status")
    require(summary["dependency_rows"] == "5", "expected five blocker rows")
    require(summary["open_physical_blocker_count"] == "5", "expected five open physical blockers")
    require(summary["next_primary_proof_gate"] == "B2_operator_leakage_theorem_open", "unexpected primary gate")
    require(summary["next_parallel_proof_gate"] == "B3_gauge_quotient_descent_open", "unexpected parallel gate")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation must remain blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(
        summary["verdict"] == "physical_promotion_ordered_leakage_and_gauge_are_next_not_validation",
        "unexpected verdict",
    )
    by_id = {row["blocker_id"]: row for row in rows}
    require(by_id["B2_operator_leakage_theorem_open"]["dependency_status"] == "NEXT_PRIMARY_PROOF_GATE", "B2 mismatch")
    require(by_id["B3_gauge_quotient_descent_open"]["dependency_status"] == "NEXT_PARALLEL_PROOF_GATE", "B3 mismatch")
    require(by_id["B4_response_unit_normalization_open"]["dependency_status"] == "AFTER_LEAKAGE_AND_QUOTIENT", "B4 mismatch")
    require(by_id["B5_standard_lensing_null_amplitude_theorem_open"]["dependency_status"] == "AFTER_UNITS_AND_NULL_SAFETY", "B5 mismatch")
    require(by_id["B1_survey_native_operator_theorem_open"]["dependency_status"] == "FINAL_SYNTHESIS_PROOF_GATE", "B1 mismatch")
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_PROMOTION_DEPENDENCY_ORDER_V1_VALIDATED "
        f"next_primary={summary['next_primary_proof_gate']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
