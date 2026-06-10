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
MANIFEST = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_v2_path_transform_bank_screen_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
PATH_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
VOID_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values.csv"
WEB_VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values.csv"
GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_transform_bank_screen_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_transform_bank_screen_v1_summary.csv"
FAMILY_SUMMARY = (
    ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_transform_bank_screen_v1_family_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_transform_bank_screen_not_endpoint_not_validation"
TRANSFORMS = [
    "existing_W_path",
    "tile_proximity_raw",
    "tile_margin",
    "tile_inverse_distance",
    "tile_gaussian_sigma_0p5",
    "tile_gaussian_sigma_1p0",
    "tile_gaussian_sigma_2p0",
    "tile_binary_core_1deg",
    "tile_binary_near_1p5deg",
    "tile_rank_quantile",
]
COUPLINGS = ["none", "void", "web", "void_web"]
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


def normalized(values: np.ndarray) -> np.ndarray:
    max_abs = float(np.max(np.abs(values)))
    if max_abs <= 0.0:
        return np.zeros_like(values)
    return values / max_abs


def rank_quantile(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    ranks = np.empty_like(values, dtype=float)
    if len(values) == 1:
        ranks[0] = 0.0
        return ranks
    ranks[order] = np.arange(len(values), dtype=float) / (len(values) - 1)
    return ranks


def stable_shuffle(values: np.ndarray, seed: int, family_index: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 1009 * (family_index + 1))
    return values[rng.permutation(len(values))]


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    path_rows = read_rows(PATH_VALUES)
    void_by_source_index = {row["source_row_index"]: row for row in read_rows(VOID_VALUES)}
    web_by_source_index = {row["source_row_index"]: row for row in read_rows(WEB_VALUES)}
    design_by_source_index = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}

    included_positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    w_path: list[float] = []
    sep_deg: list[float] = []
    void_values: list[float] = []
    web_values: list[float] = []

    for path in path_rows:
        source_index = path["source_row_index"]
        if source_index not in design_by_source_index:
            raise SystemExit(f"path row missing from retained design: {source_index}")
        if source_index not in void_by_source_index or source_index not in web_by_source_index:
            raise SystemExit(f"path row missing V2 void/web values: {source_index}")
        design_position, design = design_by_source_index[source_index]
        void = void_by_source_index[source_index]
        web = web_by_source_index[source_index]
        if not (design["CID"] == path["CID"] == void["CID"] == web["CID"]):
            raise SystemExit(f"CID mismatch for source row {source_index}")
        value = float(path["W_path_source_value"])
        if value > 0.0:
            if path["full_lowz_W_path_channel"] != "false":
                raise SystemExit("transform bank must not enable full low-z W_path")
            for row, label in [(path, "path"), (void, "void"), (web, "web")]:
                if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
                    raise SystemExit(f"{label} source values must not self-authorize replay or validation")
            included_positions.append(design_position)
            cids.append(design["CID"])
            source_indices.append(source_index)
            z_values.append(float(design["zHD"]))
            mu_values.append(float(design["MU_SH0ES"]))
            w_path.append(value)
            sep_deg.append(float(path["nearest_kids_tile_sep_deg"]))
            void_values.append(float(void["W_void_centered"]))
            web_values.append(float(web["W_web_centered"]))

    if len(included_positions) != 12:
        raise SystemExit(f"transform bank screen requires exactly 12 rows, found {len(included_positions)}")

    w = np.array(w_path, dtype=float)
    sep = np.array(sep_deg, dtype=float)
    void = np.array(void_values, dtype=float)
    web = np.array(web_values, dtype=float)
    proximity = np.maximum(0.0, (2.0 - sep) / 2.0)
    margin = np.maximum(0.0, 2.0 - sep)
    transforms = {
        "existing_W_path": w,
        "tile_proximity_raw": proximity,
        "tile_margin": margin,
        "tile_inverse_distance": 1.0 / np.maximum(sep, 0.05),
        "tile_gaussian_sigma_0p5": np.exp(-0.5 * (sep / 0.5) ** 2),
        "tile_gaussian_sigma_1p0": np.exp(-0.5 * (sep / 1.0) ** 2),
        "tile_gaussian_sigma_2p0": np.exp(-0.5 * (sep / 2.0) ** 2),
        "tile_binary_core_1deg": (sep <= 1.0).astype(float),
        "tile_binary_near_1p5deg": (sep <= 1.5).astype(float),
        "tile_rank_quantile": rank_quantile(-sep),
    }
    vectors: dict[str, np.ndarray] = {}
    for transform_id, base in transforms.items():
        vectors[f"{transform_id}__none"] = normalized(base)
        vectors[f"{transform_id}__void"] = normalized(base * void)
        vectors[f"{transform_id}__web"] = normalized(base * web)
        vectors[f"{transform_id}__void_web"] = normalized(base * void * web)
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
    if manifest["status"] != "V2_PATH_TRANSFORM_BANK_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT":
        raise SystemExit("transform-bank manifest status mismatch")
    if manifest["endpoint_replay_allowed"] != "false" or manifest["endpoint_validation_claimed"] != "false":
        raise SystemExit("transform-bank screen must not authorize replay or validation")
    if manifest["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("transform-bank screen must not claim physical path weights")

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
        "path_transform_candidate_survives_fast_screen_requires_authorization"
        if float(best_candidate["chi2_screen"]) < float(baseline["chi2_screen"])
        and float(best_candidate["chi2_screen"]) < float(best_control["chi2_screen"])
        else "path_transform_candidate_not_control_resistant_in_fast_screen"
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
            "path_transform_bank": manifest["path_transform_bank"],
            "coupling_modes": manifest["coupling_modes"],
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
        "PAPER10_V2_PATH_TRANSFORM_BANK_SCREEN_V1_COMPLETE "
        f"best_family={best_candidate['family_id']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"rank={rank} verdict={verdict}"
    )


if __name__ == "__main__":
    main()
