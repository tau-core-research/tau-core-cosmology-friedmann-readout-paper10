#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

try:
    from run_pantheon_pilot_scoring_v1 import parse_range, read_one
except ImportError:
    from scripts.run_pantheon_pilot_scoring_v1 import parse_range, read_one


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "growth_web_source_native_design_matrix_v1.csv"
RUN = ROOT / "data" / "source_manifest" / "growth_web_source_native_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_grid.csv"

GAMMA = 0.55


def e2_lcdm(a: np.ndarray, omega_m: float) -> np.ndarray:
    return omega_m * a ** -3 + (1.0 - omega_m)


def omega_m_a(a: np.ndarray, omega_m: float) -> np.ndarray:
    return omega_m * a ** -3 / e2_lcdm(a, omega_m)


def growth_factor_approx(z: np.ndarray, omega_m: float) -> np.ndarray:
    # Integrate d ln D / d ln a = Omega_m(a)^gamma from a=1 to each a,
    # normalized to D(a=1)=1. This is a standard approximation, not a Tau claim.
    out = np.empty_like(z)
    for idx, z_value in enumerate(z):
        a_target = 1.0 / (1.0 + z_value)
        grid = np.linspace(a_target, 1.0, 512)
        omega_gamma = omega_m_a(grid, omega_m) ** GAMMA
        integral = np.trapezoid(omega_gamma / grid, grid)
        out[idx] = math.exp(-integral)
    return out


def fsigma8_lcdm(z: np.ndarray, omega_m: float, sigma8_0: float) -> np.ndarray:
    a = 1.0 / (1.0 + z)
    growth = growth_factor_approx(z, omega_m)
    f_growth = omega_m_a(a, omega_m) ** GAMMA
    return f_growth * sigma8_0 * growth


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "GROWTH_WEB_SOURCE_NATIVE_PILOT_NOT_VALIDATION":
        raise SystemExit("growth web pilot status mismatch")
    forbidden = run["forbidden_inputs"]
    for marker in ["growth_residuals", "fit_improvement_driven_grid_changes", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"growth web pilot missing forbidden marker: {marker}")

    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    z = np.array([float(row["z_eff"]) for row in rows])
    fs8 = np.array([float(row["fsigma8"]) for row in rows])
    sigma = np.array([float(row["fsigma8_sigma"]) for row in rows])
    w_web = np.array([float(row["W_web_source_native_basis"]) for row in rows])

    omega_m_grid = parse_range(run["omega_m_grid"])
    sigma8_grid = parse_range(run["sigma8_0_grid"])
    mu_web_grid = parse_range(run["mu_web_grid"])
    rng = np.random.default_rng(int(run["random_seed"]))
    shuffled_web = w_web[rng.permutation(len(w_web))]

    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, sigma8_0: float, mu_web: float, active_web: np.ndarray) -> None:
        model = fsigma8_lcdm(z, omega_m, sigma8_0) * (1.0 + mu_web * active_web)
        chi2 = float(np.sum(((fs8 - model) / sigma) ** 2))
        k_eff = 2 if branch == "baseline_only" else 3
        aic = chi2 + 2 * k_eff
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "sigma8_0": f"{sigma8_0:.12g}",
                "mu_web": f"{mu_web:.12g}",
                "chi2": f"{chi2:.12g}",
                "aic": f"{aic:.12g}",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "growth_web_source_native_pilot_not_validation",
            }
        )

    zero = np.zeros_like(w_web)
    for omega_m in omega_m_grid:
        for sigma8_0 in sigma8_grid:
            add_row("baseline_only", omega_m, sigma8_0, 0.0, zero)
            for mu_web in mu_web_grid:
                add_row("web_growth_shell", omega_m, sigma8_0, mu_web, w_web)
                add_row("wrong_web_sign", omega_m, sigma8_0, mu_web, -w_web)
                add_row("deterministic_shuffled_web", omega_m, sigma8_0, mu_web, shuffled_web)

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
        "web_best_mu_web": web["mu_web"],
        "delta_chi2_web_minus_baseline": f"{float(web['chi2']) - float(base['chi2']):.12g}",
        "delta_aic_web_minus_baseline": f"{float(web['aic']) - float(base['aic']):.12g}",
        "wrong_web_sign_best_chi2": best["wrong_web_sign"]["chi2"],
        "shuffled_web_best_chi2": best["deterministic_shuffled_web"]["chi2"],
        "active_channels": run["active_channels"],
        "disabled_channels": run["disabled_channels"],
        "covariance_policy": run["covariance_policy"],
        "claim_boundary": "growth_web_source_native_pilot_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_GROWTH_WEB_SOURCE_NATIVE_PILOT_V1_COMPLETE "
        f"delta_chi2={summary['delta_chi2_web_minus_baseline']} "
        "claim_boundary=growth_web_source_native_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
