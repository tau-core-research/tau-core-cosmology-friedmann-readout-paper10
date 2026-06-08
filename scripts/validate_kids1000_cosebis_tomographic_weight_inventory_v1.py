#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_weight_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_weight_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("tomographic-weight policy must remain endpoint disabled")
    if policy["statistical_likelihood_weighting_allowed"] != "false":
        raise SystemExit("tomographic-weight policy must not define likelihood weights")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("tomographic-weight inventory must remain endpoint disabled")
    if summary["statistical_likelihood_weighting_allowed"] != "false":
        raise SystemExit("tomographic-weight inventory must not define likelihood weights")
    if len(rows) != int(policy["expected_tomographic_pairs"]):
        raise SystemExit("unexpected tomographic-pair count")
    if summary["all_pairs_unit_weight"] != "true":
        raise SystemExit("all tomographic pairs must have unit retention weight")
    if summary["n_tomographic_pairs"] != policy["expected_tomographic_pairs"]:
        raise SystemExit("summary tomographic-pair count mismatch")
    for key in ["uses_residuals", "uses_fit_statistics", "uses_posterior_chains"]:
        if summary[key] != "false":
            raise SystemExit(f"summary must not use {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must not use {key}")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false":
            raise SystemExit(f"summary must not contain {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must not contain {key}")
    for row in rows:
        if row["retention_weight"] != "1.000000":
            raise SystemExit("retention weights must remain unit weights")
        if row["retained_rows_for_pair"] != policy["expected_rows_per_pair"]:
            raise SystemExit("unexpected rows per tomographic pair")
        if row["statistical_likelihood_weighting_allowed"] != "false":
            raise SystemExit("row must not allow likelihood weighting")
    print("PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_WEIGHT_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
