#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_replay_run_v1.csv"
AUTH_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_response_v1_summary.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_grid.csv"


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

    require(run["status"] == "LOW_Z_VOID_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "run status mismatch")
    require(auth["verdict"] == "low_z_void_replay_authorized_permission_only_not_validation", "authorization missing")
    require(auth["endpoint_run_allowed"] == "true", "authorization must allow this one replay")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim validation")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_verdict"] == auth["verdict"], "summary authorization mismatch")
    require(summary["n_rows"] == auth["included_rows"], "summary row count must match authorization")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["claim_boundary"] == "low_z_void_replay_permission_only_not_validation", "claim boundary mismatch")
    require("W_VOID_MATURITY" in summary["active_channels"], "void channel must be active")
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
    ]:
        require(marker in run["forbidden_inputs"], f"forbidden marker missing: {marker}")
    branches = {row["branch"] for row in grid}
    required = {
        "baseline_only",
        "void_only",
        "wrong_void_sign",
        "wrong_void_threshold",
        "deterministic_shuffled_void_within_low_z_mask",
        "zero_void_amplitude",
    }
    require(required <= branches, f"missing grid branches: {sorted(required - branches)}")
    for key in [
        "baseline_best_chi2_lowz_distance",
        "void_best_chi2_lowz_distance",
        "wrong_void_sign_best_chi2_lowz_distance",
        "wrong_void_threshold_best_chi2_lowz_distance",
        "shuffled_best_chi2_lowz_distance",
        "zero_void_amplitude_best_chi2_lowz_distance",
        "delta_chi2_void_minus_baseline",
        "delta_aic_void_minus_baseline",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        float(summary[key])
    require(int(summary["n_rows"]) == 424, "low-z replay row count changed")
    require(int(summary["controls_better_than_candidate_chi2"]) >= 0, "invalid control count")
    require(all(row["claim_boundary"] == "low_z_void_replay_permission_only_not_validation" for row in grid), "grid claim boundary mismatch")
    print(
        "PAPER10_LOW_Z_PANTHEON_VOID_REPLAY_V1_VALIDATED "
        f"delta_chi2={summary['delta_chi2_void_minus_baseline']} "
        f"rank={summary['candidate_rank_by_chi2_among_void_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
