#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_weight_construction_rule_v1.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv"
REDSHIFT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"
MASK_SHELL = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1_summary.csv"
HEADER_DEGENERACY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv"
NULL_SEEDS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    domain = read_one(DOMAIN)
    redshift = read_one(REDSHIFT)
    route_tiles = read_one(ROUTE_TILES)
    mask_shell = read_one(MASK_SHELL)
    header_degeneracy = read_one(HEADER_DEGENERACY)
    null_seeds = read_one(NULL_SEEDS)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("path-weight construction policy must remain endpoint disabled")
    if policy["current_tile_weights_computed"].lower() != "false":
        raise SystemExit("path-weight construction rule must not compute tile weights")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("path-weight construction rule must not compute path mapping")
    if domain["domain_rows"] != "58800":
        raise SystemExit("path-weight construction rule requires the 58,800-row domain")

    rows = [
        {
            "factor_id": "N_pair",
            "factor_role": "tomographic_redshift_pair_factor",
            "source_state": "available_for_future_rule",
            "evidence_artifact": "data/derived/kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv",
            "source_count": redshift["n_source_bins"],
            "numeric_factor_computed": "false",
            "blocking_status": "not_blocking",
            "limitation": "source_redshift_summaries_available_but_no_weight_formula_evaluated",
        },
        {
            "factor_id": "T_tile",
            "factor_role": "route_tile_coordinate_factor",
            "source_state": "available_for_future_rule",
            "evidence_artifact": "data/derived/kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv",
            "source_count": route_tiles["tile_count"],
            "numeric_factor_computed": "false",
            "blocking_status": "not_blocking",
            "limitation": "filename_tile_coordinates_available_but_no_footprint_or_weight",
        },
        {
            "factor_id": "F_overlap",
            "factor_role": "row_tile_footprint_overlap_factor",
            "source_state": "available_uniform_not_promotable",
            "evidence_artifact": "data/derived/kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv",
            "source_count": header_degeneracy["tile_count"],
            "numeric_factor_computed": "false",
            "blocking_status": "blocking",
            "limitation": "header_footprint_rule_exists_but_is_uniform_requires_pixel_mask_or_subtile_overlap",
        },
        {
            "factor_id": "D_path",
            "factor_role": "depth_mask_path_load_factor",
            "source_state": "partial_available",
            "evidence_artifact": "data/derived/kids1000_dr4_path_mask_observable_shell_v1_summary.csv",
            "source_count": mask_shell["subset_count"],
            "numeric_factor_computed": "false",
            "blocking_status": "partial_blocking",
            "limitation": "three_mask_shell_only_no_full_depth_path_load_semantics",
        },
        {
            "factor_id": "E_web",
            "factor_role": "web_environment_factor",
            "source_state": "missing",
            "evidence_artifact": "data/source_manifest/kids1000_cosebis_web_path_mapping_policy_v1.csv",
            "source_count": "0",
            "numeric_factor_computed": "false",
            "blocking_status": "blocking",
            "limitation": "no_source_frozen_web_environment_catalog_for_kids_footprint",
        },
        {
            "factor_id": "C_norm",
            "factor_role": "normalization_rule",
            "source_state": "declared_not_computed",
            "evidence_artifact": "data/source_manifest/kids1000_cosebis_path_weight_construction_rule_v1.csv",
            "source_count": "0",
            "numeric_factor_computed": "false",
            "blocking_status": "blocking_until_factors_exist",
            "limitation": "normalization_rule_cannot_be_evaluated_without_nonzero_source_frozen_factors",
        },
        {
            "factor_id": "null_controls",
            "factor_role": "future_control_execution",
            "source_state": "declared_not_executed",
            "evidence_artifact": "data/derived/kids1000_cosebis_null_control_seed_inventory_v1_summary.csv",
            "source_count": null_seeds["total_declared_control_draws"],
            "numeric_factor_computed": "false",
            "blocking_status": "blocking_until_mapping_exists",
            "limitation": "controls_declared_but_not_run_and_no_mapping_vector_exists",
        },
    ]
    for row in rows:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "construction_rule_name": policy["construction_rule_name"],
                "domain_rows": domain["domain_rows"],
                "tile_weights_computed": "false",
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
                "claim_boundary": "kids1000_cosebis_path_weight_construction_rule_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_BUILT_NOT_COMPUTED",
        "factor_count": str(len(rows)),
        "available_factor_count": str(sum(row["source_state"] == "available_for_future_rule" for row in rows)),
        "available_uniform_not_promotable_factor_count": str(
            sum(row["source_state"] == "available_uniform_not_promotable" for row in rows)
        ),
        "partial_available_factor_count": str(sum(row["source_state"] == "partial_available" for row in rows)),
        "missing_factor_count": str(sum(row["source_state"] == "missing" for row in rows)),
        "declared_not_computed_factor_count": str(sum(row["source_state"] == "declared_not_computed" for row in rows)),
        "declared_not_executed_factor_count": str(sum(row["source_state"] == "declared_not_executed" for row in rows)),
        "domain_rows": domain["domain_rows"],
        "path_weight_rule_computable": "false",
        "tile_weights_computed": "false",
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
        "claim_boundary": "kids1000_cosebis_path_weight_construction_rule_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_V1_BUILT "
        f"factors={len(rows)} computable=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
