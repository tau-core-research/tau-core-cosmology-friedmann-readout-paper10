#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import math
import random
import tarfile
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy import linalg


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_family_geometry_audit_policy_v1.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
REPLAY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1.csv"
TARBALL = ROOT / "data" / "raw" / "weak_lensing" / "kids1000" / "KiDS1000_cosmic_shear_data_release.tgz"
COSEBIS_MEMBER = (
    "KiDS1000_cosmis_shear_data_release/data_fits/"
    "cosebis_KIDS1000_BlindC_with_m_bias_V1.0.0A_ugriZYJHKs_photoz_SG_mask_LF_svn_309c_2Dbins_v2_goldclasses_Flag_SOM_Fid.fits"
)
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_family_geometry_audit_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def digest(values: np.ndarray) -> str:
    import hashlib

    payload = "\n".join(f"{float(value):.12e}" for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


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


def effective_rank(singular_values: np.ndarray, tolerance: float = 1e-8) -> int:
    if len(singular_values) == 0:
        return 0
    threshold = float(singular_values[0]) * tolerance
    return int(np.sum(singular_values > threshold))


def vector_stats(values: np.ndarray) -> dict[str, str]:
    mean = float(np.mean(values))
    std = float(np.std(values))
    return {
        "vector_mean": f"{mean:.12e}",
        "vector_std": f"{std:.12e}",
        "vector_l2_norm": f"{float(np.linalg.norm(values)):.12e}",
        "vector_min": f"{float(np.min(values)):.12e}",
        "vector_max": f"{float(np.max(values)):.12e}",
        "vector_sha256": digest(values),
    }


def build_control_vectors(theory_rows: list[dict[str, str]], replay_rows: list[dict[str, str]]) -> list[tuple[dict[str, str], np.ndarray]]:
    theory_rows = sorted(theory_rows, key=lambda row: int(row["row_index_zero_based"]))
    base_values = np.asarray([float(row["theory_value"]) for row in theory_rows], dtype=float)
    pair_order: list[str] = []
    for row in theory_rows:
        if row["pair_id"] not in pair_order:
            pair_order.append(row["pair_id"])
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): float(row["theory_value"]) for row in theory_rows
    }
    vectors: list[tuple[dict[str, str], np.ndarray]] = [
        (
            {
                "family": "candidate",
                "draw_index": "0",
                "operator": "source_frozen_candidate",
                "seed": "0",
            },
            base_values,
        )
    ]
    for replay in replay_rows:
        family = replay["control_family"]
        draw = int(replay["control_draw_index_zero_based"])
        seed = int(replay["seed"])
        if family == "sky_rotation":
            shift = (draw + 1) % len(pair_order)
            rotated = pair_order[shift:] + pair_order[:shift]
            pair_map = dict(zip(pair_order, rotated))
            values = np.asarray(
                [by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
                dtype=float,
            )
        elif family == "tomographic_pair_shuffle":
            rng = random.Random(seed + draw)
            shuffled = pair_order[:]
            rng.shuffle(shuffled)
            pair_map = dict(zip(pair_order, shuffled))
            values = np.asarray(
                [by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows],
                dtype=float,
            )
        elif family == "wrong_channel_activation":
            values = np.zeros_like(base_values)
        elif family == "web_path_sign_flip":
            values = -base_values if draw == 0 else np.zeros_like(base_values)
        else:
            raise SystemExit(f"unexpected control family: {family}")
        vectors.append(
            (
                {
                    "family": family,
                    "draw_index": replay["control_draw_index_zero_based"],
                    "operator": replay["operator"],
                    "seed": replay["seed"],
                },
                values,
            )
        )
    return vectors


def main() -> None:
    policy = read_one(POLICY)
    theory_rows = read_rows(THEORY)
    replay_rows = read_rows(REPLAY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint-family geometry audit must remain endpoint disabled")
    if any(row["uses_kids_data_vector_values"] != "false" for row in replay_rows):
        raise SystemExit("null-control replay must not use KiDS data-vector values")
    if any(row["contains_control_scores"] != "false" for row in replay_rows):
        raise SystemExit("null-control replay must not contain scores")

    vectors = build_control_vectors(theory_rows, replay_rows)
    matrix = np.column_stack([values for _, values in vectors if np.linalg.norm(values) > 0])
    raw_singular = np.linalg.svd(matrix, compute_uv=False)
    cov = load_covariance()
    evals = np.linalg.eigvalsh(cov)
    if float(evals.min()) <= 0:
        raise SystemExit("KiDS covariance is not positive definite")
    factor = linalg.cho_factor(cov, lower=True, check_finite=True)
    whitened = linalg.solve_triangular(factor[0], matrix, lower=factor[1], check_finite=False)
    cov_singular = np.linalg.svd(whitened, compute_uv=False)
    raw_rank = effective_rank(raw_singular)
    cov_rank = effective_rank(cov_singular)
    min_rank = min(raw_rank, cov_rank)

    out_rows: list[dict[str, str]] = []
    for index, (meta, values) in enumerate(vectors, start=1):
        row = {
            "policy_id": policy["policy_id"],
            "selected_statistic": policy["selected_statistic"],
            "family_vector_index_one_based": str(index),
            "vector_family": meta["family"],
            "draw_index_zero_based": meta["draw_index"],
            "operator": meta["operator"],
            "seed": meta["seed"],
            "target_rows": str(len(values)),
            "is_zero_vector": str(bool(np.linalg.norm(values) == 0.0)).lower(),
            "contains_theory_vector": "true",
            "contains_control_scores": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "uses_kids_data_vector_values": "false",
            "uses_kids_covariance_for_metric_only": "true",
            "uses_posterior_chains": "false",
            "uses_posthoc_selection": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
        row.update(vector_stats(values))
        out_rows.append(row)

    passed = min_rank >= int(policy["minimum_effective_rank"])
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_BUILT_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "geometry_scope": policy["geometry_scope"],
        "family_vector_count": str(len(out_rows)),
        "nonzero_family_vector_count": str(matrix.shape[1]),
        "target_rows": "300",
        "minimum_effective_rank": policy["minimum_effective_rank"],
        "raw_effective_rank_tol_1e_minus_8": str(raw_rank),
        "covariance_metric_effective_rank_tol_1e_minus_8": str(cov_rank),
        "endpoint_family_geometry_passed": str(passed).lower(),
        "raw_singular_values_top10": ";".join(f"{value:.12g}" for value in raw_singular[:10]),
        "covariance_metric_singular_values_top10": ";".join(f"{value:.12g}" for value in cov_singular[:10]),
        "contains_theory_vector": "true",
        "contains_control_scores": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_kids_covariance_for_metric_only": "true",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_FAMILY_GEOMETRY_AUDIT_V1_BUILT "
        f"raw_rank={raw_rank} cov_rank={cov_rank} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
