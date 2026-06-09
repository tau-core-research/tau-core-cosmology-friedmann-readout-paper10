#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mapping_template_join_contract_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_mapping_template_join_contract_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mapping_template_join_contract_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["status"] != "KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_POLICY_FROZEN_NOT_COMPUTED":
        raise SystemExit("unexpected mapping-template join policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("join policy must keep endpoint scoring disabled")
    if policy["current_join_values_computed"] != "false":
        raise SystemExit("join policy must not compute join values")
    if policy["current_mapping_vector_computed"] != "false":
        raise SystemExit("join policy must not compute a mapping vector")
    if summary["status"] != "KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected join-contract summary status")
    if summary["join_rows"] != policy["expected_rows"]:
        raise SystemExit("join-contract row count mismatch")
    if summary["join_key"] != "row_index_zero_based":
        raise SystemExit("join key must remain row_index_zero_based")
    if len(rows) != int(policy["expected_rows"]):
        raise SystemExit("unexpected join-contract row count")
    if [row["row_index_zero_based"] for row in rows] != [str(i) for i in range(len(rows))]:
        raise SystemExit("join-contract row indices must be contiguous")
    if [row["row_index_one_based"] for row in rows] != [str(i) for i in range(1, len(rows) + 1)]:
        raise SystemExit("join-contract one-based row indices must be contiguous")
    if len({row["pair_id"] for row in rows}) != 15:
        raise SystemExit("join contract must cover 15 tomographic pairs")
    for key in [
        "join_values_computed",
        "mapping_vector_computed",
        "theory_values_computed",
        "contains_theory_vector",
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
    for row in rows:
        if row["join_contract_row_only"] != "true":
            raise SystemExit("rows must mark join_contract_row_only=true")
        for field in [
            "source_frozen_w_web_basis",
            "source_frozen_w_path_basis",
            "source_frozen_baseline_basis",
            "source_frozen_channel_activation",
            "source_frozen_mapping_provenance",
        ]:
            if row[field] != "":
                raise SystemExit(f"{field} must remain empty in the contract")
        for key in [
            "join_values_computed",
            "mapping_vector_computed",
            "theory_values_computed",
            "contains_theory_vector",
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
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_mapping_row_selection",
        "posthoc_channel_activation",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
