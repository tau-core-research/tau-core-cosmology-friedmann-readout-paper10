#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv"
ELIGIBILITY_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv"
ELIGIBILITY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv"
MOCK_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv"
MOCK_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv"
PATH_PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
MAPPING_VECTOR = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
D_PATH = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"
PATH_WEIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1_summary.csv"
THEORY_READY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv"


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


def bool_text(value: bool) -> str:
    return str(value).lower()


def main() -> None:
    policy = read_one(POLICY)
    eligibility_policy = read_one(ELIGIBILITY_POLICY)
    eligibility = read_one(ELIGIBILITY_SUMMARY)
    mock_policy = read_one(MOCK_POLICY)
    mock = read_one(MOCK_SUMMARY)
    path_preflight = read_one(PATH_PREFLIGHT)
    mapping = read_one(MAPPING_VECTOR)
    d_path = read_one(D_PATH)
    path_weight = read_one(PATH_WEIGHT)
    theory_ready = read_one(THEORY_READY)

    if policy["status"] != "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_FROZEN":
        raise SystemExit("unexpected survey-native path-kernel policy status")
    if policy["parent_log_band_prior_eligibility_policy"] != eligibility_policy["policy_id"]:
        raise SystemExit("parent log-band prior eligibility policy mismatch")
    if policy["parent_mock_sanity_policy"] != mock_policy["policy_id"]:
        raise SystemExit("parent mock sanity policy mismatch")
    for row in [policy, eligibility, mock, path_preflight, mapping, d_path, path_weight, theory_ready]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit("survey-native gate inputs must remain KiDS-data-vector-free")
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit("survey-native gate inputs must remain non-scoring")

    mapping_available = mapping["mapping_vector_computed"] == "true" and mapping["contains_theory_vector"] == "false"
    d_path_caveated = d_path["d_path_full_route_mask_load_non_degenerate"] == "true"
    path_rule_ready = path_weight["path_weight_rule_computable"] == "true"
    theory_source_frozen = theory_ready["current_theory_vector_computed"] == "true"
    mock_guardrail = mock["all_expected_templates_recovered"] == "true"

    rows = [
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K1_source_frozen_mapping_vector",
            "status": "PASS" if mapping_available else "FAIL",
            "source_artifact": rel(MAPPING_VECTOR),
            "criterion": "A 300-row source-frozen mapping basis must exist before a survey-native path kernel can be promoted.",
            "current_evidence": (
                f"mapping_vector_computed={mapping['mapping_vector_computed']}; "
                f"unique_mapping_value_count={mapping['unique_mapping_value_count_rounded_1e_minus_12']}; "
                f"mode_shape_generated={mapping['mode_shape_generated']}"
            ),
            "derivation_role": "source_side_basis_available_but_no_mode_response",
            "dimension_check": "dimensionless_mapping_weight",
            "known_limit_check": "zero_endpoint_amplitude_removes_carrier_contribution",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K2_full_route_path_observable",
            "status": "PASS_CAVEATED" if d_path_caveated else "FAIL",
            "source_artifact": rel(D_PATH),
            "criterion": "The survey route must provide a non-degenerate path observable or a clearly caveated source-side proxy.",
            "current_evidence": (
                f"tile_count={d_path['tile_count']}; "
                f"unique_d_path_values={d_path['unique_d_path_value_count_rounded_1e_minus_12']}; "
                f"source_scope={d_path['source_scope']}"
            ),
            "derivation_role": "survey_native_mask_load_proxy_available_not_calibrated_depth_kernel",
            "dimension_check": "normalized_dimensionless_path_proxy",
            "known_limit_check": "uniform_path_proxy_collapses_to_no_positive_path_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K3_path_weight_factorization",
            "status": "PASS" if path_rule_ready else "FAIL",
            "source_artifact": rel(PATH_WEIGHT),
            "criterion": "The path/readout weight must have a source-side factor rule before endpoint scoring.",
            "current_evidence": (
                f"factor_count={path_weight['factor_count']}; "
                f"available_factor_count={path_weight['available_factor_count']}; "
                f"path_weight_rule_computable={path_weight['path_weight_rule_computable']}"
            ),
            "derivation_role": "factorized_path_weight_rule_available_but_not_pixel_calibrated",
            "dimension_check": "all_factors_protocol_normalized_before_endpoint_amplitude",
            "known_limit_check": "missing_positive_path_factor_returns_to_source_frozen_null_control",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K4_source_frozen_theory_vector_shell",
            "status": "PASS" if theory_source_frozen else "FAIL",
            "source_artifact": rel(THEORY_READY),
            "criterion": "A source-frozen theory-vector shell must exist without predictions, residuals, or fit statistics.",
            "current_evidence": (
                f"current_theory_vector_computed={theory_ready['current_theory_vector_computed']}; "
                f"contains_predictions={theory_ready['contains_predictions']}; "
                f"contains_fit_statistics={theory_ready['contains_fit_statistics']}"
            ),
            "derivation_role": "source_frozen_shell_available_not_physical_lensing_kernel",
            "dimension_check": "dimensionless_carrier_until_endpoint_amplitude",
            "known_limit_check": "zero_channel_amplitude_returns_zero_tau_correction",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K5_template_recovery_guardrail",
            "status": "PASS" if mock_guardrail else "FAIL",
            "source_artifact": rel(MOCK_SUMMARY),
            "criterion": "The template protocol should not automatically classify all deterministic patterns as low-mode.",
            "current_evidence": (
                f"all_expected_templates_recovered={mock['all_expected_templates_recovered']}; "
                f"verdict={mock['mock_sanity_verdict']}"
            ),
            "derivation_role": "protocol_guardrail_not_physical_mock_validation",
            "dimension_check": "cosine_similarity_on_dimensionless_templates",
            "known_limit_check": "flat_high_and_oscillatory_truths_do_not_recover_low_template",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K6_survey_native_mode_response_operator",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_survey_native_cosebis_path_response_operator",
            "criterion": "A survey-native operator must map path observables into COSEBIs mode response before the envelope becomes a kernel theorem.",
            "current_evidence": "Current artifacts provide mapping weights and a shell, but no survey-native response operator from mask/depth/path fields to COSEBIs mode amplitudes.",
            "derivation_role": "missing_operator_between_path_source_fields_and_mode_shape",
            "dimension_check": "operator_units_and_normalization_not_yet_derived",
            "known_limit_check": "must reduce_to_zero_response_for_no_path_residual",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K7_log_band_prior_from_kernel",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_mode_response_spectrum_derivation",
            "criterion": "The log-band-neutral power prior must be derived from the survey-native response spectrum, not only assumed.",
            "current_evidence": (
                f"eligibility_verdict={eligibility['eligibility_verdict']}; "
                f"assumption_not_source_proven_count={eligibility['assumption_not_source_proven_count']}"
            ),
            "derivation_role": "smoothness_prior_still_conditional",
            "dimension_check": "dP_dlnn_dimensionless_after_source_normalization",
            "known_limit_check": "non_smooth_or_high_frequency_source_should_not_force_n_minus_half",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "condition_id": "K8_covariant_lensing_path_limit",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_covariant_tau_lensing_path_kernel",
            "criterion": "A covariant or survey-native limit must connect the source-side path kernel to a lensing/readout observable.",
            "current_evidence": "No perturbation-level covariant Tau Core lensing/path kernel is present in this package.",
            "derivation_role": "missing_covariant_or_survey_native_limit",
            "dimension_check": "observable_units_and_gauge_descent_not_yet_audited",
            "known_limit_check": "must recover_standard_lensing_null_when_tau_residual_channels_are_zero",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    pass_like = {"PASS", "PASS_CAVEATED"}
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_PARTIAL",
            "selected_statistic": policy["selected_statistic"],
            "conditions": str(len(rows)),
            "pass_count": str(sum(row["status"] == "PASS" for row in rows)),
            "pass_caveated_count": str(sum(row["status"] == "PASS_CAVEATED" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "fail_count": str(sum(row["status"] == "FAIL" for row in rows)),
            "route_support_conditions_passed": bool_text(all(row["status"] in pass_like for row in rows[:5])),
            "full_kernel_derivation_closed": "false",
            "survey_native_gate_verdict": "survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_V1_COMPLETE "
        f"verdict={summary[0]['survey_native_gate_verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
