#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_run_v1.csv"
)
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_response_v1_summary.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv"
)
GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_authorized_replay_v1_grid.csv"
)
CLAIM_BOUNDARY = "v2_sky_z_authorized_replay_permission_only_not_validation"
BRANCHES = {"candidate", "off", "wrong_sign", "deterministic_shuffle", "rank_reverse"}


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
    require(run["status"] == "V2_SKY_Z_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "bad run status")
    require(auth["decision"] == "GO_SKY_Z_REPLAY_PERMISSION_ONLY", "missing sky-z authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow one replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_lensing_path_weight_claimed"] == "false", "authorization must not claim path physics")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_decision"] == auth["decision"], "authorization decision mismatch")
    require(summary["active_family"] == "W_path_x_sky_z", "active family mismatch")
    require(summary["n_rows"] == "12", "sky-z replay must use exactly 12 rows")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for channel in [
        "W_VOID_SOURCE_BASIS_REFINEMENT",
        "W_WEB_ANISOTROPY",
        "W_TIME_READOUT",
        "FULL_LOWZ_W_PATH_CHANNEL",
        "OTHER_SKY_ENVIRONMENT_FAMILIES",
    ]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_sky_direction_selection",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
        "physical_validation_claims",
    ]:
        require(marker in run["forbidden_inputs"], f"missing forbidden marker: {marker}")
    family_rows = [row for row in grid if row["family_id"] == "W_path_x_sky_z"]
    baseline_rows = [row for row in grid if row["family_id"] == "baseline_flat_lcdm"]
    require({row["branch"] for row in family_rows} == BRANCHES, "sky-z branch set mismatch")
    require({row["branch"] for row in baseline_rows} == {"baseline_only"}, "baseline branch set mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "12", "grid must use exactly 12 rows")
    for key in [
        "baseline_best_chi2_sky_z_replay",
        "candidate_best_chi2_sky_z_replay",
        "candidate_best_aic_sky_z_replay",
        "best_control_chi2_sky_z_replay",
        "delta_chi2_candidate_minus_baseline",
        "delta_aic_candidate_minus_baseline",
        "delta_chi2_candidate_minus_best_control",
    ]:
        float(summary[key])
    require(summary["family_survives_controls"] == "true", "sky-z family should survive controls")
    require(summary["controls_better_than_candidate_chi2"] == "0", "unexpected better controls")
    require(summary["verdict"] == "sky_z_permission_replay_family_control_survives_not_validation", "bad verdict")
    print(
        "PAPER10_V2_SKY_Z_AUTHORIZED_REPLAY_V1_VALIDATED "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
