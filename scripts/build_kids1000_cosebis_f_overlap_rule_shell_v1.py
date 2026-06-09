#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv"
ORDER = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1.csv"
ROUTES = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_rule_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("F_overlap shell must remain endpoint disabled")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("F_overlap shell must not compute an overlap rule")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("F_overlap shell must not fetch external products")

    with ORDER.open(newline="") as f:
        order_rows = list(csv.DictReader(f))
    first_stage = min(order_rows, key=lambda row: int(row["order_rank"]))
    if first_stage["factor_id"] not in {"F_overlap", "D_path"}:
        raise SystemExit("unexpected first path blocker state before building F_overlap shell")

    with ROUTES.open(newline="") as f:
        route_rows = list(csv.DictReader(f))
    f_routes = [row for row in route_rows if row["factor_id"] == "F_overlap"]
    if len(f_routes) != 2:
        raise SystemExit("F_overlap shell expects two declared candidate/control routes")
    domain = read_one(DOMAIN)

    rows = [
        {
            "shell_item_id": "F_OVERLAP_INPUT_DOMAIN",
            "shell_role": "input_domain",
            "required_object": "cosebis_target_row_by_route_tile_domain",
            "required_source": "data/derived/kids1000_cosebis_path_mapping_domain_skeleton_v1.csv",
            "minimum_acceptance": "uses_all_declared_domain_rows_without_endpoint_tile_selection",
            "current_status": "available_shell_only",
            "blocks_overlap_computation": "false",
        },
        {
            "shell_item_id": "F_OVERLAP_ROUTE_OFFICIAL_GEOMETRY",
            "shell_role": "candidate_source_route",
            "required_object": "official_footprint_polygon_or_tile_geometry",
            "required_source": "official_KiDS_DR4_or_DR4_1_footprint_geometry_product",
            "minimum_acceptance": "assigns_target_row_tile_support_from_source_geometry_without_data_vector_values",
            "current_status": "declared_not_acquired",
            "blocks_overlap_computation": "true",
        },
        {
            "shell_item_id": "F_OVERLAP_ROUTE_PIXEL_MASK_DERIVED",
            "shell_role": "candidate_source_route",
            "required_object": "source_native_pixel_mask_overlap_from_full_route_masks",
            "required_source": "full_KiDS_DR4_1_preferred_route_mask_products",
            "minimum_acceptance": "derives_overlap_from_mask_coverage_only_without_lensing_residual_or_chain_inputs",
            "current_status": "declared_not_acquired",
            "blocks_overlap_computation": "true",
        },
        {
            "shell_item_id": "F_OVERLAP_OUTPUT_SCHEMA",
            "shell_role": "output_schema",
            "required_object": "row_tile_overlap_support_table",
            "required_source": "future_source_frozen_overlap_derivation",
            "minimum_acceptance": "one_row_per_target_row_tile_domain_entry_with_support_flag_or_fraction_and_provenance",
            "current_status": "declared_not_computed",
            "blocks_overlap_computation": "true",
        },
        {
            "shell_item_id": "F_OVERLAP_LEAKAGE_BOUNDARY",
            "shell_role": "leakage_boundary",
            "required_object": "forbidden_endpoint_inputs",
            "required_source": "policy_forbidden_inputs",
            "minimum_acceptance": "no_kids_data_vector_values_no_posterior_chains_no_residuals_no_posthoc_tile_selection",
            "current_status": "declared",
            "blocks_overlap_computation": "false",
        },
        {
            "shell_item_id": "F_OVERLAP_FAILURE_MODE",
            "shell_role": "failure_mode",
            "required_object": "no_overlap_rule_no_mapping",
            "required_source": "blocker_resolution_order_policy",
            "minimum_acceptance": "if_no_source_frozen_overlap_rule_exists_mapping_vector_and_scoring_remain_disabled",
            "current_status": "active",
            "blocks_overlap_computation": "false",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "factor_id": "F_overlap",
                "target_rows": domain["target_rows"],
                "route_tiles": domain["tile_count"],
                "domain_rows": domain["domain_rows"],
                "candidate_route_count": str(len(f_routes)),
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
                "claim_boundary": "kids1000_cosebis_f_overlap_rule_shell_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_BUILT_NOT_COMPUTED",
        "shell_item_count": str(len(rows)),
        "candidate_route_count": str(len(f_routes)),
        "target_rows": domain["target_rows"],
        "route_tiles": domain["tile_count"],
        "domain_rows": domain["domain_rows"],
        "first_blocker": policy["first_blocker"],
        "current_first_blocker": first_stage["factor_id"],
        "overlap_rule_ready": "false",
        "mapping_allowed": "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_rule_shell_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_V1_BUILT "
        f"domain_rows={domain['domain_rows']} overlap_ready=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
