#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_null_control_theory_replay_policy_v1.csv"
SEEDS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_seed_inventory_v1.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_theory_replay_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def digest(values: list[float]) -> str:
    payload = "\n".join(f"{value:.12e}" for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def stats(values: list[float]) -> dict[str, str]:
    n = len(values)
    mean = sum(values) / n
    l2 = math.sqrt(sum(value * value for value in values))
    centered = [value - mean for value in values]
    std = math.sqrt(sum(value * value for value in centered) / n)
    return {
        "vector_mean": f"{mean:.12e}",
        "vector_std": f"{std:.12e}",
        "vector_l2_norm": f"{l2:.12e}",
        "vector_min": f"{min(values):.12e}",
        "vector_max": f"{max(values):.12e}",
        "vector_sha256": digest(values),
    }


def main() -> None:
    policy = read_one(POLICY)
    seeds = read_rows(SEEDS)
    theory_rows = read_rows(THEORY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("null-control theory replay policy must remain endpoint disabled")
    if policy["current_control_scores_computed"] != "false":
        raise SystemExit("null-control theory replay must not compute scores")
    if any(row["endpoint_scoring_allowed"] != "false" for row in seeds):
        raise SystemExit("seed inventory must remain endpoint disabled")
    if any(row["contains_control_scores"] != "false" for row in seeds):
        raise SystemExit("seed inventory must not contain scores")
    if any(row["contains_prediction"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory shell must not be marked as prediction")
    if any(row["contains_residual"] != "false" for row in theory_rows):
        raise SystemExit("source-frozen theory shell must not contain residuals")

    theory_rows.sort(key=lambda row: int(row["row_index_zero_based"]))
    base_values = [float(row["theory_value"]) for row in theory_rows]
    pair_order: list[str] = []
    for row in theory_rows:
        if row["pair_id"] not in pair_order:
            pair_order.append(row["pair_id"])
    by_pair_mode = {
        (row["pair_id"], int(row["mode"])): float(row["theory_value"]) for row in theory_rows
    }

    out_rows: list[dict[str, str]] = []
    control_index = 0
    for seed_row in seeds:
        family = seed_row["control_family"]
        seed = int(seed_row["seed"])
        multiplicity = int(seed_row["multiplicity"])
        for draw_index in range(multiplicity):
            control_index += 1
            operator = ""
            if family == "sky_rotation":
                shift = (draw_index + 1) % len(pair_order)
                rotated = pair_order[shift:] + pair_order[:shift]
                pair_map = dict(zip(pair_order, rotated))
                values = [
                    by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows
                ]
                operator = f"cyclic_pair_shift_{shift}"
            elif family == "tomographic_pair_shuffle":
                rng = random.Random(seed + draw_index)
                shuffled = pair_order[:]
                rng.shuffle(shuffled)
                pair_map = dict(zip(pair_order, shuffled))
                values = [
                    by_pair_mode[(pair_map[row["pair_id"]], int(row["mode"]))] for row in theory_rows
                ]
                operator = f"seeded_pair_shuffle_{seed + draw_index}"
            elif family == "wrong_channel_activation":
                values = [0.0 for _ in base_values]
                operator = (
                    "wrong_channel_web_null_zero"
                    if draw_index == 0
                    else "wrong_channel_disabled_time_zero"
                )
            elif family == "web_path_sign_flip":
                if draw_index == 0:
                    values = [-value for value in base_values]
                    operator = "path_sign_flip_negative"
                else:
                    values = [0.0 for _ in base_values]
                    operator = "path_removed_zero_control"
            else:
                raise SystemExit(f"unexpected null-control family: {family}")

            row = {
                "policy_id": policy["policy_id"],
                "parent_null_control_policy": policy["parent_null_control_policy"],
                "parent_seed_policy": policy["parent_seed_policy"],
                "parent_theory_vector": policy["parent_theory_vector"],
                "selected_statistic": policy["selected_statistic"],
                "control_index_one_based": str(control_index),
                "control_family": family,
                "control_draw_index_zero_based": str(draw_index),
                "seed": seed_row["seed"],
                "operator": operator,
                "target_rows": str(len(values)),
                "current_control_theory_replay_executed": "true",
                "contains_theory_vector": "true",
                "contains_control_scores": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_control_selection": "false",
                "uses_posthoc_control_multiplicity": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
            row.update(stats(values))
            out_rows.append(row)

    expected = int(policy["total_declared_control_draws"])
    if len(out_rows) != expected:
        raise SystemExit(f"expected {expected} replay controls, got {len(out_rows)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_BUILT_NOT_SCORED",
        "selected_statistic": policy["selected_statistic"],
        "control_family_count": policy["control_family_count"],
        "control_draw_count": str(len(out_rows)),
        "target_rows_per_control": str(len(base_values)),
        "unique_control_digest_count": str(len({row["vector_sha256"] for row in out_rows})),
        "current_control_theory_replay_executed": "true",
        "contains_theory_vector": "true",
        "contains_control_scores": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_control_selection": "false",
        "uses_posthoc_control_multiplicity": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_NULL_CONTROL_THEORY_REPLAY_V1_BUILT "
        f"controls={summary['control_draw_count']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()
