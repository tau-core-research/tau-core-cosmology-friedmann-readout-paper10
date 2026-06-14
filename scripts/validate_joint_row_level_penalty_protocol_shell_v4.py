#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_protocol_shell_v4.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_protocol_shell_v4_not_scoring_not_validation"


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
    require(len(rows) == 6, "expected six protocol requirements")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["source_feature_inputs_complete"] == "true", "source-feature inputs should be complete")
    require(summary["channel_local_normalization_frozen"] == "true", "normalization should be frozen")
    require(summary["candidate_control_symmetric_transform_built"] == "true", "transform should be built")
    require(summary["covariance_or_block_weight_binding_frozen"] == "true", "binding should be frozen")
    require(summary["symbolic_penalty_formula_defined"] == "true", "symbolic formula should be defined")
    require(summary["penalty_formula_defined"] == "true", "penalty formula should be defined symbolically")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["lambda_row_numeric_value_defined"] == "false", "lambda_row numeric value must not be defined")
    require(summary["numeric_penalty_values_written"] == "false", "numeric penalty values must not be written")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must be false")
    require(
        summary["verdict"] == "SYMBOLIC_ROW_LEVEL_PENALTY_READY_NUMERIC_AUTHORIZATION_STILL_OPEN",
        "unexpected verdict",
    )

    statuses = {row["requirement_id"]: row["status"] for row in rows}
    for requirement in [
        "RLP_R1_SOURCE_FEATURE_INPUTS",
        "RLP_R2_CHANNEL_LOCAL_NORMALIZATION",
        "RLP_R3_CONTROL_SYMMETRY",
        "RLP_R4_COVARIANCE_OR_BLOCK_WEIGHT_BINDING",
        "RLP_R5_SYMBOLIC_PENALTY_FORMULA",
    ]:
        require(statuses[requirement] == "SATISFIED", f"{requirement} should be satisfied")
    require(
        statuses["RLP_R6_NUMERIC_PENALTY_COMPUTATION_AUTHORIZATION"] == "OPEN_REQUIRED",
        "numeric computation authorization must remain open",
    )

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row endpoint validation must remain false")
        require("do_not" in row["forbidden_action"], "forbidden action must be explicit")

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "symbolic row-level penalty ready",
        "does not compute",
        "Open gate",
    ]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_ROW_LEVEL_PENALTY_PROTOCOL_SHELL_V4_VALIDATED "
        f"open={summary['requirements_open']}"
    )


if __name__ == "__main__":
    main()
