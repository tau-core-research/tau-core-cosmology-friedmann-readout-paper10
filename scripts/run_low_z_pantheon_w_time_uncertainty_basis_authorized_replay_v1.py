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
RUN_TEMPLATE = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_run_template_v1.csv"
AUTH_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_v1_summary.csv"
DESIGN = ROOT / "data/derived/pantheon_void_web_source_native_design_matrix_v1.csv"
W_TIME = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv"
GRID = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_grid.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_authorized_replay_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_authorized_replay_permission_only_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"required input is missing: {path.relative_to(ROOT)}")
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
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_low_z_design_and_wtime() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    design_rows = read_rows(DESIGN)
    w_rows = read_rows(W_TIME)
    by_key = {(row["CID"], row["source_row_index"]): row for row in w_rows}
    positions: list[int] = []
    z_values: list[float] = []
    mu_values: list[float] = []
    w_values: list[float] = []
    for idx, row in enumerate(design_rows):
        key = (row["CID"], row["source_row_index"])
        if key not in by_key:
            continue
        w_row = by_key[key]
        if row["zHD"] != w_row["zHD"]:
            raise SystemExit(f"z mismatch for {key}")
        positions.append(idx)
        z_values.append(float(row["zHD"]))
        mu_values.append(float(row["MU_SH0ES"]))
        w_values.append(float(w_row["W_time_uncertainty_basis_candidate"]))
    if len(positions) != 424:
        raise SystemExit(f"expected 424 W_time low-z rows, got {len(positions)}")
    return (
        np.array(z_values, dtype=float),
        np.array(mu_values, dtype=float),
        np.array(w_values, dtype=float),
        np.array(positions, dtype=int),
    )


def low_z_covariance(positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(positions, positions)]


def active_basis_for_branch(w_time: np.ndarray, branch: str) -> np.ndarray:
    if branch in {"candidate", "off"}:
        return w_time
    if branch == "wrong_sign":
        return -w_time
    if branch == "deterministic_shuffle":
        rng = np.random.default_rng(20260610 + len(w_time))
        return w_time[rng.permutation(len(w_time))]
    if branch == "rank_reverse":
        order = np.argsort(w_time)
        reversed_values = np.array(w_time, copy=True)
        reversed_values[order] = w_time[order[::-1]]
        return reversed_values
    raise SystemExit(f"unknown W_time branch: {branch}")


def best(rows: list[dict[str, str]], branch: str | None = None) -> dict[str, str]:
    scope = rows if branch is None else [row for row in rows if row["branch"] == branch]
    if not scope:
        raise SystemExit(f"missing replay branch: {branch}")
    return min(scope, key=lambda row: float(row["chi2_w_time_replay"]))


def main() -> None:
    run = read_one(RUN_TEMPLATE)
    auth = read_one(AUTH_SUMMARY)
    if run["status"] != "W_TIME_UNCERTAINTY_BASIS_REPLAY_RUN_PREPARED_AUTH_REQUIRED_NOT_VALIDATION":
        raise SystemExit("W_time replay run template status mismatch")
    if auth["decision"] != "GO_W_TIME_UNCERTAINTY_BASIS_REPLAY_PERMISSION_ONLY":
        raise SystemExit("W_time replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization summary must be permission-only and non-validation")
    if auth["physical_validation_claimed"] != "false":
        raise SystemExit("authorization must not claim physical validation")
    for marker in [
        "distance_residual_driven_activation",
        "late_time_fit_parameter_selection",
        "posthoc_hz_smoothing",
        "posthoc_clock_anomaly_labels",
        "posthoc_time_channel_selection",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    z, mu, w_time, positions = load_low_z_design_and_wtime()
    cov = low_z_covariance(positions)
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite inverse-ones vector")

    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_time_grid = parse_range(run["omega_time_grid"])
    zeros = np.zeros_like(w_time)
    rows: list[dict[str, str]] = []

    def add_row(branch: str, omega_m: float, omega_time: float) -> None:
        if branch == "baseline_only":
            active = zeros
            omega_eff = 0.0
            mode = "baseline"
            k_eff = 2
        elif branch == "off":
            active = w_time
            omega_eff = 0.0
            mode = "web_only"
            k_eff = 2
        else:
            active = active_basis_for_branch(w_time, branch)
            omega_eff = omega_time
            mode = "web_only"
            k_eff = 3
        model = distance_modulus_void_web(z, omega_m, 0.0, omega_eff, zeros, active, mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        rows.append(
            {
                "run_id": run["run_id"],
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_time": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_w_time_replay": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_w_time_replay": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for omega_m in omega_m_grid:
        add_row("baseline_only", omega_m, 0.0)
        add_row("off", omega_m, 0.0)
        for omega_time in omega_time_grid:
            add_row("candidate", omega_m, omega_time)
            add_row("wrong_sign", omega_m, omega_time)
            add_row("deterministic_shuffle", omega_m, omega_time)
            add_row("rank_reverse", omega_m, omega_time)
    write_csv(GRID, rows)

    baseline = best([row for row in rows if row["branch"] == "baseline_only"])
    candidate = best(rows, "candidate")
    controls = [best(rows, branch) for branch in ["off", "wrong_sign", "deterministic_shuffle", "rank_reverse"]]
    best_control = min(controls, key=lambda row: float(row["chi2_w_time_replay"]))
    better_controls = [
        row for row in controls if float(row["chi2_w_time_replay"]) < float(candidate["chi2_w_time_replay"])
    ]
    summary = [
        {
            "run_id": run["run_id"],
            "status": "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION",
            "authorization_decision": auth["decision"],
            "active_channel_family": run["active_channel_family"],
            "n_rows": str(len(z)),
            "grid_rows": str(len(rows)),
            "baseline_best_chi2_w_time_replay": baseline["chi2_w_time_replay"],
            "baseline_best_aic_w_time_replay": baseline["aic_w_time_replay"],
            "candidate_best_chi2_w_time_replay": candidate["chi2_w_time_replay"],
            "candidate_best_aic_w_time_replay": candidate["aic_w_time_replay"],
            "candidate_best_omega_m": candidate["omega_m"],
            "candidate_best_omega_time": candidate["omega_time"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2_w_time_replay": best_control["chi2_w_time_replay"],
            "best_control_aic_w_time_replay": best_control["aic_w_time_replay"],
            "delta_chi2_candidate_minus_baseline": f"{float(candidate['chi2_w_time_replay']) - float(baseline['chi2_w_time_replay']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(candidate['aic_w_time_replay']) - float(baseline['aic_w_time_replay']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(candidate['chi2_w_time_replay']) - float(best_control['chi2_w_time_replay']):.12g}",
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "family_survives_controls": "true" if not better_controls else "false",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "disabled_channels": run["disabled_channels"],
            "covariance_regularization": "none_positive_definite_cholesky_low_z_submatrix",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "w_time_permission_replay_control_survives_not_validation"
            if not better_controls
            else "w_time_permission_replay_not_control_resistant_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_AUTHORIZED_REPLAY_V1_BUILT "
        f"verdict={summary[0]['verdict']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']}"
    )


if __name__ == "__main__":
    main()
