#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_run_v1.csv"
)
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv"
)
GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_grid.csv"
)
CLAIM_BOUNDARY = "v2_path_partial_scope_authorized_replay_permission_only_not_validation"
BRANCHES = {
    "baseline_only",
    "partial_W_path_candidate",
    "path_off_control",
    "wrong_sign_path_control",
    "deterministic_shuffle_path_control",
    "rank_reverse_path_control",
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    require(run["status"] == "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "bad run status")
    require(auth["decision"] == "GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY", "missing authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow one replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_lensing_path_weight_claimed"] == "false", "authorization must not claim path physics")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_decision"] == auth["decision"], "authorization decision mismatch")
    require(summary["n_rows"] == "12", "partial path replay must use exactly 12 rows")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["active_channel_family"] == "W_PATH_PROJECTION_PARTIAL_SCOPE_CONTROL", "active channel mismatch")
    for channel in [
        "W_VOID_SOURCE_BASIS_REFINEMENT",
        "W_WEB_ANISOTROPY",
        "W_TIME_READOUT",
        "FULL_LOWZ_W_PATH_CHANNEL",
    ]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
        "physical_validation_claims",
    ]:
        require(marker in run["forbidden_inputs"], f"missing forbidden marker: {marker}")
    require(set(row["branch"] for row in grid) == BRANCHES, "grid branch set mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "12", "grid must use exactly 12 rows")
    for key in [
        "baseline_best_chi2_partial_path",
        "candidate_best_chi2_partial_path",
        "candidate_best_aic_partial_path",
        "best_control_chi2_partial_path",
        "delta_chi2_candidate_minus_baseline",
        "delta_aic_candidate_minus_baseline",
        "delta_chi2_candidate_minus_best_control",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        float(summary[key])
    require(int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1, "bad rank")
    require(int(summary["controls_better_than_candidate_chi2"]) >= 0, "bad control count")
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_AUTHORIZED_REPLAY_V1_VALIDATED "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary['candidate_rank_by_chi2_among_candidate_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
