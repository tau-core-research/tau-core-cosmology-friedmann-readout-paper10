#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
WEIGHT_RULE = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("path-factor acquisition plan must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("path-factor acquisition plan must not fetch products")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("path-factor acquisition plan must not compute path mapping")

    with WEIGHT_RULE.open(newline="") as f:
        weight_rows = list(csv.DictReader(f))
    by_factor = {row["factor_id"]: row for row in weight_rows}
    required = {"N_pair", "T_tile", "F_overlap", "D_path", "E_web", "C_norm", "null_controls"}
    if set(by_factor) != required:
        raise SystemExit("unexpected weight-rule factor set")

    rows = [
        {
            "requirement_id": "REQ_N_PAIR_LOCK",
            "factor_id": "N_pair",
            "current_state": by_factor["N_pair"]["source_state"],
            "required_source_class": "existing_kids_nz_source_redshift_kernel_inventory",
            "minimum_acceptance": "five_source_bins_available_and_not_endpoint_weighted",
            "next_action": "none_before_mapping",
            "blocks_weight_computation": "false",
        },
        {
            "requirement_id": "REQ_T_TILE_LOCK",
            "factor_id": "T_tile",
            "current_state": by_factor["T_tile"]["source_state"],
            "required_source_class": "preferred_dr41_9band_route_tile_coordinate_inventory",
            "minimum_acceptance": "all_196_preferred_route_tiles_parsed_without_duplicates",
            "next_action": "none_before_mapping",
            "blocks_weight_computation": "false",
        },
        {
            "requirement_id": "REQ_F_OVERLAP_SOURCE",
            "factor_id": "F_overlap",
            "current_state": by_factor["F_overlap"]["source_state"],
            "required_source_class": "source_frozen_footprint_overlap_or_row_tile_assignment_rule",
            "minimum_acceptance": "assigns_each_domain_row_to_admissible_tile_footprint_support_without_kids_data_vector_values",
            "next_action": "acquire_or_derive_footprint_overlap_rule_from_kids_mask_geometry_or_official_footprint_products",
            "blocks_weight_computation": "true",
        },
        {
            "requirement_id": "REQ_D_PATH_SOURCE",
            "factor_id": "D_path",
            "current_state": by_factor["D_path"]["source_state"],
            "required_source_class": "full_preferred_route_mask_depth_or_source_native_path_load_summary",
            "minimum_acceptance": "covers_preferred_route_tiles_or_defines_documented_subset_rule_before_endpoint_scoring",
            "next_action": "promote_from_three_mask_shell_to_full_route_or_source_native_depth_mask_summary",
            "blocks_weight_computation": "true",
        },
        {
            "requirement_id": "REQ_E_WEB_SOURCE",
            "factor_id": "E_web",
            "current_state": by_factor["E_web"]["source_state"],
            "required_source_class": "source_frozen_web_environment_catalog_for_kids_footprint",
            "minimum_acceptance": "assigns_environment_observable_to_route_tiles_or_sky_regions_without_posthoc_residual_labels",
            "next_action": "select_external_cosmic_web_environment_catalog_or_predeclare_null_web_absent_control",
            "blocks_weight_computation": "true",
        },
        {
            "requirement_id": "REQ_C_NORM_RULE",
            "factor_id": "C_norm",
            "current_state": by_factor["C_norm"]["source_state"],
            "required_source_class": "normalization_rule_defined_after_nonzero_source_factors_exist",
            "minimum_acceptance": "normalizes_weights_without_using_lensing_residuals_or_fit_improvement",
            "next_action": "defer_until_F_overlap_D_path_E_web_are_source_frozen",
            "blocks_weight_computation": "true",
        },
        {
            "requirement_id": "REQ_NULL_CONTROLS_EXECUTION",
            "factor_id": "null_controls",
            "current_state": by_factor["null_controls"]["source_state"],
            "required_source_class": "predeclared_null_controls_executed_after_mapping_vector_exists",
            "minimum_acceptance": "run_declared_1008_controls_without_posthoc_multiplicity_or_seed_selection",
            "next_action": "defer_until_mapping_vector_exists",
            "blocks_weight_computation": "false",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
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
                "claim_boundary": "kids1000_cosebis_path_factor_acquisition_plan_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_BUILT_NOT_FETCHED",
        "requirement_count": str(len(rows)),
        "blocking_requirement_count": str(sum(row["blocks_weight_computation"] == "true" for row in rows)),
        "nonblocking_requirement_count": str(sum(row["blocks_weight_computation"] == "false" for row in rows)),
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
        "claim_boundary": "kids1000_cosebis_path_factor_acquisition_plan_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_V1_BUILT "
        f"requirements={len(rows)} fetched=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
