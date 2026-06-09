#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mapping_template_join_contract_policy_v1.csv"
TEMPLATE_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_theory_vector_template_policy_v1.csv"
MAPPING_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_web_path_mapping_policy_v1.csv"
TEMPLATE = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1.csv"
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_mapping_template_join_contract_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mapping_template_join_contract_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    template_policy = read_one(TEMPLATE_POLICY)
    mapping_policy = read_one(MAPPING_POLICY)
    template_summary = read_one(TEMPLATE_SUMMARY)
    with TEMPLATE.open(newline="") as f:
        template_rows = list(csv.DictReader(f))

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("join contract policy must remain endpoint disabled")
    if policy["current_join_values_computed"] != "false":
        raise SystemExit("join contract must not compute join values")
    if policy["current_theory_values_computed"] != "false":
        raise SystemExit("join contract must not compute theory values")
    if policy["current_mapping_vector_computed"] != "false":
        raise SystemExit("join contract must not compute a mapping vector")
    if template_policy["policy_id"] != policy["parent_theory_template_policy"]:
        raise SystemExit("unexpected theory-template parent policy")
    if mapping_policy["policy_id"] != policy["parent_mapping_policy"]:
        raise SystemExit("unexpected mapping parent policy")
    if mapping_policy["current_mapping_computed"] != "true":
        raise SystemExit("parent mapping policy must expose the source-frozen mapping vector")
    if policy["expected_rows"] != template_summary["template_rows"]:
        raise SystemExit("join contract expected rows must match theory-template rows")
    if len(template_rows) != int(policy["expected_rows"]):
        raise SystemExit("unexpected theory-template row count")

    rows: list[dict[str, str]] = []
    for template in template_rows:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_theory_template_policy": policy["parent_theory_template_policy"],
                "parent_mapping_policy": policy["parent_mapping_policy"],
                "selected_statistic": policy["selected_statistic"],
                "join_key": policy["join_key"],
                "row_index_zero_based": template["row_index_zero_based"],
                "row_index_one_based": template["row_index_one_based"],
                "pair_id": template["pair_id"],
                "bin1": template["bin1"],
                "bin2": template["bin2"],
                "mode": template["mode"],
                "required_future_source_columns": policy["allowed_future_source_columns"],
                "source_frozen_w_web_basis": "",
                "source_frozen_w_path_basis": "",
                "source_frozen_baseline_basis": "",
                "source_frozen_channel_activation": "",
                "source_frozen_mapping_provenance": "",
                "join_contract_row_only": "true",
                "join_values_computed": "false",
                "mapping_vector_computed": "false",
                "theory_values_computed": "false",
                "contains_theory_vector": "false",
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

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_BUILT_NOT_COMPUTED",
        "selected_statistic": policy["selected_statistic"],
        "join_rows": str(len(rows)),
        "join_key": policy["join_key"],
        "parent_theory_template_policy": policy["parent_theory_template_policy"],
        "parent_mapping_policy": policy["parent_mapping_policy"],
        "join_contract_built": "true",
        "join_values_computed": "false",
        "mapping_vector_computed": "false",
        "theory_values_computed": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_MAPPING_TEMPLATE_JOIN_CONTRACT_V1_BUILT "
        f"rows={len(rows)} mapping=false theory=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
