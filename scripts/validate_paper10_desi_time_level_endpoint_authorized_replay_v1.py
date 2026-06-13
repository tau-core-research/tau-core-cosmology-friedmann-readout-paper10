#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv"
GRID = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_authorized_replay_permission_only_not_validation"
BRANCHES = {
    "candidate_beta_free",
    "rd_off_control",
    "external_prior_width_stress",
    "wrong_prior_control",
    "BAO_pair_drop_control",
    "CC_match_window_stress",
    "level_slope_swap_control",
    "redshift_order_shuffle_control",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    summary = read_one(SUMMARY)
    grid = read_rows(GRID)
    require(run["status"] == "DESI_TIME_LEVEL_ENDPOINT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION", "bad run template")
    require(auth["decision"] == "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY", "missing authorization")
    require(auth["endpoint_replay_allowed"] == "true", "authorization must allow permission-only replay")
    require(auth["endpoint_validation_claimed"] == "false", "authorization must not claim validation")
    require(auth["physical_validation_claimed"] == "false", "authorization must not claim physical validation")
    require(summary["status"] == "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION", "bad summary status")
    require(summary["authorization_decision"] == auth["decision"], "authorization decision mismatch")
    require(summary["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_LEVEL", "bad route family")
    require(summary["n_rows"] == "5", "replay must use five authorized rows")
    require(summary["excluded_radial_rows"] == "5", "high-z row exclusion mismatch")
    require(summary["branch_count"] == "8", "bad branch count")
    require(set(row["branch"] for row in grid) == BRANCHES, "branch set mismatch")
    require(summary["endpoint_replay_allowed"] == "true", "summary must record replay permission")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in grid:
        require(row["authorized_scope_rows"] == "0;1;2;3;4", "grid scope mismatch")
        require(row["endpoint_replay_allowed"] == "true", "grid must record replay permission")
        require(row["endpoint_validation_claimed"] == "false", "grid must not claim validation")
        require(row["physical_validation_claimed"] == "false", "grid must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        for key in ["beta_rd_used", "sigma_beta_rd_free", "chi2", "aic", "prior_penalty"]:
            float(row[key])
    for key in [
        "candidate_beta_rd",
        "candidate_sigma_beta_rd",
        "candidate_chi2",
        "candidate_aic",
        "planck_beta_rd_prior",
        "planck_sigma_beta_rd_prior",
        "candidate_delta_beta_minus_planck_prior",
        "best_control_chi2",
        "best_control_aic",
        "delta_chi2_candidate_minus_best_control",
    ]:
        float(summary[key])
    require(
        summary["verdict"]
        in {
            "desi_time_level_permission_replay_control_survives_not_validation",
            "desi_time_level_permission_replay_not_control_resistant_not_validation",
        },
        "bad verdict",
    )
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZED_REPLAY_VALIDATED "
        f"verdict={summary['verdict']} "
        f"candidate_chi2={summary['candidate_chi2']}"
    )


if __name__ == "__main__":
    main()
