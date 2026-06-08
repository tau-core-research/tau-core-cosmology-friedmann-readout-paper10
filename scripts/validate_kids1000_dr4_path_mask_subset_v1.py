#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_subset_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mask subset policy must remain endpoint disabled")
    if policy["subset_rule"] != "promote_head_sample_first_middle_last_to_download_subset":
        raise SystemExit("unexpected mask subset rule")
    if policy["subset_indices_zero_based"] != "0;98;195":
        raise SystemExit("unexpected mask subset indices")
    if len(rows) != int(policy["expected_subset_count"]):
        raise SystemExit("unexpected mask subset size")
    if summary["status"] != "KIDS_DR4_PATH_MASK_SUBSET_FETCHED_INVENTORIED_NOT_SCORED":
        raise SystemExit("unexpected mask subset status")
    if summary["subset_count"] != policy["expected_subset_count"]:
        raise SystemExit("summary subset count mismatch")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mask subset summary must remain endpoint disabled")
    if summary["mask_products_fetched"] != "true":
        raise SystemExit("mask subset should fetch the selected mask products")
    if summary["mask_pixels_parsed"] != "true":
        raise SystemExit("mask subset should parse mask pixel arrays")
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_mask_subset_selection",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    if [row["sample_index_zero_based"] for row in rows] != ["0", "98", "195"]:
        raise SystemExit("unexpected mask subset row order")
    for row in rows:
        path = ROOT / row["local_path"]
        if not path.exists():
            raise SystemExit(f"missing mask subset product: {row['local_path']}")
        if row["http_status"] != "200":
            raise SystemExit("mask subset downloads must return HTTP 200")
        if int(row["byte_count"]) <= 0:
            raise SystemExit("mask subset products must be non-empty")
        if len(row["sha256"]) != 64:
            raise SystemExit("mask subset hashes must be sha256")
        if row["mask_product_fetched"] != "true":
            raise SystemExit("mask subset rows must mark products fetched")
        if row["mask_pixels_parsed"] != "true":
            raise SystemExit("mask subset rows must mark pixels parsed")
        if int(row["n_pixels"]) <= 0:
            raise SystemExit("mask products must contain pixels")
        if int(row["n_finite_pixels"]) <= 0:
            raise SystemExit("mask products must contain finite pixels")
        if float(row["finite_fraction"]) <= 0.0:
            raise SystemExit("mask finite fraction must be positive")
        if row["primary_shape"] == "":
            raise SystemExit("mask primary image shape must be recorded")
    for marker in [
        "posthoc_mask_subset_selection",
        "posthoc_path_projection_labels",
        "kids_data_vector_values",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS_DR4_PATH_MASK_SUBSET_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
