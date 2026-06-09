#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_jackknife_robustness_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_jackknife_robustness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require_finite(value: str, label: str) -> None:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise SystemExit(f"{label} must be finite")


def main() -> None:
    policy = read_one(POLICY)
    grid = read_rows(GRID)
    summary = read_one(SUMMARY)

    if policy["status"] != "ENDPOINT_JACKKNIFE_ROBUSTNESS_POLICY_FROZEN":
        raise SystemExit("unexpected jackknife policy status")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not claim validation")
    if policy["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("policy must forbid data-vector use for source selection")
    if policy["retunes_source_frozen_theory_vector"] != "false":
        raise SystemExit("policy must not retune the source-frozen theory vector")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_JACKKNIFE_ROBUSTNESS_COMPLETE":
        raise SystemExit("unexpected jackknife summary status")
    if len(grid) != 27:
        raise SystemExit("jackknife grid should contain 27 subsets")
    if summary["subset_count"] != str(len(grid)):
        raise SystemExit("subset count mismatch")
    if summary["leave_one_subset_count"] != "20":
        raise SystemExit("leave-one subset count should be 20")
    if summary["mode_band_subset_count"] != "3":
        raise SystemExit("mode-band subset count should be 3")
    if not any(row["subset_id"] == "full_reference" for row in grid):
        raise SystemExit("full reference subset missing")
    if sum(row["subset_family"] == "leave_one_source_bin" for row in grid) != 5:
        raise SystemExit("leave-one-bin subset count should be 5")
    if sum(row["subset_family"] == "leave_one_tomographic_pair" for row in grid) != 15:
        raise SystemExit("leave-one-pair subset count should be 15")
    if sum(row["subset_family"] == "mode_band" for row in grid) != 3:
        raise SystemExit("mode-band subset count should be 3")
    if sum(row["subset_family"] == "complement_mode_band" for row in grid) != 3:
        raise SystemExit("complement mode-band subset count should be 3")
    for row in [summary, *grid]:
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("jackknife rows must not claim validation")
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("jackknife rows must record data-vector use for scoring")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("jackknife rows must forbid data-vector use for source selection")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    for row in grid:
        n_rows = int(row["n_rows"])
        if not 1 <= n_rows <= 300:
            raise SystemExit("subset row count out of range")
        for field in [
            "candidate_amplitude",
            "baseline_chi2",
            "candidate_chi2",
            "baseline_aic",
            "candidate_aic",
            "delta_chi2_vs_baseline",
            "delta_aic_vs_baseline",
            "subset_covariance_min_eigenvalue",
        ]:
            require_finite(row[field], field)
        if float(row["subset_covariance_min_eigenvalue"]) <= 0.0:
            raise SystemExit("subset covariance min eigenvalue should be positive")
    negative_leave_one = int(summary["leave_one_subsets_with_negative_delta_chi2"])
    if summary["localization_verdict"] == "not_single_source_bin_or_pair_under_leave_one_chi2":
        if negative_leave_one != 20:
            raise SystemExit("non-localized verdict requires all leave-one subsets to improve chi2")
    elif summary["localization_verdict"] == "localized_or_fragile_under_leave_one_chi2":
        if negative_leave_one >= 20:
            raise SystemExit("localized verdict requires at least one non-improving leave-one subset")
    else:
        raise SystemExit("unexpected localization verdict")
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_JACKKNIFE_ROBUSTNESS_V1_VALIDATED "
        f"leave_one_negative_chi2={summary['leave_one_subsets_with_negative_delta_chi2']}/20 "
        f"mode_band_negative_chi2={summary['mode_band_subsets_with_negative_delta_chi2']}/3 "
        f"verdict={summary['localization_verdict']}"
    )


if __name__ == "__main__":
    main()
