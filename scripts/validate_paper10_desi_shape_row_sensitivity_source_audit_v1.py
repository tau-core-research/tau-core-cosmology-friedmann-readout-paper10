#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row_sensitivity_source_audit_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 4:
        raise SystemExit("row-sensitivity source audit must contain exactly four shape rows")
    if len(summary_rows) != 1:
        raise SystemExit("row-sensitivity source audit summary must contain one row")
    summary = summary_rows[0]
    if summary["status"] != "DESI_SHAPE_ROW_SENSITIVITY_SOURCE_AUDIT_BUILT_NOT_VALIDATION":
        raise SystemExit("bad row-sensitivity source audit status")
    if summary["core_sensitive_rows"] != "1;2":
        raise SystemExit("expected middle shape rows 1;2 to carry the core sensitivity")
    if summary["most_dispensable_row"] != "0":
        raise SystemExit("expected row 0 to be most dispensable")
    if summary["most_required_row"] != "1":
        raise SystemExit("expected row 1 to be most required")
    if summary["endpoint_validation_claimed"] != "false" or summary["physical_validation_claimed"] != "false":
        raise SystemExit("row-sensitivity source audit must not claim validation")
    by_row = {row["shape_row"]: row for row in rows}
    if by_row["2"]["independent_reference_pair"] != "false":
        raise SystemExit("shape row 2 must preserve the single-reference caveat")
    if by_row["1"]["sensitivity_class"] != "core_sensitive":
        raise SystemExit("shape row 1 must be core-sensitive")
    if any(row["endpoint_validation_claimed"] != "false" for row in rows):
        raise SystemExit("row records must not claim endpoint validation")
    print("paper10_desi_shape_row_sensitivity_source_audit_v1: OK")


if __name__ == "__main__":
    main()
