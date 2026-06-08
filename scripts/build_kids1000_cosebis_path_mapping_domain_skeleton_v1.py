#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv"
DESIGN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1.csv"
TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("domain skeleton policy must remain endpoint disabled")
    if policy["current_tile_weights_computed"].lower() != "false":
        raise SystemExit("domain skeleton must not compute tile weights")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("domain skeleton must not compute path mapping")

    with DESIGN.open(newline="") as f:
        design_rows = list(csv.DictReader(f))
    with TILES.open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    if len(design_rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected design row count")
    if len(tile_rows) != int(policy["expected_tile_count"]):
        raise SystemExit("unexpected tile row count")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "policy_id",
        "domain_row_index_zero_based",
        "target_row_index_zero_based",
        "tile_index_zero_based",
        "pair_id",
        "bin1",
        "bin2",
        "mode",
        "bin1_mean_z",
        "bin2_mean_z",
        "tile_ra_deg_filename_proxy",
        "tile_dec_deg_filename_proxy",
        "tile_coordinate_source",
        "domain_skeleton_computed",
        "tile_weight_computed",
        "footprint_overlap_computed",
        "path_weight_computed",
        "web_environment_label_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "endpoint_scoring_allowed",
        "claim_boundary",
    ]
    domain_row_index = 0
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for design in design_rows:
            for tile in tile_rows:
                writer.writerow(
                    {
                        "policy_id": policy["policy_id"],
                        "domain_row_index_zero_based": str(domain_row_index),
                        "target_row_index_zero_based": design["target_row_index_zero_based"],
                        "tile_index_zero_based": tile["tile_index_zero_based"],
                        "pair_id": design["pair_id"],
                        "bin1": design["bin1"],
                        "bin2": design["bin2"],
                        "mode": design["mode"],
                        "bin1_mean_z": design["bin1_mean_z"],
                        "bin2_mean_z": design["bin2_mean_z"],
                        "tile_ra_deg_filename_proxy": tile["tile_ra_deg_filename_proxy"],
                        "tile_dec_deg_filename_proxy": tile["tile_dec_deg_filename_proxy"],
                        "tile_coordinate_source": tile["tile_coordinate_source"],
                        "domain_skeleton_computed": "true",
                        "tile_weight_computed": "false",
                        "footprint_overlap_computed": "false",
                        "path_weight_computed": "false",
                        "web_environment_label_computed": "false",
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
                        "claim_boundary": "kids1000_cosebis_path_mapping_domain_skeleton_not_mapping_not_validation",
                    }
                )
                domain_row_index += 1

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_BUILT_NOT_MAPPED",
        "target_rows": str(len(design_rows)),
        "tile_count": str(len(tile_rows)),
        "domain_rows": str(domain_row_index),
        "domain_skeleton_computed": "true",
        "tile_weights_computed": "false",
        "footprint_overlap_computed": "false",
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
        "claim_boundary": "kids1000_cosebis_path_mapping_domain_skeleton_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_V1_BUILT "
        f"rows={domain_row_index} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
