#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_values_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_POLICY_FROZEN_SOURCE_ONLY":
        raise SystemExit("unexpected partial-control mapping-values policy status")
    if summary["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_BUILT_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected partial-control mapping-values summary status")
    if len(rows) != 900 or summary["shell_rows"] != "900":
        raise SystemExit("partial-control mapping-values artifact must contain 900 rows")
    if summary["target_rows"] != "300" or summary["mask_control_rows"] != "3":
        raise SystemExit("unexpected partial-control mapping-values dimensions")
    if summary["partial_mapping_values_computed"] != "true":
        raise SystemExit("partial mapping values must be marked computed")
    if summary["contains_partial_mapping_values"] != "true":
        raise SystemExit("summary must mark partial mapping values")
    for key in [
        "contains_endpoint_mapping_vector",
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
    if [row["shell_row_index_zero_based"] for row in rows] != [str(i) for i in range(900)]:
        raise SystemExit("partial-control mapping-value row indices must be contiguous")
    if len({row["target_row_index_zero_based"] for row in rows}) != 300:
        raise SystemExit("partial-control mapping values must cover all target rows")
    if len({row["mask_sample_index_zero_based"] for row in rows}) != 3:
        raise SystemExit("partial-control mapping values must cover all three mask controls")
    values = []
    for row in rows:
        if row["mapping_values_policy_id"] != policy["policy_id"]:
            raise SystemExit("mapping-values policy mismatch")
        if row["formula_id"] != policy["formula_id"]:
            raise SystemExit("formula id mismatch")
        if row["partial_mapping_values_computed"] != "true":
            raise SystemExit("row must mark partial mapping values computed")
        if row["contains_partial_mapping_values"] != "true":
            raise SystemExit("row must mark partial mapping values")
        for key in [
            "contains_endpoint_mapping_vector",
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
                raise SystemExit(f"row must keep {key}=false")
        pair_weight = float(row["normalized_pair_mean_z_weight"])
        mode_weight = float(row["mode_decay_weight"])
        source_value = float(row["source_mask_shell_value"])
        value = float(row["partial_mapping_value"])
        if not (0 < pair_weight <= 1.000000000001):
            raise SystemExit("normalized pair mean-z weight must be in (0,1]")
        if not (0 < mode_weight <= 1.000000000001):
            raise SystemExit("mode decay weight must be in (0,1]")
        expected = source_value * pair_weight * mode_weight
        if abs(value - expected) > 5e-11:
            raise SystemExit("partial mapping value does not match frozen formula")
        values.append(value)
    if abs(min(values) - float(summary["value_min"])) > 5e-11:
        raise SystemExit("summary value_min mismatch")
    if abs(max(values) - float(summary["value_max"])) > 5e-11:
        raise SystemExit("summary value_max mismatch")
    if abs(max(abs(value) for value in values) - float(summary["max_abs_value"])) > 5e-11:
        raise SystemExit("summary max_abs_value mismatch")
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "KiDS_En_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_V1_VALIDATED scoring_allowed=false")


if __name__ == "__main__":
    main()
