#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_v1.md"
AUTH = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_prevalidation_not_endpoint_scoring"
VERDICT = "NUMERIC_T_JOINT_CONTROL_SUITE_BUILT_PREVALIDATION_NOT_ENDPOINT_SCORING"
REQUIRED_FAMILIES = {
    "sign_flip",
    "block_drop",
    "shuffled_channel_labels",
    "matched_control_index_aligned",
    "null_readout",
    "scope_and_forbidden_input_guard",
}


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    auth = read_one(AUTH)
    require(DOC.exists(), "missing doc")
    require(auth["control_suite_authorization_allowed"] == "true", "control suite was not authorized")
    require(summary["verdict"] == VERDICT, "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    numeric_rows = [row for row in rows if row["numeric_t_joint_control"] != "not_applicable"]
    require(int(summary["numeric_control_count"]) == len(numeric_rows), "numeric count mismatch")
    require(int(summary["total_rows"]) == len(rows), "total row count mismatch")
    require(float(summary["candidate_numeric_t_joint"]) > 0.0, "candidate T_joint must be positive")
    require(0 <= int(summary["controls_beating_or_equal_candidate"]) <= len(numeric_rows), "bad beat count")
    families = {row["control_family"] for row in rows}
    require(REQUIRED_FAMILIES <= families, f"missing required families: {REQUIRED_FAMILIES - families}")
    counts = Counter(row["control_family"] for row in rows)
    require(counts["sign_flip"] == 7, "expected seven sign-flip controls")
    require(counts["block_drop"] == 7, "expected seven block-drop controls")
    require(counts["shuffled_channel_labels"] == 5, "expected five shuffled-channel controls")
    require(counts["matched_control_index_aligned"] >= 6, "expected at least six matched-index controls")
    require(counts["null_readout"] == 1, "expected one null-readout control")
    require(counts["scope_and_forbidden_input_guard"] == 1, "expected one guard row")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, f"{row['control_id']}: claim boundary mismatch")
        for field in [
            "same_t_joint_formula",
            "same_q_i_weights",
            "same_sign_and_standardization_rule",
            "same_row_scope_boundary",
        ]:
            require(row[field] == "true", f"{row['control_id']}: {field} must be true")
        for field in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['control_id']}: unsafe field {field}")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary unsafe field {field}")
    text = DOC.read_text()
    for marker in ["same-statistic", "not endpoint scoring", VERDICT, CLAIM_BOUNDARY]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_V1_VALIDATED "
        f"controls={summary['numeric_control_count']} beats={summary['controls_beating_or_equal_candidate']}"
    )


if __name__ == "__main__":
    main()
