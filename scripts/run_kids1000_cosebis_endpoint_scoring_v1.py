#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import math
import random
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_run_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_protocol_v1.csv"
READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"
GEOMETRY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
REPLAY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)

RESULTS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_results.csv"
RESIDUALS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_residuals.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_grid.csv"
NULL_CONTROLS = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_null_controls.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


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
        raise SystemExit("KiDS En row order does not match frozen COSEBIs row order")
    return y, cov


def chi2(y: np.ndarray, model: np.ndarray, factor: tuple[np.ndarray, bool]) -> float:
    residual = y - model
    cinv_residual = linalg.cho_solve(factor, residual, check_finite=False)
    if not np.isfinite(cinv_residual).all():
        return math.inf
    return stable_dot(residual, cinv_residual)


def best_nonnegative_amplitude(
    y: np.ndarray, x: np.ndarray, factor: tuple[np.ndarray, bool]
) -> tuple[float, float, np.ndarray]:
    if np.allclose(x, 0.0):
        model = np.zeros_like(y)
        return 0.0, chi2(y, model, factor), model
    cinv_x = linalg.cho_solve(factor, x, check_finite=False)
    cinv_y = linalg.cho_solve(factor, y, check_finite=False)
    denom = stable_dot(x, cinv_x)
    if denom <= 0.0 or not math.isfinite(denom):
        raise SystemExit("invalid amplitude denominator")
    raw_amp = stable_dot(x, cinv_y) / denom
    amp = max(0.0, raw_amp)
    model = amp * x
    return amp, chi2(y, model, factor), model


def build_control_vectors(
    theory_rows: list[dict[str, str]], replay_rows: list[dict[str, str]]
) -> list[dict[str, object]]:
    theory_rows = sorted(theory_rows, key=lambda row: int(row["row_index_zero_based"]))
    base = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    pair_order: list[str] = []
    for row in theory_rows:
        if row["pair_id"] not in pair_order:
            pair_order.append(row["pair_id"])
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): float(row["theory_value"]) for row in theory_rows
    }
    vectors: list[dict[str, object]] = []
    for replay in replay_rows:
        family = replay["control_family"]
        draw = int(replay["control_draw_index_zero_based"])
        seed = int(replay["seed"])
        if family == "sky_rotation":
            shift = (draw + 1) % len(pair_order)
            rotated = pair_order[shift:] + pair_order[:shift]
            pair_map = dict(zip(pair_order, rotated))
            values = np.asarray(
                [by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
                dtype=float,
            )
        elif family == "tomographic_pair_shuffle":
            rng = random.Random(seed + draw)
            shuffled = pair_order[:]
            rng.shuffle(shuffled)
            pair_map = dict(zip(pair_order, shuffled))
            values = np.asarray(
                [by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
                dtype=float,
            )
        elif family == "wrong_channel_activation":
            values = np.zeros_like(base)
        elif family == "web_path_sign_flip":
            values = -base if draw == 0 else np.zeros_like(base)
        else:
            raise SystemExit(f"unexpected control family: {family}")
        vectors.append(
            {
                "control_index_one_based": replay["control_index_one_based"],
                "control_family": family,
                "draw_index_zero_based": replay["control_draw_index_zero_based"],
                "seed": replay["seed"],
                "operator": replay["operator"],
                "values": values,
            }
        )
    return vectors


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    run = read_one(RUN_MANIFEST)
    protocol = read_one(PROTOCOL)
    readiness = read_one(READINESS)
    geometry = read_one(GEOMETRY)
    theory_rows = read_rows(THEORY)
    replay_rows = read_rows(REPLAY)

    if run["status"] != "ENDPOINT_SCORING_APPROVED_RUN_V1":
        raise SystemExit("endpoint scoring run must be explicitly approved")
    if run["endpoint_scoring_allowed"] != "true":
        raise SystemExit("endpoint scoring run manifest must allow scoring")
    if run["explicit_user_approval_recorded"] != "true":
        raise SystemExit("endpoint scoring run requires explicit user approval")
    if run["parent_scoring_protocol"] != protocol["protocol_id"]:
        raise SystemExit("endpoint scoring run parent protocol mismatch")
    if run["parent_readiness_policy"] != readiness["policy_id"]:
        raise SystemExit("endpoint scoring run parent readiness mismatch")
    if run["parent_endpoint_family_geometry_audit"] != geometry["policy_id"]:
        raise SystemExit("endpoint scoring run parent geometry audit mismatch")
    if readiness["first_blocker"] != "none" or readiness["blocking_component_count"] != "0":
        raise SystemExit("endpoint scoring cannot run while readiness blockers remain")
    if geometry["endpoint_family_geometry_passed"] != "true":
        raise SystemExit("endpoint scoring cannot run unless endpoint-family geometry passes")
    if any(row["contains_residual"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not contain residuals")
    if any(row["uses_kids_data_vector_values"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory vector must not use KiDS data-vector values")
    if any(row["contains_control_scores"] != "false" for row in replay_rows):
        raise SystemExit("null-control replay must not contain precomputed control scores")

    y, cov = load_kids_vector_and_covariance()
    evals = np.linalg.eigvalsh(cov)
    min_eval = float(evals.min())
    max_eval = float(evals.max())
    if min_eval <= 0.0:
        raise SystemExit("KiDS covariance is not positive definite")
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)

    theory_rows = sorted(theory_rows, key=lambda row: int(row["row_index_zero_based"]))
    candidate = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    baseline = np.zeros_like(candidate)
    baseline_chi2 = chi2(y, baseline, factor)
    baseline_aic = baseline_chi2
    cand_amp, cand_chi2, cand_model = best_nonnegative_amplitude(y, candidate, factor)
    cand_aic = cand_chi2 + 2.0
    cand_delta_chi2 = cand_chi2 - baseline_chi2
    cand_delta_aic = cand_aic - baseline_aic

    grid_rows = [
        {
            "run_id": run["run_id"],
            "branch": "baseline_zero",
            "branch_type": "baseline",
            "amplitude": "0.000000000000e+00",
            "chi2": f"{baseline_chi2:.12e}",
            "aic": f"{baseline_aic:.12e}",
            "delta_chi2_vs_baseline": "0.000000000000e+00",
            "delta_aic_vs_baseline": "0.000000000000e+00",
            "k_eff": "0",
        },
        {
            "run_id": run["run_id"],
            "branch": "source_frozen_web_path_candidate",
            "branch_type": "candidate",
            "amplitude": f"{cand_amp:.12e}",
            "chi2": f"{cand_chi2:.12e}",
            "aic": f"{cand_aic:.12e}",
            "delta_chi2_vs_baseline": f"{cand_delta_chi2:.12e}",
            "delta_aic_vs_baseline": f"{cand_delta_aic:.12e}",
            "k_eff": "1",
        },
    ]

    null_rows: list[dict[str, object]] = []
    for control in build_control_vectors(theory_rows, replay_rows):
        amp, control_chi2, _ = best_nonnegative_amplitude(y, control["values"], factor)  # type: ignore[arg-type]
        control_aic = control_chi2 + 2.0
        delta_chi2 = control_chi2 - baseline_chi2
        delta_aic = control_aic - baseline_aic
        null_rows.append(
            {
                "run_id": run["run_id"],
                "control_index_one_based": control["control_index_one_based"],
                "control_family": control["control_family"],
                "draw_index_zero_based": control["draw_index_zero_based"],
                "seed": control["seed"],
                "operator": control["operator"],
                "amplitude": f"{amp:.12e}",
                "chi2": f"{control_chi2:.12e}",
                "aic": f"{control_aic:.12e}",
                "delta_chi2_vs_baseline": f"{delta_chi2:.12e}",
                "delta_aic_vs_baseline": f"{delta_aic:.12e}",
                "beats_candidate_chi2": str(control_chi2 < cand_chi2).lower(),
                "beats_candidate_aic": str(delta_aic < cand_delta_aic).lower(),
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "endpoint_scoring_allowed": "true",
                "claim_boundary": run["claim_boundary"],
            }
        )

    null_chi2_values = [float(row["chi2"]) for row in null_rows]
    null_delta_chi2 = [float(row["delta_chi2_vs_baseline"]) for row in null_rows]
    better_chi2_count = sum(1 for value in null_chi2_values if value < cand_chi2)
    better_aic_count = sum(1 for row in null_rows if row["beats_candidate_aic"] == "true")
    plus_one_tail_chi2 = (better_chi2_count + 1.0) / (len(null_rows) + 1.0)
    plus_one_tail_aic = (better_aic_count + 1.0) / (len(null_rows) + 1.0)
    candidate_rank_chi2 = 1 + better_chi2_count
    candidate_rank_aic = 1 + better_aic_count

    residual_rows = []
    for i, row in enumerate(theory_rows):
        residual_rows.append(
            {
                "run_id": run["run_id"],
                "row_index_zero_based": row["row_index_zero_based"],
                "row_index_one_based": row["row_index_one_based"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "pair_id": row["pair_id"],
                "mode": row["mode"],
                "data_En": f"{y[i]:.12e}",
                "candidate_model": f"{cand_model[i]:.12e}",
                "candidate_residual": f"{(y[i] - cand_model[i]):.12e}",
                "baseline_residual": f"{y[i]:.12e}",
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "endpoint_scoring_allowed": "true",
                "claim_boundary": run["claim_boundary"],
            }
        )

    result_rows = [
        {
            "run_id": run["run_id"],
            "selected_statistic": run["selected_statistic"],
            "n_rows": str(len(y)),
            "covariance_policy": protocol["covariance_policy"],
            "amplitude_policy": run["amplitude_policy"],
            "baseline_chi2": f"{baseline_chi2:.12e}",
            "baseline_aic": f"{baseline_aic:.12e}",
            "candidate_amplitude": f"{cand_amp:.12e}",
            "candidate_chi2": f"{cand_chi2:.12e}",
            "candidate_aic": f"{cand_aic:.12e}",
            "candidate_delta_chi2_vs_baseline": f"{cand_delta_chi2:.12e}",
            "candidate_delta_aic_vs_baseline": f"{cand_delta_aic:.12e}",
            "null_control_count": str(len(null_rows)),
            "candidate_rank_by_chi2": str(candidate_rank_chi2),
            "candidate_rank_by_aic": str(candidate_rank_aic),
            "chi2_nulls_better_than_candidate": str(better_chi2_count),
            "aic_nulls_better_than_candidate": str(better_aic_count),
            "plus_one_tail_fraction_chi2": f"{plus_one_tail_chi2:.12e}",
            "plus_one_tail_fraction_aic": f"{plus_one_tail_aic:.12e}",
            "null_delta_chi2_min": f"{min(null_delta_chi2):.12e}",
            "null_delta_chi2_median": f"{float(np.median(null_delta_chi2)):.12e}",
            "null_delta_chi2_mean": f"{float(np.mean(null_delta_chi2)):.12e}",
            "covariance_min_eigenvalue": f"{min_eval:.12e}",
            "covariance_condition_number": f"{(max_eval / min_eval):.12e}",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_posterior_chains": "false",
            "uses_posthoc_selection": "false",
            "endpoint_scoring_executed": "true",
            "endpoint_validation_claimed": "false",
            "claim_boundary": run["claim_boundary"],
        }
    ]
    summary_rows = [
        {
            "run_id": run["run_id"],
            "status": "KIDS1000_COSEBIS_ENDPOINT_SCORING_RUN_V1_COMPLETE",
            "selected_statistic": run["selected_statistic"],
            "scoring_scope": run["scoring_scope"],
            "candidate_delta_chi2_vs_baseline": result_rows[0]["candidate_delta_chi2_vs_baseline"],
            "candidate_delta_aic_vs_baseline": result_rows[0]["candidate_delta_aic_vs_baseline"],
            "candidate_rank_by_chi2": result_rows[0]["candidate_rank_by_chi2"],
            "candidate_rank_by_aic": result_rows[0]["candidate_rank_by_aic"],
            "plus_one_tail_fraction_chi2": result_rows[0]["plus_one_tail_fraction_chi2"],
            "plus_one_tail_fraction_aic": result_rows[0]["plus_one_tail_fraction_aic"],
            "null_control_count": result_rows[0]["null_control_count"],
            "endpoint_scoring_executed": "true",
            "endpoint_validation_claimed": "false",
            "uses_kids_data_vector_values_for_scoring": "true",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_posterior_chains": "false",
            "uses_posthoc_selection": "false",
            "claim_boundary": run["claim_boundary"],
        }
    ]

    write_csv(GRID, grid_rows)
    write_csv(NULL_CONTROLS, null_rows)
    write_csv(RESIDUALS, residual_rows)
    write_csv(RESULTS, result_rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_V1_COMPLETE "
        f"delta_chi2={cand_delta_chi2:.12g} "
        f"rank_chi2={candidate_rank_chi2}/{len(null_rows) + 1} "
        f"tail_chi2={plus_one_tail_chi2:.12g} "
        "claim_boundary=endpoint_score_not_validation"
    )


if __name__ == "__main__":
    main()
