#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "pantheon_design_matrix_v1.csv"
MASK = ROOT / "data" / "derived" / "pantheon_scope_v1_row_mask.csv"
COV = ROOT / "data" / "raw" / "pantheon_plus" / "pantheon_plus_mu_covariance" / "Pantheon+SH0ES_STAT+SYS.cov"
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_pilot_scoring_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_pilot_scoring_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_pilot_scoring_v1_grid.csv"

C_LIGHT = 299792.458


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def parse_range(spec: str) -> list[float]:
    parts = [float(x) for x in spec.split(":")]
    if len(parts) == 3:
        start, stop, step = parts
        vals = []
        x = start
        while x <= stop + 1e-12:
            vals.append(round(x, 12))
            x += step
        return vals
    return parts


def load_design() -> tuple[list[str], np.ndarray, np.ndarray]:
    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    cids = [row["CID"] for row in rows]
    z = np.array([float(row["zHD"]) for row in rows], dtype=float)
    mu = np.array([float(row["MU_SH0ES"]) for row in rows], dtype=float)
    return cids, z, mu


def retained_indices() -> np.ndarray:
    with MASK.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return np.array([int(row["source_row_index"]) for row in rows if row["included"] == "true"], dtype=int)


def load_covariance(indices: np.ndarray) -> np.ndarray:
    with COV.open() as f:
        n = int(float(f.readline().strip()))
    flat = np.loadtxt(COV, skiprows=1)
    if flat.size != n * n:
        raise SystemExit(f"covariance size mismatch: got={flat.size} expected={n*n}")
    cov = flat.reshape((n, n))
    return cov[np.ix_(indices, indices)]


def e_of_z(z: np.ndarray, omega_m: float, omega_tau: float = 0.0, q: float = 2.0, a_tau: float = 0.7, mode: str = "baseline") -> np.ndarray:
    a = 1.0 / (1.0 + z)
    if mode == "baseline":
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m)
    else:
        w = a**q / (a**q + a_tau**q)
        w0 = 1.0 / (1.0 + a_tau**q)
        w_norm = w / w0
        if mode == "wrong_activation":
            w_norm = a**q
        elif mode == "shuffled_activation":
            permutation = np.random.default_rng(20260608 + len(w_norm)).permutation(len(w_norm))
            w_norm = w_norm[permutation]
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m - omega_tau) + omega_tau * w_norm
    if np.any(e2 <= 0):
        return np.full_like(z, np.nan)
    return np.sqrt(e2)


def distance_modulus(z: np.ndarray, omega_m: float, omega_tau: float = 0.0, q: float = 2.0, a_tau: float = 0.7, mode: str = "baseline") -> np.ndarray:
    order = np.argsort(z)
    zs = z[order]
    # Include z=0 anchor for cumulative trapezoid.
    grid = np.concatenate([[0.0], zs])
    mid_e = e_of_z(grid, omega_m, omega_tau, q, a_tau, mode)
    if np.any(~np.isfinite(mid_e)):
        return np.full_like(z, np.nan)
    inv_e = 1.0 / mid_e
    integ = np.zeros_like(grid)
    dz = np.diff(grid)
    integ[1:] = np.cumsum(0.5 * dz * (inv_e[:-1] + inv_e[1:]))
    d_l = (1.0 + zs) * C_LIGHT * integ[1:]
    mu_sorted = 5.0 * np.log10(np.maximum(d_l, 1e-300)) + 25.0
    out = np.empty_like(mu_sorted)
    out[order] = mu_sorted
    return out


def covariance_weights(cov: np.ndarray) -> tuple[np.ndarray, float]:
    variance = np.diag(cov).astype(float)
    if np.any(~np.isfinite(variance)):
        raise SystemExit("non-finite covariance diagonal")
    positive = variance[variance > 0]
    if positive.size == 0:
        raise SystemExit("covariance diagonal has no positive entries")
    floor = max(float(np.median(positive)) * 1e-8, 1e-12)
    clipped = np.maximum(variance, floor)
    return 1.0 / clipped, floor


def chi2_with_offset(y: np.ndarray, model: np.ndarray, weights: np.ndarray) -> tuple[float, float]:
    if np.any(~np.isfinite(model)):
        return math.inf, math.nan
    r0 = y - model
    offset = float(np.sum(weights * r0) / np.sum(weights))
    r = r0 - offset
    chi2 = float(np.sum(weights * r * r))
    return chi2, offset


def main() -> None:
    run = read_one(RUN_MANIFEST)
    if run["status"] != "PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("run status must be PILOT_SCORING_NOT_VALIDATION")
    cids, z, mu = load_design()
    cov = load_covariance(retained_indices())
    weights, cov_floor = covariance_weights(cov)

    baseline_om = parse_range(run["baseline_omega_m_grid"])
    tau_om = parse_range(run["tau_omega_m_grid"])
    tau_ot = parse_range(run["tau_omega_tau_grid"])
    tau_q = parse_range(run["tau_q_grid"])
    tau_at = parse_range(run["tau_a_tau_grid"])

    grid_rows: list[dict[str, str]] = []
    def add_row(branch: str, omega_m: float, omega_tau: float, q: float, a_tau: float, mode: str) -> None:
        model = distance_modulus(z, omega_m, omega_tau, q, a_tau, mode)
        chi2, offset = chi2_with_offset(mu, model, weights)
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
                "claim_boundary": "pilot_scoring_not_validation",
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
        "covariance_regularization": "diagonal_variance_floor_rtol_1e-8",
        "covariance_variance_floor": f"{cov_floor:.12g}",
        "claim_boundary": "pilot_scoring_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_PANTHEON_PILOT_SCORING_V1_COMPLETE "
        f"n={len(z)} delta_chi2_tau_minus_baseline={summary['delta_chi2_tau_minus_baseline']} "
        "claim_boundary=pilot_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
