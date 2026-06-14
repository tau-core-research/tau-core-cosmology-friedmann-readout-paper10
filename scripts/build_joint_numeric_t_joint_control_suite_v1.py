#!/usr/bin/env python3
from __future__ import annotations

import csv
import itertools
import math
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_v1_summary.csv"
ZI = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1.csv"
TJOINT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv"
BLOCKER = ROOT / "data/derived/joint_numeric_t_joint_control_suite_blocker_status_v1_summary.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_prevalidation_not_endpoint_scoring"
SEED = 20260614


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: float) -> str:
    return f"{value:.12e}"


def t_value(q: dict[str, float], z: dict[str, float]) -> float:
    return sum(q[ch] * z[ch] for ch in q)


def control_row(
    control_id: str,
    family: str,
    z: dict[str, float],
    q: dict[str, float],
    candidate_t: float,
    construction: str,
) -> dict[str, str]:
    value = t_value(q, z)
    return {
        "control_suite_id": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_V1",
        "control_id": control_id,
        "control_family": family,
        "construction": construction,
        "channel_z_values": ";".join(f"{ch}:{fmt(z[ch])}" for ch in q),
        "numeric_t_joint_control": fmt(value),
        "candidate_numeric_t_joint": fmt(candidate_t),
        "beats_or_equals_candidate": str(value >= candidate_t).lower(),
        "same_t_joint_formula": "true",
        "same_q_i_weights": "true",
        "same_sign_and_standardization_rule": "true",
        "same_row_scope_boundary": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    auth = read_one(AUTH)
    blocker = read_one(BLOCKER)
    if auth["control_suite_authorization_allowed"] != "true":
        raise SystemExit("numeric control-suite build is not authorized")
    if blocker["current_blocker"] != "control_suite_authorized_numeric_control_build_missing":
        raise SystemExit("control-suite blocker does not authorize build step")
    for field in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        if auth[field] != "false":
            raise SystemExit(f"unsafe authorization field: {field}")

    tjoint_rows = read_rows(TJOINT)
    q = {row["channel_id"]: float(row["q_i"]) for row in tjoint_rows}
    candidate_z = {row["channel_id"]: float(row["candidate_z_i"]) for row in tjoint_rows}
    candidate_t = t_value(q, candidate_z)
    reported_t = sum(float(row["q_i_z_i_contribution"]) for row in tjoint_rows)
    if abs(candidate_t - reported_t) > 1e-10:
        raise SystemExit("candidate T_joint mismatch")

    zi_rows = read_rows(ZI)
    controls_by_channel: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in zi_rows:
        if row["row_type"] == "matched_control":
            controls_by_channel[row["channel_id"]].append(row)
    if set(controls_by_channel) != set(q):
        raise SystemExit("matched controls missing for at least one active channel")
    for rows in controls_by_channel.values():
        rows.sort(key=lambda r: int(r["control_index"]))

    rows: list[dict[str, str]] = []
    channels = list(q)

    # Exact nontrivial sign flips on the frozen candidate z_i vector.
    for idx, signs in enumerate(itertools.product([-1.0, 1.0], repeat=len(channels)), start=1):
        if all(sign == 1.0 for sign in signs):
            continue
        z = {ch: sign * candidate_z[ch] for ch, sign in zip(channels, signs, strict=True)}
        rows.append(control_row(f"sign_flip_{idx:03d}", "sign_flip", z, q, candidate_t, "exact_nontrivial_sign_flip_candidate_z"))

    # Leave-one and all-drop block controls on the frozen candidate vector.
    for idx, mask in enumerate(itertools.product([0, 1], repeat=len(channels)), start=1):
        if all(mask):
            continue
        z = {ch: candidate_z[ch] if keep else 0.0 for ch, keep in zip(channels, mask, strict=True)}
        dropped = [ch for ch, keep in zip(channels, mask, strict=True) if not keep]
        rows.append(control_row(f"block_drop_{idx:03d}", "block_drop", z, q, candidate_t, "drop:" + "|".join(dropped)))

    # Deterministic shuffled-channel labels: same z values, reassigned to channels.
    for idx, perm in enumerate(itertools.permutations(channels), start=1):
        if list(perm) == channels:
            continue
        z = {ch: candidate_z[src] for ch, src in zip(channels, perm, strict=True)}
        rows.append(control_row(f"channel_shuffle_{idx:03d}", "shuffled_channel_labels", z, q, candidate_t, "perm:" + "|".join(perm)))

    # Matched-control aligned rows, limited by the smallest source-native control count.
    min_controls = min(len(v) for v in controls_by_channel.values())
    for idx in range(min_controls):
        z = {ch: float(controls_by_channel[ch][idx]["z_i"]) for ch in channels}
        rows.append(control_row(f"matched_index_{idx+1:03d}", "matched_control_index_aligned", z, q, candidate_t, "same_control_index_across_channels"))

    # Null readout control.
    rows.append(control_row("null_readout_001", "null_readout", {ch: 0.0 for ch in channels}, q, candidate_t, "all_channel_z_set_to_zero"))

    # Scope/forbidden-input ledger row as a nonnumeric guard control.
    guard = {
        "control_suite_id": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_V1",
        "control_id": "scope_forbidden_input_guard_001",
        "control_family": "scope_and_forbidden_input_guard",
        "construction": "all_controls_built_from_frozen_q_i_z_i_and_matched_control_ledgers_only",
        "channel_z_values": "not_applicable_guard_row",
        "numeric_t_joint_control": "not_applicable",
        "candidate_numeric_t_joint": fmt(candidate_t),
        "beats_or_equals_candidate": "false",
        "same_t_joint_formula": "true",
        "same_q_i_weights": "true",
        "same_sign_and_standardization_rule": "true",
        "same_row_scope_boundary": "true",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows.append(guard)

    numeric_rows = [row for row in rows if row["numeric_t_joint_control"] != "not_applicable"]
    beats = sum(row["beats_or_equals_candidate"] == "true" for row in numeric_rows)
    family_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        family_counts[row["control_family"]] += 1
    summary = {
        "control_suite_id": "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_V1",
        "candidate_numeric_t_joint": fmt(candidate_t),
        "numeric_control_count": str(len(numeric_rows)),
        "total_rows": str(len(rows)),
        "control_families": ";".join(f"{k}:{family_counts[k]}" for k in sorted(family_counts)),
        "controls_beating_or_equal_candidate": str(beats),
        "fraction_beating_or_equal_candidate": fmt(beats / len(numeric_rows)),
        "min_matched_control_count": str(min_controls),
        "random_seed": str(SEED),
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "review_numeric_control_suite_then_prepare_separate_endpoint_scoring_authorization_if_allowed",
        "verdict": "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint control suite v1",
                "",
                "**Doc class:** numeric same-statistic control-suite ledger",
                "**Status:** prevalidation; not endpoint scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                f"Candidate `T_joint`: `{summary['candidate_numeric_t_joint']}`.",
                f"Numeric controls: `{summary['numeric_control_count']}`.",
                f"Controls beating/equal candidate: `{summary['controls_beating_or_equal_candidate']}`.",
                f"Control families: `{summary['control_families']}`.",
                f"Verdict: `{summary['verdict']}`.",
                "",
                "Every numeric control uses the same frozen formula",
                "`T_joint = sum_i q_i z_i`, the same `q_i` weights, and the",
                "same source-frozen channel standardization ledger. This artifact",
                "does not authorize endpoint scoring or validation claims.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_V1_BUILT "
        f"controls={summary['numeric_control_count']} beats={summary['controls_beating_or_equal_candidate']}"
    )


if __name__ == "__main__":
    main()
