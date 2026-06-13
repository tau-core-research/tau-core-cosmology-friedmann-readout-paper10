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
MANIFEST = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
KERNEL = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv"
CLAIM_BOUNDARY = "v2_observer_basis_fast_screen_not_endpoint_not_validation"
CONTROL_BRANCHES = ["off", "wrong_sign", "deterministic_shuffle", "rank_reverse"]


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


def normalized(values: np.ndarray) -> np.ndarray:
    max_abs = float(np.max(np.abs(values)))
    if max_abs <= 0.0:
        return np.zeros_like(values)
    return values / max_abs


def stable_shuffle(values: np.ndarray, seed: int, family_index: int) -> np.ndarray:
    _ = family_index
    rng = np.random.default_rng(seed + len(values) + 409)
    return values[rng.permutation(len(values))]


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    design_by_source = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    w_path: list[float] = []
    sky_x: list[float] = []
    sky_y: list[float] = []
    sky_z: list[float] = []
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
        w_path.append(float(row["W_path_source_value"]))
        sky_x.append(float(row["sky_x"]))
        sky_y.append(float(row["sky_y"]))
        sky_z.append(float(row["sky_z"]))
    if len(positions) != 12:
        raise SystemExit("observer-basis fast screen requires exactly 12 rows")

    z = np.array(z_values, dtype=float)
    zc = z - float(np.mean(z))
    zc = normalized(zc)
    wp = np.array(w_path, dtype=float)
    sx = np.array(sky_x, dtype=float)
    sy = np.array(sky_y, dtype=float)
    sz = np.array(sky_z, dtype=float)
    cx = sx - float(np.mean(sx))
    cy = sy - float(np.mean(sy))
    cz = sz - float(np.mean(sz))
    raw = {
        "W_path": wp,
        "W_path_x_sky_x": wp * sx,
        "W_path_x_sky_y": wp * sy,
        "W_path_x_sky_z": wp * sz,
        "W_path_x_centered_sky_x": wp * cx,
        "W_path_x_centered_sky_y": wp * cy,
        "W_path_x_centered_sky_z": wp * cz,
        "W_path_x_sky_xy_plus": wp * (sx + sy) / math.sqrt(2.0),
        "W_path_x_sky_xy_minus": wp * (sx - sy) / math.sqrt(2.0),
        "W_path_x_sky_xz_plus": wp * (sx + sz) / math.sqrt(2.0),
        "W_path_x_sky_yz_plus": wp * (sy + sz) / math.sqrt(2.0),
        "W_path_x_centered_sky_xy_plus": wp * (cx + cy) / math.sqrt(2.0),
        "W_path_x_centered_sky_xy_minus": wp * (cx - cy) / math.sqrt(2.0),
        "W_path_x_centered_sky_xz_plus": wp * (cx + cz) / math.sqrt(2.0),
        "W_path_x_centered_sky_yz_plus": wp * (cy + cz) / math.sqrt(2.0),
        "W_path_x_sky_z_x_zcenter": wp * sz * zc,
        "W_path_x_centered_sky_z_x_zcenter": wp * cz * zc,
        "W_path_x_sky_x_x_zcenter": wp * sx * zc,
        "W_path_x_sky_y_x_zcenter": wp * sy * zc,
    }
    vectors = {key: normalized(value) for key, value in raw.items()}
    return z, np.array(mu_values, dtype=float), np.array(positions, dtype=int), vectors, cids, source_indices


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


def best(rows: list[dict[str, str]], family: str, branch: str) -> dict[str, str]:
    scope = [row for row in rows if row["family_id"] == family and row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing {family}/{branch}")
    return min(scope, key=lambda row: float(row["chi2_screen"]))


def main() -> None:
    manifest = read_one(MANIFEST)
    if manifest["status"] != "V2_OBSERVER_BASIS_FAST_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT":
        raise SystemExit("observer-basis manifest status mismatch")
    if manifest["endpoint_replay_allowed"] != "false" or manifest["endpoint_validation_claimed"] != "false":
        raise SystemExit("screen must not authorize replay or validation")
    z, mu, positions, vectors, cids, source_indices = load_scope()
    cov = load_covariance(retained_indices())[np.ix_(positions, positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(manifest["omega_m_grid"])
    omega_coupling_grid = parse_range(manifest["omega_coupling_grid"])
    seed = int(manifest["random_seed"])
    grid_rows: list[dict[str, str]] = []

    def add_row(family_id: str, branch: str, omega_m: float, omega_coupling: float, vector: np.ndarray) -> None:
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
                "screen_id": manifest["screen_id"],
                "family_id": family_id,
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_coupling": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_screen": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_screen": f"{aic:.12g}" if math.isfinite(chi2) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for om in omega_m_grid:
        add_row("baseline_flat_lcdm", "baseline_only", om, 0.0, np.zeros_like(z))
    families = sorted(vectors)
    for family_index, family_id in enumerate(families):
        candidate = vectors[family_id]
        for om in omega_m_grid:
            for oc in omega_coupling_grid:
                add_row(family_id, "candidate", om, oc, branch_vector(candidate, "candidate", seed, family_index))
                for branch in CONTROL_BRANCHES:
                    add_row(family_id, branch, om, oc, branch_vector(candidate, branch, seed, family_index))
    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_screen"] != "inf"]
    baseline = best(finite, "baseline_flat_lcdm", "baseline_only")
    family_rows: list[dict[str, str]] = []
    for family_id in families:
        candidate = best(finite, family_id, "candidate")
        controls = [best(finite, family_id, branch) for branch in CONTROL_BRANCHES]
        best_control = min(controls, key=lambda row: float(row["chi2_screen"]))
        controls_better = [row for row in controls if float(row["chi2_screen"]) < float(candidate["chi2_screen"])]
        family_rows.append(
            {
                "screen_id": manifest["screen_id"],
                "family_id": family_id,
                "candidate_best_chi2_screen": candidate["chi2_screen"],
                "candidate_best_aic_screen": candidate["aic_screen"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_coupling": candidate["omega_coupling"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2_screen": best_control["chi2_screen"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_screen']) - float(baseline['chi2_screen']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_screen']) - float(best_control['chi2_screen']):.12g}",
                "controls_better_than_candidate_chi2": str(len(controls_better)),
                "survives_family_controls": str(
                    float(candidate["chi2_screen"]) < float(baseline["chi2_screen"])
                    and float(candidate["chi2_screen"]) < float(best_control["chi2_screen"])
                ).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FAMILY_SUMMARY, family_rows)
    candidate_best = min((best(finite, family_id, "candidate") for family_id in families), key=lambda row: float(row["chi2_screen"]))
    global_controls = [best(finite, family_id, branch) for family_id in families for branch in CONTROL_BRANCHES]
    best_global_control = min(global_controls, key=lambda row: float(row["chi2_screen"]))
    surviving = [row for row in family_rows if row["survives_family_controls"] == "true"]
    summary = [
        {
            "screen_id": manifest["screen_id"],
            "status": manifest["status"],
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "n_families": str(len(families)),
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2": baseline["chi2_screen"],
            "best_candidate_family": candidate_best["family_id"],
            "best_candidate_chi2": candidate_best["chi2_screen"],
            "best_candidate_delta_chi2_minus_baseline": f"{float(candidate_best['chi2_screen']) - float(baseline['chi2_screen']):.12g}",
            "best_global_control_family": best_global_control["family_id"],
            "best_global_control_branch": best_global_control["branch"],
            "best_global_control_chi2": best_global_control["chi2_screen"],
            "best_candidate_delta_chi2_minus_best_global_control": f"{float(candidate_best['chi2_screen']) - float(best_global_control['chi2_screen']):.12g}",
            "surviving_family_count": str(len(surviving)),
            "surviving_families": ";".join(row["family_id"] for row in surviving),
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "disabled_channels": manifest["disabled_channels"],
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "observer_basis_fast_screen_has_candidate_for_review"
            if surviving
            else "observer_basis_fast_screen_no_control_surviving_candidate",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_OBSERVER_BASIS_FAST_SCREEN_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"surviving={summary[0]['surviving_family_count']} "
        f"best={summary[0]['best_candidate_family']}"
    )


if __name__ == "__main__":
    main()
