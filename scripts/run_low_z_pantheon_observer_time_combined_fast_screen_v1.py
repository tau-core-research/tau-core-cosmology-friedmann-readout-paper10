#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg

try:
    from run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from run_pantheon_pilot_scoring_v1 import C_LIGHT, load_covariance, parse_range, retained_indices
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import C_LIGHT, load_covariance, parse_range, retained_indices


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data/source_manifest/low_z_pantheon_observer_time_combined_fast_screen_v1.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
W_TIME = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv"
GRID = ROOT / "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_observer_time_combined_fast_screen_v1_summary.csv"
CLAIM_BOUNDARY = "observer_time_combined_fast_screen_source_frozen_not_replay_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalized(values: np.ndarray) -> np.ndarray:
    values = np.array(values, dtype=float)
    max_abs = float(np.max(np.abs(values))) if values.size else 0.0
    if max_abs <= 0.0:
        return np.zeros_like(values)
    return values / max_abs


def stable_shuffle(values: np.ndarray, seed: int, family_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 7919 * (family_index + 1) + len(values))
    return values[rng.permutation(len(values))]


def branch_vector(candidate: np.ndarray, branch: str, seed: int, family_index: int) -> np.ndarray:
    if branch == "candidate":
        return candidate
    if branch == "off":
        return np.zeros_like(candidate)
    if branch == "wrong_sign":
        return -candidate
    if branch == "deterministic_shuffle":
        return stable_shuffle(candidate, seed, family_index)
    if branch == "rank_reverse":
        return np.sort(candidate)[::-1]
    raise SystemExit(f"unknown branch: {branch}")


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    design_by_source = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    w_time_by_source = {row["source_row_index"]: row for row in read_rows(W_TIME)}
    positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    w_path_values: list[float] = []
    sky_x_values: list[float] = []
    time_values: list[float] = []
    for row in read_rows(OBSERVER):
        source_index = row["source_row_index"]
        if source_index not in design_by_source:
            raise SystemExit(f"observer row missing from design matrix: {source_index}")
        if source_index not in w_time_by_source:
            raise SystemExit(f"observer row missing W_time candidate: {source_index}")
        position, design = design_by_source[source_index]
        w_row = w_time_by_source[source_index]
        if row["CID"] != design["CID"] or row["CID"] != w_row["CID"]:
            raise SystemExit(f"CID mismatch for source row {source_index}")
        for key in [
            "contains_distance_residuals",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"observer kernel must keep {key}=false")
        for key in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_fit_statistics",
        ]:
            if w_row[key].lower() != "false":
                raise SystemExit(f"W_time basis must keep {key}=False")
        positions.append(position)
        cids.append(row["CID"])
        source_indices.append(source_index)
        z_values.append(float(design["zHD"]))
        mu_values.append(float(design["MU_SH0ES"]))
        w_path_values.append(float(row["W_path_source_value"]))
        sky_x_values.append(float(row["sky_x"]))
        time_values.append(float(w_row["W_time_uncertainty_basis_candidate"]))
    if len(positions) != 12:
        raise SystemExit(f"expected 12 observer-scope rows, got {len(positions)}")
    z_array = np.array(z_values, dtype=float)
    z_center = normalized(z_array - float(np.mean(z_array)))
    observer = normalized(np.array(w_path_values) * np.array(sky_x_values) * z_center)
    time = normalized(np.array(time_values) - float(np.mean(time_values)))
    vectors = {
        "observer_only": observer,
        "time_on_observer_scope": time,
        "observer_times_time": normalized(observer * time),
        "observer_plus_time": normalized(observer + time),
    }
    return (
        z_array,
        np.array(mu_values, dtype=float),
        np.array(positions, dtype=int),
        vectors,
        cids,
        source_indices,
    )


def e_of_z(z: np.ndarray, omega_m: float, omega_coupling: float, vector: np.ndarray, branch: str) -> np.ndarray:
    if branch == "baseline_only":
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m)
    else:
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m - omega_coupling) + omega_coupling * vector
    if np.any(e2 <= 0):
        return np.full_like(z, np.nan)
    return np.sqrt(e2)


def distance_modulus(z: np.ndarray, omega_m: float, omega_coupling: float, vector: np.ndarray, branch: str) -> np.ndarray:
    order = np.argsort(z)
    zs = z[order]
    vector_sorted = vector[order]
    grid = np.concatenate([[0.0], zs])
    vector_grid = np.concatenate([[vector_sorted[0]], vector_sorted])
    e = e_of_z(grid, omega_m, omega_coupling, vector_grid, branch)
    if np.any(~np.isfinite(e)):
        return np.full_like(z, np.nan)
    inv_e = 1.0 / e
    integ = np.zeros_like(grid)
    dz = np.diff(grid)
    integ[1:] = np.cumsum(0.5 * dz * (inv_e[:-1] + inv_e[1:]))
    d_l = (1.0 + zs) * C_LIGHT * integ[1:]
    mu_sorted = 5.0 * np.log10(np.maximum(d_l, 1e-300)) + 25.0
    out = np.empty_like(mu_sorted)
    out[order] = mu_sorted
    return out


def main() -> None:
    run = read_one(RUN)
    if run["status"] != "PREAUTH_FAST_SCREEN_SOURCE_FROZEN_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("unexpected run status")
    if run["endpoint_replay_allowed"] != "false" or run["endpoint_validation_claimed"] != "false":
        raise SystemExit("fast screen must not authorize replay or validation")
    z, mu, positions, vectors, cids, source_indices = load_scope()
    cov = load_covariance(retained_indices())[np.ix_(positions, positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_coupling_grid = parse_range(run["omega_coupling_grid"])
    seed = int(run["random_seed"])
    branches = ["candidate"] + run["control_branches"].split(";")
    grid_rows: list[dict[str, str]] = []

    def add_row(family_id: str, branch: str, omega_m: float, omega_coupling: float, vector: np.ndarray) -> None:
        omega_eff = 0.0 if branch in {"baseline_only", "off"} else omega_coupling
        k_eff = 2 if branch in {"baseline_only", "off"} else 3
        model = distance_modulus(z, omega_m, omega_eff, vector, branch)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "family_id": family_id,
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_coupling": f"{omega_eff:.12g}",
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
    for family_index, (family_id, candidate) in enumerate(vectors.items()):
        for om in omega_m_grid:
            for oc in omega_coupling_grid:
                for branch in branches:
                    add_row(family_id, branch, om, oc, branch_vector(candidate, branch, seed, family_index))
    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_fast_screen"] != "inf"]
    best_by_family_branch: dict[tuple[str, str], dict[str, str]] = {}
    for row in finite:
        key = (row["family_id"], row["branch"])
        old = best_by_family_branch.get(key)
        if old is None or float(row["chi2_fast_screen"]) < float(old["chi2_fast_screen"]):
            best_by_family_branch[key] = row
    baseline = min((row for row in finite if row["branch"] == "baseline_only"), key=lambda row: float(row["chi2_fast_screen"]))
    family_rows: list[dict[str, str]] = []
    for family_id in vectors:
        candidate = best_by_family_branch[(family_id, "candidate")]
        controls = [best_by_family_branch[(family_id, branch)] for branch in run["control_branches"].split(";")]
        best_control = min(controls, key=lambda row: float(row["chi2_fast_screen"]))
        controls_better = [row for row in controls if float(row["chi2_fast_screen"]) < float(candidate["chi2_fast_screen"])]
        family_rows.append(
            {
                "run_id": run["run_id"],
                "family_id": family_id,
                "candidate_best_chi2": candidate["chi2_fast_screen"],
                "candidate_best_aic": candidate["aic_fast_screen"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_coupling": candidate["omega_coupling"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2": best_control["chi2_fast_screen"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_fast_screen']) - float(baseline['chi2_fast_screen']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_fast_screen']) - float(best_control['chi2_fast_screen']):.12g}",
                "controls_better_than_candidate_chi2": str(len(controls_better)),
                "family_survives_local_controls": "true" if not controls_better else "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FAMILY_SUMMARY, family_rows)

    candidate_rows = [best_by_family_branch[(family_id, "candidate")] for family_id in vectors]
    control_rows = [
        best_by_family_branch[(family_id, branch)]
        for family_id in vectors
        for branch in run["control_branches"].split(";")
    ]
    best_candidate = min(candidate_rows, key=lambda row: float(row["chi2_fast_screen"]))
    best_control = min(control_rows, key=lambda row: float(row["chi2_fast_screen"]))
    controls_better = [row for row in control_rows if float(row["chi2_fast_screen"]) < float(best_candidate["chi2_fast_screen"])]
    ranked = sorted(candidate_rows + control_rows, key=lambda row: float(row["chi2_fast_screen"]))
    verdict = (
        "observer_time_combined_fast_screen_candidate_survives_requires_review"
        if float(best_candidate["chi2_fast_screen"]) < float(baseline["chi2_fast_screen"])
        and float(best_candidate["chi2_fast_screen"]) < float(best_control["chi2_fast_screen"])
        else "observer_time_combined_fast_screen_not_control_resistant"
    )
    summary = [
        {
            "run_id": run["run_id"],
            "status": "PREAUTH_FAST_SCREEN_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2": baseline["chi2_fast_screen"],
            "baseline_best_aic": baseline["aic_fast_screen"],
            "best_candidate_family": best_candidate["family_id"],
            "best_candidate_chi2": best_candidate["chi2_fast_screen"],
            "best_candidate_aic": best_candidate["aic_fast_screen"],
            "best_candidate_omega_m": best_candidate["omega_m"],
            "best_candidate_omega_coupling": best_candidate["omega_coupling"],
            "best_global_control_branch": best_control["branch"],
            "best_global_control_family": best_control["family_id"],
            "best_global_control_chi2": best_control["chi2_fast_screen"],
            "delta_chi2_candidate_minus_baseline": f"{float(best_candidate['chi2_fast_screen']) - float(baseline['chi2_fast_screen']):.12g}",
            "delta_chi2_candidate_minus_best_global_control": f"{float(best_candidate['chi2_fast_screen']) - float(best_control['chi2_fast_screen']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(1 + ranked.index(best_candidate)),
            "controls_better_than_candidate_chi2": str(len(controls_better)),
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
        "PAPER10_OBSERVER_TIME_COMBINED_FAST_SCREEN_BUILT "
        f"best_family={best_candidate['family_id']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
