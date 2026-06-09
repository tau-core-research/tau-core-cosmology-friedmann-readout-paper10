#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_execution_review_template_policy_v1.csv"
SCHEMA = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_template_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with SCHEMA.open(newline="") as f:
        schema_rows = list(csv.DictReader(f))
    expected_columns = [row["column_name"] for row in sorted(schema_rows, key=lambda row: int(row["column_order"]))]
    with OUT.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        actual_columns = reader.fieldnames or []
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_DECLARED_NOT_EXECUTED":
        raise SystemExit("unexpected execution-review template policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("execution-review template policy must remain endpoint disabled")
    if actual_columns != expected_columns:
        raise SystemExit("execution-review template columns must exactly match the frozen schema")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_BUILT_NOT_EXECUTED":
        raise SystemExit("unexpected execution-review template summary status")
    if summary["batch_id"] != "F_OVERLAP_FULL_MASK_BATCH_00":
        raise SystemExit("template must target the default batch 0")
    if summary["template_row_count"] != "20":
        raise SystemExit("template must contain the 20 dry-run batch products")
    if summary["schema_column_count"] != "29":
        raise SystemExit("template must use the 29-column frozen schema")
    if summary["template_fetch_mode"] != "template_not_executed":
        raise SystemExit("template must not represent an executed fetch")
    if summary["template_fetch_status"] != "template_not_fetched":
        raise SystemExit("template must not represent fetched products")
    for key in [
        "current_execution_review_artifact_present",
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
    if len(rows) != 20:
        raise SystemExit("template row count mismatch")
    for row in rows:
        if row["fetch_mode"] != "template_not_executed":
            raise SystemExit("template rows must not be executed")
        if row["fetch_status"] != "template_not_fetched":
            raise SystemExit("template rows must not be fetched")
        if row["http_status"] or row["byte_count"] or row["sha256"] or row["fetched_at_utc"]:
            raise SystemExit("template rows must not include network or checksum outputs")
        for key in [
            "forbidden_inputs_used",
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
            if row[key] != "false":
                raise SystemExit(f"template rows must keep {key}=false")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_TEMPLATE_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
