#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_path_aware_void_geometry_policy_v1.csv"
GEOM = ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_path_aware_void_geometry_v1_summary.csv"
CLAIM_BOUNDARY = "path_aware_void_geometry_source_side_not_scoring_not_validation"


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
    rows = read_rows(GEOM)
    summary = read_one(SUMMARY)
    require(policy["status"] == "PATH_AWARE_VOID_GEOMETRY_SOURCE_SIDE_NOT_SCORING", "bad policy")
    require(policy["endpoint_replay_allowed"] == "false", "policy must not authorize replay")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "PATH_AWARE_VOID_GEOMETRY_BUILT_SOURCE_SIDE_NOT_SCORING", "bad summary")
    require(summary["rows"] == str(len(rows)), "row count mismatch")
    require(summary["rows"] == "424", "expected 424 low-z rows")
    require(summary["partial_path_scope_rows"] == "12", "expected 12 partial path scope rows")
    require(int(summary["path_intersection_rows"]) >= 0, "bad intersection count")
    require(int(summary["partial_path_scope_intersection_rows"]) >= 0, "bad partial intersection count")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim physical path")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    required = [
        "path_closest_approach_fraction",
        "path_impact_parameter_mpc_over_h",
        "path_nearest_void_reff_mpc_over_h",
        "path_void_crossing_margin_mpc_over_h",
        "path_intersects_effective_void",
        "path_void_chord_length_mpc_over_h",
        "path_void_depth_fraction",
    ]
    for row in rows:
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["physical_lensing_path_weight_claimed"] == "false", "row must not claim physical path")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for key in required:
            require(key in row, f"missing field: {key}")
        float(row["path_closest_approach_fraction"])
        float(row["path_impact_parameter_mpc_over_h"])
        float(row["path_nearest_void_reff_mpc_over_h"])
        float(row["path_void_crossing_margin_mpc_over_h"])
        float(row["path_void_chord_length_mpc_over_h"])
        depth = float(row["path_void_depth_fraction"])
        require(depth >= 0.0, "depth fraction must be nonnegative")
        require(row["path_intersects_effective_void"] in {"true", "false"}, "bad crossing flag")
    print(
        "PAPER10_PATH_AWARE_VOID_GEOMETRY_VALIDATED "
        f"rows={summary['rows']} intersections={summary['path_intersection_rows']} "
        f"partial_intersections={summary['partial_path_scope_intersection_rows']}"
    )


if __name__ == "__main__":
    main()
