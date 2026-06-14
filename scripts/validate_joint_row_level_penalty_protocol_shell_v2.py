#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v2.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v2_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_protocol_shell_v2.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_protocol_shell_v2_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 4, "expected four protocol requirements")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["source_feature_inputs_complete"] == "true", "source-feature inputs should be complete")
    require(summary["channel_local_normalization_frozen"] == "true", "normalization should be frozen")
    require(summary["candidate_control_symmetric_transform_built"] == "true", "transform should be built")
    require(summary["penalty_formula_defined"] == "false", "penalty formula must remain undefined")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must be false")
    require(summary["verdict"] == "NORMALIZED_SYMMETRIC_TRANSFORM_READY_COVARIANCE_BINDING_STILL_OPEN", "unexpected verdict")

    statuses = {row["requirement_id"]: row["status"] for row in rows}
    require(statuses["RLP_R1_SOURCE_FEATURE_INPUTS"] == "SATISFIED", "source-feature input gate should be satisfied")
    require(statuses["RLP_R2_CHANNEL_LOCAL_NORMALIZATION"] == "SATISFIED", "normalization should be satisfied")
    require(statuses["RLP_R3_CONTROL_SYMMETRY"] == "SATISFIED", "transform should be satisfied")
    require(statuses["RLP_R4_COVARIANCE_OR_BLOCK_WEIGHT_BINDING"] == "OPEN_REQUIRED", "covariance binding should remain open")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row endpoint validation must remain false")
        require("do_not" in row["forbidden_action"], "forbidden action must be explicit")

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "normalized symmetric transform ready", "does not permit `T_joint`"]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V2_VALIDATED "
        f"open={summary['requirements_open']}"
    )


if __name__ == "__main__":
    main()
