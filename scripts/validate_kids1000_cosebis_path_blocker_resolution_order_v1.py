#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_blocker_resolution_order_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_blocker_resolution_order_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_POLICY_FROZEN_NOT_FETCHED":
        raise SystemExit("unexpected blocker-resolution policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("blocker-resolution policy must remain endpoint disabled")
    if len(rows) != 6:
        raise SystemExit("blocker-resolution order must contain six stages")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected blocker-resolution summary status")
    if summary["stage_count"] != "6":
        raise SystemExit("unexpected stage count")
    if summary["first_blocker"] != "D_path":
        raise SystemExit("D_path must be the first blocker after F_overlap is source-supported")
    if summary["resolved_source_supported_stage_count"] != "1":
        raise SystemExit("exactly F_overlap should be source-supported")
    if summary["blocking_unresolved_stage_count"] != "2":
        raise SystemExit("D_path and E_web should remain unresolved blockers")
    expected = [
        ("1", "freeze_footprint_overlap", "F_overlap", "resolved_source_supported"),
        ("2", "promote_path_depth_support", "D_path", "blocking_not_resolved"),
        ("3", "freeze_web_environment_support", "E_web", "blocking_not_resolved"),
        ("4", "define_source_side_normalization", "C_norm", "declared_not_computed"),
        ("5", "build_mapping_vector", "mapping_vector", "not_allowed_yet"),
        ("6", "execute_null_controls", "null_controls", "declared_not_executed"),
    ]
    observed = [(row["order_rank"], row["resolution_stage"], row["factor_id"], row["stage_status"]) for row in rows]
    if observed != expected:
        raise SystemExit("unexpected blocker-resolution ordering")
    by_rank = {row["order_rank"]: row for row in rows}
    if by_rank["1"]["next_allowed_stage_if_unresolved"] != "proceed_to_D_path":
        raise SystemExit("stage 1 should now permit D_path resolution")
    if by_rank["4"]["minimum_exit_condition"] != "normalization_protocol_uses_only_source_side_nonzero_weights":
        raise SystemExit("normalization must be source-side only")
    if by_rank["5"]["stage_status"] != "not_allowed_yet":
        raise SystemExit("mapping vector must not be allowed yet")
    for key in [
        "external_products_fetched",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_weight_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PATH_BLOCKER_RESOLUTION_ORDER_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
