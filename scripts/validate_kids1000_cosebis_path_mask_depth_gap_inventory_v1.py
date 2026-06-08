#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mask_depth_gap_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mask_depth_gap_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("path mask/depth policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("path mapping must not be computed in policy")
    if policy["path_mask_depth_product_available"] != "false":
        raise SystemExit("policy should declare external path product requirement")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("path mask/depth gap inventory must remain endpoint disabled")
    if summary["path_mask_depth_product_available"] != "false":
        raise SystemExit("gap inventory must not accept an in-tarball path product")
    if summary["accepted_path_mask_depth_products"] != "0":
        raise SystemExit("no in-tarball path mask/depth product should be accepted")
    if summary["blocker"] != "external_source_frozen_lensing_path_mask_or_depth_map_required":
        raise SystemExit("unexpected path mask/depth blocker")
    for key in [
        "current_path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_path_selection",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    if any(row["accepted_as_path_mask_depth_product"] != "false" for row in rows):
        raise SystemExit("no row should be accepted as path mask/depth product")
    if not any(row["member_name"].endswith("Read.me") for row in rows):
        raise SystemExit("gap audit should include the release Read.me")
    if not any("statistic_fits_filename_token" in row["classification_reason"] for row in rows):
        raise SystemExit("gap audit should classify statistic FITS mask-token false positives")
    for marker in [
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "kids_data_vector_values",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_BUILT_EXTERNAL_PRODUCT_REQUIRED":
        raise SystemExit("unexpected path mask/depth gap status")
    print("PAPER10_KIDS1000_COSEBIS_PATH_MASK_DEPTH_GAP_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
