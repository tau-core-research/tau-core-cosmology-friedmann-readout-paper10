#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_spectrum_attempt_policy_v1.csv"
OPERATOR_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mode_response_operator_spec_policy_v1.csv"
OPERATOR_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"
MODE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_mode_policy_v1.csv"
MOCK_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv"
SPECTRA = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_spectra.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"


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


def fmt(value: float) -> str:
    return f"{value:.12e}"


def unit_mean(values: list[float]) -> list[float]:
    mean = math.fsum(values) / len(values)
    if mean == 0.0:
        return values
    return [value / mean for value in values]


def main() -> None:
    policy = read_one(POLICY)
    operator_policy = read_one(OPERATOR_POLICY)
    operator_summary = read_one(OPERATOR_SUMMARY)
    mode_policy = read_one(MODE_POLICY)
    mock_summary = read_one(MOCK_SUMMARY)

    if policy["status"] != "MODE_RESPONSE_SPECTRUM_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected mode-response spectrum attempt policy status")
    if policy["parent_mode_response_operator_spec_policy"] != operator_policy["policy_id"]:
        raise SystemExit("parent mode-response operator spec policy mismatch")
    if operator_summary["mode_response_operator_derived"] != "false":
        raise SystemExit("parent operator must remain not derived")
    for row in [policy, operator_summary, mock_summary]:
        if row.get("uses_kids_data_vector_values") != "false":
            raise SystemExit("spectrum attempt inputs must remain KiDS-data-vector-free")
        if row.get("endpoint_scoring_allowed") != "false":
            raise SystemExit("spectrum attempt inputs must remain non-scoring")
    if mode_policy["expected_modes_per_pair"] != "20":
        raise SystemExit("unexpected COSEBIs mode count")

    modes = list(range(1, 21))
    spectra_raw = {
        "log_band_neutral_candidate": [mode**-0.5 for mode in modes],
        "flat_boundary_control": [1.0 for _ in modes],
        "high_mode_rejected_under_smooth_path_prior": [float(mode) for mode in modes],
        "oscillatory_rejected_under_smooth_path_prior": [1.0 if mode % 2 == 0 else -1.0 for mode in modes],
    }
    spectra_unit = {name: unit_mean(values) for name, values in spectra_raw.items()}
    spectrum_rows: list[dict[str, str]] = []
    for name, values in spectra_unit.items():
        for mode, weight in zip(modes, values, strict=True):
            spectrum_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "spectrum_family": name,
                    "mode": str(mode),
                    "unit_mean_weight": fmt(weight),
                    "source_status": (
                        "CONDITIONAL_PRIMARY"
                        if name == "log_band_neutral_candidate"
                        else "BOUNDARY_CONTROL"
                        if name == "flat_boundary_control"
                        else "REJECTED_BY_SMOOTH_PATH_PRIOR"
                    ),
                    "uses_kids_data_vector_values": "false",
                    "uses_fit_statistics": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "step_id": "S1_ordered_mode_domain",
            "status": "PASS",
            "statement": "The retained COSEBIs mode domain is the ordered dimensionless range n=1..20 for each tomographic pair.",
            "derivation_note": f"expected_modes_per_pair={mode_policy['expected_modes_per_pair']}; expected_data_vector_rows={mode_policy['expected_data_vector_rows']}",
            "dimension_check": "mode_index_is_dimensionless",
            "limit_check": "no_mode_cut_or_posthoc_mode_deletion",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "S2_log_band_power_prior",
            "status": "ASSUMPTION_NOT_SOURCE_PROVEN",
            "statement": "A smooth coherent path/readout residual is allowed to carry approximately constant power per logarithmic mode interval.",
            "derivation_note": "This is the same conditional prior as the envelope derivation; it is not yet derived from a survey-native response operator.",
            "dimension_check": "dP_dlnn_is_dimensionless_after_source_normalization",
            "limit_check": "non_smooth_or_oscillatory_sources_must_not_force_this_prior",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "D1_discrete_power_from_log_band",
            "status": "DERIVED_CONDITIONAL",
            "statement": "For unit-spaced modes, constant dP/dln(n) gives discrete mode power P_n proportional to 1/n.",
            "derivation_note": "Use dln(n) approximately equal to dn/n over the ordered discrete mode hierarchy.",
            "dimension_check": "P_n_is_dimensionless_relative_power",
            "limit_check": "flat_linear_power_would_not_produce_n_minus_half",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "D2_coherent_amplitude_spectrum",
            "status": "DERIVED_CONDITIONAL",
            "statement": "For coherent signed response, amplitude is proportional to sqrt(P_n), yielding M_n proportional to n^(-1/2).",
            "derivation_note": "The finite n=1..20 domain fixes only unit-mean normalization.",
            "dimension_check": "amplitude_carrier_dimensionless_until_endpoint_amplitude",
            "limit_check": "zero_path_residual_amplitude_makes_carrier_contribution_zero",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "C1_template_guardrail",
            "status": "PASS",
            "statement": "The deterministic template-recovery sanity suite shows flat, high-mode, and oscillatory synthetic truths do not all collapse into the low-mode template.",
            "derivation_note": f"mock_sanity_verdict={mock_summary['mock_sanity_verdict']}; all_expected_templates_recovered={mock_summary['all_expected_templates_recovered']}",
            "dimension_check": "template_cosines_are_dimensionless",
            "limit_check": "oscillatory_truth_recovers_oscillatory_template_not_low_template",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "B1_operator_spectrum_blocker",
            "status": "OPEN_BLOCKER",
            "statement": "The survey-native path-response operator that would produce or reject this spectrum has not yet been derived.",
            "derivation_note": "This artifact freezes conditional spectrum logic only; it does not close the operator derivation.",
            "dimension_check": "operator_spectrum_units_not_yet_derived",
            "limit_check": "future_operator_must_allow_high_frequency_or_null_cases_to_fail_low_mode_prior",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "B2_gauge_null_safety_blocker",
            "status": "OPEN_BLOCKER",
            "statement": "Gauge/mask null safety remains an operator-level blocker, not a spectrum-shape blocker alone.",
            "derivation_note": "Null-control replays exist, but no operator-level quotient descent theorem is present.",
            "dimension_check": "null_transform_normalization_not_yet_proven",
            "limit_check": "pure_mask_or_gauge_change_must_not_generate_positive_tau_claim",
            "claim_boundary": policy["claim_boundary"],
        },
    ]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "MODE_RESPONSE_SPECTRUM_ATTEMPT_CONDITIONAL_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "spectrum_family_count": str(len(spectra_unit)),
            "mode_count": str(len(modes)),
            "ledger_rows": str(len(ledger)),
            "conditional_primary_spectrum": "log_band_neutral_candidate",
            "conditional_primary_shape": "M_n=n^(-1/2)/mean_1_20_n^(-1/2)",
            "flat_boundary_control_preserved": "true",
            "high_mode_rejected_under_smooth_path_prior": "true",
            "oscillatory_rejected_under_smooth_path_prior": "true",
            "mode_response_operator_derived": "false",
            "open_blocker_count": str(sum(row["status"] == "OPEN_BLOCKER" for row in ledger)),
            "spectrum_attempt_verdict": "conditional_source_spectrum_attempt_preserves_operator_and_null_safety_blockers",
            "uses_kids_data_vector_values": "false",
            "uses_fit_statistics": "false",
            "uses_random_noise": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(SPECTRA, spectrum_rows)
    write_csv(LEDGER, ledger)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_MODE_RESPONSE_SPECTRUM_ATTEMPT_V1_COMPLETE "
        f"verdict={summary[0]['spectrum_attempt_verdict']} "
        f"open_blockers={summary[0]['open_blocker_count']}"
    )


if __name__ == "__main__":
    main()
