#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_design_matrix_v1_summary.csv"


def main() -> None:
    if not MATRIX.exists() or not SUMMARY.exists():
        raise SystemExit("source-native void/web design matrix artifacts are missing")
    with SUMMARY.open(newline="") as f:
        summary_rows = list(csv.DictReader(f))
    with MATRIX.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = set(reader.fieldnames or [])
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain exactly one row")
    summary = summary_rows[0]
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("design matrix endpoint scoring must remain false")
    if summary["contains_residuals"] != "false" or summary["contains_fit_statistics"] != "false":
        raise SystemExit("design matrix cannot contain residuals or fit statistics")
    if len(rows) != int(summary["rows"]):
        raise SystemExit("summary row count mismatch")
    required = {
        "W_void_source_native_basis",
        "W_web_source_native_basis",
        "r_pantheon_lowz_mpc_over_h",
    }
    if not required <= columns:
        raise SystemExit(f"missing source-native columns: {sorted(required - columns)}")
    forbidden = {"model_mu", "distance_residuals", "chi2", "likelihood", "fit_improvement_flags"}
    if forbidden & columns:
        raise SystemExit(f"forbidden endpoint columns present: {sorted(forbidden & columns)}")
    for row in rows:
        for key in ["W_void_source_native_basis", "W_web_source_native_basis"]:
            value = float(row[key])
            if not (0.0 <= value <= 1.0):
                raise SystemExit(f"{key} out of range: {value}")
    if int(summary["void_nonzero_rows"]) <= 0:
        raise SystemExit("void source-native basis is empty")
    if int(summary["web_nonzero_rows"]) <= 0:
        raise SystemExit("web source-native basis is empty")
    print(
        "PAPER10_PANTHEON_VOID_WEB_SOURCE_NATIVE_DESIGN_MATRIX_V1_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
