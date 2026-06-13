#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_metric_lensing_path_route_audit_policy_v1.csv"
LOW_Z_GEOMETRY = ROOT / "data/derived/low_z_pantheon_void_geometry_join_v1.csv"
KIDS_TILES = ROOT / "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
KIDS_LENSING = ROOT / "data/derived/kids1000_lensing_inventory_v1_summary.csv"
CMB_ROUTE_CACHE = ROOT / "data/source_manifest/source_page_cache/CMB_LENSING_PRODUCTS.html"
WEAK_LENSING_ROUTE_CACHE = ROOT / "data/source_manifest/source_page_cache/WEAK_LENSING_PRODUCTS.html"
OUT = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1_summary.csv"
CLAIM_BOUNDARY = "metric_lensing_path_route_audit_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def angular_sep_deg(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    ra1r = math.radians(ra1)
    ra2r = math.radians(ra2)
    dec1r = math.radians(dec1)
    dec2r = math.radians(dec2)
    cos_sep = (
        math.sin(dec1r) * math.sin(dec2r)
        + math.cos(dec1r) * math.cos(dec2r) * math.cos(ra1r - ra2r)
    )
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_sep))))


def main() -> None:
    policy = read_one(POLICY)
    if policy["status"] != "METRIC_LENSING_PATH_ROUTE_AUDIT_SOURCE_SIDE_NOT_SCORING":
        raise SystemExit("policy status mismatch")
    if policy["endpoint_replay_allowed"] != "false" or policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("route audit policy must not authorize replay or validation")
    if not CMB_ROUTE_CACHE.exists() or not WEAK_LENSING_ROUTE_CACHE.exists():
        raise SystemExit("cached lensing route pages are missing")
    kids_lensing = read_one(KIDS_LENSING)
    if kids_lensing["endpoint_scoring_allowed"] != "false":
        raise SystemExit("KiDS lensing inventory must remain endpoint disabled")
    low_z_rows = read_rows(LOW_Z_GEOMETRY)
    tile_rows = read_rows(KIDS_TILES)
    if not low_z_rows or not tile_rows:
        raise SystemExit("missing low-z rows or KiDS tile inventory")
    tiles = [
        {
            "tile_index_zero_based": row["tile_index_zero_based"],
            "ra": float(row["tile_ra_deg_filename_proxy"]),
            "dec": float(row["tile_dec_deg_filename_proxy"]),
        }
        for row in tile_rows
    ]
    rows: list[dict[str, str]] = []
    for row in low_z_rows:
        ra = float(row["ra_deg"])
        dec = float(row["dec_deg"])
        nearest = min(tiles, key=lambda tile: angular_sep_deg(ra, dec, tile["ra"], tile["dec"]))
        sep = angular_sep_deg(ra, dec, nearest["ra"], nearest["dec"])
        if sep <= 1.0:
            coverage = "KIDS_TILE_WITHIN_1_DEG_ROUTE_ONLY"
        elif sep <= 2.0:
            coverage = "KIDS_TILE_WITHIN_2_DEG_ROUTE_ONLY"
        else:
            coverage = "NO_NEARBY_KIDS_TILE_ROUTE_ONLY"
        rows.append(
            {
                "artifact_id": "LOW_Z_PANTHEON_METRIC_LENSING_PATH_ROUTE_AUDIT_V1",
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "coordinate_source": row["coordinate_source"],
                "ra_deg": row["ra_deg"],
                "dec_deg": row["dec_deg"],
                "kids_lensing_route_available": "true",
                "cmb_lensing_route_cache_available": "true",
                "weak_lensing_route_cache_available": "true",
                "nearest_kids_tile_index_zero_based": nearest["tile_index_zero_based"],
                "nearest_kids_tile_ra_deg": f"{nearest['ra']:.12g}",
                "nearest_kids_tile_dec_deg": f"{nearest['dec']:.12g}",
                "nearest_kids_tile_sep_deg": f"{sep:.12g}",
                "kids_tile_coverage_class": coverage,
                "metric_lensing_numeric_product_available_for_source": "false",
                "kappa_or_shear_value_computed": "false",
                "mass_map_integral_computed": "false",
                "path_weight_value_status": "BLOCKED_NO_SOURCE_ALIGNED_METRIC_LENSING_PRODUCT",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_lensing_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    within_1 = sum(row["kids_tile_coverage_class"] == "KIDS_TILE_WITHIN_1_DEG_ROUTE_ONLY" for row in rows)
    within_2 = sum(row["kids_tile_coverage_class"] == "KIDS_TILE_WITHIN_2_DEG_ROUTE_ONLY" for row in rows)
    partial_scope = {"344", "350", "374", "375", "384", "448", "554", "595", "603", "606", "635", "701"}
    partial_rows = [row for row in rows if row["source_row_index"] in partial_scope]
    summary = [
        {
            "artifact_id": "LOW_Z_PANTHEON_METRIC_LENSING_PATH_ROUTE_AUDIT_V1",
            "status": "METRIC_LENSING_PATH_ROUTE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING",
            "rows": str(len(rows)),
            "kids_tile_count": str(len(tiles)),
            "rows_nearest_kids_tile_within_1_deg": str(within_1),
            "rows_nearest_kids_tile_within_2_deg": str(within_2),
            "partial_path_scope_rows": str(len(partial_rows)),
            "partial_path_scope_nearest_kids_tile_within_1_deg": str(
                sum(row["kids_tile_coverage_class"] == "KIDS_TILE_WITHIN_1_DEG_ROUTE_ONLY" for row in partial_rows)
            ),
            "partial_path_scope_nearest_kids_tile_within_2_deg": str(
                sum(row["kids_tile_coverage_class"] == "KIDS_TILE_WITHIN_2_DEG_ROUTE_ONLY" for row in partial_rows)
            ),
            "kids_lensing_route_available": "true",
            "cmb_lensing_route_cache_available": "true",
            "metric_lensing_numeric_product_available_for_source": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "metric_lensing_routes_available_but_source_aligned_path_weight_missing",
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_METRIC_LENSING_PATH_ROUTE_AUDIT_BUILT "
        f"rows={summary[0]['rows']} within_1deg={summary[0]['rows_nearest_kids_tile_within_1_deg']} "
        f"numeric_product=false"
    )


if __name__ == "__main__":
    main()
