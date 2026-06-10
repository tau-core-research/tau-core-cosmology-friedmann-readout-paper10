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
MANIFEST = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
PATH_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
CROSSMAP = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit.csv"
LOS_ENV = ROOT / "data" / "derived" / "low_z_pantheon_los_environment_v1.csv"
VOID_GEOM = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_summary.csv"
FAMILY_SUMMARY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_sky_environment_screen_v1_family_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_sky_environment_screen_not_endpoint_not_validation"
CONTROL_BRANCHES = ["off", "wrong_sign", "deterministic_shuffle", "rank_reverse"]


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


def ffloat(value: str, default: float = 0.0) -> float:
    if value == "":
        return default
    return float(value)


def normalized(values: np.ndarray) -> np.ndarray:
    max_abs = float(np.max(np.abs(values)))
    if max_abs <= 0.0:
        return np.zeros_like(values)
    return values / max_abs


def stable_shuffle(values: np.ndarray, seed: int, family_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 2003 * (family_index + 1))
    return values[rng.permutation(len(values))]


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    design_by_source_index = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    cross_by_source_index = {row["source_row_index"]: row for row in read_rows(CROSSMAP)}
    los_by_source_index = {row["source_row_index"]: row for row in read_rows(LOS_ENV)}
    void_by_source_index = {row["source_row_index"]: row for row in read_rows(VOID_GEOM)}

    included_positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    raw: dict[str, list[float]] = {
        "W_path": [],
        "W_path_x_sky_x": [],
        "W_path_x_sky_y": [],
        "W_path_x_sky_z": [],
        "W_path_x_tile_offset_ra": [],
        "W_path_x_tile_offset_dec": [],
        "W_path_x_los_log_count": [],
        "W_path_x_los_density_excess": [],
        "W_path_x_nearest_env_inverse_sep": [],
        "W_path_x_nearest_env_density_excess": [],
        "W_path_x_void_wall_proximity": [],
        "W_path_x_signed_void_wall_proximity": [],
        "W_path_x_inside_void": [],
        "W_path_x_void_angular_proximity": [],
    }

    for path in read_rows(PATH_VALUES):
        source_index = path["source_row_index"]
        if source_index not in design_by_source_index:
            raise SystemExit(f"path row missing from retained design: {source_index}")
        if source_index not in cross_by_source_index or source_index not in los_by_source_index:
            raise SystemExit(f"path row missing sky/environment source values: {source_index}")
        if source_index not in void_by_source_index:
            raise SystemExit(f"path row missing void-geometry source values: {source_index}")
        value = float(path["W_path_source_value"])
        if value <= 0.0:
            continue
        design_position, design = design_by_source_index[source_index]
        cross = cross_by_source_index[source_index]
        los = los_by_source_index[source_index]
        void = void_by_source_index[source_index]
        if not (design["CID"] == path["CID"] == cross["CID"] == los["CID"] == void["CID"]):
            raise SystemExit(f"CID mismatch for source row {source_index}")
        for row, label in [(path, "path"), (cross, "crossmap"), (los, "los"), (void, "void")]:
            if row.get("endpoint_validation_claimed", "false") != "false":
                raise SystemExit(f"{label} source values must not claim validation")
            if row.get("contains_distance_residuals", "false") != "false":
                raise SystemExit(f"{label} source values must not contain distance residuals")
            if row.get("contains_fit_statistics", "false") != "false":
                raise SystemExit(f"{label} source values must not contain fit statistics")

        ra = math.radians(float(cross["ra_deg"]))
        dec = math.radians(float(cross["dec_deg"]))
        sky_x = math.cos(dec) * math.cos(ra)
        sky_y = math.cos(dec) * math.sin(ra)
        sky_z = math.sin(dec)
        tile_offset_ra = (float(cross["ra_deg"]) - float(cross["nearest_kids_tile_ra_deg"])) * math.cos(dec)
        tile_offset_dec = float(cross["dec_deg"]) - float(cross["nearest_kids_tile_dec_deg"])
        los_count = ffloat(los["los_environment_count"])
        los_density_excess = ffloat(los["los_matter_density_mean"], default=1.0) - 1.0 if los_count > 0 else 0.0
        nearest_sep = ffloat(los["nearest_environment_angular_sep_deg"], default=0.0)
        nearest_inverse_sep = 1.0 / (nearest_sep + 0.01) if los_count > 0 else 0.0
        nearest_density_excess = ffloat(los["nearest_environment_matter_density"], default=1.0) - 1.0 if los_count > 0 else 0.0
        wall_distance = ffloat(void["wall_distance_mpc_over_h"])
        wall_proximity = math.exp(-abs(wall_distance) / 10.0)
        signed_wall_proximity = math.copysign(wall_proximity, -wall_distance if wall_distance < 0 else 1.0)
        inside_void = 1.0 if void["inside_effective_void_radius"] == "true" else 0.0
        void_angle = ffloat(void["angular_separation_to_void_center_deg"])
        void_angular_proximity = math.exp(-void_angle / 20.0)

        included_positions.append(design_position)
        cids.append(design["CID"])
        source_indices.append(source_index)
        z_values.append(float(design["zHD"]))
        mu_values.append(float(design["MU_SH0ES"]))
        raw["W_path"].append(value)
        raw["W_path_x_sky_x"].append(value * sky_x)
        raw["W_path_x_sky_y"].append(value * sky_y)
        raw["W_path_x_sky_z"].append(value * sky_z)
        raw["W_path_x_tile_offset_ra"].append(value * tile_offset_ra)
        raw["W_path_x_tile_offset_dec"].append(value * tile_offset_dec)
        raw["W_path_x_los_log_count"].append(value * math.log1p(los_count))
        raw["W_path_x_los_density_excess"].append(value * los_density_excess)
        raw["W_path_x_nearest_env_inverse_sep"].append(value * nearest_inverse_sep)
        raw["W_path_x_nearest_env_density_excess"].append(value * nearest_density_excess)
        raw["W_path_x_void_wall_proximity"].append(value * wall_proximity)
        raw["W_path_x_signed_void_wall_proximity"].append(value * signed_wall_proximity)
        raw["W_path_x_inside_void"].append(value * inside_void)
        raw["W_path_x_void_angular_proximity"].append(value * void_angular_proximity)

    if len(included_positions) != 12:
        raise SystemExit(f"sky/environment screen requires exactly 12 rows, found {len(included_positions)}")
    vectors = {key: normalized(np.array(values, dtype=float)) for key, values in raw.items()}
    return (
        np.array(z_values, dtype=float),
        np.array(mu_values, dtype=float),
        np.array(included_positions, dtype=int),
        vectors,
        cids,
        source_indices,
    )


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


def low_z_covariance(included_positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(included_positions, included_positions)]


def main() -> None:
    manifest = read_one(MANIFEST)
    if manifest["status"] != "V2_PATH_SKY_ENVIRONMENT_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT":
        raise SystemExit("sky/environment manifest status mismatch")
    if manifest["endpoint_replay_allowed"] != "false" or manifest["endpoint_validation_claimed"] != "false":
        raise SystemExit("screen must not authorize replay or validation")
    if manifest["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("screen must not claim physical lensing-path weight")
    z, mu, included_positions, vectors, cids, source_indices = load_scope()
    cov = low_z_covariance(included_positions)
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
                "normalization_rule": "max_abs_on_12_row_source_scope",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for om in omega_m_grid:
        add_row("baseline_flat_lcdm", "baseline_only", om, 0.0, np.zeros_like(z))
    for family_index, (family_id, candidate) in enumerate(vectors.items()):
        for om in omega_m_grid:
            for oc in omega_coupling_grid:
                add_row(family_id, "candidate", om, oc, branch_vector(candidate, "candidate", seed, family_index))
                for branch in CONTROL_BRANCHES:
                    add_row(family_id, branch, om, oc, branch_vector(candidate, branch, seed, family_index))
    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_screen"] != "inf"]
    best_by_family_branch: dict[tuple[str, str], dict[str, str]] = {}
    for row in finite:
        key = (row["family_id"], row["branch"])
        old = best_by_family_branch.get(key)
        if old is None or float(row["chi2_screen"]) < float(old["chi2_screen"]):
            best_by_family_branch[key] = row
    baseline = best_by_family_branch[("baseline_flat_lcdm", "baseline_only")]
    family_summary_rows: list[dict[str, str]] = []
    for family_id in sorted(vectors):
        candidate = best_by_family_branch[(family_id, "candidate")]
        controls = [best_by_family_branch[(family_id, branch)] for branch in CONTROL_BRANCHES]
        best_control = min(controls, key=lambda row: float(row["chi2_screen"]))
        controls_better = [row for row in controls if float(row["chi2_screen"]) < float(candidate["chi2_screen"])]
        family_summary_rows.append(
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
    write_csv(FAMILY_SUMMARY, family_summary_rows)

    candidate_rows = [row for (family, branch), row in best_by_family_branch.items() if branch == "candidate"]
    control_rows = [
        row
        for (family, branch), row in best_by_family_branch.items()
        if family != "baseline_flat_lcdm" and branch in CONTROL_BRANCHES
    ]
    best_candidate = min(candidate_rows, key=lambda row: float(row["chi2_screen"]))
    best_control = min(control_rows, key=lambda row: float(row["chi2_screen"]))
    controls_better = [row for row in control_rows if float(row["chi2_screen"]) < float(best_candidate["chi2_screen"])]
    ranked = sorted(candidate_rows + control_rows, key=lambda row: float(row["chi2_screen"]))
    rank = 1 + ranked.index(best_candidate)
    verdict = (
        "path_sky_environment_candidate_survives_fast_screen_requires_authorization"
        if float(best_candidate["chi2_screen"]) < float(baseline["chi2_screen"])
        and float(best_candidate["chi2_screen"]) < float(best_control["chi2_screen"])
        else "path_sky_environment_candidate_not_control_resistant_in_fast_screen"
    )
    summary = [
        {
            "screen_id": manifest["screen_id"],
            "status": manifest["status"],
            "screen_status": "preauthorization_diagnostic_not_endpoint",
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "grid_rows": str(len(grid_rows)),
            "family_summary_rows": str(len(family_summary_rows)),
            "candidate_basis_bank": manifest["candidate_basis_bank"],
            "control_families": manifest["control_families"],
            "normalization_rule": "max_abs_on_12_row_source_scope",
            "baseline_best_chi2_screen": baseline["chi2_screen"],
            "baseline_best_aic_screen": baseline["aic_screen"],
            "baseline_best_omega_m": baseline["omega_m"],
            "best_candidate_family": best_candidate["family_id"],
            "best_candidate_chi2_screen": best_candidate["chi2_screen"],
            "best_candidate_aic_screen": best_candidate["aic_screen"],
            "best_candidate_omega_m": best_candidate["omega_m"],
            "best_candidate_omega_coupling": best_candidate["omega_coupling"],
            "best_control_family": best_control["family_id"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2_screen": best_control["chi2_screen"],
            "best_control_aic_screen": best_control["aic_screen"],
            "delta_chi2_candidate_minus_baseline": f"{float(best_candidate['chi2_screen']) - float(baseline['chi2_screen']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(best_candidate['aic_screen']) - float(baseline['aic_screen']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(best_candidate['chi2_screen']) - float(best_control['chi2_screen']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(rank),
            "controls_better_than_candidate_chi2": str(len(controls_better)),
            "covariance_regularization": "none_positive_definite_cholesky_12_row_submatrix",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "diagnostic_screen_executed": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": verdict,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_SKY_ENVIRONMENT_SCREEN_V1_COMPLETE "
        f"best_family={best_candidate['family_id']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"rank={rank} verdict={verdict}"
    )


if __name__ == "__main__":
    main()
