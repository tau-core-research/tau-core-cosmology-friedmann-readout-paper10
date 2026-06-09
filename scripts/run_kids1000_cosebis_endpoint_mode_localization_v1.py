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
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_mode_localization_policy_v1.csv"
JACKKNIFE = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv"
ENDPOINT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"


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
        row_order = [
            (int(data["BIN1"][i]), int(data["BIN2"][i]), int(data["ANGBIN"][i]))
            for i in range(len(y))
        ]
    expected_order = [
        (bin1, bin2, mode)
        for bin1 in range(1, 6)
        for bin2 in range(bin1, 6)
        for mode in range(1, 21)
    ]
    if len(y) != 300 or cov.shape != (300, 300):
        raise SystemExit("unexpected KiDS COSEBIs data/covariance shape")
    if row_order != expected_order:
        raise SystemExit("KiDS En row order does not match frozen row order")
    return y, cov


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


def chi2(y: np.ndarray, model: np.ndarray, factor: tuple[np.ndarray, bool]) -> float:
    residual = y - model
    cinv_residual = linalg.cho_solve(factor, residual, check_finite=False)
    if not np.isfinite(cinv_residual).all():
        return math.inf
    return stable_dot(residual, cinv_residual)


def best_nonnegative_amplitude(
    y: np.ndarray, x: np.ndarray, factor: tuple[np.ndarray, bool]
) -> tuple[float, float]:
    if np.allclose(x, 0.0):
        return 0.0, chi2(y, np.zeros_like(y), factor)
    cinv_x = linalg.cho_solve(factor, x, check_finite=False)
    cinv_y = linalg.cho_solve(factor, y, check_finite=False)
    denom = stable_dot(x, cinv_x)
    if denom <= 0.0 or not math.isfinite(denom):
        raise SystemExit("invalid amplitude denominator")
    amp = max(0.0, stable_dot(x, cinv_y) / denom)
    return amp, chi2(y, amp * x, factor)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def build_subsets(mode: np.ndarray) -> list[tuple[str, str, np.ndarray]]:
    subsets: list[tuple[str, str, np.ndarray]] = []
    for n in range(1, 21):
        subsets.append((f"single_mode_{n}", "single_mode", mode == n))
    for n in range(1, 21):
        subsets.append((f"cumulative_low_modes_1_to_{n}", "cumulative_low_modes", mode <= n))
    for n in range(1, 20):
        subsets.append((f"without_low_modes_1_to_{n}", "without_low_modes", mode > n))
    return subsets


def score_subset(
    y: np.ndarray, cov: np.ndarray, candidate: np.ndarray, keep: np.ndarray
) -> tuple[float, float, float, float, float, float]:
    idx = np.flatnonzero(keep)
    y_sub = y[idx]
    x_sub = candidate[idx]
    cov_sub = cov[np.ix_(idx, idx)]
    evals = np.linalg.eigvalsh(cov_sub)
    if float(evals.min()) <= 0.0:
        raise SystemExit("subset covariance is not positive definite")
    factor = linalg.cho_factor(cov_sub, lower=True, check_finite=True)
    baseline_chi2 = chi2(y_sub, np.zeros_like(y_sub), factor)
    amp, candidate_chi2 = best_nonnegative_amplitude(y_sub, x_sub, factor)
    return amp, baseline_chi2, candidate_chi2, baseline_chi2, candidate_chi2 + 2.0, float(evals.min())


def main() -> None:
    policy = read_one(POLICY)
    jackknife = read_one(JACKKNIFE)
    endpoint = read_one(ENDPOINT)
    theory_rows = sorted(read_rows(THEORY), key=lambda row: int(row["row_index_zero_based"]))
    if policy["status"] != "ENDPOINT_MODE_LOCALIZATION_POLICY_FROZEN":
        raise SystemExit("unexpected mode-localization policy status")
    if policy["parent_jackknife_policy"] != jackknife["policy_id"]:
        raise SystemExit("mode-localization policy parent jackknife mismatch")
    if policy["parent_endpoint_scoring_run"] != endpoint["run_id"]:
        raise SystemExit("mode-localization policy parent endpoint mismatch")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("mode-localization policy must not claim validation")
    if policy["retunes_source_frozen_theory_vector"] != "false":
        raise SystemExit("mode-localization policy must not retune source vector")
    if any(row["uses_kids_data_vector_values"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not use KiDS data values")

    y, cov = load_kids_vector_and_covariance()
    candidate = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    mode = np.asarray([int(row["mode"]) for row in theory_rows])
    rows: list[dict[str, str]] = []
    for subset_id, subset_family, keep in build_subsets(mode):
        amp, baseline_chi2, candidate_chi2, baseline_aic, candidate_aic, min_eval = score_subset(
            y, cov, candidate, keep
        )
        delta_chi2 = candidate_chi2 - baseline_chi2
        delta_aic = candidate_aic - baseline_aic
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_run_id": endpoint["run_id"],
                "subset_id": subset_id,
                "subset_family": subset_family,
                "n_rows": str(int(keep.sum())),
                "candidate_amplitude": fmt(amp),
                "baseline_chi2": fmt(baseline_chi2),
                "candidate_chi2": fmt(candidate_chi2),
                "baseline_aic": fmt(baseline_aic),
                "candidate_aic": fmt(candidate_aic),
                "delta_chi2_vs_baseline": fmt(delta_chi2),
                "delta_aic_vs_baseline": fmt(delta_aic),
                "candidate_improves_chi2": str(delta_chi2 < 0.0).lower(),
                "candidate_improves_aic": str(delta_aic < 0.0).lower(),
                "subset_covariance_min_eigenvalue": fmt(min_eval),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_posthoc_source_selection": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    single = [row for row in rows if row["subset_family"] == "single_mode"]
    cumulative = [row for row in rows if row["subset_family"] == "cumulative_low_modes"]
    without = [row for row in rows if row["subset_family"] == "without_low_modes"]
    best_single = min(single, key=lambda row: float(row["delta_chi2_vs_baseline"]))
    best_cumulative = min(cumulative, key=lambda row: float(row["delta_chi2_vs_baseline"]))
    first_without_non_improving = next(
        (row for row in without if row["candidate_improves_chi2"] == "false"),
        {"subset_id": "none", "delta_chi2_vs_baseline": "nan"},
    )
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "parent_run_id": endpoint["run_id"],
            "status": "KIDS1000_COSEBIS_ENDPOINT_MODE_LOCALIZATION_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "subset_count": str(len(rows)),
            "single_mode_subset_count": str(len(single)),
            "cumulative_low_subset_count": str(len(cumulative)),
            "without_low_subset_count": str(len(without)),
            "single_modes_with_negative_delta_chi2": str(sum(row["candidate_improves_chi2"] == "true" for row in single)),
            "single_modes_with_negative_delta_aic": str(sum(row["candidate_improves_aic"] == "true" for row in single)),
            "cumulative_low_subsets_with_negative_delta_chi2": str(sum(row["candidate_improves_chi2"] == "true" for row in cumulative)),
            "without_low_subsets_with_negative_delta_chi2": str(sum(row["candidate_improves_chi2"] == "true" for row in without)),
            "best_single_mode_subset_id": best_single["subset_id"],
            "best_single_mode_delta_chi2_vs_baseline": best_single["delta_chi2_vs_baseline"],
            "best_cumulative_low_subset_id": best_cumulative["subset_id"],
            "best_cumulative_low_delta_chi2_vs_baseline": best_cumulative["delta_chi2_vs_baseline"],
            "first_without_low_non_improving_subset_id": first_without_non_improving["subset_id"],
            "first_without_low_non_improving_delta_chi2_vs_baseline": first_without_non_improving["delta_chi2_vs_baseline"],
            "mode_localization_verdict": "low_modes_1_to_5_dominate_endpoint_signal",
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_MODE_LOCALIZATION_V1_COMPLETE "
        f"best_single={best_single['subset_id']} "
        f"best_cumulative={best_cumulative['subset_id']} "
        f"first_without_low_non_improving={first_without_non_improving['subset_id']}"
    )


if __name__ == "__main__":
    main()
