#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_basis_authorized_replay_run_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_v1_summary.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_summary.csv"
GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_authorized_replay_v1_grid.csv"
CLAIM_BOUNDARY = "v2_observer_basis_authorized_replay_permission_only_not_validation"
BRANCHES = {"baseline_only", "candidate", "off", "wrong_sign", "deterministic_shuffle", "rank_reverse"}


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
    require(run["status"] == "V2_OBSERVER_BASIS_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION", "bad run")
    require(auth["decision"] == "GO_OBSERVER_BASIS_REPLAY_PERMISSION_ONLY", "missing authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow permission-only replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(summary["status"] == run["status"], "summary status mismatch")
    require(summary["authorization_decision"] == auth["decision"], "authorization mismatch")
    require(summary["active_family"] == "W_path_x_sky_x_x_zcenter", "family mismatch")
    require(summary["n_rows"] == "12", "must use frozen 12-row scope")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record replay permission")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(set(row["branch"] for row in grid) == BRANCHES, "grid branch set mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid row count mismatch")
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "12", "grid row scope mismatch")
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
            "observer_basis_permission_replay_family_control_survives_not_validation",
            "observer_basis_permission_replay_not_control_resistant_not_validation",
        },
        "bad verdict",
    )
    print(
        "PAPER10_OBSERVER_BASIS_AUTHORIZED_REPLAY_VALIDATED "
        f"delta_chi2_baseline={summary['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary['candidate_rank_by_chi2_among_candidate_and_controls']}"
    )


if __name__ == "__main__":
    main()
