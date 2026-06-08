#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_policy_v1.csv"
FULL_MASK_MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv"
CACHE_DIR = ROOT / "data" / "raw" / "weak_lensing" / "kids1000_path_masks" / "full_route_cache_v1"
BATCH_SIZE = 20


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("full-mask batch plan must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("full-mask batch plan must not fetch products")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("full-mask batch plan must not compute overlap")

    with FULL_MASK_MANIFEST.open(newline="") as f:
        manifest_rows = list(csv.DictReader(f))
    missing = [row for row in manifest_rows if row["local_mask_present"] == "false"]
    present = [row for row in manifest_rows if row["local_mask_present"] == "true"]
    if len(manifest_rows) != 196:
        raise SystemExit("full-mask manifest must contain 196 rows")
    if not missing:
        raise SystemExit("batch plan expects missing masks; full set is already present")

    rows: list[dict[str, str]] = []
    batch_count = math.ceil(len(missing) / BATCH_SIZE)
    for batch_index in range(batch_count):
        batch_rows = missing[batch_index * BATCH_SIZE : (batch_index + 1) * BATCH_SIZE]
        tile_indices = ";".join(row["tile_index_zero_based"] for row in batch_rows)
        urls = ";".join(row["mask_product_url"] for row in batch_rows)
        expected_cache_paths = ";".join(
            str((CACHE_DIR / Path(row["expected_local_path"]).name).relative_to(ROOT)) for row in batch_rows
        )
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "batch_index_zero_based": str(batch_index),
                "batch_id": f"F_OVERLAP_FULL_MASK_BATCH_{batch_index:02d}",
                "batch_size": str(len(batch_rows)),
                "tile_indices_zero_based": tile_indices,
                "mask_product_urls": urls,
                "expected_cache_paths": expected_cache_paths,
                "cache_directory": str(CACHE_DIR.relative_to(ROOT)),
                "cache_git_policy": "large_fits_files_ignored_manifest_only_committed",
                "batch_fetch_executed": "false",
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
                "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_batch_plan_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_BUILT_NOT_FETCHED",
        "expected_mask_count": str(len(manifest_rows)),
        "local_present_count": str(len(present)),
        "missing_mask_count": str(len(missing)),
        "batch_size_limit": str(BATCH_SIZE),
        "batch_count": str(len(rows)),
        "cache_directory": str(CACHE_DIR.relative_to(ROOT)),
        "cache_git_policy": "large_fits_files_ignored_manifest_only_committed",
        "batch_fetches_executed": "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_batch_plan_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_PLAN_V1_BUILT "
        f"batches={len(rows)} missing={len(missing)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
