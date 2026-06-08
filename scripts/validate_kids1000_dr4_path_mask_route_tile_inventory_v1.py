#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected route tile inventory policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("route tile inventory policy must remain endpoint disabled")
    if policy["preferred_route_id"] != "KIDS_DR41_9BAND_MASK_WGET_SCRIPT":
        raise SystemExit("route tile inventory must use the DR4.1 9-band route")
    if len(rows) != int(policy["expected_tile_count"]):
        raise SystemExit("unexpected route tile inventory row count")
    if summary["status"] != "KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected route tile inventory summary status")
    if summary["tile_count"] != policy["expected_tile_count"]:
        raise SystemExit("route tile count mismatch")
    if summary["unique_tile_coordinate_count"] != policy["expected_tile_count"]:
        raise SystemExit("preferred route should not contain duplicate tile coordinates")
    if summary["duplicate_tile_coordinate_count"] != "0":
        raise SystemExit("duplicate tile coordinates detected")
    if rows[0]["mask_product_url"] != "http://ds.astro.rug.astro-wise.org:8000/KiDS_DR4.1_0.0_-28.2_ugriZYJHKs_msk.fits.gz":
        raise SystemExit("unexpected first preferred route URL")
    if rows[-1]["mask_product_url"] != "http://ds.astro.rug.astro-wise.org:8000/KiDS_DR4.1_5.6_-28.2_ugriZYJHKs_msk.fits.gz":
        raise SystemExit("unexpected last preferred route URL")
    if rows[0]["tile_ra_deg_filename_proxy"] != "0.0" or rows[0]["tile_dec_deg_filename_proxy"] != "-28.2":
        raise SystemExit("unexpected first tile coordinate")
    if rows[-1]["tile_ra_deg_filename_proxy"] != "5.6" or rows[-1]["tile_dec_deg_filename_proxy"] != "-28.2":
        raise SystemExit("unexpected last tile coordinate")
    if summary["mask_products_fetched"] != "false":
        raise SystemExit("summary must keep mask_products_fetched=false")
    if any(row["mask_product_fetched"] != "false" for row in rows):
        raise SystemExit("rows must keep mask_product_fetched=false")
    for key in [
        "mask_pixels_parsed",
        "footprint_polygon_computed",
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
    for row in rows:
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])
        if row["tile_coordinate_source"] != "KiDS_mask_filename_token":
            raise SystemExit("unexpected tile coordinate source")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
