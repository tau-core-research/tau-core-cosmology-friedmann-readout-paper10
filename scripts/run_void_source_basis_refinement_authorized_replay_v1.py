#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from collections import defaultdict
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
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_authorized_replay_run_v1.csv"
AUTH_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_endpoint_replay_authorization_review_response_v1_summary.csv"
)
R5_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv"
R5_VECTORS = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_vectors_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_grid.csv"

CONTROL_COLUMNS = [
    "zero_control",
    "wrong_sign_control",
    "deterministic_row_shuffle_control",
    "threshold_low_control",
    "threshold_high_control",
]


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


def load_low_z_design() -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
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
    return z, mu, np.array(included_positions, dtype=int), cids, source_indices


def low_z_covariance(included_positions: np.ndarray) -> np.ndarray:
    full_cov = load_covariance(retained_indices())
    return full_cov[np.ix_(included_positions, included_positions)]


def load_source_vectors(source_indices: list[str]) -> dict[str, dict[str, np.ndarray]]:
    rows = read_rows(R5_VECTORS)
    by_feature: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        by_feature[row["feature_id"]][row["source_row_index"]] = row
    vectors: dict[str, dict[str, np.ndarray]] = {}
    for feature_id, feature_rows in by_feature.items():
        missing = [idx for idx in source_indices if idx not in feature_rows]
        if missing:
            raise SystemExit(f"{feature_id} missing low-z source rows: {missing[:5]}")
        vectors[feature_id] = {
            "candidate_source_feature": np.array(
                [float(feature_rows[idx]["candidate_source_feature"]) for idx in source_indices], dtype=float
            )
        }
        for control in CONTROL_COLUMNS:
            vectors[feature_id][control] = np.array([float(feature_rows[idx][control]) for idx in source_indices], dtype=float)
    if not vectors:
        raise SystemExit("no R5 source vectors found")
    return vectors


def main() -> None:
    run = read_one(RUN_MANIFEST)
    auth = read_one(AUTH_SUMMARY)
    r5 = read_one(R5_SUMMARY)

    if run["status"] != "REFINED_VOID_REPLAY_AUTHORIZED_PERMISSION_ONLY_NOT_VALIDATION":
        raise SystemExit("refined replay run status mismatch")
    if auth["verdict"] != "refined_void_replay_authorized_permission_only_not_validation":
        raise SystemExit("refined void replay is not authorized")
    if auth["endpoint_replay_allowed"] != "true" or auth["endpoint_validation_claimed"] != "false":
        raise SystemExit("authorization summary must be permission-only and non-validation")
    if r5["control_resistance_preflight_complete"] != "true":
        raise SystemExit("R5 control-resistance preflight must be complete")
    for marker in [
        "distance_residual_driven_activation",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_source_basis_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        if marker not in run["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    z, mu, included_positions, cids, source_indices = load_low_z_design()
    source_vectors = load_source_vectors(source_indices)
    cov = low_z_covariance(included_positions)
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    if not np.isfinite(cinv_ones).all():
        raise SystemExit("non-finite low-z inverse-ones vector")

    omega_m_grid = parse_range(run["omega_m_grid"])
    omega_source_grid = parse_range(run["omega_source_grid"])
    zeros = np.zeros_like(mu)
    grid_rows: list[dict[str, str]] = []

    def add_row(feature_id: str, branch: str, omega_m: float, omega_source: float, active_source: np.ndarray) -> None:
        if branch == "baseline_only":
            omega_eff = 0.0
            vector = zeros
            k_eff = 2
            mode = "baseline"
        else:
            omega_eff = omega_source
            vector = active_source
            k_eff = 2 if branch == "zero_control" else 3
            mode = "void_only"
        model = distance_modulus_void_web(z, omega_m, omega_eff, 0.0, vector, zeros, mode)
        chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
        aic = chi2 + 2 * k_eff if math.isfinite(chi2) else math.inf
        grid_rows.append(
            {
                "run_id": run["run_id"],
                "feature_id": feature_id,
                "branch": branch,
                "omega_m": f"{omega_m:.12g}",
                "omega_source": f"{omega_eff:.12g}",
                "offset": f"{offset:.12g}" if math.isfinite(offset) else "",
                "chi2_lowz_distance": f"{chi2:.12g}" if math.isfinite(chi2) else "inf",
                "aic_lowz": f"{aic:.12g}" if math.isfinite(aic) else "inf",
                "n_rows": str(len(z)),
                "k_eff": str(k_eff),
                "claim_boundary": "void_source_basis_refinement_authorized_replay_permission_only_not_validation",
            }
        )

    for om in omega_m_grid:
        add_row("NONE", "baseline_only", om, 0.0, zeros)
    for feature_id, vectors in source_vectors.items():
        for om in omega_m_grid:
            for osrc in omega_source_grid:
                add_row(feature_id, "candidate_source_feature", om, osrc, vectors["candidate_source_feature"])
                for control in CONTROL_COLUMNS:
                    add_row(feature_id, control, om, osrc, vectors[control])

    write_csv(GRID, grid_rows)

    finite = [row for row in grid_rows if row["chi2_lowz_distance"] != "inf"]
    by_branch: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in finite:
        by_branch[(row["feature_id"], row["branch"])].append(row)
    best = {key: min(rows, key=lambda row: float(row["chi2_lowz_distance"])) for key, rows in by_branch.items()}
    baseline = best[("NONE", "baseline_only")]
    candidates = [row for key, row in best.items() if key[1] == "candidate_source_feature"]
    controls = [row for key, row in best.items() if key[1] in CONTROL_COLUMNS]
    best_candidate = min(candidates, key=lambda row: float(row["chi2_lowz_distance"]))
    better_controls = [row for row in controls if float(row["chi2_lowz_distance"]) < float(best_candidate["chi2_lowz_distance"])]
    better_or_equal_controls = [
        row for row in controls if float(row["chi2_lowz_distance"]) <= float(best_candidate["chi2_lowz_distance"])
    ]
    best_control = min(controls, key=lambda row: float(row["chi2_lowz_distance"]))

    summary = [
        {
            "run_id": run["run_id"],
            "status": run["status"],
            "authorization_verdict": auth["verdict"],
            "n_rows": str(len(z)),
            "feature_count": str(len(source_vectors)),
            "control_family_count": str(len(CONTROL_COLUMNS)),
            "grid_rows": str(len(grid_rows)),
            "first_source_row_index": source_indices[0],
            "last_source_row_index": source_indices[-1],
            "z_min": f"{float(z.min()):.12g}",
            "z_max": f"{float(z.max()):.12g}",
            "baseline_best_chi2_lowz_distance": baseline["chi2_lowz_distance"],
            "baseline_best_aic_lowz": baseline["aic_lowz"],
            "baseline_best_omega_m": baseline["omega_m"],
            "best_candidate_feature_id": best_candidate["feature_id"],
            "best_candidate_chi2_lowz_distance": best_candidate["chi2_lowz_distance"],
            "best_candidate_aic_lowz": best_candidate["aic_lowz"],
            "best_candidate_omega_m": best_candidate["omega_m"],
            "best_candidate_omega_source": best_candidate["omega_source"],
            "best_control_feature_id": best_control["feature_id"],
            "best_control_branch": best_control["branch"],
            "best_control_chi2_lowz_distance": best_control["chi2_lowz_distance"],
            "best_control_aic_lowz": best_control["aic_lowz"],
            "delta_chi2_candidate_minus_baseline": f"{float(best_candidate['chi2_lowz_distance']) - float(baseline['chi2_lowz_distance']):.12g}",
            "delta_aic_candidate_minus_baseline": f"{float(best_candidate['aic_lowz']) - float(baseline['aic_lowz']):.12g}",
            "delta_chi2_candidate_minus_best_control": f"{float(best_candidate['chi2_lowz_distance']) - float(best_control['chi2_lowz_distance']):.12g}",
            "candidate_rank_by_chi2_among_candidate_and_controls": str(1 + len(better_controls)),
            "controls_better_than_candidate_chi2": str(len(better_controls)),
            "controls_better_or_equal_candidate_chi2": str(len(better_or_equal_controls)),
            "active_channel_family": run["active_channel_family"],
            "disabled_channels": run["disabled_channels"],
            "covariance_regularization": "none_positive_definite_cholesky_low_z_submatrix",
            "covariance_min_eigenvalue": f"{min_eval:.12g}",
            "covariance_condition_number": f"{condition_number:.12g}",
            "endpoint_replay_allowed": "true",
            "endpoint_validation_claimed": "false",
            "claim_boundary": "void_source_basis_refinement_authorized_replay_permission_only_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_AUTHORIZED_REPLAY_V1_COMPLETE "
        f"n={len(z)} best_feature={summary[0]['best_candidate_feature_id']} "
        f"delta_chi2_baseline={summary[0]['delta_chi2_candidate_minus_baseline']} "
        f"rank={summary[0]['candidate_rank_by_chi2_among_candidate_and_controls']} "
        "claim_boundary=permission_only_not_validation"
    )


if __name__ == "__main__":
    main()
