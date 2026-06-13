#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_candidate_policy_v1.csv"
DELTA_CLOCK = ROOT / "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1.csv"
DELTA_CLOCK_SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_delta_clock_uncertainty_candidate_v1_summary.csv"
OUT = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_candidate_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def population_std(values: list[float], center: float) -> float:
    return math.sqrt(sum((value - center) ** 2 for value in values) / len(values))


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "W_TIME_UNCERTAINTY_BASIS_CANDIDATE_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("W_time basis candidate policy must not authorize replay or validation")
    delta_summary = read_one(DELTA_CLOCK_SUMMARY)
    if delta_summary["verdict"] != "delta_clock_uncertainty_candidate_frozen_but_w_time_missing":
        raise SystemExit("unexpected parent Delta_clock candidate verdict")
    delta_rows = read_rows(DELTA_CLOCK)
    values = [float(row["Delta_clock_uncertainty_candidate"]) for row in delta_rows]
    center = mean(values)
    scale = population_std(values, center)
    if scale <= 0.0:
        raise SystemExit("Delta_clock candidate is degenerate; cannot build W_time basis")

    rows: list[dict[str, str]] = []
    w_values: list[float] = []
    for row in delta_rows:
        delta = float(row["Delta_clock_uncertainty_candidate"])
        w_time = (delta - center) / scale
        w_values.append(w_time)
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_CANDIDATE_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "assigned_cc_bin_index": row["assigned_cc_bin_index"],
                "Delta_clock_uncertainty_candidate": row["Delta_clock_uncertainty_candidate"],
                "W_time_uncertainty_basis_candidate": f"{w_time:.12g}",
                "source_normalization_mean": f"{center:.12g}",
                "source_normalization_std": f"{scale:.12g}",
                "W_time_candidate_interpretation": "source_normalized_CC_uncertainty_readout_basis_not_endpoint",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_late_time_fit_parameters": "false",
                "contains_fit_statistics": "false",
                "uses_posthoc_hz_smoothing": "false",
                "uses_posthoc_clock_anomaly_labels": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_CANDIDATE_V1",
            "status": "W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "source_normalization_mean": f"{center:.12g}",
            "source_normalization_std": f"{scale:.12g}",
            "W_time_min": f"{min(w_values):.12g}",
            "W_time_max": f"{max(w_values):.12g}",
            "W_time_mean": f"{mean(w_values):.12g}",
            "W_time_values_computed": "true",
            "W_time_values_status": "SOURCE_SIDE_BASIS_CANDIDATE_ONLY_NOT_ENDPOINT",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT "
        f"rows={summary[0]['rows']} "
        f"W_time_range=[{summary[0]['W_time_min']},{summary[0]['W_time_max']}] "
        "endpoint=false"
    )


if __name__ == "__main__":
    main()
