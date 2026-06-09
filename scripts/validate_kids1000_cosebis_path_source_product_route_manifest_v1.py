#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_source_product_route_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_source_product_route_manifest_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_POLICY_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected source-product route policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("source-product route policy must remain endpoint disabled")
    if policy["current_external_products_fetched"] != "false":
        raise SystemExit("source-product route policy must not fetch products")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_MANIFEST_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected source-product route manifest status")
    if len(rows) != 10:
        raise SystemExit("source-product route manifest must contain ten routes")
    if summary["route_count"] != "10":
        raise SystemExit("unexpected route count")
    if summary["declared_not_acquired_route_count"] != "2":
        raise SystemExit("unexpected declared-not-acquired route count")
    if summary["already_supported_route_count"] != "4":
        raise SystemExit("unexpected already-supported route count")
    if summary["alternative_not_needed_route_count"] != "2":
        raise SystemExit("unexpected alternative-not-needed route count")
    if summary["declared_not_computed_route_count"] != "1":
        raise SystemExit("unexpected declared-not-computed route count")
    if summary["declared_not_executed_route_count"] != "1":
        raise SystemExit("unexpected declared-not-executed route count")
    if summary["blocker_resolving_candidate_count"] != "2":
        raise SystemExit("unexpected blocker-resolving candidate count")
    if summary["control_or_lock_candidate_count"] != "8":
        raise SystemExit("unexpected control-or-lock candidate count")

    expected_routes = {
        "ROUTE_N_PAIR_EXISTING_REDSHIFT_LOCK": ("REQ_N_PAIR_LOCK", "N_pair", "false"),
        "ROUTE_T_TILE_EXISTING_ROUTE_TILE_LOCK": ("REQ_T_TILE_LOCK", "T_tile", "false"),
        "ROUTE_F_OVERLAP_OFFICIAL_FOOTPRINT_GEOMETRY": ("REQ_F_OVERLAP_SOURCE", "F_overlap", "false"),
        "ROUTE_F_OVERLAP_PIXEL_MASK_DERIVED": ("REQ_F_OVERLAP_SOURCE", "F_overlap", "false"),
        "ROUTE_D_PATH_FULL_MASK_DEPTH_PRODUCTS": ("REQ_D_PATH_SOURCE", "D_path", "false"),
        "ROUTE_D_PATH_DOCUMENTED_SUBSET_CONTROL": ("REQ_D_PATH_SOURCE", "D_path", "false"),
        "ROUTE_E_WEB_EXTERNAL_ENVIRONMENT_CATALOG": ("REQ_E_WEB_SOURCE", "E_web", "true"),
        "ROUTE_E_WEB_NULL_ABSENT_CONTROL": ("REQ_E_WEB_SOURCE", "E_web", "false"),
        "ROUTE_C_NORM_SOURCE_NORMALIZATION_PROTOCOL": ("REQ_C_NORM_RULE", "C_norm", "true"),
        "ROUTE_NULL_CONTROLS_AFTER_MAPPING": ("REQ_NULL_CONTROLS_EXECUTION", "null_controls", "false"),
    }
    by_route = {row["route_id"]: row for row in rows}
    if set(by_route) != set(expected_routes):
        raise SystemExit("unexpected source-product route ids")
    for route_id, (requirement_id, factor_id, may_resolve_blocker) in expected_routes.items():
        row = by_route[route_id]
        if row["requirement_id"] != requirement_id:
            raise SystemExit(f"unexpected requirement for {route_id}")
        if row["factor_id"] != factor_id:
            raise SystemExit(f"unexpected factor for {route_id}")
        if row["may_resolve_blocker"] != may_resolve_blocker:
            raise SystemExit(f"unexpected blocker-resolution flag for {route_id}")
        if row["route_status"] in {"declared_not_acquired", "declared_not_computed", "declared_not_executed"}:
            if row["external_products_fetched"] != "false":
                raise SystemExit(f"{route_id} must not fetch products")

    for key in [
        "external_products_fetched",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_weight_selection",
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
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PATH_SOURCE_PRODUCT_ROUTE_MANIFEST_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
