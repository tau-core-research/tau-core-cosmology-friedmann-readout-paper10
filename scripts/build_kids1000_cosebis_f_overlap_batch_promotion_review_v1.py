#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_batch_promotion_review_policy_v1.csv"
DRY_RUN = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
DRY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1_summary.csv"
BATCH_PLAN_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_plan_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    dry_summary = read_one(DRY_SUMMARY)
    batch_plan = read_one(BATCH_PLAN_SUMMARY)
    with DRY_RUN.open(newline="") as f:
        dry_rows = list(csv.DictReader(f))

    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("promotion review policy must remain endpoint disabled")
    if policy["current_overlap_rule_computed"].lower() != "false":
        raise SystemExit("promotion review policy must not compute overlap")
    if dry_summary["fetch_mode"] != "dry_run":
        raise SystemExit("promotion review must attach to committed dry-run output")
    if dry_summary["external_products_fetched"] != "false":
        raise SystemExit("committed dry-run must remain unfetched")

    # This public review gate is intentionally deterministic: it does not read ignored
    # data/local execution logs. A fetched batch becomes reviewable only after a
    # committed source-freeze review artifact with checksums exists in the package.
    requirements = [
        {
            "requirement_id": "PROMOTE_01_EXECUTION_REVIEW_ARTIFACT",
            "requirement": "committed_execution_review_artifact_exists",
            "status": "missing",
            "evidence": "none",
            "why_required": "manual_execute_logs_under_data_local_are_machine_local_and_not_reproducible",
            "blocks_promotion": "true",
        },
        {
            "requirement_id": "PROMOTE_02_CHECKSUM_MANIFEST",
            "requirement": "sha256_or_provider_checksum_manifest_committed",
            "status": "missing",
            "evidence": "none",
            "why_required": "fetched_fits_products_must_be_content_locked_before_any_overlap_derivation",
            "blocks_promotion": "true",
        },
        {
            "requirement_id": "PROMOTE_03_BATCH_PRODUCT_COUNT",
            "requirement": "all_products_for_declared_batch_accounted_for",
            "status": "not_reviewable",
            "evidence": "dry_run_batch_size_only",
            "why_required": "batch_promotion_requires_source_freeze_artifact_not_dry_run_urls",
            "blocks_promotion": "true",
        },
        {
            "requirement_id": "PROMOTE_04_FORBIDDEN_INPUT_AUDIT",
            "requirement": "no_endpoint_or_posterior_inputs_used_for_promotion",
            "status": "not_reviewable",
            "evidence": "no_committed_execution_review_artifact",
            "why_required": "promotion_must_be_source_side_not_likelihood_or_residual_selected",
            "blocks_promotion": "true",
        },
        {
            "requirement_id": "PROMOTE_05_OVERLAP_DERIVATION_STILL_SEPARATE",
            "requirement": "overlap_rule_derivation_not_performed_in_promotion_gate",
            "status": "satisfied_not_computed",
            "evidence": "promotion_gate_has_no_overlap_columns_or_values",
            "why_required": "batch_fetch_review_is_not_an_overlap_factor",
            "blocks_promotion": "false",
        },
        {
            "requirement_id": "PROMOTE_06_FILLED_REVIEW_VALIDATOR_AVAILABLE",
            "requirement": "filled_execution_review_artifact_validator_available",
            "status": "satisfied_not_executed",
            "evidence": "scripts/validate_kids1000_cosebis_f_overlap_filled_execution_review_artifact_v1.py",
            "why_required": "future_filled_review_artifacts_must_be_checked_against_frozen_schema_and_dry_run_identity",
            "blocks_promotion": "false",
        },
    ]
    rows: list[dict[str, str]] = []
    for row in requirements:
        row.update(
            {
                "policy_id": policy["policy_id"],
                "dry_run_batch_id": dry_summary["batch_id"],
                "dry_run_batch_size": dry_summary["batch_size"],
                "planned_total_batch_count": batch_plan["batch_count"],
                "planned_missing_mask_count": batch_plan["missing_mask_count"],
                "dry_run_row_count": str(len(dry_rows)),
                "promotion_ready": "false",
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
                "claim_boundary": "kids1000_cosebis_f_overlap_batch_promotion_review_not_overlap_not_mapping_not_validation",
            }
        )
        rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    blockers = [row for row in rows if row["blocks_promotion"] == "true"]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_BUILT_NOT_READY",
        "dry_run_batch_id": dry_summary["batch_id"],
        "dry_run_batch_size": dry_summary["batch_size"],
        "planned_total_batch_count": batch_plan["batch_count"],
        "planned_missing_mask_count": batch_plan["missing_mask_count"],
        "requirement_count": str(len(rows)),
        "blocking_requirement_count": str(len(blockers)),
        "promotion_ready": "false",
        "first_blocker": blockers[0]["requirement_id"],
        "execution_review_artifact_present": "false",
        "checksum_manifest_present": "false",
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
        "claim_boundary": "kids1000_cosebis_f_overlap_batch_promotion_review_not_overlap_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_BATCH_PROMOTION_REVIEW_V1_BUILT "
        f"ready=false blockers={len(blockers)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
