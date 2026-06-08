#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "pantheon_void_web_proxy_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "pantheon_void_web_proxy_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "pantheon_void_web_proxy_full_cov_pilot_v1_grid.csv"


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
    if manifest["status"] != "VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("void/web proxy manifest status mismatch")
    if summary["status"] != "VOID_WEB_PROXY_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("void/web proxy summary status mismatch")
    if summary["claim_boundary"] != "void_web_proxy_full_cov_pilot_not_validation":
        raise SystemExit("void/web proxy summary has wrong claim boundary")
    if "W_VOID_MATURITY" not in summary["active_channels"]:
        raise SystemExit("W_void must be active")
    if "W_WEB_ANISOTROPY" not in summary["active_channels"]:
        raise SystemExit("W_web must be active")
    if "W_PATH_PROJECTION" not in summary["disabled_channels"]:
        raise SystemExit("W_path must remain disabled")
    if "W_TIME_READOUT" not in summary["disabled_channels"]:
        raise SystemExit("W_time must remain disabled")
    for key in [
        "baseline_best_chi2",
        "void_web_best_chi2",
        "void_only_best_chi2",
        "web_only_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_best_chi2",
        "covariance_min_eigenvalue",
        "covariance_condition_number",
    ]:
        if not (float(summary[key]) > 0):
            raise SystemExit(f"invalid positive value for {key}")
    branches = {row["branch"] for row in grid_rows}
    for branch in [
        "baseline_only",
        "void_web_proxy_shell",
        "void_only",
        "web_only",
        "wrong_web_sign",
        "deterministic_shuffled_void_web",
    ]:
        if branch not in branches:
            raise SystemExit(f"void/web proxy grid missing branch: {branch}")
    if any(row["claim_boundary"] != "void_web_proxy_full_cov_pilot_not_validation" for row in grid_rows):
        raise SystemExit("void/web proxy grid has wrong claim boundary")
    print(
        "PAPER10_VOID_WEB_PROXY_FULL_COV_PILOT_V1_VALIDATED "
        f"delta_chi2={summary['delta_chi2_void_web_minus_baseline']} "
        "claim_boundary=void_web_proxy_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()
