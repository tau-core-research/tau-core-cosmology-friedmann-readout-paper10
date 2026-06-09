#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_e_web_null_control_rule_policy_v1.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
OUT_TILE = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_tile_rule_v1.csv"
OUT_DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("E_web null-control policy must keep endpoint scoring disabled")
    if policy["positive_web_claim_allowed"].lower() != "false":
        raise SystemExit("E_web null-control policy must forbid positive web claims")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("E_web null-control rule must not compute path mapping")
    if policy["current_theory_vector_computed"].lower() != "false":
        raise SystemExit("E_web null-control rule must not compute theory vectors")

    domain_rows = read_rows(DOMAIN)
    tile_rows_in = read_rows(ROUTE_TILES)
    if len(tile_rows_in) != int(policy["expected_tile_count"]):
        raise SystemExit("E_web null-control rule expects 196 route tiles")
    if len(domain_rows) != int(policy["expected_domain_rows"]):
        raise SystemExit("E_web null-control rule expects 58,800 domain rows")

    tile_rows: list[dict[str, str]] = []
    for row in tile_rows_in:
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "mask_product_url": row["mask_product_url"],
                "source_scope": policy["source_scope"],
                "e_web_rule": policy["e_web_rule"],
                "e_web_null_control_value": "1.000000000000e+00",
                "e_web_null_control_computed": "true",
                "positive_web_claim_allowed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "uses_posthoc_web_environment_labels": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    domain_out: list[dict[str, str]] = []
    for row in domain_rows:
        domain_out.append(
            {
                "policy_id": policy["policy_id"],
                "domain_row_index_zero_based": row["domain_row_index_zero_based"],
                "target_row_index_zero_based": row["target_row_index_zero_based"],
                "tile_index_zero_based": row["tile_index_zero_based"],
                "pair_id": row["pair_id"],
                "mode": row["mode"],
                "source_scope": policy["source_scope"],
                "e_web_rule": policy["e_web_rule"],
                "e_web_value": "1.000000000000e+00",
                "e_web_null_control_computed": "true",
                "positive_web_claim_allowed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "uses_posthoc_web_environment_labels": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    OUT_TILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TILE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tile_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(tile_rows)
    with OUT_DOMAIN.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(domain_out[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(domain_out)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED",
        "tile_count": str(len(tile_rows)),
        "target_rows": policy["expected_target_rows"],
        "domain_rows": str(len(domain_out)),
        "source_scope": policy["source_scope"],
        "e_web_rule": policy["e_web_rule"],
        "min_e_web_value": "1.000000000000e+00",
        "max_e_web_value": "1.000000000000e+00",
        "mean_e_web_value": "1.000000000000e+00",
        "unique_e_web_value_count_rounded_1e_minus_12": "1",
        "e_web_null_control_uniform": "true",
        "e_web_source_route_support": "true",
        "positive_web_claim_allowed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "uses_posthoc_sky_direction_selection": "false",
        "uses_posthoc_web_environment_labels": "false",
        "uses_posthoc_path_projection_labels": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_V1_BUILT "
        f"domain_rows={len(domain_out)} positive_web_claim=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
