#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv"
UNITS_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"
C_NORM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
AMPLITUDE = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv"


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
    units_summary = read_one(UNITS_SUMMARY)
    c_norm_summary = read_one(C_NORM_SUMMARY)
    operator_summary = read_one(OPERATOR_SUMMARY)

    if policy["status"] != "SOURCE_SIDE_AMPLITUDE_MAP_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected source-side amplitude map policy status")
    for label, row in [
        ("policy", policy),
        ("units summary", units_summary),
        ("c_norm summary", c_norm_summary),
        ("operator summary", operator_summary),
    ]:
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit(f"{label} must keep endpoint_scoring_allowed=false")
    for label, row in [("policy", policy), ("operator summary", operator_summary)]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit(f"{label} must keep uses_kids_data_vector_values=false")
    if units_summary["dimensionless_source_kernel_identified"] != "true":
        raise SystemExit("dimensionless source kernel must be identified first")
    if c_norm_summary["mean_normalized_source_weight_fde"] != "1.000000000000e+00":
        raise SystemExit("source-side c_norm must enforce unit mean")
    if abs(float(operator_summary["mean_operator_kernel_value"]) - 1.0) > 1.0e-12:
        raise SystemExit("operator kernel mean must be unit-normalized before amplitude attempt")

    amplitude_value = 1.0
    amplitude_rows = [
        {
            "policy_id": policy["policy_id"],
            "amplitude_id": "A_src_unit_mean_dimensionless",
            "status": "DIMENSIONLESS_SOURCE_AMPLITUDE_MAP_CONSTRUCTED",
            "selected_statistic": policy["selected_statistic"],
            "amplitude_value": f"{amplitude_value:.12e}",
            "amplitude_units": "dimensionless",
            "amplitude_rule": "unit_mean_source_normalization_A_src_equals_one",
            "source_artifact": f"{rel(C_NORM_SUMMARY)};{rel(OPERATOR_SUMMARY)}",
            "physical_units_derived": "false",
            "endpoint_calibrated": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "A1_unit_mean_source_normalization_available",
            "status": "SATISFIED_AS_SOURCE_LIMIT",
            "source_artifact": rel(C_NORM_SUMMARY),
            "requirement": "A dimensionless source-side amplitude can only be frozen after source weights are normalized without endpoint feedback.",
            "current_evidence": f"c_norm_value={c_norm_summary['c_norm_value']}; mean_normalized_source_weight_fde={c_norm_summary['mean_normalized_source_weight_fde']}",
            "amplitude_implication": "unit_mean_source_normalization_supports_A_src_equals_one",
            "dimension_check": "A_src_is_dimensionless_because_it_normalizes_dimensionless_source_weights",
            "known_limit_check": "unit_mean_normalization_keeps_mean_source_weight_equal_to_one",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "A2_dimensionless_amplitude_map_constructed",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": rel(AMPLITUDE),
            "requirement": "Freeze the source-side dimensionless amplitude map A_src=1 for the unit-mean kernel.",
            "current_evidence": "A_src=1.000000000000e+00; amplitude_units=dimensionless",
            "amplitude_implication": "operator_skeleton_has_a_source_normalized_scale_but_no_physical_units",
            "dimension_check": "dimensionless_amplitude_does_not_convert_kernel_to_cosebis_units",
            "known_limit_check": "zero_source_kernel_still_gives_zero_after_multiplication_by_A_src",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "A3_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The amplitude attempt must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "amplitude_implication": "A_src_is_not_a_fit_or_residual_calibration",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_attempt",
            "known_limit_check": "attempt_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "A4_physical_amplitude_units_not_derived",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(UNITS_SUMMARY),
            "requirement": "A physical amplitude carrying COSEBIs response units must be derived before endpoint prediction.",
            "current_evidence": f"physical_operator_units_derived={units_summary['physical_operator_units_derived']}; source_side_amplitude_map_derived={units_summary['source_side_amplitude_map_derived']}",
            "amplitude_implication": "dimensionless_A_src_does_not_close_physical_amplitude_blocker",
            "dimension_check": "physical_amplitude_must_carry_missing_response_units",
            "known_limit_check": "physical_amplitude_must_respect_standard_lensing_null_limit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "A5_standard_lensing_null_amplitude_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(UNITS_SUMMARY),
            "requirement": "The future physical amplitude must vanish or route to null controls in the no-Tau-source limit.",
            "current_evidence": f"standard_lensing_null_normalization_proven={units_summary['standard_lensing_null_normalization_proven']}",
            "amplitude_implication": "A_src_equals_one_is_only_internal_normalization_not_a_standard_lensing_null_theorem",
            "dimension_check": "null_amplitude_statement_requires_physical_units_after_operator_derivation",
            "known_limit_check": "no_tau_source_should_not_create_positive_cosebis_response",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "DIMENSIONLESS_SOURCE_SIDE_AMPLITUDE_MAP_CONSTRUCTED_PHYSICAL_AMPLITUDE_OPEN",
            "selected_statistic": policy["selected_statistic"],
            "amplitude_rows": str(len(amplitude_rows)),
            "ledger_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_as_source_limit_count": str(sum(row["status"] == "SATISFIED_AS_SOURCE_LIMIT" for row in ledger)),
            "satisfied_caveated_count": str(sum(row["status"] == "SATISFIED_CAVEATED" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "dimensionless_source_side_amplitude_map_constructed": "true",
            "dimensionless_amplitude_value": f"{amplitude_value:.12e}",
            "source_side_amplitude_map_derived": "true",
            "physical_amplitude_units_derived": "false",
            "physical_operator_units_derived": "false",
            "endpoint_calibrated_amplitude": "false",
            "standard_lensing_null_amplitude_proven": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "dimensionless_source_amplitude_map_exists_but_physical_amplitude_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(AMPLITUDE, amplitude_rows)
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_SIDE_AMPLITUDE_MAP_ATTEMPT_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
