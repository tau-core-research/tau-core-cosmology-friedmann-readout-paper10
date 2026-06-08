#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv"
TOMO = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1.csv"
REDSHIFT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    route_tiles = read_one(ROUTE_TILES)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("design skeleton policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("design skeleton must not compute path mapping")
    if policy["current_path_weights_computed"].lower() != "false":
        raise SystemExit("design skeleton must not compute path weights")
    if route_tiles["tile_count"] != policy["route_tile_count"]:
        raise SystemExit("route tile count mismatch")

    with TOMO.open(newline="") as f:
        tomo_rows = list(csv.DictReader(f))
    with REDSHIFT.open(newline="") as f:
        redshift_rows = list(csv.DictReader(f))
    if sum(int(row["rows_for_pair"]) for row in tomo_rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected target row count from tomographic inventory")

    redshift_by_bin = {row["source_bin"]: row for row in redshift_rows}
    rows: list[dict[str, str]] = []
    target_row_index = 0
    for tomo in tomo_rows:
        bin1 = tomo["bin1"]
        bin2 = tomo["bin2"]
        z1 = redshift_by_bin[bin1]
        z2 = redshift_by_bin[bin2]
        for mode in tomo["modes"].split(";"):
            rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "target_row_index_zero_based": str(target_row_index),
                    "selected_statistic": "COSEBIs",
                    "selected_hdu_data_vector": tomo["selected_hdu_data_vector"],
                    "pair_id": tomo["pair_id"],
                    "bin1": bin1,
                    "bin2": bin2,
                    "mode": mode,
                    "bin1_mean_z": z1["mean_z"],
                    "bin2_mean_z": z2["mean_z"],
                    "bin1_support_z_min_nonzero": z1["support_z_min_nonzero"],
                    "bin1_support_z_max_nonzero": z1["support_z_max_nonzero"],
                    "bin2_support_z_min_nonzero": z2["support_z_min_nonzero"],
                    "bin2_support_z_max_nonzero": z2["support_z_max_nonzero"],
                    "preferred_route_tile_count": route_tiles["tile_count"],
                    "preferred_route_ra_min_deg_filename_proxy": route_tiles["min_tile_ra_deg_filename_proxy"],
                    "preferred_route_ra_max_deg_filename_proxy": route_tiles["max_tile_ra_deg_filename_proxy"],
                    "preferred_route_dec_min_deg_filename_proxy": route_tiles["min_tile_dec_deg_filename_proxy"],
                    "preferred_route_dec_max_deg_filename_proxy": route_tiles["max_tile_dec_deg_filename_proxy"],
                    "design_skeleton_computed": "true",
                    "path_weights_computed": "false",
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
                    "claim_boundary": "kids1000_cosebis_path_mapping_design_skeleton_not_mapping_not_validation",
                }
            )
            target_row_index += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_BUILT_NOT_MAPPED",
        "target_rows": str(len(rows)),
        "tomographic_pair_count": str(len(tomo_rows)),
        "mode_count_per_pair": tomo_rows[0]["n_modes"],
        "route_tile_count": route_tiles["tile_count"],
        "design_skeleton_computed": "true",
        "path_weights_computed": "false",
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
        "claim_boundary": "kids1000_cosebis_path_mapping_design_skeleton_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_V1_BUILT "
        f"rows={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
