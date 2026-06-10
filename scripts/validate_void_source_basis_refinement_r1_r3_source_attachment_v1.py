#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACH = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv"
GEOM = ROOT / "data" / "derived" / "low_z_pantheon_void_geometry_join_v1.csv"
ENV = ROOT / "data" / "derived" / "low_z_pantheon_los_environment_v1.csv"
ACQ_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1_summary.csv"


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


def finite_float(value: str, field: str) -> float:
    try:
        x = float(value)
    except ValueError as exc:
        raise SystemExit(f"{field} is not float: {value}") from exc
    require(math.isfinite(x), f"{field} is not finite: {value}")
    return x


def main() -> None:
    acq = read_one(ACQ_SUMMARY)
    summary = read_one(SUMMARY)
    attach = read_rows(ATTACH)
    geom = read_rows(GEOM)
    env = read_rows(ENV)

    require(acq["endpoint_replay_allowed"] == "false", "parent acquisition manifest must not allow replay")
    require(summary["status"] == "R1_R3_SOURCE_ARTIFACTS_ATTACHED_R4_R6_STILL_OPEN", "unexpected summary status")
    require(summary["attached_routes"] == "3", "R1-R3 attachment should attach exactly three routes")
    require(summary["required_routes"] == acq["required_routes"], "required route count mismatch")
    require(summary["source_unique_ready"] == "false", "R1-R3 attachment alone must not claim source uniqueness")
    for key in [
        "redshift_independence_preflight_complete",
        "control_resistance_preflight_complete",
        "leakage_review_complete",
        "endpoint_replay_allowed",
        "computes_new_scores",
        "uses_distance_residuals",
        "uses_fit_statistics",
        "physical_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    expected_routes = {
        "R1_void_catalogue_object_properties",
        "R2_supernova_host_to_void_geometry",
        "R3_line_of_sight_environment",
    }
    require({row["route_id"] for row in attach} == expected_routes, "unexpected attached route set")
    for row in attach:
        for key in ["endpoint_replay_allowed", "contains_distance_residuals", "contains_fit_statistics", "physical_validation_claimed"]:
            require(row[key] == "false", f"attachment route must keep {key}=false")
    low_z_rows = int(summary["low_z_rows"])
    require(len(geom) == low_z_rows, "geometry row count mismatch")
    require(len(env) == low_z_rows, "environment row count mismatch")
    require(int(summary["host_to_void_geometry_rows"]) == len(geom), "geometry summary mismatch")
    require(int(summary["los_environment_rows"]) == len(env), "environment summary mismatch")
    require(int(summary["los_environment_nonempty_rows"]) > 0, "line-of-sight environment should have nonempty rows")

    geom_required = {
        "nearest_void_id",
        "nearest_void_center_distance_mpc_over_h",
        "nearest_void_reff_mpc_over_h",
        "wall_distance_mpc_over_h",
        "inside_effective_void_radius",
        "angular_separation_to_void_center_deg",
    }
    env_required = {
        "los_dz_window",
        "los_angular_radius_deg",
        "los_environment_count",
        "los_matter_density_median",
        "nearest_environment_matter_density",
    }
    require(geom_required <= set(geom[0]), f"missing geometry fields: {sorted(geom_required - set(geom[0]))}")
    require(env_required <= set(env[0]), f"missing environment fields: {sorted(env_required - set(env[0]))}")
    for row in geom:
        finite_float(row["nearest_void_center_distance_mpc_over_h"], "nearest_void_center_distance_mpc_over_h")
        finite_float(row["nearest_void_reff_mpc_over_h"], "nearest_void_reff_mpc_over_h")
        finite_float(row["wall_distance_mpc_over_h"], "wall_distance_mpc_over_h")
        sep = finite_float(row["angular_separation_to_void_center_deg"], "angular_separation_to_void_center_deg")
        require(0.0 <= sep <= 180.0, "angular separation out of range")
        for key in ["endpoint_replay_allowed", "contains_distance_residuals", "contains_fit_statistics", "physical_validation_claimed"]:
            require(row[key] == "false", f"geometry row must keep {key}=false")
    for row in env:
        count = int(row["los_environment_count"])
        require(count >= 0, "environment count must be nonnegative")
        if count > 0:
            finite_float(row["los_matter_density_median"], "los_matter_density_median")
            finite_float(row["nearest_environment_matter_density"], "nearest_environment_matter_density")
        for key in ["endpoint_replay_allowed", "contains_distance_residuals", "contains_fit_statistics", "physical_validation_claimed"]:
            require(row[key] == "false", f"environment row must keep {key}=false")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R1_R3_SOURCE_ATTACHMENT_V1_VALIDATED "
        f"low_z_rows={low_z_rows} los_nonempty={summary['los_environment_nonempty_rows']} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
