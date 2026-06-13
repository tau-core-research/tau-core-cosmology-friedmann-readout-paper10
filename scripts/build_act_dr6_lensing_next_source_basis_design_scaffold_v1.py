#!/usr/bin/env python3
"""Build the next-source-basis design scaffold for the ACT DR6 path route.

This artifact is deliberately not a replay authorization.  It records the
source-side requirements that a future ACT observer/path attempt must satisfy
before any endpoint score is allowed.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_next_source_basis_design_scaffold_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv"


ROWS = [
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_01_PHYSICAL_K_PATH_MAPPING",
        "required_source_side_content": (
            "source-native convergence-to-path response units or a theorem-bounded mapping "
            "from ACT kappa samples to a K_path amplitude"
        ),
        "allowed_role": "future_source_basis_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "endpoint_scores;distance_residuals;fit_statistics;best_fit_amplitude",
        "claim_boundary": "no physical K_path promotion until this mapping is frozen source-side",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_02_OPERATOR_QUOTIENT_DESCENT",
        "required_source_side_content": (
            "operator-level rule separating E-mode path response from curl/gauge/null response, "
            "including quotient-triviality conditions"
        ),
        "allowed_role": "future_source_basis_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "curl_endpoint_performance;distance_residuals;fit_statistics",
        "claim_boundary": "curl remains K_null control unless quotient descent is independently justified",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_03_MASK_COVERAGE_POPULATION_POLICY",
        "required_source_side_content": (
            "predeclared sky scope, mask-positive rule, outside-mask handling, and population-coverage "
            "interpretation before replay"
        ),
        "allowed_role": "future_source_basis_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "posthoc_row_dropping;endpoint_score_thresholds;distance_residuals",
        "claim_boundary": "coverage policy may define scope but cannot rescue a branch after scoring",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_04_SOURCE_BASIS_RECENTER_STRESS",
        "required_source_side_content": (
            "predeclared recentering or standardization stress that is computed from source rows only "
            "and run as a control, not as an endpoint rescue"
        ),
        "allowed_role": "future_control_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "posthoc_recenter_rescue;endpoint_scores;distance_residuals",
        "claim_boundary": "recenter stress is a null/robustness control, not a positive tuning channel",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_05_CONTROL_SUITE_PRECOMMIT",
        "required_source_side_content": (
            "predeclared off, baseline-only, curl-null, frequency-difference-null, wrong-sign, "
            "deterministic-shuffle, rank-reverse, and recenter-stress controls"
        ),
        "allowed_role": "future_control_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": (
            "endpoint_score_based_control_selection;selecting_controls_after_score;"
            "dropping_best_controls;family_winner"
        ),
        "claim_boundary": "future replay must beat or explicitly survive its frozen controls",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_06_CHANNEL_HANDOFF_DECISION",
        "required_source_side_content": (
            "predeclared handoff verdict among K_path, K_closure, K_null, or source-diagnostic-only, "
            "with no endpoint-score dependency"
        ),
        "allowed_role": "future_source_basis_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "endpoint_scores;fit_statistics;posthoc_channel_promotion",
        "claim_boundary": "channel promotion requires source-side justification before replay",
    },
    {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "design_requirement_id": "ACT_NEXT_BASIS_07_FORBIDDEN_ENDPOINT_FIELDS",
        "required_source_side_content": (
            "machine-checkable forbidden-field ledger covering endpoint residuals, scores, fit statistics, "
            "winner labels, fitted amplitudes, and posthoc family choices"
        ),
        "allowed_role": "leakage_prevention_requirement",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "forbidden_inputs": "endpoint_residuals;endpoint_scores;fit_statistics;winner_labels;fitted_amplitudes",
        "claim_boundary": "source basis cannot be built from any endpoint-side information",
    },
]


def main() -> None:
    SOURCE_MANIFEST.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ROWS[0]))
        writer.writeheader()
        writer.writerows(ROWS)

    summary = {
        "artifact_id": "ACT_DR6_LENSING_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_V1",
        "status": "NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN",
        "requirements_count": str(len(ROWS)),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "family_verdict_allowed": "false",
        "current_branch_status": "previous_ACT_branch_quarantined_control_dominated",
        "next_branch_allowed_action": "source_basis_design_and_external_review_before_any_replay",
        "forbidden_action": (
            "reuse_current_endpoint_scores;posthoc_recenter_rescue;physical_K_path_promotion;"
            "endpoint_replay_without_new_source_basis_review"
        ),
        "claim_boundary": (
            "this scaffold defines future source-basis requirements only; it is not replay "
            "authorization and not evidence for an ACT path-weight signal"
        ),
        "verdict": "ACT_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN_NOT_REPLAY",
    }
    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)


if __name__ == "__main__":
    main()
