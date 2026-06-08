#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_mode_policy_v1.csv"
INVENTORY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("COSEBIs tomographic/mode policy must remain endpoint disabled")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("COSEBIs tomographic/mode inventory must remain endpoint disabled")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false":
            raise SystemExit(f"tomographic/mode inventory must not contain {key}")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"tomographic/mode rows must not contain {key}")

    expected_pairs = int(policy["expected_tomographic_pairs"])
    expected_bins = int(policy["expected_tomographic_bins"])
    expected_modes = int(policy["expected_modes_per_pair"])
    expected_rows = int(policy["expected_data_vector_rows"])
    expected_mode_text = ";".join(str(value) for value in range(1, expected_modes + 1))

    if len(rows) != expected_pairs:
        raise SystemExit("unexpected number of COSEBIs tomographic pairs")
    pairs = {(int(row["bin1"]), int(row["bin2"])) for row in rows}
    expected_pair_set = {
        (bin1, bin2)
        for bin1 in range(1, expected_bins + 1)
        for bin2 in range(bin1, expected_bins + 1)
    }
    if pairs != expected_pair_set:
        raise SystemExit("COSEBIs tomographic-pair set is not the expected upper triangle")
    for row in rows:
        bin1 = int(row["bin1"])
        bin2 = int(row["bin2"])
        if not (1 <= bin1 <= bin2 <= expected_bins):
            raise SystemExit("non upper-triangular tomographic pair found")
        if row["rows_for_pair"] != str(expected_modes):
            raise SystemExit("unexpected row count for tomographic pair")
        if row["n_modes"] != str(expected_modes):
            raise SystemExit("unexpected mode count for tomographic pair")
        if row["modes"] != expected_mode_text:
            raise SystemExit("unexpected COSEBIs mode list")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("COSEBIs tomographic/mode row is endpoint enabled")

    if summary["status"] != "KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_INVENTORY_BUILT_NOT_SCORED":
        raise SystemExit("unexpected tomographic/mode inventory status")
    if int(summary["n_tomographic_bins"]) != expected_bins:
        raise SystemExit("unexpected tomographic-bin count")
    if int(summary["n_tomographic_pairs"]) != expected_pairs:
        raise SystemExit("unexpected tomographic-pair count")
    if int(summary["n_modes_per_pair"]) != expected_modes:
        raise SystemExit("unexpected modes-per-pair count")
    if int(summary["data_vector_rows"]) != expected_rows:
        raise SystemExit("unexpected COSEBIs data-vector row count")
    if summary["all_pairs_upper_triangular"] != "true":
        raise SystemExit("not all COSEBIs pairs are upper triangular")
    if summary["all_pairs_complete"] != "true":
        raise SystemExit("not all COSEBIs pairs have complete mode coverage")
    print("PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
