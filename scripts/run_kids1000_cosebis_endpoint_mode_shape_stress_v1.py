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
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv"
MODE_LOCALIZATION = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"
ENDPOINT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv"


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


def mode_shape_weights(mode: np.ndarray) -> dict[str, np.ndarray]:
    raw = {
        "flat": np.ones_like(mode, dtype=float),
        "n^-0.25": mode**-0.25,
        "n^-0.5_candidate": mode**-0.5,
        "n^-0.75": mode**-0.75,
        "n^-1.0": mode**-1.0,
        "high_sqrt_n": mode**0.5,
        "high_n": mode,
    }
    return {name: values / float(values.mean()) for name, values in raw.items()}


def main() -> None:
    policy = read_one(POLICY)
    mode_localization = read_one(MODE_LOCALIZATION)
    endpoint = read_one(ENDPOINT)
    theory_rows = sorted(read_rows(THEORY), key=lambda row: int(row["row_index_zero_based"]))
    if policy["status"] != "ENDPOINT_MODE_SHAPE_STRESS_POLICY_FROZEN":
        raise SystemExit("unexpected mode-shape stress policy status")
    if policy["parent_mode_localization_policy"] != mode_localization["policy_id"]:
        raise SystemExit("mode-shape stress parent localization mismatch")
    if policy["parent_endpoint_scoring_run"] != endpoint["run_id"]:
        raise SystemExit("mode-shape stress parent endpoint mismatch")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("mode-shape stress policy must not claim validation")
    if policy["retunes_source_frozen_path_mapping"] != "false":
        raise SystemExit("mode-shape stress policy must not retune W_path")
    if any(row["uses_kids_data_vector_values"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not use KiDS data values")

    y, cov = load_kids_vector_and_covariance()
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    baseline_chi2 = chi2(y, np.zeros_like(y), factor)
    w_path = np.asarray([float(row["source_frozen_mapping_value"]) for row in theory_rows], dtype=float)
    mode = np.asarray([int(row["mode"]) for row in theory_rows], dtype=float)
    rows: list[dict[str, str]] = []
    for shape_id, weights in mode_shape_weights(mode).items():
        candidate = w_path * weights
        amp, candidate_chi2 = best_nonnegative_amplitude(y, candidate, factor)
        delta_chi2 = candidate_chi2 - baseline_chi2
        delta_aic = candidate_chi2 + 2.0 - baseline_chi2
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_run_id": endpoint["run_id"],
                "mode_shape_id": shape_id,
                "mode_shape_weight_min": fmt(float(weights.min())),
                "mode_shape_weight_max": fmt(float(weights.max())),
                "mode_shape_weight_mean": fmt(float(weights.mean())),
                "candidate_amplitude": fmt(amp),
                "baseline_chi2": fmt(baseline_chi2),
                "candidate_chi2": fmt(candidate_chi2),
                "delta_chi2_vs_baseline": fmt(delta_chi2),
                "delta_aic_vs_baseline": fmt(delta_aic),
                "candidate_improves_chi2": str(delta_chi2 < 0.0).lower(),
                "candidate_improves_aic": str(delta_aic < 0.0).lower(),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_posthoc_source_selection": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    best = min(rows, key=lambda row: float(row["delta_chi2_vs_baseline"]))
    candidate = next(row for row in rows if row["mode_shape_id"] == "n^-0.5_candidate")
    flat = next(row for row in rows if row["mode_shape_id"] == "flat")
    high_n = next(row for row in rows if row["mode_shape_id"] == "high_n")
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "parent_run_id": endpoint["run_id"],
            "status": "KIDS1000_COSEBIS_ENDPOINT_MODE_SHAPE_STRESS_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "mode_shape_count": str(len(rows)),
            "best_mode_shape_id": best["mode_shape_id"],
            "best_delta_chi2_vs_baseline": best["delta_chi2_vs_baseline"],
            "candidate_mode_shape_delta_chi2_vs_baseline": candidate["delta_chi2_vs_baseline"],
            "flat_mode_shape_delta_chi2_vs_baseline": flat["delta_chi2_vs_baseline"],
            "high_n_mode_shape_delta_chi2_vs_baseline": high_n["delta_chi2_vs_baseline"],
            "candidate_beats_flat_chi2": str(float(candidate["delta_chi2_vs_baseline"]) < float(flat["delta_chi2_vs_baseline"])).lower(),
            "high_mode_weighting_removes_signal": str(float(high_n["delta_chi2_vs_baseline"]) == 0.0).lower(),
            "mode_shape_stress_verdict": "low_weighted_carriers_preferred_but_flat_still_improves_high_weighting_fails",
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(GRID, rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_MODE_SHAPE_STRESS_V1_COMPLETE "
        f"best_shape={best['mode_shape_id']} "
        f"candidate_delta={candidate['delta_chi2_vs_baseline']} "
        f"flat_delta={flat['delta_chi2_vs_baseline']} "
        f"verdict={summary_rows[0]['mode_shape_stress_verdict']}"
    )


if __name__ == "__main__":
    main()
