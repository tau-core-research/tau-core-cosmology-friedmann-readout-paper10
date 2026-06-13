#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_time_readout_clock_rate_phase_candidate_policy_v1.csv"
ROWS = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_time_readout_clock_rate_phase_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_clock_rate_phase_candidate_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(ROWS)
    summary = read_one(SUMMARY)
    require(policy["status"] == "TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(summary["status"] == "TIME_READOUT_CLOCK_RATE_PHASE_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING", "bad status")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["used_cc_bin_count"] == "3", "expected three low-z CC bins")
    for key in ["level_scale", "slope_scale", "phase_scale"]:
        require(float(summary[key]) > 0, f"{key} must be positive")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(
        summary["verdict"] == "clock_rate_phase_candidate_frozen_source_side_not_endpoint_authorized",
        "bad verdict",
    )
    for row in rows:
        float(row["W_time_clock_level_basis"])
        float(row["W_time_clock_slope_basis"])
        float(row["W_time_clock_phase_basis"])
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_late_time_fit_parameters"] == "false", "row must not contain fit parameters")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_posthoc_hz_smoothing"] == "false", "row must not use posthoc smoothing")
        require(row["uses_posthoc_clock_anomaly_labels"] == "false", "row must not use anomaly labels")
        require(row["physical_validation_claimed"] == "false", "row must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    print(
        "PAPER10_CLOCK_RATE_PHASE_CANDIDATE_VALIDATED "
        f"rows={summary['rows']} phase_range={summary['phase_basis_range']}"
    )


if __name__ == "__main__":
    main()
