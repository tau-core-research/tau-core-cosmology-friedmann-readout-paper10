#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_mapping_shell_policy_v1.csv"
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_scoring_protocol_v1.csv"
F_OVERLAP_DECISION = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1.csv"
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_template_v1_summary.csv"
MASK_SHELL = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1.csv"
MASK_SHELL_SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_mapping_shell_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    protocol = read_one(PROTOCOL)
    f_overlap = read_one(F_OVERLAP_DECISION)
    template_summary = read_one(TEMPLATE_SUMMARY)
    mask_summary = read_one(MASK_SHELL_SUMMARY)
    with TEMPLATE.open(newline="") as f:
        template_rows = list(csv.DictReader(f))
    with MASK_SHELL.open(newline="") as f:
        mask_rows = list(csv.DictReader(f))

    if policy["current_endpoint_scoring_allowed"] != "false":
        raise SystemExit("partial-control mapping shell must keep endpoint scoring disabled")
    if policy["current_partial_control_scoring_allowed"] != "false":
        raise SystemExit("partial-control mapping shell must not enable control scoring")
    if policy["current_partial_mapping_values_computed"] != "false":
        raise SystemExit("partial-control mapping shell must not compute mapping values")
    if policy["current_theory_values_computed"] != "false":
        raise SystemExit("partial-control mapping shell must not compute theory values")
    if protocol["protocol_id"] != policy["parent_partial_control_protocol"]:
        raise SystemExit("unexpected partial-control protocol parent")
    if protocol["partial_control_scoring_allowed"] != "false":
        raise SystemExit("parent partial-control protocol must remain frozen-not-run")
    if f_overlap["f_overlap_endpoint_ready"] != "true" or f_overlap["f_overlap_control_ready"] != "true":
        raise SystemExit("partial-control mapping shell requires source-supported F_overlap decision")
    if f_overlap["endpoint_scoring_allowed"] != "false":
        raise SystemExit("partial-control mapping shell must not inherit endpoint scoring permission")
    if f_overlap["accepted_control_scope"] != policy["control_scope"]:
        raise SystemExit("partial-control scope mismatch")
    if template_summary["template_rows"] != policy["expected_target_rows"]:
        raise SystemExit("template row count mismatch")
    if mask_summary["subset_count"] != policy["expected_mask_control_rows"]:
        raise SystemExit("mask control row count mismatch")
    if len(template_rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected target row count")
    if len(mask_rows) != int(policy["expected_mask_control_rows"]):
        raise SystemExit("unexpected mask-control row count")

    rows: list[dict[str, str]] = []
    shell_index = 0
    for template in template_rows:
        for mask in mask_rows:
            rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "partial_control_protocol": policy["parent_partial_control_protocol"],
                    "selected_statistic": policy["selected_statistic"],
                    "control_scope": policy["control_scope"],
                    "shell_row_index_zero_based": str(shell_index),
                    "target_row_index_zero_based": template["row_index_zero_based"],
                    "target_row_index_one_based": template["row_index_one_based"],
                    "pair_id": template["pair_id"],
                    "bin1": template["bin1"],
                    "bin2": template["bin2"],
                    "mode": template["mode"],
                    "mask_sample_index_zero_based": mask["sample_index_zero_based"],
                    "mask_local_path": mask["local_path"],
                    "tile_ra_deg_filename_proxy": mask["tile_ra_deg_filename_proxy"],
                    "tile_dec_deg_filename_proxy": mask["tile_dec_deg_filename_proxy"],
                    "source_mask_shell_value": mask["source_mask_shell_value"],
                    "source_shell_scope": mask["source_shell_scope"],
                    "tile_coordinate_source": mask["tile_coordinate_source"],
                    "mapping_shell_row_only": "true",
                    "partial_mapping_value": "",
                    "partial_mapping_values_computed": "false",
                    "contains_mapping_vector": "false",
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
            shell_index += 1

    if len(rows) != int(policy["expected_shell_rows"]):
        raise SystemExit("unexpected partial-control mapping shell row count")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_BUILT_NOT_MAPPED",
        "selected_statistic": policy["selected_statistic"],
        "control_scope": policy["control_scope"],
        "target_rows": str(len(template_rows)),
        "mask_control_rows": str(len(mask_rows)),
        "shell_rows": str(len(rows)),
        "mapping_shell_built": "true",
        "partial_mapping_values_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
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
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_MAPPING_SHELL_V1_BUILT "
        f"rows={len(rows)} mapping=false scoring=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
