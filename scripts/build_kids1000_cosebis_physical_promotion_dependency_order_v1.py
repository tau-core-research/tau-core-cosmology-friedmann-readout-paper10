#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_promotion_dependency_order_policy_v1.csv"
PHYSICAL = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"
LEAKAGE = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
GAUGE = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
UNITS = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"
NULL = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"
OPERATOR = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_dependency_order_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    physical = read_one(PHYSICAL)
    leakage = read_one(LEAKAGE)
    gauge = read_one(GAUGE)
    units = read_one(UNITS)
    null = read_one(NULL)
    operator = read_one(OPERATOR)

    require(policy["status"] == "PHYSICAL_PROMOTION_DEPENDENCY_ORDER_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "dependency order must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "dependency order must not claim validation")
    require(physical["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(physical["open_blocker_count"] == "5", "expected five open physical blockers")
    require(leakage["operator_leakage_theorem_proven"] == "false", "leakage theorem should remain open")
    require(gauge["gauge_quotient_descent_proven"] == "false", "gauge quotient theorem should remain open")
    require(units["response_unit_normalization_derived"] == "false", "response-unit normalization should remain open")
    require(null["standard_lensing_null_amplitude_proven"] == "false", "standard null theorem should remain open")
    require(operator["operator_theorem_proven"] == "false", "operator theorem should remain open")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "dependency_rank": "1",
            "blocker_id": "B2_operator_leakage_theorem_open",
            "dependency_status": "NEXT_PRIMARY_PROOF_GATE",
            "depends_on": "requirements_frozen;uniform_tile_null_limit_available;pure_mask_rejection_requirement_frozen",
            "why_before_operator_theorem": "survey_native_operator_cannot_be_physical_if_nonuniform_mask_leakage_can_mimic_low_mode_response",
            "minimum_exit_condition": "prove_mask_only_and_nonuniform_leakage_directions_are_null_or_controlled_for_the_operator_class",
            "current_source_status": (
                f"open_blockers={leakage['open_blocker_count']};"
                f"nonuniform_leakage_risk_recorded={leakage['nonuniform_leakage_risk_recorded']}"
            ),
            "computes_new_scores": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "dependency_rank": "2",
            "blocker_id": "B3_gauge_quotient_descent_open",
            "dependency_status": "NEXT_PARALLEL_PROOF_GATE",
            "depends_on": "equivalence_classes_declared;uniform_mask_offset_limit_available",
            "why_before_operator_theorem": "physical_response_must_not_depend_on_representative_or_gauge_choice",
            "minimum_exit_condition": "prove_normalization_invariance_tile_relabeling_invariance_and_pure_mask_control_compatibility",
            "current_source_status": (
                f"open_blockers={gauge['open_blocker_count']};"
                f"equivalence_classes_declared={gauge['equivalence_classes_declared']}"
            ),
            "computes_new_scores": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "dependency_rank": "3",
            "blocker_id": "B4_response_unit_normalization_open",
            "dependency_status": "AFTER_LEAKAGE_AND_QUOTIENT",
            "depends_on": "B2_operator_leakage_theorem;B3_gauge_quotient_descent;dimensionless_kernel_and_source_amplitude_available",
            "why_before_operator_theorem": "dimensionless_source_kernel_needs_a_response_unit_map_before_physical_cosebis_prediction",
            "minimum_exit_condition": "derive_response_unit_map_without_endpoint_feedback_and_with_standard_lensing_compatibility",
            "current_source_status": (
                f"open_blockers={units['open_blocker_count']};"
                f"covariance_metric_used_as_units_derivation={units['covariance_metric_used_as_units_derivation']}"
            ),
            "computes_new_scores": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "dependency_rank": "4",
            "blocker_id": "B5_standard_lensing_null_amplitude_theorem_open",
            "dependency_status": "AFTER_UNITS_AND_NULL_SAFETY",
            "depends_on": "B2_operator_leakage_theorem;B3_gauge_quotient_descent;B4_response_unit_normalization",
            "why_before_operator_theorem": "tau_absent_limit_must_recover_standard_lensing_or_null_response",
            "minimum_exit_condition": "prove_A_phys_tau_source_zero_equals_zero_or_equivalent_null_control_response",
            "current_source_status": (
                f"open_blockers={null['open_blocker_count']};"
                f"zero_tau_source_amplitude_statement_specified={null['zero_tau_source_amplitude_statement_specified']}"
            ),
            "computes_new_scores": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "dependency_rank": "5",
            "blocker_id": "B1_survey_native_operator_theorem_open",
            "dependency_status": "FINAL_SYNTHESIS_PROOF_GATE",
            "depends_on": "B2_operator_leakage_theorem;B3_gauge_quotient_descent;B4_response_unit_normalization;B5_standard_lensing_null_amplitude_theorem",
            "why_before_operator_theorem": "operator_skeleton_exists_but_full_physical_operator_theorem_requires_leakage_quotient_units_and_null_limit",
            "minimum_exit_condition": "derive_or_reject_a_survey_native_operator_that_generates_the_cosebis_response_with_units_and_null_limits",
            "current_source_status": (
                f"operator_skeleton_constructed={operator['operator_skeleton_constructed']};"
                f"operator_theorem_proven={operator['operator_theorem_proven']}"
            ),
            "computes_new_scores": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PHYSICAL_PROMOTION_DEPENDENCY_ORDER_BUILT_NOT_PROOF",
            "selected_statistic": policy["selected_statistic"],
            "dependency_rows": str(len(rows)),
            "open_physical_blocker_count": physical["open_blocker_count"],
            "next_primary_proof_gate": "B2_operator_leakage_theorem_open",
            "next_parallel_proof_gate": "B3_gauge_quotient_descent_open",
            "unit_normalization_waits_for": "B2_operator_leakage_theorem_open;B3_gauge_quotient_descent_open",
            "standard_null_waits_for": "B2_operator_leakage_theorem_open;B3_gauge_quotient_descent_open;B4_response_unit_normalization_open",
            "operator_theorem_waits_for": "B2_operator_leakage_theorem_open;B3_gauge_quotient_descent_open;B4_response_unit_normalization_open;B5_standard_lensing_null_amplitude_theorem_open",
            "physical_promotion_ready": "false",
            "validation_ready": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "verdict": "physical_promotion_ordered_leakage_and_gauge_are_next_not_validation",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_PROMOTION_DEPENDENCY_ORDER_V1_BUILT "
        f"next_primary={summary[0]['next_primary_proof_gate']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
