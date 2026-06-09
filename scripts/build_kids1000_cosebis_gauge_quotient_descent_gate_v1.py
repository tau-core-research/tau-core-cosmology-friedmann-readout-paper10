#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv"
REQ_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv"
REQ_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
NULL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
PREFLIGHT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"


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
    req_policy = read_one(REQ_POLICY)
    req_summary = read_one(REQ_SUMMARY)
    null_summary = read_one(NULL_SUMMARY)
    preflight_summary = read_one(PREFLIGHT_SUMMARY)

    if policy["status"] != "GAUGE_QUOTIENT_DESCENT_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected gauge quotient descent policy status")
    if policy["parent_operator_leakage_theorem_requirements_policy"] != req_policy["policy_id"]:
        raise SystemExit("operator leakage requirements parent mismatch")
    for label, row in [
        ("policy", policy),
        ("requirements summary", req_summary),
        ("null summary", null_summary),
        ("source preflight summary", preflight_summary),
    ]:
        for key in ["uses_kids_data_vector_values", "endpoint_scoring_allowed"]:
            if row.get(key) != "false":
                raise SystemExit(f"{label} must keep {key}=false")
    if req_summary["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("this gate must not inherit a proven quotient descent theorem")

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q1_equivalence_class_declared",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(POLICY),
            "requirement": "Declare the allowed representation changes before endpoint interpretation: tile relabeling, source-basis recentering, admissible normalization changes, and pure gauge/null directions.",
            "current_evidence": "equivalence_classes_declared_but_not_yet_proven_for_survey_native_operator",
            "quotient_descent_requirement": "future_operator_must_depend_only_on_equivalence_classes_not_representatives",
            "dimension_check": "representation_changes_are_dimensionless_or_unit_preserving",
            "known_limit_check": "identity_transform_must_leave_all_source_artifacts_unchanged",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q2_uniform_mask_offset_limit",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": rel(REQ_SUMMARY),
            "requirement": "Uniform mask-offset directions must be quotient-trivial in the centered pure-mask source limit.",
            "current_evidence": f"uniform_tile_null_limit_available={req_summary['uniform_tile_null_limit_available']}",
            "quotient_descent_requirement": "future_operator_must_preserve_uniform_offset_null_limit",
            "dimension_check": "uniform_offset_limit_uses_dimensionless_centered_mask_basis",
            "known_limit_check": "uniform_mask_offset_collapse_is_null",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q3_normalization_representative_independence",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(PREFLIGHT_SUMMARY),
            "requirement": "Changing admissible source normalization representatives must not create or remove a positive quotient-visible path response.",
            "current_evidence": "source_preflight_has_mapping_ready_artifacts_but_no_normalization_invariance_theorem",
            "quotient_descent_requirement": "prove_response_is_invariant_under_allowed_c_norm_and_basis_rescalings_or_route_changes_to_controls",
            "dimension_check": "normalization_changes_must_preserve_cosebis_response_units_after_operator_application",
            "known_limit_check": "zero_path_source_and_null_web_controls_must_remain zero after normalization changes",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q4_tile_relabeling_and_route_coordinate_invariance",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(PREFLIGHT_SUMMARY),
            "requirement": "Tile ordering or route-coordinate relabeling must not change the quotient-visible operator output.",
            "current_evidence": "route domain is indexed and reproducible, but relabeling invariance is not yet an operator theorem",
            "quotient_descent_requirement": "future_operator_must_commute_with_admissible_tile_relabeling_or_use_label_invariant_aggregates",
            "dimension_check": "tile_indices_are_labels_not_physical_units",
            "known_limit_check": "permutation_of_identical_route_tiles_should_not_change_physical_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q5_mask_pure_mode_control_compatibility",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(REQ_SUMMARY),
            "requirement": "The quotient descent theorem must be compatible with the pure-mask rejection or null-control requirement.",
            "current_evidence": f"pure_mask_rejection_requirement_frozen={req_summary['pure_mask_rejection_requirement_frozen']}; mask_null_operator_proven={null_summary['mask_null_operator_proven']}",
            "quotient_descent_requirement": "representation_changes_of_pure_mask_modes_must_stay_in_null_or_control_subspace",
            "dimension_check": "pure_mask_control_modes_are_dimensionless_and_cannot_set_endpoint_amplitudes",
            "known_limit_check": "standard_lensing_null_limit_cannot_gain_positive_path_signal_from_mask_representatives",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q6_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": f"{rel(POLICY)};{rel(REQ_POLICY)}",
            "requirement": "The quotient-descent gate must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "quotient_descent_requirement": "future_descent_theorem_inputs_remain_source_side_and_predeclared",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_gate",
            "known_limit_check": "gate_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q7_gauge_quotient_descent_theorem_not_proven",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_gauge_quotient_descent_theorem",
            "requirement": "A complete theorem must prove that all admissible representation changes descend to the same quotient-visible response class.",
            "current_evidence": "requirements are frozen, but no gauge/quotient descent theorem is present",
            "quotient_descent_requirement": "prove_representation_independence_of_the_survey_native_path_readout_operator",
            "dimension_check": "future_operator_must_map_equivalent_source_representatives_to_dimensionally_consistent_equivalent_responses",
            "known_limit_check": "identity_uniform_mask_and_standard_lensing_null_limits_must_be_recovered",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "Q8_survey_native_operator_not_constructed",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_survey_native_path_readout_operator",
            "requirement": "The survey-native operator must be constructed before quotient descent can be proven rather than specified.",
            "current_evidence": f"mode_response_operator_derived={req_summary['mode_response_operator_derived']}",
            "quotient_descent_requirement": "construct_or_reject_operator_then_test_descent_requirements_on_that_operator",
            "dimension_check": "operator_domain_and_codomain_units_must_be_explicit_before_proof",
            "known_limit_check": "operator_must_reduce_to_standard_lensing_null_limit_when_tau_path_source_is_absent",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "GAUGE_QUOTIENT_DESCENT_REQUIREMENTS_FROZEN_NOT_PROVEN",
            "selected_statistic": policy["selected_statistic"],
            "gate_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in ledger)),
            "requirement_frozen_count": str(sum(row["status"] == "REQUIREMENT_FROZEN" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "equivalence_classes_declared": "true",
            "uniform_mask_offset_limit_available": "true",
            "normalization_invariance_proven": "false",
            "tile_relabeling_invariance_proven": "false",
            "pure_mask_control_compatibility_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "survey_native_operator_constructed": "false",
            "operator_leakage_theorem_proven": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "gauge_quotient_descent_requirements_frozen_but_theorem_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_GATE_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
