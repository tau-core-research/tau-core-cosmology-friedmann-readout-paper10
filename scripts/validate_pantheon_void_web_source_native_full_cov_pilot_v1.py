#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_void_web_source_native_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_grid.csv"


def main() -> None:
    with MANIFEST.open(newline="") as f:
        manifest_rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary_rows = list(csv.DictReader(f))
    with GRID.open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    if len(manifest_rows) != 1 or len(summary_rows) != 1:
        raise SystemExit("manifest and summary must contain exactly one row")
    manifest = manifest_rows[0]
    summary = summary_rows[0]
    if manifest["status"] != "VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("manifest status mismatch")
    if summary["status"] != manifest["status"]:
        raise SystemExit("summary status mismatch")
    if summary["claim_boundary"] != "void_web_source_native_full_cov_pilot_not_validation":
        raise SystemExit("claim boundary mismatch")
    if "W_PATH_PROJECTION" not in summary["disabled_channels"] or "W_TIME_READOUT" not in summary["disabled_channels"]:
        raise SystemExit("W_path and W_time must remain disabled")
    forbidden = manifest["forbidden_inputs"]
    for marker in ["distance_residuals", "growth_residuals", "lensing_residuals", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"missing forbidden marker: {marker}")
    branches = {row["branch"] for row in grid_rows}
    required = {
        "baseline_only",
        "source_native_void_web_shell",
        "source_native_void_only",
        "source_native_web_only",
        "wrong_web_sign",
        "deterministic_shuffled_source_native_void_web",
    }
    if not required <= branches:
        raise SystemExit(f"missing branches: {sorted(required - branches)}")
    for key in [
        "baseline_best_chi2",
        "source_native_void_web_best_chi2",
        "source_native_void_only_best_chi2",
        "source_native_web_only_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_best_chi2",
        "delta_aic_source_native_void_web_minus_baseline",
    ]:
        float(summary[key])
    print(
        "PAPER10_VOID_WEB_SOURCE_NATIVE_FULL_COV_PILOT_V1_VALIDATED "
        f"delta_chi2={summary['delta_chi2_source_native_void_web_minus_baseline']} "
        "claim_boundary=void_web_source_native_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
