#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1.csv"
SUMMARY = ROOT / "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1_summary.csv"
CLAIM_BOUNDARY = "time_readout_clock_rate_phase_cc_support_candidate_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["status"] == "TIME_READOUT_CLOCK_RATE_PHASE_CC_SUPPORT_CANDIDATE_BUILT_SOURCE_SIDE_NOT_SCORING", "bad status")
    require(summary["input_design_rows"] == "1371", "unexpected design row count")
    require(summary["included_rows"] == "1370", "expected 1370 rows within CC upper support")
    require(summary["excluded_above_cc_support_rows"] == "1", "expected one row above CC support")
    require(summary["used_cc_bin_count"] == "31", "expected 31 nearest-neighbor CC support bins to be used")
    require(len(rows) == int(summary["included_rows"]), "row count mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "candidate must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "candidate must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "candidate must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
        require(row["endpoint_replay_allowed"] == "false", "row must not allow endpoint replay")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "row must not contain distance residuals")
    print(
        "PAPER10_CLOCK_RATE_PHASE_CC_SUPPORT_CANDIDATE_VALIDATED "
        f"rows={summary['included_rows']} used_cc_bins={summary['used_cc_bin_count']}"
    )


if __name__ == "__main__":
    main()
