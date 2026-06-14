#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TJOINT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv"
SCORES = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.csv"
SUITE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_closest_shuffle_decomposition_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_closest_shuffle_decomposition_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_closest_shuffle_decomposition_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_closest_shuffle_decomposition_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_channel_z_values(value: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for item in value.split(";"):
        channel, raw = item.split(":", 1)
        out[channel] = float(raw)
    return out


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    ledger = read_rows(TJOINT)
    scores = read_rows(SCORES)
    suite = read_rows(SUITE)

    candidate_q = {row["channel_id"]: float(row["q_i"]) for row in ledger}
    candidate_z = {row["channel_id"]: float(row["candidate_z_i"]) for row in ledger}
    candidate_t = sum(candidate_q[ch] * candidate_z[ch] for ch in candidate_q)

    closest = min(
        [row for row in scores if row["control_family"] == "shuffled_channel_labels"],
        key=lambda row: float(row["candidate_minus_control"]),
    )
    control_id = closest["control_id"]
    control_suite_row = next(row for row in suite if row["control_id"] == control_id)
    control_z = parse_channel_z_values(control_suite_row["channel_z_values"])
    control_t = float(control_suite_row["numeric_t_joint_control"])

    source_by_value = {}
    for ch, z in candidate_z.items():
        source_by_value[round(z, 12)] = ch

    rows: list[dict[str, str]] = []
    for ch in candidate_q:
        assigned_z = control_z[ch]
        source_channel = source_by_value.get(round(assigned_z, 12), "unknown")
        candidate_contribution = candidate_q[ch] * candidate_z[ch]
        control_contribution = candidate_q[ch] * assigned_z
        rows.append(
            {
                "diagnostic_id": "JOINT_NUMERIC_T_JOINT_CLOSEST_SHUFFLE_DECOMPOSITION_V1",
                "control_id": control_id,
                "control_family": "shuffled_channel_labels",
                "target_channel": ch,
                "assigned_source_channel": source_channel,
                "q_i": fmt(candidate_q[ch]),
                "candidate_z_i": fmt(candidate_z[ch]),
                "assigned_control_z_i": fmt(assigned_z),
                "candidate_qz_contribution": fmt(candidate_contribution),
                "control_qz_contribution": fmt(control_contribution),
                "candidate_minus_control_contribution": fmt(candidate_contribution - control_contribution),
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    margin = candidate_t - control_t
    weighted_spread = max(candidate_q.values()) - min(candidate_q.values())
    z_spread = max(candidate_z.values()) - min(candidate_z.values())
    summary = {
        "diagnostic_id": "JOINT_NUMERIC_T_JOINT_CLOSEST_SHUFFLE_DECOMPOSITION_V1",
        "closest_control_id": control_id,
        "closest_control_construction": control_suite_row["construction"],
        "candidate_numeric_t_joint": fmt(candidate_t),
        "control_numeric_t_joint": fmt(control_t),
        "candidate_minus_control": fmt(margin),
        "weighted_q_spread": fmt(weighted_spread),
        "candidate_z_spread": fmt(z_spread),
        "absolute_contribution_differences_sum": fmt(sum(abs(float(row["candidate_minus_control_contribution"])) for row in rows)),
        "interpretation": "closest_shuffle_is_near_because_frozen_channel_weights_and_positive_z_values_are_similar",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_csv(OUT, rows)
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint closest-shuffle decomposition v1",
                "",
                "**Doc class:** permission-only diagnostic decomposition.",
                "**Status:** not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"Closest shuffled-channel control: `{control_id}`.",
                f"Construction: `{summary['closest_control_construction']}`.",
                f"Candidate-minus-control margin: `{summary['candidate_minus_control']}`.",
                "",
                "Interpretation: the closest shuffled control is close because the",
                "three frozen positive channel `z_i` values and the three frozen",
                "`q_i` weights are numerically similar. The shuffle therefore",
                "preserves much of the weighted sum even though it violates the",
                "source-declared channel assignment. This is a thin-margin",
                "channel-assignment diagnostic, not validation.",
                "",
            ]
        )
    )
    print(
        "JOINT_NUMERIC_T_JOINT_CLOSEST_SHUFFLE_DECOMPOSITION_V1_BUILT "
        f"control={control_id} margin={summary['candidate_minus_control']}"
    )


if __name__ == "__main__":
    main()
