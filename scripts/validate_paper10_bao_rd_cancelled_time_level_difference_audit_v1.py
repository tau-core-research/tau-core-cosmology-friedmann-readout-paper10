#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_bao_rd_cancelled_time_level_difference_audit_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 2, "audit must keep exactly two radial BAO rows")
    require(summary["status"] == "SOURCE_SIDE_RD_CANCELLED_DIFFERENCE_AUDIT_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["rd_cancels_in_difference"] == "true", "rd cancellation must be explicit")
    require(summary["differential_direction_sign_agreement"] == "true", "differential sign agreement changed")
    require(float(summary["delta_bao_snr"]) < 1.0, "current BAO differential significance must remain caveated")
    require(summary["amplitude_interpretation_allowed"] == "false", "amplitude interpretation must remain forbidden")
    require(
        summary["verdict"] == "rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint",
        "bad verdict",
    )
    for row in rows + [summary]:
        require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    print(
        "PAPER10_BAO_RD_CANCELLED_TIME_LEVEL_DIFFERENCE_AUDIT_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
