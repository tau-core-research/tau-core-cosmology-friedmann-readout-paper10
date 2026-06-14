#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "data/derived/joint_numeric_t_joint_authorization_response_v1_summary.csv"
ZI_SUMMARY = ROOT / "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv"
SHELL = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
OUT = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_ledger_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_ledger_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_ledger_not_endpoint_scoring_not_validation"


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


def f(value: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise SystemExit(f"non-numeric value: {value}") from exc


def fmt(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    auth = read_one(AUTH)
    if auth["numeric_t_joint_allowed"] != "true":
        raise SystemExit("numeric T_joint ledger is not authorized")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if auth[field] != "false":
            raise SystemExit(f"unsafe authorization field: {field}")

    zi_rows = [row for row in read_rows(ZI_SUMMARY) if row["channel_id"] != "all_channels"]
    shell_rows = read_rows(SHELL)
    if len(zi_rows) != 3 or len(shell_rows) != 3:
        raise SystemExit("expected exactly three z_i rows and three shell rows")
    shell_by_channel = {row["channel_id"]: row for row in shell_rows}
    if set(shell_by_channel) != {row["channel_id"] for row in zi_rows}:
        raise SystemExit("shell and z_i channels mismatch")

    rows: list[dict[str, str]] = []
    t_joint = 0.0
    for zi in zi_rows:
        channel_id = zi["channel_id"]
        shell = shell_by_channel[channel_id]
        if shell["symbolic_joint_statistic"] != "T_joint = sum_i q_i z_i":
            raise SystemExit(f"{channel_id}: unexpected symbolic joint statistic")
        if shell["computes_numeric_statistic_now"] != "false":
            raise SystemExit(f"{channel_id}: shell must not already compute numeric statistic")
        if zi["numeric_z_i_defined"] != "true":
            raise SystemExit(f"{channel_id}: numeric z_i is not defined")
        q_i = f(shell["q_i"])
        z_i = f(zi["candidate_z_i"])
        contribution = q_i * z_i
        t_joint += contribution
        rows.append(
            {
                "ledger_id": "JOINT_NUMERIC_T_JOINT_LEDGER_V1",
                "channel_order": shell["channel_order"],
                "channel_id": channel_id,
                "q_i": fmt(q_i),
                "candidate_z_i": fmt(z_i),
                "q_i_z_i_contribution": fmt(contribution),
                "channel_caveat": zi["caveat"],
                "source_zi_ledger": "data/derived/joint_numeric_zi_distribution_ledger_v1_summary.csv",
                "symbolic_joint_statistic": shell["symbolic_joint_statistic"],
                "computes_endpoint_score_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "ledger_id": "JOINT_NUMERIC_T_JOINT_LEDGER_V1",
                "channel_count": str(len(rows)),
                "symbolic_joint_statistic": "T_joint = sum_i q_i z_i",
                "numeric_t_joint": fmt(t_joint),
                "numeric_t_joint_allowed": "true",
                "computes_endpoint_score_now": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "caveat": "numeric_joint_ledger_only_not_endpoint_scoring_not_validation",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Joint numeric T_joint ledger v1",
                "",
                "**Doc class:** numeric joint ledger",
                "**Status:** numeric T_joint computed; not endpoint scoring; not validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This artifact combines the already built channel-level `z_i` ledger",
                "under the frozen shell:",
                "",
                "```text",
                "T_joint = sum_i q_i z_i",
                "```",
                "",
                f"Numeric `T_joint`: `{fmt(t_joint)}`.",
                "",
                "This is not an endpoint score and not a cosmological or physical",
                "validation claim.",
                "",
            ]
        )
    )
    print(f"JOINT_NUMERIC_T_JOINT_LEDGER_V1_BUILT T_joint={fmt(t_joint)}")


if __name__ == "__main__":
    main()
