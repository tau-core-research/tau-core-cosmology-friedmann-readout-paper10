#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_pilot_scoring_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_pilot_scoring_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_pilot_scoring_v1_grid.csv"


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
    if manifest["status"] != "PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("pilot scoring manifest status mismatch")
    if summary["status"] != "PILOT_SCORING_NOT_VALIDATION":
        raise SystemExit("pilot scoring summary status mismatch")
    if summary["claim_boundary"] != "pilot_scoring_not_validation":
        raise SystemExit("pilot scoring summary has wrong claim boundary")
    if not grid_rows:
        raise SystemExit("pilot scoring grid is empty")
    branches = {row["branch"] for row in grid_rows}
    for branch in [
        "baseline_only",
        "tau_shell",
        "wrong_activation",
        "deterministic_shuffled_activation",
    ]:
        if branch not in branches:
            raise SystemExit(f"pilot scoring grid missing branch: {branch}")
    if int(summary["n_rows"]) != 1371:
        raise SystemExit("pilot scoring row count changed")
    for key in [
        "baseline_best_chi2",
        "tau_best_chi2",
        "wrong_best_chi2",
        "shuffled_best_chi2",
    ]:
        value = float(summary[key])
        if not (value > 0):
            raise SystemExit(f"invalid positive chi2 value for {key}")
    print(
        "PAPER10_PANTHEON_PILOT_SCORING_V1_VALIDATED "
        f"delta_chi2_tau_minus_baseline={summary['delta_chi2_tau_minus_baseline']} "
        "claim_boundary=pilot_scoring_not_validation"
    )


if __name__ == "__main__":
    main()
