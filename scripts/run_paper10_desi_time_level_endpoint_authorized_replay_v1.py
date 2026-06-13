#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_TEMPLATE = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_v1_summary.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
RD_PRIOR = ROOT / "data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv"
GRID = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_authorized_replay_permission_only_not_validation"
C_KM_S = 299792.458
BRANCHES = [
    "candidate_beta_free",
    "rd_off_control",
    "external_prior_width_stress",
    "wrong_prior_control",
    "BAO_pair_drop_control",
    "CC_match_window_stress",
    "level_slope_swap_control",
    "redshift_order_shuffle_control",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def covariance_from_rows(rows: list[dict[str, str]], allowed: list[int]) -> np.ndarray:
    index = {radial: i for i, radial in enumerate(allowed)}
    cov = np.zeros((len(allowed), len(allowed)), dtype=float)
    for row in rows:
        i = int(row["row_i"])
        j = int(row["row_j"])
        if i in index and j in index:
            cov[index[i], index[j]] = float(row["cov_minus_log_DH_over_rs"])
    return cov


def fit_constant_beta(values: np.ndarray, cov: np.ndarray) -> tuple[float, float, float, float]:
    inv = np.linalg.inv(cov)
    ones = np.ones(len(values), dtype=float)
    denom = float(ones @ inv @ ones)
    beta = float((ones @ inv @ values) / denom)
    resid = values - beta
    chi2 = float(resid @ inv @ resid)
    sigma_beta = math.sqrt(1.0 / denom)
    return beta, sigma_beta, chi2, denom


def chi2_fixed_beta(values: np.ndarray, cov: np.ndarray, beta: float) -> float:
    inv = np.linalg.inv(cov)
    resid = values - beta
    return float(resid @ inv @ resid)


def planck_beta_prior(rd_mpc: float, sigma_rd_mpc: float) -> tuple[float, float]:
    beta = math.log(rd_mpc / C_KM_S)
    sigma_beta = sigma_rd_mpc / rd_mpc
    return beta, sigma_beta


def branch_values(branch: str, base_values: np.ndarray, z: np.ndarray, seed: int) -> tuple[np.ndarray, str]:
    if branch in {
        "candidate_beta_free",
        "rd_off_control",
        "external_prior_width_stress",
        "wrong_prior_control",
        "BAO_pair_drop_control",
        "CC_match_window_stress",
    }:
        return np.array(base_values, copy=True), "identity"
    if branch == "redshift_order_shuffle_control":
        rng = np.random.default_rng(seed)
        return base_values[rng.permutation(len(base_values))], f"deterministic_permutation_seed_{seed}"
    if branch == "level_slope_swap_control":
        order = np.argsort(z)
        z_sorted = z[order]
        v_sorted = base_values[order]
        slope = np.gradient(v_sorted, z_sorted)
        slope_centered = slope - float(np.mean(slope))
        slope_scaled = slope_centered * (float(np.std(v_sorted)) / (float(np.std(slope_centered)) or 1.0))
        out_sorted = float(np.mean(v_sorted)) + slope_scaled
        out = np.empty_like(base_values)
        out[order] = out_sorted
        return out, "finite_difference_slope_substitution"
    raise SystemExit(f"unknown branch {branch}")


def branch_cov(branch: str, cov: np.ndarray, seed: int) -> tuple[np.ndarray, str]:
    if branch != "CC_match_window_stress":
        return np.array(cov, copy=True), "nominal_covariance"
    # Predeclared stress: inflate the CC contribution to represent a looser
    # nearest-neighbor support window without changing row labels or smoothing.
    out = np.array(cov, copy=True)
    out += np.eye(out.shape[0]) * np.median(np.diag(cov))
    return out, f"diagonal_window_stress_seed_{seed}"


def main() -> None:
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    rd = read_one(RD_PRIOR)
    if run["status"] != "DESI_TIME_LEVEL_ENDPOINT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("bad DESI replay run template status")
    if auth["decision"] != "GO_DESI_CC_5ROW_TIME_LEVEL_REPLAY_PERMISSION_ONLY":
        raise SystemExit("DESI time-level replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization must be permission-only and non-validation")
    if auth["physical_validation_claimed"] != "false":
        raise SystemExit("authorization must not claim physical validation")
    if rd["verdict"] != "planck2018_rd_prior_frozen_as_caveated_external_source_not_endpoint":
        raise SystemExit("external rd prior is not frozen")

    allowed = [int(x) for x in run["radial_rows_allowed"].split(";")]
    if allowed != [0, 1, 2, 3, 4]:
        raise SystemExit("DESI replay scope must remain the first five rows")
    rows_all = read_rows(CC_MATCH)
    rows = [row for row in rows_all if int(row["radial_index"]) in allowed]
    if len(rows) != 5:
        raise SystemExit("DESI authorized replay requires exactly five CC-matched rows")
    if any(row["cc_support_status"] != "MATCHED_WITHIN_CC_RANGE" for row in rows):
        raise SystemExit("all authorized rows must be matched within CC range")
    if any(row["cc_extrapolation_used"] != "false" for row in rows):
        raise SystemExit("CC extrapolation is forbidden")

    z = np.array([float(row["z_eff"]) for row in rows], dtype=float)
    y_bao = np.array([float(row["minus_log_DH_over_rs"]) for row in rows], dtype=float)
    logh_cc = np.array([float(row["nearest_cc_logH"]) for row in rows], dtype=float)
    sigma_logh_cc = np.array([float(row["nearest_cc_sigma_logH"]) for row in rows], dtype=float)
    base_values = y_bao - logh_cc
    cov_bao = covariance_from_rows(read_rows(BAO_COV), allowed)
    cov = cov_bao + np.diag(sigma_logh_cc**2)
    beta_prior, sigma_prior = planck_beta_prior(float(rd["rd_mpc"]), float(rd["sigma_rd_mpc"]))
    seeds = {row["control_family"]: int(row["seed"]) for row in read_rows(ROOT / run["control_seed_manifest"])}

    grid: list[dict[str, str]] = []
    for branch in BRANCHES:
        seed = seeds.get(branch, 0)
        values, transform = branch_values(branch, base_values, z, seed)
        active_cov, cov_rule = branch_cov(branch, cov, seed)
        beta_free, sigma_beta_free, chi2_free, _ = fit_constant_beta(values, active_cov)
        beta_used = beta_free
        chi2 = chi2_free
        k_eff = 1
        prior_penalty = 0.0
        branch_rule = "free_constant_beta_rd_nuisance"
        if branch == "rd_off_control":
            beta_used = 0.0
            chi2 = chi2_fixed_beta(values, active_cov, beta_used)
            k_eff = 0
            branch_rule = "fixed_beta_rd_zero"
        elif branch == "external_prior_width_stress":
            beta_used = beta_free
            prior_penalty = ((beta_free - beta_prior) / sigma_prior) ** 2
            chi2 = chi2_free + prior_penalty
            branch_rule = "free_beta_plus_frozen_planck2018_rd_prior_penalty"
        elif branch == "wrong_prior_control":
            beta_used = beta_prior + 5.0 * sigma_prior
            chi2 = chi2_fixed_beta(values, active_cov, beta_used)
            k_eff = 0
            branch_rule = "fixed_wrong_beta_prior_plus_5sigma"
        elif branch == "BAO_pair_drop_control":
            # Deterministic seed selects the first leave-pair subset; this reports
            # the best 3-row beta consistency without changing the authorized
            # five-row endpoint scope.
            rng = np.random.default_rng(seed)
            drop = sorted(rng.choice(np.arange(len(values)), size=2, replace=False).tolist())
            keep = [i for i in range(len(values)) if i not in drop]
            sub_values = values[keep]
            sub_cov = active_cov[np.ix_(keep, keep)]
            beta_used, sigma_beta_free, chi2, _ = fit_constant_beta(sub_values, sub_cov)
            branch_rule = "deterministic_leave_pair_reported_as_control_only"
        aic = chi2 + 2 * k_eff
        grid.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "branch_rule": branch_rule,
                "transform": transform,
                "covariance_rule": cov_rule,
                "n_rows": "5" if branch != "BAO_pair_drop_control" else "3",
                "authorized_scope_rows": "0;1;2;3;4",
                "beta_rd_used": f"{beta_used:.12g}",
                "sigma_beta_rd_free": f"{sigma_beta_free:.12g}",
                "chi2": f"{chi2:.12g}",
                "aic": f"{aic:.12g}",
                "k_eff": str(k_eff),
                "prior_penalty": f"{prior_penalty:.12g}",
                "endpoint_replay_allowed": "true",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(GRID, grid)

    by_branch = {row["branch"]: row for row in grid}
    candidate = by_branch["candidate_beta_free"]
    controls = [row for row in grid if row["branch"] != "candidate_beta_free"]
    best_control = min(controls, key=lambda row: float(row["chi2"]))
    better_controls = [row for row in controls if float(row["chi2"]) < float(candidate["chi2"])]
    summary = [
        {
            "run_id": run["run_id"],
            "status": "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION",
            "authorization_decision": auth["decision"],
            "active_route_family": run["active_route_family"],
            "n_rows": "5",
            "excluded_radial_rows": run["radial_rows_excluded"],
            "branch_count": str(len(grid)),
            "candidate_beta_rd": candidate["beta_rd_used"],
            "candidate_sigma_beta_rd": candidate["sigma_beta_rd_free"],
            "candidate_chi2": candidate["chi2"],
            "candidate_aic": candidate["aic"],
            "planck_beta_rd_prior": f"{beta_prior:.12g}",
            "planck_sigma_beta_rd_prior": f"{sigma_prior:.12g}",
            "candidate_delta_beta_minus_planck_prior": f"{float(candidate['beta_rd_used']) - beta_prior:.12g}",
            "best_control_branch": best_control["branch"],
            "best_control_chi2": best_control["chi2"],
            "best_control_aic": best_control["aic"],
            "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2']) - float(best_control['chi2']):.12g}",
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "family_survives_controls": "true" if not better_controls else "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_time_level_permission_replay_control_survives_not_validation"
            if not better_controls
            else "desi_time_level_permission_replay_not_control_resistant_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZED_REPLAY_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"candidate_chi2={summary[0]['candidate_chi2']}"
    )


if __name__ == "__main__":
    main()
