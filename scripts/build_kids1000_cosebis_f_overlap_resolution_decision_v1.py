#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv"
SOURCE_AVAILABILITY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1.csv"
SOURCE_AVAILABILITY_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_source_availability_v1_summary.csv"
PROMOTION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_batch_promotion_review_v1_summary.csv"
ACQUISITION_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_acquisition_manifest_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    source_summary = read_one(SOURCE_AVAILABILITY_SUMMARY)
    promotion_summary = read_one(PROMOTION_SUMMARY)
    acquisition_summary = read_one(ACQUISITION_SUMMARY)
    with SOURCE_AVAILABILITY.open(newline="") as f:
        source_rows = list(csv.DictReader(f))

    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("F_overlap resolution decision must remain endpoint disabled")
    if policy["current_overlap_rule_computed"] != "false":
        raise SystemExit("F_overlap decision must not compute overlap")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("F_overlap decision must not compute path mapping")
    if source_summary["accepted_overlap_route_count"] != "0":
        raise SystemExit("current decision builder assumes no endpoint-accepted F_overlap route")
    if promotion_summary["promotion_ready"] != "false":
        raise SystemExit("batch promotion must remain not ready")
    if acquisition_summary["full_mask_set_present"] != "false":
        raise SystemExit("current decision builder assumes full mask set is not present")

    by_item = {row["availability_item_id"]: row for row in source_rows}
    rows = [
        {
            "decision_item_id": "F_OVERLAP_OFFICIAL_GEOMETRY_ROUTE",
            "source_evidence_item": "F_OVERLAP_OFFICIAL_GEOMETRY_PRODUCT",
            "decision_class": "rejected_unresolved",
            "endpoint_route_accepted": "false",
            "control_route_accepted": "false",
            "decision_reason": "official_KiDS_footprint_geometry_product_missing",
            "minimum_exit_condition": "source_frozen_official_footprint_geometry_or_equivalent_documented_provider_product",
        },
        {
            "decision_item_id": "F_OVERLAP_FULL_PIXEL_MASK_ROUTE",
            "source_evidence_item": "F_OVERLAP_FULL_PIXEL_MASK_SET",
            "decision_class": "rejected_unresolved",
            "endpoint_route_accepted": "false",
            "control_route_accepted": "false",
            "decision_reason": (
                f"full_196_mask_route_missing_present_{acquisition_summary['local_present_count']}_of_"
                f"{acquisition_summary['expected_mask_count']}"
            ),
            "minimum_exit_condition": "all_preferred_route_mask_products_source_frozen_with_checksums",
        },
        {
            "decision_item_id": "F_OVERLAP_THREE_MASK_SUBSET",
            "source_evidence_item": "F_OVERLAP_PIXEL_MASK_SUBSET",
            "decision_class": "accepted_caveated_control_only",
            "endpoint_route_accepted": "false",
            "control_route_accepted": "true",
            "decision_reason": "three_predeclared_masks_are_source_frozen_but_do_not_cover_full_survey_overlap",
            "minimum_exit_condition": "may_be_used_only_as_partial_path_mask_control_not_as_population_endpoint_overlap",
        },
        {
            "decision_item_id": "F_OVERLAP_BATCH0_DRY_RUN",
            "source_evidence_item": "F_OVERLAP_BATCH_PROMOTION_REVIEW",
            "decision_class": "rejected_unresolved",
            "endpoint_route_accepted": "false",
            "control_route_accepted": "false",
            "decision_reason": "batch0_is_dry_run_without_committed_execution_review_or_checksum_manifest",
            "minimum_exit_condition": "filled_execution_review_artifact_and_checksum_manifest_pass_validator",
        },
    ]
    for row in rows:
        evidence_item = row["source_evidence_item"]
        source_evidence = by_item.get(evidence_item, {})
        row.update(
            {
                "policy_id": policy["policy_id"],
                "availability_status": source_evidence.get("availability_status", "not_applicable"),
                "source_acceptance_status": source_evidence.get("acceptance_status", "not_applicable"),
                "source_count": source_evidence.get("source_count", promotion_summary.get("dry_run_batch_size", "0")),
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
                "claim_boundary": policy["claim_boundary"],
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    endpoint_routes = [row for row in rows if row["endpoint_route_accepted"] == "true"]
    control_routes = [row for row in rows if row["control_route_accepted"] == "true"]
    unresolved_routes = [row for row in rows if row["decision_class"] == "rejected_unresolved"]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_BUILT_NOT_RESOLVED",
        "decision_item_count": str(len(rows)),
        "endpoint_route_accepted_count": str(len(endpoint_routes)),
        "control_route_accepted_count": str(len(control_routes)),
        "unresolved_route_count": str(len(unresolved_routes)),
        "f_overlap_endpoint_ready": "false",
        "f_overlap_control_ready": "true" if control_routes else "false",
        "accepted_control_scope": "three_mask_subset_partial_path_control_only" if control_routes else "none",
        "first_required_next_action": "source_freeze_full_196_mask_route_or_official_footprint_geometry",
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
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_V1_BUILT "
        "endpoint_ready=false control_ready="
        f"{summary['f_overlap_control_ready']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
