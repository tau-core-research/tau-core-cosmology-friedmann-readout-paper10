#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_control_dominance_audit_v1_summary.csv"
BRANCH_AUDIT = ROOT / "data" / "derived" / "void_source_basis_refinement_control_dominance_audit_v1_branches.csv"


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
    branches = read_rows(BRANCH_AUDIT)
    by_role = {row["role"]: row for row in branches}
    require(summary["status"] == "CONTROL_DOMINANCE_AUDIT_COMPLETE_NOT_VALIDATION", "bad audit status")
    require(summary["endpoint_validation_claimed"] == "false", "audit must not claim validation")
    require(summary["contains_endpoint_residuals"] == "true", "audit must declare post-score residual diagnostics")
    require(summary["uses_endpoint_residuals_for_new_source_selection"] == "false", "audit must not feed residuals back")
    require(
        summary["claim_boundary"] == "post_score_control_dominance_audit_not_validation",
        "summary claim boundary mismatch",
    )
    require({"baseline_best", "best_candidate", "best_control"} <= set(by_role), "missing branch audit roles")
    for row in branches:
        require(row["endpoint_validation_claimed"] == "false", "branch audit must not claim validation")
        require(row["contains_endpoint_residuals"] == "true", "branch audit must mark residual diagnostic status")
        require(
            row["claim_boundary"] == "post_score_control_dominance_audit_not_validation",
            "branch claim boundary mismatch",
        )
    require(summary["candidate_improves_chi2_over_baseline"] == "true", "candidate should keep weak chi2 improvement")
    require(summary["candidate_loses_aic_to_baseline"] == "true", "candidate should lose AIC to baseline")
    require(summary["best_control_beats_candidate_chi2"] == "true", "best control should beat candidate")
    require(summary["best_control_is_row_shuffle"] == "true", "best control should be row-shuffle")
    require(summary["best_control_low_redshift_row_leakage"] == "true", "best control should not be a simple z/row leak")
    require(float(summary["delta_chi2_candidate_minus_baseline"]) < 0.0, "candidate should improve chi2 vs baseline")
    require(float(summary["delta_aic_candidate_minus_baseline"]) > 0.0, "candidate should lose AIC vs baseline")
    require(float(summary["delta_chi2_candidate_minus_best_control"]) > 0.0, "candidate should lose chi2 vs control")
    require(int(summary["controls_better_than_candidate_chi2"]) > 0, "at least one control should beat candidate")
    require(
        summary["verdict"] == "candidate_signal_not_source_specific_shuffled_control_dominates_without_redshift_leak",
        "unexpected audit verdict",
    )
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_CONTROL_DOMINANCE_AUDIT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
