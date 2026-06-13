#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DETAIL = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_clock_rate_phase_rank_control_audit_v1_summary.csv"
CLAIM_BOUNDARY = "clock_rate_phase_rank_control_audit_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    detail = read_rows(DETAIL)
    summary_rows = read_rows(SUMMARY)
    require(len(detail) == 3, f"expected 3 detail rows, got {len(detail)}")
    require(len(summary_rows) == 1, f"expected one summary row, got {len(summary_rows)}")
    summary = summary_rows[0]
    require(summary["status"] == "SOURCE_SIDE_DIAGNOSTIC_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["assigned_cc_bin_count"] == "3", "expected the low-z candidate to use three CC bins")
    require(summary["all_families_rank_control_dominated"] == "true", "expected rank-control dominance flag")
    require(summary["endpoint_replay_allowed"] == "false", "audit must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "audit must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "audit must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(
        summary["verdict"] == "low_cc_bin_count_rank_control_dominance_confirmed_not_validation",
        "unexpected audit verdict",
    )
    for row in detail:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad detail claim boundary")
        require(row["assigned_cc_bin_count"] == "3", "expected three CC bins in every row")
        require(int(row["unique_basis_value_count"]) <= 3, "basis should be coarse in this low-z audit")
        require(row["best_local_control_branch"] == "rank_reverse", "expected rank_reverse to be local best control")
        require(row["rank_control_dominance_flag"] == "true", "expected rank-control dominance flag")
    print(
        "PAPER10_CLOCK_RATE_PHASE_RANK_CONTROL_AUDIT_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
