#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with TILE_OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected pixel-fraction pilot policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("pixel-fraction pilot policy must keep endpoint scoring disabled")
    if policy["source_scope"] != "three_committed_mask_subset_only":
        raise SystemExit("pixel-fraction pilot must remain limited to the committed subset")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_BUILT_SOURCE_ONLY_NOT_MAPPED":
        raise SystemExit("unexpected pixel-fraction pilot summary status")
    if summary["tile_count"] != policy["expected_tile_count"] or len(rows) != int(policy["expected_tile_count"]):
        raise SystemExit("pixel-fraction pilot row count mismatch")
    if summary["pixel_fraction_pilot_non_degenerate"] != "true":
        raise SystemExit("pixel-fraction pilot should demonstrate non-degenerate source support on the subset")
    if summary["header_footprint_rule_uniformity_resolved_for_subset"] != "true":
        raise SystemExit("pixel-fraction pilot should resolve header-footprint uniformity on the subset")
    if summary["full_route_pixel_rule_computed"] != "false":
        raise SystemExit("pixel-fraction pilot must not claim a full-route pixel rule")
    min_value = float(summary["min_f_overlap_pixel_fraction_value"])
    max_value = float(summary["max_f_overlap_pixel_fraction_value"])
    if not (0.0 < min_value < max_value <= 1.0):
        raise SystemExit("pixel-fraction F_overlap values must be non-uniform and normalized to (0,1]")
    if int(summary["unique_f_overlap_value_count_rounded_1e_minus_12"]) <= 1:
        raise SystemExit("pixel-fraction pilot must contain more than one rounded value")
    for row in rows:
        if row["mask_pixels_parsed_upstream"] != "true":
            raise SystemExit("pixel-fraction pilot rows must come from upstream parsed masks")
        if row["source_scope"] != policy["source_scope"]:
            raise SystemExit("pixel-fraction pilot rows have unexpected source scope")
        if row["pixel_fraction_pilot_computed"] != "true":
            raise SystemExit("pixel-fraction pilot rows must mark the pilot computed")
        value = float(row["f_overlap_pixel_fraction_value"])
        if not (0.0 < value <= 1.0):
            raise SystemExit("row-level pixel-fraction values must be in (0,1]")
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "uses_posthoc_path_projection_labels",
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
        "fit_statistics",
        "posthoc_tile_selection",
        "posthoc_path_projection_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_V1_VALIDATED "
        "non_degenerate=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
