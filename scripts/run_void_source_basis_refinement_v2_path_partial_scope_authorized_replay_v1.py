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
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import C_LIGHT, load_covariance, parse_range, read_one, retained_indices


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_run_v1.csv"
)
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_v1_summary.csv"
)
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
PATH_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
GRID = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_grid.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_authorized_replay_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_partial_scope_authorized_replay_permission_only_not_validation"
CONTROL_BRANCHES = {
    "path_off_control",
    "wrong_sign_path_control",
    "deterministic_shuffle_path_control",
    "rank_reverse_path_control",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_partial_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    path_rows = read_rows(PATH_VALUES)
    design_by_source_index = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    included_positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    w_values: list[float] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    for path in path_rows:
        if path["source_row_index"] not in design_by_source_index:
            raise SystemExit(f"path row missing from retained design: {path['source_row_index']}")
        design_position, design = design_by_source_index[path["source_row_index"]]
        if design["CID"] != path["CID"]:
            raise SystemExit(f"design/path CID mismatch for source row {path['source_row_index']}")
        value = float(path["W_path_source_value"])
        if value > 0.0:
            if path["full_lowz_W_path_channel"] != "false":
                raise SystemExit("partial replay must not enable full low-z W_path")
            if path["endpoint_replay_allowed"] != "false" or path["endpoint_validation_claimed"] != "false":
                raise SystemExit("source values must not self-authorize replay or validation")
            included_positions.append(design_position)
            cids.append(design["CID"])
            source_indices.append(design["source_row_index"])
            z_values.append(float(design["zHD"]))
            mu_values.append(float(design["MU_SH0ES"]))
            w_values.append(value)
    if len(included_positions) != 12:
        raise SystemExit(f"partial path replay requires exactly 12 rows, found {len(included_positions)}")
    z = np.array(z_values, dtype=float)
    mu = np.array(mu_values, dtype=float)
    return z, mu, np.array(w_values, dtype=float), np.array(included_positions, dtype=int), cids, source_indices


def path_control(w_path: np.ndarray, branch: str, seed: int) -> np.ndarray:
    if branch == "partial_W_path_candidate":
        return w_path
    if branch == "path_off_control":
        return np.zeros_like(w_path)
    if branch == "wrong_sign_path_control":
        return -w_path
    if branch == "deterministic_shuffle_path_control":
        rng = np.random.default_rng(seed + len(w_path))
        return w_path[rng.permutation(len(w_path))]
    if branch == "rank_reverse_path_control":
        return np.sort(w_path)[::-1]
    raise SystemExit(f"unknown path branch: {branch}")


def e_of_z_path(z: np.ndarray, omega_m: float, omega_path: float, w_path: np.ndarray, branch: str) -> np.ndarray:
    if branch == "baseline_only":
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m)
    else:
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m - omega_path) + omega_path * w_path
    if np.any(e2 <= 0):
        return np.full_like(z, np.nan)
    return np.sqrt(e2)


def distance_modulus_path(z: np.ndarray, omega_m: float, omega_path: float, w_path: np.ndarray, branch: str) -> np.ndarray:
    order = np.argsort(z)
    zs = z[order]
    path_sorted = w_path[order]
    grid = np.concatenate([[0.0], zs])
    path_grid = np.concatenate([[path_sorted[0]], path_sorted])
    e = e_of_z_path(grid, omega_m, omega_path, path_grid, branch)
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


def low_z_covariance(included_positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(included_positions, included_positions)]


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("partial path replay run status mismatch")
    if auth["decision"] != "GO_PARTIAL_PATH_REPLAY_PERMISSION_ONLY":
        raise SystemExit("partial path replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization summary must be permission-only and non-validation")
    if auth["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("authorization must not claim physical lensing-path weight")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_sky_direction_selection",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
        "physical_validation_claims",
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    z, mu, w_path, included_positions, cids, source_indices = load_partial_scope()
    cov = low_z_covariance(included_positions)
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite partial path inverse-ones vector")

    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_path_grid = parse_range(run["omega_path_grid"])
    seed = int(run["random_seed"])
    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_path: float, vector: np.ndarray) -> None:
        if branch == "baseline_only":
            omega_eff = 0.0
            k_eff = 2
        else:
            omega_eff = omega_path
            k_eff = 2 if branch == "path_off_control" else 3
        model = distance_modulus_path(z, omega_m, omega_eff, vector, branch)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_path": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_partial_path": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_partial_path": f"{aic:.12g}" if math.isfinite(chi2) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for om in omega_m_grid:
        add_row("baseline_only", om, 0.0, np.zeros_like(w_path))
    for om in omega_m_grid:
        for opath in omega_path_grid:
            for branch in ["partial_W_path_candidate", *sorted(CONTROL_BRANCHES)]:
                add_row(branch, om, opath, path_control(w_path, branch, seed))

    write_csv(GRID, grid_rows)
    finite = [row for row in grid_rows if row["chi2_partial_path"] != "inf"]
    by_branch: dict[str, list[dict[str, str]]] = {}
    for row in finite:
        by_branch.setdefault(row["branch"], []).append(row)
    best = {branch: min(rows, key=lambda row: float(row["chi2_partial_path"])) for branch, rows in by_branch.items()}
    baseline = best["baseline_only"]
    candidate = best["partial_W_path_candidate"]
    controls = [best[branch] for branch in CONTROL_BRANCHES]
    better_controls = [row for row in controls if float(row["chi2_partial_path"]) < float(candidate["chi2_partial_path"])]
    best_control = min(controls, key=lambda row: float(row["chi2_partial_path"]))
    summary = [
        {
            "run_id": run["run_id"],
            "status": run["status"],
            "authorization_decision": auth["decision"],
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "z_min": f"{float(z.min()):.12g}",
            "z_max": f"{float(z.max()):.12g}",
            "w_path_min": f"{float(w_path.min()):.12g}",
            "w_path_max": f"{float(w_path.max()):.12g}",
            "w_path_mean": f"{float(w_path.mean()):.12g}",
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2_partial_path": baseline["chi2_partial_path"],
            "baseline_best_aic_partial_path": baseline["aic_partial_path"],
            "baseline_best_omega_m": baseline["omega_m"],
            "candidate_best_chi2_partial_path": candidate["chi2_partial_path"],
            "candidate_best_aic_partial_path": candidate["aic_partial_path"],
            "candidate_best_omega_m": candidate["omega_m"],
            "candidate_best_omega_path": candidate["omega_path"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2_partial_path": best_control["chi2_partial_path"],
            "best_control_aic_partial_path": best_control["aic_partial_path"],
            "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_partial_path']) - float(baseline['chi2_partial_path']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(candidate['aic_partial_path']) - float(baseline['aic_partial_path']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_partial_path']) - float(best_control['chi2_partial_path']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(1 + len(better_controls)),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "active_channel_family": run["active_channel_family"],
            "disabled_channels": run["disabled_channels"],
            "covariance_regularization": "none_positive_definite_cholesky_12_row_submatrix",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_AUTHORIZED_REPLAY_V1_COMPLETE "
        f"n={len(z)} delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary[0]['candidate_rank_by_chi2_among_candidate_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
