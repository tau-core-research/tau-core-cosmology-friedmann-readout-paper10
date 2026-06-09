#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_design_matrix_policy_v1.csv"
MAPPING_VALUES_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_values_policy_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_scoring_protocol_v1.csv"
MAPPING_VALUES = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1.csv"
MAPPING_VALUES_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_design_matrix_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    mapping_policy = read_one(MAPPING_VALUES_POLICY)
    protocol = read_one(PROTOCOL)
    mapping_summary = read_one(MAPPING_VALUES_SUMMARY)
    mapping_rows = read_rows(MAPPING_VALUES)

    if policy["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_POLICY_FROZEN_SOURCE_ONLY":
        raise SystemExit("unexpected design-matrix policy status")
    if policy["parent_mapping_values_policy"] != mapping_policy["policy_id"]:
        raise SystemExit("design-matrix parent mapping-values policy mismatch")
    if policy["parent_partial_control_protocol"] != protocol["protocol_id"]:
        raise SystemExit("design-matrix parent partial-control protocol mismatch")
    if mapping_summary["partial_mapping_values_computed"] != "true":
        raise SystemExit("partial mapping values must exist before design-matrix build")
    if mapping_summary["contains_endpoint_mapping_vector"] != "false":
        raise SystemExit("input mapping values must not be endpoint mapping vector")
    if protocol["partial_control_scoring_allowed"] != "false" or protocol["endpoint_scoring_allowed"] != "false":
        raise SystemExit("design matrix must not enable scoring")
    for key in [
        "current_design_matrix_built",
        "current_contains_partial_control_candidate_vectors",
        "current_contains_endpoint_theory_vector",
        "current_contains_predictions",
        "current_contains_residuals",
        "current_contains_fit_statistics",
        "current_uses_kids_data_vector_values",
        "current_uses_posterior_chains",
        "current_uses_posthoc_selection",
        "current_partial_control_scoring_allowed",
        "current_endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy must keep {key}=false before build")

    grouped: dict[str, dict[str, str]] = {}
    for row in mapping_rows:
        target = row["target_row_index_zero_based"]
        grouped.setdefault(target, row.copy())
        grouped[target][f"mask_sample_{row['mask_sample_index_zero_based']}_value"] = row[
            "partial_mapping_value"
        ]

    rows: list[dict[str, str]] = []
    for target in sorted(grouped, key=lambda value: int(value)):
        row = grouped[target]
        v0 = float(row["mask_sample_0_value"])
        v98 = float(row["mask_sample_98_value"])
        v195 = float(row["mask_sample_195_value"])
        positive_mean = 0.5 * (v98 + v195)
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_mapping_values_policy": policy["parent_mapping_values_policy"],
                "selected_statistic": policy["selected_statistic"],
                "control_scope": policy["control_scope"],
                "target_row_index_zero_based": row["target_row_index_zero_based"],
                "target_row_index_one_based": row["target_row_index_one_based"],
                "pair_id": row["pair_id"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "mode": row["mode"],
                "baseline_zero": "0",
                "mask_sample_0": f"{v0:.12g}",
                "mask_sample_98": f"{v98:.12g}",
                "mask_sample_195": f"{v195:.12g}",
                "positive_mask_mean": f"{positive_mean:.12g}",
                "sign_flip_positive_mean": f"{-positive_mean:.12g}",
                "contains_partial_control_candidate_vectors": "true",
                "contains_endpoint_theory_vector": "false",
                "contains_prediction": "false",
                "contains_residual": "false",
                "contains_fit_statistic": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_selection": "false",
                "partial_control_scoring_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    if len(rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected design-matrix row count")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_BUILT_SOURCE_ONLY_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "control_scope": policy["control_scope"],
        "target_rows": str(len(rows)),
        "branch_count": policy["expected_branch_count"],
        "branch_set": policy["branch_set"],
        "design_matrix_built": "true",
        "contains_partial_control_candidate_vectors": "true",
        "contains_endpoint_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "partial_control_scoring_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DESIGN_MATRIX_V1_BUILT "
        f"rows={len(rows)} branches={policy['expected_branch_count']} scoring=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
