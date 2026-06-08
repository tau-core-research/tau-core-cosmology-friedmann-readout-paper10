#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_hdu_policy_v1.csv"
INVENTORY = ROOT / "data" / "derived" / "kids1000_cosebis_hdu_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_hdu_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("COSEBIs HDU policy must remain endpoint disabled")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("COSEBIs HDU inventory must remain endpoint disabled")
    if summary["contains_residuals"] != "false" or summary["contains_fit_statistics"] != "false":
        raise SystemExit("COSEBIs HDU inventory must not contain residuals or fit statistics")
    if summary["covariance_positive_definite"] != "true":
        raise SystemExit("COSEBIs covariance must be positive definite for the future route")
    if int(summary["n_hdus"]) != len(rows):
        raise SystemExit("HDU count mismatch")
    if summary["data_vector_rows"] != policy["expected_data_vector_rows"]:
        raise SystemExit("unexpected COSEBIs data-vector row count")
    if summary["covariance_shape"] != policy["expected_covariance_shape"]:
        raise SystemExit("unexpected COSEBIs covariance shape")
    if summary["redshift_distribution_rows"] != policy["expected_nz_rows"]:
        raise SystemExit("unexpected COSEBIs NZ row count")
    roles = {row["role"] for row in rows}
    if not {"data_vector", "covariance", "redshift_distribution"} <= roles:
        raise SystemExit(f"missing required HDU roles: {roles}")
    data_row = [row for row in rows if row["role"] == "data_vector"][0]
    for column in ["BIN1", "BIN2", "ANGBIN", "VALUE", "ANG"]:
        if column not in data_row["columns"]:
            raise SystemExit(f"missing COSEBIs data-vector column: {column}")
    print("PAPER10_KIDS1000_COSEBIS_HDU_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
