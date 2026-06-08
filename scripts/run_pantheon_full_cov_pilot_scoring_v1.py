#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_pantheon_pilot_scoring_v1 import (
        distance_modulus,
        load_covariance,
        load_design,
        parse_range,
        read_one,
        retained_indices,
    )
except ImportError:
    from scripts.run_pantheon_pilot_scoring_v1 import (
        distance_modulus,
        load_covariance,
        load_design,
        parse_range,
        read_one,
        retained_indices,
    )


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_full_cov_pilot_scoring_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_grid.csv"


def covariance_factor(cov: np.ndarray) -> tuple[tuple[np.ndarray, bool], float, float]:
    evals = np.linalg.eigvalsh(cov)
    min_eval = float(evals.min())
    max_eval = float(evals.max())
    if min_eval <= 0 or not np.isfinite(min_eval) or not np.isfinite(max_eval):
        raise SystemExit("retained covariance is not positive definite")
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    return factor, min_eval, max_eval / min_eval


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


def chi2_with_offset(y: np.ndarray, model: np.ndarray, factor: tuple[np.ndarray, bool], cinv_ones: np.ndarray) -> tuple[float, float]:
    if np.any(~np.isfinite(model)):
        return math.inf, math.nan
    ones = np.ones_like(y)
    r0 = y - model
    cinv_r0 = linalg.cho_solve(factor, r0, check_finite=False)
    if not np.isfinite(cinv_r0).all():
        return math.inf, math.nan
    denom = stable_dot(ones, cinv_ones)
    if denom == 0 or not math.isfinite(denom):
        raise SystemExit("invalid full-cov intercept denominator")
    offset = stable_dot(ones, cinv_r0) / denom
    r = r0 - offset
    cinv_r = linalg.cho_solve(factor, r, check_finite=False)
    if not np.isfinite(cinv_r).all():
        return math.inf, math.nan
    chi2 = stable_dot(r, cinv_r)
    return chi2, offset


def main() -> None:
    run = read_one(RUN_MANIFEST)
    if run["status"] != "FULL_COV_PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("run status must be FULL_COV_PILOT_SCORING_NOT_VALIDATION")
    _, z, mu = load_design()
    cov = load_covariance(retained_indices())
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite full-cov inverse-ones vector")

    baseline_om = parse_range(run["baseline_omega_m_grid"])
    tau_om = parse_range(run["tau_omega_m_grid"])
    tau_ot = parse_range(run["tau_omega_tau_grid"])
    tau_q = parse_range(run["tau_q_grid"])
    tau_at = parse_range(run["tau_a_tau_grid"])

    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_tau: float, q: float, a_tau: float, mode: str) -> None:
        model = distance_modulus(z, omega_m, omega_tau, q, a_tau, mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        if branch == "baseline_only":
            k_eff = 2
        elif branch in {"tau_shell", "wrong_activation", "deterministic_shuffled_activation"}:
            k_eff = 5
        else:
            k_eff = 0
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_tau": f"{omega_tau:.12g}",
                "q": f"{q:.12g}",
                "a_tau": f"{a_tau:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "full_cov_pilot_scoring_not_validation",
            }
        )

    for om in baseline_om:
        add_row("baseline_only", om, 0.0, 2.0, 0.7, "baseline")

    for om in tau_om:
        for ot in tau_ot:
            for q in tau_q:
                for at in tau_at:
                    add_row("tau_shell", om, ot, q, at, "tau_shell")
                    add_row("wrong_activation", om, ot, q, at, "wrong_activation")
                    add_row("deterministic_shuffled_activation", om, ot, q, at, "shuffled_activation")

    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()))
        writer.writeheader()
        writer.writerows(grid_rows)

    finite_rows = [r for r in grid_rows if r["chi2"] != "inf"]
    by_branch: dict[str, list[dict[str, str]]] = {}
    for row in finite_rows:
        by_branch.setdefault(row["branch"], []).append(row)
    best = {branch: min(rows, key=lambda r: float(r["chi2"])) for branch, rows in by_branch.items()}
    base = best["baseline_only"]
    tau = best["tau_shell"]
    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "n_rows": str(len(z)),
        "baseline_best_chi2": base["chi2"],
        "baseline_best_aic": base["aic"],
        "baseline_best_omega_m": base["omega_m"],
        "tau_best_chi2": tau["chi2"],
        "tau_best_aic": tau["aic"],
        "tau_best_omega_m": tau["omega_m"],
        "tau_best_omega_tau": tau["omega_tau"],
        "tau_best_q": tau["q"],
        "tau_best_a_tau": tau["a_tau"],
        "delta_chi2_tau_minus_baseline": f"{float(tau['chi2']) - float(base['chi2']):.12g}",
        "delta_aic_tau_minus_baseline": f"{float(tau['aic']) - float(base['aic']):.12g}",
        "wrong_best_chi2": best["wrong_activation"]["chi2"],
        "shuffled_best_chi2": best["deterministic_shuffled_activation"]["chi2"],
        "covariance_regularization": "none_positive_definite_cholesky",
        "covariance_min_eigenvalue": f"{min_eval:.12g}",
        "covariance_condition_number": f"{condition_number:.12g}",
        "claim_boundary": "full_cov_pilot_scoring_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_PANTHEON_FULL_COV_PILOT_SCORING_V1_COMPLETE "
        f"n={len(z)} delta_chi2_tau_minus_baseline={summary['delta_chi2_tau_minus_baseline']} "
        "claim_boundary=full_cov_pilot_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
