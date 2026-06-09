#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
LEAKAGE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
GAUGE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"
NULL_AMP_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"
READINESS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"


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
    operator = read_one(OPERATOR_SUMMARY)
    leakage = read_one(LEAKAGE_SUMMARY)
    gauge = read_one(GAUGE_SUMMARY)
    response = read_one(RESPONSE_SUMMARY)
    null_amp = read_one(NULL_AMP_SUMMARY)
    readiness = read_one(READINESS_SUMMARY)

    if policy["status"] != "PHYSICAL_PROMOTION_BLOCKER_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected physical promotion blocker policy status")
    if policy["parent_operator_construction_attempt_policy"] != operator["policy_id"]:
        raise SystemExit("operator parent mismatch")
    if policy["parent_response_unit_requirements_policy"] != response["policy_id"]:
        raise SystemExit("response-unit parent mismatch")
    if policy["parent_null_amplitude_requirements_policy"] != null_amp["policy_id"]:
        raise SystemExit("null-amplitude parent mismatch")

    for label, row in [
        ("policy", policy),
        ("operator", operator),
        ("leakage", leakage),
        ("gauge", gauge),
        ("response", response),
        ("null amplitude", null_amp),
        ("readiness", readiness),
    ]:
        require_false(label, row, ["endpoint_scoring_allowed"])
    for label, row in [
        ("policy", policy),
        ("operator", operator),
        ("leakage", leakage),
        ("gauge", gauge),
        ("response", response),
        ("null amplitude", null_amp),
    ]:
        require_false(label, row, ["uses_kids_data_vector_values"])

    if operator["operator_skeleton_constructed"] != "true":
        raise SystemExit("source-side operator skeleton must exist")
    if readiness["blocking_component_count"] != "0":
        raise SystemExit("diagnostic endpoint readiness should remain separate and currently unblocked")
    if response["response_unit_normalization_derived"] != "false":
        raise SystemExit("physical promotion ledger must not inherit response-unit derivation")
    if null_amp["standard_lensing_null_amplitude_proven"] != "false":
        raise SystemExit("physical promotion ledger must not inherit null-amplitude theorem")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "G0_diagnostic_endpoint_pipeline_ready_not_physical_promotion",
            "status": "DIAGNOSTIC_READY_NOT_PHYSICAL",
            "source_artifact": rel(READINESS_SUMMARY),
            "current_evidence": f"ready_component_count={readiness['ready_component_count']}; blocking_component_count={readiness['blocking_component_count']}; scoring_executed={readiness['scoring_executed']}",
            "promotion_implication": "diagnostic_endpoint_pipeline_can_run_but_does_not_imply_physical_prediction",
            "required_for_physical_promotion": "all_operator_units_null_and_gauge_blockers_closed_before_physical_claim",
            "dimension_check": "diagnostic_scoring_metric_does_not_supply_physical_response_units",
            "known_limit_check": "diagnostic_readiness_does_not_prove_standard_lensing_no_tau_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "B1_survey_native_operator_theorem_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(OPERATOR_SUMMARY),
            "current_evidence": f"survey_native_operator_constructed={operator['survey_native_operator_constructed']}; operator_theorem_proven={operator['operator_theorem_proven']}; operator_skeleton_constructed={operator['operator_skeleton_constructed']}",
            "promotion_implication": "factorized_source_side_skeleton_exists_but_is_not_a_physical_operator_theorem",
            "required_for_physical_promotion": "derive_or_reject_survey_native_operator_that_generates_the_cosebis_response",
            "dimension_check": "dimensionless_skeleton_cannot_set_physical_response_units",
            "known_limit_check": "future_operator_must_recover_zero_response_when_tau_channel_is_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "B2_operator_leakage_theorem_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(LEAKAGE_SUMMARY),
            "current_evidence": f"operator_leakage_theorem_proven={leakage['operator_leakage_theorem_proven']}; nonuniform_leakage_risk_recorded={leakage['nonuniform_leakage_risk_recorded']}",
            "promotion_implication": "nonuniform_mask_leakage_risk_remains_a_theorem_blocker",
            "required_for_physical_promotion": "prove_mask_only_and_nonuniform_leakage_directions_are_null_or_controlled",
            "dimension_check": "leakage_norms_are_dimensionless_risks_not_lensing_response_units",
            "known_limit_check": "uniform_mask_limit_is_null_but_nonuniform_limit_remains_open",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "B3_gauge_quotient_descent_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(GAUGE_SUMMARY),
            "current_evidence": f"gauge_quotient_descent_proven={gauge['gauge_quotient_descent_proven']}; equivalence_classes_declared={gauge['equivalence_classes_declared']}",
            "promotion_implication": "representation_or_gauge_independence_is_not_yet_proven",
            "required_for_physical_promotion": "prove_response_class_descends_to_the_quotient_before_physical_interpretation",
            "dimension_check": "gauge_transformations_cannot_supply_missing_units_or_amplitude",
            "known_limit_check": "quotient_trivial_transformations_must_leave_physical_response_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "B4_response_unit_normalization_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(RESPONSE_SUMMARY),
            "current_evidence": f"response_unit_normalization_derived={response['response_unit_normalization_derived']}; covariance_metric_used_as_units_derivation={response['covariance_metric_used_as_units_derivation']}",
            "promotion_implication": "dimensionless_A_src_K_i_has_no_physical_cosebis_response_units_yet",
            "required_for_physical_promotion": "derive_response_unit_map_without_endpoint_feedback",
            "dimension_check": "A_phys_or_operator_units_must_carry_missing_cosebis_response_units",
            "known_limit_check": "unit_map_must_be_compatible_with_standard_lensing_null_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "blocker_id": "B5_standard_lensing_null_amplitude_theorem_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(NULL_AMP_SUMMARY),
            "current_evidence": f"standard_lensing_null_amplitude_proven={null_amp['standard_lensing_null_amplitude_proven']}; zero_tau_source_amplitude_statement_specified={null_amp['zero_tau_source_amplitude_statement_specified']}",
            "promotion_implication": "no_tau_source_limit_is_specified_but_not_proven",
            "required_for_physical_promotion": "prove_A_phys_tau_source_zero_equals_zero_or_null_control_response",
            "dimension_check": "null_amplitude_statement_requires_physical_response_space",
            "known_limit_check": "standard_lensing_baseline_must_be_recovered_when_tau_channel_is_absent",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    blocker_count = sum(row["status"] == "OPEN_BLOCKER" for row in rows)
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PHYSICAL_PROMOTION_BLOCKER_LEDGER_BUILT_NOT_CLOSED",
            "selected_statistic": policy["selected_statistic"],
            "ledger_rows": str(len(rows)),
            "diagnostic_ready_not_physical_count": str(sum(row["status"] == "DIAGNOSTIC_READY_NOT_PHYSICAL" for row in rows)),
            "open_blocker_count": str(blocker_count),
            "diagnostic_endpoint_pipeline_ready": "true",
            "physical_promotion_ready": "false",
            "survey_native_operator_theorem_proven": "false",
            "operator_leakage_theorem_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "response_unit_normalization_derived": "false",
            "standard_lensing_null_amplitude_proven": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "diagnostic_endpoint_ready_but_physical_promotion_blocked_by_five_open_requirements",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_PROMOTION_BLOCKER_LEDGER_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
