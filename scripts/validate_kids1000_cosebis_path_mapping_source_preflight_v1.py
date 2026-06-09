#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_source_preflight_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected path-mapping source preflight policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("path-mapping source preflight policy must remain endpoint disabled")
    if len(rows) != 10:
        raise SystemExit("path-mapping source preflight must contain ten components")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected path-mapping source preflight summary status")
    if summary["component_count"] != "10":
        raise SystemExit("unexpected component count")
    if summary["target_rows"] != "300":
        raise SystemExit("path-mapping source preflight must target 300 COSEBIs rows")
    if summary["mapping_ready"] != "false":
        raise SystemExit("mapping must not be marked ready")
    expected_states = {
        "cosebis_target_rows": "available",
        "redshift_kernel_inventory": "available",
        "mask_observable_shell": "partial_available_control",
        "preferred_route_tile_inventory": "available",
        "cosebis_path_mapping_design_skeleton": "available",
        "cosebis_path_mapping_domain_skeleton": "available",
        "path_weight_construction_rule": "declared_not_computed",
        "full_path_depth_footprint_mapping": "available_caveated_mask_load_proxy",
        "web_environment_catalog": "available_uniform_null_web_control",
        "null_control_seed_policy": "declared_not_executed",
    }
    by_component = {row["component_id"]: row for row in rows}
    if set(by_component) != set(expected_states):
        raise SystemExit("unexpected path-mapping source preflight components")
    for component_id, expected_state in expected_states.items():
        if by_component[component_id]["source_state"] != expected_state:
            raise SystemExit(f"unexpected state for {component_id}")
    if by_component["mask_observable_shell"]["source_count"] != "3":
        raise SystemExit("mask observable shell should carry only the three-mask subset")
    if by_component["preferred_route_tile_inventory"]["source_count"] != "196":
        raise SystemExit("preferred route tile inventory should carry all 196 route tiles")
    if by_component["cosebis_path_mapping_design_skeleton"]["source_count"] != "300":
        raise SystemExit("design skeleton should carry all 300 COSEBIs target rows")
    if by_component["cosebis_path_mapping_domain_skeleton"]["source_count"] != "58800":
        raise SystemExit("domain skeleton should carry all 300x196 target-tile rows")
    if by_component["path_weight_construction_rule"]["source_count"] != "7":
        raise SystemExit("path-weight construction rule should carry seven factors")
    if by_component["redshift_kernel_inventory"]["source_count"] != "5":
        raise SystemExit("redshift kernel inventory should carry five source bins")
    if by_component["full_path_depth_footprint_mapping"]["blocking_status"] != "not_blocking":
        raise SystemExit("full path/depth mask-load proxy should no longer block source preflight")
    if by_component["full_path_depth_footprint_mapping"]["source_count"] != "196":
        raise SystemExit("full path/depth mask-load proxy should carry all 196 route tiles")
    if by_component["web_environment_catalog"]["blocking_status"] != "not_blocking":
        raise SystemExit("web environment catalogue must be nonblocking only as a null-web control")
    if by_component["web_environment_catalog"]["source_count"] != "196":
        raise SystemExit("web null-control should carry all 196 route tiles")
    if "no_positive_web_claim" not in by_component["web_environment_catalog"]["limitation"]:
        raise SystemExit("web null-control must forbid positive web claims")
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_sky_direction_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_SOURCE_PREFLIGHT_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
