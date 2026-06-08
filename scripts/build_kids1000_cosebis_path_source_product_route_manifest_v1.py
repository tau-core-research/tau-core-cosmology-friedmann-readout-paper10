#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_source_product_route_policy_v1.csv"
ACQUISITION = ROOT / "data" / "derived" / "kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("source-product route policy must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("source-product route policy must not fetch products")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("source-product route policy must not compute path mapping")

    with ACQUISITION.open(newline="") as f:
        acquisition_rows = list(csv.DictReader(f))
    by_req = {row["requirement_id"]: row for row in acquisition_rows}
    expected = {
        "REQ_N_PAIR_LOCK",
        "REQ_T_TILE_LOCK",
        "REQ_F_OVERLAP_SOURCE",
        "REQ_D_PATH_SOURCE",
        "REQ_E_WEB_SOURCE",
        "REQ_C_NORM_RULE",
        "REQ_NULL_CONTROLS_EXECUTION",
    }
    if set(by_req) != expected:
        raise SystemExit("unexpected acquisition-plan requirements")

    rows = [
        {
            "route_id": "ROUTE_N_PAIR_EXISTING_REDSHIFT_LOCK",
            "requirement_id": "REQ_N_PAIR_LOCK",
            "factor_id": "N_pair",
            "route_status": "already_source_supported_no_fetch",
            "source_route_class": "existing_redshift_kernel_inventory_lock",
            "candidate_product_family": "kids1000_cosebis_redshift_kernel_inventory_v1",
            "minimum_acceptance": "reuse_existing_five_source_bin_inventory_without_endpoint_weighting",
            "next_action": "none_before_mapping",
            "may_resolve_blocker": "false",
        },
        {
            "route_id": "ROUTE_T_TILE_EXISTING_ROUTE_TILE_LOCK",
            "requirement_id": "REQ_T_TILE_LOCK",
            "factor_id": "T_tile",
            "route_status": "already_source_supported_no_fetch",
            "source_route_class": "existing_preferred_route_tile_inventory_lock",
            "candidate_product_family": "kids_dr41_preferred_9band_route_tile_coordinate_inventory",
            "minimum_acceptance": "reuse_196_route_tiles_without_endpoint_tile_selection",
            "next_action": "none_before_mapping",
            "may_resolve_blocker": "false",
        },
        {
            "route_id": "ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY",
            "requirement_id": "REQ_F_OVERLAP_SOURCE",
            "factor_id": "F_overlap",
            "route_status": "declared_not_acquired",
            "source_route_class": "official_footprint_polygon_or_tile_geometry",
            "candidate_product_family": "kids_dr4_official_footprint_or_mask_geometry_products",
            "minimum_acceptance": "assigns_target_row_tile_support_from_source_geometry_without_kids_data_vector_values",
            "next_action": "locate_official_footprint_or_tile_geometry_product_and_freeze_overlap_rule",
            "may_resolve_blocker": "true",
        },
        {
            "route_id": "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
            "requirement_id": "REQ_F_OVERLAP_SOURCE",
            "factor_id": "F_overlap",
            "route_status": "declared_not_acquired",
            "source_route_class": "source_native_pixel_mask_overlap_from_full_route_masks",
            "candidate_product_family": "kids_dr41_full_mask_products_for_preferred_route_tiles",
            "minimum_acceptance": "derives_overlap_from_mask_coverage_only_without_lensing_residual_or_chain_inputs",
            "next_action": "fetch_or_verify_full_route_mask_products_then_build_frozen_overlap_derivation",
            "may_resolve_blocker": "true",
        },
        {
            "route_id": "ROUTE_D_PATH_FULL_MASK_DEPTH_PRODUCTS",
            "requirement_id": "REQ_D_PATH_SOURCE",
            "factor_id": "D_path",
            "route_status": "declared_not_acquired",
            "source_route_class": "full_mask_depth_products_for_preferred_route_tiles",
            "candidate_product_family": "kids_dr41_mask_depth_or_source_native_path_load_products",
            "minimum_acceptance": "covers_preferred_route_tiles_or_declares_source_frozen_subset_before_mapping",
            "next_action": "promote_three_mask_shell_to_full_route_or_documented_subset_rule",
            "may_resolve_blocker": "true",
        },
        {
            "route_id": "ROUTE_D_PATH_DOCUMENTED_SUBSET_CONTROL",
            "requirement_id": "REQ_D_PATH_SOURCE",
            "factor_id": "D_path",
            "route_status": "declared_not_acquired",
            "source_route_class": "documented_subset_control_if_full_route_unavailable",
            "candidate_product_family": "predeclared_mask_depth_subset_control",
            "minimum_acceptance": "declares_incomplete_path_depth_status_and_disables_population_endpoint_claims",
            "next_action": "use_only_as_control_if_full_route_product_remains_unavailable",
            "may_resolve_blocker": "false",
        },
        {
            "route_id": "ROUTE_E_WEB_EXTERNAL_ENVIRONMENT_CATALOG",
            "requirement_id": "REQ_E_WEB_SOURCE",
            "factor_id": "E_web",
            "route_status": "declared_not_acquired",
            "source_route_class": "external_web_environment_catalog_covering_kids_footprint",
            "candidate_product_family": "source_frozen_cosmic_web_or_large_scale_environment_catalog",
            "minimum_acceptance": "assigns_environment_observable_to_route_tiles_or_sky_regions_without_posthoc_residual_labels",
            "next_action": "select_environment_catalog_and_freeze_tile_or_region_assignment_rule",
            "may_resolve_blocker": "true",
        },
        {
            "route_id": "ROUTE_E_WEB_NULL_ABSENT_CONTROL",
            "requirement_id": "REQ_E_WEB_SOURCE",
            "factor_id": "E_web",
            "route_status": "declared_not_acquired",
            "source_route_class": "predeclared_null_web_absent_control",
            "candidate_product_family": "zero_or_blind_web_factor_control",
            "minimum_acceptance": "declares_web_factor_absent_before_scoring_and_does_not_use_endpoint_outcomes",
            "next_action": "use_as_stress_control_only_if_environment_catalog_is_unavailable",
            "may_resolve_blocker": "false",
        },
        {
            "route_id": "ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL",
            "requirement_id": "REQ_C_NORM_RULE",
            "factor_id": "C_norm",
            "route_status": "declared_not_computed",
            "source_route_class": "normalization_protocol_after_nonzero_factors_exist",
            "candidate_product_family": "source_side_weight_normalization_rule",
            "minimum_acceptance": "normalizes_nonzero_weights_without_using_predictions_residuals_or_fit_improvement",
            "next_action": "defer_until_F_overlap_D_path_and_E_web_are_source_frozen",
            "may_resolve_blocker": "true",
        },
        {
            "route_id": "ROUTE_NULL_CONTROLS_AFTER_MAPPING",
            "requirement_id": "REQ_NULL_CONTROLS_EXECUTION",
            "factor_id": "null_controls",
            "route_status": "declared_not_executed",
            "source_route_class": "predeclared_null_controls_after_mapping_vector_exists",
            "candidate_product_family": "sky_rotation_pair_shuffle_wrong_channel_and_sign_flip_controls",
            "minimum_acceptance": "runs_frozen_seed_and_multiplicity_policy_without_posthoc_selection",
            "next_action": "defer_until_mapping_vector_exists",
            "may_resolve_blocker": "false",
        },
    ]
    for row in rows:
        acquisition = by_req[row["requirement_id"]]
        row.update(
            {
                "policy_id": policy["policy_id"],
                "requirement_current_state": acquisition["current_state"],
                "requirement_blocks_weight_computation": acquisition["blocks_weight_computation"],
                "external_products_fetched": "false",
                "numeric_factor_computed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_weight_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_path_source_product_route_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_MANIFEST_BUILT_NOT_FETCHED",
        "route_count": str(len(rows)),
        "declared_not_acquired_route_count": str(sum(row["route_status"] == "declared_not_acquired" for row in rows)),
        "already_supported_route_count": str(sum(row["route_status"] == "already_source_supported_no_fetch" for row in rows)),
        "declared_not_computed_route_count": str(sum(row["route_status"] == "declared_not_computed" for row in rows)),
        "declared_not_executed_route_count": str(sum(row["route_status"] == "declared_not_executed" for row in rows)),
        "blocker_resolving_candidate_count": str(sum(row["may_resolve_blocker"] == "true" for row in rows)),
        "control_or_lock_candidate_count": str(sum(row["may_resolve_blocker"] == "false" for row in rows)),
        "external_products_fetched": "false",
        "numeric_factors_computed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_weight_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_path_source_product_route_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_MANIFEST_V1_BUILT "
        f"routes={len(rows)} fetched=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
