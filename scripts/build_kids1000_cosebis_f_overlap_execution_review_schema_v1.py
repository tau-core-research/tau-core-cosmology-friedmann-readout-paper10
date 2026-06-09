#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_execution_review_schema_policy_v1.csv"
PROMOTION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    promotion = read_one(PROMOTION_SUMMARY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("execution-review schema policy must remain endpoint disabled")
    if policy["current_external_products_fetched"].lower() != "false":
        raise SystemExit("execution-review schema declaration must not fetch products")
    if promotion["promotion_ready"] != "false":
        raise SystemExit("schema declaration expects the promotion gate to remain not ready")

    schema_rows = [
        ("policy_id", "string", "identifier", "required", "links_review_to_policy", "false"),
        ("batch_id", "string", "batch_identity", "required", "must_match_declared_batch_plan", "false"),
        ("batch_index_zero_based", "integer", "batch_identity", "required", "must_match_declared_batch_plan", "false"),
        ("tile_index_zero_based", "integer", "product_identity", "required", "must_match_declared_tile_index", "false"),
        ("mask_product_url", "url", "product_source", "required", "must_match_route_manifest_url", "false"),
        ("expected_cache_path", "relative_path", "product_source", "required", "must_match_declared_ignored_cache_path", "false"),
        ("fetch_mode", "enum", "execution_metadata", "required", "must_be_execute_for_promoted_review", "false"),
        ("fetch_status", "enum", "execution_metadata", "required", "must_be_fetched_or_failed_with_reason", "false"),
        ("http_status", "integer_or_empty", "execution_metadata", "required", "network_status_only_not_scoring", "false"),
        ("byte_count", "integer_or_empty", "checksum_input", "required", "content_accounting_only", "false"),
        ("sha256", "hex_or_empty", "checksum_input", "required", "content_lock_for_fetched_product", "false"),
        ("fetched_at_utc", "iso8601_or_empty", "execution_metadata", "required", "provenance_timestamp_only", "false"),
        ("review_artifact_status", "enum", "review_status", "required", "accepted_or_rejected_source_freeze_review_state", "false"),
        ("reviewer_id_or_role", "string", "review_status", "required", "records_independent_review_role_without_private_identity", "false"),
        ("forbidden_inputs_used", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "false"),
        ("uses_kids_data_vector_values", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "true"),
        ("uses_posterior_chains", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "true"),
        ("uses_lensing_residuals", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "true"),
        ("uses_fit_improvement_flags", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "true"),
        ("uses_posthoc_tile_selection", "boolean", "leakage_audit", "required", "must_be_false_for_any_promotion", "true"),
        ("overlap_rule_computed", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("path_mapping_computed", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("contains_mapping_vector", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("contains_theory_vector", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("contains_predictions", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("contains_residuals", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("contains_fit_statistics", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("endpoint_scoring_allowed", "boolean", "claim_boundary", "required", "must_be_false_in_execution_review", "true"),
        ("claim_boundary", "string", "claim_boundary", "required", "must_state_fetch_review_not_overlap_not_validation", "false"),
    ]
    rows = []
    for index, (column_name, value_type, column_role, requirement_status, review_rule, forbidden_if_true) in enumerate(
        schema_rows, start=1
    ):
        rows.append(
            {
                "schema_policy_id": policy["policy_id"],
                "column_order": str(index),
                "column_name": column_name,
                "value_type": value_type,
                "column_role": column_role,
                "requirement_status": requirement_status,
                "review_rule": review_rule,
                "forbidden_if_true": forbidden_if_true,
                "current_execution_review_artifact_present": "false",
                "external_products_fetched": "false",
                "overlap_rule_computed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_f_overlap_execution_review_schema_not_fetch_not_overlap_not_mapping_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    forbidden_true_columns = [row for row in rows if row["forbidden_if_true"] == "true"]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_BUILT_NOT_EXECUTED",
        "schema_column_count": str(len(rows)),
        "forbidden_true_column_count": str(len(forbidden_true_columns)),
        "promotion_ready": promotion["promotion_ready"],
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
        "claim_boundary": "kids1000_cosebis_f_overlap_execution_review_schema_not_fetch_not_overlap_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_EXECUTION_REVIEW_SCHEMA_V1_BUILT "
        f"columns={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
