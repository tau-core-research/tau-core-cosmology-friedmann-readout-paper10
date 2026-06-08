#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_mapping_domain_skeleton_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_domain_skeleton_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected domain skeleton policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("domain skeleton policy must remain endpoint disabled")
    expected_rows = int(policy["expected_domain_rows"])
    if len(rows) != expected_rows:
        raise SystemExit("unexpected domain skeleton row count")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected domain skeleton summary status")
    if summary["target_rows"] != "300" or summary["tile_count"] != "196":
        raise SystemExit("unexpected domain skeleton dimensions")
    if summary["domain_rows"] != policy["expected_domain_rows"]:
        raise SystemExit("domain row summary mismatch")
    if [row["domain_row_index_zero_based"] for row in rows] != [str(i) for i in range(expected_rows)]:
        raise SystemExit("domain row indices must be contiguous")
    first = rows[0]
    last = rows[-1]
    if first["target_row_index_zero_based"] != "0" or first["tile_index_zero_based"] != "0":
        raise SystemExit("unexpected first domain row")
    if last["target_row_index_zero_based"] != "299" or last["tile_index_zero_based"] != "195":
        raise SystemExit("unexpected last domain row")
    if len({row["target_row_index_zero_based"] for row in rows}) != 300:
        raise SystemExit("domain skeleton must cover all target rows")
    if len({row["tile_index_zero_based"] for row in rows}) != 196:
        raise SystemExit("domain skeleton must cover all route tiles")
    for key in [
        "tile_weights_computed",
        "footprint_overlap_computed",
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
        if row["domain_skeleton_computed"] != "true":
            raise SystemExit("domain skeleton rows must mark domain_skeleton_computed=true")
        for key in [
            "tile_weight_computed",
            "footprint_overlap_computed",
            "path_weight_computed",
            "web_environment_label_computed",
            "path_mapping_computed",
            "contains_mapping_vector",
            "contains_theory_vector",
            "contains_predictions",
            "contains_residuals",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_tile_selection",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
        float(row["bin1_mean_z"])
        float(row["bin2_mean_z"])
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])
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
    print("PAPER10_KIDS1000_COSEBIS_PATH_MAPPING_DOMAIN_SKELETON_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
