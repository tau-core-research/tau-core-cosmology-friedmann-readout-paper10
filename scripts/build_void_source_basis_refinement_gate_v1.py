#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_gate_policy_v1.csv"
DIAGNOSTIC = ROOT / "data" / "derived" / "low_z_void_replay_diagnostics_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_gate_v1.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_one(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    policy = read_one(POLICY)
    diagnostic = read_one(DIAGNOSTIC)

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("refinement policy must not allow endpoint scoring")
    if policy["physical_validation_claimed"] != "false":
        raise SystemExit("refinement policy must not claim validation")
    if diagnostic["physical_validation_claimed"] != "false":
        raise SystemExit("parent diagnostic must not claim validation")
    if diagnostic["diagnosis"] != "grid_edge_pressure_and_shuffled_control_beats_candidate":
        raise SystemExit("unexpected parent diagnostic")
    if float(diagnostic["shuffled_minus_candidate_chi2"]) >= 0.0:
        raise SystemExit("refinement gate requires shuffled control to beat candidate")
    if diagnostic["candidate_omega_m_at_grid_edge"] != "true" or diagnostic["candidate_omega_void_at_grid_edge"] != "true":
        raise SystemExit("refinement gate requires recorded grid-edge pressure")

    redshift_correlation = abs(float(diagnostic["void_basis_pearson_r_with_zHD"]))
    row_correlation = abs(float(diagnostic["void_basis_pearson_r_with_source_row_index"]))
    source_unique_ready = "false"
    blocker = "redshift_degeneracy_and_control_nonuniqueness"
    if redshift_correlation < 0.5 and row_correlation < 0.5 and int(diagnostic["controls_better_than_candidate_chi2"]) == 0:
        source_unique_ready = "review_required_unexpected_pass"
        blocker = "manual_review_required"

    row = {
        "gate_id": "VOID_SOURCE_BASIS_REFINEMENT_GATE_V1",
        "policy_id": policy["policy_id"],
        "parent_diagnostic_id": diagnostic["diagnostic_id"],
        "status": policy["status"],
        "current_basis_status": policy["current_basis_status"],
        "parent_diagnosis": diagnostic["diagnosis"],
        "delta_chi2_void_minus_baseline": diagnostic["delta_chi2_void_minus_baseline"],
        "delta_aic_void_minus_baseline": diagnostic["delta_aic_void_minus_baseline"],
        "shuffled_minus_candidate_chi2": diagnostic["shuffled_minus_candidate_chi2"],
        "candidate_grid_edge_pressure": "true",
        "void_basis_pearson_r_with_zHD": diagnostic["void_basis_pearson_r_with_zHD"],
        "void_basis_pearson_r_with_source_row_index": diagnostic["void_basis_pearson_r_with_source_row_index"],
        "source_unique_ready": source_unique_ready,
        "refinement_blocker": blocker,
        "required_source_features": policy["required_source_features"],
        "required_independence_tests": policy["required_independence_tests"],
        "required_controls": policy["required_controls"],
        "forbidden_inputs": policy["forbidden_inputs"],
        "endpoint_scoring_allowed": "false",
        "physical_validation_claimed": "false",
        "next_allowed_artifact": policy["next_allowed_artifact"],
        "recommended_next_action": "build_source_side_acquisition_manifest_before_any_new_void_replay",
        "claim_boundary": policy["claim_boundary"],
    }
    write_one(OUT, row)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_GATE_V1_BUILT "
        f"blocker={blocker} source_unique_ready={source_unique_ready} "
        "claim_boundary=not_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
