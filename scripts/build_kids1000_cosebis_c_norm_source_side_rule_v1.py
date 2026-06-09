#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_c_norm_source_side_rule_policy_v1.csv"
F_OVERLAP = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_route_pixel_fraction_rule_v1.csv"
D_PATH = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv"
E_WEB = ROOT / "data" / "derived" / "kids1000_cosebis_e_web_null_control_rule_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv"


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
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("C_norm policy must keep endpoint scoring disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("C_norm policy must not compute path mapping")
    if policy["current_theory_vector_computed"].lower() != "false":
        raise SystemExit("C_norm policy must not compute theory vectors")

    f_rows = read_rows(F_OVERLAP)
    d_rows = read_rows(D_PATH)
    e_rows = read_rows(E_WEB)
    expected_rows = int(policy["expected_domain_rows"])
    if not (len(f_rows) == len(d_rows) == len(e_rows) == expected_rows):
        raise SystemExit("C_norm requires aligned 58,800-row source-factor ledgers")

    rows: list[dict[str, str]] = []
    raw_values: list[float] = []
    for f_row, d_row, e_row in zip(f_rows, d_rows, e_rows, strict=True):
        key = (
            f_row["domain_row_index_zero_based"],
            f_row["target_row_index_zero_based"],
            f_row["tile_index_zero_based"],
        )
        if key != (
            d_row["domain_row_index_zero_based"],
            d_row["target_row_index_zero_based"],
            d_row["tile_index_zero_based"],
        ):
            raise SystemExit("F_overlap and D_path rows are not aligned")
        if key != (
            e_row["domain_row_index_zero_based"],
            e_row["target_row_index_zero_based"],
            e_row["tile_index_zero_based"],
        ):
            raise SystemExit("F_overlap and E_web rows are not aligned")
        f_val = float(f_row["f_overlap_value"])
        d_val = float(d_row["d_path_value"])
        e_val = float(e_row["e_web_value"])
        raw = f_val * d_val * e_val
        raw_values.append(raw)
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "domain_row_index_zero_based": key[0],
                "target_row_index_zero_based": key[1],
                "tile_index_zero_based": key[2],
                "pair_id": f_row["pair_id"],
                "mode": f_row["mode"],
                "f_overlap_value": f"{f_val:.12e}",
                "d_path_value": f"{d_val:.12e}",
                "e_web_value": f"{e_val:.12e}",
                "raw_source_weight_fde": f"{raw:.12e}",
                "c_norm_rule": policy["c_norm_rule"],
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_weight_selection": "false",
                "uses_posthoc_tile_selection": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "uses_posthoc_web_environment_labels": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    if any(value <= 0.0 for value in raw_values):
        raise SystemExit("C_norm source-side raw weights must be strictly positive")
    mean_raw = sum(raw_values) / len(raw_values)
    if mean_raw <= 0.0:
        raise SystemExit("C_norm source-side mean raw weight collapsed")
    c_norm = 1.0 / mean_raw

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    normalized_values = [value * c_norm for value in raw_values]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED",
        "domain_rows": str(len(rows)),
        "source_scope": policy["source_scope"],
        "c_norm_rule": policy["c_norm_rule"],
        "min_raw_source_weight_fde": f"{min(raw_values):.12e}",
        "max_raw_source_weight_fde": f"{max(raw_values):.12e}",
        "mean_raw_source_weight_fde": f"{mean_raw:.12e}",
        "c_norm_value": f"{c_norm:.12e}",
        "mean_normalized_source_weight_fde": f"{sum(normalized_values) / len(normalized_values):.12e}",
        "min_normalized_source_weight_fde": f"{min(normalized_values):.12e}",
        "max_normalized_source_weight_fde": f"{max(normalized_values):.12e}",
        "c_norm_source_route_support": "true",
        "c_norm_positive_raw_support": "true",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_weight_selection": "false",
        "uses_posthoc_tile_selection": "false",
        "uses_posthoc_sky_direction_selection": "false",
        "uses_posthoc_web_environment_labels": "false",
        "uses_posthoc_path_projection_labels": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)

    print(
        "PAPER10_KIDS1000_COSEBIS_C_NORM_SOURCE_SIDE_RULE_V1_BUILT "
        f"domain_rows={len(rows)} c_norm={c_norm:.12e} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
