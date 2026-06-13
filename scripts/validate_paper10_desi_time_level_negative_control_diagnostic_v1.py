#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_rows.csv"
BRANCHES = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_branches.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv"
FIGURE = ROOT / "paper10_submission_source/figures/fig_desi_time_level_negative_control_diagnostic.pdf"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(ROWS)
    branches = read_rows(BRANCHES)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 5:
        raise SystemExit("DESI diagnostic must contain exactly five row records")
    if len(branches) != 8:
        raise SystemExit("DESI diagnostic must contain the eight frozen replay branches")
    if len(summary_rows) != 1:
        raise SystemExit("DESI diagnostic summary must contain exactly one row")
    summary = summary_rows[0]
    expected_status = "DESI_TIME_LEVEL_NEGATIVE_CONTROL_DIAGNOSTIC_BUILT_NOT_VALIDATION"
    if summary["status"] != expected_status:
        raise SystemExit(f"bad diagnostic status: {summary['status']}")
    if summary["verdict"] != "desi_time_level_negative_control_diagnostic_explains_non_control_resistance_not_validation":
        raise SystemExit("bad diagnostic verdict")
    if summary["endpoint_validation_claimed"] != "false" or summary["physical_validation_claimed"] != "false":
        raise SystemExit("diagnostic must not claim endpoint or physical validation")
    if summary["failure_mode"] != "five_row_time_level_constant_beta_endpoint_is_ordering_fragile":
        raise SystemExit("unexpected DESI diagnostic failure mode")
    if int(summary["controls_better_than_candidate_chi2"]) < 1:
        raise SystemExit("negative-control diagnostic must preserve at least one better control")
    if summary["largest_candidate_diag_pull_radial_index"] != "3":
        raise SystemExit("expected radial row 3 to be the largest candidate diagonal pull")
    best = min(branches, key=lambda row: float(row["chi2"]))
    if best["branch"] != "redshift_order_shuffle_control":
        raise SystemExit("expected redshift-order shuffle to remain the best control")
    if not FIGURE.exists() or FIGURE.stat().st_size == 0:
        raise SystemExit("missing DESI diagnostic figure")
    print("paper10_desi_time_level_negative_control_diagnostic_v1: OK")


if __name__ == "__main__":
    main()
