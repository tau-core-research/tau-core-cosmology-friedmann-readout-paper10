#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv"
MAPPING = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1.csv"
MAPPING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
THEORY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
SPECTRUM = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv"
SPECTRUM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"
LEAKAGE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
QUOTIENT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
OPERATOR = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def float_text(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    mapping_summary = read_one(MAPPING_SUMMARY)
    theory_summary = read_one(THEORY_SUMMARY)
    spectrum_summary = read_one(SPECTRUM_SUMMARY)
    leakage_summary = read_one(LEAKAGE_SUMMARY)
    quotient_summary = read_one(QUOTIENT_SUMMARY)
    mapping_rows = read_rows(MAPPING)
    spectrum_rows = read_rows(SPECTRUM)

    if policy["status"] != "SURVEY_NATIVE_OPERATOR_CONSTRUCTION_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected operator construction attempt policy status")
    for label, row in [
        ("policy", policy),
        ("mapping summary", mapping_summary),
        ("theory summary", theory_summary),
        ("spectrum summary", spectrum_summary),
        ("leakage summary", leakage_summary),
        ("quotient summary", quotient_summary),
    ]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit(f"{label} must keep uses_kids_data_vector_values=false")
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit(f"{label} must keep endpoint_scoring_allowed=false")
    if mapping_summary["mapping_vector_computed"] != "true":
        raise SystemExit("source-frozen mapping vector must exist before operator attempt")
    if spectrum_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("this attempt must not inherit a derived mode-response operator")
    if leakage_summary["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("operator leakage theorem must remain unproven")
    if quotient_summary["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("gauge quotient descent must remain unproven")

    weights = {
        int(row["mode"]): float(row["unit_mean_weight"])
        for row in spectrum_rows
        if row["spectrum_family"] == spectrum_summary["conditional_primary_spectrum"]
    }
    if set(weights) != set(range(1, 21)):
        raise SystemExit("conditional primary spectrum must provide modes 1..20")

    operator_rows: list[dict[str, str]] = []
    values: list[float] = []
    for row in mapping_rows:
        mode = int(row["mode"])
        mapping_value = float(row["source_frozen_mapping_value"])
        mode_weight = weights[mode]
        value = mapping_value * mode_weight
        values.append(value)
        operator_rows.append(
            {
                "policy_id": policy["policy_id"],
                "row_index_zero_based": row["row_index_zero_based"],
                "row_index_one_based": row["row_index_one_based"],
                "selected_statistic": policy["selected_statistic"],
                "pair_id": row["pair_id"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "mode": row["mode"],
                "source_mapping_component": float_text(mapping_value),
                "mode_response_component": float_text(mode_weight),
                "operator_kernel_value": float_text(value),
                "operator_factorization_rule": "source_mapping_component_times_conditional_log_band_mode_response",
                "operator_skeleton_constructed": "true",
                "operator_theorem_proven": "false",
                "mask_leakage_theorem_proven": "false",
                "gauge_quotient_descent_proven": "false",
                "contains_theory_vector": "true",
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
        )

    min_value = min(values)
    max_value = max(values)
    mean_value = sum(values) / len(values)
    ledger = [
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O1_domain_codomain_available",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": f"{rel(MAPPING_SUMMARY)};{rel(SPECTRUM_SUMMARY)}",
            "requirement": "A source-side mapping domain and retained 300-row COSEBIs codomain must be available before an operator skeleton can be attempted.",
            "current_evidence": f"target_rows={mapping_summary['target_rows']}; conditional_primary_spectrum={spectrum_summary['conditional_primary_spectrum']}",
            "operator_construction_implication": "factorized_source_to_cosebis_operator_skeleton_can_be_written",
            "dimension_check": "source_mapping_component_and_mode_response_component_are_dimensionless_kernel_weights",
            "known_limit_check": "zero_source_mapping_component_or_zero_mode_response_component_gives_zero_operator_kernel_value",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O2_factorized_operator_skeleton_constructed",
            "status": "SATISFIED_CAVEATED",
            "source_artifact": rel(OPERATOR),
            "requirement": "Construct the first source-side factorized skeleton K_i = M_i S_n without endpoint amplitude, residuals, posterior chains, or fit feedback.",
            "current_evidence": f"operator_rows={len(operator_rows)}; min={float_text(min_value)}; max={float_text(max_value)}; mean={float_text(mean_value)}",
            "operator_construction_implication": "operator_skeleton_exists_but_is_not_yet_a_survey_native_theorem",
            "dimension_check": "unit_amplitude_kernel_is_dimensionless_until_physical_operator_units_are_derived",
            "known_limit_check": "unit_mean_mapping_and_unit_mean_mode_response_keep_mean_kernel_near_unity",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O3_mask_leakage_theorem_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(LEAKAGE_SUMMARY),
            "requirement": "The skeleton cannot be interpreted as physical until pure-mask directions are proven quotient-trivial or controlled.",
            "current_evidence": f"operator_leakage_theorem_proven={leakage_summary['operator_leakage_theorem_proven']}",
            "operator_construction_implication": "positive_kernel_value_cannot_yet_be_separated_from_possible_mask_only_leakage_at_operator_level",
            "dimension_check": "mask_leakage_controls_are_dimensionless_and_do_not_set_physical_amplitude",
            "known_limit_check": "uniform_mask_null_limit_available_but_nonuniform_leakage_risk_remains",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O4_gauge_quotient_descent_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": rel(QUOTIENT_SUMMARY),
            "requirement": "The skeleton cannot be promoted to a Tau-side operator theorem until representation changes descend to the same quotient-visible response.",
            "current_evidence": f"gauge_quotient_descent_proven={quotient_summary['gauge_quotient_descent_proven']}",
            "operator_construction_implication": "operator_skeleton_is_representative_level_until_quotient_descent_is_proven",
            "dimension_check": "representative_changes_must_preserve_units_and_response_class",
            "known_limit_check": "tile_relabeling_and_normalization_changes_must_not_change_physical_response",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O5_no_endpoint_feedback",
            "status": "SATISFIED",
            "source_artifact": rel(POLICY),
            "requirement": "The construction attempt must not use KiDS En values, residuals, fit statistics, posterior chains, random noise, or endpoint scores.",
            "current_evidence": "uses_kids_data_vector_values=false; uses_fit_statistics=false; endpoint_scoring_allowed=false",
            "operator_construction_implication": "operator_skeleton_is_source_side_and_predeclared",
            "dimension_check": "no_observed_lensing_units_or_chi2_statistics_enter_this_attempt",
            "known_limit_check": "construction_can_be_rebuilt_without_endpoint_data",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "gate_id": "O6_physical_operator_units_open",
            "status": "OPEN_BLOCKER",
            "source_artifact": "future_physical_operator_units_derivation",
            "requirement": "A physical survey-native operator must derive the units and normalization connecting the dimensionless source kernel to COSEBIs response units.",
            "current_evidence": f"contains_theory_vector={theory_summary['contains_theory_vector']}; contains_predictions={theory_summary['contains_predictions']}",
            "operator_construction_implication": "unit_amplitude_kernel_is_not_a_physical_prediction_until_units_and_amplitude_are_derived",
            "dimension_check": "current_kernel_is_dimensionless_unit_amplitude",
            "known_limit_check": "standard_lensing_null_limit_and_zero_tau_source_limit_must_be_recovered_after_unit_derivation",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "SURVEY_NATIVE_OPERATOR_SKELETON_CONSTRUCTED_THEOREM_OPEN",
            "selected_statistic": policy["selected_statistic"],
            "operator_rows": str(len(operator_rows)),
            "ledger_rows": str(len(ledger)),
            "satisfied_count": str(sum(row["status"] == "SATISFIED" for row in ledger)),
            "satisfied_caveated_count": str(sum(row["status"] == "SATISFIED_CAVEATED" for row in ledger)),
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "operator_skeleton_constructed": "true",
            "survey_native_operator_constructed": "false",
            "operator_theorem_proven": "false",
            "operator_leakage_theorem_proven": "false",
            "mask_leakage_theorem_proven": "false",
            "gauge_quotient_descent_proven": "false",
            "physical_operator_units_derived": "false",
            "mode_response_operator_derived": "false",
            "min_operator_kernel_value": float_text(min_value),
            "max_operator_kernel_value": float_text(max_value),
            "mean_operator_kernel_value": float_text(mean_value),
            "contains_theory_vector": "true",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "factorized_source_side_operator_skeleton_exists_but_operator_theorem_remains_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OPERATOR, operator_rows)
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_CONSTRUCTION_ATTEMPT_V1_COMPLETE "
        f"verdict={summary[0]['verdict']} open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
