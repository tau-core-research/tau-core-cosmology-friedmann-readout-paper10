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
RUN_MANIFEST = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_run.csv"
AUTH_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_v1_summary.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
KERNEL = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_grid.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_authorized_replay_summary.csv"
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_authorized_replay_permission_only_not_validation"
BRANCHES = [
    "primary_centered_sky_z_candidate",
    "off",
    "wrong_sign",
    "deterministic_shuffle",
    "rank_reverse",
    "axis_x_reference",
    "axis_y_reference",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    design_by_source = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    primary: list[float] = []
    axis_x: list[float] = []
    axis_y: list[float] = []
    reference: list[float] = []
    for row in read_rows(KERNEL):
        source_index = row["source_row_index"]
        if source_index not in design_by_source:
            raise SystemExit(f"kernel row missing from retained design: {source_index}")
        position, design = design_by_source[source_index]
        if design["CID"] != row["CID"]:
            raise SystemExit(f"kernel/design CID mismatch for {source_index}")
        for key in [
            "contains_distance_residuals",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"kernel row must keep {key}=false")
        positions.append(position)
        cids.append(row["CID"])
        source_indices.append(source_index)
        z_values.append(float(design["zHD"]))
        mu_values.append(float(design["MU_SH0ES"]))
        primary.append(float(row["K_primary_normalized"]))
        axis_x.append(float(row["K_axis_x_reference_normalized"]))
        axis_y.append(float(row["K_axis_y_reference_normalized"]))
        reference.append(float(row["K_reference_normalized"]))
    if len(positions) != 12:
        raise SystemExit("observer-orientation replay requires exactly 12 rows")
    vectors = {
        "primary_centered_sky_z_candidate": np.array(primary, dtype=float),
        "axis_x_reference": np.array(axis_x, dtype=float),
        "axis_y_reference": np.array(axis_y, dtype=float),
        "raw_sky_z_reference": np.array(reference, dtype=float),
    }
    return (
        np.array(z_values, dtype=float),
        np.array(mu_values, dtype=float),
        np.array(positions, dtype=int),
        vectors,
        cids,
        source_indices,
    )


def branch_vector(vectors: dict[str, np.ndarray], branch: str, seed: int) -> np.ndarray:
    candidate = vectors["primary_centered_sky_z_candidate"]
    if branch == "primary_centered_sky_z_candidate":
        return candidate
    if branch == "off":
        return np.zeros_like(candidate)
    if branch == "wrong_sign":
        return -candidate
    if branch == "deterministic_shuffle":
        rng = np.random.default_rng(seed + len(candidate) + 409)
        return candidate[rng.permutation(len(candidate))]
    if branch == "rank_reverse":
        return np.sort(candidate)[::-1]
    if branch == "axis_x_reference":
        return vectors["axis_x_reference"]
    if branch == "axis_y_reference":
        return vectors["axis_y_reference"]
    raise SystemExit(f"unknown branch: {branch}")


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


def best(rows: list[dict[str, str]], branch: str | None = None) -> dict[str, str]:
    scope = rows if branch is None else [row for row in rows if row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing branch: {branch}")
    return min(scope, key=lambda row: float(row["chi2_observer_orientation_v2"]))


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("run manifest status mismatch")
    if auth["decision"] != "GO_OBSERVER_ORIENTATION_V2_REPLAY_PERMISSION_ONLY":
        raise SystemExit("observer-orientation V2 replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization must be permission-only and non-validation")
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
    z, mu, positions, vectors, cids, source_indices = load_scope()
    cov = load_covariance(retained_indices())[np.ix_(positions, positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_coupling_grid = parse_range(run["omega_coupling_grid"])
    seed = int(run["random_seed"])
    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_coupling: float, vector: np.ndarray) -> None:
        if branch == "baseline_only":
            omega_eff = 0.0
            k_eff = 2
        else:
            omega_eff = omega_coupling
            k_eff = 2 if branch == "off" else 3
        model = distance_modulus(z, omega_m, omega_eff, vector, branch)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_coupling": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_observer_orientation_v2": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_observer_orientation_v2": f"{aic:.12g}" if math.isfinite(chi2) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for om in omega_m_grid:
        add_row("baseline_only", om, 0.0, np.zeros_like(z))
    for om in omega_m_grid:
        for oc in omega_coupling_grid:
            for branch in BRANCHES:
                add_row(branch, om, oc, branch_vector(vectors, branch, seed))
    write_csv(GRID, grid_rows)
    finite = [row for row in grid_rows if row["chi2_observer_orientation_v2"] != "inf"]
    baseline = best(finite, "baseline_only")
    candidate = best(finite, "primary_centered_sky_z_candidate")
    controls = [best(finite, branch) for branch in BRANCHES if branch != "primary_centered_sky_z_candidate"]
    best_control = min(controls, key=lambda row: float(row["chi2_observer_orientation_v2"]))
    better_controls = [
        row for row in controls if float(row["chi2_observer_orientation_v2"]) < float(candidate["chi2_observer_orientation_v2"])
    ]
    candidate_rank = 1 + len(better_controls)
    summary = [
        {
            "run_id": run["run_id"],
            "status": run["status"],
            "authorization_decision": auth["decision"],
            "active_family": run["active_family"],
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2": baseline["chi2_observer_orientation_v2"],
            "baseline_best_aic": baseline["aic_observer_orientation_v2"],
            "baseline_best_omega_m": baseline["omega_m"],
            "candidate_best_chi2": candidate["chi2_observer_orientation_v2"],
            "candidate_best_aic": candidate["aic_observer_orientation_v2"],
            "candidate_best_omega_m": candidate["omega_m"],
            "candidate_best_omega_coupling": candidate["omega_coupling"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2": best_control["chi2_observer_orientation_v2"],
            "best_control_aic": best_control["aic_observer_orientation_v2"],
            "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_observer_orientation_v2']) - float(baseline['chi2_observer_orientation_v2']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(candidate['aic_observer_orientation_v2']) - float(baseline['aic_observer_orientation_v2']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_observer_orientation_v2']) - float(best_control['chi2_observer_orientation_v2']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(candidate_rank),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "family_survives_controls": "true" if not better_controls else "false",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "disabled_channels": run["disabled_channels"],
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "observer_orientation_v2_permission_replay_family_control_survives_not_validation"
            if not better_controls
            else "observer_orientation_v2_permission_replay_not_control_resistant_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTHORIZED_REPLAY_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']}"
    )


if __name__ == "__main__":
    main()
