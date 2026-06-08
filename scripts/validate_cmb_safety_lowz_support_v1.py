#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "cmb_safety_lowz_support_v1.csv"
OUT = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1_summary.csv"


def main() -> None:
    with RUN.open(newline="") as f:
        run = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if run["status"] != "CMB_SAFETY_SUPPORT_CHECK_NOT_VALIDATION":
        raise SystemExit("run status mismatch")
    if summary["status"] != run["status"]:
        raise SystemExit("summary status mismatch")
    if summary["claim_boundary"] != "cmb_safety_lowz_support_check_not_validation":
        raise SystemExit("claim boundary mismatch")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("CMB safety support check must remain endpoint disabled")
    if summary["contains_cmb_map_data"] != "false" or summary["contains_cmb_likelihood"] != "false":
        raise SystemExit("CMB safety support check must not contain CMB map data or likelihoods")
    if summary["passes_cmb_lowz_support_check"] != "true":
        raise SystemExit("late-time channels did not vanish in the CMB safety support check")
    if len(rows) != 2:
        raise SystemExit("expected two CMB safety probe rows")
    for row in rows:
        if row["passes_zero_support"] != "true":
            raise SystemExit(f"probe row failed zero-support check: {row['probe_id']}")
        if float(row["W_void_source_native_basis"]) != 0.0:
            raise SystemExit("W_void must vanish at CMB-safety probe redshift")
        if float(row["W_web_source_native_basis"]) != 0.0:
            raise SystemExit("W_web must vanish at CMB-safety probe redshift")
    print("PAPER10_CMB_SAFETY_LOWZ_SUPPORT_V1_VALIDATED passes=true")


if __name__ == "__main__":
    main()
