#!/usr/bin/env python3
from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
BINDING = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
OUT = ROOT / "data/derived/joint_control_block_drop_symbolic_v1.csv"
SUMMARY = ROOT / "data/derived/joint_control_block_drop_symbolic_v1_summary.csv"
DOC = ROOT / "docs/joint_control_block_drop_symbolic_v1.md"
CLAIM_BOUNDARY = "joint_control_block_drop_symbolic_not_scoring_not_validation"


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


def expr(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "0"
    return " + ".join(f"{row['q_i']}*z[{row['channel_id']}]" for row in rows)


def main() -> None:
    shell_rows = read_rows(SHELL)
    binding = read_one(BINDING)
    if binding["symbolic_binding_passed"] != "true":
        raise SystemExit("symbolic binding must pass before block-drop controls")
    if binding["numeric_executable_binding_passed"] != "false":
        raise SystemExit("block-drop symbolic controls must not run after numeric promotion")
    channel_ids = [row["channel_id"] for row in shell_rows]
    if len(channel_ids) != 3:
        raise SystemExit("expected exactly three active channels")

    rows: list[dict[str, str]] = []
    for size in range(1, len(channel_ids) + 1):
        for dropped_tuple in combinations(channel_ids, size):
            dropped = set(dropped_tuple)
            kept_rows = [row for row in shell_rows if row["channel_id"] not in dropped]
            rows.append(
                {
                    "control_id": f"JCBD_{len(rows)+1:02d}",
                    "control_family": "leave_one_probe_or_block_drop",
                    "active_channel_order": ";".join(channel_ids),
                    "dropped_channels": ";".join(dropped_tuple),
                    "kept_channels": ";".join(row["channel_id"] for row in kept_rows) or "none",
                    "drop_count": str(size),
                    "kept_count": str(len(kept_rows)),
                    "symbolic_control_statistic": f"T_joint_block_drop = {expr(kept_rows)}",
                    "same_rows_required": "true",
                    "same_covariance_required": "true",
                    "same_weights_required": "true",
                    "complete_nontrivial_enumeration": "true",
                    "computes_numeric_statistic_now": "false",
                    "endpoint_scoring_allowed": "false",
                    "endpoint_validation_claimed": "false",
                    "cosmological_validation_claimed": "false",
                    "physical_validation_claimed": "false",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(OUT, rows)
    summary = {
        "control_id": "JOINT_CONTROL_BLOCK_DROP_SYMBOLIC_V1",
        "control_family": "leave_one_probe_or_block_drop",
        "active_channel_count": str(len(channel_ids)),
        "control_count": str(len(rows)),
        "expected_nontrivial_block_drops": str(2 ** len(channel_ids) - 1),
        "leave_one_controls": str(sum(1 for row in rows if row["drop_count"] == "1")),
        "all_but_one_controls": str(sum(1 for row in rows if row["kept_count"] == "1")),
        "all_drop_null_control_included": str(any(row["kept_count"] == "0" for row in rows)).lower(),
        "complete_nontrivial_enumeration": str(len(rows) == 2 ** len(channel_ids) - 1).lower(),
        "symbolic_binding_passed": binding["symbolic_binding_passed"],
        "numeric_executable_binding_passed": "false",
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "bind_numeric_T_joint_and_covariance_before_using_block_drops_as_scoring_controls",
        "verdict": "BLOCK_DROP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint symbolic block-drop controls v1",
                "",
                "**Doc class:** matched-control symbolic artifact",
                "**Status:** complete symbolic enumeration; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact enumerates every nontrivial block-drop control for the",
                "three active channels under the shared symbolic statistic",
                "`T_joint = sum_i q_i z_i`. It includes leave-one, all-but-one, and",
                "all-drop/null controls. It does not compute a numeric statistic.",
                "",
                "Summary:",
                "",
                f"- active channels: `{';'.join(channel_ids)}`",
                f"- controls enumerated: `{summary['control_count']}`",
                f"- leave-one controls: `{summary['leave_one_controls']}`",
                f"- all-but-one controls: `{summary['all_but_one_controls']}`",
                f"- all-drop/null control included: `{summary['all_drop_null_control_included']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_CONTROL_BLOCK_DROP_SYMBOLIC_V1_BUILT "
        f"controls={summary['control_count']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
