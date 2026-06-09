#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    summary = read_one(SUMMARY)

    if policy["status"] != "KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected C_norm policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("C_norm policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED":
        raise SystemExit("unexpected C_norm summary status")
    if summary["domain_rows"] != "58800":
        raise SystemExit("C_norm summary must cover 58,800 domain rows")
    if len(rows) != 58800:
        raise SystemExit("C_norm domain ledger must contain 58,800 rows")
    if summary["c_norm_source_route_support"] != "true":
        raise SystemExit("C_norm source route support should be true")
    if summary["c_norm_positive_raw_support"] != "true":
        raise SystemExit("C_norm raw support should be positive")
    if not (float(summary["min_raw_source_weight_fde"]) > 0.0):
        raise SystemExit("C_norm raw source weights must be positive")
    if not (float(summary["c_norm_value"]) > 0.0):
        raise SystemExit("C_norm value must be positive")
    if abs(float(summary["mean_normalized_source_weight_fde"]) - 1.0) > 1.0e-10:
        raise SystemExit("C_norm must normalize source weights to unit mean")

    raw_values = [float(row["raw_source_weight_fde"]) for row in rows]
    if any(value <= 0.0 for value in raw_values):
        raise SystemExit("C_norm rows must have positive raw weights")
    mean_raw = sum(raw_values) / len(raw_values)
    if abs((1.0 / mean_raw) - float(summary["c_norm_value"])) > 1.0e-10:
        raise SystemExit("C_norm summary value does not match row mean")

    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_weight_selection",
        "uses_posthoc_tile_selection",
        "uses_posthoc_sky_direction_selection",
        "uses_posthoc_web_environment_labels",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary leakage flag should be false: {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"row leakage flag should be false: {key}")

    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_statistics",
        "fit_improvement_flags",
        "posthoc_weight_selection",
        "posthoc_tile_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_c_norm_rule_choice",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    print(
        "PAPER10_KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_V1_VALIDATED "
        f"c_norm={float(summary['c_norm_value']):.12e} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
