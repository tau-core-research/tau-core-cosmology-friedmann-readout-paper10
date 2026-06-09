#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv"
AMP_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv"
AMP_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv"
AMP_ROWS = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv"
UNITS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"
NULL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
COV_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv"


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
    amp_policy = read_one(AMP_POLICY)
    amp_summary = read_one(AMP_SUMMARY)
    amp_row = read_one(AMP_ROWS)
    units_summary = read_one(UNITS_SUMMARY)
    null_summary = read_one(NULL_SUMMARY)
    cov_summary = read_one(COV_SUMMARY)

    if policy["status"] != "PHYSICAL_AMPLITUDE_REQUIREMENTS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected physical amplitude requirements policy status")
    if policy["parent_source_side_amplitude_policy"] != amp_policy["policy_id"]:
        raise SystemExit("source-side amplitude parent mismatch")
    if policy["parent_physical_operator_units_policy"] != units_summary["policy_id"]:
        raise SystemExit("physical units parent mismatch")
    if policy["parent_operator_null_safety_policy"] != null_summary["policy_id"]:
        raise SystemExit("operator null-safety parent mismatch")

    for label, row in [
        ("policy", policy),
        ("source amplitude policy", amp_policy),
        ("source amplitude summary", amp_summary),
        ("physical units summary", units_summary),
        ("operator null summary", null_summary),
        ("covariance summary", cov_summary),
    ]:
        require_false(label, row, ["endpoint_scoring_allowed"])
    for label, row in [
        ("policy", policy),
        ("source amplitude policy", amp_policy),
        ("source amplitude summary", amp_summary),
        ("physical units summary", units_summary),
        ("operator null summary", null_summary),
    ]:
        require_false(label, row, ["uses_kids_data_vector_values"])

    if amp_summary["source_side_amplitude_map_derived"] != "true":
        raise SystemExit("dimensionless source-side amplitude map must exist first")
    if amp_summary["physical_amplitude_units_derived"] != "false":
        raise SystemExit("source-side amplitude attempt must not already derive physical units")
    if amp_row["amplitude_units"] != "dimensionless" or amp_row["amplitude_value"] != "1.000000000000e+00":
        raise SystemExit("source-side amplitude must be the unit dimensionless normalization")
    if units_summary["physical_operator_units_derived"] != "false":
        raise SystemExit("physical operator units must remain open in this requirements gate")
    if null_summary["operator_null_safety_proven"] != "false":
        raise SystemExit("operator null safety must remain open in this requirements gate")

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P1_dimensionless_source_amplitude_available",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": f"{rel(AMP_SUMMARY)};{rel(AMP_ROWS)}",
            "requirement": "Start from the frozen source-side unit normalization A_src=1.",
            "current_evidence": f"dimensionless_amplitude_value={amp_summary['dimensionless_amplitude_value']}; amplitude_units={amp_row['amplitude_units']}",
            "physical_amplitude_requirement": "future_physical_amplitude_must_extend_A_src_without_endpoint_feedback",
            "dimension_check": "A_src_is_dimensionless_and_cannot_by_itself_carry_cosebis_response_units",
            "known_limit_check": "unit_source_normalization_does_not_change_the_zero_source_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P2_response_unit_normalization_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(UNITS_SUMMARY),
            "requirement": "Derive the response-unit normalization that maps the dimensionless source kernel into the retained COSEBIs statistic.",
            "current_evidence": f"physical_operator_units_derived={units_summary['physical_operator_units_derived']}; covariance_metric_available={units_summary['covariance_metric_available']}",
            "physical_amplitude_requirement": "derive_units_for_A_phys_so_that_A_phys_K_i_has_cosebis_response_units",
            "dimension_check": "A_phys_must_supply_the_missing_response_units_not_supplied_by_dimensionless_K_i",
            "known_limit_check": "response_units_must_reduce_to_zero_tau_contribution_in_standard_lensing_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P3_standard_lensing_null_amplitude_required",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(NULL_SUMMARY),
            "requirement": "Prove that the physical amplitude vanishes or routes to a null-control response when the Tau path/readout source is absent.",
            "current_evidence": f"operator_null_safety_proven={null_summary['operator_null_safety_proven']}; standard_lensing_null_normalization_proven={units_summary['standard_lensing_null_normalization_proven']}",
            "physical_amplitude_requirement": "derive_no_tau_source_limit_for_A_phys",
            "dimension_check": "null_amplitude_is_a_statement_about_physical_response_after_units_are_supplied",
            "known_limit_check": "standard_lensing_no_tau_source_limit_must_not_generate_positive_cosebis_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P4_covariance_metric_not_amplitude_derivation",
            "status": "REQUIREMENT_FROZEN",
            "source_artifact": rel(COV_SUMMARY),
            "requirement": "Keep the covariance metric separate from the physical amplitude derivation.",
            "current_evidence": f"positive_definite={cov_summary['positive_definite']}; cholesky_ready={cov_summary['cholesky_ready']}; contains_fit_statistics={cov_summary['contains_fit_statistics']}",
            "physical_amplitude_requirement": "covariance_can_score_a_future_vector_but_cannot_set_A_phys",
            "dimension_check": "covariance_readiness_does_not_define_source_response_units",
            "known_limit_check": "a_good_scoring_metric_does_not_imply_nonzero_tau_source",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "P5_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The physical-amplitude requirements gate must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "physical_amplitude_requirement": "future_A_phys_derivation_must_be_source_side_or_theorem_side_before_endpoint_replay",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_gate",
            "known_limit_check": "requirements_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "PHYSICAL_AMPLITUDE_REQUIREMENTS_FROZEN_NOT_DERIVED",
            "selected_statistic": policy["selected_statistic"],
            "gate_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in ledger)),
            "requirement_frozen_count": str(sum(row["status"] == "REQUIREMENT_FROZEN" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "dimensionless_source_amplitude_available": "true",
            "dimensionless_amplitude_value": amp_summary["dimensionless_amplitude_value"],
            "physical_amplitude_units_derived": "false",
            "response_unit_normalization_derived": "false",
            "standard_lensing_null_amplitude_proven": "false",
            "covariance_metric_used_as_amplitude_derivation": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_AMPLITUDE_REQUIREMENTS_GATE_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
