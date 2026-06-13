#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_metric_lensing_path_route_audit_policy_v1.csv"
AUDIT = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_metric_lensing_path_route_audit_v1_summary.csv"
CLAIM_BOUNDARY = "metric_lensing_path_route_audit_source_side_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(AUDIT)
    summary = read_one(SUMMARY)
    require(policy["status"] == "METRIC_LENSING_PATH_ROUTE_AUDIT_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(policy["physical_lensing_path_weight_claimed"] == "false", "policy must not claim physical lensing path")
    require(summary["status"] == "METRIC_LENSING_PATH_ROUTE_AUDIT_BUILT_SOURCE_SIDE_NOT_SCORING", "bad summary")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["partial_path_scope_rows"] == "12", "expected 12 partial path-scope rows")
    require(int(summary["rows_nearest_kids_tile_within_1_deg"]) >= 0, "bad coverage count")
    require(summary["metric_lensing_numeric_product_available_for_source"] == "false", "numeric product must remain missing")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical lensing path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "metric_lensing_routes_available_but_source_aligned_path_weight_missing",
        "bad verdict",
    )
    for row in rows:
        require(row["metric_lensing_numeric_product_available_for_source"] == "false", "row cannot have numeric product")
        require(row["kappa_or_shear_value_computed"] == "false", "row cannot compute kappa/shear")
        require(row["mass_map_integral_computed"] == "false", "row cannot compute mass-map integral")
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_lensing_residuals"] == "false", "row must not contain lensing residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_kids_data_vector_values"] == "false", "row must not use KiDS data vectors")
        require(row["uses_posterior_chains"] == "false", "row must not use posterior chains")
        require(row["physical_lensing_path_weight_claimed"] == "false", "row must not claim physical lensing path")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(
            row["kids_tile_coverage_class"]
            in {"KIDS_TILE_WITHIN_1_DEG_ROUTE_ONLY", "KIDS_TILE_WITHIN_2_DEG_ROUTE_ONLY", "NO_NEARBY_KIDS_TILE_ROUTE_ONLY"},
            "bad coverage class",
        )
        float(row["nearest_kids_tile_sep_deg"])
    print(
        "PAPER10_METRIC_LENSING_PATH_ROUTE_AUDIT_VALIDATED "
        f"rows={summary['rows']} within_1deg={summary['rows_nearest_kids_tile_within_1_deg']} "
        "numeric_product=false"
    )


if __name__ == "__main__":
    main()
