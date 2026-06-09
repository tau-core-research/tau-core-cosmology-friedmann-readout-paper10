#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv"
LEAKAGE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv"
LEAKAGE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv"
PURE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
NULL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
SPEC_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"
SPECTRUM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"


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
    leakage_policy = read_one(LEAKAGE_POLICY)
    leakage_summary = read_one(LEAKAGE_SUMMARY)
    pure_summary = read_one(PURE_SUMMARY)
    null_summary = read_one(NULL_SUMMARY)
    spec_summary = read_one(SPEC_SUMMARY)
    spectrum_summary = read_one(SPECTRUM_SUMMARY)

    if policy["status"] != "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_POLICY_FROZEN":
        raise SystemExit("unexpected operator leakage requirements policy status")
    if policy["parent_mask_mode_leakage_audit_policy"] != leakage_policy["policy_id"]:
        raise SystemExit("mask-mode leakage parent mismatch")
    if policy["parent_operator_null_safety_gate_policy"] != null_summary["policy_id"]:
        raise SystemExit("operator null-safety parent mismatch")
    for label, row in [
        ("policy", policy),
        ("leakage summary", leakage_summary),
        ("pure summary", pure_summary),
        ("null summary", null_summary),
        ("spec summary", spec_summary),
        ("spectrum summary", spectrum_summary),
    ]:
        for key in ["uses_kids_data_vector_values", "endpoint_scoring_allowed"]:
            if row.get(key) != "false":
                raise SystemExit(f"{label} must keep {key}=false")

    max_uniform = float(leakage_summary["max_uniform_collapse_norm"])
    max_low_mode_risk = float(leakage_summary["max_low_mode_rms_envelope_norm"])
    if leakage_summary["uniform_collapse_all_null"] != "true" or max_uniform >= 1.0e-10:
        raise SystemExit("uniform pure-mask collapse must be available before freezing requirements")
    if leakage_summary["leakage_risk_recorded"] != "true" or max_low_mode_risk <= 0.0:
        raise SystemExit("nonuniform leakage risk must be recorded before freezing requirements")
    if null_summary["operator_null_safety_proven"] != "false":
        raise SystemExit("requirements gate must not inherit a proven operator-null theorem")
    if spec_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("requirements gate must not mark the mode-response operator derived")

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T1_uniform_tile_null_limit",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": rel(LEAKAGE_SUMMARY),
            "requirement": "The future operator theorem must reproduce the uniform tile-average limit in which centered pure-mask directions collapse to zero.",
            "current_evidence": f"uniform_collapse_all_null=true; max_uniform_collapse_norm={leakage_summary['max_uniform_collapse_norm']}",
            "future_theorem_requirement": "operator_reduces_to_uniform_null_limit_for_centered_pure_mask_basis",
            "dimension_check": "pure_mask_basis_and_uniform_collapse_norm_are_dimensionless",
            "known_limit_check": "uniform_operator_limit_maps_centered_mask_modes_to_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T2_nonuniform_mask_leakage_risk",
            "status": "RISK_RECORDED",
            "source_artifact": rel(LEAKAGE_SUMMARY),
            "requirement": "The future operator theorem must control non-uniform mask load so that mask-only amplitudes cannot masquerade as the low-mode path carrier.",
            "current_evidence": f"max_low_mode_rms_envelope_norm={leakage_summary['max_low_mode_rms_envelope_norm']}",
            "future_theorem_requirement": "nonuniform_mask_response_must_be_projected_to_null_or_independent_control_subspace",
            "dimension_check": "leakage_risk_norm_is_dimensionless_not_a_lensing_prediction",
            "known_limit_check": "risk_disappears_only_in_uniform_limit_or_after_operator_null_projection",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T3_pure_mask_rejection_or_control_subspace",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": f"{rel(PURE_SUMMARY)};{rel(NULL_SUMMARY)}",
            "requirement": "An admissible source-native operator must either reject the pure-mask basis in quotient space or route it into a separately scored null-control family.",
            "current_evidence": f"pure_mask_basis_constructed={pure_summary['pure_mask_basis_constructed']}; mask_null_operator_proven={null_summary['mask_null_operator_proven']}",
            "future_theorem_requirement": "prove_pure_mask_basis_is_quotient_trivial_or_controlled_before_positive_endpoint_interpretation",
            "dimension_check": "pure_mask_basis_is_dimensionless_and_cannot_set_amplitude_units",
            "known_limit_check": "standard_lensing_null_limit_should_not_generate_positive_tau_path_signal_from_mask_only_modes",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T4_mode_spectrum_coupling_requirement",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": f"{rel(SPEC_SUMMARY)};{rel(SPECTRUM_SUMMARY)}",
            "requirement": "The same survey-native operator must connect the conditional mode spectrum to the null-transform checks; separate spectrum and null artifacts are not enough.",
            "current_evidence": f"conditional_primary_spectrum={spectrum_summary['conditional_primary_spectrum']}; mode_response_operator_derived={spec_summary['mode_response_operator_derived']}",
            "future_theorem_requirement": "derive_or_reject_one_operator_that_generates_mode_response_and_null_descent_together",
            "dimension_check": "mode_weights_are_dimensionless_response_weights_not_observed_shear_units",
            "known_limit_check": "operator_must_have_standard_lensing_null_limit_and_no_mask_only_positive_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T5_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": f"{rel(POLICY)};{rel(LEAKAGE_POLICY)}",
            "requirement": "The requirements gate must be source-side only and must not use KiDS En values, residuals, fit statistics, posterior chains, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "future_theorem_requirement": "operator_theorem_inputs_remain_frozen_before_endpoint_replay",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_requirements_gate",
            "known_limit_check": "requirements_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T6_operator_leakage_theorem_not_proven",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_survey_native_operator_leakage_theorem",
            "requirement": "A complete theorem must prove that the source-native path/readout operator sends mask-only directions to quotient-trivial or controlled-null responses.",
            "current_evidence": "requirements are frozen, but no survey-native operator leakage theorem is present",
            "future_theorem_requirement": "prove_operator_level_mask_leakage_safety",
            "dimension_check": "future_operator_must_map_dimensionless_source_modes_to_dimensionally_consistent_cosebis_response",
            "known_limit_check": "standard_lensing_and_uniform_mask_limits_must_be_recovered",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "T7_gauge_quotient_descent_not_proven",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_gauge_quotient_descent_theorem",
            "requirement": "A complete theorem must prove that representation/gauge changes descend to the same quotient-visible response class.",
            "current_evidence": f"gauge_quotient_descent_proven={null_summary['gauge_quotient_descent_proven']}",
            "future_theorem_requirement": "prove_gauge_and_representation_independence_of_the_source_native_operator",
            "dimension_check": "gauge_transformations_should_not_change_physical_units_or_response_amplitude",
            "known_limit_check": "quotient_trivial_transformations_must_not_change_endpoint_predictions",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    open_blockers = sum(row["status"] == "OPEN_BLOCKER" for row in ledger)
    requirement_frozen = sum(row["status"] == "REQUIREMENT_FROZEN" for row in ledger)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN",
            "selected_statistic": policy["selected_statistic"],
            "requirement_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in ledger)),
            "risk_recorded_count": str(sum(row["status"] == "RISK_RECORDED" for row in ledger)),
            "requirement_frozen_count": str(requirement_frozen),
            "open_blocker_count": str(open_blockers),
            "uniform_tile_null_limit_available": "true",
            "nonuniform_leakage_risk_recorded": "true",
            "pure_mask_rejection_requirement_frozen": "true",
            "mode_spectrum_coupling_requirement_frozen": "true",
            "operator_leakage_theorem_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "mode_response_operator_derived": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
