#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1.csv"
SUMMARY = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv"
CLAIM_BOUNDARY = "sdss_bao_time_readout_observable_route_audit_not_validation"


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
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 2, "expected two radial BAO rows")
    require(summary["status"] == "SOURCE_SIDE_ROUTE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["radial_bao_rows"] == "2", "expected two radial BAO rows")
    require(summary["redshift_bin_count"] == "2", "expected two radial BAO redshift bins")
    require(summary["independent_from_pantheon_distance_residuals"] == "true", "must be Pantheon-residual independent")
    require(summary["independent_from_cc_clock_level_route"] == "true", "must be CC-level-route independent")
    require(summary["rd_nuisance_unresolved"] == "true", "rd nuisance blocker must remain explicit")
    require(summary["underresolved_for_endpoint_route"] == "true", "underresolved blocker must remain explicit")
    require(summary["endpoint_replay_allowed"] == "false", "audit must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "audit must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "audit must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(
        summary["verdict"] == "independent_radial_bao_time_observable_present_but_underresolved_not_replay",
        "unexpected verdict",
    )
    for row in rows:
        require(row["observable"] == "DH_over_rd", "only radial BAO rows should be present")
        require(row["rd_nuisance_status"] == "rd_not_solved_here_route_requires_future_joint_BAO_handling", "bad rd status")
        require(row["endpoint_replay_allowed"] == "false", "row must not allow endpoint replay")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_residuals"] == "false", "row must not contain residuals")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    print(
        "PAPER10_SDSS_BAO_TIME_READOUT_ROUTE_AUDIT_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
