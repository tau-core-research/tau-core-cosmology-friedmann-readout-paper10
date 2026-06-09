#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv"
PLAUSIBILITY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_plausibility_audit_v1_summary.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"
ZINV = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
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


def main() -> None:
    policy = read_one(POLICY)
    plausibility = read_one(PLAUSIBILITY)
    tomo = read_one(TOMO)
    zrows = read_rows(ZINV)

    if policy["status"] != "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected holdout gate policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("holdout gate must not compute scores")
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("holdout gate must not authorize endpoint replay")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("holdout gate must not claim validation")
    if plausibility["tomographic_controls_block_validation"] != "true":
        raise SystemExit("tomographic plausibility audit should still block validation")
    if plausibility["accepted_physical_alternative_count"] != "0":
        raise SystemExit("no better tomographic control should be accepted as physical alternative")
    if tomo["controls_better_than_candidate_chi2"] != "3":
        raise SystemExit("expected three better controls in tomographic robustness summary")
    if {row["source_bin"] for row in zrows} != {"1", "2", "3", "4", "5"}:
        raise SystemExit("unexpected source-bin set in redshift inventory")

    rows = [
        {
            "gate_id": policy["policy_id"],
            "step_id": "H0_context",
            "step_status": "DIAGNOSTIC_SIGNAL_RETAINED_NOT_VALIDATED",
            "source_requirement": "keep_current_endpoint_score_as_context_only",
            "allowed_inputs": "committed_endpoint_summaries;committed_control_summaries",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "no_new_score_and_no_validation_claim",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "gate_id": policy["policy_id"],
            "step_id": "H1_independent_tomographic_evidence",
            "step_status": "REQUIRED_BEFORE_REPLAY",
            "source_requirement": "freeze_photoz_or_tomographic_calibration_evidence_independent_of_endpoint_residuals",
            "allowed_inputs": "survey_photoz_calibration;redshift_distributions;tomographic_bin_edges;calibration_quality_flags",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "evidence_manifest_exists_and_validator_confirms_no_endpoint_leakage",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "gate_id": policy["policy_id"],
            "step_id": "H2_holdout_partition_freeze",
            "step_status": "REQUIRED_BEFORE_REPLAY",
            "source_requirement": "predeclare_source_bin_or_tomographic_pair_holdout_partition",
            "allowed_inputs": "source_bin_ids;tomographic_pair_ids;calibration_quality_strata;fixed_random_seed_if_needed",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "holdout_manifest_frozen_before_endpoint_replay",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "gate_id": policy["policy_id"],
            "step_id": "H3_tomographic_alternative_promotion_rule",
            "step_status": "REQUIRED_BEFORE_REPLAY",
            "source_requirement": "define_when_a_control_can_be_promoted_to_source_systematic_candidate",
            "allowed_inputs": "independent_photoz_or_tomographic_calibration_support_only",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "promotion_rule_accepts_no_control_without_independent_calibration_support",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "gate_id": policy["policy_id"],
            "step_id": "H4_replay_protocol_freeze",
            "step_status": "REQUIRED_BEFORE_REPLAY",
            "source_requirement": "freeze_candidate_vector_null_controls_amplitude_rule_and_covariance_policy_for_holdout_replay",
            "allowed_inputs": "source_frozen_vector;null_control_policy;amplitude_rule;covariance_policy;holdout_manifest",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "all_replay_artifacts_exist_and_leakage_validator_passes",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "gate_id": policy["policy_id"],
            "step_id": "H5_authorization_gate",
            "step_status": "BLOCKED_UNTIL_H1_TO_H4_COMPLETE",
            "source_requirement": "authorize_endpoint_replay_only_after_source_side_holdout_and_calibration_freeze",
            "allowed_inputs": "completed_H1_to_H4_manifests",
            "forbidden_inputs": policy["forbidden_endpoint_fields"],
            "completion_condition": "future_gate_may_set_endpoint_replay_allowed_true_after_independent_source_freeze",
            "endpoint_replay_allowed_after_step": "false",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_BUILT",
            "selected_statistic": policy["selected_statistic"],
            "source_bin_count": str(len(zrows)),
            "required_steps": str(len(rows)),
            "completed_steps": "0",
            "requires_independent_photoz_or_tomographic_calibration": "true",
            "requires_holdout_partition_freeze": "true",
            "requires_leakage_validator_before_replay": "true",
            "accepted_physical_alternative_count_in_parent_audit": plausibility["accepted_physical_alternative_count"],
            "tomographic_controls_block_validation": plausibility["tomographic_controls_block_validation"],
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "tomographic_holdout_required_before_endpoint_replay_or_validation",
            "recommended_next_action": "build_source_frozen_photoz_tomographic_calibration_manifest_and_holdout_partition",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
