#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_redshift_kernel_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("redshift-kernel policy must remain endpoint disabled")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("redshift-kernel inventory must remain endpoint disabled")
    if len(rows) != int(policy["expected_source_bins"]):
        raise SystemExit("unexpected source-bin count")
    if summary["nz_rows"] != policy["expected_nz_rows"]:
        raise SystemExit("unexpected redshift-kernel row count")
    for key in [
        "uses_kids_data_vector_values",
        "uses_residuals",
        "uses_fit_statistics",
        "uses_posterior_chains",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    means = [float(row["mean_z"]) for row in rows]
    if means != sorted(means):
        raise SystemExit("source-bin mean redshifts should be ordered")
    for row in rows:
        if row["nz_rows"] != policy["expected_nz_rows"]:
            raise SystemExit("unexpected per-bin nz row count")
        if float(row["area_sum_nz_dz"]) <= 0.0:
            raise SystemExit("redshift kernel area must be positive")
        if float(row["support_z_min_nonzero"]) < 0.0:
            raise SystemExit("redshift support must be non-negative")
    if summary["status"] != "KIDS1000_COSEBIS_REDSHIFT_KERNEL_INVENTORY_BUILT_NOT_SCORED":
        raise SystemExit("unexpected redshift-kernel inventory status")
    print("PAPER10_KIDS1000_COSEBIS_REDSHIFT_KERNEL_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
