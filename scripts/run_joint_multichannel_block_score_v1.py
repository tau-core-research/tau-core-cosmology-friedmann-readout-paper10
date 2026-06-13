#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import math
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
OUT = ROOT / "data/derived/joint_multichannel_block_score_v1.csv"
CONTROLS = ROOT / "data/derived/joint_multichannel_block_score_v1_controls.csv"
LOO = ROOT / "data/derived/joint_multichannel_block_score_v1_leave_one_channel.csv"
SUMMARY = ROOT / "data/derived/joint_multichannel_block_score_v1_summary.csv"
DOC = ROOT / "docs/joint_multichannel_block_score_v1.md"
CLAIM_BOUNDARY = "joint_multichannel_block_score_prevalidation_not_joint_likelihood"
SEED = 100913


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def weighted_sum(rows: list[dict[str, str]]) -> float:
    return sum(float(row["weighted_channel_score"]) for row in rows)


def effective_sigma(rows: list[dict[str, str]]) -> float:
    return math.sqrt(sum(float(row["channel_weight"]) ** 2 for row in rows if float(row["channel_weight"]) != 0.0))


def normalized_score(rows: list[dict[str, str]]) -> float:
    sigma = effective_sigma(rows)
    return weighted_sum(rows) / sigma if sigma else 0.0


def main() -> None:
    rows = read_rows(INPUT)
    active_rows = [row for row in rows if float(row["channel_weight"]) != 0.0]
    if len(active_rows) < 4:
        raise SystemExit("need at least four nonzero-weight channels for block scoring")

    obs_sum = weighted_sum(active_rows)
    obs_norm = normalized_score(active_rows)
    abs_weight = sum(abs(float(row["channel_weight"])) for row in active_rows)
    protocol_normalized = obs_sum / abs_weight if abs_weight else 0.0

    score_rows = []
    for row in rows:
        score_rows.append(
            {
                "block_score_id": "JOINT_MULTICHANNEL_BLOCK_SCORE_V1",
                "channel_id": row["channel_id"],
                "bounded_channel_score": row["bounded_channel_score"],
                "channel_weight": row["channel_weight"],
                "weighted_channel_score": row["weighted_channel_score"],
                "included_in_block_score": str(float(row["channel_weight"]) != 0.0).lower(),
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    control_rows = []
    values = [float(row["weighted_channel_score"]) for row in active_rows]
    channel_ids = [row["channel_id"] for row in active_rows]

    # Exact sign-flip control over the nonzero weighted block contributions.
    sign_scores = []
    for idx, signs in enumerate(itertools.product([-1, 1], repeat=len(values))):
        s = sum(sign * value for sign, value in zip(signs, values, strict=True))
        norm = s / effective_sigma(active_rows)
        sign_scores.append(norm)
        control_rows.append(
            {
                "control_id": f"exact_sign_flip_{idx:03d}",
                "control_family": "exact_sign_flip_nonzero_channels",
                "seed": "deterministic_complete_enumeration",
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= obs_norm).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    # Deterministic channel-label shuffle control. This tests whether the same
    # scores look as good after the frozen weights are reassigned to channels.
    rng = random.Random(SEED)
    weights = [float(row["channel_weight"]) for row in active_rows]
    bounded = [float(row["bounded_channel_score"]) for row in active_rows]
    for idx in range(1000):
        shuffled = weights[:]
        rng.shuffle(shuffled)
        s = sum(weight * score for weight, score in zip(shuffled, bounded, strict=True))
        sigma = math.sqrt(sum(weight * weight for weight in shuffled))
        norm = s / sigma if sigma else 0.0
        control_rows.append(
            {
                "control_id": f"seeded_weight_shuffle_{idx:04d}",
                "control_family": "seeded_channel_weight_shuffle",
                "seed": str(SEED),
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= obs_norm).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    p_sign = sum(1 for score in sign_scores if score >= obs_norm) / len(sign_scores)
    p_all = sum(1 for row in control_rows if row["beats_observed"] == "true") / len(control_rows)

    loo_rows = []
    for row in active_rows:
        subset = [r for r in active_rows if r["channel_id"] != row["channel_id"]]
        loo_sum = weighted_sum(subset)
        loo_norm = normalized_score(subset)
        loo_abs = sum(abs(float(r["channel_weight"])) for r in subset)
        loo_protocol = loo_sum / loo_abs if loo_abs else 0.0
        loo_rows.append(
            {
                "block_score_id": "JOINT_MULTICHANNEL_BLOCK_SCORE_V1",
                "dropped_channel_id": row["channel_id"],
                "leave_one_weighted_sum": f"{loo_sum:.9f}",
                "leave_one_block_normalized_score": f"{loo_norm:.9f}",
                "leave_one_protocol_normalized_score": f"{loo_protocol:.9f}",
                "retains_positive_score": str(loo_sum > 0).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    retains = sum(1 for row in loo_rows if row["retains_positive_score"] == "true")
    if obs_norm > 0.0 and retains == len(loo_rows):
        verdict = "JOINT_BLOCK_SCORE_POSITIVE_BUT_CONTROL_LIMITED_PREVALIDATION"
    else:
        verdict = "JOINT_BLOCK_SCORE_FRAGILE_OR_INCONCLUSIVE_PREVALIDATION"

    summary = {
        "block_score_id": "JOINT_MULTICHANNEL_BLOCK_SCORE_V1",
        "nonzero_weight_channels": str(len(active_rows)),
        "channel_order": ";".join(channel_ids),
        "weighted_sum": f"{obs_sum:.9f}",
        "block_normalized_score": f"{obs_norm:.9f}",
        "protocol_normalized_score": f"{protocol_normalized:.9f}",
        "exact_sign_flip_control_count": str(2 ** len(active_rows)),
        "exact_sign_flip_one_sided_p_ge_observed": f"{p_sign:.9f}",
        "combined_control_count": str(len(control_rows)),
        "combined_control_one_sided_p_ge_observed": f"{p_all:.9f}",
        "leave_one_positive_count": str(retains),
        "leave_one_total_count": str(len(loo_rows)),
        "verdict": verdict,
        "joint_likelihood_claimed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "next_required_gate": "replace_block_score_with_single_joint_likelihood_and_cross_probe_covariance",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, score_rows)
    write_csv(CONTROLS, control_rows)
    write_csv(LOO, loo_rows)
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint multichannel block score v1",
                "",
                "**Doc class:** block-aware joint-score preflight",
                "**Status:** not a joint likelihood; not endpoint validation",
                "",
                "This score combines the already frozen joint-channel candidate rows",
                "using their weighted channel contributions. It adds exact sign-flip",
                "controls, seeded channel-weight shuffles, and leave-one-channel checks.",
                "It does not access raw endpoint residuals and does not estimate a",
                "cross-probe covariance.",
                "",
                "Summary:",
                "",
                f"- nonzero-weight channels: `{summary['nonzero_weight_channels']}`",
                f"- block-normalized score: `{summary['block_normalized_score']}`",
                f"- protocol-normalized score: `{summary['protocol_normalized_score']}`",
                f"- exact sign-flip p(score >= observed): `{summary['exact_sign_flip_one_sided_p_ge_observed']}`",
                f"- leave-one positive: `{summary['leave_one_positive_count']}/{summary['leave_one_total_count']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )

    print(
        "JOINT_MULTICHANNEL_BLOCK_SCORE_V1_RUN "
        f"block_normalized_score={summary['block_normalized_score']} "
        f"p_sign={summary['exact_sign_flip_one_sided_p_ge_observed']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
