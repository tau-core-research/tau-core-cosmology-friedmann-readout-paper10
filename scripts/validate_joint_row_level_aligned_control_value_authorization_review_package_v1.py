#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_template_v1.csv"
AUTH_DIAG_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_value_authorization_review_package_v1.md"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_value_authorization_not_values_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = read_rows(MANIFEST)
    summary_rows = read_rows(SUMMARY)
    template = read_rows(TEMPLATE)
    diag_rows = read_rows(AUTH_DIAG_SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    require(len(diag_rows) == 1, "diagnostic summary must contain one row")
    require(len(template) == 4, "template must contain four review questions")
    summary = summary_rows[0]
    diag = diag_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["review_completed"] == "false", "review must not be pre-completed")
    require(summary["upstream_design_accepted"] == "true", "upstream design must be accepted")
    require(summary["aligned_control_value_computation_authorized"] == "false", "computation authorization must default false")
    require(summary["aligned_joint_control_values_authorized"] == "false", "aligned values must not be authorized")
    require(summary["contains_aligned_joint_control_values"] == "false", "aligned values must not be present")
    require(summary["contains_lambda_row_numeric_value"] == "false", "lambda value must be absent")
    require(summary["contains_t_joint_rescoring"] == "false", "rescoring must be absent")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must be false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must be false")

    require(diag["alignment_design_decision"] == "ACCEPT_CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION", "bad design decision")
    require(diag["blocker_verdict"] == "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED", "bad blocker verdict")
    require(diag["alignment_values_computed"] == "false", "diagnostic must not compute aligned values")
    require(diag["min_aligned_control_count_if_later_authorized"] == "6", "expected min aligned control count is 6")

    recorded_sha = SHA.read_text().split()[0]
    require(sha256(PACKAGE) == recorded_sha, "zip sha256 mismatch")
    require(recorded_sha == summary["zip_sha256"], "summary sha mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in manifest} | {str(MANIFEST.relative_to(ROOT))}
    require(expected.issubset(names), "zip missing manifest-listed files")

    for row in manifest:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        require(row["contains_endpoint_residuals"] == "false", "manifest endpoint residual flag must be false")
        require(row["contains_new_endpoint_scores"] == "false", "manifest endpoint score flag must be false")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag must be false")
        require(row["contains_aligned_joint_control_values"] == "false", "manifest aligned values flag must be false")
        require(row["contains_lambda_row_numeric_value"] == "false", "manifest lambda flag must be false")
        require(row["contains_t_joint_rescoring"] == "false", "manifest rescoring flag must be false")
        require(row["endpoint_scoring_allowed"] == "false", "manifest scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag must be false")

    for row in template:
        require(row["review_completed"] == "false", "template must not be pre-completed")
        require(row["forbidden_inputs_used"] == "false", "template forbidden flag must default false")
        require(row["aligned_control_value_computation_authorized"] == "false", "computation authorization must default false")
        require(row["aligned_joint_control_values_authorized"] == "false", "aligned values authorization must default false")
        require(row["lambda_row_numeric_value_authorized"] == "false", "lambda authorization must default false")
        require(row["t_joint_rescoring_authorized"] == "false", "rescoring authorization must default false")
        require(row["endpoint_scoring_authorized"] == "false", "endpoint scoring authorization must default false")

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "authorization to compute aligned control values only",
        "It does not contain aligned joint-control values.",
        "does not rescore",
        "separate numeric-lambda gate",
    ]:
        require(marker in text, f"doc missing marker: {marker}")

    print(f"JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_REVIEW_PACKAGE_V1_VALIDATED sha256={recorded_sha}")


if __name__ == "__main__":
    main()
