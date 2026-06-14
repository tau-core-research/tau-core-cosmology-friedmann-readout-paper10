#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_package_v1.md"
INSTRUCTIONS = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_reviewer_instructions_v1.md"
EXTERNAL_MESSAGE = ROOT / "docs/joint_numeric_t_joint_control_suite_authorization_external_reviewer_message_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_control_suite_authorization_not_scoring_not_validation"


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        require(row[field] == "false", f"{label}: {field} must be false")


def main() -> None:
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    template = read_rows(TEMPLATE)
    require(PACKAGE.exists(), "missing package zip")
    require(SHA.exists(), "missing sha sidecar")
    require(summary["status"] == "JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED", "bad package status")
    require(summary["zip_sha256"] == sha256(PACKAGE), "zip checksum mismatch")
    require(SHA.read_text().split()[0] == summary["zip_sha256"], "sha sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package cannot be pre-completed")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require_false(
        summary,
        [
            "control_suite_authorization_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
            "contains_endpoint_scores",
            "contains_fit_statistics",
        ],
        "summary",
    )
    require(len(template) == 4, "template must contain four rows")
    for row in template:
        require(row["review_completed"] == "false", "template must be blank")
        require(row["forbidden_inputs_used"] == "false", "template forbidden flag mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "template claim boundary mismatch")
        require_false(
            row,
            [
                "control_suite_authorization_allowed",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
                "physical_validation_claimed",
            ],
            f"template {row['question_id']}",
        )
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    require(str(MANIFEST.relative_to(ROOT)) in names, "zip missing manifest")
    for row in manifest:
        path = ROOT / row["package_path"]
        require(path.exists(), f"manifest path missing: {row['package_path']}")
        require(row["package_path"] in names, f"zip missing {row['package_path']}")
        require(row["sha256"] == sha256(path), f"manifest checksum mismatch: {row['package_path']}")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        require_false(
            row,
            [
                "contains_endpoint_scores",
                "contains_fit_statistics",
                "control_suite_authorization_allowed",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
                "physical_validation_claimed",
            ],
            f"manifest {row['package_path']}",
        )
    doc = DOC.read_text()
    for marker in ["control-suite authorization", "does not authorize endpoint scoring", CLAIM_BOUNDARY]:
        require(marker in doc, f"doc missing marker: {marker}")
    instructions = INSTRUCTIONS.read_text()
    for marker in [
        "AUTHORIZE_CONTROL_SUITE_BUILD_ONLY_NOT_ENDPOINT_SCORING",
        "ACCEPT_SAME_NUMERIC_TJOINT_BINDING_NO_RETUNING",
        "ACCEPT_REQUIRED_CONTROL_FAMILIES_AS_ENDPOINT_BLOCKERS",
        "ACCEPT_CAVEATED_COVARIANCE_BOUNDARY",
    ]:
        require(marker in instructions, f"instructions missing marker: {marker}")
    external = EXTERNAL_MESSAGE.read_text()
    for marker in ["You do not need repository access", "not endpoint", "not evidence"]:
        require(marker in external, f"external message missing marker: {marker}")
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_AUTHORIZATION_PACKAGE_V1_VALIDATED sha256={summary['zip_sha256']}")


if __name__ == "__main__":
    main()
