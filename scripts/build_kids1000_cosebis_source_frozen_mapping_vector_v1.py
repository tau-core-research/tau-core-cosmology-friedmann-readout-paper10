#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_frozen_mapping_vector_policy_v1.csv"
DESIGN = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_design_skeleton_v1.csv"
C_NORM_DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_domain_rule_v1.csv"
C_NORM_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_c_norm_source_side_rule_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_domain_weights_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"


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
    c_norm_summary = read_one(C_NORM_SUMMARY)
    design_rows = read_rows(DESIGN)
    domain_rows = read_rows(C_NORM_DOMAIN)

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mapping-vector policy must keep endpoint scoring disabled")
    if policy["current_theory_vector_computed"] != "false":
        raise SystemExit("mapping-vector policy must not compute a theory vector")
    if len(design_rows) != int(policy["expected_target_rows"]):
        raise SystemExit("unexpected target-row count for mapping vector")
    if len(domain_rows) != int(policy["expected_domain_rows"]):
        raise SystemExit("unexpected domain-row count for mapping vector")
    c_norm = float(c_norm_summary["c_norm_value"])
    if c_norm <= 0.0:
        raise SystemExit("C_norm must be positive before mapping")

    n_pair_raw_by_row = {
        row["target_row_index_zero_based"]: 0.5 * (float(row["bin1_mean_z"]) + float(row["bin2_mean_z"]))
        for row in design_rows
    }
    mean_n_pair = sum(n_pair_raw_by_row.values()) / len(n_pair_raw_by_row)
    if mean_n_pair <= 0.0:
        raise SystemExit("redshift-pair source factor collapsed")

    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    domain_out: list[dict[str, str]] = []
    for row in domain_rows:
        target = row["target_row_index_zero_based"]
        raw_fde = float(row["raw_source_weight_fde"])
        normalized_fde = raw_fde * c_norm
        n_pair_factor = n_pair_raw_by_row[target] / mean_n_pair
        mapping_weight = normalized_fde * n_pair_factor
        sums[target] += mapping_weight
        counts[target] += 1
        domain_out.append(
            {
                "policy_id": policy["policy_id"],
                "domain_row_index_zero_based": row["domain_row_index_zero_based"],
                "target_row_index_zero_based": target,
                "tile_index_zero_based": row["tile_index_zero_based"],
                "pair_id": row["pair_id"],
                "mode": row["mode"],
                "normalized_fde_weight": f"{normalized_fde:.12e}",
                "n_pair_raw": f"{n_pair_raw_by_row[target]:.12e}",
                "n_pair_unit_mean_factor": f"{n_pair_factor:.12e}",
                "source_frozen_mapping_domain_weight": f"{mapping_weight:.12e}",
                "path_mapping_computed": "true",
                "contains_mapping_vector": "true",
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

    design_by_target = {row["target_row_index_zero_based"]: row for row in design_rows}
    out_rows: list[dict[str, str]] = []
    values: list[float] = []
    for target in sorted(sums, key=lambda item: int(item)):
        if counts[target] != 196:
            raise SystemExit("each COSEBIs row must aggregate all 196 route tiles")
        mapping_value = sums[target] / counts[target]
        values.append(mapping_value)
        design = design_by_target[target]
        out_rows.append(
            {
                "policy_id": policy["policy_id"],
                "row_index_zero_based": target,
                "row_index_one_based": str(int(target) + 1),
                "selected_statistic": policy["selected_statistic"],
                "pair_id": design["pair_id"],
                "bin1": design["bin1"],
                "bin2": design["bin2"],
                "mode": design["mode"],
                "source_frozen_mapping_value": f"{mapping_value:.12e}",
                "w_path_basis": f"{mapping_value:.12e}",
                "w_web_basis": "0.000000000000e+00",
                "baseline_basis": "1.000000000000e+00",
                "n_pair_unit_mean_factor": f"{n_pair_raw_by_row[target] / mean_n_pair:.12e}",
                "tile_count_aggregated": str(counts[target]),
                "mapping_rule": policy["mapping_rule"],
                "positive_web_claim_allowed": "false",
                "mode_shape_generated": "false",
                "path_mapping_computed": "true",
                "contains_mapping_vector": "true",
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

    unique_values = {round(value, 12) for value in values}
    positive = all(value > 0.0 for value in values)
    mode_degenerate_pairs = len({(row["pair_id"], row["source_frozen_mapping_value"]) for row in out_rows})
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_BUILT_NOT_THEORY_NOT_SCORED",
        "target_rows": str(len(out_rows)),
        "domain_rows": str(len(domain_out)),
        "mapping_vector_computed": "true",
        "path_mapping_computed": "true",
        "contains_mapping_vector": "true",
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
        "min_mapping_value": f"{min(values):.12e}",
        "max_mapping_value": f"{max(values):.12e}",
        "mean_mapping_value": f"{sum(values) / len(values):.12e}",
        "unique_mapping_value_count_rounded_1e_minus_12": str(len(unique_values)),
        "positive_mapping_support": str(positive).lower(),
        "positive_web_claim_allowed": "false",
        "mode_shape_generated": "false",
        "pair_level_mode_degenerate_value_count": str(mode_degenerate_pairs),
        "limitation": "source_frozen_mapping_vector_has_pair_redshift_and_path_variation_but_no_mode_shape_or_theory_vector",
        "claim_boundary": policy["claim_boundary"],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with DOMAIN_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(domain_out[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(domain_out)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_FROZEN_MAPPING_VECTOR_V1_BUILT "
        f"rows={len(out_rows)} unique={len(unique_values)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
