#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_design_skeleton_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected design skeleton policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("design skeleton policy must remain endpoint disabled")
    if len(rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected design skeleton row count")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected design skeleton summary status")
    if summary["target_rows"] != "300":
        raise SystemExit("design skeleton must contain 300 target rows")
    if summary["tomographic_pair_count"] != "15":
        raise SystemExit("design skeleton must contain 15 tomographic pairs")
    if summary["mode_count_per_pair"] != "20":
        raise SystemExit("design skeleton must contain 20 modes per pair")
    if summary["route_tile_count"] != "196":
        raise SystemExit("design skeleton must carry the 196-tile route span")
    if rows[0]["pair_id"] != "1-1" or rows[0]["mode"] != "1":
        raise SystemExit("unexpected first design skeleton row")
    if rows[-1]["pair_id"] != "5-5" or rows[-1]["mode"] != "20":
        raise SystemExit("unexpected last design skeleton row")
    if [row["target_row_index_zero_based"] for row in rows] != [str(i) for i in range(300)]:
        raise SystemExit("target row indices must be contiguous")
    for key in [
        "path_weights_computed",
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
    for row in rows:
        if row["design_skeleton_computed"] != "true":
            raise SystemExit("design skeleton rows must mark design_skeleton_computed=true")
        float(row["bin1_mean_z"])
        float(row["bin2_mean_z"])
        if row["preferred_route_tile_count"] != "196":
            raise SystemExit("each row must carry the route tile count")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_DESIGN_SKELETON_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
