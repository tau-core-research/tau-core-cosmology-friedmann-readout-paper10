#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_null_safety_gate_policy_v1.csv"
OPERATOR_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_operator_spec_policy_v1.csv"
SPECTRUM_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"
SPECTRUM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"
NULL_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_policy_v1.csv"
NULL_REPLAY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1_summary.csv"
NULL_READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"
E_WEB_NULL = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1_summary.csv"
MAPPING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
D_PATH_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"


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


def require_false(row: dict[str, str], key: str, label: str) -> None:
    if row.get(key) != "false":
        raise SystemExit(f"{label} must have {key}=false")


def main() -> None:
    policy = read_one(POLICY)
    operator_policy = read_one(OPERATOR_POLICY)
    spectrum_policy = read_one(SPECTRUM_POLICY)
    operator_summary = read_one(OPERATOR_SUMMARY)
    spectrum_summary = read_one(SPECTRUM_SUMMARY)
    null_policy = read_one(NULL_POLICY)
    null_replay = read_one(NULL_REPLAY)
    null_readiness = read_one(NULL_READINESS)
    e_web_null = read_one(E_WEB_NULL)
    mapping = read_one(MAPPING_SUMMARY)
    d_path = read_one(D_PATH_SUMMARY)

    if policy["status"] != "OPERATOR_NULL_SAFETY_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected operator null-safety gate policy status")
    if policy["parent_mode_response_operator_spec_policy"] != operator_policy["policy_id"]:
        raise SystemExit("operator spec parent policy mismatch")
    if policy["parent_mode_response_spectrum_attempt_policy"] != spectrum_policy["policy_id"]:
        raise SystemExit("spectrum attempt parent policy mismatch")

    for label, row in [
        ("gate policy", policy),
        ("operator policy", operator_policy),
        ("spectrum policy", spectrum_policy),
        ("operator summary", operator_summary),
        ("spectrum summary", spectrum_summary),
        ("null replay", null_replay),
        ("null readiness", null_readiness),
        ("e-web null", e_web_null),
        ("mapping summary", mapping),
        ("d-path summary", d_path),
    ]:
        require_false(row, "uses_kids_data_vector_values", label)
        if "endpoint_scoring_allowed" in row:
            require_false(row, "endpoint_scoring_allowed", label)

    if operator_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("operator must remain not derived before null-safety gate")
    if spectrum_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("spectrum attempt must not mark operator derived")
    if null_replay["contains_control_scores"] != "false":
        raise SystemExit("null replay scores must not enter operator null-safety gate")
    if null_readiness["current_controls_executed"] != "true":
        raise SystemExit("null controls must be replayed before null-safety gate")
    if e_web_null["e_web_null_control_uniform"] != "true":
        raise SystemExit("uniform E_web null control is required for this audit")

    control_families = null_readiness["control_families"]
    rows = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N1_source_frozen_null_family_inventory",
            "status": "SATISFIED",
            "source_artifact": rel(NULL_READINESS),
            "requirement": "Null-control families must be frozen before endpoint scoring and before any operator-null claim.",
            "current_evidence": (
                f"control_family_count={null_readiness['control_family_count']}; "
                f"control_families={control_families}; "
                f"control_draw_count={null_readiness['control_draw_count']}"
            ),
            "operator_null_implication": "control_inventory_exists_but_is_not_operator_theorem",
            "dimension_check": "null_transforms_act_on_dimensionless_theory_vector_shell",
            "limit_check": "zero_or_wrong_channel_controls_must_not_be_promoted_to_positive_path_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N2_no_endpoint_feedback_in_null_replay",
            "status": "SATISFIED",
            "source_artifact": rel(NULL_REPLAY),
            "requirement": "Null-control replay must not read KiDS En values, residuals, fit statistics, posterior chains, or control scores.",
            "current_evidence": (
                f"uses_kids_data_vector_values={null_replay['uses_kids_data_vector_values']}; "
                f"contains_control_scores={null_replay['contains_control_scores']}; "
                f"contains_fit_statistics={null_replay['contains_fit_statistics']}"
            ),
            "operator_null_implication": "leakage_prevention_passes_for_available_null_replay",
            "dimension_check": "no_observed_lensing_units_enter_the_null_operator_audit",
            "limit_check": "audit_can_be_rebuilt_without_endpoint_scores",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N3_domain_and_codomain_support",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": f"{rel(D_PATH_SUMMARY)};{rel(MAPPING_SUMMARY)}",
            "requirement": "The future null-safe operator must have a source-side path domain and a retained 300-row COSEBIs codomain.",
            "current_evidence": (
                f"source_scope={d_path['source_scope']}; "
                f"target_rows={mapping['target_rows']}; "
                f"unique_d_path_values={d_path['unique_d_path_value_count_rounded_1e_minus_12']}"
            ),
            "operator_null_implication": "domain_and_codomain_exist_but_path_domain_is_caveated_mask_load_proxy",
            "dimension_check": "source_proxy_and_row_carrier_are_dimensionless_before_endpoint_amplitude",
            "limit_check": "uniform_domain_proxy_should_not_create_positive_non_null_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N4_uniform_web_null_control",
            "status": "SATISFIED_AS_NULL_CONTROL_ONLY",
            "source_artifact": rel(E_WEB_NULL),
            "requirement": "A wrong-channel or null-web route must remain a null control, not a physical web/environment claim.",
            "current_evidence": (
                f"e_web_null_control_uniform={e_web_null['e_web_null_control_uniform']}; "
                f"positive_web_claim_allowed={e_web_null['positive_web_claim_allowed']}"
            ),
            "operator_null_implication": "wrong_channel_activation_can_be_a_control_but_not_a_gauge_descent_proof",
            "dimension_check": "uniform_null_control_value_is_dimensionless",
            "limit_check": "uniform_web_environment_has_no_positive_environmental_readout_claim",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N5_mask_null_operator_response",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_mask_null_response_operator",
            "requirement": "A pure survey-mask perturbation must be shown to map to a quotient-trivial response or an explicitly controlled null direction.",
            "current_evidence": "Mask-route and mask-load proxies exist, but no operator-level pure-mask response theorem is present.",
            "operator_null_implication": "cannot_yet_claim_mask_null_safety_for_survey_native_mode_response",
            "dimension_check": "mask_transform_should_preserve_source_normalization_and_row_domain",
            "limit_check": "pure_mask_change_must_not_generate_positive_tau_residual",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N6_gauge_quotient_descent",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_gauge_quotient_descent_argument",
            "requirement": "The mode-response operator must descend to the physical quotient by killing gauge/coordinate representation changes.",
            "current_evidence": "Existing null replays are deterministic controls; they do not prove quotient descent.",
            "operator_null_implication": "operator_level_gauge_safety_not_proven",
            "dimension_check": "gauge_transform_should_not_change_physical_units_or_normalization",
            "limit_check": "coordinate_or_representation_change_should_leave_physical_response_class_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N7_spectrum_null_coupling",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(SPECTRUM_SUMMARY),
            "requirement": "The conditional mode spectrum must be coupled to null transforms by the same source-native operator, not by a separate envelope assumption.",
            "current_evidence": (
                f"conditional_primary_spectrum={spectrum_summary['conditional_primary_spectrum']}; "
                f"mode_response_operator_derived={spectrum_summary['mode_response_operator_derived']}"
            ),
            "operator_null_implication": "n_minus_half_envelope_remains_conditional_until_null_safe_operator_generates_it",
            "dimension_check": "mode_spectrum_is_dimensionless_unit_mean_carrier",
            "limit_check": "smooth_prior_rejection_of_high_or_oscillatory_modes_is_not_a_null_safety_theorem",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "N8_standard_lensing_zero_tau_limit",
            "status": "SPECIFIED_NOT_DERIVED",
            "source_artifact": rel(OPERATOR_SUMMARY),
            "requirement": "When the Tau residual channel is zero, the operator contribution must vanish and standard lensing remains the baseline.",
            "current_evidence": f"operator_spec_verdict={operator_summary['operator_spec_verdict']}",
            "operator_null_implication": "zero_tau_limit_is_required_but_not_yet_derived_from_survey_native_operator",
            "dimension_check": "endpoint_amplitude_or_lensing_units_enter_only_after_operator_freeze",
            "limit_check": "tau_channel_zero_implies_no_additive_cosebis_response",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "OPERATOR_NULL_SAFETY_GATE_BLOCKED_NOT_DERIVED",
            "selected_statistic": policy["selected_statistic"],
            "gate_rows": str(len(rows)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in rows)),
            "satisfied_caveated_count": str(sum(row["status"] == "SATISFIED_CAVEATED" for row in rows)),
            "satisfied_as_null_control_only_count": str(sum(row["status"] == "SATISFIED_AS_NULL_CONTROL_ONLY" for row in rows)),
            "specified_not_derived_count": str(sum(row["status"] == "SPECIFIED_NOT_DERIVED" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "null_control_family_count": null_readiness["control_family_count"],
            "null_control_draw_count": null_readiness["control_draw_count"],
            "operator_null_safety_proven": "false",
            "mask_null_operator_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "spectrum_null_coupling_proven": "false",
            "mode_response_operator_derived": "false",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "null_controls_exist_but_operator_level_null_safety_remains_blocked",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_NULL_SAFETY_GATE_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
