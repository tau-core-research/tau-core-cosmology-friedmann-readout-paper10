#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import os
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
RUN_TEMPLATE = ROOT / "data" / "source_manifest" / "act_dr6_lensing_path_weight_replay_run_template_v1.csv"
AUTH_SUMMARY = Path(
    os.environ.get(
        "ACT_DR6_LENSING_PATH_WEIGHT_AUTH_SUMMARY",
        ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_replay_authorization_review_response_v1_summary.csv",
    )
)
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
CANDIDATE = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_candidate_v1.csv"
GRID = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_path_weight_authorized_replay_permission_only_not_validation"
CONTROL_BRANCHES = {
    "wrong_sign",
    "curl_null",
    "diff_f150_f090_null",
    "deterministic_shuffle",
    "rank_reverse",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_design_and_candidate() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    design_rows = read_rows(DESIGN)
    candidate_rows = read_rows(CANDIDATE)
    candidate_by_key = {(row["CID"], row["source_row_index"]): row for row in candidate_rows}
    positions: list[int] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    w_values: list[float] = []
    curl_values: list[float] = []
    diff_values: list[float] = []
    for idx, design in enumerate(design_rows):
        key = (design["CID"], design["source_row_index"])
        if key not in candidate_by_key:
            continue
        cand = candidate_by_key[key]
        if design["zHD"] != cand["zHD"]:
            raise SystemExit(f"z mismatch for {key}")
        positions.append(idx)
        z_values.append(float(design["zHD"]))
        mu_values.append(float(design["MU_SH0ES"]))
        w_values.append(float(cand["w_act_baseline_candidate"]))
        curl_values.append(float(cand["w_act_curl_null"]))
        diff_values.append(float(cand["w_act_diff_f150_f090_null"]))
    if len(positions) != 424:
        raise SystemExit(f"expected 424 ACT candidate rows, got {len(positions)}")
    return (
        np.array(z_values, dtype=float),
        np.array(mu_values, dtype=float),
        np.array(w_values, dtype=float),
        np.array(curl_values, dtype=float),
        np.array(diff_values, dtype=float),
        np.array(positions, dtype=int),
    )


def covariance_for_positions(positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(positions, positions)]


def vector_for_branch(w: np.ndarray, curl: np.ndarray, diff: np.ndarray, branch: str) -> np.ndarray:
    if branch == "candidate":
        return w
    if branch == "off":
        return np.zeros_like(w)
    if branch == "wrong_sign":
        return -w
    if branch == "curl_null":
        return curl
    if branch == "diff_f150_f090_null":
        return diff
    if branch == "deterministic_shuffle":
        rng = np.random.default_rng(20260612 + len(w))
        return w[rng.permutation(len(w))]
    if branch == "rank_reverse":
        order = np.argsort(w)
        out = np.array(w, copy=True)
        out[order] = w[order[::-1]]
        return out
    raise SystemExit(f"unknown ACT replay branch: {branch}")


def e_of_z(z: np.ndarray, omega_m: float, omega_path: float, w_path: np.ndarray, branch: str) -> np.ndarray:
    if branch == "baseline_only":
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m)
    else:
        e2 = omega_m * (1.0 + z) ** 3 + (1.0 - omega_m - omega_path) + omega_path * w_path
    if np.any(e2 <= 0):
        return np.full_like(z, np.nan)
    return np.sqrt(e2)


def distance_modulus(z: np.ndarray, omega_m: float, omega_path: float, w_path: np.ndarray, branch: str) -> np.ndarray:
    order = np.argsort(z)
    zs = z[order]
    w_sorted = w_path[order]
    grid = np.concatenate([[0.0], zs])
    w_grid = np.concatenate([[w_sorted[0]], w_sorted])
    e = e_of_z(grid, omega_m, omega_path, w_grid, branch)
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
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "ACT_DR6_LENSING_PATH_WEIGHT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("bad ACT replay template status")
    if auth["permission_only_replay_authorized"] != "true":
        raise SystemExit("ACT path-weight replay is not authorized")
    if auth["endpoint_validation_claimed"] != "false" or auth["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("authorization must remain non-validation and non-physical")
    if auth["verdict"] != "act_dr6_lensing_path_weight_caveated_replay_authorized_not_validation":
        raise SystemExit("authorization verdict does not permit guarded replay")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    z, mu, w, curl, diff, positions = load_design_and_candidate()
    cov = covariance_for_positions(positions)
    factor, _, _ = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite inverse-ones vector")

    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_path_grid = parse_range(run["omega_path_grid"])
    rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_path: float, vec: np.ndarray) -> None:
        omega_eff = 0.0 if branch in {"baseline_only", "off"} else omega_path
        model = distance_modulus(z, omega_m, omega_eff, vec, branch)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        k_eff = 2 if branch in {"baseline_only", "off"} else 3
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        rows.append(
            {
                "run_id": "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_V1",
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_path": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_act_path": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_act_path": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "permission_only_replay_authorized": "true",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for omega_m in omega_m_grid:
        add_row("baseline_only", omega_m, 0.0, np.zeros_like(w))
        add_row("off", omega_m, 0.0, np.zeros_like(w))
        for omega_path in omega_path_grid:
            for branch in ["candidate", *sorted(CONTROL_BRANCHES)]:
                add_row(branch, omega_m, omega_path, vector_for_branch(w, curl, diff, branch))

    write_csv(GRID, rows)
    finite = [row for row in rows if row["chi2_act_path"] != "inf"]
    best_by_branch = {
        branch: min([row for row in finite if row["branch"] == branch], key=lambda row: float(row["chi2_act_path"]))
        for branch in sorted({row["branch"] for row in finite})
    }
    baseline = best_by_branch["baseline_only"]
    candidate = best_by_branch["candidate"]
    controls = [best_by_branch[branch] for branch in CONTROL_BRANCHES]
    best_control = min(controls, key=lambda row: float(row["chi2_act_path"]))
    better_controls = [row for row in controls if float(row["chi2_act_path"]) < float(candidate["chi2_act_path"])]
    verdict = (
        "act_dr6_lensing_path_weight_candidate_survives_controls_permission_only_not_validation"
        if not better_controls
        else "act_dr6_lensing_path_weight_candidate_not_control_resistant_permission_only_not_validation"
    )
    write_csv(
        SUMMARY,
        [
            {
                "run_id": "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_V1",
                "status": "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_PERMISSION_ONLY_NOT_VALIDATION",
                "authorization_verdict": auth["verdict"],
                "n_rows": str(len(z)),
                "grid_rows": str(len(rows)),
                "candidate_best_chi2_act_path": candidate["chi2_act_path"],
                "candidate_best_aic_act_path": candidate["aic_act_path"],
                "candidate_best_omega_m": candidate["omega_m"],
                "candidate_best_omega_path": candidate["omega_path"],
                "baseline_best_chi2_act_path": baseline["chi2_act_path"],
                "baseline_best_aic_act_path": baseline["aic_act_path"],
                "best_control_branch": best_control["branch"],
                "best_control_chi2_act_path": best_control["chi2_act_path"],
                "best_control_aic_act_path": best_control["aic_act_path"],
                "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_act_path']) - float(baseline['chi2_act_path']):.12g}",
                "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_act_path']) - float(best_control['chi2_act_path']):.12g}",
                "controls_better_than_candidate": str(len(better_controls)),
                "family_survives_controls": "true" if not better_controls else "false",
                "permission_only_replay_authorized": "true",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": verdict,
            }
        ],
    )
    print(
        "ACT_DR6_LENSING_PATH_WEIGHT_AUTHORIZED_REPLAY_RUN "
        f"verdict={verdict} candidate_chi2={candidate['chi2_act_path']}"
    )


if __name__ == "__main__":
    main()
