#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_seed_policy_v1.csv"
NULL_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"


FAMILY_RULES = {
    "sky_rotation": {
        "seed": "601001",
        "multiplicity": "4",
        "control_shell": "deterministic_sky_rotation_angles",
        "source_frozen_descriptor": "predeclare_rotation_angle_grid_without_applying_to_data",
    },
    "tomographic_pair_shuffle": {
        "seed": "601002",
        "multiplicity": "1000",
        "control_shell": "deterministic_pair_shuffle_catalog",
        "source_frozen_descriptor": "predeclare_pair_shuffle_seed_without_permuting_data_vector",
    },
    "wrong_channel_activation": {
        "seed": "601003",
        "multiplicity": "2",
        "control_shell": "wrong_channel_activation_table",
        "source_frozen_descriptor": "predeclare_disabled_channel_controls_without_theory_vector",
    },
    "web_path_sign_flip": {
        "seed": "601004",
        "multiplicity": "2",
        "control_shell": "web_path_sign_flip_table",
        "source_frozen_descriptor": "predeclare_sign_flip_controls_without_mapping_vector",
    },
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    null_policy = read_one(NULL_POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("null-control seed policy must remain endpoint disabled")
    if policy["current_controls_executed"].lower() != "false":
        raise SystemExit("null controls must not be executed in this gate")
    if null_policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("null-control parent policy must remain endpoint disabled")
    families = null_policy["control_families"].split(";")
    if set(families) != set(FAMILY_RULES):
        raise SystemExit("null-control seed rules must cover readiness families exactly")

    rows: list[dict[str, str]] = []
    for family in families:
        rule = FAMILY_RULES[family]
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "selected_statistic": policy["selected_statistic"],
                "control_family": family,
                "control_shell": rule["control_shell"],
                "seed": rule["seed"],
                "multiplicity": rule["multiplicity"],
                "source_frozen_descriptor": rule["source_frozen_descriptor"],
                "current_control_executed": "false",
                "contains_control_scores": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_seed_selection": "false",
                "uses_posthoc_control_multiplicity": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_cosebis_null_control_seed_inventory_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_NULL_CONTROL_SEED_INVENTORY_BUILT_NOT_RUN",
        "selected_statistic": policy["selected_statistic"],
        "control_family_count": str(len(rows)),
        "total_declared_control_draws": str(sum(int(row["multiplicity"]) for row in rows)),
        "current_seed_policy_frozen": policy["current_seed_policy_frozen"],
        "current_controls_executed": "false",
        "contains_control_scores": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_seed_selection": "false",
        "uses_posthoc_control_multiplicity": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_cosebis_null_control_seed_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_SEED_INVENTORY_V1_BUILT "
        f"controls={len(rows)} draws={summary['total_declared_control_draws']} executed=false"
    )


if __name__ == "__main__":
    main()
