#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1.zip.sha256"
SUMMARY = ROOT / "data/derived/joint_row_level_open_blocker_reviewer_handoff_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_open_blocker_reviewer_handoff_v1.md"

REQUIRED_MEMBERS = {
    "docs/joint_row_level_open_blocker_reviewer_handoff_v1.md",
    "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip",
    "data/derived/joint_row_level_cross_channel_control_alignment_review_package_v1.zip.sha256",
    "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv",
    "docs/joint_row_level_cross_channel_control_alignment_blocker_status_v1.md",
    "data/derived/joint_row_level_lambda_policy_review_package_v1.zip",
    "data/derived/joint_row_level_lambda_policy_review_package_v1.zip.sha256",
    "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv",
    "docs/joint_row_level_lambda_policy_blocker_status_v1.md",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(OUT.exists(), "handoff zip missing")
    require(SHA.exists(), "handoff sha missing")
    require(DOC.exists(), "handoff doc missing")
    rows = read_rows(SUMMARY)
    require(len(rows) == 1, "summary must contain one row")
    summary = rows[0]
    digest = sha256(OUT)
    require(summary["zip_sha256"] == digest, "summary sha mismatch")
    require(SHA.read_text().split()[0] == digest, "sha file mismatch")
    require(summary["endpoint_scoring_allowed"] == "false", "scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(summary["numeric_lambda_authorized"] == "false", "numeric lambda must remain false")
    require(summary["aligned_control_values_authorized"] == "false", "aligned values must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    with zipfile.ZipFile(OUT) as zf:
        members = set(zf.namelist())
    require(REQUIRED_MEMBERS.issubset(members), f"missing zip members: {sorted(REQUIRED_MEMBERS - members)}")
    text = DOC.read_text()
    for marker in ["No endpoint residuals", "No endpoint scores", "No endpoint validation claim"]:
        require(marker in text, f"handoff doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_OPEN_BLOCKER_REVIEWER_HANDOFF_V1_VALIDATED sha256={digest}")


if __name__ == "__main__":
    main()
