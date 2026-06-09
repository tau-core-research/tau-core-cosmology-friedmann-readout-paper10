#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_theory_vector_policy_v1.csv"
TEMPLATE = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1.csv"
MAPPING = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1.csv"
MAPPING_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    mapping_summary = read_one(MAPPING_SUMMARY)
    with TEMPLATE.open(newline="") as f:
        template_rows = list(csv.DictReader(f))
    with MAPPING.open(newline="") as f:
        mapping_rows = list(csv.DictReader(f))

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("source-frozen theory-vector policy must remain endpoint disabled")
    if policy["current_theory_vector_computed"] != "true":
        raise SystemExit("source-frozen theory-vector policy must declare computed=true")
    if mapping_summary["contains_mapping_vector"] != "true":
        raise SystemExit("source-frozen mapping vector must exist before theory-vector shell")
    if mapping_summary["contains_theory_vector"] != "false":
        raise SystemExit("mapping vector artifact must not already contain a theory vector")
    if len(template_rows) != int(policy["expected_rows"]) or len(mapping_rows) != int(policy["expected_rows"]):
        raise SystemExit("template and mapping rows must match expected source-frozen theory-vector length")

    mapping_by_row = {row["row_index_zero_based"]: row for row in mapping_rows}
    if set(mapping_by_row) != {row["row_index_zero_based"] for row in template_rows}:
        raise SystemExit("template and mapping row indices must match")

    raw_mode_weights = {str(mode): mode ** -0.5 for mode in range(1, 21)}
    mean_mode_weight = sum(raw_mode_weights.values()) / len(raw_mode_weights)
    mode_weights = {mode: value / mean_mode_weight for mode, value in raw_mode_weights.items()}

    rows: list[dict[str, str]] = []
    for template in template_rows:
        mapping = mapping_by_row[template["row_index_zero_based"]]
        if template["pair_id"] != mapping["pair_id"] or template["mode"] != mapping["mode"]:
            raise SystemExit(f"template/mapping mismatch at row {template['row_index_zero_based']}")
        mode_weight = mode_weights[template["mode"]]
        w_path = float(mapping["w_path_basis"]) * mode_weight
        w_web = 0.0
        baseline = 0.0
        theory_value = baseline + w_path + w_web
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_theory_policy": policy["parent_theory_policy"],
                "parent_mapping_vector": policy["parent_mapping_vector"],
                "selected_statistic": policy["selected_statistic"],
                "row_index_zero_based": template["row_index_zero_based"],
                "row_index_one_based": template["row_index_one_based"],
                "bin1": template["bin1"],
                "bin2": template["bin2"],
                "pair_id": template["pair_id"],
                "mode": template["mode"],
                "source_frozen_mapping_value": mapping["source_frozen_mapping_value"],
                "mode_shape_weight": f"{mode_weight:.12e}",
                "theory_value_status": "source_frozen_unit_amplitude_theory_shell",
                "theory_value": f"{theory_value:.12e}",
                "w_web_contribution": f"{w_web:.12e}",
                "w_path_contribution": f"{w_path:.12e}",
                "baseline_contribution": f"{baseline:.12e}",
                "amplitude_policy": policy["amplitude_policy"],
                "mode_shape_rule": policy["mode_shape_rule"],
                "contains_theory_vector": "true",
                "contains_prediction": "false",
                "contains_residual": "false",
                "contains_fit_statistic": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    values = [float(row["theory_value"]) for row in rows]
    mode_values = [float(row["mode_shape_weight"]) for row in rows]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_BUILT_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "theory_rows": str(len(rows)),
        "theory_vector_computed": "true",
        "contains_theory_vector": "true",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "endpoint_scoring_allowed": "false",
        "mode_shape_rule": policy["mode_shape_rule"],
        "amplitude_policy": policy["amplitude_policy"],
        "min_theory_value": f"{min(values):.12e}",
        "max_theory_value": f"{max(values):.12e}",
        "mean_theory_value": f"{sum(values) / len(values):.12e}",
        "min_mode_shape_weight": f"{min(mode_values):.12e}",
        "max_mode_shape_weight": f"{max(mode_values):.12e}",
        "mean_mode_shape_weight": f"{sum(mode_values) / len(mode_values):.12e}",
        "unique_theory_value_count_rounded_1e_minus_12": str(len({round(value, 12) for value in values})),
        "positive_theory_support": str(all(value > 0 and math.isfinite(value) for value in values)).lower(),
        "positive_web_claim_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_THEORY_VECTOR_V1_BUILT "
        f"rows={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
