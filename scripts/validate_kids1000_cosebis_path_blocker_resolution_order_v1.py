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
    if summary["first_blocker"] != "none":
        raise SystemExit("path-side blockers should be resolved after null-control theory replay")
    if summary["resolved_source_supported_stage_count"] != "4":
        raise SystemExit("F_overlap, D_path, C_norm, and mapping_vector should be source-supported")
    if summary["resolved_control_supported_stage_count"] != "1":
        raise SystemExit("E_web should be resolved only as a null-control stage")
    if summary["blocking_unresolved_stage_count"] != "0":
        raise SystemExit("no path-side blocker should remain after null-control theory replay")
    expected = [
        ("1", "freeze_footprint_overlap", "F_overlap", "resolved_source_supported"),
        ("2", "promote_path_depth_support", "D_path", "resolved_source_supported"),
        ("3", "freeze_web_environment_support", "E_web", "resolved_control_supported"),
        ("4", "define_source_side_normalization", "C_norm", "resolved_source_supported"),
        ("5", "build_mapping_vector", "mapping_vector", "resolved_source_supported"),
        ("6", "execute_null_controls", "null_controls", "resolved_control_replay_supported"),
    ]
    observed = [(row["order_rank"], row["resolution_stage"], row["factor_id"], row["stage_status"]) for row in rows]
    if observed != expected:
        raise SystemExit("unexpected blocker-resolution ordering")
    by_rank = {row["order_rank"]: row for row in rows}
    if by_rank["1"]["next_allowed_stage_if_unresolved"] != "proceed_to_D_path":
        raise SystemExit("stage 1 should now permit D_path resolution")
    if by_rank["4"]["minimum_exit_condition"] != "normalization_protocol_uses_only_source_side_nonzero_weights":
        raise SystemExit("normalization must be source-side only")
    if "ROUTE_E_WEB_NULL_ABSENT_CONTROL" not in by_rank["3"]["accepted_route_ids"]:
        raise SystemExit("E_web stage must record the null-web control route")
    if "no_positive_web_claim" not in by_rank["3"]["next_allowed_stage_if_unresolved"]:
        raise SystemExit("E_web control stage must forbid positive web claims")
    if by_rank["5"]["stage_status"] != "resolved_source_supported":
        raise SystemExit("mapping vector should be source-supported")
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
        if key in {"path_mapping_computed", "contains_mapping_vector"}:
            if summary[key] != "true":
                raise SystemExit(f"summary must keep {key}=true")
            if any(row[key] != "true" for row in rows):
                raise SystemExit(f"rows must keep {key}=true")
        else:
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
