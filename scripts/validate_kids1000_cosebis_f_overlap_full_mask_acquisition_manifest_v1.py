#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_POLICY_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected full-mask acquisition policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("full-mask acquisition policy must remain endpoint disabled")
    if policy["current_external_products_fetched"] != "false":
        raise SystemExit("full-mask acquisition policy must not fetch products")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_MANIFEST_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected full-mask acquisition manifest status")
    if len(rows) != 196:
        raise SystemExit("full-mask acquisition manifest must contain 196 tile rows")
    if summary["expected_mask_count"] != "196":
        raise SystemExit("unexpected expected mask count")
    if summary["local_present_count"] != "3":
        raise SystemExit("current local present count should preserve the three-mask subset")
    if summary["missing_mask_count"] != "193":
        raise SystemExit("current missing mask count should be 193")
    if summary["full_mask_set_present"] != "false":
        raise SystemExit("full mask set must not be marked present")
    if summary["accepted_for_full_overlap_count"] != "0":
        raise SystemExit("no masks should be accepted for full overlap yet")
    if summary["overlap_rule_ready"] != "false":
        raise SystemExit("overlap rule must not be ready")
    present = [row for row in rows if row["local_mask_present"] == "true"]
    missing = [row for row in rows if row["local_mask_present"] == "false"]
    if len(present) != 3 or len(missing) != 193:
        raise SystemExit("row-level local mask counts do not match summary")
    if any(row["accepted_for_full_overlap"] != "false" for row in rows):
        raise SystemExit("no row may be accepted until the full set is present")
    for key in [
        "external_products_fetched",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_MANIFEST_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
