#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv"
ROUTES = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("blocker-resolution policy must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("blocker-resolution policy must not fetch products")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("blocker-resolution policy must not compute path mapping")

    with ROUTES.open(newline="") as f:
        route_rows = list(csv.DictReader(f))
    by_route = {row["route_id"]: row for row in route_rows}
    required_routes = {
        "ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY",
        "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
        "ROUTE_D_PATH_FULL_MASK_DEPTH_PRODUCTS",
        "ROUTE_E_WEB_EXTERNAL_ENVIRONMENT_CATALOG",
        "ROUTE_E_WEB_NULL_ABSENT_CONTROL",
        "ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL",
        "ROUTE_NULL_CONTROLS_AFTER_MAPPING",
    }
    if not required_routes <= set(by_route):
        raise SystemExit("route manifest is missing blocker-resolution routes")

    rows = [
        {
            "order_rank": "1",
            "resolution_stage": "freeze_footprint_overlap",
            "factor_id": "F_overlap",
            "accepted_route_ids": "ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY;ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED",
            "stage_status": "resolved_source_supported",
            "why_first": "target_row_tile_support_is_structural_for_any_path_weight",
            "minimum_exit_condition": "source_frozen_full_route_pixel_fraction_rule_exists_without_endpoint_inputs",
            "next_allowed_stage_if_unresolved": "proceed_to_D_path",
        },
        {
            "order_rank": "2",
            "resolution_stage": "promote_path_depth_support",
            "factor_id": "D_path",
            "accepted_route_ids": "ROUTE_D_PATH_FULL_MASK_DEPTH_PRODUCTS",
            "stage_status": "resolved_source_supported",
            "why_first": "path_depth_load_is_only_meaningful_after_overlap_domain_exists",
            "minimum_exit_condition": "source_frozen_full_route_mask_load_proxy_exists_without_endpoint_inputs",
            "next_allowed_stage_if_unresolved": "proceed_to_E_web",
        },
        {
            "order_rank": "3",
            "resolution_stage": "freeze_web_environment_support",
            "factor_id": "E_web",
            "accepted_route_ids": "ROUTE_E_WEB_EXTERNAL_ENVIRONMENT_CATALOG;ROUTE_E_WEB_NULL_ABSENT_CONTROL",
            "stage_status": "resolved_control_supported",
            "why_first": "web_factor_needs_route_tile_or_sky_region_assignment_after_domain_support",
            "minimum_exit_condition": "source_frozen_environment_observable_or_predeclared_null_web_control",
            "next_allowed_stage_if_unresolved": "proceed_to_C_norm_as_path_only_control_no_positive_web_claim",
        },
        {
            "order_rank": "4",
            "resolution_stage": "define_source_side_normalization",
            "factor_id": "C_norm",
            "accepted_route_ids": "ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL",
            "stage_status": "resolved_source_supported",
            "why_first": "normalization_is_well_defined_only_after_nonzero_source_factors_exist",
            "minimum_exit_condition": "normalization_protocol_uses_only_source_side_nonzero_weights",
            "next_allowed_stage_if_unresolved": "proceed_to_mapping_vector",
        },
        {
            "order_rank": "5",
            "resolution_stage": "build_mapping_vector",
            "factor_id": "mapping_vector",
            "accepted_route_ids": "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_POLICY_V1",
            "stage_status": "resolved_source_supported",
            "why_first": "mapping_vector_requires_resolved_or_control_declared_factor_state",
            "minimum_exit_condition": "path_mapping_vector_built_from_frozen_factors_without_predictions_or_residuals",
            "next_allowed_stage_if_unresolved": "proceed_to_null_controls",
        },
        {
            "order_rank": "6",
            "resolution_stage": "execute_null_controls",
            "factor_id": "null_controls",
            "accepted_route_ids": "ROUTE_NULL_CONTROLS_AFTER_MAPPING",
            "stage_status": "blocking_not_executed",
            "why_first": "null_controls_need_a_mapping_vector_to_act_on",
            "minimum_exit_condition": "frozen_seed_and_multiplicity_controls_executed_without_posthoc_selection",
            "next_allowed_stage_if_unresolved": "none",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "external_products_fetched": "false",
                "numeric_factor_computed": "false",
                "path_mapping_computed": "true",
                "contains_mapping_vector": "true",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_weight_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_path_blocker_resolution_order_not_theory_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_BUILT_NOT_FETCHED",
        "stage_count": str(len(rows)),
        "resolved_source_supported_stage_count": str(sum(row["stage_status"] == "resolved_source_supported" for row in rows)),
        "resolved_control_supported_stage_count": str(sum(row["stage_status"] == "resolved_control_supported" for row in rows)),
        "blocking_unresolved_stage_count": str(
            sum(row["stage_status"] in {"blocking_not_resolved", "blocking_not_built", "blocking_not_executed"} for row in rows)
        ),
        "not_allowed_stage_count": str(sum(row["stage_status"] == "not_allowed_yet" for row in rows)),
        "declared_not_computed_stage_count": str(sum(row["stage_status"] == "declared_not_computed" for row in rows)),
        "declared_not_executed_stage_count": str(sum(row["stage_status"] == "declared_not_executed" for row in rows)),
        "first_blocker": "null_controls",
        "next_action": "execute_null_controls_and_build_theory_vector_before_scoring",
        "external_products_fetched": "false",
        "numeric_factors_computed": "false",
        "path_mapping_computed": "true",
        "contains_mapping_vector": "true",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_weight_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_path_blocker_resolution_order_not_theory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_V1_BUILT "
        f"stages={len(rows)} first_blocker=null_controls endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
