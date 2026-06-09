#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_template_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_POLICY_FROZEN_NOT_COMPUTED":
        raise SystemExit("unexpected theory-vector template policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("theory-vector template policy must remain endpoint disabled")
    if policy["current_theory_values_computed"] != "false":
        raise SystemExit("theory-vector template policy must not compute values")
    if len(rows) != 300:
        raise SystemExit("theory-vector template must contain 300 rows")
    if summary["status"] != "KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected theory-vector template summary status")
    if summary["template_rows"] != "300":
        raise SystemExit("theory-vector template summary must report 300 rows")
    if summary["tomographic_pair_count"] != "15" or summary["modes_per_pair"] != "20":
        raise SystemExit("unexpected theory-vector template tomographic/mode structure")

    expected_zero_based = [str(i) for i in range(300)]
    expected_one_based = [str(i) for i in range(1, 301)]
    if [row["row_index_zero_based"] for row in rows] != expected_zero_based:
        raise SystemExit("zero-based row index is not contiguous")
    if [row["row_index_one_based"] for row in rows] != expected_one_based:
        raise SystemExit("one-based row index is not contiguous")
    pair_ids = {row["pair_id"] for row in rows}
    if len(pair_ids) != 15:
        raise SystemExit("theory-vector template must contain 15 tomographic pairs")
    for pair_id in pair_ids:
        pair_rows = [row for row in rows if row["pair_id"] == pair_id]
        if len(pair_rows) != 20:
            raise SystemExit(f"pair {pair_id} must contain 20 modes")
        if [row["mode"] for row in pair_rows] != [str(i) for i in range(1, 21)]:
            raise SystemExit(f"pair {pair_id} modes must be 1..20")

    empty_value_columns = ["theory_value", "w_web_contribution", "w_path_contribution", "baseline_contribution"]
    false_columns = [
        "contains_theory_value",
        "contains_prediction",
        "contains_residual",
        "contains_fit_statistic",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "endpoint_scoring_allowed",
    ]
    for row in rows:
        if row["theory_value_status"] != "template_pending_source_frozen_mapping":
            raise SystemExit("template rows must remain pending source-frozen mapping")
        if row["template_row_only"] != "true":
            raise SystemExit("template rows must be marked template-only")
        for key in empty_value_columns:
            if row[key] != "":
                raise SystemExit(f"{key} must remain empty in the template")
        for key in false_columns:
            if row[key] != "false":
                raise SystemExit(f"{key} must remain false in the template")
    for key in [
        "theory_values_computed",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_theory_vector_choice",
        "posthoc_mode_cuts",
        "posthoc_tomographic_selection",
        "posthoc_channel_activation",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_THEORY_VECTOR_TEMPLATE_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
