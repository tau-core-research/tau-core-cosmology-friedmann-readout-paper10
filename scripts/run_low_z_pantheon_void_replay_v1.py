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
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_replay_run_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_replay_protocol_v1.csv"
AUTH_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_response_v1_summary.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_grid.csv"


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


def load_low_z_design() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
    design_rows = read_rows(DESIGN)
    mask_rows = read_rows(MASK)
    if len(design_rows) != len(mask_rows):
        raise SystemExit("design/mask row-count mismatch")
    included_positions: list[int] = []
    cids: list[str] = []
    source_indices: list[str] = []
    for i, (design, mask) in enumerate(zip(design_rows, mask_rows, strict=True)):
        if design["CID"] != mask["CID"] or design["source_row_index"] != mask["source_row_index"]:
            raise SystemExit("design/mask row-order mismatch")
        if mask["included"] == "true":
            included_positions.append(i)
            cids.append(design["CID"])
            source_indices.append(design["source_row_index"])
    if not included_positions:
        raise SystemExit("low-z replay mask contains no included rows")
    z = np.array([float(design_rows[i]["zHD"]) for i in included_positions], dtype=float)
    mu = np.array([float(design_rows[i]["MU_SH0ES"]) for i in included_positions], dtype=float)
    w_void = np.array([float(design_rows[i]["W_void_source_native_basis"]) for i in included_positions], dtype=float)
    return z, mu, w_void, np.array(included_positions, dtype=int), cids, source_indices


def low_z_covariance(included_positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(included_positions, included_positions)]


def active_void_for_mode(w_void: np.ndarray, mode: str, seed: int) -> np.ndarray:
    if mode in {"void_only", "zero_void_amplitude"}:
        return w_void
    if mode == "wrong_void_sign":
        return -w_void
    if mode == "wrong_void_threshold":
        positives = w_void[w_void > 0.0]
        if positives.size == 0:
            return np.zeros_like(w_void)
        threshold = float(np.median(positives))
        return np.where(w_void >= threshold, w_void, 0.0)
    if mode == "shuffled":
        rng = np.random.default_rng(seed + len(w_void))
        return w_void[rng.permutation(len(w_void))]
    raise SystemExit(f"unknown void mode: {mode}")


def main() -> None:
    run = read_one(RUN_MANIFEST)
    protocol = read_one(PROTOCOL)
    auth = read_one(AUTH_SUMMARY)

    if run["status"] != "LOW_Z_VOID_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("low-z replay run status mismatch")
    if auth["verdict"] != "low_z_void_replay_authorized_permission_only_not_validation":
        raise SystemExit("low-z replay is not authorized")
    if auth["endpoint_run_allowed"] != "true" or auth["physical_validation_claimed"] != "false":
        raise SystemExit("authorization summary must be permission-only and non-validation")
    if protocol["included_channel_families"] != "W_VOID_MATURITY":
        raise SystemExit("low-z protocol must include only W_VOID_MATURITY")
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        if channel not in run["disabled_channels"]:
            raise SystemExit(f"disabled channel missing from run manifest: {channel}")
    for marker in [
        "distance_residual_driven_activation",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    z, mu, w_void, included_positions, cids, source_indices = load_low_z_design()
    cov = low_z_covariance(included_positions)
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite low-z inverse-ones vector")

    baseline_om = parse_range(run["baseline_omega_m_grid"])
    model_om = parse_range(run["void_omega_m_grid"])
    omega_void_grid = parse_range(run["omega_void_grid"])
    seed = int(run["random_seed"])
    zeros = np.zeros_like(w_void)

    grid_rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_void: float, mode: str) -> None:
        if branch == "baseline_only":
            active_void = zeros
            omega_void_eff = 0.0
            k_eff = 2
            model_mode = "baseline"
        else:
            active_void = active_void_for_mode(w_void, mode, seed)
            omega_void_eff = omega_void
            k_eff = 2 if branch == "zero_void_amplitude" else 3
            model_mode = "void_only"
        model = distance_modulus_void_web(z, omega_m, omega_void_eff, 0.0, active_void, zeros, model_mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_void": f"{omega_void_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_lowz_distance": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_lowz": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "low_z_void_replay_permission_only_not_validation",
            }
        )

    for om in baseline_om:
        add_row("baseline_only", om, 0.0, "void_only")
    for om in model_om:
        for ov in omega_void_grid:
            add_row("void_only", om, ov, "void_only")
            add_row("wrong_void_sign", om, ov, "wrong_void_sign")
            add_row("wrong_void_threshold", om, ov, "wrong_void_threshold")
            add_row("deterministic_shuffled_void_within_low_z_mask", om, ov, "shuffled")
        add_row("zero_void_amplitude", om, 0.0, "zero_void_amplitude")

    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_lowz_distance"] != "inf"]
    by_branch: dict[str, list[dict[str, str]]] = {}
    for row in finite:
        by_branch.setdefault(row["branch"], []).append(row)
    best = {branch: min(rows, key=lambda row: float(row["chi2_lowz_distance"])) for branch, rows in by_branch.items()}
    baseline = best["baseline_only"]
    candidate = best["void_only"]
    controls = [
        best["wrong_void_sign"],
        best["wrong_void_threshold"],
        best["deterministic_shuffled_void_within_low_z_mask"],
        best["zero_void_amplitude"],
    ]
    better_controls = [row for row in controls if float(row["chi2_lowz_distance"]) < float(candidate["chi2_lowz_distance"])]
    summary = [
        {
            "run_id": run["run_id"],
            "status": run["status"],
            "authorization_verdict": auth["verdict"],
            "n_rows": str(len(z)),
            "first_source_row_index": source_indices[0],
            "last_source_row_index": source_indices[-1],
            "z_min": f"{float(z.min()):.12g}",
            "z_max": f"{float(z.max()):.12g}",
            "baseline_best_chi2_lowz_distance": baseline["chi2_lowz_distance"],
            "baseline_best_aic_lowz": baseline["aic_lowz"],
            "baseline_best_omega_m": baseline["omega_m"],
            "void_best_chi2_lowz_distance": candidate["chi2_lowz_distance"],
            "void_best_aic_lowz": candidate["aic_lowz"],
            "void_best_omega_m": candidate["omega_m"],
            "void_best_omega_void": candidate["omega_void"],
            "delta_chi2_void_minus_baseline": f"{float(candidate['chi2_lowz_distance']) - float(baseline['chi2_lowz_distance']):.12g}",
            "delta_aic_void_minus_baseline": f"{float(candidate['aic_lowz']) - float(baseline['aic_lowz']):.12g}",
            "wrong_void_sign_best_chi2_lowz_distance": best["wrong_void_sign"]["chi2_lowz_distance"],
            "wrong_void_threshold_best_chi2_lowz_distance": best["wrong_void_threshold"]["chi2_lowz_distance"],
            "shuffled_best_chi2_lowz_distance": best["deterministic_shuffled_void_within_low_z_mask"]["chi2_lowz_distance"],
            "zero_void_amplitude_best_chi2_lowz_distance": best["zero_void_amplitude"]["chi2_lowz_distance"],
            "candidate_rank_by_chi2_among_void_and_controls": str(1 + len(better_controls)),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "active_channels": run["active_channels"],
            "disabled_channels": run["disabled_channels"],
            "covariance_regularization": "none_positive_definite_cholesky_low_z_submatrix",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "physical_validation_claimed": "false",
            "claim_boundary": "low_z_void_replay_permission_only_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_LOW_Z_PANTHEON_VOID_REPLAY_V1_COMPLETE "
        f"n={len(z)} delta_chi2={summary[0]['delta_chi2_void_minus_baseline']} "
        f"rank={summary[0]['candidate_rank_by_chi2_among_void_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
