#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_LOCAL_ONLY_NOT_SCORED":
        raise SystemExit("unexpected full-route cache inventory policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("full-route cache policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_BUILT_LOCAL_ONLY_NOT_SCORED":
        raise SystemExit("unexpected full-route cache inventory summary status")
    if len(rows) != 196 or summary["expected_mask_count"] != "196":
        raise SystemExit("inventory must cover 196 mask products")
    if summary["present_mask_count"] != "196":
        raise SystemExit("local inventory snapshot must account for all 196 mask products")
    if summary["missing_mask_count"] != "0":
        raise SystemExit("local inventory snapshot should have zero missing masks")
    if summary["nonzero_file_count"] != "196":
        raise SystemExit("all inventory files must be nonzero")
    if summary["local_full_route_cache_count"] != "193":
        raise SystemExit("local full-route cache should contain the 193 previously missing masks")
    if summary["committed_subset_count"] != "3":
        raise SystemExit("committed subset should provide the three package masks")
    if summary["source_cache_complete"] != "true":
        raise SystemExit("source cache should be complete in the committed inventory snapshot")
    if summary["local_cache_required_for_public_reproduce"] != "false":
        raise SystemExit("public reproduce must not require ignored raw cache files")
    if summary["public_reproduce_uses_committed_inventory_only"] != "true":
        raise SystemExit("public reproduce must be documented as committed-inventory only")
    if any(row["sha256"] == "" for row in rows):
        raise SystemExit("all present mask products must have sha256 hashes")
    if any(row["local_or_committed_mask_present"] != "true" for row in rows):
        raise SystemExit("all rows must be present in this inventory snapshot")
    if any(row["accepted_for_source_cache_inventory"] != "true" for row in rows):
        raise SystemExit("all rows must be accepted for source-cache inventory")
    for key in [
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
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_ROUTE_CACHE_INVENTORY_V1_VALIDATED "
        "present=196 endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
