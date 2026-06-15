#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_aligned_control_values_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_values_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_values_v1.md"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_values_not_rescoring_not_validation"


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
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["aligned_control_values_computed"] == "true", "aligned values should be computed")
    require(summary["verdict"] == "ALIGNED_CONTROL_VALUES_COMPUTED_NOT_RESCORING", "unexpected verdict")
    require(summary["lambda_row_numeric_value_defined"] == "false", "lambda must remain false")
    require(summary["t_joint_rescoring_allowed"] == "false", "rescoring must remain false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(len(rows) == int(summary["aligned_control_rows"]), "aligned row count mismatch")
    require(len(rows) == 6, "expected six aligned controls from min-count rule")
    p_values = []
    for expected_idx, row in enumerate(rows, start=1):
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["alignment_index"] == str(expected_idx), "alignment index mismatch")
        require(row["channels_present_count"] == "3", "expected three channels per aligned row")
        require(row["lambda_row_numeric_value_defined"] == "false", "row lambda must remain false")
        require(row["t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
        require(row["endpoint_scoring_allowed"] == "false", "row endpoint scoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
        p_value = parse_float(row["P_row_control"], f"P_row_control {row['aligned_value_id']}")
        require(p_value >= 0.0, "P_row_control must be non-negative")
        p_values.append(p_value)
    require(abs(min(p_values) - parse_float(summary["P_row_control_min"], "summary min")) < 1e-9, "min mismatch")
    require(abs(max(p_values) - parse_float(summary["P_row_control_max"], "summary max")) < 1e-9, "max mismatch")
    require(abs((sum(p_values) / len(p_values)) - parse_float(summary["P_row_control_mean"], "summary mean")) < 1e-9, "mean mismatch")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not `T_joint` rescoring", "deterministic residual-blind", "aligned rows"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUES_V1_VALIDATED rows={len(rows)}")


if __name__ == "__main__":
    main()
