#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv"
ENDPOINT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv"
DIAGNOSTICS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_diagnostics_v1_summary.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"
TOMO_PLAUSIBILITY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv"
JACKKNIFE = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv"
MODE_LOCAL = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"
MODE_SHAPE = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv"
PHYSICAL = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"

OUT_LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv"
OUT_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    endpoint = read_one(ENDPOINT)
    diagnostics = read_one(DIAGNOSTICS)
    tomo = read_one(TOMO)
    tomo_plausibility = read_one(TOMO_PLAUSIBILITY)
    jackknife = read_one(JACKKNIFE)
    mode_local = read_one(MODE_LOCAL)
    mode_shape = read_one(MODE_SHAPE)
    physical = read_one(PHYSICAL)

    if policy["status"] != "ENDPOINT_SCORING_SYNTHESIS_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected synthesis ledger policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("synthesis ledger must not compute new scores")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("synthesis ledger must not claim endpoint validation")
    if endpoint["endpoint_scoring_executed"] != "true":
        raise SystemExit("endpoint scoring must be executed before synthesis")
    if endpoint["endpoint_validation_claimed"] != "false":
        raise SystemExit("endpoint scoring summary must not claim validation")
    if physical["physical_promotion_ready"] != "false":
        raise SystemExit("physical promotion should remain blocked in this synthesis")

    rows = [
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S0_endpoint_score",
            "component_status": "DIAGNOSTIC_ENDPOINT_SIGNAL_PRESENT",
            "evidence_summary": (
                f"candidate_delta_chi2={endpoint['candidate_delta_chi2_vs_baseline']};"
                f"candidate_rank={endpoint['candidate_rank_by_chi2']}/"
                f"{int(endpoint['null_control_count']) + 1};"
                f"plus_one_tail_fraction={endpoint['plus_one_tail_fraction_chi2']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "endpoint_score_not_validation",
            "recommended_next_action": "preserve_as_diagnostic_endpoint_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S1_null_control_diagnostics",
            "component_status": "LOW_TAIL_NOT_ABSOLUTE_WINNER",
            "evidence_summary": (
                f"better_controls={diagnostics['better_than_candidate_chi2_count']};"
                f"families={diagnostics['families_with_better_than_candidate']};"
                f"verdict={diagnostics['diagnostic_verdict']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "tomographic_shuffle_controls_beat_candidate",
            "recommended_next_action": "deepen_tomographic_structure_controls",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S2_tomographic_structure_robustness",
            "component_status": "TOMOGRAPHIC_CAVEAT_ACTIVE",
            "evidence_summary": (
                f"candidate_rank={tomo['candidate_rank_by_chi2']}/"
                f"{int(tomo['control_count']) + 1};"
                f"controls_better={tomo['controls_better_than_candidate_chi2']};"
                f"families={tomo['families_with_better_than_candidate']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "structured_tomographic_controls_still_outperform_candidate",
            "recommended_next_action": "use_independent_tomographic_holdout_or_external_lensing_probe",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S2b_tomographic_control_plausibility",
            "component_status": "BETTER_CONTROLS_NOT_ACCEPTED_AS_PHYSICAL_ALTERNATIVES",
            "evidence_summary": (
                f"better_audited={tomo_plausibility['better_than_candidate_audited_count']};"
                f"control_only={tomo_plausibility['better_control_only_count']};"
                f"conditional_source_systematic={tomo_plausibility['better_conditional_source_systematic_count']};"
                f"accepted_physical_alternatives={tomo_plausibility['accepted_physical_alternative_count']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "better_controls_block_validation_but_do_not_refute_endpoint_signal",
            "recommended_next_action": "freeze_independent_photoz_or_tomographic_calibration_holdout",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S3_jackknife_localization",
            "component_status": "NOT_SINGLE_BIN_OR_PAIR",
            "evidence_summary": (
                f"leave_one_source_or_pair_negative_delta_chi2="
                f"{jackknife['leave_one_subsets_with_negative_delta_chi2']}/20;"
                f"localization={jackknife['localization_verdict']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "mode_band_caveat_remains",
            "recommended_next_action": "keep_low_mode_localization_caveat_explicit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S4_mode_localization",
            "component_status": "LOW_MODE_LOCALIZED",
            "evidence_summary": (
                f"best_single={mode_local['best_single_mode_subset_id']};"
                f"best_cumulative={mode_local['best_cumulative_low_subset_id']};"
                f"without_low={mode_local['first_without_low_non_improving_subset_id']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "signal_is_low_mode_localized_not_broad_mode_validation",
            "recommended_next_action": "ground_low_mode_carrier_source_side_before_stronger_claims",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S5_mode_shape_stress",
            "component_status": "LOW_WEIGHTED_CARRIER_PREFERRED_CAVEATED",
            "evidence_summary": (
                f"best_shape={mode_shape['best_mode_shape_id']};"
                f"candidate_beats_flat={mode_shape['candidate_beats_flat_chi2']};"
                f"high_mode_weighting_removes_signal={mode_shape['high_mode_weighting_removes_signal']}"
            ),
            "supports_endpoint_signal": "true",
            "caveat": "carrier_sensitive_but_not_exact_carrier_only",
            "recommended_next_action": "derive_survey_native_mode_response_operator",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "S6_physical_promotion",
            "component_status": "PHYSICAL_PROMOTION_BLOCKED",
            "evidence_summary": (
                f"open_blockers={physical['open_blocker_count']};"
                f"verdict={physical['verdict']}"
            ),
            "supports_endpoint_signal": "false",
            "caveat": "diagnostic_endpoint_ready_does_not_imply_physical_prediction",
            "recommended_next_action": "resolve_physical_promotion_blockers_before_validation_claims",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "ENDPOINT_SCORING_SYNTHESIS_LEDGER_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "ledger_rows": str(len(rows)),
            "diagnostic_endpoint_signal_present": "true",
            "candidate_low_tail": "true",
            "candidate_absolute_winner": "false",
            "tomographic_caveat_active": "true",
            "better_tomographic_controls_accepted_as_physical_alternatives": "false",
            "jackknife_supports_not_single_bin_or_pair": "true",
            "low_mode_localized": "true",
            "mode_shape_candidate_preferred": "true",
            "physical_promotion_ready": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": policy["uses_kids_data_vector_values_for_scoring"],
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "recommended_next_scoring_action": "tomographic_structure_holdout_or_independent_lensing_probe_before_physical_promotion",
            "verdict": "endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT_LEDGER, rows)
    write_csv(OUT_SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_SYNTHESIS_LEDGER_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
