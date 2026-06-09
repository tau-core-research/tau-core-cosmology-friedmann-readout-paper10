#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_operator_spec_policy_v1.csv"
PARENT_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv"
PARENT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv"
MAPPING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
D_PATH_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"
THEORY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
MODE_DERIVATION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_kernel_envelope_derivation_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"


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


def main() -> None:
    policy = read_one(POLICY)
    parent_policy = read_one(PARENT_POLICY)
    parent_summary = read_one(PARENT_SUMMARY)
    mapping = read_one(MAPPING_SUMMARY)
    d_path = read_one(D_PATH_SUMMARY)
    theory = read_one(THEORY_SUMMARY)
    mode_derivation = read_one(MODE_DERIVATION_SUMMARY)

    if policy["status"] != "MODE_RESPONSE_OPERATOR_SPEC_POLICY_FROZEN":
        raise SystemExit("unexpected mode-response operator spec policy status")
    if policy["parent_survey_native_path_kernel_gate_policy"] != parent_policy["policy_id"]:
        raise SystemExit("parent survey-native path-kernel gate policy mismatch")
    if parent_summary["full_kernel_derivation_closed"] != "false":
        raise SystemExit("parent gate must keep full kernel derivation open")
    for row in [policy, parent_summary, mapping, d_path, theory, mode_derivation]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit("operator spec inputs must remain KiDS-data-vector-free")
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit("operator spec inputs must remain non-scoring")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R1_domain_path_observable",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": rel(D_PATH_SUMMARY),
            "requirement": "The operator domain must contain a source-side path observable or explicitly caveated path proxy.",
            "current_evidence": (
                f"source_scope={d_path['source_scope']}; "
                f"unique_d_path_values={d_path['unique_d_path_value_count_rounded_1e_minus_12']}"
            ),
            "operator_implication": "domain_can_use_caveated_full_route_mask_load_proxy",
            "dimension_check": "input_proxy_dimensionless_after_source_normalization",
            "limit_check": "uniform_path_proxy_must_not_create_positive_path_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R2_codomain_cosebis_rows",
            "status": "SATISFIED",
            "source_artifact": rel(MAPPING_SUMMARY),
            "requirement": "The operator codomain must be the retained 300-row COSEBIs tomographic-pair/mode domain.",
            "current_evidence": f"target_rows={mapping['target_rows']}; pair_level_mode_degenerate_value_count={mapping['pair_level_mode_degenerate_value_count']}",
            "operator_implication": "operator_outputs_one_value_per_retained_cosebis_row",
            "dimension_check": "row_output_dimensionless_until_endpoint_amplitude",
            "limit_check": "zero_channel_amplitude_returns_zero_output",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R3_linearity_before_endpoint_amplitude",
            "status": "SPECIFIED_NOT_DERIVED",
            "source_artifact": "operator_specification",
            "requirement": "Before endpoint amplitude, the response operator should be linear in the source-side path/readout residual channel.",
            "current_evidence": "Current theory shell is unit-amplitude and source-frozen, but no survey-native response operator has been derived.",
            "operator_implication": "future_operator_should_support_superposition_and_null_controls",
            "dimension_check": "linear_map_between_dimensionless_source_proxy_and_dimensionless_row_carrier",
            "limit_check": "zero_input_path_residual_maps_to_zero_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R4_mode_response_from_source_operator",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_survey_native_cosebis_path_response_operator",
            "requirement": "The COSEBIs mode dependence must come from the survey-native response operator, not only from an assumed mode envelope.",
            "current_evidence": f"current_derivation_verdict={mode_derivation['derivation_verdict']}",
            "operator_implication": "must_derive_or_reject_n_minus_half_from_operator_spectrum",
            "dimension_check": "mode_response_spectrum_normalization_not_yet_derived",
            "limit_check": "high_frequency_or_oscillatory_source_should_not_force_low_mode_envelope",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R5_pair_redshift_path_separation",
            "status": "PARTIAL",
            "source_artifact": rel(MAPPING_SUMMARY),
            "requirement": "The operator should separate tomographic-pair/redshift support from path support before applying any mode response.",
            "current_evidence": (
                f"unique_mapping_value_count={mapping['unique_mapping_value_count_rounded_1e_minus_12']}; "
                f"mode_shape_generated={mapping['mode_shape_generated']}"
            ),
            "operator_implication": "pair_path_basis_exists_but_mode_response_is_not_source_native",
            "dimension_check": "pair_and_path_factors_unit_normalized",
            "limit_check": "removing_mode_response_leaves_pair_path_degenerate_shell",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R6_no_data_vector_or_fit_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(THEORY_SUMMARY),
            "requirement": "The operator specification must not read KiDS En values, residuals, fit statistics, or posterior chains.",
            "current_evidence": (
                f"uses_kids_data_vector_values={theory['uses_kids_data_vector_values']}; "
                f"contains_fit_statistics={theory['contains_fit_statistics']}; "
                f"uses_posterior_chains={theory['uses_posterior_chains']}"
            ),
            "operator_implication": "source_side_freeze_is_preserved",
            "dimension_check": "no_empirical_amplitude_or_residual_unit_enters_operator_spec",
            "limit_check": "operator_spec_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R7_gauge_or_mask_null_safety",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_null_sky_rotation_and_mask_response_operator",
            "requirement": "The operator must distinguish physical path/readout response from mask/gauge artifacts under null rotations or equivalent controls.",
            "current_evidence": "Null-control replays exist, but no operator-level gauge/null response theorem is present.",
            "operator_implication": "future_operator_must_descend_to_quotient_safe_path_response",
            "dimension_check": "null_transform_should_preserve_normalization",
            "limit_check": "pure_mask_or_gauge_change_should_not_generate_positive_tau_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "R8_standard_lensing_null_limit",
            "status": "SPECIFIED_NOT_DERIVED",
            "source_artifact": "operator_specification",
            "requirement": "When Tau residual channels are set to zero, the operator contribution must vanish and leave the standard lensing baseline unchanged.",
            "current_evidence": "Current source-frozen shell is unit-amplitude only and records no physical prediction.",
            "operator_implication": "operator_is_residual_channel_not_baseline_replacement",
            "dimension_check": "endpoint_amplitude_carries_observable_units_later",
            "limit_check": "tau_channel_amplitude_zero_implies_no_additive_lensing_response",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "MODE_RESPONSE_OPERATOR_SPEC_COMPLETE_NOT_DERIVED",
            "selected_statistic": policy["selected_statistic"],
            "requirements": str(len(rows)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in rows)),
            "satisfied_caveated_count": str(sum(row["status"] == "SATISFIED_CAVEATED" for row in rows)),
            "partial_count": str(sum(row["status"] == "PARTIAL" for row in rows)),
            "specified_not_derived_count": str(sum(row["status"] == "SPECIFIED_NOT_DERIVED" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "mode_response_operator_derived": "false",
            "operator_spec_verdict": "operator_requirements_frozen_but_survey_native_mode_response_not_derived",
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
        "PAPER10_KIDS1000_COSEBIS_MODE_RESPONSE_OPERATOR_SPEC_V1_COMPLETE "
        f"verdict={summary[0]['operator_spec_verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
