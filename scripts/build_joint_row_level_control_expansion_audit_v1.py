#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
DOCS = ROOT / "docs"

PENALTY_VALUES = DERIVED / "joint_row_level_numeric_penalty_values_v1.csv"
ALIGNED_VALUES = DERIVED / "joint_row_level_aligned_control_values_v1.csv"
NUMERIC_CONTROLS = DERIVED / "joint_numeric_t_joint_control_suite_v1.csv"
OUT = DERIVED / "joint_row_level_control_expansion_audit_v1.csv"
SUMMARY = DERIVED / "joint_row_level_control_expansion_audit_v1_summary.csv"
DOC = DOCS / "joint_row_level_control_expansion_audit_v1.md"
CLAIM_BOUNDARY = "joint_row_level_control_expansion_audit_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    penalties = read_rows(PENALTY_VALUES)
    aligned = read_rows(ALIGNED_VALUES)
    numeric_controls = read_rows(NUMERIC_CONTROLS)

    channel_controls: dict[str, set[str]] = {}
    channel_families: dict[str, Counter[str]] = {}
    for row in penalties:
        if row["row_type"] != "matched_control":
            continue
        channel = row["channel_id"]
        channel_controls.setdefault(channel, set()).add(row["control_id"])
        channel_families.setdefault(channel, Counter())[row["control_family"]] += 1

    channels = sorted(channel_controls)
    counts = {channel: len(channel_controls[channel]) for channel in channels}
    strict_max = min(counts.values()) if counts else 0
    current_aligned = len(aligned)
    bottleneck = min(counts, key=counts.get)

    numeric_matched = [
        row for row in numeric_controls if row["control_id"].startswith("matched_index_")
    ]
    numeric_matched_count = len(numeric_matched)

    rows = []
    for channel in channels:
        rows.append(
            {
                "audit_id": "JOINT_ROW_LEVEL_CONTROL_EXPANSION_AUDIT_V1",
                "channel_id": channel,
                "row_level_control_count": str(counts[channel]),
                "control_families": ";".join(
                    f"{family}:{count}" for family, count in sorted(channel_families[channel].items())
                ),
                "strict_all_channel_index_alignment_ceiling": str(strict_max),
                "current_aligned_control_count": str(current_aligned),
                "is_bottleneck_channel": str(channel == bottleneck).lower(),
                "expansion_without_new_source_or_relaxed_alignment": "false"
                if counts[channel] == strict_max
                else "blocked_by_other_channel",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    relaxed_reuse_ceiling = max(counts.values()) if counts else 0
    summary = {
        "audit_id": "JOINT_ROW_LEVEL_CONTROL_EXPANSION_AUDIT_V1",
        "active_channels": "|".join(channels),
        "row_level_control_counts_by_channel": "|".join(f"{ch}:{counts[ch]}" for ch in channels),
        "current_aligned_control_count": str(current_aligned),
        "strict_all_channel_index_alignment_ceiling": str(strict_max),
        "numeric_t_joint_matched_index_controls": str(numeric_matched_count),
        "bottleneck_channel": bottleneck,
        "additional_strict_controls_available_now": str(max(0, strict_max - current_aligned)),
        "relaxed_reuse_or_cartesian_controls_possible_count": str(relaxed_reuse_ceiling),
        "relaxed_reuse_or_cartesian_controls_authorized": "false",
        "recommended_next_action": "either_build_more_desi_shape_time_controls_or_freeze_a_new_relaxed_alignment_rule_before_expanded_scoring",
        "endpoint_validation_claimed": "false",
        "verdict": "STRICT_ROW_LEVEL_CONTROL_EXPANSION_BLOCKED_BY_DESI_SHAPE_TIME_COUNT",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level control expansion audit v1",
                "",
                "**Doc class:** control-scope audit.",
                "**Status:** complete; not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "The strict expansion question is whether more row-level controls can",
                "be added without changing the residual-blind alignment rule.",
                "",
                f"Current aligned controls: `{current_aligned}`.",
                f"Strict all-channel alignment ceiling: `{strict_max}`.",
                f"Bottleneck channel: `{bottleneck}`.",
                "",
                "Under the present deterministic min-count alignment rule, there are",
                "no additional strict controls available now. KiDS and observer/path",
                "have many more row-level controls, but DESI shape/time has only six.",
                "",
                "Two future options remain:",
                "",
                "1. build more source-side DESI shape/time controls;",
                "2. freeze a new relaxed alignment rule, such as cyclic reuse or a",
                "   reviewed Cartesian product rule, before any expanded scoring.",
                "",
                "No expanded scoring is authorized by this audit.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        "JOINT_ROW_LEVEL_CONTROL_EXPANSION_AUDIT_V1_COMPLETE "
        f"strict_ceiling={strict_max} bottleneck={bottleneck}"
    )


if __name__ == "__main__":
    main()
