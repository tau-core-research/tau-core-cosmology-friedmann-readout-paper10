#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1.csv"
JOINT_OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_values_joint_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_values_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_values_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_values_not_rescoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


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


def main() -> None:
    rows = read_rows(OUT)
    joint_rows = read_rows(JOINT_OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]

    require(len(rows) == int(summary["channel_penalty_rows"]), "channel row count mismatch")
    require(len(joint_rows) == int(summary["complete_joint_penalty_rows"]), "joint row count mismatch")
    require(summary["penalty_values_computed"] == "true", "summary should mark penalty values computed")
    require(summary["lambda_row_numeric_value_defined"] == "false", "lambda_row numeric value must remain false")
    require(summary["t_joint_rescoring_allowed"] == "false", "T_joint rescoring must remain false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["verdict"] == "NUMERIC_PENALTY_VALUES_COMPUTED_NOT_RESCORING", "unexpected verdict")

    candidate_rows = [row for row in rows if row["row_type"] == "candidate"]
    control_rows = [row for row in rows if row["row_type"] != "candidate"]
    require(len(candidate_rows) == int(summary["candidate_channel_penalty_rows"]), "candidate row count mismatch")
    require(len(control_rows) == int(summary["control_channel_penalty_rows"]), "control row count mismatch")
    require(len(candidate_rows) == 3, "expected one candidate penalty row per active channel")
    require(len(joint_rows) == 1, "expected exactly one complete joint candidate penalty row")

    p_sum = sum(parse_float(row["P_i"], f"P_i {row['channel_id']}") for row in candidate_rows)
    p_joint = parse_float(joint_rows[0]["P_row"], "joint P_row")
    p_summary = parse_float(summary["P_row_candidate"], "summary P_row_candidate")
    require(abs(p_sum - p_joint) < 1e-9, "joint P_row does not match candidate P_i sum")
    require(abs(p_joint - p_summary) < 1e-9, "summary P_row does not match joint row")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_row_numeric_value_defined"] == "false", "row lambda_row must remain false")
        require(row["t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
        require(parse_float(row["P_i"], f"P_i {row['value_id']}") >= 0.0, "P_i must be non-negative")
        if row["row_type"] == "candidate":
            require(row["joint_scope"] == "complete_joint_candidate", "candidate joint scope mismatch")
            require(row["joint_penalty_contribution_allowed"] == "true", "candidate contribution flag mismatch")
        else:
            require(row["joint_scope"] == "channel_local_control_only", "control joint scope mismatch")
            require(row["joint_penalty_contribution_allowed"] == "false", "control contribution flag mismatch")

    joint = joint_rows[0]
    require(joint["joint_penalty_computed"] == "true", "candidate joint penalty should be computed")
    require(joint["control_joint_penalty_computed"] == "false", "control joint penalty must remain false")
    require(joint["lambda_row_numeric_value_defined"] == "false", "joint lambda must remain false")
    require(joint["t_joint_rescoring_allowed"] == "false", "joint rescoring must remain false")
    require(joint["endpoint_validation_claimed"] == "false", "joint validation must remain false")
    require(joint["claim_boundary"] == CLAIM_BOUNDARY, "joint claim boundary mismatch")

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not `T_joint` rescoring", "Controls are kept as channel-local", "P_i(a)"]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUES_V1_VALIDATED "
        f"channel_rows={len(rows)} P_row_candidate={p_joint:.12g}"
    )


if __name__ == "__main__":
    main()
