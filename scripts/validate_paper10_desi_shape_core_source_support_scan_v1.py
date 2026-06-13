#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_source_support_scan_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("shape-core support scan summary must contain one row")
    summary = summary_rows[0]
    if summary["status"] != "DESI_SHAPE_CORE_SOURCE_SUPPORT_SCAN_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad shape-core support scan status")
    if summary["row2_moresco2012_support_found"] != "true":
        raise SystemExit("expected Moresco et al. (2012) row2 support in frozen CC table")
    if summary["row2_support_status"] != "partial_strengthening_in_interval_not_endpoint_pair_replacement":
        raise SystemExit("row2 support must remain partial, not endpoint-ready")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("shape-core support scan must not authorize replay")
    if summary["endpoint_validation_claimed"] != "false" or summary["physical_validation_claimed"] != "false":
        raise SystemExit("shape-core support scan must not claim validation")
    row2 = [
        row for row in rows
        if row["shape_row"] == "2"
        and row["candidate_reference"] == "Moresco et al. (2012)"
        and row["independent_of_current_endpoint_families"] == "true"
    ]
    if len(row2) != 1:
        raise SystemExit("expected exactly one independent Moresco 2012 row2 support row")
    if row2[0]["candidate_z"] != "1.037":
        raise SystemExit("expected Moresco 2012 row2 support at z=1.037")
    if any(row["endpoint_validation_claimed"] != "false" for row in rows):
        raise SystemExit("support rows must not claim endpoint validation")
    print("paper10_desi_shape_core_source_support_scan_v1: OK")


if __name__ == "__main__":
    main()
