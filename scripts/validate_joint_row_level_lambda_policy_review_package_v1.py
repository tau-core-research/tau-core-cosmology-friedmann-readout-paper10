#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_lambda_policy_review_response_template_v1.csv"
DIAG = ROOT / "data/derived/joint_row_level_lambda_policy_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_lambda_policy_review_package_v1.md"
CLAIM_BOUNDARY = "joint_row_level_lambda_policy_review_not_numeric_not_scoring_not_validation"


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
    summary = read_rows(SUMMARY)[0]
    template = read_rows(TEMPLATE)
    diag = read_rows(DIAG)[0]
    require(len(template) == 3, "template must contain three review questions")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["review_completed"] == "false", "review must not be pre-completed")
    require(summary["contains_lambda_row_numeric_value"] == "false", "numeric lambda must be absent")
    require(summary["contains_t_joint_rescoring"] == "false", "rescoring must be absent")
    require(summary["endpoint_validation_claimed"] == "false", "validation must be false")
    require(diag["lambda_row_dimension"] == "dimensionless", "lambda dimension must be dimensionless")
    require(diag["lambda_row_numeric_value_defined"] == "false", "numeric lambda must be undefined")
    require(diag["t_joint_rescoring_authorized"] == "false", "rescoring must be false")

    recorded_sha = SHA.read_text().split()[0]
    require(sha256(PACKAGE) == recorded_sha, "zip sha256 mismatch")
    require(recorded_sha == summary["zip_sha256"], "summary sha mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in manifest} | {str(MANIFEST.relative_to(ROOT))}
    require(expected.issubset(names), "zip missing manifest-listed files")

    for row in manifest:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        require(row["contains_endpoint_residuals"] == "false", "endpoint residual flag must be false")
        require(row["contains_new_endpoint_scores"] == "false", "endpoint score flag must be false")
        require(row["contains_fit_statistics"] == "false", "fit flag must be false")
        require(row["contains_lambda_row_numeric_value"] == "false", "lambda flag must be false")
        require(row["contains_t_joint_rescoring"] == "false", "rescoring flag must be false")
    for row in template:
        require(row["review_completed"] == "false", "template must not be pre-completed")
        require(row["forbidden_inputs_used"] == "false", "template forbidden flag must default false")
        require(row["lambda_row_numeric_value_authorized"] == "false", "lambda authorization must default false")
        require(row["t_joint_rescoring_authorized"] == "false", "rescoring authorization must default false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "no numeric lambda", "Dimensional audit", "no `T_joint` rescoring"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_LAMBDA_POLICY_REVIEW_PACKAGE_V1_VALIDATED sha256={recorded_sha}")


if __name__ == "__main__":
    main()
