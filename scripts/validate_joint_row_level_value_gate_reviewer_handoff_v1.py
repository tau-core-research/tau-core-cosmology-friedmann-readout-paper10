#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1.zip.sha256"
SUMMARY = ROOT / "data/derived/joint_row_level_value_gate_reviewer_handoff_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_value_gate_reviewer_handoff_v1.md"
CLAIM_BOUNDARY = "joint_row_level_value_gate_handoff_not_scoring_not_validation"

REQUIRED_FILES = {
    "docs/joint_row_level_value_gate_reviewer_handoff_v1.md",
    "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip",
    "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip.sha256",
    "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv",
    "docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md",
    "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip",
    "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip.sha256",
    "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv",
    "docs/joint_row_level_numeric_lambda_review_package_v1.md",
    "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv",
    "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv",
}


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    summary = read_one(SUMMARY)
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["package_count"] == "2", "expected two inner packages")
    require(summary["included_review_packages"] == "aligned_control_value_authorization;numeric_lambda_candidate", "bad package list")
    require(summary["aligned_control_value_computation_authorized"] == "false", "aligned computation must not be pre-authorized")
    require(summary["numeric_lambda_authorized"] == "false", "numeric lambda must not be pre-authorized")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must be false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must be false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must be false")

    recorded_sha = SHA.read_text().split()[0]
    require(sha256(OUT) == recorded_sha, "handoff zip sha256 mismatch")
    require(recorded_sha == summary["zip_sha256"], "summary sha mismatch")

    with zipfile.ZipFile(OUT) as zf:
        names = set(zf.namelist())
    require(REQUIRED_FILES.issubset(names), "handoff zip missing required files")

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "repository access",
        "aligned-control value authorization",
        "numeric lambda candidate",
        "Forbidden inputs",
        "endpoint scoring or validation",
    ]:
        require(marker in text, f"handoff doc missing marker: {marker}")

    print(f"JOINT_ROW_LEVEL_VALUE_GATE_REVIEWER_HANDOFF_V1_VALIDATED sha256={recorded_sha}")


if __name__ == "__main__":
    main()
