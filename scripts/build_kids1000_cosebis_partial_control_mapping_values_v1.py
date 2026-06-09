#!/usr/bin/env python3
from __future__ import annotations

import csv
from math import sqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_values_policy_v1.csv"
SHELL_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_scoring_protocol_v1.csv"
SHELL = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1.csv"
SHELL_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv"
REDSHIFT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_values_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def as_bool_false(row: dict[str, str], keys: list[str]) -> None:
    for key in keys:
        if row[key] != "false":
            raise SystemExit(f"{key} must remain false in {row.get('policy_id', 'artifact')}")


def main() -> None:
    policy = read_one(POLICY)
    shell_policy = read_one(SHELL_POLICY)
    protocol = read_one(PROTOCOL)
    shell_summary = read_one(SHELL_SUMMARY)
    shell_rows = read_rows(SHELL)
    redshift_rows = read_rows(REDSHIFT)

    if policy["status"] != "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_POLICY_FROZEN_SOURCE_ONLY":
        raise SystemExit("unexpected mapping-values policy status")
    if policy["parent_mapping_shell_policy"] != shell_policy["policy_id"]:
        raise SystemExit("mapping-values policy parent shell mismatch")
    if policy["parent_partial_control_protocol"] != protocol["protocol_id"]:
        raise SystemExit("mapping-values policy parent protocol mismatch")
    if protocol["partial_control_scoring_allowed"] != "false" or protocol["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mapping-values builder must not enable scoring")
    if shell_summary["partial_mapping_values_computed"] != "false":
        raise SystemExit("input shell must not already contain mapping values")
    if shell_summary["shell_rows"] != policy["expected_shell_rows"]:
        raise SystemExit("shell row count mismatch")
    if len(shell_rows) != int(policy["expected_shell_rows"]):
        raise SystemExit("unexpected shell row count")
    as_bool_false(
        policy,
        [
            "current_partial_mapping_values_computed",
            "current_contains_endpoint_mapping_vector",
            "current_contains_theory_vector",
            "current_contains_predictions",
            "current_contains_residuals",
            "current_contains_fit_statistics",
            "current_uses_kids_data_vector_values",
            "current_uses_posterior_chains",
            "current_uses_posthoc_selection",
            "current_partial_control_scoring_allowed",
            "current_endpoint_scoring_allowed",
        ],
    )

    mean_z_by_bin = {row["source_bin"]: float(row["mean_z"]) for row in redshift_rows}
    if set(mean_z_by_bin) != {"1", "2", "3", "4", "5"}:
        raise SystemExit("redshift inventory must contain source bins 1..5")
    max_pair_mean_z = max((a + b) / 2.0 for a in mean_z_by_bin.values() for b in mean_z_by_bin.values())
    if max_pair_mean_z <= 0:
        raise SystemExit("max pair mean-z must be positive")

    rows: list[dict[str, str]] = []
    values: list[float] = []
    for row in shell_rows:
        bin1 = row["bin1"]
        bin2 = row["bin2"]
        mode = int(row["mode"])
        mask_value = float(row["source_mask_shell_value"])
        pair_mean_z = (mean_z_by_bin[bin1] + mean_z_by_bin[bin2]) / 2.0
        normalized_pair_mean_z_weight = pair_mean_z / max_pair_mean_z
        mode_decay_weight = 1.0 / sqrt(mode)
        partial_mapping_value = mask_value * normalized_pair_mean_z_weight * mode_decay_weight
        values.append(partial_mapping_value)
        rows.append(
            {
                **row,
                "mapping_values_policy_id": policy["policy_id"],
                "formula_id": policy["formula_id"],
                "pair_mean_z": f"{pair_mean_z:.12g}",
                "max_pair_mean_z": f"{max_pair_mean_z:.12g}",
                "normalized_pair_mean_z_weight": f"{normalized_pair_mean_z_weight:.12g}",
                "mode_decay_weight": f"{mode_decay_weight:.12g}",
                "partial_mapping_value": f"{partial_mapping_value:.12g}",
                "partial_mapping_values_computed": "true",
                "contains_partial_mapping_values": "true",
                "contains_endpoint_mapping_vector": "false",
                "contains_theory_vector": "false",
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

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_BUILT_SOURCE_ONLY_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "control_scope": policy["control_scope"],
        "formula_id": policy["formula_id"],
        "shell_rows": str(len(rows)),
        "target_rows": str(len({row["target_row_index_zero_based"] for row in rows})),
        "mask_control_rows": str(len({row["mask_sample_index_zero_based"] for row in rows})),
        "partial_mapping_values_computed": "true",
        "contains_partial_mapping_values": "true",
        "contains_endpoint_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "partial_control_scoring_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "value_min": f"{min(values):.12g}",
        "value_max": f"{max(values):.12g}",
        "max_abs_value": f"{max(abs(value) for value in values):.12g}",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_VALUES_V1_BUILT "
        f"rows={len(rows)} scoring=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
