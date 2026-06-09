#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_readiness_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected endpoint scoring readiness policy status")
    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("policy must keep endpoint scoring disabled")
    if policy["current_scoring_executed"] != "false":
        raise SystemExit("policy must not execute scoring")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_BUILT_NOT_SCORED":
        raise SystemExit("unexpected endpoint scoring readiness summary status")
    if summary["component_count"] != "12":
        raise SystemExit("endpoint scoring readiness must contain twelve components")
    if summary["ready_component_count"] != "8":
        raise SystemExit(
            "data vector, covariance, covariance solve policy, theory template, "
            "mapping-template join contract, web/path mapping, source preflight, "
            "and F_overlap decision should be ready"
        )
    if summary["blocking_component_count"] != "4":
        raise SystemExit("four components should block endpoint scoring")
    if summary["first_blocker"] != "theory_vector":
        raise SystemExit("theory_vector must be the first scoring blocker after mapping vector is source-supported")

    expected = {
        "data_vector_structure": ("true", "not_blocking"),
        "covariance_matrix": ("true", "not_blocking"),
        "covariance_solve_policy": ("true", "not_blocking"),
        "theory_vector_template": ("true", "not_blocking"),
        "mapping_template_join_contract": ("true", "not_blocking"),
        "theory_vector": ("false", "blocking"),
        "web_path_mapping": ("true", "not_blocking"),
        "source_preflight": ("true", "not_blocking"),
        "blocker_resolution_order": ("false", "blocking"),
        "f_overlap_resolution_decision": ("true", "not_blocking"),
        "null_controls": ("false", "blocking_until_null_controls_execute"),
        "partial_control_degeneracy_audit": ("false", "blocking_partial_control_endpoint"),
    }
    by_component = {row["component_id"]: row for row in rows}
    if set(by_component) != set(expected):
        raise SystemExit("unexpected endpoint scoring readiness components")
    for component_id, (ready, blocker) in expected.items():
        row = by_component[component_id]
        if row["ready_for_scoring"] != ready:
            raise SystemExit(f"unexpected ready state for {component_id}")
        if row["blocking_status"] != blocker:
            raise SystemExit(f"unexpected blocking state for {component_id}")

    for key in [
        "endpoint_scoring_allowed",
        "scoring_executed",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values_for_source_selection",
        "uses_posterior_chains",
        "uses_posthoc_selection",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")

    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "fit_improvement_flags",
        "lensing_residuals",
        "posthoc_channel_activation",
        "posthoc_mode_cuts",
        "posthoc_tomographic_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
