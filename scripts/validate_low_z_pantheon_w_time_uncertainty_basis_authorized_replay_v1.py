#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_run_template_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv"
GRID = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_authorized_replay_permission_only_not_validation"
BRANCHES = {"baseline_only", "off", "candidate", "wrong_sign", "deterministic_shuffle", "rank_reverse"}


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
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    require(run["status"] == "W_TIME_UNCERTAINTY_BASIS_REPLAY_RUN_PREPARED_AUTH_REQUIRED_NOT_VALIDATION", "bad run template status")
    require(auth["decision"] == "GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY", "missing W_time authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow one replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim physical validation")
    require(summary["status"] == "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "bad summary status")
    require(summary["authorization_decision"] == auth["decision"], "authorization decision mismatch")
    require(summary["active_channel_family"] == "W_TIME_UNCERTAINTY_BASIS", "active family mismatch")
    require(summary["n_rows"] == "424", "W_time replay must use exactly 424 rows")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record permission-only replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for channel in [
        "W_VOID_SOURCE_BASIS_REFINEMENT",
        "W_WEB_ANISOTROPY",
        "W_PATH_PROJECTION",
        "FULL_OBSERVER_PATH_KERNEL",
        "PHYSICAL_CLOCK_DRIFT_CLAIM",
    ]:
        require(channel in summary["disabled_channels"], f"disabled channel missing: {channel}")
    require({row["branch"] for row in grid} == BRANCHES, "branch set mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "424", "grid must use exactly 424 rows")
    for key in [
        "baseline_best_chi2_w_time_replay",
        "candidate_best_chi2_w_time_replay",
        "candidate_best_aic_w_time_replay",
        "best_control_chi2_w_time_replay",
        "delta_chi2_candidate_minus_baseline",
        "delta_aic_candidate_minus_baseline",
        "delta_chi2_candidate_minus_best_control",
    ]:
        float(summary[key])
    require(summary["verdict"] in {
        "w_time_permission_replay_control_survives_not_validation",
        "w_time_permission_replay_not_control_resistant_not_validation",
    }, "bad verdict")
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_AUTHORIZED_REPLAY_V1_VALIDATED "
        f"verdict={summary['verdict']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
