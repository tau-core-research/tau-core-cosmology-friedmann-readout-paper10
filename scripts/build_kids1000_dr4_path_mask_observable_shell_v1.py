#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_observable_shell_policy_v1.csv"
INVENTORY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_observable_shell_v1_summary.csv"

FILENAME_RE = re.compile(
    r"KiDS_DR4\.1_(?P<ra>[0-9.]+)_(?P<dec>-?[0-9.]+)_ugriZYJHKs_msk\.fits\.gz$"
)


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def parse_tile_coordinates(local_path: str) -> tuple[str, str]:
    match = FILENAME_RE.search(Path(local_path).name)
    if not match:
        raise SystemExit(f"could not parse KiDS tile coordinates from {local_path}")
    return match.group("ra"), match.group("dec")


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("observable shell policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("observable shell must not compute path mapping")
    if policy["current_theory_vector_computed"].lower() != "false":
        raise SystemExit("observable shell must not compute theory vectors")
    if policy["parent_subset_inventory"] != str(INVENTORY.relative_to(ROOT)):
        raise SystemExit("unexpected parent subset inventory")

    with INVENTORY.open(newline="") as f:
        inventory_rows = list(csv.DictReader(f))
    if len(inventory_rows) != int(policy["expected_subset_count"]):
        raise SystemExit("unexpected source mask subset size")

    zero_fractions = [
        1.0 - float(row["nonzero_finite_fraction"])
        for row in inventory_rows
    ]
    mean_zero_fraction = sum(zero_fractions) / len(zero_fractions)
    centered = [value - mean_zero_fraction for value in zero_fractions]
    scale = max(abs(value) for value in centered) or 1.0

    rows: list[dict[str, str]] = []
    for row, zero_fraction, centered_value in zip(inventory_rows, zero_fractions, centered):
        tile_ra, tile_dec = parse_tile_coordinates(row["local_path"])
        shell_value = centered_value / scale
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy_id": row["policy_id"],
                "sample_index_zero_based": row["sample_index_zero_based"],
                "local_path": row["local_path"],
                "tile_ra_deg_filename_proxy": tile_ra,
                "tile_dec_deg_filename_proxy": tile_dec,
                "mask_nonzero_finite_fraction": f"{float(row['nonzero_finite_fraction']):.12e}",
                "mask_zero_finite_fraction_proxy": f"{zero_fraction:.12e}",
                "mean_finite_value": row["mean_finite_value"],
                "mask_shell_centered_zero_fraction": f"{centered_value:.12e}",
                "source_mask_shell_value": f"{shell_value:.12e}",
                "source_shell_scope": "three_mask_subset_only",
                "tile_coordinate_source": "KiDS_mask_filename_token",
                "mask_value_semantics_interpreted": "false",
                "source_observable_shell_computed": "true",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_path_projection_labels": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_dr4_path_mask_observable_shell_source_only_not_mapping_not_validation",
            }
        )

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_BUILT_SOURCE_ONLY_NOT_SCORED",
        "subset_count": str(len(rows)),
        "mean_mask_zero_finite_fraction_proxy": f"{mean_zero_fraction:.12e}",
        "min_source_mask_shell_value": f"{min(float(row['source_mask_shell_value']) for row in rows):.12e}",
        "max_source_mask_shell_value": f"{max(float(row['source_mask_shell_value']) for row in rows):.12e}",
        "source_observable_shell_computed": "true",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_path_projection_labels": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_dr4_path_mask_observable_shell_source_only_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS_DR4_PATH_MASK_OBSERVABLE_SHELL_V1_BUILT "
        f"subset={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
