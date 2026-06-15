#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTH_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_v1_summary.csv"
BLOCKER_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1_summary.csv"
VALUES = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1.csv"
ALIGN_DIAG = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_diagnostic_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_aligned_control_values_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_values_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_values_v1.md"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_values_not_rescoring_not_validation"


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
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def parse_float(value: str, context: str) -> float:
    try:
        result = float(value)
    except ValueError as exc:
        raise SystemExit(f"non-numeric {context}: {value!r}") from exc
    if not math.isfinite(result):
        raise SystemExit(f"non-finite {context}: {value!r}")
    return result


def check_authorization() -> tuple[dict[str, str], dict[str, str]]:
    auth = read_one(AUTH_SUMMARY)
    blocker = read_one(BLOCKER_SUMMARY)
    require(
        auth["decision"] == "AUTHORIZE_ALIGNED_CONTROL_VALUE_COMPUTATION_ONLY_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION",
        f"unexpected aligned-control authorization decision: {auth['decision']}",
    )
    require(auth["aligned_control_value_computation_authorized"] == "true", "aligned-control computation not authorized")
    require(auth["aligned_joint_control_values_authorized"] == "false", "pre-existing aligned values authorization must remain false")
    require(auth["lambda_row_numeric_value_authorized"] == "false", "lambda_row must remain unauthorized")
    require(auth["t_joint_rescoring_authorized"] == "false", "T_joint rescoring must remain unauthorized")
    require(auth["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain forbidden")
    require(auth["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(
        blocker["verdict"] == "ALIGNED_CONTROL_VALUE_COMPUTATION_AUTHORIZED_VALUES_STILL_UNCOMPUTED",
        f"unexpected aligned-control blocker verdict: {blocker['verdict']}",
    )
    return auth, blocker


def main() -> None:
    auth, blocker = check_authorization()
    diag = read_one(ALIGN_DIAG)
    require(
        diag["proposed_alignment_rule"]
        == "deterministic_min_count_index_alignment_after_sort_by_control_family_then_control_id",
        "unexpected alignment rule",
    )
    active_channels = diag["active_channels"].split("|")
    min_count = int(diag["min_index_aligned_count_if_accepted"])
    require(min_count > 0, "min aligned count must be positive")

    values = read_rows(VALUES)
    by_channel: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in values:
        require(row["lambda_row_numeric_value_defined"] == "false", "input lambda flag must remain false")
        require(row["t_joint_rescoring_allowed"] == "false", "input rescoring flag must remain false")
        require(row["endpoint_validation_claimed"] == "false", "input validation flag must remain false")
        if row["row_type"] != "candidate":
            by_channel[row["channel_id"]].append(row)

    require(sorted(by_channel) == sorted(active_channels), f"control channels mismatch: {sorted(by_channel)} vs {active_channels}")
    for channel in active_channels:
        by_channel[channel].sort(key=lambda r: (r["control_family"], r["control_id"]))
        require(len(by_channel[channel]) >= min_count, f"not enough controls for channel {channel}")

    out_rows: list[dict[str, str]] = []
    for idx in range(min_count):
        channel_rows = [by_channel[channel][idx] for channel in active_channels]
        p_row = sum(parse_float(row["P_i"], f"P_i {row['channel_id']} aligned index {idx}") for row in channel_rows)
        out_rows.append(
            {
                "aligned_value_id": f"JRLACV1_{idx + 1:03d}",
                "alignment_index": str(idx + 1),
                "alignment_rule": diag["proposed_alignment_rule"],
                "channels_present": "|".join(active_channels),
                "channels_present_count": str(len(active_channels)),
                "control_ids_by_channel": "|".join(f"{row['channel_id']}:{row['control_id']}" for row in channel_rows),
                "control_families_by_channel": "|".join(f"{row['channel_id']}:{row['control_family']}" for row in channel_rows),
                "P_i_by_channel": "|".join(f"{row['channel_id']}:{row['P_i']}" for row in channel_rows),
                "P_row_control": f"{p_row:.12g}",
                "lambda_row_numeric_value_defined": "false",
                "t_joint_rescoring_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(OUT, out_rows)
    p_values = [parse_float(row["P_row_control"], f"P_row_control {row['aligned_value_id']}") for row in out_rows]
    summary = {
        "artifact_id": "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUES_V1",
        "authorization_response": str(AUTH_SUMMARY.relative_to(ROOT)),
        "authorization_decision": auth["decision"],
        "blocker_verdict": blocker["verdict"],
        "source_values": str(VALUES.relative_to(ROOT)),
        "alignment_rule": diag["proposed_alignment_rule"],
        "active_channels": "|".join(active_channels),
        "aligned_control_rows": str(len(out_rows)),
        "P_row_control_min": f"{min(p_values):.12g}",
        "P_row_control_max": f"{max(p_values):.12g}",
        "P_row_control_mean": f"{sum(p_values) / len(p_values):.12g}",
        "lambda_row_numeric_value_defined": "false",
        "t_joint_rescoring_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "aligned_control_values_computed": "true",
        "verdict": "ALIGNED_CONTROL_VALUES_COMPUTED_NOT_RESCORING",
        "next_required_action": "review_aligned_control_values_before_any_T_joint_rescoring",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level aligned control values v1",
                "",
                "**Doc class:** guarded numeric value artifact.",
                "**Status:** aligned control values only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact is produced only after a completed reviewer response",
                "authorizes a value-computation-only aligned-control step. It applies",
                "the deterministic residual-blind min-count alignment rule to the",
                "already frozen channel-local penalty values.",
                "",
                "It does not choose `lambda_row`, does not rescore `T_joint`, and does",
                "not perform endpoint scoring or validation.",
                "",
                f"- aligned rows: `{summary['aligned_control_rows']}`",
                f"- active channels: `{summary['active_channels']}`",
                f"- mean aligned control `P_row`: `{summary['P_row_control_mean']}`",
                "",
            ]
        )
    )
    print(
        "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUES_V1_BUILT "
        f"rows={summary['aligned_control_rows']} mean={summary['P_row_control_mean']}"
    )


if __name__ == "__main__":
    main()
