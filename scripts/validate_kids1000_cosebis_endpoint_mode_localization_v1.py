#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_mode_localization_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_localization_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    grid = read_rows(GRID)
    summary = read_one(SUMMARY)
    if policy["status"] != "ENDPOINT_MODE_LOCALIZATION_POLICY_FROZEN":
        raise SystemExit("unexpected mode-localization policy status")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not claim validation")
    if policy["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("policy must forbid source-selection leakage")
    if policy["retunes_source_frozen_theory_vector"] != "false":
        raise SystemExit("policy must not retune the source-frozen theory vector")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_MODE_LOCALIZATION_COMPLETE":
        raise SystemExit("unexpected mode-localization summary status")
    if len(grid) != 59:
        raise SystemExit("mode-localization grid should contain 59 subsets")
    if summary["subset_count"] != "59":
        raise SystemExit("subset count mismatch")
    if summary["single_mode_subset_count"] != "20":
        raise SystemExit("single-mode subset count should be 20")
    if summary["cumulative_low_subset_count"] != "20":
        raise SystemExit("cumulative-low subset count should be 20")
    if summary["without_low_subset_count"] != "19":
        raise SystemExit("without-low subset count should be 19")
    if summary["best_single_mode_subset_id"] != "single_mode_1":
        raise SystemExit("unexpected best single mode")
    if summary["best_cumulative_low_subset_id"] != "cumulative_low_modes_1_to_3":
        raise SystemExit("unexpected best cumulative low-mode subset")
    if summary["first_without_low_non_improving_subset_id"] != "without_low_modes_1_to_5":
        raise SystemExit("unexpected first non-improving without-low subset")
    if summary["mode_localization_verdict"] != "low_modes_1_to_5_dominate_endpoint_signal":
        raise SystemExit("unexpected mode localization verdict")
    for row in [summary, *grid]:
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("mode-localization rows must not claim validation")
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("mode-localization rows should record scoring data use")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("mode-localization rows must forbid source-selection leakage")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    for row in grid:
        for field in [
            "candidate_amplitude",
            "baseline_chi2",
            "candidate_chi2",
            "delta_chi2_vs_baseline",
            "delta_aic_vs_baseline",
            "subset_covariance_min_eigenvalue",
        ]:
            value = float(row[field])
            if not math.isfinite(value):
                raise SystemExit(f"{field} must be finite")
        if float(row["subset_covariance_min_eigenvalue"]) <= 0.0:
            raise SystemExit("subset covariance min eigenvalue must be positive")
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_MODE_LOCALIZATION_V1_VALIDATED "
        f"best_single={summary['best_single_mode_subset_id']} "
        f"best_cumulative={summary['best_cumulative_low_subset_id']} "
        f"verdict={summary['mode_localization_verdict']}"
    )


if __name__ == "__main__":
    main()
