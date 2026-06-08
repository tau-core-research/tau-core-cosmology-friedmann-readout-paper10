#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "growth_web_source_native_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_grid.csv"


def main() -> None:
    with RUN.open(newline="") as f:
        run = list(csv.DictReader(f))[0]
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with GRID.open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    if run["status"] != "GROWTH_WEB_SOURCE_NATIVE_PILOT_NOT_VALIDATION":
        raise SystemExit("run status mismatch")
    if summary["status"] != run["status"]:
        raise SystemExit("summary status mismatch")
    if summary["claim_boundary"] != "growth_web_source_native_pilot_not_validation":
        raise SystemExit("claim boundary mismatch")
    if summary["covariance_policy"] != "diagonal_summary_errors_only":
        raise SystemExit("growth pilot must remain diagonal-only")
    if "W_VOID_MATURITY" not in summary["disabled_channels"]:
        raise SystemExit("W_void must remain disabled in growth-only pilot")
    forbidden = run["forbidden_inputs"]
    for marker in ["growth_residuals", "fit_improvement_driven_grid_changes", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"missing forbidden marker: {marker}")
    branches = {row["branch"] for row in grid_rows}
    required = {"baseline_only", "web_growth_shell", "wrong_web_sign", "deterministic_shuffled_web"}
    if not required <= branches:
        raise SystemExit(f"missing branches: {sorted(required - branches)}")
    for key in [
        "baseline_best_chi2",
        "web_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_web_best_chi2",
        "delta_aic_web_minus_baseline",
    ]:
        float(summary[key])
    print(
        "PAPER10_GROWTH_WEB_SOURCE_NATIVE_PILOT_V1_VALIDATED "
        f"delta_chi2={summary['delta_chi2_web_minus_baseline']} "
        "claim_boundary=growth_web_source_native_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
