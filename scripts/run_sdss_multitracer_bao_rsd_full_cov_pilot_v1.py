#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_growth_web_source_native_pilot_v1 import fsigma8_lcdm
    from run_pantheon_pilot_scoring_v1 import parse_range, read_one
except ImportError:
    from scripts.run_growth_web_source_native_pilot_v1 import fsigma8_lcdm
    from scripts.run_pantheon_pilot_scoring_v1 import parse_range, read_one


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_design_matrix_v1.csv"
RUN = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_grid.csv"


def e_lcdm(z: np.ndarray, omega_m: float) -> np.ndarray:
    return np.sqrt(omega_m * (1.0 + z) ** 3 + (1.0 - omega_m))


def comoving_integral(z_value: float, omega_m: float) -> float:
    grid = np.linspace(0.0, z_value, 1024)
    return float(np.trapezoid(1.0 / e_lcdm(grid, omega_m), grid))


def model_vector(
    z: np.ndarray,
    observables: list[str],
    w_web: np.ndarray,
    omega_m: float,
    sigma8_0: float,
    q_bao: float,
    mu_web: float,
    active_web: np.ndarray,
) -> np.ndarray:
    fs8 = fsigma8_lcdm(z, omega_m, sigma8_0) * (1.0 + mu_web * active_web)
    e_values = e_lcdm(z, omega_m)
    dm_values = np.array([q_bao * comoving_integral(float(item), omega_m) for item in z])
    dh_values = q_bao / e_values
    out = np.empty_like(z)
    for idx, observable in enumerate(observables):
        if observable == "DM_over_rd":
            out[idx] = dm_values[idx]
        elif observable == "DH_over_rd":
            out[idx] = dh_values[idx]
        elif observable == "fsigma8":
            out[idx] = fs8[idx]
        else:
            raise SystemExit(f"unknown observable: {observable}")
    return out


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("SDSS multitracer pilot status mismatch")
    if run["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("SDSS multitracer pilot must remain endpoint disabled")
    forbidden = run["forbidden_inputs"]
    for marker in ["distance_residuals", "growth_residuals", "fit_improvement_driven_grid_changes"]:
        if marker not in forbidden:
            raise SystemExit(f"SDSS multitracer pilot missing forbidden marker: {marker}")

    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    z = np.array([float(row["z_eff"]) for row in rows])
    observed = np.array([float(row["observed_value"]) for row in rows])
    observables = [row["observable"] for row in rows]
    w_web_raw = np.array([float(row["W_web_source_native_basis"]) for row in rows])
    applies = np.array([row["W_web_applies_to_observable"] == "true" for row in rows])
    w_web = np.where(applies, w_web_raw, 0.0)
    cov = np.loadtxt(ROOT / rows[0]["covariance_path"])
    factor = linalg.cho_factor(cov, lower=True, check_finite=False)
    eig = np.linalg.eigvalsh(cov)

    omega_m_grid = parse_range(run["omega_m_grid"])
    sigma8_grid = parse_range(run["sigma8_0_grid"])
    q_bao_grid = parse_range(run["q_bao_grid"])
    mu_web_grid = parse_range(run["mu_web_grid"])
    rng = np.random.default_rng(int(run["random_seed"]))
    shuffled_web = w_web[rng.permutation(len(w_web))]
    zero = np.zeros_like(w_web)

    grid_rows: list[dict[str, str]] = []

    def add_row(
        branch: str,
        omega_m: float,
        sigma8_0: float,
        q_bao: float,
        mu_web: float,
        active_web: np.ndarray,
    ) -> None:
        prediction = model_vector(z, observables, w_web, omega_m, sigma8_0, q_bao, mu_web, active_web)
        residual = observed - prediction
        solved = linalg.cho_solve(factor, residual, check_finite=False)
        chi2 = float(residual @ solved)
        k_eff = 3 if branch == "baseline_only" else 4
        aic = chi2 + 2 * k_eff
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "sigma8_0": f"{sigma8_0:.12g}",
                "q_bao": f"{q_bao:.12g}",
                "mu_web": f"{mu_web:.12g}",
                "chi2": f"{chi2:.12g}",
                "aic": f"{aic:.12g}",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "sdss_multitracer_bao_rsd_full_cov_pilot_not_validation",
            }
        )

    for omega_m in omega_m_grid:
        for sigma8_0 in sigma8_grid:
            for q_bao in q_bao_grid:
                add_row("baseline_only", omega_m, sigma8_0, q_bao, 0.0, zero)
                for mu_web in mu_web_grid:
                    add_row("web_growth_shell", omega_m, sigma8_0, q_bao, mu_web, w_web)
                    add_row("wrong_web_sign", omega_m, sigma8_0, q_bao, mu_web, -w_web)
                    add_row("deterministic_shuffled_web", omega_m, sigma8_0, q_bao, mu_web, shuffled_web)

    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(grid_rows)

    by_branch: dict[str, list[dict[str, str]]] = {}
    for row in grid_rows:
        by_branch.setdefault(row["branch"], []).append(row)
    best = {branch: min(items, key=lambda row: float(row["chi2"])) for branch, items in by_branch.items()}
    base = best["baseline_only"]
    web = best["web_growth_shell"]
    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "n_rows": str(len(z)),
        "baseline_best_chi2": base["chi2"],
        "baseline_best_aic": base["aic"],
        "web_best_chi2": web["chi2"],
        "web_best_aic": web["aic"],
        "web_best_omega_m": web["omega_m"],
        "web_best_sigma8_0": web["sigma8_0"],
        "web_best_q_bao": web["q_bao"],
        "web_best_mu_web": web["mu_web"],
        "delta_chi2_web_minus_baseline": f"{float(web['chi2']) - float(base['chi2']):.12g}",
        "delta_aic_web_minus_baseline": f"{float(web['aic']) - float(base['aic']):.12g}",
        "wrong_web_sign_best_chi2": best["wrong_web_sign"]["chi2"],
        "shuffled_web_best_chi2": best["deterministic_shuffled_web"]["chi2"],
        "active_channels": run["active_channels"],
        "disabled_channels": run["disabled_channels"],
        "covariance_policy": run["covariance_policy"],
        "covariance_min_eigenvalue": f"{float(eig[0]):.12g}",
        "covariance_condition_number": f"{float(eig[-1] / eig[0]):.12g}",
        "claim_boundary": "sdss_multitracer_bao_rsd_full_cov_pilot_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_V1_COMPLETE "
        f"delta_chi2={summary['delta_chi2_web_minus_baseline']} "
        "claim_boundary=sdss_multitracer_bao_rsd_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
