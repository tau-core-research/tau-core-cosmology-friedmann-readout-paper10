#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_operator_units_gate_policy_v1.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
OPERATOR_ROWS = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv"
COV_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
THEORY_READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    policy = read_one(POLICY)
    operator_summary = read_one(OPERATOR_SUMMARY)
    cov_summary = read_one(COV_SUMMARY)
    theory_readiness = read_one(THEORY_READINESS)
    operator_rows = read_rows(OPERATOR_ROWS)

    if policy["status"] != "PHYSICAL_OPERATOR_UNITS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected physical operator units policy status")
    for label, row in [
        ("policy", policy),
        ("operator summary", operator_summary),
        ("theory readiness", theory_readiness),
    ]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit(f"{label} must keep uses_kids_data_vector_values=false")
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit(f"{label} must keep endpoint_scoring_allowed=false")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics", "endpoint_scoring_allowed"]:
        if cov_summary.get(key) != "false":
            raise SystemExit(f"covariance summary must keep {key}=false")
    if operator_summary["operator_skeleton_constructed"] != "true":
        raise SystemExit("operator skeleton must exist before units gate")
    if operator_summary["physical_operator_units_derived"] != "false":
        raise SystemExit("units gate must not inherit derived physical units")
    if len(operator_rows) != 300:
        raise SystemExit("expected 300 operator skeleton rows")

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U1_dimensionless_source_kernel_identified",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": rel(OPERATOR_SUMMARY),
            "requirement": "Identify the current operator skeleton as a dimensionless unit-amplitude kernel rather than a physical COSEBIs prediction.",
            "current_evidence": f"operator_rows={operator_summary['operator_rows']}; mean_operator_kernel_value={operator_summary['mean_operator_kernel_value']}; contains_predictions={operator_summary['contains_predictions']}",
            "units_requirement": "future_physical_operator_must_supply_units_and_amplitude_map_from_dimensionless_kernel_to_cosebis_response",
            "dimension_check": "K_i=M_iS_n_is_dimensionless_because_both_factors_are_dimensionless_source_weights",
            "known_limit_check": "zero_mapping_or_zero_mode_response_gives_zero_unit_kernel",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U2_cosebis_response_units_need_derivation",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(COV_SUMMARY),
            "requirement": "A future operator must derive the response normalization compatible with the retained COSEBIs statistic and covariance domain.",
            "current_evidence": f"shape={cov_summary['covariance_shape']}; positive_definite={cov_summary['positive_definite']}; inverse_saved={cov_summary['inverse_saved']}",
            "units_requirement": "derive_response_units_before_calling_the_unit_kernel_a_physical_prediction",
            "dimension_check": "covariance_domain_checks_numerical_readiness_but_does_not_set_tau_operator_units",
            "known_limit_check": "standard_lensing_null_limit_must_remain_zero_when_tau_source_is_absent",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U3_amplitude_map_not_derived",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(OPERATOR_SUMMARY),
            "requirement": "A source-side amplitude map must be derived before converting the unit-amplitude skeleton into a numerical physical prediction.",
            "current_evidence": f"physical_operator_units_derived={operator_summary['physical_operator_units_derived']}; contains_predictions={operator_summary['contains_predictions']}",
            "units_requirement": "derive_source_side_amplitude_without_endpoint_residual_or_fit_feedback",
            "dimension_check": "amplitude_map_must_carry_any_missing_physical_units",
            "known_limit_check": "amplitude_must_vanish_or_be_controlled_in_zero_tau_path_source_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U4_standard_lensing_null_normalization_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(THEORY_READINESS),
            "requirement": "A future physical operator must show that the Tau path/readout contribution vanishes or routes to null controls in the standard-lensing/no-Tau-source limit.",
            "current_evidence": f"theory_vector_status={theory_readiness['theory_vector_status']}; current_theory_vector_computed={theory_readiness['current_theory_vector_computed']}",
            "units_requirement": "prove_standard_lensing_null_normalization_for_the_physical_operator",
            "dimension_check": "null_limit_is_a_statement_about_response_units_after_amplitude_derivation",
            "known_limit_check": "no_tau_path_source_should_not_create_positive_cosebis_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U5_covariance_metric_not_units_derivation",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(COV_SUMMARY),
            "requirement": "Covariance readiness permits later scoring but does not by itself derive physical operator units or amplitude.",
            "current_evidence": f"condition={cov_summary['condition_number']}; cholesky_ready={cov_summary['cholesky_ready']}; current_inversion_allowed={cov_summary['current_inversion_allowed']}",
            "units_requirement": "keep_covariance_metric_separate_from_source_side_units_derivation",
            "dimension_check": "covariance_metric_and_operator_units_are_distinct_requirements",
            "known_limit_check": "well_conditioned_scoring_metric_does_not_imply_physical_source_derivation",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "U6_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The units gate must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "units_requirement": "future_units_and_amplitude_derivation_must_be_source_side_and_predeclared",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_gate",
            "known_limit_check": "gate_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PHYSICAL_OPERATOR_UNITS_REQUIREMENTS_FROZEN_NOT_DERIVED",
            "selected_statistic": policy["selected_statistic"],
            "gate_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in ledger)),
            "requirement_frozen_count": str(sum(row["status"] == "REQUIREMENT_FROZEN" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "dimensionless_source_kernel_identified": "true",
            "physical_operator_units_derived": "false",
            "source_side_amplitude_map_derived": "false",
            "standard_lensing_null_normalization_proven": "false",
            "covariance_metric_available": "true",
            "covariance_metric_used_as_units_derivation": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_OPERATOR_UNITS_GATE_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
