#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "derived" / "growth_web_source_native_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "growth_web_source_native_design_matrix_v1_summary.csv"


def main() -> None:
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with MATRIX.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 6 or int(summary["rows"]) != 6:
        raise SystemExit("growth web design matrix must contain 6 rows")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring must remain false")
    if summary["contains_residuals"] != "false" or summary["contains_fit_statistics"] != "false":
        raise SystemExit("design matrix cannot contain residuals or fit statistics")
    if int(summary["web_nonzero_rows"]) <= 0:
        raise SystemExit("W_web is empty")
    for row in rows:
        value = float(row["W_web_source_native_basis"])
        if not (0.0 <= value <= 1.0):
            raise SystemExit(f"W_web out of range: {value}")
    print("PAPER10_GROWTH_WEB_SOURCE_NATIVE_DESIGN_MATRIX_V1_VALIDATED rows=6 endpoint_scoring_allowed=false")


if __name__ == "__main__":
    main()
