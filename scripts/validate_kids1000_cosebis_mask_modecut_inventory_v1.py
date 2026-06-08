#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_modecut_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mask/mode-cut policy must remain endpoint disabled")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mask/mode-cut inventory must remain endpoint disabled")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false":
            raise SystemExit(f"mask/mode-cut summary must not contain {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"mask/mode-cut rows must not contain {key}")
    if summary["uses_residuals"] != "false" or summary["uses_fit_statistics"] != "false":
        raise SystemExit("mask/mode-cut policy must not use endpoint residuals or fit statistics")
    if len(rows) != 15:
        raise SystemExit("expected 15 retained tomographic pairs")
    if int(summary["input_rows"]) != int(policy["expected_input_rows"]):
        raise SystemExit("unexpected mask/mode-cut input row count")
    if int(summary["retained_rows"]) != int(policy["expected_retained_rows"]):
        raise SystemExit("unexpected mask/mode-cut retained row count")
    if summary["dropped_rows"] != "0":
        raise SystemExit("this pre-score policy must not drop rows")
    for row in rows:
        if row["dropped_rows_for_pair"] != "0":
            raise SystemExit("this pre-score policy must not drop rows by pair")
        if row["dropped_modes"] != "":
            raise SystemExit("this pre-score policy must not drop modes")
        if row["uses_residuals"] != "false" or row["uses_fit_statistics"] != "false":
            raise SystemExit("mask/mode-cut rows must not use residuals or fit statistics")
        if row["retained_rows_for_pair"] != "20":
            raise SystemExit("each tomographic pair must retain 20 modes")
    print("PAPER10_KIDS1000_COSEBIS_MASK_MODECUT_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
