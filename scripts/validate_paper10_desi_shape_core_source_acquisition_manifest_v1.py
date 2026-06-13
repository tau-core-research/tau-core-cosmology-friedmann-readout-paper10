#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_acquisition_manifest_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 2:
        raise SystemExit("shape-core acquisition manifest must contain row 1 and row 2")
    if len(summary_rows) != 1:
        raise SystemExit("shape-core acquisition manifest summary must contain one row")
    summary = summary_rows[0]
    if summary["status"] != "DESI_SHAPE_CORE_SOURCE_ACQUISITION_MANIFEST_FROZEN_NOT_FETCHED_NOT_VALIDATION":
        raise SystemExit("bad shape-core acquisition manifest status")
    if summary["p0_targets"] != "DESI_SHAPE_ROW_2_CORE_SUPPORT":
        raise SystemExit("row 2 must be the P0 caveated target")
    if summary["p1_targets"] != "DESI_SHAPE_ROW_1_CORE_SUPPORT":
        raise SystemExit("row 1 must be the P1 confirmatory target")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("shape-core acquisition manifest must not authorize replay")
    if summary["endpoint_validation_claimed"] != "false" or summary["physical_validation_claimed"] != "false":
        raise SystemExit("shape-core acquisition manifest must not claim validation")
    by_row = {row["shape_row"]: row for row in rows}
    if by_row["2"]["priority"] != "P0":
        raise SystemExit("row 2 must be priority P0")
    if "single_reference" not in by_row["2"]["current_source_caveat"]:
        raise SystemExit("row 2 must preserve the single-reference caveat")
    if by_row["1"]["priority"] != "P1":
        raise SystemExit("row 1 must be priority P1")
    if any(row["source_fetch_status"] != "not_fetched" for row in rows):
        raise SystemExit("source fetch must remain pending")
    print("paper10_desi_shape_core_source_acquisition_manifest_v1: OK")


if __name__ == "__main__":
    main()
