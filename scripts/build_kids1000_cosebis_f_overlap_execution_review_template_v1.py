#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv"
SCHEMA = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
DRY_RUN = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("execution-review template policy must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("execution-review template must not fetch products")
    with SCHEMA.open(newline="") as f:
        schema_rows = list(csv.DictReader(f))
    required_columns = [row["column_name"] for row in sorted(schema_rows, key=lambda row: int(row["column_order"]))]
    with DRY_RUN.open(newline="") as f:
        dry_rows = list(csv.DictReader(f))
    if len(dry_rows) != 20:
        raise SystemExit("execution-review template currently targets the default 20-row dry-run batch")

    rows: list[dict[str, str]] = []
    for dry in dry_rows:
        row = {
            "policy_id": policy["policy_id"],
            "batch_id": dry["batch_id"],
            "batch_index_zero_based": dry["batch_index_zero_based"],
            "tile_index_zero_based": dry["tile_index_zero_based"],
            "mask_product_url": dry["mask_product_url"],
            "expected_cache_path": dry["expected_cache_path"],
            "fetch_mode": "template_not_executed",
            "fetch_status": "template_not_fetched",
            "http_status": "",
            "byte_count": "",
            "sha256": "",
            "fetched_at_utc": "",
            "review_artifact_status": "template_pending_manual_execution_review",
            "reviewer_id_or_role": "",
            "forbidden_inputs_used": "false",
            "uses_kids_data_vector_values": "false",
            "uses_posterior_chains": "false",
            "uses_lensing_residuals": "false",
            "uses_fit_improvement_flags": "false",
            "uses_posthoc_tile_selection": "false",
            "overlap_rule_computed": "false",
            "path_mapping_computed": "false",
            "contains_mapping_vector": "false",
            "contains_theory_vector": "false",
            "contains_predictions": "false",
            "contains_residuals": "false",
            "contains_fit_statistics": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "kids1000_cosebis_f_overlap_execution_review_template_not_fetch_not_overlap_not_mapping_not_validation",
        }
        if set(row) != set(required_columns):
            missing = sorted(set(required_columns) - set(row))
            extra = sorted(set(row) - set(required_columns))
            raise SystemExit(f"template row does not match schema: missing={missing} extra={extra}")
        rows.append({column: row[column] for column in required_columns})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=required_columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_BUILT_NOT_EXECUTED",
        "batch_id": rows[0]["batch_id"],
        "batch_index_zero_based": rows[0]["batch_index_zero_based"],
        "template_row_count": str(len(rows)),
        "schema_column_count": str(len(required_columns)),
        "template_fetch_mode": "template_not_executed",
        "template_fetch_status": "template_not_fetched",
        "current_execution_review_artifact_present": "false",
        "external_products_fetched": "false",
        "overlap_rule_computed": "false",
        "numeric_factors_computed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_f_overlap_execution_review_template_not_fetch_not_overlap_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_V1_BUILT "
        f"rows={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
