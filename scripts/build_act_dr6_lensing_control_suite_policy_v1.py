#!/usr/bin/env python3
"""Freeze the ACT DR6 control-suite policy for the path-weight branch."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
BRANCHES = DERIVED / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_branches.csv"
SUMMARY = DERIVED / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_control_suite_policy_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_control_suite_policy_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    diagnostic = read_one(SUMMARY)
    branch_rows = read_rows(BRANCHES)
    available = {row["branch"] for row in branch_rows}
    control_rows = [
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "off",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "zero_path_weight",
            "role": "checks whether any path term is needed relative to baseline",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "baseline_only",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "omega_path_zero_baseline",
            "role": "standard no-path comparator inside the guarded replay grid",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "curl_null",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL_VETO_ACTIVE",
            "source_basis": "ACT_DR6_curl_null_kappa_like_samples",
            "role": "source-native null/control branch; if it beats candidate, promotion is vetoed",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "diff_f150_f090_null",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "ACT_DR6_frequency_difference_null_samples",
            "role": "frequency-difference null/control branch",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "wrong_sign",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "negative_candidate_weight",
            "role": "sign-direction control",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "deterministic_shuffle",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "deterministically_shuffled_candidate_weight",
            "role": "sky-row association null",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "rank_reverse",
            "control_channel": "K_null",
            "current_status": "FROZEN_SCORED_CONTROL",
            "source_basis": "rank_reversed_candidate_weight",
            "role": "monotone-order null",
            "scored_in_current_replay": "true",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_control_selection,endpoint_score_dependent_control_choice",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
            "control_id": "source_basis_recenter_stress",
            "control_channel": "K_null",
            "current_status": "FROZEN_REOPEN_STRESS_NOT_SCORED_IN_CURRENT_REPLAY",
            "source_basis": "alternative_source_side_center_scale_policy",
            "role": (
                "future source-basis reopen stress; forbidden as post-hoc rescue for the "
                "current control-dominated branch"
            ),
            "scored_in_current_replay": "false",
            "endpoint_replay_allowed": "false",
            "validation_claimed": "false",
            "forbidden_inputs": "posthoc_recenter_choice,endpoint_score_dependent_recenter_choice",
        },
    ]

    scored_controls = [row for row in control_rows if row["scored_in_current_replay"] == "true"]
    expected_scored = {row["control_id"] for row in scored_controls}
    missing_scored = sorted(expected_scored - available)
    curl_veto_active = diagnostic["best_control_branch"] == "curl_null"
    summary_row = {
        "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
        "status": "CURRENT_CONTROL_SUITE_FROZEN_VALIDATION_REOPEN_STRESS_DECLARED",
        "scored_control_count": str(len(scored_controls)),
        "declared_control_count": str(len(control_rows)),
        "missing_scored_controls": ";".join(missing_scored) if missing_scored else "none",
        "curl_veto_active": str(curl_veto_active).lower(),
        "best_control_branch": diagnostic["best_control_branch"],
        "controls_better_than_candidate": diagnostic["controls_better_than_candidate"],
        "source_basis_recenter_stress_status": "FROZEN_REOPEN_STRESS_NOT_SCORED_IN_CURRENT_REPLAY",
        "current_suite_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": (
            "posthoc_control_selection,endpoint_score_dependent_control_choice,"
            "posthoc_recenter_choice,endpoint_score_dependent_recenter_choice"
        ),
        "claim_boundary": (
            "freezes the current ACT control suite and preserves source-basis recentering "
            "only as a future reopen stress, not as current endpoint rescue"
        ),
        "verdict": "ACT_REOPEN_07_CONTROL_SUITE_FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED",
    }

    SOURCE_MANIFEST.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(control_rows[0]))
        writer.writeheader()
        writer.writerows(control_rows)
    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_row))
        writer.writeheader()
        writer.writerow(summary_row)


if __name__ == "__main__":
    main()
