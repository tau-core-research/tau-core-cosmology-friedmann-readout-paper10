#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_subselection_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_subselection_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance-subselection policy must remain endpoint disabled")
    if policy["current_inversion_allowed"] != "false":
        raise SystemExit("covariance inversion must remain disabled")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance-subselection inventory must remain endpoint disabled")
    if summary["current_inversion_allowed"] != "false" or summary["inverse_saved"] != "false":
        raise SystemExit("covariance-subselection inventory must not save or allow inverse covariance")
    for key in ["uses_residuals", "uses_fit_statistics", "uses_posterior_chains"]:
        if summary[key] != "false":
            raise SystemExit(f"summary must not use {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must not use {key}")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false":
            raise SystemExit(f"summary must not contain {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must not contain {key}")
    if summary["full_covariance_shape"] != policy["expected_full_covariance_shape"]:
        raise SystemExit("unexpected full covariance shape")
    if summary["retained_covariance_shape"] != policy["expected_retained_covariance_shape"]:
        raise SystemExit("unexpected retained covariance shape")
    if summary["retained_rows"] != policy["expected_retained_rows"]:
        raise SystemExit("unexpected retained covariance row count")
    if summary["full_covariance_retained"] != "true":
        raise SystemExit("full covariance must be retained")
    if summary["dropped_covariance_rows"] != "0" or summary["dropped_covariance_cols"] != "0":
        raise SystemExit("this pre-score policy must not drop covariance rows or columns")
    if len(rows) != 15:
        raise SystemExit("expected 15 covariance pair blocks")
    expected_start = 0
    for row in rows:
        if row["retained_rows_for_pair"] != "20":
            raise SystemExit("each pair block must retain 20 rows")
        start = int(row["covariance_row_start_zero_based"])
        end = int(row["covariance_row_end_zero_based"])
        if start != expected_start or end != expected_start + 19:
            raise SystemExit("covariance row intervals must cover contiguous 20-row blocks")
        if row["covariance_col_start_zero_based"] != row["covariance_row_start_zero_based"]:
            raise SystemExit("covariance row/column block starts must match")
        if row["covariance_col_end_zero_based"] != row["covariance_row_end_zero_based"]:
            raise SystemExit("covariance row/column block ends must match")
        if row["dropped_covariance_rows"] != "0" or row["dropped_covariance_cols"] != "0":
            raise SystemExit("pair blocks must not drop covariance entries")
        expected_start += 20
    if expected_start != 300:
        raise SystemExit("covariance pair blocks must cover 300 rows")
    print("PAPER10_KIDS1000_COSEBIS_COVARIANCE_SUBSELECTION_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
