#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_policy_v1.csv"
INVENTORY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_tile_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_pixel_fraction_pilot_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def float_text(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("pixel-fraction pilot policy must keep endpoint scoring disabled")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("pixel-fraction pilot must not compute path mapping")
    if policy["current_theory_vector_computed"] != "false":
        raise SystemExit("pixel-fraction pilot must not compute theory vectors")

    with INVENTORY.open(newline="") as f:
        inventory_rows = list(csv.DictReader(f))
    expected = int(policy["expected_tile_count"])
    if len(inventory_rows) != expected:
        raise SystemExit("pixel-fraction pilot requires the frozen three-mask subset inventory")

    fractions = [float(row["nonzero_finite_fraction"]) for row in inventory_rows]
    max_fraction = max(fractions)
    min_fraction = min(fractions)
    mean_fraction = sum(fractions) / len(fractions)
    if max_fraction <= 0.0:
        raise SystemExit("nonzero finite fractions must contain positive source support")

    tile_rows: list[dict[str, str]] = []
    for row, fraction in zip(inventory_rows, fractions):
        f_overlap = fraction / max_fraction
        tile_rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy_id": row["policy_id"],
                "sample_index_zero_based": row["sample_index_zero_based"],
                "local_path": row["local_path"],
                "sha256": row["sha256"],
                "source_scope": policy["source_scope"],
                "pixel_rule": policy["pixel_rule"],
                "mask_pixels_parsed_upstream": row["mask_pixels_parsed"],
                "mask_nonzero_finite_fraction": float_text(fraction),
                "f_overlap_pixel_fraction_value": float_text(f_overlap),
                "normalization_rule": policy["normalization_rule"],
                "pixel_fraction_pilot_computed": "true",
                "full_route_pixel_rule_computed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    values = [float(row["f_overlap_pixel_fraction_value"]) for row in tile_rows]
    unique_values = len({round(value, 12) for value in values})
    non_degenerate = unique_values > 1 and (max(values) - min(values)) > 1e-6
    TILE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with TILE_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tile_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(tile_rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_BUILT_SOURCE_ONLY_NOT_MAPPED",
        "tile_count": str(len(tile_rows)),
        "source_scope": policy["source_scope"],
        "pixel_rule": policy["pixel_rule"],
        "min_mask_nonzero_finite_fraction": float_text(min_fraction),
        "max_mask_nonzero_finite_fraction": float_text(max_fraction),
        "mean_mask_nonzero_finite_fraction": float_text(mean_fraction),
        "min_f_overlap_pixel_fraction_value": float_text(min(values)),
        "max_f_overlap_pixel_fraction_value": float_text(max(values)),
        "mean_f_overlap_pixel_fraction_value": float_text(sum(values) / len(values)),
        "unique_f_overlap_value_count_rounded_1e_minus_12": str(unique_values),
        "pixel_fraction_pilot_non_degenerate": "true" if non_degenerate else "false",
        "header_footprint_rule_uniformity_resolved_for_subset": "true" if non_degenerate else "false",
        "full_route_pixel_rule_computed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "uses_posthoc_path_projection_labels": "false",
        "endpoint_scoring_allowed": "false",
        "recommended_next_action": "promote_to_full_route_pixel_or_subtile_rule_with_streaming_cache_before_endpoint_scoring",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_PIXEL_FRACTION_PILOT_V1_BUILT "
        f"tiles={len(tile_rows)} non_degenerate={summary['pixel_fraction_pilot_non_degenerate']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
