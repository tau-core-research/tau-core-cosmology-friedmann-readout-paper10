#!/usr/bin/env python3
from __future__ import annotations

import csv
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
BINDING = ROOT / "data/derived/joint_symbolic_statistic_binding_status_v1_summary.csv"
OUT = ROOT / "data/derived/joint_control_sign_flip_symbolic_v1.csv"
SUMMARY = ROOT / "data/derived/joint_control_sign_flip_symbolic_v1_summary.csv"
DOC = ROOT / "docs/joint_control_sign_flip_symbolic_v1.md"
CLAIM_BOUNDARY = "joint_control_sign_flip_symbolic_not_scoring_not_validation"


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


def term(sign: int, q: str, channel_id: str) -> str:
    prefix = "+" if sign > 0 else "-"
    return f"{prefix}{q}*z[{channel_id}]"


def main() -> None:
    shell_rows = read_rows(SHELL)
    binding = read_one(BINDING)
    if binding["symbolic_binding_passed"] != "true":
        raise SystemExit("symbolic same-statistic binding must pass before sign-flip controls")
    if binding["numeric_executable_binding_passed"] != "false":
        raise SystemExit("this symbolic control must not run after numeric validation binding is promoted")
    channel_ids = [row["channel_id"] for row in shell_rows]
    if len(channel_ids) != 3:
        raise SystemExit("expected exactly three active channels")

    rows: list[dict[str, str]] = []
    for index, signs in enumerate(product([-1, 1], repeat=len(shell_rows)), start=1):
        if all(sign == 1 for sign in signs):
            continue
        flipped = [channel_ids[i] for i, sign in enumerate(signs) if sign == -1]
        expression = " ".join(term(sign, shell_rows[i]["q_i"], channel_ids[i]) for i, sign in enumerate(signs))
        rows.append(
            {
                "control_id": f"JCSF_{len(rows)+1:02d}",
                "control_family": "sign_flip_controls",
                "active_channel_order": ";".join(channel_ids),
                "flipped_channels": ";".join(flipped),
                "sign_vector": ";".join(str(sign) for sign in signs),
                "symbolic_control_statistic": f"T_joint_sign_flip = {expression}",
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
        "control_id": "JOINT_CONTROL_SIGN_FLIP_SYMBOLIC_V1",
        "control_family": "sign_flip_controls",
        "active_channel_count": str(len(channel_ids)),
        "control_count": str(len(rows)),
        "expected_nontrivial_sign_flips": str(2 ** len(channel_ids) - 1),
        "complete_nontrivial_enumeration": str(len(rows) == 2 ** len(channel_ids) - 1).lower(),
        "symbolic_binding_passed": binding["symbolic_binding_passed"],
        "numeric_executable_binding_passed": "false",
        "computes_numeric_statistic_now": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "bind_numeric_T_joint_and_covariance_before_using_sign_flips_as_scoring_controls",
        "verdict": "SIGN_FLIP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint symbolic sign-flip controls v1",
                "",
                "**Doc class:** matched-control symbolic artifact",
                "**Status:** complete symbolic enumeration; not scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact enumerates every nontrivial sign-flip control for the",
                "three active channels under the shared symbolic statistic",
                "`T_joint = sum_i q_i z_i`. It does not compute a numeric statistic.",
                "",
                "Summary:",
                "",
                f"- active channels: `{';'.join(channel_ids)}`",
                f"- controls enumerated: `{summary['control_count']}`",
                f"- complete enumeration: `{summary['complete_nontrivial_enumeration']}`",
                f"- numeric executable binding passed: `{summary['numeric_executable_binding_passed']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_CONTROL_SIGN_FLIP_SYMBOLIC_V1_BUILT "
        f"controls={summary['control_count']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
