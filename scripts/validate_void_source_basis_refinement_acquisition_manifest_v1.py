#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_acquisition_manifest_policy_v1.csv"
PLAN = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(PLAN)
    summary = read_one(SUMMARY)

    require(policy["current_endpoint_replay_allowed"] == "false", "policy must not allow replay")
    require(summary["status"] == "VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_BUILT_NOT_ATTACHED", "summary status mismatch")
    require(len(rows) == 6, "expected six acquisition routes")
    require(summary["required_routes"] == "6", "summary route count mismatch")
    require(summary["attached_routes"] == "0", "no route should be attached yet")
    require(summary["source_unique_ready"] == "false", "source uniqueness must remain open")
    require(summary["redshift_independence_preflight_complete"] == "false", "independence preflight must remain open")
    require(summary["control_resistance_preflight_complete"] == "false", "control preflight must remain open")
    require(summary["leakage_review_complete"] == "false", "leakage review must remain open")
    for key in [
        "computes_new_scores",
        "uses_distance_residuals",
        "uses_fit_statistics",
        "endpoint_replay_allowed",
        "physical_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    expected_routes = {
        "R1_void_catalogue_object_properties",
        "R2_supernova_host_to_void_geometry",
        "R3_line_of_sight_environment",
        "R4_redshift_degeneracy_independence_preflight",
        "R5_control_resistance_preflight",
        "R6_independent_leakage_review",
    }
    require({row["route_id"] for row in rows} == expected_routes, "unexpected acquisition route set")
    for row in rows:
        require(row["forbidden_inputs_used"] == "false", "routes must not use forbidden inputs")
        require(row["endpoint_replay_allowed"] == "false", "routes must not allow replay")
        require(row["physical_validation_claimed"] == "false", "routes must not claim validation")
        require(row["claim_boundary"] == policy["claim_boundary"], "row claim boundary mismatch")
    required_markers = [
        "void_depth",
        "void_radius",
        "wall_distance",
        "host_to_void_position",
        "line_of_sight_environment",
        "low_correlation_with_redshift",
        "shuffled_control_resistance",
    ]
    blob = ";".join(row["required_features"] for row in rows)
    for marker in required_markers:
        require(marker in blob, f"missing required feature marker: {marker}")
    require(summary["claim_boundary"] == policy["claim_boundary"], "summary claim boundary mismatch")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
