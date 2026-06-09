#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv"
PHYS_AMP_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv"
OP_NULL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
NULL_READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"
NULL_REPLAY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1_summary.csv"
GAUGE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
LEAKAGE_REQ_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"


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
    op_null = read_one(OP_NULL_SUMMARY)
    null_readiness = read_one(NULL_READINESS)
    null_replay = read_one(NULL_REPLAY)
    gauge = read_one(GAUGE_SUMMARY)
    leakage_req = read_one(LEAKAGE_REQ_SUMMARY)

    if policy["status"] != "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_POLICY_FROZEN":
        raise SystemExit("unexpected standard-lensing null-amplitude theorem policy status")
    if policy["parent_physical_amplitude_requirements_policy"] != phys_amp["policy_id"]:
        raise SystemExit("physical amplitude parent mismatch")
    if policy["parent_operator_null_safety_policy"] != op_null["policy_id"]:
        raise SystemExit("operator null-safety parent mismatch")

    for label, row in [
        ("policy", policy),
        ("physical amplitude summary", phys_amp),
        ("operator null summary", op_null),
        ("null readiness", null_readiness),
        ("null replay", null_replay),
        ("gauge summary", gauge),
        ("leakage requirements summary", leakage_req),
    ]:
        require_false(label, row, ["endpoint_scoring_allowed"])
    for label, row in [
        ("policy", policy),
        ("physical amplitude summary", phys_amp),
        ("operator null summary", op_null),
        ("null replay", null_replay),
        ("gauge summary", gauge),
        ("leakage requirements summary", leakage_req),
    ]:
        require_false(label, row, ["uses_kids_data_vector_values"])

    if phys_amp["standard_lensing_null_amplitude_proven"] != "false":
        raise SystemExit("requirements gate must not inherit proven null amplitude")
    if op_null["operator_null_safety_proven"] != "false":
        raise SystemExit("requirements gate must not inherit proven operator null safety")
    if gauge["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("requirements gate must not inherit proven gauge descent")
    if null_readiness["current_controls_executed"] != "true":
        raise SystemExit("null controls must be source-replayed before freezing theorem requirements")
    if null_replay["contains_control_scores"] != "false":
        raise SystemExit("null replay scores must not enter theorem requirements")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z1_source_replayed_null_controls_available",
            "status": "SATISFIED_AS_CONTROL_LIMIT",
            "source_artifact": f"{rel(NULL_READINESS)};{rel(NULL_REPLAY)}",
            "requirement": "A standard-lensing null-amplitude theorem may use source-replayed null controls only as control limits, not as fitted evidence.",
            "current_evidence": f"control_family_count={null_readiness['control_family_count']}; control_draw_count={null_readiness['control_draw_count']}; contains_control_scores={null_replay['contains_control_scores']}",
            "theorem_requirement": "null_control_families_remain_controls_when_tau_source_is_absent",
            "dimension_check": "null_controls_act_on_dimensionless_source_frozen_theory_vector_shell",
            "known_limit_check": "no_tau_source_limit_must_not_be_promoted_from_control_replay_to_positive_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z2_zero_tau_source_amplitude_statement",
            "status": "SPECIFIED_NOT_DERIVED",
            "source_artifact": rel(PHYS_AMP_SUMMARY),
            "requirement": "In the no-Tau-source limit the future physical amplitude must vanish or route entirely to null-control response.",
            "current_evidence": f"dimensionless_source_amplitude_available={phys_amp['dimensionless_source_amplitude_available']}; physical_amplitude_units_derived={phys_amp['physical_amplitude_units_derived']}",
            "theorem_requirement": "prove_A_phys_tau_source_zero_equals_zero_or_control_null_response",
            "dimension_check": "A_src_equals_one_is_dimensionless_and_is_not_the_physical_null_amplitude",
            "known_limit_check": "standard_lensing_baseline_is_recovered_when_tau_residual_channel_is_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z3_operator_null_safety_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(OP_NULL_SUMMARY),
            "requirement": "The same operator that generates the source-native response must kill or control pure null, mask, and wrong-channel directions.",
            "current_evidence": f"operator_null_safety_proven={op_null['operator_null_safety_proven']}; mask_null_operator_proven={op_null['mask_null_operator_proven']}; spectrum_null_coupling_proven={op_null['spectrum_null_coupling_proven']}",
            "theorem_requirement": "prove_operator_null_safety_before_physical_null_amplitude_claim",
            "dimension_check": "null_safety_must_hold_before_response_units_are_attached",
            "known_limit_check": "mask_or_wrong_channel_perturbations_must_not_create_positive_tau_cosebis_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z4_gauge_quotient_descent_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(GAUGE_SUMMARY),
            "requirement": "The null-amplitude theorem must descend to the quotient: gauge or representation changes cannot alter the zero physical response.",
            "current_evidence": f"gauge_quotient_descent_proven={gauge['gauge_quotient_descent_proven']}; requirement_frozen_count={gauge['requirement_frozen_count']}",
            "theorem_requirement": "prove_zero_tau_response_is_representation_independent",
            "dimension_check": "gauge_transforms_cannot_supply_missing_physical_units_or_amplitude",
            "known_limit_check": "quotient_trivial_changes_leave_standard_lensing_null_limit_unchanged",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z5_leakage_theorem_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(LEAKAGE_REQ_SUMMARY),
            "requirement": "Non-uniform mask leakage must be controlled by a leakage theorem before it can be excluded from the physical null amplitude.",
            "current_evidence": f"operator_leakage_theorem_proven={leakage_req['operator_leakage_theorem_proven']}; nonuniform_leakage_risk_recorded={leakage_req['nonuniform_leakage_risk_recorded']}",
            "theorem_requirement": "prove_nonuniform_mask_leakage_maps_to_null_or_control_subspace",
            "dimension_check": "leakage_norms_are_dimensionless_risks_not_lensing_response_units",
            "known_limit_check": "uniform_mask_limit_is_null_but_nonuniform_limit_remains_open",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "requirement_id": "Z6_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The theorem-requirements gate must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "theorem_requirement": "future_null_amplitude_theorem_remains_pre_endpoint_and_source_or_theorem_side",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_requirements_gate",
            "known_limit_check": "requirements_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN",
            "selected_statistic": policy["selected_statistic"],
            "requirement_rows": str(len(rows)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in rows)),
            "satisfied_as_control_limit_count": str(sum(row["status"] == "SATISFIED_AS_CONTROL_LIMIT" for row in rows)),
            "specified_not_derived_count": str(sum(row["status"] == "SPECIFIED_NOT_DERIVED" for row in rows)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in rows)),
            "null_controls_available_as_control_limit": "true",
            "zero_tau_source_amplitude_statement_specified": "true",
            "standard_lensing_null_amplitude_proven": "false",
            "operator_null_safety_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "operator_leakage_theorem_proven": "false",
            "physical_amplitude_units_derived": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "standard_lensing_null_amplitude_requirements_frozen_but_theorem_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
