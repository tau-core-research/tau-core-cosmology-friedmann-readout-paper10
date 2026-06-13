#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_readout_shape_observable_gate_policy_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
BAO_COV = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
HIGH_Z_AUDIT = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_readout_shape_observable_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
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


def covariance_from_rows(rows: list[dict[str, str]], allowed: list[int]) -> np.ndarray:
    index = {radial: i for i, radial in enumerate(allowed)}
    cov = np.zeros((len(allowed), len(allowed)), dtype=float)
    for row in rows:
        i = int(row["row_i"])
        j = int(row["row_j"])
        if i in index and j in index:
            cov[index[i], index[j]] = float(row["cov_minus_log_DH_over_rs"])
    return cov


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad shape observable gate claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    high_z = one_row(HIGH_Z_AUDIT)
    if high_z["high_z_row_can_enter_replay"] != "false":
        raise SystemExit("shape gate expects high-z row to remain outside replay")

    cc_rows_all = read_rows(CC_MATCH)
    allowed_rows = [row for row in cc_rows_all if row["cc_support_status"] == "MATCHED_WITHIN_CC_RANGE"]
    allowed_rows = sorted(allowed_rows, key=lambda row: int(row["radial_index"]))
    allowed = [int(row["radial_index"]) for row in allowed_rows]
    if allowed != [0, 1, 2, 3, 4]:
        raise SystemExit("shape gate expects the first five CC-matched DESI rows")

    z = np.array([float(row["z_eff"]) for row in allowed_rows], dtype=float)
    y_bao = np.array([float(row["minus_log_DH_over_rs"]) for row in allowed_rows], dtype=float)
    logh = np.array([float(row["nearest_cc_logH"]) for row in allowed_rows], dtype=float)
    sigma_logh = np.array([float(row["nearest_cc_sigma_logH"]) for row in allowed_rows], dtype=float)
    beta_like = y_bao - logh
    cov = covariance_from_rows(read_rows(BAO_COV), allowed) + np.diag(sigma_logh**2)

    records: list[dict[str, str]] = []
    # Adjacent first differences remove the constant beta_rd nuisance.
    first_matrix = np.zeros((len(z) - 1, len(z)), dtype=float)
    for i in range(len(z) - 1):
        dz = z[i + 1] - z[i]
        first_matrix[i, i] = -1.0 / dz
        first_matrix[i, i + 1] = 1.0 / dz
    first_values = first_matrix @ beta_like
    first_cov = first_matrix @ cov @ first_matrix.T
    first_sigma = np.sqrt(np.diag(first_cov))
    for i, value in enumerate(first_values):
        records.append(
            {
                "gate_id": policy["gate_id"],
                "observable_family": "adjacent_first_difference_beta_shape",
                "shape_row": str(i),
                "radial_index_left": str(allowed[i]),
                "radial_index_right": str(allowed[i + 1]),
                "z_left": f"{z[i]:.12g}",
                "z_right": f"{z[i + 1]:.12g}",
                "z_mid": f"{0.5 * (z[i] + z[i + 1]):.12g}",
                "delta_z": f"{z[i + 1] - z[i]:.12g}",
                "shape_value": f"{value:.12g}",
                "shape_sigma_diag": f"{first_sigma[i]:.12g}",
                "shape_abs_snr_diag": f"{abs(value) / first_sigma[i]:.12g}" if first_sigma[i] > 0 else "nan",
                "constant_beta_nuisance_removed": "true",
                "high_z_row_included": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    # Uneven-grid second derivative proxy from adjacent slopes.
    second_matrix = []
    for i in range(len(z) - 2):
        dz_left = z[i + 1] - z[i]
        dz_right = z[i + 2] - z[i + 1]
        span = z[i + 2] - z[i]
        row = np.zeros(len(z), dtype=float)
        row[i] = 2.0 / (span * dz_left)
        row[i + 1] = -2.0 * (1.0 / dz_left + 1.0 / dz_right) / span
        row[i + 2] = 2.0 / (span * dz_right)
        second_matrix.append(row)
    second_matrix_arr = np.array(second_matrix)
    second_values = second_matrix_arr @ beta_like
    second_cov = second_matrix_arr @ cov @ second_matrix_arr.T
    second_sigma = np.sqrt(np.diag(second_cov))
    for i, value in enumerate(second_values):
        records.append(
            {
                "gate_id": policy["gate_id"],
                "observable_family": "second_difference_curvature_shape",
                "shape_row": str(i),
                "radial_index_left": str(allowed[i]),
                "radial_index_right": str(allowed[i + 2]),
                "z_left": f"{z[i]:.12g}",
                "z_right": f"{z[i + 2]:.12g}",
                "z_mid": f"{z[i + 1]:.12g}",
                "delta_z": f"{z[i + 2] - z[i]:.12g}",
                "shape_value": f"{value:.12g}",
                "shape_sigma_diag": f"{second_sigma[i]:.12g}",
                "shape_abs_snr_diag": f"{abs(value) / second_sigma[i]:.12g}" if second_sigma[i] > 0 else "nan",
                "constant_beta_nuisance_removed": "true",
                "high_z_row_included": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, records)

    first_rank = int(np.linalg.matrix_rank(first_cov))
    second_rank = int(np.linalg.matrix_rank(second_cov))
    first_max_snr = max(float(row["shape_abs_snr_diag"]) for row in records if row["observable_family"] == "adjacent_first_difference_beta_shape")
    second_max_snr = max(float(row["shape_abs_snr_diag"]) for row in records if row["observable_family"] == "second_difference_curvature_shape")
    summary = [
        {
            "gate_id": policy["gate_id"],
            "status": "DESI_TIME_READOUT_SHAPE_OBSERVABLE_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION",
            "input_cc_matched_rows": str(len(allowed)),
            "high_z_row_included": "false",
            "constant_beta_nuisance_removed": "true",
            "first_difference_rows": str(len(first_values)),
            "second_difference_rows": str(len(second_values)),
            "first_difference_cov_rank": str(first_rank),
            "second_difference_cov_rank": str(second_rank),
            "first_difference_max_abs_snr_diag": f"{first_max_snr:.12g}",
            "second_difference_max_abs_snr_diag": f"{second_max_snr:.12g}",
            "shape_observable_candidate_available": "true",
            "endpoint_ready_shape_observable": "false",
            "blocks_endpoint_reason": "source_side_shape_exists_but_uses_only_5row_nearest_CC_scope_and_high_z_clock_support_missing",
            "next_primary_gate": "multi_clock_support_per_BAO_row_or_independent_shape_review",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_time_readout_shape_candidate_frozen_but_not_endpoint_ready",
        }
    ]
    if not math.isfinite(first_max_snr) or not math.isfinite(second_max_snr):
        raise SystemExit("non-finite shape diagnostic value")
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()
