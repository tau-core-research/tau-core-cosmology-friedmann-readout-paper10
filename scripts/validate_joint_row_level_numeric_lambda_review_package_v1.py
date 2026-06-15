#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_template_v1.csv"
DIAG_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_candidate_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_lambda_review_package_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_lambda_review_not_rescoring_not_validation"


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
    diag_rows = read_rows(DIAG_SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    require(len(diag_rows) == 1, "diagnostic summary must contain one row")
    require(len(template) == 3, "template must contain three review questions")
    summary = summary_rows[0]
    diag = diag_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["review_completed"] == "false", "review must not be pre-completed")
    require(summary["lambda_row_numeric_value"] == "1.0", "expected lambda_row=1.0")
    require(summary["lambda_row_dimension"] == "dimensionless", "lambda must be dimensionless")
    require(summary["lambda_rule"] == "dimensionless_unit_weight_prior", "unexpected lambda rule")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda must not be pre-authorized")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must be false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must be false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must be false")
    require(summary["contains_lambda_row_numeric_value"] == "true", "package should contain numeric lambda candidate")
    require(summary["contains_t_joint_rescoring"] == "false", "package must not contain rescoring")

    require(diag["lambda_row_numeric_value"] == "1.0", "diagnostic lambda mismatch")
    require(diag["lambda_row_dimension"] == "dimensionless", "diagnostic dimension mismatch")
    require(diag["lambda_source_status"] == "residual_blind_unit_prior_candidate_for_review", "bad lambda source status")
    require(diag["policy_decision"] == "ACCEPT_LAMBDA_POLICY_BOUNDARY_NOT_NUMERIC_NOT_RESCORING_NOT_VALIDATION", "bad policy decision")
    require(diag["blocker_verdict"] == "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED", "bad blocker verdict")
    require(diag["lambda_row_numeric_value_authorized"] == "false", "diagnostic lambda authorization must be false")
    require(diag["t_joint_rescoring_authorized"] == "false", "diagnostic rescoring must be false")
    require(diag["endpoint_scoring_allowed"] == "false", "diagnostic scoring must be false")
    require(diag["endpoint_validation_claimed"] == "false", "diagnostic validation must be false")

    recorded_sha = SHA.read_text().split()[0]
    require(sha256(PACKAGE) == recorded_sha, "zip sha256 mismatch")
    require(recorded_sha == summary["zip_sha256"], "summary sha mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in manifest} | {str(MANIFEST.relative_to(ROOT))}
    require(expected.issubset(names), "zip missing manifest-listed files")

    lambda_file_count = 0
    for row in manifest:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        require(row["contains_endpoint_residuals"] == "false", "manifest endpoint residual flag must be false")
        require(row["contains_new_endpoint_scores"] == "false", "manifest endpoint score flag must be false")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag must be false")
        require(row["contains_t_joint_rescoring"] == "false", "manifest rescoring flag must be false")
        require(row["contains_endpoint_scoring"] == "false", "manifest endpoint scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag must be false")
        if row["contains_lambda_row_numeric_value"] == "true":
            lambda_file_count += 1
    require(lambda_file_count == 2, "expected exactly lambda candidate CSV and summary to carry numeric lambda flag")

    for row in template:
        require(row["review_completed"] == "false", "template must not be pre-completed")
        require(row["forbidden_inputs_used"] == "false", "template forbidden flag must default false")
        require(row["lambda_row_numeric_value_authorized"] == "false", "template lambda authorization must default false")
        require(row["t_joint_rescoring_authorized"] == "false", "template rescoring authorization must default false")
        require(row["endpoint_scoring_authorized"] == "false", "template endpoint scoring authorization must default false")

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "`lambda_row = 1`",
        "unit-weight",
        "does not apply the value",
        "not authorize `T_joint` rescoring",
    ]:
        require(marker in text, f"doc missing marker: {marker}")

    print(f"JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_V1_VALIDATED sha256={recorded_sha}")


if __name__ == "__main__":
    main()
