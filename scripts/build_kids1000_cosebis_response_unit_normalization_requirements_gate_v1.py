#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv"
PHYS_AMP_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv"
UNITS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"
SOURCE_AMP_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
HDU_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_hdu_inventory_v1_summary.csv"
COV_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
COV_INV_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_false(label: str, row: dict[str, str], keys: list[str]) -> None:
    for key in keys:
        if row.get(key) != "false":
            raise SystemExit(f"{label} must keep {key}=false")


def main() -> None:
    policy = read_one(POLICY)
    phys_amp = read_one(PHYS_AMP_SUMMARY)
    units = read_one(UNITS_SUMMARY)
    source_amp = read_one(SOURCE_AMP_SUMMARY)
    operator = read_one(OPERATOR_SUMMARY)
    hdu = read_one(HDU_SUMMARY)
    cov = read_one(COV_SUMMARY)
    cov_inv = read_one(COV_INV_SUMMARY)
    template = read_one(TEMPLATE_SUMMARY)

    if policy["status"] != "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected response-unit normalization policy status")
    if policy["parent_physical_amplitude_requirements_policy"] != phys_amp["policy_id"]:
        raise SystemExit("physical amplitude parent mismatch")
    if policy["parent_physical_operator_units_policy"] != units["policy_id"]:
        raise SystemExit("physical operator units parent mismatch")
    if policy["parent_covariance_readiness_policy"] != cov["policy_id"]:
        raise SystemExit("covariance readiness parent mismatch")

    for label, row in [
        ("policy", policy),
        ("physical amplitude summary", phys_amp),
        ("physical units summary", units),
        ("source amplitude summary", source_amp),
        ("operator summary", operator),
        ("hdu summary", hdu),
        ("covariance summary", cov),
        ("covariance inversion summary", cov_inv),
        ("template summary", template),
    ]:
        require_false(label, row, ["endpoint_scoring_allowed"])
    for label, row in [
        ("policy", policy),
        ("physical amplitude summary", phys_amp),
        ("physical units summary", units),
        ("source amplitude summary", source_amp),
        ("operator summary", operator),
        ("template summary", template),
    ]:
        require_false(label, row, ["uses_kids_data_vector_values"])

    if source_amp["dimensionless_source_side_amplitude_map_constructed"] != "true":
        raise SystemExit("dimensionless source amplitude must exist before response-unit gate")
    if operator["operator_skeleton_constructed"] != "true":
        raise SystemExit("dimensionless operator skeleton must exist before response-unit gate")
    if cov["positive_definite"] != "true" or cov["cholesky_ready"] != "true":
        raise SystemExit("COSEBIs covariance domain must be positive definite and Cholesky ready")
    if hdu["data_vector_rows"] != "300" or template["template_rows"] != "300":
        raise SystemExit("COSEBIs data-vector and theory-template row domains must match")
    if phys_amp["response_unit_normalization_derived"] != "false":
        raise SystemExit("requirements gate must not inherit a derived response-unit normalization")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R1_cosebis_row_domain_available",
            "status": "SATISFIED_AS_DOMAIN_LIMIT",
            "source_artifact": f"{rel(HDU_SUMMARY)};{rel(TEMPLATE_SUMMARY)}",
            "requirement": "A response-unit normalization theorem must act on the retained 300-row COSEBIs data-vector/template domain.",
            "current_evidence": f"data_vector_rows={hdu['data_vector_rows']}; template_rows={template['template_rows']}; selected_statistic={template['selected_statistic']}",
            "response_unit_requirement": "derive_units_for_each_retained_cosebis_row_or_one_consistent_common_response_scale",
            "dimension_check": "COSEBIs_rows_define_the_codomain_but_not_the_tau_response_units",
            "known_limit_check": "row_domain_matching_is_required_before_any_standard_lensing_or_tau_limit_statement",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R2_dimensionless_kernel_and_source_amplitude_available",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": f"{rel(OPERATOR_SUMMARY)};{rel(SOURCE_AMP_SUMMARY)}",
            "requirement": "The current kernel and source amplitude are dimensionless source-side objects.",
            "current_evidence": f"mean_operator_kernel_value={operator['mean_operator_kernel_value']}; dimensionless_amplitude_value={source_amp['dimensionless_amplitude_value']}",
            "response_unit_requirement": "future_response_unit_map_must_supply_the_missing_units_between_dimensionless_source_kernel_and_cosebis_response",
            "dimension_check": "K_i_and_A_src_are_dimensionless_so_A_phys_must_carry_missing_response_units",
            "known_limit_check": "dimensionless_normalization_alone_cannot_create_a_physical_cosebis_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R3_covariance_metric_available_not_units",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": f"{rel(COV_SUMMARY)};{rel(COV_INV_SUMMARY)}",
            "requirement": "The covariance metric may score a future vector, but it cannot define the response-unit normalization.",
            "current_evidence": f"covariance_shape={cov['covariance_shape']}; positive_definite={cov['positive_definite']}; cholesky_ready={cov_inv['cholesky_ready']}; inverse_saved={cov_inv['inverse_saved']}",
            "response_unit_requirement": "keep_covariance_scoring_metric_separate_from_the_theoretical_response_unit_map",
            "dimension_check": "covariance_units_or_metric_readiness_are_not_a_tau_source_units_derivation",
            "known_limit_check": "a_valid_likelihood_metric_does_not_imply_nonzero_tau_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R4_response_unit_map_not_derived",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(PHYS_AMP_SUMMARY),
            "requirement": "A theorem or source-side physical derivation must map the dimensionless kernel into COSEBIs response units.",
            "current_evidence": f"response_unit_normalization_derived={phys_amp['response_unit_normalization_derived']}; physical_amplitude_units_derived={phys_amp['physical_amplitude_units_derived']}",
            "response_unit_requirement": "derive_A_phys_or_response_operator_units_without_endpoint_residual_or_fit_feedback",
            "dimension_check": "the_missing_map_must_turn_dimensionless_A_src_K_i_into_a_quantity_with_cosebis_response_units",
            "known_limit_check": "response_unit_map_must_be_compatible_with_no_tau_source_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R5_standard_lensing_null_compatibility_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(PHYS_AMP_SUMMARY),
            "requirement": "The response-unit normalization must be compatible with the standard-lensing/no-Tau-source null-amplitude theorem.",
            "current_evidence": f"standard_lensing_null_amplitude_proven={phys_amp['standard_lensing_null_amplitude_proven']}",
            "response_unit_requirement": "derive_response_units_that_do_not_generate_positive_tau_contribution_when_tau_source_is_zero",
            "dimension_check": "unit_normalization_and_null_limit_must_be_derived_in_the_same_physical_response_space",
            "known_limit_check": "standard_lensing_baseline_must_be_recovered_when_tau_residual_channel_is_absent",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "R6_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The response-unit requirements gate must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "response_unit_requirement": "future_response_unit_derivation_must_be_pre_endpoint_and_source_or_theorem_side",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_requirements_gate",
            "known_limit_check": "requirements_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_FROZEN_NOT_DERIVED",
            "selected_statistic": policy["selected_statistic"],
            "gate_rows": str(len(rows)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in rows)),
            "satisfied_as_domain_limit_count": str(sum(row["status"] == "SATISFIED_AS_DOMAIN_LIMIT" for row in rows)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in rows)),
            "requirement_frozen_count": str(sum(row["status"] == "REQUIREMENT_FROZEN" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "cosebis_row_domain_available": "true",
            "dimensionless_kernel_and_source_amplitude_available": "true",
            "covariance_metric_available": "true",
            "covariance_metric_used_as_units_derivation": "false",
            "response_unit_normalization_derived": "false",
            "physical_amplitude_units_derived": "false",
            "standard_lensing_null_compatibility_proven": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "cosebis_response_unit_requirements_frozen_but_normalization_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_GATE_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
