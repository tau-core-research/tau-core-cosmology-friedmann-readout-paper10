#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_DECLARED_NOT_EXECUTED":
        raise SystemExit("unexpected execution-review schema policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("execution-review schema policy must remain endpoint disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_BUILT_NOT_EXECUTED":
        raise SystemExit("unexpected execution-review schema summary status")
    if summary["schema_column_count"] != "29":
        raise SystemExit("unexpected execution-review schema column count")
    if summary["forbidden_true_column_count"] != "13":
        raise SystemExit("unexpected forbidden-if-true column count")
    if summary["promotion_ready"] != "false":
        raise SystemExit("schema should attach to a not-ready promotion gate")
    required_columns = {row["column_name"] for row in rows}
    for column in [
        "batch_id",
        "tile_index_zero_based",
        "mask_product_url",
        "expected_cache_path",
        "fetch_status",
        "sha256",
        "review_artifact_status",
        "forbidden_inputs_used",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_lensing_residuals",
        "uses_fit_improvement_flags",
        "uses_posthoc_tile_selection",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_theory_vector",
        "contains_residuals",
        "endpoint_scoring_allowed",
        "claim_boundary",
    ]:
        if column not in required_columns:
            raise SystemExit(f"missing required execution-review column: {column}")
    by_column = {row["column_name"]: row for row in rows}
    for column in [
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_lensing_residuals",
        "uses_fit_improvement_flags",
        "uses_posthoc_tile_selection",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
    ]:
        if by_column[column]["forbidden_if_true"] != "true":
            raise SystemExit(f"{column} must be forbidden if true")
    for key in [
        "external_products_fetched",
        "overlap_rule_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
