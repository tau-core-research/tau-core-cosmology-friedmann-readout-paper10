#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_acquisition_policy_v1.csv"
AVAILABILITY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1_summary.csv"
ROUTE_TILES = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
RAW_DIR = ROOT / "data" / "raw" / "weak_lensing" / "kids1000_path_masks" / "mask_subset_v1"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("full-mask acquisition manifest must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("full-mask acquisition manifest must not fetch products")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("full-mask acquisition manifest must not compute overlap")
    availability = read_one(AVAILABILITY)
    if availability["overlap_rule_ready"] != "false":
        raise SystemExit("full-mask acquisition manifest expects unresolved F_overlap")

    with ROUTE_TILES.open(newline="") as f:
        route_rows = list(csv.DictReader(f))
    if len(route_rows) != int(availability["expected_route_tile_count"]):
        raise SystemExit("route tile inventory does not match expected F_overlap route count")

    rows: list[dict[str, str]] = []
    for route in route_rows:
        url = route["mask_product_url"]
        filename = url.rsplit("/", 1)[-1]
        local_path = RAW_DIR / filename
        local_present = local_path.exists()
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "tile_index_zero_based": route["tile_index_zero_based"],
                "mask_product_url": url,
                "expected_local_path": str(local_path.relative_to(ROOT)),
                "tile_ra_deg_filename_proxy": route["tile_ra_deg_filename_proxy"],
                "tile_dec_deg_filename_proxy": route["tile_dec_deg_filename_proxy"],
                "local_mask_present": "true" if local_present else "false",
                "mask_product_fetch_required": "false" if local_present else "true",
                "accepted_for_full_overlap": "false",
                "acceptance_status": "local_file_present_but_full_set_incomplete"
                if local_present
                else "missing_required_for_full_set",
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
                "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_acquisition_not_mapping_not_validation",
            }
        )

    local_present_count = sum(row["local_mask_present"] == "true" for row in rows)
    missing_count = sum(row["local_mask_present"] == "false" for row in rows)
    full_set_present = missing_count == 0
    if full_set_present:
        for row in rows:
            row["accepted_for_full_overlap"] = "true"
            row["acceptance_status"] = "accepted_full_mask_set_present"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_MANIFEST_BUILT_NOT_FETCHED",
        "expected_mask_count": str(len(rows)),
        "local_present_count": str(local_present_count),
        "missing_mask_count": str(missing_count),
        "full_mask_set_present": "true" if full_set_present else "false",
        "accepted_for_full_overlap_count": str(sum(row["accepted_for_full_overlap"] == "true" for row in rows)),
        "overlap_rule_ready": "true" if full_set_present else "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_acquisition_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_ACQUISITION_MANIFEST_V1_BUILT "
        f"present={local_present_count} missing={missing_count} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
