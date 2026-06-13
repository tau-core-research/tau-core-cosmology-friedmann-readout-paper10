#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_run.csv"
)
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv"
)
GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_grid.csv"
)
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_authorized_replay_permission_only_not_validation"
BRANCHES = {
    "baseline_only",
    "primary_centered_sky_z_candidate",
    "off",
    "wrong_sign",
    "deterministic_shuffle",
    "rank_reverse",
    "axis_x_reference",
    "axis_y_reference",
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

    require(
        run["status"] == "V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION",
        "bad run status",
    )
    require(auth["decision"] == "GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY", "missing authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow one replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_lensing_path_weight_claimed"] == "false", "authorization must not claim path physics")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_decision"] == auth["decision"], "authorization decision mismatch")
    require(summary["active_family"] == "W_path_times_centered_sky_z", "active family mismatch")
    require(summary["n_rows"] == "12", "observer-orientation V2 replay must use exactly 12 rows")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for channel in ["W_VOID_SOURCE_BASIS_REFINEMENT", "W_WEB_ANISOTROPY", "W_TIME_READOUT"]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_sky_direction_selection",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
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
        "baseline_best_chi2",
        "candidate_best_chi2",
        "candidate_best_aic",
        "best_control_chi2",
        "best_control_aic",
        "delta_chi2_candidate_minus_baseline",
        "delta_aic_candidate_minus_baseline",
        "delta_chi2_candidate_minus_best_control",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        float(summary[key])
    require(int(summary["candidate_rank_by_chi2_among_candidate_and_controls"]) >= 1, "bad rank")
    require(int(summary["controls_better_than_candidate_chi2"]) >= 0, "bad control count")
    require(
        summary["verdict"]
        in {
            "observer_orientation_v2_permission_replay_family_control_survives_not_validation",
            "observer_orientation_v2_permission_replay_not_control_resistant_not_validation",
        },
        "bad verdict",
    )
    print(
        "PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTHORIZED_REPLAY_VALIDATED "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary['candidate_rank_by_chi2_among_candidate_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
