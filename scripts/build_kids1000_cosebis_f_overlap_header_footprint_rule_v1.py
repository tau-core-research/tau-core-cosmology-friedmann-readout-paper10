#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_header_footprint_rule_policy_v1.csv"
CACHE_INVENTORY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1.csv"
CACHE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_cache_inventory_v1_summary.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_tile_rule_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def float_text(value: float) -> str:
    return f"{value:.12e}"


def read_header_metrics(path: Path) -> dict[str, str | float | int]:
    with fits.open(path, memmap=False) as hdul:
        h = hdul[0].header
    naxis1 = int(h["NAXIS1"])
    naxis2 = int(h["NAXIS2"])
    cd11 = float(h["CD1_1"])
    cd12 = float(h.get("CD1_2", 0.0))
    cd21 = float(h.get("CD2_1", 0.0))
    cd22 = float(h["CD2_2"])
    pixel_area_deg2 = abs(cd11 * cd22 - cd12 * cd21)
    footprint_area_deg2 = pixel_area_deg2 * naxis1 * naxis2
    return {
        "naxis1": naxis1,
        "naxis2": naxis2,
        "ctype1": str(h.get("CTYPE1", "")),
        "ctype2": str(h.get("CTYPE2", "")),
        "crval1": float(h["CRVAL1"]),
        "crval2": float(h["CRVAL2"]),
        "crpix1": float(h["CRPIX1"]),
        "crpix2": float(h["CRPIX2"]),
        "cd1_1": cd11,
        "cd1_2": cd12,
        "cd2_1": cd21,
        "cd2_2": cd22,
        "pixel_area_deg2": pixel_area_deg2,
        "footprint_area_deg2": footprint_area_deg2,
        "nominal_side_deg": math.sqrt(footprint_area_deg2),
    }


def main() -> None:
    policy = read_one(POLICY)
    cache_summary = read_one(CACHE_SUMMARY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("header-footprint rule policy must keep endpoint scoring disabled")
    if policy["current_pixel_mask_overlap_computed"] != "false":
        raise SystemExit("header-footprint rule must not claim pixel-mask overlap")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("header-footprint rule must not compute path mapping")
    if cache_summary["source_cache_complete"] != "true":
        raise SystemExit("header-footprint rule requires complete source cache inventory")

    with CACHE_INVENTORY.open(newline="") as f:
        cache_rows = list(csv.DictReader(f))
    if len(cache_rows) != 196:
        raise SystemExit("header-footprint rule expects 196 cached mask products")

    tile_rows: list[dict[str, str]] = []
    raw_areas: list[float] = []
    for row in cache_rows:
        if row["accepted_for_source_cache_inventory"] != "true":
            raise SystemExit("all cache rows must be accepted before header-footprint derivation")
        if row["cache_source"] == "local_full_route_cache_v1":
            fits_path = ROOT / row["expected_local_full_route_cache_path"]
        elif row["cache_source"] == "committed_subset_v1":
            fits_path = ROOT / row["committed_subset_path"]
        else:
            raise SystemExit("missing cache row cannot be used for header-footprint derivation")
        metrics = read_header_metrics(fits_path)
        raw_areas.append(float(metrics["footprint_area_deg2"]))
        tile_ra = float(row["filename"].split("_")[2])
        tile_dec = float(row["filename"].split("_")[3])
        crval1 = float(metrics["crval1"])
        crval2 = float(metrics["crval2"])
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "filename": row["filename"],
                "cache_source": row["cache_source"],
                "sha256": row["sha256"],
                "tile_ra_deg_filename_proxy": float_text(tile_ra),
                "tile_dec_deg_filename_proxy": float_text(tile_dec),
                "header_crval1_deg": float_text(crval1),
                "header_crval2_deg": float_text(crval2),
                "header_filename_center_abs_delta_deg": float_text(abs(crval1 - tile_ra) + abs(crval2 - tile_dec)),
                "naxis1": str(metrics["naxis1"]),
                "naxis2": str(metrics["naxis2"]),
                "ctype1": str(metrics["ctype1"]),
                "ctype2": str(metrics["ctype2"]),
                "cd1_1": float_text(float(metrics["cd1_1"])),
                "cd1_2": float_text(float(metrics["cd1_2"])),
                "cd2_1": float_text(float(metrics["cd2_1"])),
                "cd2_2": float_text(float(metrics["cd2_2"])),
                "pixel_area_deg2": float_text(float(metrics["pixel_area_deg2"])),
                "header_footprint_area_deg2": float_text(float(metrics["footprint_area_deg2"])),
                "nominal_side_deg": float_text(float(metrics["nominal_side_deg"])),
                "header_footprint_support": "true",
                "pixel_mask_values_read": "false",
                "pixel_mask_overlap_computed": "false",
                "overlap_rule_computed": "true",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    max_area = max(raw_areas)
    min_area = min(raw_areas)
    mean_area = sum(raw_areas) / len(raw_areas)
    for row in tile_rows:
        area = float(row["header_footprint_area_deg2"])
        row["f_overlap_tile_header_area_norm"] = float_text(area / max_area)

    tile_by_index = {row["tile_index_zero_based"]: row for row in tile_rows}
    domain_rows: list[dict[str, str]] = []
    with DOMAIN.open(newline="") as f:
        for domain in csv.DictReader(f):
            tile = tile_by_index[domain["tile_index_zero_based"]]
            domain_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "domain_row_index_zero_based": domain["domain_row_index_zero_based"],
                    "target_row_index_zero_based": domain["target_row_index_zero_based"],
                    "tile_index_zero_based": domain["tile_index_zero_based"],
                    "pair_id": domain["pair_id"],
                    "bin1": domain["bin1"],
                    "bin2": domain["bin2"],
                    "mode": domain["mode"],
                    "tile_ra_deg_filename_proxy": domain["tile_ra_deg_filename_proxy"],
                    "tile_dec_deg_filename_proxy": domain["tile_dec_deg_filename_proxy"],
                    "f_overlap_value": tile["f_overlap_tile_header_area_norm"],
                    "f_overlap_rule_component": "header_wcs_area_normalized_by_max_tile_area",
                    "header_footprint_area_deg2": tile["header_footprint_area_deg2"],
                    "pixel_mask_values_read": "false",
                    "pixel_mask_overlap_computed": "false",
                    "overlap_rule_computed": "true",
                    "path_mapping_computed": "false",
                    "contains_mapping_vector": "false",
                    "contains_theory_vector": "false",
                    "contains_predictions": "false",
                    "contains_residuals": "false",
                    "contains_fit_statistics": "false",
                    "uses_kids_data_vector_values": "false",
                    "uses_posterior_chains": "false",
                    "uses_posthoc_tile_selection": "false",
                    "endpoint_scoring_allowed": "false",
                    "claim_boundary": policy["claim_boundary"],
                }
            )
    if len(domain_rows) != 58800:
        raise SystemExit("header-footprint domain rule must contain 58,800 rows")

    TILE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with TILE_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tile_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(tile_rows)
    with DOMAIN_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(domain_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(domain_rows)

    norm_values = [float(row["f_overlap_tile_header_area_norm"]) for row in tile_rows]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_BUILT_NOT_MAPPED",
        "tile_count": str(len(tile_rows)),
        "target_rows": "300",
        "domain_rows": str(len(domain_rows)),
        "min_header_footprint_area_deg2": float_text(min_area),
        "max_header_footprint_area_deg2": float_text(max_area),
        "mean_header_footprint_area_deg2": float_text(mean_area),
        "min_f_overlap_value": float_text(min(norm_values)),
        "max_f_overlap_value": float_text(max(norm_values)),
        "mean_f_overlap_value": float_text(sum(norm_values) / len(norm_values)),
        "unique_f_overlap_value_count_rounded_1e_minus_12": str(len({round(v, 12) for v in norm_values})),
        "header_footprint_rule_available": "true",
        "pixel_mask_values_read": "false",
        "pixel_mask_overlap_computed": "false",
        "overlap_rule_computed": "true",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_V1_BUILT "
        f"domain_rows={len(domain_rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
