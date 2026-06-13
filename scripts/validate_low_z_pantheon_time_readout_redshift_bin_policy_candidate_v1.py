#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_redshift_bin_policy_candidate_policy_v1.csv"
ROWS = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_redshift_bin_policy_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_redshift_bin_policy_candidate_source_side_not_scoring_not_validation"


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


def parse_upper(value: str) -> float:
    return math.inf if value == "inf" else float(value)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(ROWS)
    summary = read_one(SUMMARY)
    require(policy["status"] == "TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(summary["status"] == "TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING", "bad status")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(int(summary["used_cc_bin_count"]) >= 1, "expected at least one used CC bin")
    require(float(summary["delta_clock_star_candidate"]) > 0.0, "clock scale candidate should be positive")
    require(summary["delta_clock_values_computed"] == "false", "Delta_clock values must not be computed")
    require(summary["W_time_values_computed"] == "false", "W_time values must not be computed")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "redshift_bin_policy_candidate_frozen_but_delta_clock_and_w_time_missing",
        "bad verdict",
    )
    for row in rows:
        z = float(row["zHD"])
        lower = float(row["assigned_cc_bin_lower_z"])
        upper = parse_upper(row["assigned_cc_bin_upper_z"])
        require(lower <= z < upper, "source redshift must be inside assigned CC support cell")
        require(float(row["nearest_cc_hz_delta_z"]) >= 0.0, "nearest CC delta must be nonnegative")
        require(float(row["nearest_sdss_bao_rsd_delta_z"]) >= 0.0, "nearest SDSS delta must be nonnegative")
        require(row["delta_clock_value_status"] == "NOT_COMPUTED_BIN_POLICY_ONLY", "Delta_clock must stay uncomputed")
        require(row["W_time_value_status"] == "NOT_COMPUTED_BIN_POLICY_ONLY", "W_time must stay uncomputed")
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_late_time_fit_parameters"] == "false", "row must not contain late-time fits")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_posthoc_hz_smoothing"] == "false", "row must not use posthoc smoothing")
        require(row["uses_posthoc_clock_anomaly_labels"] == "false", "row must not use clock labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_TIME_READOUT_REDSHIFT_BIN_POLICY_CANDIDATE_VALIDATED "
        f"rows={summary['rows']} used_cc_bins={summary['used_cc_bin_count']} "
        "w_time=false"
    )


if __name__ == "__main__":
    main()
