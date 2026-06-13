#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_row4_clock_reopen_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_clock_reopen_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_clock_reopen_manifest_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 1, "row4 reopen manifest must contain exactly one target")
    require(len(summary_rows) == 1, "row4 reopen summary must contain exactly one row")
    row = rows[0]
    summary = summary_rows[0]
    require(row["row_id"] == "4", "only row 4 may be reopened here")
    require(row["target_z_eff"] == "1.484", "row 4 target z mismatch")
    require(row["required_bracket_z_low"] == "1.43", "low bracket mismatch")
    require(row["required_bracket_z_high"] == "1.53", "high bracket mismatch")
    require(row["source_action_status"] == "source_acquisition_reopened_not_cached", "bad source action status")
    require(row["source_values_frozen"] == "false", "source values must not be marked frozen")
    require(row["row_can_enter_replay"] == "false", "row 4 must not enter replay yet")
    require(row["row5_remains_blocked"] == "true", "row 5 blocker must be preserved")
    require(row["endpoint_replay_allowed"] == "false", "manifest must not authorize replay")
    require(row["endpoint_validation_claimed"] == "false", "manifest must not claim endpoint validation")
    require(row["physical_validation_claimed"] == "false", "manifest must not claim physical validation")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(summary["status"] == "ROW4_SOURCE_ACQUISITION_REOPENED_NOT_REPLAY_ROW5_BLOCKED", "bad summary status")
    require(summary["row4_source_acquisition_gate_can_reopen"] == "true", "row4 reopen flag mismatch")
    require(summary["row4_source_values_frozen"] == "false", "row4 values must not be frozen")
    require(summary["row4_can_enter_replay"] == "false", "row4 replay must remain disabled")
    require(summary["row5_remains_blocked"] == "true", "row5 must remain blocked")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print("paper10_desi_row4_clock_reopen_manifest_v1: OK")


if __name__ == "__main__":
    main()
