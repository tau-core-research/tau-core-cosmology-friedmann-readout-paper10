#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "pantheon_design_matrix_protocol_v1.csv"
DESIGN = ROOT / "data" / "derived" / "pantheon_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_design_matrix_v1_summary.csv"

FORBIDDEN_COLUMNS = {
    "distance_residuals",
    "model_mu",
    "delta_mu",
    "chi2",
    "likelihood",
    "fit_improvement_flags",
    "Tau_residual_parameters",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    summary = read_one(SUMMARY)
    with DESIGN.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = set(reader.fieldnames or [])

    if protocol["status"] != "DESIGN_MATRIX_FROZEN_NOT_SCORED":
        raise SystemExit("design matrix protocol must remain frozen-not-scored")
    if protocol["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("design matrix protocol endpoint flag must be false")
    if summary["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("design matrix summary endpoint flag must be false")
    if FORBIDDEN_COLUMNS & columns:
        raise SystemExit(f"design matrix contains forbidden columns: {sorted(FORBIDDEN_COLUMNS & columns)}")
    for flag in [
        "contains_model_predictions",
        "contains_residuals",
        "contains_fit_statistics",
    ]:
        if summary[flag].lower() != "false":
            raise SystemExit(f"design matrix summary has {flag}=true")
    if int(summary["rows"]) != len(rows):
        raise SystemExit("design matrix row count mismatch")
    if summary["design_matrix_sha256"] != sha256(DESIGN):
        raise SystemExit("design matrix sha mismatch")
    if not rows:
        raise SystemExit("design matrix is empty")
    print(
        "PAPER10_PANTHEON_DESIGN_MATRIX_V1_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()
