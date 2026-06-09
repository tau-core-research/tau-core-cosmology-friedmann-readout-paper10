#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import itertools
import math
import random
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_structure_robustness_policy_v1.csv"
ENDPOINT_RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
CONTROLS = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_controls.csv"
FAMILY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_family_summary.csv"
TOP = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_top_controls.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_structure_robustness_v1_summary.csv"


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
    return stable_dot(residual, cinv_residual)


def best_nonnegative_amplitude(y: np.ndarray, x: np.ndarray, factor: tuple[np.ndarray, bool]) -> tuple[float, float]:
    if np.allclose(x, 0.0):
        return 0.0, chi2(y, np.zeros_like(y), factor)
    cinv_x = linalg.cho_solve(factor, x, check_finite=False)
    cinv_y = linalg.cho_solve(factor, y, check_finite=False)
    denom = stable_dot(x, cinv_x)
    if denom <= 0 or not math.isfinite(denom):
        raise SystemExit("invalid amplitude denominator")
    amp = max(0.0, stable_dot(x, cinv_y) / denom)
    return amp, chi2(y, amp * x, factor)


def pair_id(bin1: int, bin2: int) -> str:
    lo, hi = sorted((bin1, bin2))
    return f"{lo}-{hi}"


def build_vector(theory_rows: list[dict[str, str]], pair_map: dict[str, str]) -> np.ndarray:
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): float(row["theory_value"]) for row in theory_rows
    }
    return np.asarray(
        [by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
        dtype=float,
    )


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    endpoint = read_one(ENDPOINT_RESULTS)
    theory_rows = sorted(read_rows(THEORY), key=lambda row: int(row["row_index_zero_based"]))
    if policy["parent_endpoint_scoring_run"] != endpoint["run_id"]:
        raise SystemExit("robustness policy parent endpoint run mismatch")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("robustness policy must not claim validation")
    if any(row["uses_kids_data_vector_values"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not use KiDS data values")

    y, cov = load_kids_vector_and_covariance()
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    baseline_chi2 = float(endpoint["baseline_chi2"])
    candidate_delta = float(endpoint["candidate_delta_chi2_vs_baseline"])
    candidate_aic_delta = float(endpoint["candidate_delta_aic_vs_baseline"])
    pairs = [f"{i}-{j}" for i in range(1, 6) for j in range(i, 6)]
    autos = [f"{i}-{i}" for i in range(1, 6)]
    crosses = [pair for pair in pairs if pair not in autos]

    controls_meta: list[dict[str, object]] = []
    identity = {pair: pair for pair in pairs}
    for perm in itertools.permutations([1, 2, 3, 4, 5]):
        if tuple(perm) == (1, 2, 3, 4, 5):
            continue
        bin_map = {str(i + 1): str(perm[i]) for i in range(5)}
        mapping = {pair: pair_id(int(bin_map[pair.split("-")[0]]), int(bin_map[pair.split("-")[1]])) for pair in pairs}
        controls_meta.append(
            {
                "control_family": "bin_label_permutation",
                "operator": "bin_perm_" + "".join(str(x) for x in perm),
                "seed": "0",
                "mapping": mapping,
            }
        )

    rng_seed = 702001
    for draw in range(1000):
        rng = random.Random(rng_seed + draw)
        auto_target = autos[:]
        cross_target = crosses[:]
        rng.shuffle(auto_target)
        rng.shuffle(cross_target)
        mapping = dict(identity)
        mapping.update(dict(zip(autos, auto_target)))
        mapping.update(dict(zip(crosses, cross_target)))
        controls_meta.append(
            {
                "control_family": "auto_cross_preserving_shuffle",
                "operator": f"seeded_auto_cross_shuffle_{rng_seed + draw}",
                "seed": str(rng_seed),
                "mapping": mapping,
            }
        )

    control_rows: list[dict[str, str]] = []
    for index, meta in enumerate(controls_meta, start=1):
        vector = build_vector(theory_rows, meta["mapping"])  # type: ignore[arg-type]
        amp, score = best_nonnegative_amplitude(y, vector, factor)
        aic = score + 2.0
        delta = score - baseline_chi2
        delta_aic = aic - baseline_chi2
        control_rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": endpoint["run_id"],
                "control_index_one_based": str(index),
                "control_family": str(meta["control_family"]),
                "operator": str(meta["operator"]),
                "seed": str(meta["seed"]),
                "mapping_signature": ";".join(f"{pair}->{meta['mapping'][pair]}" for pair in pairs),  # type: ignore[index]
                "amplitude": fmt(amp),
                "chi2": fmt(score),
                "aic": fmt(aic),
                "delta_chi2_vs_baseline": fmt(delta),
                "delta_aic_vs_baseline": fmt(delta_aic),
                "beats_candidate_chi2": str(delta < candidate_delta).lower(),
                "beats_candidate_aic": str(delta_aic < candidate_aic_delta).lower(),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    family_rows: list[dict[str, str]] = []
    for family in sorted({row["control_family"] for row in control_rows}):
        rows = [row for row in control_rows if row["control_family"] == family]
        deltas = [float(row["delta_chi2_vs_baseline"]) for row in rows]
        aic_deltas = [float(row["delta_aic_vs_baseline"]) for row in rows]
        family_rows.append(
            {
                "policy_id": policy["policy_id"],
                "run_id": endpoint["run_id"],
                "control_family": family,
                "control_count": str(len(rows)),
                "min_delta_chi2_vs_baseline": fmt(min(deltas)),
                "median_delta_chi2_vs_baseline": fmt(float(np.median(deltas))),
                "mean_delta_chi2_vs_baseline": fmt(float(np.mean(deltas))),
                "min_delta_aic_vs_baseline": fmt(min(aic_deltas)),
                "median_delta_aic_vs_baseline": fmt(float(np.median(aic_deltas))),
                "candidate_delta_chi2_vs_baseline": fmt(candidate_delta),
                "candidate_delta_aic_vs_baseline": fmt(candidate_aic_delta),
                "controls_better_than_candidate_chi2": str(sum(value < candidate_delta for value in deltas)),
                "controls_better_than_candidate_aic": str(sum(value < candidate_aic_delta for value in aic_deltas)),
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    better_chi2 = sum(row["beats_candidate_chi2"] == "true" for row in control_rows)
    better_aic = sum(row["beats_candidate_aic"] == "true" for row in control_rows)
    tail_chi2 = (better_chi2 + 1.0) / (len(control_rows) + 1.0)
    tail_aic = (better_aic + 1.0) / (len(control_rows) + 1.0)
    top_rows = sorted(control_rows, key=lambda row: float(row["chi2"]))[:25]
    summary_rows = [
        {
            "policy_id": policy["policy_id"],
            "run_id": endpoint["run_id"],
            "status": "KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_COMPLETE",
            "selected_statistic": policy["selected_statistic"],
            "control_count": str(len(control_rows)),
            "candidate_delta_chi2_vs_baseline": fmt(candidate_delta),
            "candidate_delta_aic_vs_baseline": fmt(candidate_aic_delta),
            "controls_better_than_candidate_chi2": str(better_chi2),
            "controls_better_than_candidate_aic": str(better_aic),
            "candidate_rank_by_chi2": str(1 + better_chi2),
            "candidate_rank_by_aic": str(1 + better_aic),
            "plus_one_tail_fraction_chi2": fmt(tail_chi2),
            "plus_one_tail_fraction_aic": fmt(tail_aic),
            "families_with_better_than_candidate": ";".join(
                row["control_family"] for row in family_rows if int(row["controls_better_than_candidate_chi2"]) > 0
            )
            or "none",
            "top_control_family": top_rows[0]["control_family"],
            "top_control_operator": top_rows[0]["operator"],
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(CONTROLS, control_rows)
    write_csv(FAMILY_SUMMARY, family_rows)
    write_csv(TOP, top_rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_STRUCTURE_ROBUSTNESS_V1_COMPLETE "
        f"rank_chi2={summary_rows[0]['candidate_rank_by_chi2']}/{len(control_rows) + 1} "
        f"tail_chi2={summary_rows[0]['plus_one_tail_fraction_chi2']} "
        f"families_with_better={summary_rows[0]['families_with_better_than_candidate']}"
    )


if __name__ == "__main__":
    main()
