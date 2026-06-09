#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_POLICY_FROZEN_NOT_MAPPED":
        raise SystemExit("unexpected partial-control mapping shell policy status")
    if policy["current_partial_mapping_values_computed"] != "false":
        raise SystemExit("partial-control mapping values must remain uncomputed")
    if policy["current_partial_control_scoring_allowed"] != "false":
        raise SystemExit("partial-control scoring must remain disabled")
    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring must remain disabled")
    if summary["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected partial-control mapping shell summary status")
    if summary["target_rows"] != "300" or summary["mask_control_rows"] != "3":
        raise SystemExit("unexpected partial-control mapping shell dimensions")
    if summary["shell_rows"] != "900":
        raise SystemExit("partial-control mapping shell must contain 900 rows")
    if len(rows) != 900:
        raise SystemExit("unexpected partial-control mapping shell row count")
    if [row["shell_row_index_zero_based"] for row in rows] != [str(i) for i in range(900)]:
        raise SystemExit("partial-control shell row indices must be contiguous")
    if len({row["target_row_index_zero_based"] for row in rows}) != 300:
        raise SystemExit("partial-control shell must cover all target rows")
    if len({row["mask_sample_index_zero_based"] for row in rows}) != 3:
        raise SystemExit("partial-control shell must cover all three mask controls")
    for key in [
        "partial_mapping_values_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_selection",
        "partial_control_scoring_allowed",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    for row in rows:
        if row["mapping_shell_row_only"] != "true":
            raise SystemExit("rows must mark mapping_shell_row_only=true")
        if row["partial_mapping_value"] != "":
            raise SystemExit("partial mapping values must remain empty")
        if row["source_shell_scope"] != "three_mask_subset_only":
            raise SystemExit("unexpected source shell scope")
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])
        value = float(row["source_mask_shell_value"])
        if abs(value) > 1.000000000001:
            raise SystemExit("source mask shell value must be normalized")
        for key in [
            "partial_mapping_values_computed",
            "contains_mapping_vector",
            "contains_theory_vector",
            "contains_prediction",
            "contains_residual",
            "contains_fit_statistic",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_selection",
            "partial_control_scoring_allowed",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
        "posthoc_channel_activation",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
