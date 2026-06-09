#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import math
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_degeneracy_audit_policy_v1.csv"
DESIGN = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1.csv"
DESIGN_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1_summary.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
PAIR_GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_degeneracy_audit_v1_pair_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv"

BRANCHES = [
    "mask_sample_0",
    "mask_sample_98",
    "mask_sample_195",
    "positive_mask_mean",
    "sign_flip_positive_mean",
]
POSITIVE_BRANCHES = ["mask_sample_98", "mask_sample_195", "positive_mask_mean"]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_covariance() -> np.ndarray:
    if not TARBALL.exists():
        raise SystemExit(f"missing KiDS tarball: {TARBALL}")
    with tarfile.open(TARBALL) as tf:
        member = tf.extractfile(COSEBIS_MEMBER)
        if member is None:
            raise SystemExit("selected COSEBIs FITS member missing from KiDS tarball")
        payload = member.read()
    with fits.open(io.BytesIO(payload)) as hdul:
        cov = np.asarray(hdul["COVMAT"].data, dtype=float)
        if cov.shape != (300, 300):
            raise SystemExit("unexpected KiDS COSEBIs covariance shape")
    return cov


def stable_dot(a: np.ndarray, b: np.ndarray) -> float:
    return math.fsum(float(x) * float(y) for x, y in zip(a, b, strict=True))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = math.sqrt(stable_dot(a, a) * stable_dot(b, b))
    if denom <= 0:
        return math.nan
    return stable_dot(a, b) / denom


def metric_cosine(
    a: np.ndarray, b: np.ndarray, factor: tuple[np.ndarray, bool]
) -> float:
    cinv_a = linalg.cho_solve(factor, a, check_finite=False)
    cinv_b = linalg.cho_solve(factor, b, check_finite=False)
    aa = stable_dot(a, cinv_a)
    bb = stable_dot(b, cinv_b)
    if aa <= 0 or bb <= 0:
        return math.nan
    return stable_dot(a, cinv_b) / math.sqrt(aa * bb)


def normalized_residual(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    denom = stable_dot(b, b)
    if denom <= 0:
        return math.nan, math.nan
    scale = stable_dot(a, b) / denom
    residual = np.linalg.norm(a - scale * b) / max(np.linalg.norm(a), 1e-300)
    return scale, float(residual)


def effective_rank(singular_values: np.ndarray, tolerance: float = 1e-8) -> int:
    if len(singular_values) == 0:
        return 0
    threshold = float(singular_values[0]) * tolerance
    return int(np.sum(singular_values > threshold))


def main() -> None:
    policy = read_one(POLICY)
    design_summary = read_one(DESIGN_SUMMARY)
    design_rows = read_rows(DESIGN)
    if policy["status"] != "PARTIAL_CONTROL_DEGENERACY_AUDIT_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected degeneracy audit policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("degeneracy audit must not enable endpoint scoring")
    if design_summary["branch_set"].split(";")[1:] != BRANCHES:
        raise SystemExit("unexpected design branch order")
    matrix = {
        branch: np.asarray([float(row[branch]) for row in design_rows], dtype=float)
        for branch in BRANCHES
    }
    cov = load_covariance()
    evals = np.linalg.eigvalsh(cov)
    if float(evals.min()) <= 0:
        raise SystemExit("KiDS covariance is not positive definite")
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)

    pair_rows: list[dict[str, str]] = []
    for left_index, left in enumerate(BRANCHES):
        for right_index, right in enumerate(BRANCHES):
            if right_index <= left_index:
                continue
            raw_cos = cosine(matrix[left], matrix[right])
            cov_cos = metric_cosine(matrix[left], matrix[right], factor)
            scale, residual = normalized_residual(matrix[left], matrix[right])
            pair_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "branch_left": left,
                    "branch_right": right,
                    "raw_cosine": f"{raw_cos:.12g}",
                    "covariance_inverse_cosine": f"{cov_cos:.12g}",
                    "least_squares_scale_left_on_right": f"{scale:.12g}",
                    "relative_shape_residual_left_on_right": f"{residual:.12g}",
                    "uses_kids_data_vector_values": "false",
                    "uses_kids_covariance_for_metric_only": "true",
                    "uses_posterior_chains": "false",
                    "uses_posthoc_selection": "false",
                    "endpoint_scoring_allowed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )

    X = np.column_stack([matrix[branch] for branch in BRANCHES])
    positive_X = np.column_stack([matrix[branch] for branch in POSITIVE_BRANCHES])
    singular_values = np.linalg.svd(X, compute_uv=False)
    positive_singular_values = np.linalg.svd(positive_X, compute_uv=False)
    max_positive_shape_residual = max(
        float(row["relative_shape_residual_left_on_right"])
        for row in pair_rows
        if row["branch_left"] in POSITIVE_BRANCHES and row["branch_right"] in POSITIVE_BRANCHES
    )
    min_positive_abs_cov_cosine = min(
        abs(float(row["covariance_inverse_cosine"]))
        for row in pair_rows
        if row["branch_left"] in POSITIVE_BRANCHES and row["branch_right"] in POSITIVE_BRANCHES
    )
    sign_flip = next(
        row
        for row in pair_rows
        if row["branch_left"] == "positive_mask_mean"
        and row["branch_right"] == "sign_flip_positive_mean"
    )
    summary = {
        "policy_id": policy["policy_id"],
        "status": "PARTIAL_CONTROL_DEGENERACY_AUDIT_BUILT_NOT_ENDPOINT_VALIDATION",
        "selected_statistic": policy["selected_statistic"],
        "control_scope": policy["control_scope"],
        "branch_count": str(len(BRANCHES)),
        "positive_branch_count": str(len(POSITIVE_BRANCHES)),
        "raw_effective_rank_tol_1e_minus_8": str(effective_rank(singular_values)),
        "positive_effective_rank_tol_1e_minus_8": str(effective_rank(positive_singular_values)),
        "raw_singular_values": ";".join(f"{value:.12g}" for value in singular_values),
        "positive_singular_values": ";".join(f"{value:.12g}" for value in positive_singular_values),
        "min_positive_abs_covariance_inverse_cosine": f"{min_positive_abs_cov_cosine:.12g}",
        "max_positive_relative_shape_residual": f"{max_positive_shape_residual:.12g}",
        "positive_sign_flip_covariance_inverse_cosine": sign_flip["covariance_inverse_cosine"],
        "branch_degeneracy_detected": "true",
        "endpoint_blocker": "positive_mask_branches_are_effectively_rank_one_partial_control_not_full_path_mapping",
        "recommended_next_action": "replace_three_mask_partial_control_with_non_degenerate_source_frozen_full_route_or_official_geometry_mapping_before_endpoint_scoring",
        "uses_kids_data_vector_values": "false",
        "uses_kids_covariance_for_metric_only": "true",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    PAIR_GRID.parent.mkdir(parents=True, exist_ok=True)
    with PAIR_GRID.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(pair_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pair_rows)
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DEGENERACY_AUDIT_V1_BUILT "
        f"positive_rank={summary['positive_effective_rank_tol_1e_minus_8']} "
        f"min_positive_abs_cov_cos={summary['min_positive_abs_covariance_inverse_cosine']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
