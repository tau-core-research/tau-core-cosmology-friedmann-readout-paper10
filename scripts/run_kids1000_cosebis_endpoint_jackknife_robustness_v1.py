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
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv"
ENDPOINT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
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


def build_masks(theory_rows: list[dict[str, str]]) -> list[tuple[str, str, np.ndarray]]:
    bin1 = np.asarray([int(row["bin1"]) for row in theory_rows])
    bin2 = np.asarray([int(row["bin2"]) for row in theory_rows])
    mode = np.asarray([int(row["mode"]) for row in theory_rows])
    pair = np.asarray([row["pair_id"] for row in theory_rows])

    masks: list[tuple[str, str, np.ndarray]] = [
        ("full_reference", "full", np.ones(len(theory_rows), dtype=bool))
    ]
    for source_bin in range(1, 6):
        keep = (bin1 != source_bin) & (bin2 != source_bin)
        masks.append((f"leave_source_bin_{source_bin}", "leave_one_source_bin", keep))
    pairs = [f"{i}-{j}" for i in range(1, 6) for j in range(i, 6)]
    for pair_id in pairs:
        masks.append((f"leave_pair_{pair_id}", "leave_one_tomographic_pair", pair != pair_id))
    bands = [
        ("low_1_5", (mode >= 1) & (mode <= 5)),
        ("mid_6_10", (mode >= 6) & (mode <= 10)),
        ("high_11_20", (mode >= 11) & (mode <= 20)),
    ]
    for band_id, keep in bands:
        masks.append((f"mode_band_{band_id}", "mode_band", keep))
        masks.append((f"without_mode_band_{band_id}", "complement_mode_band", ~keep))
    return masks


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
    baseline_aic = baseline_chi2
    candidate_aic = candidate_chi2 + 2.0
    return amp, baseline_chi2, candidate_chi2, baseline_aic, candidate_aic, float(evals.min())


def main() -> None:
    policy = read_one(POLICY)
    endpoint = read_one(ENDPOINT)
    theory_rows = sorted(read_rows(THEORY), key=lambda row: int(row["row_index_zero_based"]))

    if policy["status"] != "ENDPOINT_JACKKNIFE_ROBUSTNESS_POLICY_FROZEN":
        raise SystemExit("unexpected jackknife policy status")
    if policy["parent_endpoint_scoring_run"] != endpoint["run_id"]:
        raise SystemExit("jackknife policy parent endpoint scoring run mismatch")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("jackknife policy must not claim validation")
    if policy["retunes_source_frozen_theory_vector"] != "false":
        raise SystemExit("jackknife policy must not retune the source-frozen theory vector")
    if any(row["uses_kids_data_vector_values"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not use KiDS data values")

    y, cov = load_kids_vector_and_covariance()
    candidate = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    rows: list[dict[str, str]] = []
    for subset_id, subset_family, keep in build_masks(theory_rows):
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

    leave_one_rows = [
        row for row in rows if row["subset_family"] in {"leave_one_source_bin", "leave_one_tomographic_pair"}
    ]
    negative_leave_one_chi2 = sum(row["candidate_improves_chi2"] == "true" for row in leave_one_rows)
    negative_leave_one_aic = sum(row["candidate_improves_aic"] == "true" for row in leave_one_rows)
    mode_rows = [row for row in rows if row["subset_family"] == "mode_band"]
    negative_mode_chi2 = sum(row["candidate_improves_chi2"] == "true" for row in mode_rows)
    negative_mode_aic = sum(row["candidate_improves_aic"] == "true" for row in mode_rows)
    full = next(row for row in rows if row["subset_id"] == "full_reference")
    worst = max(rows, key=lambda row: float(row["delta_chi2_vs_baseline"]))
    best = min(rows, key=lambda row: float(row["delta_chi2_vs_baseline"]))
    if negative_leave_one_chi2 == len(leave_one_rows):
        localization_verdict = "not_single_source_bin_or_pair_under_leave_one_chi2"
    else:
        localization_verdict = "localized_or_fragile_under_leave_one_chi2"
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "parent_run_id": endpoint["run_id"],
            "status": "KIDS1000_COSEBIS_ENDPOINT_JACKKNIFE_ROBUSTNESS_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "subset_count": str(len(rows)),
            "leave_one_subset_count": str(len(leave_one_rows)),
            "mode_band_subset_count": str(len(mode_rows)),
            "full_reference_delta_chi2_vs_baseline": full["delta_chi2_vs_baseline"],
            "full_reference_delta_aic_vs_baseline": full["delta_aic_vs_baseline"],
            "leave_one_subsets_with_negative_delta_chi2": str(negative_leave_one_chi2),
            "leave_one_subsets_with_negative_delta_aic": str(negative_leave_one_aic),
            "mode_band_subsets_with_negative_delta_chi2": str(negative_mode_chi2),
            "mode_band_subsets_with_negative_delta_aic": str(negative_mode_aic),
            "best_subset_id": best["subset_id"],
            "best_subset_delta_chi2_vs_baseline": best["delta_chi2_vs_baseline"],
            "worst_subset_id": worst["subset_id"],
            "worst_subset_delta_chi2_vs_baseline": worst["delta_chi2_vs_baseline"],
            "localization_verdict": localization_verdict,
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_JACKKNIFE_ROBUSTNESS_V1_COMPLETE "
        f"leave_one_negative_chi2={negative_leave_one_chi2}/{len(leave_one_rows)} "
        f"mode_band_negative_chi2={negative_mode_chi2}/{len(mode_rows)} "
        f"verdict={localization_verdict}"
    )


if __name__ == "__main__":
    main()
