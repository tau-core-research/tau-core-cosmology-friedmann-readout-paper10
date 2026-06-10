#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_gate_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "void_source_basis_refinement_gate_v1.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    gate = read_one(GATE)

    require(gate["gate_id"] == "VOID_SOURCE_BASIS_REFINEMENT_GATE_V1", "gate id mismatch")
    require(gate["policy_id"] == policy["policy_id"], "policy id mismatch")
    require(gate["status"] == "REFINEMENT_REQUIRED_NOT_SCORING", "status mismatch")
    require(gate["source_unique_ready"] == "false", "current basis must remain not source-unique-ready")
    require(gate["refinement_blocker"] == "redshift_degeneracy_and_control_nonuniqueness", "blocker mismatch")
    require(float(gate["shuffled_minus_candidate_chi2"]) < 0.0, "shuffled control should remain better")
    require(gate["candidate_grid_edge_pressure"] == "true", "grid-edge pressure must be recorded")
    require(abs(float(gate["void_basis_pearson_r_with_zHD"])) > 0.9, "redshift degeneracy should remain explicit")
    for marker in [
        "void_depth",
        "void_radius",
        "wall_distance",
        "host_to_void_position",
        "line_of_sight_environment",
        "catalogue_selection_function",
    ]:
        require(marker in gate["required_source_features"], f"missing source feature: {marker}")
    for marker in [
        "low_correlation_with_redshift",
        "shuffled_control_resistance",
        "wrong_sign_control_resistance",
        "threshold_control_resistance",
    ]:
        require(marker in gate["required_independence_tests"], f"missing independence test: {marker}")
    for marker in [
        "distance_residuals",
        "fit_improvement_driven_basis_changes",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_amplitude_tuning",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        require(marker in gate["forbidden_inputs"], f"missing forbidden marker: {marker}")
    require(gate["endpoint_scoring_allowed"] == "false", "gate must not allow endpoint scoring")
    require(gate["physical_validation_claimed"] == "false", "gate must not claim validation")
    require(
        gate["claim_boundary"] == "void_source_basis_refinement_gate_not_scoring_not_validation",
        "claim boundary mismatch",
    )
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_GATE_V1_VALIDATED "
        f"blocker={gate['refinement_blocker']} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
