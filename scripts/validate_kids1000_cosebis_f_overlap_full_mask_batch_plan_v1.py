#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv"
GITIGNORE = ROOT / ".gitignore"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected full-mask batch-plan policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("full-mask batch-plan policy must remain endpoint disabled")
    if policy["current_external_products_fetched"] != "false":
        raise SystemExit("full-mask batch-plan policy must not fetch products")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected full-mask batch-plan summary status")
    if summary["expected_mask_count"] != "196":
        raise SystemExit("unexpected expected mask count")
    if summary["local_present_count"] != "3":
        raise SystemExit("batch plan must preserve the three local subset masks")
    if summary["missing_mask_count"] != "193":
        raise SystemExit("batch plan must preserve the 193 missing masks")
    if summary["batch_size_limit"] != "20":
        raise SystemExit("unexpected batch size limit")
    if summary["batch_count"] != "10":
        raise SystemExit("193 missing masks should produce ten batches with size limit 20")
    if summary["cache_git_policy"] != "large_fits_files_ignored_manifest_only_committed":
        raise SystemExit("unexpected cache git policy")
    if "full_route_cache_v1/*.fits.gz" not in GITIGNORE.read_text():
        raise SystemExit(".gitignore must ignore future full-route FITS cache files")
    sizes = [int(row["batch_size"]) for row in rows]
    if len(rows) != 10:
        raise SystemExit("batch plan must contain ten rows")
    if sum(sizes) != 193:
        raise SystemExit("batch sizes must sum to the missing mask count")
    if max(sizes) > 20:
        raise SystemExit("batch size exceeds policy limit")
    if sizes[-1] != 13:
        raise SystemExit("last batch should contain the remaining 13 masks")
    for key in [
        "batch_fetches_executed",
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
    for row in rows:
        if row["batch_fetch_executed"] != "false":
            raise SystemExit("batch rows must remain unfetched")
        for key in [
            "external_products_fetched",
            "overlap_rule_computed",
            "path_mapping_computed",
            "contains_mapping_vector",
            "contains_theory_vector",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_tile_selection",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
