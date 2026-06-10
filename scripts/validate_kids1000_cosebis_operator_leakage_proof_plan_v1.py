#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_proof_plan_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_proof_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv"


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
    require(policy["status"] == "OPERATOR_LEAKAGE_PROOF_PLAN_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "OPERATOR_LEAKAGE_PROOF_PLAN_BUILT_NOT_PROOF", "unexpected status")
    require(summary["proof_plan_rows"] == "5", "expected five proof-plan rows")
    require(summary["anchor_available_count"] == "1", "expected one anchor")
    require(summary["guard_satisfied_count"] == "1", "expected one guard")
    require(summary["open_proof_step_count"] == "3", "expected three open proof steps")
    require(summary["operator_leakage_theorem_proven"] == "false", "leakage theorem must remain open")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation must remain blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["verdict"] == "B2_operator_leakage_exit_conditions_frozen_but_theorem_open", "unexpected verdict")
    by_step = {row["step_id"]: row for row in rows}
    require(by_step["P1_uniform_null_limit_anchor"]["step_status"] == "ANCHOR_AVAILABLE", "P1 mismatch")
    require(by_step["P2_nonuniform_leakage_projection"]["step_status"] == "PRIMARY_OPEN_PROOF_STEP", "P2 mismatch")
    require(by_step["P3_pure_mask_quotient_or_control"]["step_status"] == "PRIMARY_OPEN_PROOF_STEP", "P3 mismatch")
    require(by_step["P4_single_operator_coupling"]["step_status"] == "COUPLING_OPEN_PROOF_STEP", "P4 mismatch")
    require(by_step["P5_no_endpoint_feedback_guard"]["step_status"] == "GUARD_SATISFIED", "P5 mismatch")
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_PROOF_PLAN_V1_VALIDATED "
        f"open_steps={summary['open_proof_step_count']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
