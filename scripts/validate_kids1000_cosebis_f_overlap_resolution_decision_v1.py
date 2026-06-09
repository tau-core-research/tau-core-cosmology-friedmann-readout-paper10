#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_resolution_decision_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_POLICY_FROZEN_NOT_RESOLVED":
        raise SystemExit("unexpected F_overlap resolution decision policy status")
    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("F_overlap decision policy must keep endpoint scoring disabled")
    if policy["current_overlap_rule_computed"] != "false":
        raise SystemExit("F_overlap decision policy must not compute overlap")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("F_overlap decision policy must not compute path mapping")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_BUILT_NOT_RESOLVED":
        raise SystemExit("unexpected F_overlap decision summary status")
    if summary["decision_item_count"] != "4":
        raise SystemExit("F_overlap decision must contain four decision items")
    if summary["endpoint_route_accepted_count"] != "0":
        raise SystemExit("no endpoint F_overlap route may be accepted yet")
    if summary["control_route_accepted_count"] != "1":
        raise SystemExit("exactly the three-mask subset should be accepted as control-only")
    if summary["unresolved_route_count"] != "3":
        raise SystemExit("three F_overlap routes should remain unresolved")
    if summary["f_overlap_endpoint_ready"] != "false":
        raise SystemExit("F_overlap endpoint must remain not ready")
    if summary["f_overlap_control_ready"] != "true":
        raise SystemExit("partial control route should be marked ready")
    if summary["full_route_source_cache_complete"] != "true":
        raise SystemExit("full-route source cache inventory should now be complete")
    if summary["first_required_next_action"] != "derive_source_frozen_full_mask_overlap_rule_without_endpoint_inputs":
        raise SystemExit("next F_overlap action should be source-frozen overlap-rule derivation")
    by_item = {row["decision_item_id"]: row for row in rows}
    expected_items = {
        "F_OVERLAP_OFFICIAL_GEOMETRY_ROUTE",
        "F_OVERLAP_FULL_PIXEL_MASK_ROUTE",
        "F_OVERLAP_THREE_MASK_SUBSET",
        "F_OVERLAP_BATCH0_DRY_RUN",
    }
    if set(by_item) != expected_items:
        raise SystemExit("unexpected F_overlap decision items")
    if by_item["F_OVERLAP_THREE_MASK_SUBSET"]["decision_class"] != "accepted_caveated_control_only":
        raise SystemExit("three-mask subset must remain caveated control only")
    if by_item["F_OVERLAP_THREE_MASK_SUBSET"]["endpoint_route_accepted"] != "false":
        raise SystemExit("three-mask subset must not be an endpoint route")
    if by_item["F_OVERLAP_THREE_MASK_SUBSET"]["control_route_accepted"] != "true":
        raise SystemExit("three-mask subset should be accepted only as a control route")
    for item_id in [
        "F_OVERLAP_OFFICIAL_GEOMETRY_ROUTE",
        "F_OVERLAP_BATCH0_DRY_RUN",
    ]:
        if by_item[item_id]["decision_class"] != "rejected_unresolved":
            raise SystemExit(f"{item_id} must remain unresolved")
    if by_item["F_OVERLAP_FULL_PIXEL_MASK_ROUTE"]["decision_class"] != "source_cache_complete_overlap_rule_pending":
        raise SystemExit("full mask route should be source-cache complete but overlap-rule pending")
    if by_item["F_OVERLAP_FULL_PIXEL_MASK_ROUTE"]["endpoint_route_accepted"] != "false":
        raise SystemExit("full mask route must not be an endpoint route before overlap rule derivation")
    for key in [
        "overlap_rule_computed",
        "numeric_factors_computed",
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
    for row in rows:
        for key in [
            "overlap_rule_computed",
            "numeric_factor_computed",
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
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_overlap_rule_choice",
        "posthoc_path_projection_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_RESOLUTION_DECISION_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
