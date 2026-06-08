#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected batch dry-run policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("batch dry-run policy must remain endpoint disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected batch dry-run summary status")
    if summary["batch_index_zero_based"] != policy["default_batch_index"]:
        raise SystemExit("dry-run must use the default declared batch index")
    if summary["batch_size"] != "20":
        raise SystemExit("default dry-run batch should contain 20 files")
    if summary["fetch_mode"] != "dry_run":
        raise SystemExit("reproducibility run must stay in dry-run mode")
    if summary["batch_fetch_executed"] != "false":
        raise SystemExit("dry-run must not execute fetch")
    if len(rows) != 20:
        raise SystemExit("dry-run output must contain the 20 selected batch rows")
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
    if any(row["fetch_mode"] != "dry_run" for row in rows):
        raise SystemExit("row fetch modes must remain dry_run")
    if any(row["fetch_status"] != "dry_run_not_fetched" for row in rows):
        raise SystemExit("row fetch statuses must remain dry_run_not_fetched")
    if any(row["http_status"] or row["byte_count"] or row["sha256"] for row in rows):
        raise SystemExit("dry-run rows must not contain network fetch outputs")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
