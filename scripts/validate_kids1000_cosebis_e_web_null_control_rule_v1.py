#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_e_web_null_control_rule_policy_v1.csv"
TILE = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_tile_rule_v1.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    tile_rows = read_rows(TILE)
    domain_rows = read_rows(DOMAIN)

    if policy["status"] != "KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected E_web null-control policy status")
    if policy["positive_web_claim_allowed"] != "false":
        raise SystemExit("E_web null-control policy must forbid positive web claims")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("E_web null-control policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED":
        raise SystemExit("unexpected E_web null-control summary status")
    if summary["tile_count"] != "196":
        raise SystemExit("E_web null-control rule must contain 196 tile rows")
    if summary["domain_rows"] != "58800":
        raise SystemExit("E_web null-control rule must contain 58,800 domain rows")
    if summary["e_web_null_control_uniform"] != "true":
        raise SystemExit("E_web null-control must be explicitly uniform")
    if summary["e_web_source_route_support"] != "true":
        raise SystemExit("E_web null-control should resolve only the source/control route")
    if summary["positive_web_claim_allowed"] != "false":
        raise SystemExit("E_web null-control summary must forbid positive web claims")
    if summary["unique_e_web_value_count_rounded_1e_minus_12"] != "1":
        raise SystemExit("E_web null-control must have exactly one value")
    if not (float(summary["min_e_web_value"]) == float(summary["max_e_web_value"]) == 1.0):
        raise SystemExit("E_web null-control values must equal one")

    if len(tile_rows) != 196:
        raise SystemExit("unexpected E_web null-control tile-row count")
    if len(domain_rows) != 58800:
        raise SystemExit("unexpected E_web null-control domain-row count")
    if any(row["e_web_null_control_computed"] != "true" for row in tile_rows + domain_rows):
        raise SystemExit("all E_web null-control rows must be marked computed")
    if any(float(row.get("e_web_null_control_value", row.get("e_web_value", "nan"))) != 1.0 for row in tile_rows + domain_rows):
        raise SystemExit("all E_web null-control values must equal one")
    if any(row["positive_web_claim_allowed"] != "false" for row in tile_rows + domain_rows):
        raise SystemExit("all E_web rows must forbid positive web claims")

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
        "uses_posthoc_sky_direction_selection",
        "uses_posthoc_web_environment_labels",
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary leakage flag should be false: {key}")
        if any(row[key] != "false" for row in tile_rows + domain_rows):
            raise SystemExit(f"row leakage flag should be false: {key}")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_tile_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_e_web_rule_choice",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden marker: {marker}")

    print(
        "PAPER10_KIDS1000_COSEBIS_E_WEB_NULL_CONTROL_RULE_V1_VALIDATED "
        "uniform=true positive_web_claim=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
