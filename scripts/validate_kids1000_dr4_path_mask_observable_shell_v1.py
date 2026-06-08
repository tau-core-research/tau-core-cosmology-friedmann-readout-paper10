#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_observable_shell_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected observable shell policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("observable shell policy must remain endpoint disabled")
    if policy["observable_rule"] != "filename_tile_coordinate_plus_centered_zero_fraction_shell":
        raise SystemExit("unexpected observable shell rule")
    if len(rows) != int(policy["expected_subset_count"]):
        raise SystemExit("unexpected observable shell row count")
    if summary["status"] != "KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_BUILT_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected observable shell summary status")
    if summary["subset_count"] != policy["expected_subset_count"]:
        raise SystemExit("observable shell summary subset mismatch")
    if summary["source_observable_shell_computed"] != "true":
        raise SystemExit("source observable shell should be computed")
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    if [row["sample_index_zero_based"] for row in rows] != ["0", "98", "195"]:
        raise SystemExit("unexpected observable shell row order")
    shell_values = [float(row["source_mask_shell_value"]) for row in rows]
    if min(shell_values) >= 0.0 or max(shell_values) <= 0.0:
        raise SystemExit("centered shell should contain both signs in this subset")
    if any(abs(value) > 1.000000000001 for value in shell_values):
        raise SystemExit("source shell values must be normalized to [-1, 1]")
    for row in rows:
        if row["source_shell_scope"] != "three_mask_subset_only":
            raise SystemExit("unexpected source shell scope")
        if row["tile_coordinate_source"] != "KiDS_mask_filename_token":
            raise SystemExit("unexpected tile coordinate source")
        if row["mask_value_semantics_interpreted"] != "false":
            raise SystemExit("mask value semantics must not be interpreted in this gate")
        float(row["tile_ra_deg_filename_proxy"])
        float(row["tile_dec_deg_filename_proxy"])
        if not (0.0 <= float(row["mask_nonzero_finite_fraction"]) <= 1.0):
            raise SystemExit("mask nonzero fraction must be in [0,1]")
        if not (0.0 <= float(row["mask_zero_finite_fraction_proxy"]) <= 1.0):
            raise SystemExit("mask zero fraction proxy must be in [0,1]")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_mask_subset_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
