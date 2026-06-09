#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_design_matrix_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1_summary.csv"


BRANCH_COLUMNS = [
    "baseline_zero",
    "mask_sample_0",
    "mask_sample_98",
    "mask_sample_195",
    "positive_mask_mean",
    "sign_flip_positive_mean",
]


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_POLICY_FROZEN_SOURCE_ONLY":
        raise SystemExit("unexpected partial-control design-matrix policy status")
    if summary["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_BUILT_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected partial-control design-matrix summary status")
    if len(rows) != 300 or summary["target_rows"] != "300":
        raise SystemExit("partial-control design matrix must contain 300 rows")
    if summary["branch_count"] != "6":
        raise SystemExit("partial-control design matrix must declare 6 branches")
    if summary["branch_set"].split(";") != BRANCH_COLUMNS:
        raise SystemExit("unexpected branch order")
    for key in [
        "contains_endpoint_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_selection",
        "partial_control_scoring_allowed",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["contains_partial_control_candidate_vectors"] != "true":
        raise SystemExit("summary must mark partial-control candidate vectors")
    if [row["target_row_index_zero_based"] for row in rows] != [str(i) for i in range(300)]:
        raise SystemExit("design-matrix target rows must be contiguous")
    for row in rows:
        if row["policy_id"] != policy["policy_id"]:
            raise SystemExit("policy mismatch")
        if row["contains_partial_control_candidate_vectors"] != "true":
            raise SystemExit("row must mark partial-control candidate vectors")
        for key in [
            "contains_endpoint_theory_vector",
            "contains_prediction",
            "contains_residual",
            "contains_fit_statistic",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_selection",
            "partial_control_scoring_allowed",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"row must keep {key}=false")
        values = {key: float(row[key]) for key in BRANCH_COLUMNS}
        if values["baseline_zero"] != 0:
            raise SystemExit("baseline_zero branch must be zero")
        expected_positive_mean = 0.5 * (values["mask_sample_98"] + values["mask_sample_195"])
        if abs(values["positive_mask_mean"] - expected_positive_mean) > 5e-11:
            raise SystemExit("positive mask mean mismatch")
        if abs(values["sign_flip_positive_mean"] + expected_positive_mean) > 5e-11:
            raise SystemExit("sign-flip positive mean mismatch")
    print("PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_V1_VALIDATED scoring_allowed=false")


if __name__ == "__main__":
    main()
