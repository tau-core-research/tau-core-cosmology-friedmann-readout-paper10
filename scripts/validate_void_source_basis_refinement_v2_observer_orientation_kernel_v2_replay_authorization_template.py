#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_policy.csv"
TEMPLATE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_template.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv"
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_observer_orientation_kernel_v2_replay_not_validation"
EXPECTED = {"Q1_kernel_freeze", "Q2_centering_rule", "Q3_control_scope", "Q4_authorization"}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one(path: Path) -> dict[str, str]:
    r = rows(path)
    if len(r) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return r[0]


def require(c: bool, m: str) -> None:
    if not c:
        raise SystemExit(m)


def main() -> None:
    policy = rows(POLICY)
    template = rows(TEMPLATE)
    summary = one(SUMMARY)
    require({r["question_id"] for r in policy} == EXPECTED, "unexpected policy questions")
    require({r["question_id"] for r in template} == EXPECTED, "unexpected template questions")
    for r in policy:
        require(r["claim_boundary"] == CLAIM_BOUNDARY, "policy claim boundary mismatch")
        for marker in ["distance_residuals", "fit_statistics", "endpoint_scores", "posthoc_sky_direction_selection"]:
            require(marker in r["forbidden_inputs"], f"missing forbidden marker {marker}")
    for r in template:
        require(r["review_completed"] == "false", "template must be blank")
        require(r["forbidden_inputs_used"] == "false", "template forbidden flag must be false")
        require(r["endpoint_replay_allowed"] == "false", "template must not authorize replay")
        require(r["endpoint_validation_claimed"] == "false", "template must not claim validation")
        require(r["physical_lensing_path_weight_claimed"] == "false", "template must not claim path physics")
        require(r["authorization_scope"] == AUTH_SCOPE, "authorization scope mismatch")
        require(r["primary_kernel"] == "W_path_times_centered_sky_z", "primary kernel mismatch")
        require(r["claim_boundary"] == CLAIM_BOUNDARY, "template claim boundary mismatch")
    require(summary["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED", "bad summary status")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    print("PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTH_TEMPLATE_VALIDATED review_completed=false")


if __name__ == "__main__":
    main()
