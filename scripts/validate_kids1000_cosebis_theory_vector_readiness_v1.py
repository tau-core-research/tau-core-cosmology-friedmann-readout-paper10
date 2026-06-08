#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(rows) != 1:
        raise SystemExit("theory-vector readiness must contain one row")
    row = rows[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("theory-vector policy must remain endpoint disabled")
    if policy["current_theory_vector_computed"] != "false":
        raise SystemExit("theory vector must not be computed in the policy")
    if summary["endpoint_scoring_allowed"] != "false" or row["endpoint_scoring_allowed"] != "false":
        raise SystemExit("theory-vector readiness must remain endpoint disabled")
    if summary["current_theory_vector_computed"] != "false" or row["current_theory_vector_computed"] != "false":
        raise SystemExit("theory vector must not be computed")
    for key in [
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
    ]:
        if summary[key] != "false" or row[key] != "false":
            raise SystemExit(f"theory-vector readiness must keep {key}=false")
    if row["expected_theory_vector_rows"] != policy["expected_theory_vector_rows"]:
        raise SystemExit("unexpected theory-vector row count")
    if row["retained_data_vector_rows"] != policy["expected_theory_vector_rows"]:
        raise SystemExit("retained data-vector rows do not match theory-vector target length")
    if "W_WEB_ANISOTROPY" not in row["active_channels"] or "W_PATH_PROJECTION" not in row["active_channels"]:
        raise SystemExit("theory-vector policy must keep web/path channels active")
    if "W_TIME_READOUT" not in row["disabled_channels"]:
        raise SystemExit("theory-vector policy must keep time channel disabled for this lensing route")
    if "kids_data_vector_values" not in policy["forbidden_inputs"]:
        raise SystemExit("policy must forbid use of KiDS observed data-vector values")
    if summary["status"] != "KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected theory-vector readiness status")
    print("PAPER10_KIDS1000_COSEBIS_THEORY_VECTOR_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
