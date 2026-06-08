#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_head_sample_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_head_sample_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_head_sample_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("HEAD sample policy must remain endpoint disabled")
    if policy["current_mask_products_fetched"] != "false":
        raise SystemExit("HEAD sample policy must not fetch mask products")
    if policy["sample_rule"] != "first_middle_last_from_preferred_route":
        raise SystemExit("unexpected HEAD sample rule")
    if policy["sample_indices_zero_based"] != "0;98;195":
        raise SystemExit("unexpected HEAD sample indices")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("HEAD sample summary must remain endpoint disabled")
    if summary["status"] != "KIDS_DR4_PATH_MASK_HEAD_SAMPLE_CHECKED_NOT_FETCHED":
        raise SystemExit("unexpected HEAD sample status")
    if summary["sample_count"] != "3":
        raise SystemExit("HEAD sample must contain three rows")
    if summary["http_200_count"] != "3":
        raise SystemExit("all HEAD sample products must return HTTP 200")
    if int(summary["min_content_length"]) <= 0:
        raise SystemExit("HEAD sample products must have positive content length")
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
    if summary["mask_products_fetched"] != "false":
        raise SystemExit("summary must keep mask_products_fetched=false")
    if any(row["mask_product_fetched"] != "false" for row in rows):
        raise SystemExit("rows must keep mask_product_fetched=false")
    if [row["sample_index_zero_based"] for row in rows] != ["0", "98", "195"]:
        raise SystemExit("unexpected HEAD sample row order")
    for row in rows:
        if row["head_status"] != "HEAD_CHECKED_MASK_NOT_FETCHED":
            raise SystemExit("HEAD rows must remain metadata-only")
        if row["http_status"] != "200":
            raise SystemExit("HEAD rows must return HTTP 200")
        if int(row["content_length"]) <= 0:
            raise SystemExit("HEAD rows must expose positive content length")
        if "fits" not in row["content_type"].lower():
            raise SystemExit("HEAD rows should identify FITS content")
        if not row["mask_product_url"].endswith("_ugriZYJHKs_msk.fits.gz"):
            raise SystemExit("HEAD rows must target KiDS 9-band mask FITS products")
    for marker in [
        "posthoc_mask_subset_selection",
        "posthoc_path_projection_labels",
        "kids_data_vector_values",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS_DR4_PATH_MASK_HEAD_SAMPLE_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
