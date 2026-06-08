#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_rule_shell_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_rule_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_rule_shell_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_DECLARED_NOT_COMPUTED":
        raise SystemExit("unexpected F_overlap shell policy status")
    if policy["first_blocker"] != "F_overlap":
        raise SystemExit("F_overlap shell must refer to F_overlap as first blocker")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("F_overlap shell policy must remain endpoint disabled")
    if policy["current_overlap_rule_computed"] != "false":
        raise SystemExit("F_overlap shell policy must not compute an overlap rule")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected F_overlap shell summary status")
    if summary["shell_item_count"] != "6":
        raise SystemExit("unexpected F_overlap shell item count")
    if summary["candidate_route_count"] != "2":
        raise SystemExit("F_overlap shell must retain two candidate source routes")
    if summary["target_rows"] != "300":
        raise SystemExit("F_overlap shell must target 300 COSEBIs rows")
    if summary["route_tiles"] != "196":
        raise SystemExit("F_overlap shell must target 196 route tiles")
    if summary["domain_rows"] != "58800":
        raise SystemExit("F_overlap shell must target the full 58,800-row domain")
    if summary["overlap_rule_ready"] != "false":
        raise SystemExit("F_overlap shell must not mark overlap rule ready")
    if summary["mapping_allowed"] != "false":
        raise SystemExit("F_overlap shell must not allow mapping")

    expected_items = {
        "F_OVERLAP_INPUT_DOMAIN",
        "F_OVERLAP_ROUTE_OFFICIAL_GEOMETRY",
        "F_OVERLAP_ROUTE_PIXEL_MASK_DERIVED",
        "F_OVERLAP_OUTPUT_SCHEMA",
        "F_OVERLAP_LEAKAGE_BOUNDARY",
        "F_OVERLAP_FAILURE_MODE",
    }
    by_item = {row["shell_item_id"]: row for row in rows}
    if set(by_item) != expected_items:
        raise SystemExit("unexpected F_overlap shell items")
    if by_item["F_OVERLAP_INPUT_DOMAIN"]["blocks_overlap_computation"] != "false":
        raise SystemExit("input domain should already be available")
    for item in [
        "F_OVERLAP_ROUTE_OFFICIAL_GEOMETRY",
        "F_OVERLAP_ROUTE_PIXEL_MASK_DERIVED",
        "F_OVERLAP_OUTPUT_SCHEMA",
    ]:
        if by_item[item]["blocks_overlap_computation"] != "true":
            raise SystemExit(f"{item} must block overlap computation")
    if "one_row_per_target_row_tile_domain_entry" not in by_item["F_OVERLAP_OUTPUT_SCHEMA"]["minimum_acceptance"]:
        raise SystemExit("F_overlap output schema must require one row per domain entry")
    for key in [
        "external_products_fetched",
        "overlap_rule_computed",
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
    print("PAPER10_KIDS1000_COSEBIS_F_OVERLAP_RULE_SHELL_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
