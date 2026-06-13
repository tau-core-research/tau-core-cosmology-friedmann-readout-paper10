#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_basis_fast_screen_v1.csv"
GRID = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_fast_screen_v1_summary.csv"
CLAIM_BOUNDARY = "v2_observer_basis_fast_screen_not_endpoint_not_validation"
BRANCHES = {"candidate", "off", "wrong_sign", "deterministic_shuffle", "rank_reverse"}


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
    manifest = read_one(MANIFEST)
    grid = read_rows(GRID)
    families = read_rows(FAMILY_SUMMARY)
    summary = read_one(SUMMARY)
    require(manifest["status"] == "V2_OBSERVER_BASIS_FAST_SCREEN_PREAUTH_DIAGNOSTIC_NOT_ENDPOINT", "bad manifest")
    require(manifest["endpoint_replay_allowed"] == "false", "manifest must not authorize replay")
    require(manifest["endpoint_validation_claimed"] == "false", "manifest must not claim validation")
    require(summary["status"] == manifest["status"], "summary status mismatch")
    require(summary["n_rows"] == "12", "screen must use 12 rows")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(int(summary["n_families"]) == len(families), "family count mismatch")
    require(int(summary["grid_rows"]) == len(grid), "grid count mismatch")
    require(int(summary["surviving_family_count"]) >= 0, "bad surviving count")
    for marker in [
        "distance_residual_driven_activation",
        "lensing_residual_driven_activation",
        "posthoc_sky_direction_selection",
        "posthoc_path_projection_labels",
        "posthoc_path_weight_tuning",
        "posthoc_row_selection",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_lensing_path_weight_claims",
        "physical_validation_claims",
    ]:
        require(marker in manifest["forbidden_inputs"], f"missing forbidden marker: {marker}")
    branch_by_family: dict[str, set[str]] = {}
    for row in grid:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "grid claim boundary mismatch")
        require(row["n_rows"] == "12", "grid must use 12 rows")
        branch_by_family.setdefault(row["family_id"], set()).add(row["branch"])
    for row in families:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "family claim boundary mismatch")
        float(row["candidate_best_chi2_screen"])
        float(row["candidate_best_aic_screen"])
        float(row["delta_chi2_candidate_minus_baseline"])
        float(row["delta_chi2_candidate_minus_best_control"])
        require(int(row["controls_better_than_candidate_chi2"]) >= 0, "bad control count")
        require(row["family_id"] in branch_by_family, "family missing from grid")
        require(BRANCHES.issubset(branch_by_family[row["family_id"]]), "family branch set incomplete")
    float(summary["baseline_best_chi2"])
    float(summary["best_candidate_chi2"])
    float(summary["best_candidate_delta_chi2_minus_baseline"])
    float(summary["best_candidate_delta_chi2_minus_best_global_control"])
    require(
        summary["verdict"]
        in {
            "observer_basis_fast_screen_has_candidate_for_review",
            "observer_basis_fast_screen_no_control_surviving_candidate",
        },
        "bad verdict",
    )
    print(
        "PAPER10_OBSERVER_BASIS_FAST_SCREEN_VALIDATED "
        f"verdict={summary['verdict']} "
        f"surviving={summary['surviving_family_count']} "
        f"best={summary['best_candidate_family']}"
    )


if __name__ == "__main__":
    main()
