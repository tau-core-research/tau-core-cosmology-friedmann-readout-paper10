#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_full_cov_pilot_scoring_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_full_cov_pilot_scoring_v1_grid.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    manifest = read_one(RUN_MANIFEST)
    summary = read_one(SUMMARY)
    with GRID.open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    if manifest["status"] != "FULL_COV_PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("full-cov pilot scoring manifest status mismatch")
    if summary["status"] != "FULL_COV_PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("full-cov pilot scoring summary status mismatch")
    if summary["claim_boundary"] != "full_cov_pilot_scoring_not_validation":
        raise SystemExit("full-cov pilot scoring summary has wrong claim boundary")
    if "cholesky" not in manifest["covariance_policy"]:
        raise SystemExit("full-cov pilot manifest must declare Cholesky full covariance")
    if summary["covariance_regularization"] != "none_positive_definite_cholesky":
        raise SystemExit("full-cov pilot unexpectedly uses covariance regularization")
    if int(summary["n_rows"]) != 1371:
        raise SystemExit("full-cov pilot row count changed")
    for key in [
        "baseline_best_chi2",
        "tau_best_chi2",
        "wrong_best_chi2",
        "shuffled_best_chi2",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        value = float(summary[key])
        if not (value > 0):
            raise SystemExit(f"invalid positive full-cov value for {key}")
    branches = {row["branch"] for row in grid_rows}
    for branch in [
        "baseline_only",
        "tau_shell",
        "wrong_activation",
        "deterministic_shuffled_activation",
    ]:
        if branch not in branches:
            raise SystemExit(f"full-cov grid missing branch: {branch}")
    if any(row["claim_boundary"] != "full_cov_pilot_scoring_not_validation" for row in grid_rows):
        raise SystemExit("full-cov grid has wrong claim boundary")
    print(
        "PAPER10_PANTHEON_FULL_COV_PILOT_SCORING_V1_VALIDATED "
        f"delta_chi2_tau_minus_baseline={summary['delta_chi2_tau_minus_baseline']} "
        "claim_boundary=full_cov_pilot_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
