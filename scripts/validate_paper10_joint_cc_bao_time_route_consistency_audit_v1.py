#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_joint_cc_bao_time_route_consistency_audit_not_validation"


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
    require(len(rows) == 2, "expected two joint audit rows")
    require(summary["status"] == "SOURCE_SIDE_JOINT_ROUTE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["radial_bao_rows"] == "2", "expected two radial BAO rows")
    require(summary["nearest_cc_rows_used"] == "2", "expected two nearest CC rows")
    require(float(summary["bao_cc_level_two_point_alignment"]) > 0.0, "BAO should align with CC level")
    require(float(summary["bao_cc_slope_two_point_alignment"]) < 0.0, "BAO should not align with CC slope")
    require(summary["rd_nuisance_unresolved"] == "true", "rd nuisance must remain explicit")
    require(summary["two_point_underresolved"] == "true", "two-point blocker must remain explicit")
    require(summary["endpoint_replay_allowed"] == "false", "audit must not allow replay")
    require(summary["endpoint_validation_claimed"] == "false", "audit must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "audit must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    require(
        summary["verdict"] == "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay",
        "unexpected verdict",
    )
    for row in rows:
        require(row["endpoint_replay_allowed"] == "false", "row must not allow replay")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_residuals"] == "false", "row must not contain residuals")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    print(
        "PAPER10_JOINT_CC_BAO_TIME_ROUTE_CONSISTENCY_AUDIT_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
