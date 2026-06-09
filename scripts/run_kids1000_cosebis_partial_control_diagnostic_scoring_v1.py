#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import math
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv"
DESIGN_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_design_matrix_policy_v1.csv"
DESIGN_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1_summary.csv"
DESIGN = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv"

BRANCH_COLUMNS = [
    "baseline_zero",
    "mask_sample_0",
    "mask_sample_98",
    "mask_sample_195",
    "positive_mask_mean",
    "sign_flip_positive_mean",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_kids_vector_and_covariance() -> tuple[np.ndarray, np.ndarray]:
    if not TARBALL.exists():
        raise SystemExit(f"missing KiDS tarball: {TARBALL}")
    with tarfile.open(TARBALL) as tf:
        member = tf.extractfile(COSEBIS_MEMBER)
        if member is None:
            raise SystemExit("selected COSEBIs FITS member missing from KiDS tarball")
        payload = member.read()
    with fits.open(io.BytesIO(payload)) as hdul:
        data = hdul["En"].data
        cov = np.asarray(hdul["COVMAT"].data, dtype=float)
        y = np.asarray(data["VALUE"], dtype=float)
        if len(y) != 300 or cov.shape != (300, 300):
            raise SystemExit("unexpected KiDS COSEBIs data/covariance shape")
        row_order = [
            (int(data["BIN1"][i]), int(data["BIN2"][i]), int(data["ANGBIN"][i]))
            for i in range(len(y))
        ]
    expected_order = []
    for bin1 in range(1, 6):
        for bin2 in range(bin1, 6):
            for mode in range(1, 21):
                expected_order.append((bin1, bin2, mode))
    if row_order != expected_order:
        raise SystemExit("KiDS En row order does not match frozen COSEBIs design order")
    return y, cov


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


def chi2(y: np.ndarray, model: np.ndarray, factor: tuple[np.ndarray, bool]) -> float:
    r = y - model
    cinv_r = linalg.cho_solve(factor, r, check_finite=False)
    if not np.isfinite(cinv_r).all():
        return math.inf
    return stable_dot(r, cinv_r)


def best_nonnegative_amplitude(
    y: np.ndarray, x: np.ndarray, factor: tuple[np.ndarray, bool]
) -> tuple[float, float]:
    if np.allclose(x, 0.0):
        return 0.0, chi2(y, np.zeros_like(y), factor)
    cinv_x = linalg.cho_solve(factor, x, check_finite=False)
    cinv_y = linalg.cho_solve(factor, y, check_finite=False)
    denom = stable_dot(x, cinv_x)
    if denom <= 0 or not math.isfinite(denom):
        raise SystemExit("invalid amplitude denominator")
    raw = stable_dot(x, cinv_y) / denom
    amp = max(0.0, raw)
    return amp, chi2(y, amp * x, factor)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    design_policy = read_one(DESIGN_POLICY)
    design_summary = read_one(DESIGN_SUMMARY)
    design_rows = read_rows(DESIGN)
    if run["status"] != "PARTIAL_CONTROL_DIAGNOSTIC_SCORING_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected diagnostic scoring run status")
    if run["parent_design_matrix_policy"] != design_policy["policy_id"]:
        raise SystemExit("run parent design policy mismatch")
    if run["partial_control_scoring_allowed"] != "true":
        raise SystemExit("diagnostic scoring manifest must explicitly allow partial-control scoring")
    if run["endpoint_scoring_allowed"] != "false":
        raise SystemExit("diagnostic scoring must not enable endpoint scoring")
    if design_summary["contains_endpoint_theory_vector"] != "false":
        raise SystemExit("design matrix must not be an endpoint theory vector")
    if design_summary["contains_residuals"] != "false":
        raise SystemExit("design matrix must not contain residuals")
    if design_summary["branch_set"].split(";") != BRANCH_COLUMNS:
        raise SystemExit("branch order mismatch")

    y, cov = load_kids_vector_and_covariance()
    evals = np.linalg.eigvalsh(cov)
    min_eval = float(evals.min())
    max_eval = float(evals.max())
    if min_eval <= 0:
        raise SystemExit("KiDS covariance is not positive definite")
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)

    matrix = {branch: np.asarray([float(row[branch]) for row in design_rows]) for branch in BRANCH_COLUMNS}
    grid_rows: list[dict[str, str]] = []
    baseline_chi2 = None
    baseline_aic = None
    for branch in BRANCH_COLUMNS:
        amp, branch_chi2 = best_nonnegative_amplitude(y, matrix[branch], factor)
        k_eff = 0 if branch == "baseline_zero" else 1
        branch_aic = branch_chi2 + 2 * k_eff
        if branch == "baseline_zero":
            baseline_chi2 = branch_chi2
            baseline_aic = branch_aic
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "amplitude_policy": run["amplitude_policy"],
                "best_nonnegative_amplitude": f"{amp:.12g}",
                "chi2": f"{branch_chi2:.12g}",
                "aic": f"{branch_aic:.12g}",
                "k_eff": str(k_eff),
                "n_rows": str(len(y)),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": run["claim_boundary"],
            }
        )
    assert baseline_chi2 is not None and baseline_aic is not None
    for row in grid_rows:
        row["delta_chi2_vs_baseline"] = f"{float(row['chi2']) - baseline_chi2:.12g}"
        row["delta_aic_vs_baseline"] = f"{float(row['aic']) - baseline_aic:.12g}"

    ranked = sorted(grid_rows, key=lambda row: float(row["chi2"]))
    best = ranked[0]
    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(grid_rows)

    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "selected_statistic": run["selected_statistic"],
        "control_scope": run["control_scope"],
        "n_rows": str(len(y)),
        "branch_count": str(len(BRANCH_COLUMNS)),
        "baseline_chi2": f"{baseline_chi2:.12g}",
        "baseline_aic": f"{baseline_aic:.12g}",
        "best_branch": best["branch"],
        "best_branch_chi2": best["chi2"],
        "best_branch_aic": best["aic"],
        "best_branch_amplitude": best["best_nonnegative_amplitude"],
        "best_delta_chi2_vs_baseline": best["delta_chi2_vs_baseline"],
        "best_delta_aic_vs_baseline": best["delta_aic_vs_baseline"],
        "covariance_regularization": "none_positive_definite_cholesky",
        "covariance_min_eigenvalue": f"{min_eval:.12g}",
        "covariance_condition_number": f"{max_eval / min_eval:.12g}",
        "partial_control_scoring_executed": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "uses_kids_data_vector_values_for_scoring": "true",
        "uses_kids_data_vector_values_for_source_selection": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "claim_boundary": run["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DIAGNOSTIC_SCORING_V1_COMPLETE "
        f"best_branch={summary['best_branch']} "
        f"delta_chi2={summary['best_delta_chi2_vs_baseline']} "
        "endpoint_allowed=false claim_boundary=partial_control_diagnostic_scoring_not_endpoint_not_validation"
    )


if __name__ == "__main__":
    main()
