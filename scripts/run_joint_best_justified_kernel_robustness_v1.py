#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import math
import random
from pathlib import Path

from run_joint_best_justified_kernel_score_v1 import GATE_ROWS, GATES


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/derived/joint_multichannel_endpoint_candidate_v1.csv"
OUT = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1.csv"
CONTROLS = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_controls.csv"
SUMMARY = ROOT / "data/derived/joint_best_justified_kernel_robustness_v1_summary.csv"
DOC = ROOT / "docs/joint_best_justified_kernel_robustness_v1.md"
CLAIM_BOUNDARY = "joint_best_justified_kernel_robustness_prevalidation_not_joint_likelihood"
SEED = 240914


SCHEMES: dict[str, dict[str, float]] = {
    "equal_geometric": {key: 1.0 / 7.0 for key in GATES},
    "source_heavy": {
        "g_src": 0.35,
        "g_tr": 0.15,
        "g_norm": 0.10,
        "g_ctrl": 0.10,
        "g_leak": 0.10,
        "g_dim": 0.10,
        "g_proj": 0.10,
    },
    "control_heavy": {
        "g_src": 0.10,
        "g_tr": 0.10,
        "g_norm": 0.10,
        "g_ctrl": 0.35,
        "g_leak": 0.15,
        "g_dim": 0.10,
        "g_proj": 0.10,
    },
    "projection_heavy": {
        "g_src": 0.10,
        "g_tr": 0.10,
        "g_norm": 0.10,
        "g_ctrl": 0.10,
        "g_leak": 0.10,
        "g_dim": 0.15,
        "g_proj": 0.35,
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def geometric_quality(row: dict[str, str], exponents: dict[str, float]) -> float:
    if row["positive_support_allowed"] != "true":
        return 0.0
    vals = {key: float(row[key]) for key in GATES}
    if min(vals.values()) <= 0.0:
        return 0.0
    return math.prod(vals[key] ** exponents[key] for key in GATES)


def min_gate_quality(row: dict[str, str]) -> float:
    if row["positive_support_allowed"] != "true":
        return 0.0
    vals = [float(row[key]) for key in GATES]
    if min(vals) <= 0.0:
        return 0.0
    return min(vals)


def score_scheme(
    scheme_id: str,
    q_by_channel: dict[str, float],
    bounded_scores: dict[str, float],
) -> tuple[dict[str, str], list[dict[str, str]]]:
    q_sum = sum(q_by_channel.values())
    if q_sum <= 0.0:
        raise SystemExit(f"no positive q for {scheme_id}")
    active = []
    for row in GATE_ROWS:
        channel = row["channel_id"]
        q = q_by_channel[channel]
        if q <= 0.0:
            continue
        weight = q / q_sum
        bounded = bounded_scores[channel]
        active.append(
            {
                "channel_id": channel,
                "bounded_channel_score": bounded,
                "Q_i": q,
                "w_i": weight,
                "weighted_channel_score": weight * bounded,
            }
        )

    weighted_sum = sum(row["weighted_channel_score"] for row in active)
    sigma = math.sqrt(sum(row["w_i"] ** 2 for row in active))
    normalized = weighted_sum / sigma if sigma else 0.0

    controls = []
    values = [row["weighted_channel_score"] for row in active]
    for idx, signs in enumerate(itertools.product([-1, 1], repeat=len(values))):
        s = sum(sign * value for sign, value in zip(signs, values, strict=True))
        norm = s / sigma if sigma else 0.0
        controls.append(
            {
                "scheme_id": scheme_id,
                "control_id": f"{scheme_id}_exact_sign_flip_{idx:03d}",
                "control_family": "exact_sign_flip_active_channels",
                "seed": "deterministic_complete_enumeration",
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= normalized).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    rng = random.Random(SEED + sum(ord(ch) for ch in scheme_id))
    weights = [row["w_i"] for row in active]
    scores = [row["bounded_channel_score"] for row in active]
    for idx in range(1000):
        shuffled = weights[:]
        rng.shuffle(shuffled)
        s = sum(weight * score for weight, score in zip(shuffled, scores, strict=True))
        sh_sigma = math.sqrt(sum(weight * weight for weight in shuffled))
        norm = s / sh_sigma if sh_sigma else 0.0
        controls.append(
            {
                "scheme_id": scheme_id,
                "control_id": f"{scheme_id}_weight_shuffle_{idx:04d}",
                "control_family": "seeded_weight_shuffle",
                "seed": str(SEED),
                "control_score": f"{norm:.9f}",
                "beats_observed": str(norm >= normalized).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    p_sign = sum(
        1
        for row in controls
        if row["control_family"] == "exact_sign_flip_active_channels"
        and row["beats_observed"] == "true"
    ) / (2 ** len(active))
    p_all = sum(1 for row in controls if row["beats_observed"] == "true") / len(controls)
    min_weight = min(row["w_i"] for row in active)
    max_weight = max(row["w_i"] for row in active)
    summary = {
        "scheme_id": scheme_id,
        "active_channels": str(len(active)),
        "active_channel_order": ";".join(row["channel_id"] for row in active),
        "weighted_sum": f"{weighted_sum:.9f}",
        "normalized_score": f"{normalized:.9f}",
        "min_active_weight": f"{min_weight:.9f}",
        "max_active_weight": f"{max_weight:.9f}",
        "exact_sign_flip_one_sided_p_ge_observed": f"{p_sign:.9f}",
        "combined_control_one_sided_p_ge_observed": f"{p_all:.9f}",
        "positive_score": str(weighted_sum > 0.0).lower(),
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    details = []
    for row in active:
        details.append(
            {
                "scheme_id": scheme_id,
                "channel_id": row["channel_id"],
                "bounded_channel_score": f"{row['bounded_channel_score']:.9f}",
                "Q_i": f"{row['Q_i']:.9f}",
                "w_i": f"{row['w_i']:.9f}",
                "weighted_channel_score": f"{row['weighted_channel_score']:.9f}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return summary, controls + details


def main() -> None:
    score_rows = {row["channel_id"]: row for row in read_rows(INPUT)}
    bounded_scores = {channel: float(row["bounded_channel_score"]) for channel, row in score_rows.items()}
    bounded_scores["act_kpath_lensing_path"] = 0.0

    summaries = []
    all_controls = []
    detail_rows = []

    for scheme_id, exponents in SCHEMES.items():
        q_by_channel = {
            row["channel_id"]: geometric_quality(row, exponents)
            for row in GATE_ROWS
        }
        summary, rows = score_scheme(scheme_id, q_by_channel, bounded_scores)
        summaries.append(summary)
        for row in rows:
            if "control_id" in row:
                all_controls.append(row)
            else:
                detail_rows.append(row)

    q_by_channel = {row["channel_id"]: min_gate_quality(row) for row in GATE_ROWS}
    summary, rows = score_scheme("conservative_min_gate", q_by_channel, bounded_scores)
    summaries.append(summary)
    for row in rows:
        if "control_id" in row:
            all_controls.append(row)
        else:
            detail_rows.append(row)

    positive_count = sum(1 for row in summaries if row["positive_score"] == "true")
    max_p_sign = max(float(row["exact_sign_flip_one_sided_p_ge_observed"]) for row in summaries)
    min_norm = min(float(row["normalized_score"]) for row in summaries)
    verdict = (
        "BEST_JUSTIFIED_KERNEL_ROBUST_POSITIVE_PREFLIGHT_NOT_VALIDATION"
        if positive_count == len(summaries)
        else "BEST_JUSTIFIED_KERNEL_ROBUSTNESS_MIXED_PREFLIGHT_NOT_VALIDATION"
    )
    aggregate = {
        "robustness_id": "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1",
        "schemes_tested": str(len(summaries)),
        "positive_scheme_count": str(positive_count),
        "min_normalized_score": f"{min_norm:.9f}",
        "max_exact_sign_flip_p": f"{max_p_sign:.9f}",
        "verdict": verdict,
        "joint_likelihood_claimed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, detail_rows)
    write_csv(CONTROLS, all_controls)
    write_csv(SUMMARY, summaries + [aggregate])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint best-justified kernel robustness v1",
                "",
                "**Doc class:** source-side weighting robustness preflight",
                "**Status:** not a joint likelihood; not validation",
                "",
                "The audit stress-tests the source-side support rule for the same",
                "positive-support channel set. It changes the residual-blind gate",
                "exponents, not the endpoint scores or channel labels.",
                "",
                f"- schemes tested: `{aggregate['schemes_tested']}`",
                f"- positive schemes: `{aggregate['positive_scheme_count']}`",
                f"- minimum normalized score: `{aggregate['min_normalized_score']}`",
                f"- maximum exact sign-flip p-value: `{aggregate['max_exact_sign_flip_p']}`",
                f"- verdict: `{aggregate['verdict']}`",
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
        "JOINT_BEST_JUSTIFIED_KERNEL_ROBUSTNESS_V1_RUN "
        f"positive={positive_count}/{len(summaries)} "
        f"min_norm={aggregate['min_normalized_score']} "
        f"verdict={verdict}"
    )


if __name__ == "__main__":
    main()
