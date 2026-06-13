#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_cc_bracket_source_freeze_not_validation"


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
    require(len(rows) == 2, "row4 bracket freeze must contain exactly two entries")
    require(len(summary_rows) == 1, "row4 bracket freeze summary must contain exactly one row")
    by_entry = {row["entry_id"]: row for row in rows}
    require(set(by_entry) == {"SIMON_2005_CC_Z1P43", "SIMON_2005_CC_Z1P53"}, "unexpected frozen entries")
    require(by_entry["SIMON_2005_CC_Z1P43"]["z"] == "1.43", "z=1.43 entry missing")
    require(by_entry["SIMON_2005_CC_Z1P43"]["H_z_km_s_Mpc"] == "177", "z=1.43 H(z) mismatch")
    require(by_entry["SIMON_2005_CC_Z1P43"]["sigma_H_km_s_Mpc"] == "18", "z=1.43 sigma mismatch")
    require(by_entry["SIMON_2005_CC_Z1P53"]["z"] == "1.53", "z=1.53 entry missing")
    require(by_entry["SIMON_2005_CC_Z1P53"]["H_z_km_s_Mpc"] == "140", "z=1.53 H(z) mismatch")
    require(by_entry["SIMON_2005_CC_Z1P53"]["sigma_H_km_s_Mpc"] == "14", "z=1.53 sigma mismatch")
    require({row["source_reference_family"] for row in rows} == {"Simon_2005"}, "reference family must be Simon_2005")
    require(
        {row["independent_of_current_blocker_reference_family"] for row in rows} == {"false"},
        "entries must not be promoted to independent-family support",
    )
    require({row["source_values_frozen"] for row in rows} == {"true"}, "source values must be frozen")
    require({row["row_can_enter_replay"] for row in rows} == {"false"}, "row must not enter replay")
    require({row["endpoint_replay_allowed"] for row in rows} == {"false"}, "replay must remain disabled")
    require({row["endpoint_validation_claimed"] for row in rows} == {"false"}, "endpoint validation must remain false")
    require({row["physical_validation_claimed"] for row in rows} == {"false"}, "physical validation must remain false")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "row claim boundary mismatch")
    summary = summary_rows[0]
    require(
        summary["status"] == "ROW4_CC_BRACKET_SOURCE_VALUES_FROZEN_REFERENCE_FAMILY_NOT_INDEPENDENT_NOT_REPLAY",
        "bad summary status",
    )
    require(summary["frozen_entry_count"] == "2", "summary entry count mismatch")
    require(summary["source_values_frozen"] == "true", "summary source freeze mismatch")
    require(summary["independent_reference_family_redundancy_satisfied"] == "false", "independence blocker must remain")
    require(summary["row4_can_enter_replay"] == "false", "row4 replay must remain disabled")
    require(summary["row5_remains_blocked"] == "true", "row5 must remain blocked")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print("paper10_desi_row4_cc_bracket_source_freeze_v1: OK")


if __name__ == "__main__":
    main()
