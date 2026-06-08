#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv"
MAPPING_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_web_path_mapping_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"
REDSHIFT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"
MASK_SHELL = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1_summary.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"
DESIGN_SKELETON = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv"
NULL_SEEDS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    mapping_policy = read_one(MAPPING_POLICY)
    tomo = read_one(TOMO)
    redshift = read_one(REDSHIFT)
    mask_shell = read_one(MASK_SHELL)
    route_tiles = read_one(ROUTE_TILES)
    design_skeleton = read_one(DESIGN_SKELETON)
    null_seeds = read_one(NULL_SEEDS)

    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("path-mapping source preflight must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("path mapping must not be computed in source preflight")
    if mapping_policy["current_mapping_computed"].lower() != "false":
        raise SystemExit("parent mapping policy must remain not computed")
    if mask_shell["path_mapping_computed"].lower() != "false":
        raise SystemExit("mask shell must not contain a path mapping")

    rows = [
        {
            "component_id": "cosebis_target_rows",
            "source_state": "available",
            "evidence_artifact": "data/derived/kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv",
            "source_count": tomo["data_vector_rows"],
            "preflight_role": "target_row_structure",
            "blocking_status": "not_blocking",
            "limitation": "target_rows_only_no_path_observable_assignment",
        },
        {
            "component_id": "redshift_kernel_inventory",
            "source_state": "available",
            "evidence_artifact": "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv",
            "source_count": redshift["n_source_bins"],
            "preflight_role": "tomographic_redshift_support",
            "blocking_status": "not_blocking",
            "limitation": "redshift_kernels_not_yet_combined_with_path_shell",
        },
        {
            "component_id": "mask_observable_shell",
            "source_state": "partial_available",
            "evidence_artifact": "data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv",
            "source_count": mask_shell["subset_count"],
            "preflight_role": "source_side_mask_observable_shell",
            "blocking_status": "partial_blocking",
            "limitation": "three_mask_subset_only_not_full_survey_geometry_not_cosebis_row_mapping",
        },
        {
            "component_id": "preferred_route_tile_inventory",
            "source_state": "available",
            "evidence_artifact": "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv",
            "source_count": route_tiles["tile_count"],
            "preflight_role": "preferred_route_tile_coordinate_index",
            "blocking_status": "not_blocking",
            "limitation": "filename_tile_coordinates_only_no_footprint_polygon_no_pixel_weight_no_cosebis_row_mapping",
        },
        {
            "component_id": "cosebis_path_mapping_design_skeleton",
            "source_state": "available",
            "evidence_artifact": "data/derived/kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv",
            "source_count": design_skeleton["target_rows"],
            "preflight_role": "target_row_redshift_route_span_design_skeleton",
            "blocking_status": "not_blocking",
            "limitation": "design_layout_only_no_tile_weights_no_path_mapping_no_theory_vector",
        },
        {
            "component_id": "full_path_depth_footprint_mapping",
            "source_state": "missing",
            "evidence_artifact": "data/derived/kids1000_cosebis_path_mask_depth_gap_inventory_v1_summary.csv",
            "source_count": "0",
            "preflight_role": "survey_geometry_to_cosebis_path_mapping",
            "blocking_status": "blocking",
            "limitation": "no_source_frozen_rule_assigns_path_mask_or_depth_to_300_cosebis_rows",
        },
        {
            "component_id": "web_environment_catalog",
            "source_state": "missing",
            "evidence_artifact": "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv",
            "source_count": "0",
            "preflight_role": "cosmic_web_environment_for_w_web",
            "blocking_status": "blocking",
            "limitation": "no_source_frozen_web_environment_catalog_for_kids_footprint",
        },
        {
            "component_id": "null_control_seed_policy",
            "source_state": "declared_not_executed",
            "evidence_artifact": "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv",
            "source_count": null_seeds["total_declared_control_draws"],
            "preflight_role": "future_null_controls",
            "blocking_status": "blocking_until_mapping_exists",
            "limitation": "controls_declared_but_not_run_and_no_mapping_vector_exists",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "selected_statistic": mapping_policy["selected_statistic"],
                "target_rows": mapping_policy["expected_target_rows"],
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_path_mapping_source_preflight_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_BUILT_NOT_MAPPED",
        "component_count": str(len(rows)),
        "available_component_count": str(sum(row["source_state"] == "available" for row in rows)),
        "partial_available_component_count": str(sum(row["source_state"] == "partial_available" for row in rows)),
        "missing_component_count": str(sum(row["source_state"] == "missing" for row in rows)),
        "declared_not_executed_component_count": str(sum(row["source_state"] == "declared_not_executed" for row in rows)),
        "target_rows": mapping_policy["expected_target_rows"],
        "mapping_ready": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_sky_direction_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_path_mapping_source_preflight_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_V1_BUILT "
        f"components={len(rows)} mapping_ready=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
