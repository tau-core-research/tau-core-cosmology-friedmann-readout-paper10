#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_candidate_policy_v1.csv"
ROWS = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1.csv"
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(ROWS)
    summary = read_one(SUMMARY)
    require(policy["status"] == "W_TIME_UNCERTAINTY_BASIS_CANDIDATE_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(summary["status"] == "W_TIME_UNCERTAINTY_BASIS_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING", "bad status")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(float(summary["source_normalization_std"]) > 0.0, "normalization std must be positive")
    require(float(summary["W_time_min"]) < float(summary["W_time_max"]), "W_time range must be nondegenerate")
    require(abs(float(summary["W_time_mean"])) < 1e-10, "source-normalized W_time basis should have zero mean")
    require(summary["W_time_values_computed"] == "true", "W_time basis values should be computed")
    require(
        summary["W_time_values_status"] == "SOURCE_SIDE_BASIS_CANDIDATE_ONLY_NOT_ENDPOINT",
        "bad W_time status",
    )
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized",
        "bad verdict",
    )
    for row in rows:
        float(row["W_time_uncertainty_basis_candidate"])
        require(
            row["W_time_candidate_interpretation"] == "source_normalized_CC_uncertainty_readout_basis_not_endpoint",
            "bad interpretation",
        )
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_late_time_fit_parameters"] == "false", "row must not contain late-time fits")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_posthoc_hz_smoothing"] == "false", "row must not use posthoc smoothing")
        require(row["uses_posthoc_clock_anomaly_labels"] == "false", "row must not use clock labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_CANDIDATE_VALIDATED "
        f"rows={summary['rows']} "
        f"W_time_range=[{summary['W_time_min']},{summary['W_time_max']}] "
        "endpoint=false"
    )


if __name__ == "__main__":
    main()
