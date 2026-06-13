#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from run_pantheon_pilot_scoring_v1 import load_covariance, parse_range, read_one, retained_indices
    from run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import load_covariance, parse_range, read_one, retained_indices
    from scripts.run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data/source_manifest/low_z_pantheon_clock_rate_phase_fast_screen_v1.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
CANDIDATE = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.csv"
GRID = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_fast_screen_v1_summary.csv"
CLAIM_BOUNDARY = "clock_rate_phase_fast_screen_source_frozen_not_replay_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def stable_shuffle(values: np.ndarray, seed: int, family_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed + len(values) + 104729 * (family_index + 1))
    return values[rng.permutation(len(values))]


def branch_vector(values: np.ndarray, branch: str, seed: int, family_index: int) -> np.ndarray:
    if branch == "candidate":
        return values
    if branch == "off":
        return np.zeros_like(values)
    if branch == "wrong_sign":
        return -values
    if branch == "deterministic_shuffle":
        return stable_shuffle(values, seed, family_index)
    if branch == "rank_reverse":
        order = np.argsort(values)
        out = np.array(values, copy=True)
        out[order] = values[order[::-1]]
        return out
    raise SystemExit(f"unknown branch: {branch}")


def load_design_and_vectors() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    design = read_rows(DESIGN)
    cand = {(row["CID"], row["source_row_index"]): row for row in read_rows(CANDIDATE)}
    positions: list[int] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    vectors = {"clock_level": [], "clock_slope": [], "clock_phase": []}
    for idx, row in enumerate(design):
        key = (row["CID"], row["source_row_index"])
        if key not in cand:
            continue
        c = cand[key]
        if row["zHD"] != c["zHD"]:
            raise SystemExit(f"z mismatch for {key}")
        positions.append(idx)
        z_values.append(float(row["zHD"]))
        mu_values.append(float(row["MU_SH0ES"]))
        vectors["clock_level"].append(float(c["W_time_clock_level_basis"]))
        vectors["clock_slope"].append(float(c["W_time_clock_slope_basis"]))
        vectors["clock_phase"].append(float(c["W_time_clock_phase_basis"]))
    if len(positions) != 424:
        raise SystemExit(f"expected 424 rows, got {len(positions)}")
    return (
        np.array(z_values, dtype=float),
        np.array(mu_values, dtype=float),
        np.array(positions, dtype=int),
        {key: np.array(value, dtype=float) for key, value in vectors.items()},
    )


def best(rows: list[dict[str, str]], family: str | None = None, branch: str | None = None) -> dict[str, str]:
    scope = rows
    if family is not None:
        scope = [row for row in scope if row["family_id"] == family]
    if branch is not None:
        scope = [row for row in scope if row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing best row for family={family} branch={branch}")
    return min(scope, key=lambda row: float(row["chi2_fast_screen"]))


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "PREAUTH_FAST_SCREEN_SOURCE_FROZEN_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad run status")
    if run["endpoint_replay_allowed"] != "false" or run["endpoint_validation_claimed"] != "false":
        raise SystemExit("fast screen must not authorize replay")
    z, mu, positions, vectors = load_design_and_vectors()
    cov = load_covariance(retained_indices())[np.ix_(positions, positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_time_grid = parse_range(run["omega_time_grid"])
    branches = ["candidate"] + run["control_branches"].split(";")
    seed = int(run["random_seed"])
    grid_rows: list[dict[str, str]] = []

    def add_row(family_id: str, branch: str, omega_m: float, omega_time: float, vector: np.ndarray) -> None:
        omega_eff = 0.0 if branch in {"baseline_only", "off"} else omega_time
        mode = "baseline" if branch == "baseline_only" else "web_only"
        k_eff = 2 if branch in {"baseline_only", "off"} else 3
        model = distance_modulus_void_web(z, omega_m, 0.0, omega_eff, np.zeros_like(vector), vector, mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "family_id": family_id,
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_time": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_fast_screen": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_fast_screen": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for om in omega_m_grid:
        add_row("baseline", "baseline_only", om, 0.0, np.zeros_like(z))
    for family_index, (family_id, vector) in enumerate(vectors.items()):
        for om in omega_m_grid:
            for ot in omega_time_grid:
                for branch in branches:
                    add_row(family_id, branch, om, ot, branch_vector(vector, branch, seed, family_index))
    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_fast_screen"] != "inf"]
    baseline = best(finite, branch="baseline_only")
    family_rows: list[dict[str, str]] = []
    for family_id in vectors:
        candidate = best(finite, family_id, "candidate")
        controls = [best(finite, family_id, branch) for branch in run["control_branches"].split(";")]
        best_control = min(controls, key=lambda row: float(row["chi2_fast_screen"]))
        better = [row for row in controls if float(row["chi2_fast_screen"]) < float(candidate["chi2_fast_screen"])]
        family_rows.append(
            {
                "run_id": run["run_id"],
                "family_id": family_id,
                "candidate_best_chi2": candidate["chi2_fast_screen"],
                "candidate_best_aic": candidate["aic_fast_screen"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_time": candidate["omega_time"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2": best_control["chi2_fast_screen"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_fast_screen']) - float(baseline['chi2_fast_screen']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_fast_screen']) - float(best_control['chi2_fast_screen']):.12g}",
                "controls_better_than_candidate_chi2": str(len(better)),
                "family_survives_local_controls": "true" if not better else "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FAMILY_SUMMARY, family_rows)

    candidates = [best(finite, family_id, "candidate") for family_id in vectors]
    controls = [best(finite, family_id, branch) for family_id in vectors for branch in run["control_branches"].split(";")]
    best_candidate = min(candidates, key=lambda row: float(row["chi2_fast_screen"]))
    best_control = min(controls, key=lambda row: float(row["chi2_fast_screen"]))
    better_controls = [row for row in controls if float(row["chi2_fast_screen"]) < float(best_candidate["chi2_fast_screen"])]
    ranked = sorted(candidates + controls, key=lambda row: float(row["chi2_fast_screen"]))
    verdict = (
        "clock_rate_phase_fast_screen_candidate_survives_requires_review"
        if float(best_candidate["chi2_fast_screen"]) < float(baseline["chi2_fast_screen"])
        and float(best_candidate["chi2_fast_screen"]) < float(best_control["chi2_fast_screen"])
        else "clock_rate_phase_fast_screen_not_control_resistant"
    )
    summary = [
        {
            "run_id": run["run_id"],
            "status": "PREAUTH_FAST_SCREEN_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
            "n_rows": str(len(z)),
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2": baseline["chi2_fast_screen"],
            "baseline_best_aic": baseline["aic_fast_screen"],
            "best_candidate_family": best_candidate["family_id"],
            "best_candidate_chi2": best_candidate["chi2_fast_screen"],
            "best_candidate_aic": best_candidate["aic_fast_screen"],
            "best_candidate_omega_m": best_candidate["omega_m"],
            "best_candidate_omega_time": best_candidate["omega_time"],
            "best_global_control_branch": best_control["branch"],
            "best_global_control_family": best_control["family_id"],
            "best_global_control_chi2": best_control["chi2_fast_screen"],
            "delta_chi2_candidate_minus_baseline": f"{float(best_candidate['chi2_fast_screen']) - float(baseline['chi2_fast_screen']):.12g}",
            "delta_chi2_candidate_minus_best_global_control": f"{float(best_candidate['chi2_fast_screen']) - float(best_control['chi2_fast_screen']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(1 + ranked.index(best_candidate)),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_CLOCK_RATE_PHASE_FAST_SCREEN_BUILT "
        f"best_family={best_candidate['family_id']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
