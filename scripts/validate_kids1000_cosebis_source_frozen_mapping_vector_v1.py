#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with DOMAIN_OUT.open(newline="") as f:
        domain_rows = list(csv.DictReader(f))

    if policy["status"] != "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected mapping-vector policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mapping-vector policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_BUILT_NOT_THEORY_NOT_SCORED":
        raise SystemExit("unexpected mapping-vector summary status")
    if len(rows) != 300 or summary["target_rows"] != "300":
        raise SystemExit("mapping vector must contain 300 target rows")
    if len(domain_rows) != 58800 or summary["domain_rows"] != "58800":
        raise SystemExit("mapping domain weights must contain 58,800 rows")
    if summary["mapping_vector_computed"] != "true":
        raise SystemExit("mapping vector should be computed")
    if summary["contains_mapping_vector"] != "true":
        raise SystemExit("summary should contain a mapping vector")
    if summary["contains_theory_vector"] != "false":
        raise SystemExit("mapping vector must not contain a theory vector")
    if summary["contains_predictions"] != "false":
        raise SystemExit("mapping vector must not contain predictions")
    if summary["positive_web_claim_allowed"] != "false":
        raise SystemExit("null E_web route must not become a positive web claim")
    if summary["positive_mapping_support"] != "true":
        raise SystemExit("mapping vector should have positive source support")
    if int(summary["unique_mapping_value_count_rounded_1e_minus_12"]) <= 1:
        raise SystemExit("mapping vector should not collapse to a single value")

    values = [float(row["source_frozen_mapping_value"]) for row in rows]
    if min(values) <= 0.0:
        raise SystemExit("mapping values must be positive")
    if abs(min(values) - float(summary["min_mapping_value"])) > 1.0e-10:
        raise SystemExit("summary min does not match row values")
    if abs(max(values) - float(summary["max_mapping_value"])) > 1.0e-10:
        raise SystemExit("summary max does not match row values")
    if abs((sum(values) / len(values)) - float(summary["mean_mapping_value"])) > 1.0e-10:
        raise SystemExit("summary mean does not match row values")
    if {row["w_web_basis"] for row in rows} != {"0.000000000000e+00"}:
        raise SystemExit("W_web must remain a null-control basis in this route")
    if {row["tile_count_aggregated"] for row in rows} != {"196"}:
        raise SystemExit("each target row should aggregate 196 route tiles")

    for key in [
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
            raise SystemExit(f"mapping rows leakage flag should be false: {key}")
        if any(row[key] != "false" for row in domain_rows):
            raise SystemExit(f"domain rows leakage flag should be false: {key}")
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
        "posthoc_mapping_rule_choice",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_V1_VALIDATED "
        f"rows={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
