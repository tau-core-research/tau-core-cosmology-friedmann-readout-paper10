#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_row_level_t_joint_rescoring_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_row_level_t_joint_rescoring_authorization_review_package_v1.md"
CLAIM_BOUNDARY = "joint_row_level_t_joint_rescoring_authorization_not_endpoint_scoring_not_validation"


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
    require(len(summary_rows) == 1, "summary must contain one row")
    require(len(template) == 3, "template must contain three review questions")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["review_completed"] == "false", "review must not be pre-completed")
    require(summary["aligned_control_values_ready"] == "true", "aligned-control values should be ready")
    require(summary["numeric_lambda_ready"] == "true", "numeric lambda should be ready")
    require(summary["lambda_row_numeric_value"] == "1.0", "expected lambda_row=1.0")
    require(summary["t_joint_rescoring_ledger_authorized"] == "false", "rescoring must not be pre-authorized")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must be false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must be false")
    require(summary["contains_t_joint_penalized_values"] == "false", "package must not contain penalized values")
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
        require(row["contains_new_endpoint_scores"] == "false", "manifest endpoint scores flag must be false")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag must be false")
        require(row["contains_t_joint_penalized_values"] == "false", "manifest penalized values flag must be false")
        require(row["contains_rescoring_authorization"] == "false", "manifest rescoring authorization flag must be false")
        require(row["endpoint_scoring_allowed"] == "false", "manifest endpoint scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag must be false")
    for row in template:
        require(row["review_completed"] == "false", "template must not be pre-completed")
        require(row["forbidden_inputs_used"] == "false", "template forbidden flag must default false")
        require(row["t_joint_rescoring_ledger_authorized"] == "false", "template rescoring authorization must default false")
        require(row["endpoint_scoring_authorized"] == "false", "template endpoint scoring must default false")
        require(row["endpoint_validation_claimed_by_reviewer"] == "false", "template validation must default false")
    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "not endpoint scoring",
        "not validation",
        "does not compute `T_joint_penalized`",
        "future record-only penalized `T_joint` ledger",
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_T_JOINT_RESCORING_AUTHORIZATION_REVIEW_PACKAGE_V1_VALIDATED sha256={recorded_sha}")


if __name__ == "__main__":
    main()
