#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_DECLARED_NOT_READY":
        raise SystemExit("unexpected promotion-review policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("promotion-review policy must remain endpoint disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_BUILT_NOT_READY":
        raise SystemExit("unexpected promotion-review summary status")
    if summary["dry_run_batch_id"] != "F_OVERLAP_FULL_MASK_BATCH_00":
        raise SystemExit("promotion review must attach to the committed default dry-run batch")
    if summary["dry_run_batch_size"] != "20":
        raise SystemExit("default dry-run batch should contain 20 products")
    if summary["planned_total_batch_count"] != "10":
        raise SystemExit("promotion review must preserve the ten-batch plan")
    if summary["planned_missing_mask_count"] != "193":
        raise SystemExit("promotion review must preserve the 193 missing-mask plan")
    if summary["requirement_count"] != "6":
        raise SystemExit("promotion review must contain six checklist requirements")
    if summary["blocking_requirement_count"] != "4":
        raise SystemExit("four requirements should currently block promotion")
    if summary["promotion_ready"] != "false":
        raise SystemExit("promotion must not be ready without committed execution review")
    if summary["first_blocker"] != "PROMOTE_01_EXECUTION_REVIEW_ARTIFACT":
        raise SystemExit("first promotion blocker should be the absent execution review artifact")
    expected_ids = {
        "PROMOTE_01_EXECUTION_REVIEW_ARTIFACT",
        "PROMOTE_02_CHECKSUM_MANIFEST",
        "PROMOTE_03_BATCH_PRODUCT_COUNT",
        "PROMOTE_04_FORBIDDEN_INPUT_AUDIT",
        "PROMOTE_05_OVERLAP_DERIVATION_STILL_SEPARATE",
        "PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE",
    }
    if {row["requirement_id"] for row in rows} != expected_ids:
        raise SystemExit("unexpected promotion checklist requirements")
    if any(row["promotion_ready"] != "false" for row in rows):
        raise SystemExit("all rows must keep promotion_ready=false")
    by_id = {row["requirement_id"]: row for row in rows}
    if by_id["PROMOTE_05_OVERLAP_DERIVATION_STILL_SEPARATE"]["blocks_promotion"] != "false":
        raise SystemExit("the separate-overlap-derivation reminder should not itself block promotion")
    if by_id["PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE"]["blocks_promotion"] != "false":
        raise SystemExit("the filled-review validator availability row should not itself block promotion")
    for key in [
        "external_products_fetched",
        "overlap_rule_computed",
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
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
