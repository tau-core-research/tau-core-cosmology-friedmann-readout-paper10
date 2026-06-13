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
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
METRIC_ENV = ROOT / "data/derived/observer_path_metric_environment_product_v1.csv"
OBSERVER = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
GRID = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_fast_screen_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_fast_screen_not_endpoint_not_validation"
CONTROL_BRANCHES = ["off", "wrong_sign", "deterministic_shuffle", "rank_reverse"]
OMEGA_M_GRID = "0.20:0.40:0.02"
OMEGA_COUPLING_GRID = "-0.20:0.20:0.05"
RANDOM_SEED = 20260612


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


def branch_vector(candidate: np.ndarray, branch: str, family_index: int) -> np.ndarray:
    if branch == "candidate":
        return candidate
    if branch == "off":
        return np.zeros_like(candidate)
    if branch == "wrong_sign":
        return -candidate
    if branch == "deterministic_shuffle":
        rng = np.random.default_rng(RANDOM_SEED + len(candidate) + 733 + family_index)
        return candidate[rng.permutation(len(candidate))]
    if branch == "rank_reverse":
        return np.sort(candidate)[::-1]
    raise SystemExit(f"unknown branch: {branch}")


def load_scope() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, np.ndarray], list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    design_by_source = {row["source_row_index"]: (i, row) for i, row in enumerate(design_rows)}
    observer_by_source = {row["source_row_index"]: row for row in read_rows(OBSERVER)}
    positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    metric_env: list[float] = []
    sky_x: list[float] = []
    sky_z: list[float] = []
    w_path: list[float] = []
    for row in read_rows(METRIC_ENV):
        source_index = row["source_row_index"]
        if row["metric_environment_product_available_for_source"] != "true":
            raise SystemExit(f"metric product unavailable for {source_index}")
        for key in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_lensing_residuals",
            "contains_fit_statistics",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"metric product row must keep {key}=false")
        if source_index not in design_by_source or source_index not in observer_by_source:
            raise SystemExit(f"missing design/observer row for {source_index}")
        position, design = design_by_source[source_index]
        observer = observer_by_source[source_index]
        if design["CID"] != row["CID"] or observer["CID"] != row["CID"]:
            raise SystemExit(f"CID mismatch for {source_index}")
        positions.append(position)
        cids.append(row["CID"])
        source_indices.append(source_index)
        z_values.append(float(design["zHD"]))
        mu_values.append(float(design["MU_SH0ES"]))
        metric_env.append(float(row["metric_environment_path_weight"]))
        sky_x.append(float(observer["sky_x"]))
        sky_z.append(float(observer["sky_z"]))
        w_path.append(float(observer["W_path_source_value"]))
    if len(positions) != 12:
        raise SystemExit("metric-environment screen requires exactly 12 rows")
    z = np.array(z_values, dtype=float)
    zc = normalized(z - float(np.mean(z)))
    metric = np.array(metric_env, dtype=float)
    sx = np.array(sky_x, dtype=float)
    sz = np.array(sky_z, dtype=float)
    wp = np.array(w_path, dtype=float)
    raw = {
        "metric_environment_path": metric,
        "metric_environment_x_sky_x": metric * sx,
        "metric_environment_x_sky_z": metric * sz,
        "metric_environment_x_zcenter": metric * zc,
        "metric_environment_x_sky_x_x_zcenter": metric * sx * zc,
        "metric_environment_x_w_path": metric * wp,
        "metric_environment_x_w_path_x_sky_x_x_zcenter": metric * wp * sx * zc,
    }
    return (
        z,
        np.array(mu_values, dtype=float),
        np.array(positions, dtype=int),
        {key: normalized(value) for key, value in raw.items()},
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


def best(rows: list[dict[str, str]], family: str, branch: str) -> dict[str, str]:
    scope = [row for row in rows if row["family_id"] == family and row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing {family}/{branch}")
    return min(scope, key=lambda row: float(row["chi2_metric_environment_screen"]))


def main() -> None:
    z, mu, positions, vectors, cids, source_indices = load_scope()
    cov = load_covariance(retained_indices())[np.ix_(positions, positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    omega_m_grid = parse_range(OMEGA_M_GRID)
    omega_coupling_grid = parse_range(OMEGA_COUPLING_GRID)
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
                "screen_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_FAST_SCREEN_V1",
                "family_id": family_id,
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_coupling": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_metric_environment_screen": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_metric_environment_screen": f"{aic:.12g}" if math.isfinite(chi2) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
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
                add_row(family_id, "candidate", om, oc, branch_vector(candidate, "candidate", family_index))
                for branch in CONTROL_BRANCHES:
                    add_row(family_id, branch, om, oc, branch_vector(candidate, branch, family_index))
    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_metric_environment_screen"] != "inf"]
    baseline = best(finite, "baseline_flat_lcdm", "baseline_only")
    family_rows: list[dict[str, str]] = []
    for family_id in families:
        candidate = best(finite, family_id, "candidate")
        controls = [best(finite, family_id, branch) for branch in CONTROL_BRANCHES]
        best_control = min(controls, key=lambda row: float(row["chi2_metric_environment_screen"]))
        controls_better = [
            row for row in controls
            if float(row["chi2_metric_environment_screen"]) < float(candidate["chi2_metric_environment_screen"])
        ]
        family_rows.append(
            {
                "screen_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_FAST_SCREEN_V1",
                "family_id": family_id,
                "candidate_best_chi2": candidate["chi2_metric_environment_screen"],
                "candidate_best_aic": candidate["aic_metric_environment_screen"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_coupling": candidate["omega_coupling"],
                "baseline_best_chi2": baseline["chi2_metric_environment_screen"],
                "baseline_best_aic": baseline["aic_metric_environment_screen"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2": best_control["chi2_metric_environment_screen"],
                "best_control_aic": best_control["aic_metric_environment_screen"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_metric_environment_screen']) - float(baseline['chi2_metric_environment_screen']):.12g}",
                "delta_aic_candidate_minus_baseline": f"{float(candidate['aic_metric_environment_screen']) - float(baseline['aic_metric_environment_screen']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_metric_environment_screen']) - float(best_control['chi2_metric_environment_screen']):.12g}",
                "controls_better_than_candidate_chi2": str(len(controls_better)),
                "survives_family_controls": "true" if not controls_better else "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FAMILY_SUMMARY, family_rows)
    best_family = min(family_rows, key=lambda row: float(row["candidate_best_chi2"]))
    surviving = [row for row in family_rows if row["survives_family_controls"] == "true"]
    summary = [
        {
            "screen_id": "OBSERVER_PATH_METRIC_ENVIRONMENT_FAST_SCREEN_V1",
            "status": "PREAUTH_DIAGNOSTIC_SCREEN_NOT_ENDPOINT",
            "n_rows": str(len(z)),
            "source_row_indices": ";".join(source_indices),
            "cids": ";".join(cids),
            "family_count": str(len(family_rows)),
            "grid_rows": str(len(grid_rows)),
            "baseline_best_chi2": baseline["chi2_metric_environment_screen"],
            "baseline_best_aic": baseline["aic_metric_environment_screen"],
            "best_candidate_family": best_family["family_id"],
            "best_candidate_chi2": best_family["candidate_best_chi2"],
            "best_candidate_aic": best_family["candidate_best_aic"],
            "best_candidate_delta_chi2_minus_baseline": best_family["delta_chi2_candidate_minus_baseline"],
            "best_candidate_delta_chi2_minus_best_control": best_family["delta_chi2_candidate_minus_best_control"],
            "best_candidate_survives_controls": best_family["survives_family_controls"],
            "control_surviving_family_count": str(len(surviving)),
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "METRIC_ENVIRONMENT_PREAUTH_SIGNAL_SURVIVES_CONTROLS_NOT_ENDPOINT"
            if best_family["survives_family_controls"] == "true"
            else "METRIC_ENVIRONMENT_PREAUTH_SIGNAL_NOT_CONTROL_RESISTANT_NOT_ENDPOINT",
        }
    ]
    write_csv(SUMMARY, summary)
    DOC.write_text(
        "# Observer/path metric-environment fast screen v1\n\n"
        "**Doc class:** preauthorization diagnostic screen\n"
        "**Status:** not endpoint replay; not validation\n\n"
        "This screen tests the newly built caveated metric-environment path product "
        "on the frozen 12-row observer/path scope. It compares source-side candidate "
        "families against off, wrong-sign, deterministic-shuffle, and rank-reverse "
        "controls. It does not authorize endpoint use.\n\n"
        f"Best candidate family: `{summary[0]['best_candidate_family']}`.\n"
        f"Delta chi2 versus baseline: `{summary[0]['best_candidate_delta_chi2_minus_baseline']}`.\n"
        f"Delta chi2 versus best control: `{summary[0]['best_candidate_delta_chi2_minus_best_control']}`.\n"
        f"Verdict: `{summary[0]['verdict']}`.\n\n"
        f"Claim boundary: `{CLAIM_BOUNDARY}`.\n"
    )
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_FAST_SCREEN_V1_BUILT "
        f"best={summary[0]['best_candidate_family']} verdict={summary[0]['verdict']} "
        f"delta_baseline={summary[0]['best_candidate_delta_chi2_minus_baseline']}"
    )


if __name__ == "__main__":
    main()
