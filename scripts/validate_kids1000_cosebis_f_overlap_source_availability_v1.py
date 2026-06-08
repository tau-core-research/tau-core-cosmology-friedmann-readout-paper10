#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_source_availability_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_POLICY_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected F_overlap availability policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("F_overlap availability policy must remain endpoint disabled")
    if policy["current_external_products_fetched"] != "false":
        raise SystemExit("F_overlap availability policy must not fetch products")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected F_overlap availability summary status")
    if summary["availability_item_count"] != "5":
        raise SystemExit("unexpected F_overlap availability item count")
    if summary["expected_route_tile_count"] != "196":
        raise SystemExit("unexpected preferred route tile count")
    if summary["partial_mask_subset_count"] != "3":
        raise SystemExit("F_overlap availability should preserve the three-mask subset status")
    if summary["accepted_overlap_route_count"] != "0":
        raise SystemExit("no F_overlap route should be accepted yet")
    if summary["overlap_rule_ready"] != "false":
        raise SystemExit("F_overlap rule must not be ready")
    if summary["first_unresolved_source_gap"] != "official_geometry_or_full_196_mask_products":
        raise SystemExit("unexpected first unresolved source gap")
    by_item = {row["availability_item_id"]: row for row in rows}
    expected = {
        "F_OVERLAP_DOMAIN_SHELL",
        "F_OVERLAP_OFFICIAL_GEOMETRY_PRODUCT",
        "F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT",
        "F_OVERLAP_PIXEL_MASK_SUBSET",
        "F_OVERLAP_FULL_PIXEL_MASK_SET",
    }
    if set(by_item) != expected:
        raise SystemExit("unexpected F_overlap availability items")
    if by_item["F_OVERLAP_DOMAIN_SHELL"]["blocks_overlap_rule_ready"] != "false":
        raise SystemExit("domain shell should not block source availability")
    for item in [
        "F_OVERLAP_OFFICIAL_GEOMETRY_PRODUCT",
        "F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT",
        "F_OVERLAP_PIXEL_MASK_SUBSET",
        "F_OVERLAP_FULL_PIXEL_MASK_SET",
    ]:
        if by_item[item]["blocks_overlap_rule_ready"] != "true":
            raise SystemExit(f"{item} must block current overlap readiness")
    if by_item["F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT"]["source_count"] != "196":
        raise SystemExit("route script must keep the 196-tile route count")
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
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
