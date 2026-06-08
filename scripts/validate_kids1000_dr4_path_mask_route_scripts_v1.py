#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_route_scripts_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv"


def main() -> None:
    with MANIFEST.open(newline="") as f:
        manifest = list(csv.DictReader(f))
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(manifest) != 3 or len(rows) != 3:
        raise SystemExit("expected three KiDS path-mask route scripts")
    manifest_ids = {row["route_id"] for row in manifest}
    row_ids = {row["route_id"] for row in rows}
    if manifest_ids != row_ids:
        raise SystemExit("route script inventory must match manifest routes")
    if summary["preferred_route_id"] != "KIDS_DR41_9BAND_MASK_WGET_SCRIPT":
        raise SystemExit("DR4.1 9-band mask route must remain preferred")
    if int(summary["preferred_listed_mask_product_count"]) <= 0:
        raise SystemExit("preferred route must list mask products")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("path mask route scripts must remain endpoint disabled")
    if summary["mask_products_fetched"] != "false":
        raise SystemExit("mask FITS products must not be fetched in this route freeze")
    for key in [
        "path_mapping_computed",
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
    for route, row in zip(manifest, rows, strict=True):
        if route["endpoint_allowed"] != "false":
            raise SystemExit("manifest routes must remain endpoint disabled")
        if row["status"] != "KIDS_DR4_PATH_MASK_ROUTE_SCRIPT_FETCHED_FROZEN":
            raise SystemExit("unexpected route script status")
        if int(row["http_status"]) != 200:
            raise SystemExit("route scripts must fetch successfully")
        if int(row["byte_count"]) <= 0:
            raise SystemExit("route scripts must be non-empty")
        if len(row["sha256"]) != 64:
            raise SystemExit("route script hashes must be sha256")
        if int(row["listed_mask_product_count"]) <= 0:
            raise SystemExit("route scripts must list mask products")
        if row["mask_products_fetched"] != "false":
            raise SystemExit("mask products must not be fetched")
        if not (ROOT / row["local_path"]).exists():
            raise SystemExit(f"missing frozen route script: {row['local_path']}")
        for marker in [
            "posthoc_path_projection_labels",
            "posthoc_sky_direction_selection",
            "kids_data_vector_values",
        ]:
            if marker not in route["forbidden_inputs"]:
                raise SystemExit(f"missing forbidden input {marker} in {route['route_id']}")
    if summary["status"] != "KIDS_DR4_PATH_MASK_ROUTE_SCRIPTS_FETCHED_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected path mask route script summary status")
    print("PAPER10_KIDS_DR4_PATH_MASK_ROUTE_SCRIPTS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
