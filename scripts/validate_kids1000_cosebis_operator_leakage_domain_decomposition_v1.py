#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_domain_decomposition_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_domain_decomposition_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv"


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

    require(policy["status"] == "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_POLICY_FROZEN", "unexpected policy")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(policy["physical_validation_claimed"] == "false", "policy must not claim physics")
    require(
        summary["status"] == "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_DECLARED_NOT_PROJECTION_PROOF",
        "unexpected status",
    )
    require(summary["component_rows"] == "5", "expected five component rows")
    require(summary["domain_decomposition_declared"] == "true", "domain decomposition should be declared")
    require(summary["candidate_physical_component_declared"] == "true", "candidate component missing")
    require(summary["mask_component_declared"] == "true", "mask component missing")
    require(summary["control_or_null_component_declared"] == "true", "control/null component missing")
    require(summary["no_endpoint_feedback_guard_satisfied"] == "true", "endpoint guard should be satisfied")
    require(summary["components_pairwise_orthogonality_proven"] == "false", "orthogonality must not be claimed")
    require(summary["mask_component_quotient_triviality_proven"] == "false", "mask quotient proof must remain open")
    require(summary["operator_projection_condition_proven"] == "false", "projection condition must remain open")
    require(summary["control_routing_condition_proven"] == "false", "control routing condition must remain open")
    require(summary["single_operator_consistency_proven"] == "false", "single-operator condition must remain open")
    require(summary["operator_leakage_theorem_proven"] == "false", "leakage theorem must remain open")
    require(summary["p2_nonuniform_leakage_closed"] == "false", "P2 must remain open")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation must remain blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must not be claimed")
    require(summary["physical_validation_claimed"] == "false", "physical validation must not be claimed")
    require(
        summary["verdict"] == "domain_decomposition_declared_but_projection_and_leakage_theorem_remain_open",
        "unexpected verdict",
    )
    by_id = {row["component_id"]: row for row in rows}
    require(by_id["V_phys_candidate"]["component_status"] == "DECLARED_CANDIDATE_NOT_PHYSICAL_PROOF", "candidate mismatch")
    require(by_id["V_mask"]["component_status"] == "DECLARED_MASK_ONLY_BASIS_NOT_NULL_PROVEN", "mask mismatch")
    require(by_id["V_control_or_null"]["component_status"] == "DECLARED_CONTROL_OR_NULL_NOT_SIGNAL", "control mismatch")
    require(by_id["no_endpoint_feedback_guard"]["component_status"] == "SATISFIED_AS_LEDGER_GUARD", "guard mismatch")
    require(
        by_id["decomposition_status"]["component_status"] == "DECLARED_BOOKKEEPING_NOT_PROJECTION_PROOF",
        "status mismatch",
    )
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_V1_VALIDATED "
        f"declared={summary['domain_decomposition_declared']} "
        f"p2_closed={summary['p2_nonuniform_leakage_closed']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
