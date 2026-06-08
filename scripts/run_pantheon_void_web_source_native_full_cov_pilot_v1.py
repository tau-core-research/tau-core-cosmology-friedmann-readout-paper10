#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from run_pantheon_pilot_scoring_v1 import C_LIGHT, load_covariance, parse_range, read_one, retained_indices
    from run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import C_LIGHT, load_covariance, parse_range, read_one, retained_indices
    from scripts.run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_void_web_source_native_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_grid.csv"


def load_design_with_source_native_channels() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    z = np.array([float(row["zHD"]) for row in rows], dtype=float)
    mu = np.array([float(row["MU_SH0ES"]) for row in rows], dtype=float)
    w_void = np.array([float(row["W_void_source_native_basis"]) for row in rows], dtype=float)
    w_web = np.array([float(row["W_web_source_native_basis"]) for row in rows], dtype=float)
    return z, mu, w_void, w_web


def main() -> None:
    run = read_one(RUN_MANIFEST)
    if run["status"] != "VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("source-native void/web run status mismatch")
    if "W_PATH_PROJECTION" not in run["disabled_channels"] or "W_TIME_READOUT" not in run["disabled_channels"]:
        raise SystemExit("W_path and W_time must remain disabled in this pilot")
    forbidden = run["forbidden_inputs"]
    for marker in ["distance_residuals", "growth_residuals", "lensing_residuals", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"source-native void/web pilot missing forbidden marker: {marker}")

    z, mu, w_void, w_web = load_design_with_source_native_channels()
    cov = load_covariance(retained_indices())
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite inverse-ones vector")

    baseline_om = parse_range(run["baseline_omega_m_grid"])
    model_om = parse_range(run["source_native_omega_m_grid"])
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
                "claim_boundary": "void_web_source_native_full_cov_pilot_not_validation",
            }
        )

    for om in baseline_om:
        add_row("baseline_only", om, 0.0, 0.0, "baseline")

    for om in model_om:
        for ov in omega_void_grid:
            for ow in omega_web_grid:
                add_row("source_native_void_web_shell", om, ov, ow, "void_web")
                add_row("source_native_void_only", om, ov, 0.0, "void_only")
                add_row("source_native_web_only", om, 0.0, ow, "web_only")
                add_row("wrong_web_sign", om, ov, ow, "wrong_web_sign")
                add_row("deterministic_shuffled_source_native_void_web", om, ov, ow, "shuffled")

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
    matched = best["source_native_void_web_shell"]
    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "n_rows": str(len(z)),
        "baseline_best_chi2": base["chi2"],
        "baseline_best_aic": base["aic"],
        "source_native_void_web_best_chi2": matched["chi2"],
        "source_native_void_web_best_aic": matched["aic"],
        "source_native_void_web_best_omega_m": matched["omega_m"],
        "source_native_void_web_best_omega_void": matched["omega_void"],
        "source_native_void_web_best_omega_web": matched["omega_web"],
        "delta_chi2_source_native_void_web_minus_baseline": f"{float(matched['chi2']) - float(base['chi2']):.12g}",
        "delta_aic_source_native_void_web_minus_baseline": f"{float(matched['aic']) - float(base['aic']):.12g}",
        "source_native_void_only_best_chi2": best["source_native_void_only"]["chi2"],
        "source_native_web_only_best_chi2": best["source_native_web_only"]["chi2"],
        "wrong_web_sign_best_chi2": best["wrong_web_sign"]["chi2"],
        "shuffled_best_chi2": best["deterministic_shuffled_source_native_void_web"]["chi2"],
        "active_channels": run["active_channels"],
        "disabled_channels": run["disabled_channels"],
        "covariance_regularization": "none_positive_definite_cholesky",
        "covariance_min_eigenvalue": f"{min_eval:.12g}",
        "covariance_condition_number": f"{condition_number:.12g}",
        "claim_boundary": "void_web_source_native_full_cov_pilot_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_V1_COMPLETE "
        f"delta_chi2={summary['delta_chi2_source_native_void_web_minus_baseline']} "
        "claim_boundary=void_web_source_native_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
