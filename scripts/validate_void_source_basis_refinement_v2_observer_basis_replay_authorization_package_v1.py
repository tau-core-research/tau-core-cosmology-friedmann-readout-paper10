#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_package_v1.zip"
TEMPLATE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_basis_replay_authorization_response_template_v1.csv"
CLAIM_BOUNDARY = "v2_observer_basis_replay_authorization_not_validation"


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
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    template = read_rows(TEMPLATE)
    require(PACKAGE.exists(), "missing package")
    require(summary["status"] == "V2_OBSERVER_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["candidate_family"] == "W_path_x_sky_x_x_zcenter", "bad candidate")
    require(summary["review_completed"] == "false", "package must not be completed")
    require(summary["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "package must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0, "candidate must improve baseline in screen")
    require(float(summary["delta_chi2_candidate_minus_best_control"]) < 0.0, "candidate must survive controls in screen")
    require(len(template) == 4, "template must contain four questions")
    require(all(row["review_completed"] == "false" for row in template), "template must be blank")
    require(all(row["endpoint_replay_allowed"] == "false" for row in template), "template must not pre-authorize replay")
    require(all(row["endpoint_validation_claimed"] == "false" for row in template), "template must not claim validation")
    require(all(row["claim_boundary"] == CLAIM_BOUNDARY for row in template), "template claim boundary mismatch")
    require({row["claim_boundary"] for row in manifest} == {CLAIM_BOUNDARY}, "manifest claim boundary mismatch")
    print(
        "PAPER10_OBSERVER_BASIS_REPLAY_AUTHORIZATION_PACKAGE_VALIDATED "
        f"candidate={summary['candidate_family']}"
    )


if __name__ == "__main__":
    main()
