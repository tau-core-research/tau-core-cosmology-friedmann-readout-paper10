#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_policy_v1.csv"
BIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_bins_v1.csv"
PAIR_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_pairs_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_tomographic_holdout_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    bins = read_rows(BIN_OUT)
    pairs = read_rows(PAIR_OUT)
    summary = read_one(SUMMARY)

    if policy["status"] != "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_POLICY_FROZEN":
        raise SystemExit("unexpected policy status")
    if policy["computes_new_scores"] != "false" or policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("policy must not score or authorize replay")
    if summary["status"] != "SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_BUILT":
        raise SystemExit("unexpected summary status")
    if len(bins) != 5 or summary["source_bin_count"] != "5":
        raise SystemExit("expected five source bins")
    if len(pairs) != 75 or summary["holdout_fold_count"] != "5":
        raise SystemExit("expected five folds times fifteen tomographic pairs")
    if summary["h1_independent_evidence_complete"] != "false":
        raise SystemExit("independent evidence must remain open")
    if summary["h2_holdout_partition_frozen"] != "true":
        raise SystemExit("holdout partition should be frozen")
    if summary["endpoint_replay_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize replay or claim validation")
    if summary["verdict"] != "holdout_partition_frozen_but_independent_photoz_calibration_still_open":
        raise SystemExit("unexpected verdict")

    for row in [*bins, *pairs]:
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("source selection must not use KiDS data-vector values")
        if row["uses_residuals"] != "false" or row["uses_fit_statistics"] != "false":
            raise SystemExit("holdout manifest must not use residuals or fit statistics")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("rows must not authorize replay or claim validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")

    folds = {str(i) for i in range(1, 6)}
    for fold in folds:
        fold_rows = [row for row in pairs if row["held_out_source_bin"] == fold]
        if len(fold_rows) != 15:
            raise SystemExit(f"fold {fold} does not contain 15 tomographic pairs")
        holdout = [row for row in fold_rows if row["pair_role"] == "holdout_pair"]
        expected_holdout_count = 5
        if len(holdout) != expected_holdout_count:
            raise SystemExit(f"unexpected holdout-pair count for fold {fold}")
        for row in holdout:
            if fold not in {row["bin_i"], row["bin_j"]}:
                raise SystemExit("holdout pair does not touch held-out source bin")

    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_TOMOGRAPHIC_HOLDOUT_MANIFEST_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
