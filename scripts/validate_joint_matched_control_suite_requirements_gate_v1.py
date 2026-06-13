#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
POLICY = ROOT / "data/source_manifest/joint_matched_control_suite_requirements_policy_v1.csv"
DOC = ROOT / "docs/joint_matched_control_suite_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_suite_requirements_gate_not_scoring_not_validation"
EXPECTED_VERDICT = "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_FROZEN_IMPLEMENTATION_BLOCKED"
EXPECTED_CONTROL_IDS = [
    "JMC_REQ_01_SHUFFLED_CHANNEL",
    "JMC_REQ_02_WRONG_CHANNEL",
    "JMC_REQ_03_SIGN_FLIP",
    "JMC_REQ_04_BLOCK_DROP",
    "JMC_REQ_05_NULL_READOUT",
    "JMC_REQ_06_SCOPE_AND_LEAKAGE",
    "JMC_REQ_07_SHARED_STATISTIC_BINDING",
    "JMC_REQ_08_COVARIANCE_BINDING",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    rows = read_rows(OUT)
    policy = read_rows(POLICY)
    summary = read_one(SUMMARY)
    if rows != policy:
        raise SystemExit("policy and derived gate rows must match")
    if [row["control_id"] for row in rows] != EXPECTED_CONTROL_IDS:
        raise SystemExit("unexpected control row order")
    if len(rows) != 8:
        raise SystemExit("matched control gate must contain eight rows")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['control_id']}")
        if row["status"] not in {"specified_not_implemented", "blocked"}:
            raise SystemExit(f"unexpected status for {row['control_id']}: {row['status']}")
        if not row["implementation_blocker"]:
            raise SystemExit(f"missing implementation blocker for {row['control_id']}")
        for flag in [
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
        ]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['control_id']}")
    for control_id in ["JMC_REQ_07_SHARED_STATISTIC_BINDING", "JMC_REQ_08_COVARIANCE_BINDING"]:
        row = next(row for row in rows if row["control_id"] == control_id)
        if row["status"] != "blocked":
            raise SystemExit(f"{control_id} must remain blocked")
    if summary["verdict"] != EXPECTED_VERDICT:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if summary["required_control_families"] != "8":
        raise SystemExit("expected eight required control families")
    if summary["specified_control_families"] != "8":
        raise SystemExit("all control families should be specified")
    if summary["implemented_control_families"] != "0":
        raise SystemExit("no controls should be implemented under the final joint statistic yet")
    if summary["control_suite_defined"] != "true":
        raise SystemExit("control suite requirements should be defined")
    if summary["control_suite_implemented_under_joint_statistic"] != "false":
        raise SystemExit("control suite must not be marked implemented")
    for flag in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    text = DOC.read_text()
    for marker in ["not scoring", "shuffled channel", "block-drop", "covariance binding", EXPECTED_VERDICT]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_MATCHED_CONTROL_SUITE_REQUIREMENTS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']} controls={summary['specified_control_families']}/{summary['required_control_families']}"
    )


if __name__ == "__main__":
    main()
