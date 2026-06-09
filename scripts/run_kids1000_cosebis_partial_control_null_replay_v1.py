#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_kids1000_cosebis_partial_control_diagnostic_scoring_v1 import (
        best_nonnegative_amplitude,
        load_kids_vector_and_covariance,
        read_one,
        read_rows,
    )
except ImportError:
    from scripts.run_kids1000_cosebis_partial_control_diagnostic_scoring_v1 import (
        best_nonnegative_amplitude,
        load_kids_vector_and_covariance,
        read_one,
        read_rows,
    )


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_null_replay_v1.csv"
DIAGNOSTIC_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv"
NULL_SEEDS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1.csv"
DESIGN = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_null_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_null_replay_v1_summary.csv"


def pair_blocks(rows: list[dict[str, str]]) -> list[np.ndarray]:
    blocks: list[np.ndarray] = []
    for start in range(0, len(rows), 20):
        block = rows[start : start + 20]
        if len(block) != 20:
            raise SystemExit("COSEBIs pair block length mismatch")
        blocks.append(np.asarray([int(row["target_row_index_zero_based"]) for row in block], dtype=int))
    if len(blocks) != 15:
        raise SystemExit("expected 15 COSEBIs pair blocks")
    return blocks


def mode_reverse_indices(rows: list[dict[str, str]]) -> np.ndarray:
    indices: list[int] = []
    for start in range(0, len(rows), 20):
        indices.extend(range(start + 19, start - 1, -1))
    return np.asarray(indices, dtype=int)


def pair_reverse_indices(rows: list[dict[str, str]]) -> np.ndarray:
    blocks = pair_blocks(rows)
    return np.concatenate(list(reversed(blocks)))


def branch_score(
    y: np.ndarray, factor: tuple[np.ndarray, bool], vector: np.ndarray
) -> tuple[float, float, float]:
    amp, chi2 = best_nonnegative_amplitude(y, vector, factor)
    return amp, chi2, chi2 + 2.0


def main() -> None:
    run = read_one(RUN_MANIFEST)
    diagnostic = read_one(DIAGNOSTIC_SUMMARY)
    seed_rows = read_rows(NULL_SEEDS)
    design_rows = read_rows(DESIGN)
    if run["status"] != "PARTIAL_CONTROL_NULL_REPLAY_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected null replay status")
    if run["parent_diagnostic_scoring_run"] != diagnostic["run_id"]:
        raise SystemExit("null replay parent diagnostic run mismatch")
    if run["partial_control_scoring_allowed"] != "true" or run["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null replay must allow only partial-control scoring")
    if run["observed_branch"] != "positive_mask_mean":
        raise SystemExit("null replay currently supports positive_mask_mean observed branch")
    seed_by_family = {row["control_family"]: row for row in seed_rows}
    expected_families = run["null_control_families"].split(";")
    if set(seed_by_family) != set(expected_families):
        raise SystemExit("null replay seed family mismatch")

    y, cov = load_kids_vector_and_covariance()
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    observed = np.asarray([float(row["positive_mask_mean"]) for row in design_rows], dtype=float)
    observed_amp, observed_chi2, observed_aic = branch_score(y, factor, observed)
    diagnostic_chi2 = float(diagnostic["best_branch_chi2"])
    if abs(observed_chi2 - diagnostic_chi2) > 5e-8:
        raise SystemExit("observed positive-mask null replay does not match diagnostic score")

    grid_rows: list[dict[str, str]] = []

    def add_control(family: str, draw_index: int, descriptor: str, vector: np.ndarray) -> None:
        amp, chi2, aic = branch_score(y, factor, vector)
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "control_family": family,
                "draw_index": str(draw_index),
                "control_descriptor": descriptor,
                "best_nonnegative_amplitude": f"{amp:.12g}",
                "chi2": f"{chi2:.12g}",
                "aic": f"{aic:.12g}",
                "delta_chi2_vs_observed": f"{chi2 - observed_chi2:.12g}",
                "delta_aic_vs_observed": f"{aic - observed_aic:.12g}",
                "uses_kids_data_vector_values_for_scoring": "true",
                "uses_kids_data_vector_values_for_source_selection": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": run["claim_boundary"],
            }
        )

    rotation_seed = int(seed_by_family["sky_rotation"]["seed"])
    for i, shift in enumerate([60, 120, 180, 240]):
        add_control("sky_rotation", i, f"row_cyclic_shift_{shift}_seed_{rotation_seed}", np.roll(observed, shift))

    blocks = pair_blocks(design_rows)
    shuffle_seed = int(seed_by_family["tomographic_pair_shuffle"]["seed"])
    rng = np.random.default_rng(shuffle_seed)
    for i in range(int(seed_by_family["tomographic_pair_shuffle"]["multiplicity"])):
        perm = rng.permutation(len(blocks))
        indices = np.concatenate([blocks[j] for j in perm])
        add_control("tomographic_pair_shuffle", i, f"pair_block_permutation_seed_{shuffle_seed}", observed[indices])

    wrong_seed = int(seed_by_family["wrong_channel_activation"]["seed"])
    add_control("wrong_channel_activation", 0, f"mode_reverse_within_pairs_seed_{wrong_seed}", observed[mode_reverse_indices(design_rows)])
    add_control("wrong_channel_activation", 1, f"pair_order_reverse_seed_{wrong_seed}", observed[pair_reverse_indices(design_rows)])

    sign_seed = int(seed_by_family["web_path_sign_flip"]["seed"])
    add_control("web_path_sign_flip", 0, f"negative_positive_mean_seed_{sign_seed}", -observed)
    add_control("web_path_sign_flip", 1, f"alternating_pair_sign_seed_{sign_seed}", observed * np.repeat([1, -1] * 8, 20)[:300])

    expected_draws = int(run["total_null_draws"])
    if len(grid_rows) != expected_draws:
        raise SystemExit(f"expected {expected_draws} null draws, got {len(grid_rows)}")

    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(grid_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(grid_rows)

    chi2_values = np.asarray([float(row["chi2"]) for row in grid_rows])
    aic_values = np.asarray([float(row["aic"]) for row in grid_rows])
    chi2_le = int(np.sum(chi2_values <= observed_chi2 + 1e-10))
    aic_le = int(np.sum(aic_values <= observed_aic + 1e-10))
    plus_one_chi2_p = (chi2_le + 1) / (len(grid_rows) + 1)
    plus_one_aic_p = (aic_le + 1) / (len(grid_rows) + 1)
    best_null = min(grid_rows, key=lambda row: float(row["chi2"]))

    summary = {
        "run_id": run["run_id"],
        "status": run["status"],
        "selected_statistic": run["selected_statistic"],
        "control_scope": run["control_scope"],
        "observed_branch": run["observed_branch"],
        "observed_amplitude": f"{observed_amp:.12g}",
        "observed_chi2": f"{observed_chi2:.12g}",
        "observed_aic": f"{observed_aic:.12g}",
        "null_draws": str(len(grid_rows)),
        "best_null_family": best_null["control_family"],
        "best_null_descriptor": best_null["control_descriptor"],
        "best_null_chi2": best_null["chi2"],
        "best_null_aic": best_null["aic"],
        "null_chi2_le_observed_count": str(chi2_le),
        "null_aic_le_observed_count": str(aic_le),
        "plus_one_tail_fraction_chi2_le_observed": f"{plus_one_chi2_p:.12g}",
        "plus_one_tail_fraction_aic_le_observed": f"{plus_one_aic_p:.12g}",
        "median_null_delta_chi2_vs_observed": f"{float(np.median(chi2_values - observed_chi2)):.12g}",
        "partial_control_null_replay_executed": "true",
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
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_NULL_REPLAY_V1_COMPLETE "
        f"null_draws={len(grid_rows)} "
        f"chi2_tail_fraction={summary['plus_one_tail_fraction_chi2_le_observed']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
