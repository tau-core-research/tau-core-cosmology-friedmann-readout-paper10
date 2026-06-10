#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_authorized_replay_run_v1.csv"
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv"
)
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_grid.csv"

CONTROL_BRANCHES = {
    "zero_control",
    "wrong_sign_control",
    "deterministic_row_shuffle_control",
    "threshold_low_control",
    "threshold_high_control",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)

    require(run["status"] == "REFINED_VOID_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "run status mismatch")
    require(auth["verdict"] == "refined_void_replay_authorized_permission_only_not_validation", "authorization missing")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow this replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_verdict"] == auth["verdict"], "summary authorization mismatch")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(
        summary["claim_boundary"] == "void_source_basis_refinement_authorized_replay_permission_only_not_validation",
        "summary claim boundary mismatch",
    )
    require("W_VOID_SOURCE_BASIS_REFINEMENT" == summary["active_channel_family"], "active channel mismatch")
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_source_basis_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        require(marker in run["forbidden_inputs"], f"forbidden marker missing: {marker}")

    require(int(summary["n_rows"]) == 424, "low-z replay row count changed")
    require(int(summary["feature_count"]) >= 1, "no refined source-basis features scored")
    require(int(summary["control_family_count"]) == len(CONTROL_BRANCHES), "control family count mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")
    branches = {row["branch"] for row in grid}
    require("baseline_only" in branches, "baseline branch missing")
    require("candidate_source_feature" in branches, "candidate branch missing")
    require(CONTROL_BRANCHES <= branches, f"missing control branches: {sorted(CONTROL_BRANCHES - branches)}")
    for row in grid:
        require(
            row["claim_boundary"] == "void_source_basis_refinement_authorized_replay_permission_only_not_validation",
            "grid claim boundary mismatch",
        )
    for key in [
        "baseline_best_chi2_lowz_distance",
        "best_candidate_chi2_lowz_distance",
        "best_candidate_aic_lowz",
        "best_control_chi2_lowz_distance",
        "delta_chi2_candidate_minus_baseline",
        "delta_aic_candidate_minus_baseline",
        "delta_chi2_candidate_minus_best_control",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        float(summary[key])
    require(int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1, "invalid candidate rank")
    require(int(summary["controls_better_than_candidate_chi2"]) >= 0, "invalid control count")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_AUTHORIZED_REPLAY_V1_VALIDATED "
        f"best_feature={summary['best_candidate_feature_id']} "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary['candidate_rank_by_chi2_among_candidate_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
