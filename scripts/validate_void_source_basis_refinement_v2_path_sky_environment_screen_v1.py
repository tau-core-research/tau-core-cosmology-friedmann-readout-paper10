#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv"
FAMILY_SUMMARY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
)
GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_grid.csv"
CLAIM_BOUNDARY = "v2_path_sky_environment_screen_not_endpoint_not_validation"
CANDIDATES = {
    "W_path",
    "W_path_x_sky_x",
    "W_path_x_sky_y",
    "W_path_x_sky_z",
    "W_path_x_tile_offset_ra",
    "W_path_x_tile_offset_dec",
    "W_path_x_los_log_count",
    "W_path_x_los_density_excess",
    "W_path_x_nearest_env_inverse_sep",
    "W_path_x_nearest_env_density_excess",
    "W_path_x_void_wall_proximity",
    "W_path_x_signed_void_wall_proximity",
    "W_path_x_inside_void",
    "W_path_x_void_angular_proximity",
}
CONTROL_BRANCHES = {"off", "wrong_sign", "deterministic_shuffle", "rank_reverse"}
ALLOWED_VERDICTS = {
    "path_sky_environment_candidate_survives_fast_screen_requires_authorization",
    "path_sky_environment_candidate_not_control_resistant_in_fast_screen",
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
    manifest = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    family_summary = read_rows(FAMILY_SUMMARY)
    grid = read_rows(GRID)

    require(
        manifest["status"] == "V2_PATH_SKY_ENVIRONMENT_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT",
        "bad manifest status",
    )
    require(summary["status"] == manifest["status"], "summary status mismatch")
    require(summary["screen_status"] == "preauthorization_diagnostic_not_endpoint", "bad screen status")
    require(summary["n_rows"] == "12", "screen must use exactly 12 rows")
    require(summary["diagnostic_screen_executed"] == "true", "screen not marked executed")
    require(summary["endpoint_replay_allowed"] == "false", "screen must not authorize endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "screen must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "screen must not claim physical path weights")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["verdict"] in ALLOWED_VERDICTS, "unexpected verdict")
    require(set(row["family_id"] for row in family_summary) == CANDIDATES, "family summary set mismatch")
    require(int(summary["family_summary_rows"]) == len(family_summary), "family summary count mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")

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
        require(marker in manifest["forbidden_inputs"], f"missing forbidden marker: {marker}")

    by_family = {family: set() for family in CANDIDATES}
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "12", "grid must use 12 rows")
        require(row["normalization_rule"] == "max_abs_on_12_row_source_scope", "bad normalization")
        if row["family_id"] in by_family:
            by_family[row["family_id"]].add(row["branch"])
        float(row["omega_m"])
        float(row["omega_coupling"])
        if row["chi2_screen"] != "inf":
            float(row["chi2_screen"])
            float(row["aic_screen"])
    for family, branches in by_family.items():
        require({"candidate", *CONTROL_BRANCHES}.issubset(branches), f"missing branch for {family}")

    for row in family_summary:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "family summary claim boundary mismatch")
        require(row["survives_family_controls"] in {"true", "false"}, "bad family verdict flag")
        float(row["candidate_best_chi2_screen"])
        float(row["delta_chi2_candidate_minus_baseline"])
        float(row["delta_chi2_candidate_minus_best_control"])
        int(row["controls_better_than_candidate_chi2"])

    for key in [
        "baseline_best_chi2_screen",
        "best_candidate_chi2_screen",
        "best_candidate_aic_screen",
        "best_control_chi2_screen",
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
        "PAPER10_V2_PATH_SKY_ENVIRONMENT_SCREEN_V1_VALIDATED "
        f"best_family={summary['best_candidate_family']} "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
