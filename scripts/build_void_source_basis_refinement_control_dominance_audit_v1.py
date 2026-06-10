#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import linalg, stats

try:
    from run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from run_pantheon_pilot_scoring_v1 import load_covariance, read_one, retained_indices
    from run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web
except ImportError:
    from scripts.run_pantheon_full_cov_pilot_scoring_v1 import chi2_with_offset, covariance_factor
    from scripts.run_pantheon_pilot_scoring_v1 import load_covariance, read_one, retained_indices
    from scripts.run_pantheon_void_web_proxy_full_cov_pilot_v1 import distance_modulus_void_web


ROOT = Path(__file__).resolve().parents[1]
REPLAY_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_summary.csv"
REPLAY_GRID = ROOT / "data" / "derived" / "void_source_basis_refinement_authorized_replay_v1_grid.csv"
R5_VECTORS = ROOT / "data" / "derived" / "void_source_basis_refinement_r5_control_vectors_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
MASK = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_row_mask.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_control_dominance_audit_v1_summary.csv"
BRANCH_AUDIT = ROOT / "data" / "derived" / "void_source_basis_refinement_control_dominance_audit_v1_branches.csv"


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


def safe_pearson(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return math.nan
    if float(np.std(x[mask])) == 0.0 or float(np.std(y[mask])) == 0.0:
        return math.nan
    return float(np.corrcoef(x[mask], y[mask])[0, 1])


def safe_spearman(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 3:
        return math.nan
    if float(np.std(x[mask])) == 0.0 or float(np.std(y[mask])) == 0.0:
        return math.nan
    result = stats.spearmanr(x[mask], y[mask])
    return float(result.correlation)


def fmt(value: float) -> str:
    if not math.isfinite(value):
        return ""
    return f"{value:.12g}"


def load_low_z_design() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    design_rows = read_rows(DESIGN)
    mask_rows = read_rows(MASK)
    if len(design_rows) != len(mask_rows):
        raise SystemExit("design/mask row-count mismatch")
    included_positions: list[int] = []
    source_indices: list[str] = []
    for i, (design, mask) in enumerate(zip(design_rows, mask_rows, strict=True)):
        if design["CID"] != mask["CID"] or design["source_row_index"] != mask["source_row_index"]:
            raise SystemExit("design/mask row-order mismatch")
        if mask["included"] == "true":
            included_positions.append(i)
            source_indices.append(design["source_row_index"])
    z = np.array([float(design_rows[i]["zHD"]) for i in included_positions], dtype=float)
    mu = np.array([float(design_rows[i]["MU_SH0ES"]) for i in included_positions], dtype=float)
    row_index = np.array([float(design_rows[i]["source_row_index"]) for i in included_positions], dtype=float)
    return z, mu, row_index, np.array(included_positions, dtype=int), source_indices


def load_vector(feature_id: str, branch: str, source_indices: list[str], n: int) -> np.ndarray:
    if feature_id == "NONE" or branch == "baseline_only":
        return np.zeros(n, dtype=float)
    rows = [
        row
        for row in read_rows(R5_VECTORS)
        if row["feature_id"] == feature_id
    ]
    by_source = {row["source_row_index"]: row for row in rows}
    column = "candidate_source_feature" if branch == "candidate_source_feature" else branch
    missing = [idx for idx in source_indices if idx not in by_source]
    if missing:
        raise SystemExit(f"{feature_id}/{branch} missing low-z rows: {missing[:5]}")
    return np.array([float(by_source[idx][column]) for idx in source_indices], dtype=float)


def best_row(feature_id: str, branch: str) -> dict[str, str]:
    rows = [
        row
        for row in read_rows(REPLAY_GRID)
        if row["feature_id"] == feature_id and row["branch"] == branch and row["chi2_lowz_distance"] != "inf"
    ]
    if not rows:
        raise SystemExit(f"missing replay rows for {feature_id}/{branch}")
    return min(rows, key=lambda row: float(row["chi2_lowz_distance"]))


def model_residual(
    z: np.ndarray,
    mu: np.ndarray,
    factor: tuple[np.ndarray, bool],
    cinv_ones: np.ndarray,
    row: dict[str, str],
    vector: np.ndarray,
) -> tuple[np.ndarray, float, float]:
    mode = "baseline" if row["branch"] == "baseline_only" else "void_only"
    omega_source = float(row["omega_source"])
    model = distance_modulus_void_web(z, float(row["omega_m"]), omega_source, 0.0, vector, np.zeros_like(vector), mode)
    chi2, offset = chi2_with_offset(mu, model, factor, cinv_ones)
    residual = mu - model - offset
    return residual, chi2, offset


def main() -> None:
    summary = read_one(REPLAY_SUMMARY)
    z, mu, row_index, included_positions, source_indices = load_low_z_design()
    cov = load_covariance(retained_indices())[np.ix_(included_positions, included_positions)]
    factor, min_eval, condition_number = covariance_factor(cov)
    ones = np.ones_like(mu)
    cinv_ones = linalg.cho_solve(factor, ones, check_finite=False)
    precision_diag = np.diag(linalg.cho_solve(factor, np.eye(len(mu)), check_finite=False))
    covariance_diag = np.diag(cov)

    candidate_feature = summary["best_candidate_feature_id"]
    control_feature = summary["best_control_feature_id"]
    control_branch = summary["best_control_branch"]
    audit_targets = [
        ("baseline_best", "NONE", "baseline_only"),
        ("best_candidate", candidate_feature, "candidate_source_feature"),
        ("best_control", control_feature, control_branch),
    ]

    branch_rows: list[dict[str, str]] = []
    residuals: dict[str, np.ndarray] = {}
    vectors: dict[str, np.ndarray] = {}
    replay_rows: dict[str, dict[str, str]] = {}
    for role, feature_id, branch in audit_targets:
        replay = best_row(feature_id, branch)
        vector = load_vector(feature_id, branch, source_indices, len(z))
        residual, chi2, offset = model_residual(z, mu, factor, cinv_ones, replay, vector)
        residuals[role] = residual
        vectors[role] = vector
        replay_rows[role] = replay
        branch_rows.append(
            {
                "audit_id": "VOID_SOURCE_BASIS_REFINEMENT_CONTROL_DOMINANCE_AUDIT_V1",
                "role": role,
                "feature_id": feature_id,
                "branch": branch,
                "omega_m": replay["omega_m"],
                "omega_source": replay["omega_source"],
                "chi2_lowz_distance": replay["chi2_lowz_distance"],
                "aic_lowz": replay["aic_lowz"],
                "offset": fmt(offset),
                "activation_pearson_zHD": fmt(safe_pearson(vector, z)),
                "activation_spearman_zHD": fmt(safe_spearman(vector, z)),
                "activation_pearson_source_row_index": fmt(safe_pearson(vector, row_index)),
                "activation_spearman_source_row_index": fmt(safe_spearman(vector, row_index)),
                "activation_pearson_covariance_diag": fmt(safe_pearson(vector, covariance_diag)),
                "activation_pearson_precision_diag": fmt(safe_pearson(vector, precision_diag)),
                "residual_rms_mag": fmt(float(np.sqrt(np.mean(residual**2)))),
                "residual_pearson_zHD": fmt(safe_pearson(residual, z)),
                "residual_pearson_source_row_index": fmt(safe_pearson(residual, row_index)),
                "contains_endpoint_residuals": "true",
                "endpoint_validation_claimed": "false",
                "claim_boundary": "post_score_control_dominance_audit_not_validation",
            }
        )

    candidate_chi2 = float(replay_rows["best_candidate"]["chi2_lowz_distance"])
    baseline_chi2 = float(replay_rows["baseline_best"]["chi2_lowz_distance"])
    control_chi2 = float(replay_rows["best_control"]["chi2_lowz_distance"])
    candidate_aic = float(replay_rows["best_candidate"]["aic_lowz"])
    baseline_aic = float(replay_rows["baseline_best"]["aic_lowz"])
    control_aic = float(replay_rows["best_control"]["aic_lowz"])
    control_is_shuffle = control_branch == "deterministic_row_shuffle_control"
    control_low_redshift_leak = max(
        abs(safe_pearson(vectors["best_control"], z)),
        abs(safe_pearson(vectors["best_control"], row_index)),
        abs(safe_spearman(vectors["best_control"], z)),
        abs(safe_spearman(vectors["best_control"], row_index)),
    ) < 0.3
    candidate_improves_chi2 = candidate_chi2 < baseline_chi2
    candidate_loses_aic = candidate_aic > baseline_aic
    control_beats_candidate = control_chi2 < candidate_chi2
    if control_beats_candidate and control_is_shuffle and control_low_redshift_leak:
        verdict = "candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak"
        recommended_next_action = "treat_refined_void_replay_as_weak_negative_and_revisit_source_basis_before_any_new_endpoint"
    elif control_beats_candidate:
        verdict = "candidate_not_control_dominant_control_dominates_requires_artifact_review"
        recommended_next_action = "audit_control_construction_before_any_new_endpoint"
    else:
        verdict = "candidate_survives_best_control_in_this_audit"
        recommended_next_action = "proceed_to_predeclared_robustness_only_if_no_other_blockers"

    summary_rows = [
        {
            "audit_id": "VOID_SOURCE_BASIS_REFINEMENT_CONTROL_DOMINANCE_AUDIT_V1",
            "status": "CONTROL_DOMINANCE_AUDIT_COMPLETE_NOT_VALIDATION",
            "best_candidate_feature_id": candidate_feature,
            "best_control_feature_id": control_feature,
            "best_control_branch": control_branch,
            "candidate_improves_chi2_over_baseline": str(candidate_improves_chi2).lower(),
            "candidate_loses_aic_to_baseline": str(candidate_loses_aic).lower(),
            "best_control_beats_candidate_chi2": str(control_beats_candidate).lower(),
            "best_control_is_row_shuffle": str(control_is_shuffle).lower(),
            "best_control_low_redshift_row_leakage": str(control_low_redshift_leak).lower(),
            "delta_chi2_candidate_minus_baseline": fmt(candidate_chi2 - baseline_chi2),
            "delta_aic_candidate_minus_baseline": fmt(candidate_aic - baseline_aic),
            "delta_chi2_candidate_minus_best_control": fmt(candidate_chi2 - control_chi2),
            "delta_aic_candidate_minus_best_control": fmt(candidate_aic - control_aic),
            "candidate_rank_by_chi2_among_candidate_and_controls": summary["candidate_rank_by_chi2_among_candidate_and_controls"],
            "controls_better_than_candidate_chi2": summary["controls_better_than_candidate_chi2"],
            "contains_endpoint_residuals": "true",
            "uses_endpoint_residuals_for_new_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "verdict": verdict,
            "recommended_next_action": recommended_next_action,
            "claim_boundary": "post_score_control_dominance_audit_not_validation",
            "covariance_min_eigenvalue": fmt(min_eval),
            "covariance_condition_number": fmt(condition_number),
        }
    ]
    write_csv(BRANCH_AUDIT, branch_rows)
    write_csv(SUMMARY, summary_rows)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_CONTROL_DOMINANCE_AUDIT_V1_COMPLETE "
        f"verdict={verdict} delta_chi2_candidate_control={fmt(candidate_chi2 - control_chi2)}"
    )


if __name__ == "__main__":
    main()
