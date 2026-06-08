#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_source_availability_policy_v1.csv"
SHELL = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"
MASK_SUBSET = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1_summary.csv"
MASK_ROUTE_SCRIPT = ROOT / "data" / "raw" / "weak_lensing" / "kids1000_path_masks" / "kids_dr4.1_9band_msk_wget.sh"
MASK_SUBSET_DIR = ROOT / "data" / "raw" / "weak_lensing" / "kids1000_path_masks" / "mask_subset_v1"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("F_overlap source availability must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("F_overlap source availability must not fetch products")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("F_overlap source availability must not compute overlap")

    shell = read_one(SHELL)
    route_tiles = read_one(ROUTE_TILES)
    mask_subset = read_one(MASK_SUBSET)
    if shell["first_blocker"] != "F_overlap":
        raise SystemExit("source availability check must attach to F_overlap shell")
    tile_count = int(route_tiles["tile_count"])
    subset_count = int(mask_subset["subset_count"])
    local_subset_files = sorted(MASK_SUBSET_DIR.glob("*.fits.gz")) if MASK_SUBSET_DIR.exists() else []
    full_mask_files_available = subset_count >= tile_count and len(local_subset_files) >= tile_count

    rows = [
        {
            "availability_item_id": "F_OVERLAP_DOMAIN_SHELL",
            "route_id": "not_a_source_route",
            "factor_id": "F_overlap",
            "availability_status": "available_shell_only",
            "local_or_manifest_evidence": "data/derived/kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv",
            "source_count": shell["domain_rows"],
            "acceptance_status": "accepted_as_domain_shell_not_overlap_rule",
            "blocks_overlap_rule_ready": "false",
            "next_action": "none",
        },
        {
            "availability_item_id": "F_OVERLAP_OFFICIAL_GEOMETRY_PRODUCT",
            "route_id": "ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY",
            "factor_id": "F_overlap",
            "availability_status": "missing",
            "local_or_manifest_evidence": "none",
            "source_count": "0",
            "acceptance_status": "not_accepted_missing_official_geometry_product",
            "blocks_overlap_rule_ready": "true",
            "next_action": "locate_or_fetch_official_KiDS_DR4_or_DR4_1_footprint_geometry_without_endpoint_inputs",
        },
        {
            "availability_item_id": "F_OVERLAP_PIXEL_MASK_ROUTE_SCRIPT",
            "route_id": "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
            "factor_id": "F_overlap",
            "availability_status": "available_route_script_only",
            "local_or_manifest_evidence": str(MASK_ROUTE_SCRIPT.relative_to(ROOT)) if MASK_ROUTE_SCRIPT.exists() else "missing_route_script",
            "source_count": route_tiles["tile_count"],
            "acceptance_status": "not_accepted_for_overlap_rule_without_full_mask_products",
            "blocks_overlap_rule_ready": "true",
            "next_action": "use_route_script_only_as_acquisition_route_not_as_overlap_derivation",
        },
        {
            "availability_item_id": "F_OVERLAP_PIXEL_MASK_SUBSET",
            "route_id": "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
            "factor_id": "F_overlap",
            "availability_status": "partial_available",
            "local_or_manifest_evidence": "data/derived/kids1000_dr4_path_mask_subset_inventory_v1_summary.csv",
            "source_count": mask_subset["subset_count"],
            "acceptance_status": "not_accepted_for_full_overlap_rule_partial_three_mask_shell_only",
            "blocks_overlap_rule_ready": "true",
            "next_action": "promote_to_full_preferred_route_mask_products_or_keep_as_partial_control",
        },
        {
            "availability_item_id": "F_OVERLAP_FULL_PIXEL_MASK_SET",
            "route_id": "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
            "factor_id": "F_overlap",
            "availability_status": "available" if full_mask_files_available else "missing",
            "local_or_manifest_evidence": str(MASK_SUBSET_DIR.relative_to(ROOT)),
            "source_count": str(len(local_subset_files)),
            "acceptance_status": "accepted_for_future_overlap_derivation" if full_mask_files_available else "not_accepted_full_196_mask_set_missing",
            "blocks_overlap_rule_ready": "false" if full_mask_files_available else "true",
            "next_action": "derive_source_native_pixel_overlap_rule" if full_mask_files_available else "fetch_or_verify_all_preferred_route_mask_products_before_overlap_derivation",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "expected_route_tile_count": route_tiles["tile_count"],
                "domain_rows": shell["domain_rows"],
                "external_products_fetched": "false",
                "overlap_rule_computed": "false",
                "numeric_factor_computed": "false",
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
                "claim_boundary": "kids1000_cosebis_f_overlap_source_availability_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    accepted_overlap_routes = [
        row for row in rows if row["acceptance_status"].startswith("accepted_for_future_overlap_derivation")
    ]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_BUILT_NOT_FETCHED",
        "availability_item_count": str(len(rows)),
        "expected_route_tile_count": route_tiles["tile_count"],
        "local_full_mask_file_count": str(len(local_subset_files)),
        "partial_mask_subset_count": mask_subset["subset_count"],
        "accepted_overlap_route_count": str(len(accepted_overlap_routes)),
        "overlap_rule_ready": "true" if accepted_overlap_routes else "false",
        "first_unresolved_source_gap": "official_geometry_or_full_196_mask_products",
        "external_products_fetched": "false",
        "overlap_rule_computed": "false",
        "numeric_factors_computed": "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_source_availability_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_SOURCE_AVAILABILITY_V1_BUILT "
        f"accepted_routes={len(accepted_overlap_routes)} overlap_ready={summary['overlap_rule_ready']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
