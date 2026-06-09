#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("source-frozen theory-vector policy must remain endpoint disabled")
    if policy["current_theory_vector_computed"] != "true":
        raise SystemExit("source-frozen theory-vector policy must declare computed=true")
    if len(rows) != int(policy["expected_rows"]):
        raise SystemExit("unexpected source-frozen theory-vector row count")
    if summary["status"] != "KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_BUILT_NOT_SCORED":
        raise SystemExit("unexpected source-frozen theory-vector summary status")
    if summary["theory_rows"] != policy["expected_rows"]:
        raise SystemExit("source-frozen theory-vector summary row count mismatch")
    for key in [
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["theory_vector_computed"] != "true" or summary["contains_theory_vector"] != "true":
        raise SystemExit("summary must expose a source-frozen theory-vector shell")
    if summary["positive_theory_support"] != "true":
        raise SystemExit("source-frozen theory-vector shell must have positive finite support")
    if summary["positive_web_claim_allowed"] != "false":
        raise SystemExit("source-frozen theory-vector shell must not make a positive web claim")
    if abs(float(summary["mean_mode_shape_weight"]) - 1.0) > 1e-12:
        raise SystemExit("mode-shape weights must be unit-mean normalized")
    if len({row["row_index_zero_based"] for row in rows}) != len(rows):
        raise SystemExit("source-frozen theory-vector rows must have unique row indices")
    if [row["row_index_zero_based"] for row in rows] != [str(i) for i in range(len(rows))]:
        raise SystemExit("source-frozen theory-vector rows must be contiguous")
    if len({row["pair_id"] for row in rows}) != 15:
        raise SystemExit("source-frozen theory-vector shell must cover 15 tomographic pairs")
    if len({row["mode"] for row in rows}) != 20:
        raise SystemExit("source-frozen theory-vector shell must cover 20 COSEBIs modes")
    for row in rows:
        if row["contains_theory_vector"] != "true":
            raise SystemExit("each row must mark contains_theory_vector=true")
        for key in [
            "contains_prediction",
            "contains_residual",
            "contains_fit_statistic",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_posthoc_selection",
            "endpoint_scoring_allowed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"rows must keep {key}=false")
        if float(row["w_web_contribution"]) != 0.0:
            raise SystemExit("W_web must remain zero under the null-web control")
        if float(row["theory_value"]) <= 0.0:
            raise SystemExit("unit-amplitude source-frozen theory values must be positive")
    for marker in [
        "kids_data_vector_values",
        "lensing_residuals",
        "posthoc_mode_shape_choice",
        "posthoc_amplitude_fit",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
