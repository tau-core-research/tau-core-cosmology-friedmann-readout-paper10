#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_projection_criterion_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_projection_criterion_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv"


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
    require(policy["status"] == "OPERATOR_LEAKAGE_PROJECTION_CRITERION_POLICY_FROZEN", "unexpected policy")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "OPERATOR_LEAKAGE_PROJECTION_CRITERION_BUILT_NOT_PROVEN", "unexpected status")
    require(summary["criterion_rows"] == "5", "expected five criterion rows")
    require(summary["sufficient_projection_criterion_frozen"] == "true", "criterion should be frozen")
    require(summary["domain_decomposition_declared"] == "false", "domain decomposition is not yet declared")
    require(summary["null_projection_condition_proven"] == "false", "null projection condition must remain open")
    require(summary["control_routing_condition_proven"] == "false", "control routing condition must remain open")
    require(summary["single_operator_consistency_proven"] == "false", "single-operator condition must remain open")
    require(summary["operator_leakage_theorem_proven"] == "false", "operator leakage theorem must remain open")
    require(summary["p2_nonuniform_leakage_closed"] == "false", "P2 must remain open")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation must remain blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must not be claimed")
    require(summary["physical_validation_claimed"] == "false", "physical validation must not be claimed")
    require(summary["verdict"] == "nonuniform_leakage_projection_criterion_frozen_but_not_proven", "unexpected verdict")
    by_id = {row["criterion_id"]: row for row in rows}
    require(by_id["C1_domain_decomposition"]["criterion_status"] == "DEFINITION_REQUIRED", "C1 mismatch")
    require(
        by_id["C2_null_projection_condition"]["criterion_status"] == "SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN",
        "C2 mismatch",
    )
    require(
        by_id["C3_control_routing_alternative"]["criterion_status"]
        == "ALTERNATIVE_SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN",
        "C3 mismatch",
    )
    require(
        by_id["C4_single_operator_consistency"]["criterion_status"] == "CONSISTENCY_CONDITION_FROZEN_NOT_PROVEN",
        "C4 mismatch",
    )
    require(by_id["C5_theorem_status"]["criterion_status"] == "OPEN_NOT_PROVEN", "C5 mismatch")
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_PROJECTION_CRITERION_V1_VALIDATED "
        f"p2_closed={summary['p2_nonuniform_leakage_closed']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
