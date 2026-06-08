#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_seed_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1_summary.csv"


EXPECTED = {
    "sky_rotation": ("601001", "4"),
    "tomographic_pair_shuffle": ("601002", "1000"),
    "wrong_channel_activation": ("601003", "2"),
    "web_path_sign_flip": ("601004", "2"),
}


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]

    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control seed policy must remain endpoint disabled")
    if policy["current_controls_executed"] != "false":
        raise SystemExit("null controls must not execute in the policy")
    if policy["current_seed_policy_frozen"] != "true":
        raise SystemExit("seed policy must be frozen")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control seed inventory must remain endpoint disabled")
    if summary["current_controls_executed"] != "false":
        raise SystemExit("null-control seed inventory must not execute controls")
    if summary["current_seed_policy_frozen"] != "true":
        raise SystemExit("summary must keep seed policy frozen")
    if len(rows) != len(EXPECTED):
        raise SystemExit("unexpected null-control seed row count")
    for key in [
        "contains_control_scores",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_seed_selection",
        "uses_posthoc_control_multiplicity",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    seen = {}
    for row in rows:
        family = row["control_family"]
        if family not in EXPECTED:
            raise SystemExit(f"unexpected null-control family: {family}")
        if (row["seed"], row["multiplicity"]) != EXPECTED[family]:
            raise SystemExit(f"unexpected seed/multiplicity for {family}")
        if int(row["seed"]) <= 0:
            raise SystemExit("seeds must be positive integers")
        if int(row["multiplicity"]) <= 0:
            raise SystemExit("multiplicity must be positive")
        if row["current_control_executed"] != "false":
            raise SystemExit("controls must not be executed")
        seen[family] = True
    if set(seen) != set(EXPECTED):
        raise SystemExit("missing null-control family")
    if int(summary["total_declared_control_draws"]) != sum(
        int(mult) for _, mult in EXPECTED.values()
    ):
        raise SystemExit("unexpected total declared control draws")
    for marker in [
        "posthoc_seed_selection",
        "posthoc_control_multiplicity",
        "kids_data_vector_values",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    if summary["status"] != "KIDS1000_COSEBIS_NULL_CONTROL_SEED_INVENTORY_BUILT_NOT_RUN":
        raise SystemExit("unexpected null-control seed inventory status")
    print("PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_SEED_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()
