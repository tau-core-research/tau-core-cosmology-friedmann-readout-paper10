#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_policy_v1.csv"
BATCH_PLAN = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1.csv"
DRY_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
DRY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv"
EXECUTION_LOG_DIR = ROOT / "data" / "local" / "weak_lensing" / "kids1000_cosebis_f_overlap_batch_execute_logs_v1"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run or execute one KiDS F_overlap full-mask acquisition batch."
    )
    parser.add_argument("--batch-index", type=int, default=None, help="Zero-based batch index to inspect or fetch.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually fetch the batch into the ignored cache. Reproduce does not use this.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("batch dry-run policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("batch dry-run policy must not compute path mapping")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("batch dry-run policy must not compute overlap")

    batch_index = args.batch_index
    if batch_index is None:
        batch_index = int(policy["default_batch_index"])
    with BATCH_PLAN.open(newline="") as f:
        plan_rows = list(csv.DictReader(f))
    selected = [row for row in plan_rows if int(row["batch_index_zero_based"]) == batch_index]
    if len(selected) != 1:
        raise SystemExit(f"batch {batch_index} not found")
    batch = selected[0]
    urls = batch["mask_product_urls"].split(";")
    paths = [ROOT / rel for rel in batch["expected_cache_paths"].split(";")]
    tile_indices = batch["tile_indices_zero_based"].split(";")
    if len(urls) != int(batch["batch_size"]) or len(paths) != len(urls) or len(tile_indices) != len(urls):
        raise SystemExit("batch plan row has inconsistent list lengths")

    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat() if args.execute else ""
    rows: list[dict[str, str]] = []
    for tile_index, url, local_path in zip(tile_indices, urls, paths):
        local_path.parent.mkdir(parents=True, exist_ok=True)
        existed_before = local_path.exists() if args.execute else False
        http_status = ""
        byte_count = ""
        sha256 = ""
        fetch_status = "dry_run_not_fetched"
        if args.execute:
            response = requests.get(
                url,
                timeout=90,
                headers={"User-Agent": "tau-core-paper10-kids-full-mask-batch/0.1"},
            )
            response.raise_for_status()
            content = response.content
            local_path.write_bytes(content)
            http_status = str(response.status_code)
            byte_count = str(len(content))
            sha256 = sha256_bytes(content)
            fetch_status = "fetched"
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "batch_index_zero_based": str(batch_index),
                "batch_id": batch["batch_id"],
                "tile_index_zero_based": tile_index,
                "mask_product_url": url,
                "expected_cache_path": str(local_path.relative_to(ROOT)),
                "local_file_existed_before": "true" if existed_before else "false",
                "fetch_mode": "execute" if args.execute else "dry_run",
                "fetch_status": fetch_status,
                "http_status": http_status,
                "byte_count": byte_count,
                "sha256": sha256,
                "fetched_at_utc": fetched_at,
                "external_products_fetched": "true" if args.execute else "false",
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
                "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_not_mapping_not_validation"
                if not args.execute
                else "kids1000_cosebis_f_overlap_full_mask_batch_fetch_not_mapping_not_validation",
            }
        )

    if args.execute:
        output_path = EXECUTION_LOG_DIR / f"kids1000_cosebis_f_overlap_full_mask_batch_execute_{batch_index:02d}_v1.csv"
        summary_path = (
            EXECUTION_LOG_DIR
            / f"kids1000_cosebis_f_overlap_full_mask_batch_execute_{batch_index:02d}_v1_summary.csv"
        )
    else:
        output_path = DRY_OUT
        summary_path = DRY_SUMMARY

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_DRY_RUN_BUILT_NOT_FETCHED"
        if not args.execute
        else "KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_FETCHED_NOT_MAPPED",
        "batch_index_zero_based": str(batch_index),
        "batch_id": batch["batch_id"],
        "batch_size": str(len(rows)),
        "fetch_mode": "execute" if args.execute else "dry_run",
        "batch_fetch_executed": "true" if args.execute else "false",
        "external_products_fetched": "true" if args.execute else "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_not_mapping_not_validation"
        if not args.execute
        else "kids1000_cosebis_f_overlap_full_mask_batch_fetch_not_mapping_not_validation",
    }
    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FULL_MASK_BATCH_V1 "
        f"batch={batch_index} mode={summary['fetch_mode']} size={len(rows)} "
        f"output={output_path.relative_to(ROOT)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
