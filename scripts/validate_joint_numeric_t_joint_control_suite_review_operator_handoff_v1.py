#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/joint_numeric_t_joint_control_suite_review_operator_handoff_v1.md"
PACKAGE = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip.sha256"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    require(DOC.exists(), "missing operator handoff doc")
    require(PACKAGE.exists(), "missing review package")
    require(SHA.exists(), "missing review package sha")
    doc = DOC.read_text()
    doc_lower = doc.lower()
    checksum = SHA.read_text().split()[0]
    for marker in [
        "joint_numeric_t_joint_control_suite_review_not_endpoint_scoring_not_validation",
        "data/derived/joint_numeric_t_joint_control_suite_review_package_v1.zip",
        checksum,
        "0/26",
        "endpoint_scoring_authorization_package_preparation_allowed=true",
        "endpoint_scoring_allowed=false",
        "endpoint_validation_claimed=false",
        "cosmological_validation_claimed=false",
        "physical_validation_claimed=false",
        "ACCEPT_PREPARE_SEPARATE_ENDPOINT_AUTHORIZATION_PACKAGE",
        "scripts/import_joint_numeric_t_joint_control_suite_review_response_v1.py",
        "READY_TO_BUILD_ENDPOINT_AUTHORIZATION_PACKAGE_NOT_SCORING",
    ]:
        require(marker in doc, f"handoff doc missing marker: {marker}")
    require("does not" in doc_lower and "authorize endpoint scoring" in doc_lower, "handoff doc missing scoring prohibition")
    print(f"JOINT_NUMERIC_T_JOINT_CONTROL_SUITE_REVIEW_OPERATOR_HANDOFF_V1_VALIDATED sha256={checksum}")


if __name__ == "__main__":
    main()
