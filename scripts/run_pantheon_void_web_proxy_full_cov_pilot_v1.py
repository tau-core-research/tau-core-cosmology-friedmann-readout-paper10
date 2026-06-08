#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_pantheon_full_cov_pilot_scoring_v1 import (
        chi2_with_offset,
        covariance_factor,
        stable_dot,
    )
    from run_pantheon_pilot_scoring_v1 import (
        C_LIGHT,
        load_covariance,
        parse_range,
        read_one,
        retained_indices,
    )
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import (
        chi2_with_offset,
        covariance_factor,
        stable_dot,
    )
    from scripts.run_pantheon_pilot_scoring_v1 import (
        C_LIGHT,
        load_covariance,
        parse_range,
        read_one,
        retained_indices,
    )


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "pantheon_design_matrix_v1.csv"
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_void_web_proxy_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv"


def load_design_with_channels() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    z = np.array([float(row["zHD"]) for row in rows], dtype=float)
    mu = np.array([float(row["MU_SH0ES"]) for row in rows], dtype=float)
    w_void = np.array([float(row["W_void_proxy_basis"]) for row in rows], dtype=float)
    w_web = np.array([float(row["W_web_proxy_basis"]) for row in rows], dtype=float)
    return z, mu, w_void, w_web


def e_of_z_void_web(
    z: np.ndarray,
    omega_m: float,
    omega_void: float,
    omega_web: float,
    w_void: np.ndarray,
    w_web: np.ndarray,
    mode: str,
) -> np.ndarray:
    if mode == "baseline":
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m)
    else:
        if mode == "void_only":
            active_void = w_void
            active_web = np.zeros_like(w_web)
        elif mode == "web_only":
            active_void = np.zeros_like(w_void)
            active_web = w_web
        elif mode == "wrong_web_sign":
            active_void = w_void
            active_web = -w_web
        elif mode == "shuffled":
            rng = np.random.default_rng(20260608 + len(z))
            active_void = w_void[rng.permutation(len(w_void))]
            active_web = w_web[rng.permutation(len(w_web))]
        else:
            active_void = w_void
            active_web = w_web
        e2 = (
            omega_m * (1.0 + z) ** 3
            + (1.0 - omega_m - omega_void - omega_web)
            + omega_void * active_void
            + omega_web * active_web
        )
    if np.any(e2 <= 0):
        return np.full_like(z, np.nan)
    return np.sqrt(e2)


def distance_modulus_void_web(
    z: np.ndarray,
    omega_m: float,
    omega_void: float,
    omega_web: float,
    w_void: np.ndarray,
    w_web: np.ndarray,
    mode: str,
) -> np.ndarray:
    order = np.argsort(z)
    zs = z[order]
    void_sorted = w_void[order]
    web_sorted = w_web[order]

    grid = np.concatenate([[0.0], zs])
    # Hold the first source-only activation value at the z=0 anchor. This is a
    # numerical integration convention for the pilot, not a cosmological claim.
    void_grid = np.concatenate([[void_sorted[0]], void_sorted])
    web_grid = np.concatenate([[web_sorted[0]], web_sorted])
    e = e_of_z_void_web(grid, omega_m, omega_void, omega_web, void_grid, web_grid, mode)
    if np.any(~np.isfinite(e)):
        return np.full_like(z, np.nan)
    inv_e = 1.0 / e
    integ = np.zeros_like(grid)
    dz = np.diff(grid)
    integ[1:] = np.cumsum(0.5 * dz * (inv_e[:-1] + inv_e[1:]))
    d_l = (1.0 + zs) * C_LIGHT * integ[1:]
    mu_sorted = 5.0 * np.log10(np.maximum(d_l, 1e-300)) + 25.0
    out = np.empty_like(mu_sorted)
    out[order] = mu_sorted
    return out


def main() -> None:
    run = read_one(RUN_MANIFEST)
    if run["status"] != "VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("void/web proxy run status mismatch")
    if "W_PATH_PROJECTION" not in run["disabled_channels"] or "W_TIME_READOUT" not in run["disabled_channels"]:
        raise SystemExit("W_path and W_time must remain disabled in this pilot")
    forbidden = run["forbidden_inputs"]
    for marker in ["distance_residuals", "growth_residuals", "lensing_residuals", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"void/web proxy pilot missing forbidden marker: {marker}")

    z, mu, w_void, w_web = load_design_with_channels()
    cov = load_covariance(retained_indices())
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite inverse-ones vector")

    baseline_om = parse_range(run["baseline_omega_m_grid"])
    model_om = parse_range(run["void_web_omega_m_grid"])
    omega_void_grid = parse_range(run["omega_void_grid"])
    omega_web_grid = parse_range(run["omega_web_grid"])

    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_void: float, omega_web: float, mode: str) -> None:
        model = distance_modulus_void_web(z, omega_m, omega_void, omega_web, w_void, w_web, mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        k_eff = 2 if branch == "baseline_only" else 4
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_void": f"{omega_void:.12g}",
                "omega_web": f"{omega_web:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic": f"{aic:.12g}" if math.isfinite(chi2) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "void_web_proxy_full_cov_pilot_not_validation",
            }
        )

    for om in baseline_om:
        add_row("baseline_only", om, 0.0, 0.0, "baseline")

    for om in model_om:
        for ov in omega_void_grid:
            for ow in omega_web_grid:
                add_row("void_web_proxy_shell", om, ov, ow, "void_web")
                add_row("void_only", om, ov, 0.0, "void_only")
                add_row("web_only", om, 0.0, ow, "web_only")
                add_row("wrong_web_sign", om, ov, ow, "wrong_web_sign")
                add_row("deterministic_shuffled_void_web", om, ov, ow, "shuffled")

    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(grid_rows)

    finite_rows = [row for row in grid_rows if row["chi2"] != "inf"]
    by_branch: dict[str, list[dict[str, str]]] = {}
    for row in finite_rows:
        by_branch.setdefault(row["branch"], []).append(row)
    best = {branch: min(rows, key=lambda row: float(row["chi2"])) for branch, rows in by_branch.items()}
    base = best["baseline_only"]
    matched = best["void_web_proxy_shell"]
    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "n_rows": str(len(z)),
        "baseline_best_chi2": base["chi2"],
        "baseline_best_aic": base["aic"],
        "void_web_best_chi2": matched["chi2"],
        "void_web_best_aic": matched["aic"],
        "void_web_best_omega_m": matched["omega_m"],
        "void_web_best_omega_void": matched["omega_void"],
        "void_web_best_omega_web": matched["omega_web"],
        "delta_chi2_void_web_minus_baseline": f"{float(matched['chi2']) - float(base['chi2']):.12g}",
        "delta_aic_void_web_minus_baseline": f"{float(matched['aic']) - float(base['aic']):.12g}",
        "void_only_best_chi2": best["void_only"]["chi2"],
        "web_only_best_chi2": best["web_only"]["chi2"],
        "wrong_web_sign_best_chi2": best["wrong_web_sign"]["chi2"],
        "shuffled_best_chi2": best["deterministic_shuffled_void_web"]["chi2"],
        "active_channels": run["active_channels"],
        "disabled_channels": run["disabled_channels"],
        "covariance_regularization": "none_positive_definite_cholesky",
        "covariance_min_eigenvalue": f"{min_eval:.12g}",
        "covariance_condition_number": f"{condition_number:.12g}",
        "claim_boundary": "void_web_proxy_full_cov_pilot_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_VOID_WEB_PROXY_FULL_COV_PILOT_V1_COMPLETE "
        f"delta_chi2={summary['delta_chi2_void_web_minus_baseline']} "
        "claim_boundary=void_web_proxy_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
