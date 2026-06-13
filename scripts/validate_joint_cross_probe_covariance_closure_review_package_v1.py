#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip"
SHA = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv"
DOC = ROOT / "docs/joint_cross_probe_covariance_closure_review_package_v1.md"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_closure_review_not_scoring_not_validation"
EXPECTED_STATUS = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_READY_NOT_COMPLETED"


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


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row[field] != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    template = read_rows(TEMPLATE)
    if not PACKAGE.exists():
        raise SystemExit("missing review package zip")
    if not DOC.exists():
        raise SystemExit("missing review package docs")
    if summary["status"] != EXPECTED_STATUS:
        raise SystemExit(f"unexpected package status: {summary['status']}")
    if summary["zip_sha256"] != sha256(PACKAGE):
        raise SystemExit("zip checksum mismatch")
    if SHA.read_text().split()[0] != summary["zip_sha256"]:
        raise SystemExit("sha sidecar mismatch")
    if summary["package_file_count"] != str(len(manifest) + 1):
        raise SystemExit("package file count mismatch")
    require_false(
        summary,
        [
            "review_completed",
            "cross_probe_covariance_defined",
            "block_diagonal_shell_executable",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
        ],
        "summary",
    )
    if summary["hard_blocker_remains_open"] != "true":
        raise SystemExit("summary must keep hard blocker open")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if len(template) != 5:
        raise SystemExit("template must contain five reviewer questions")
    for row in template:
        if row["review_completed"] != "false":
            raise SystemExit("template must be blank")
        require_false(
            row,
            [
                "forbidden_inputs_used",
                "cross_probe_covariance_product_available",
                "block_diagonal_independence_source_justified",
                "future_scoring_precondition_closure_allowed",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
            ],
            f"template {row['question_id']}",
        )
        if row["separate_scoring_authorization_required"] != "true":
            raise SystemExit("template must require separate scoring authorization")
        if row["hard_blocker_remains_open"] != "true":
            raise SystemExit("template must keep hard blocker open")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("template claim boundary mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    if str(MANIFEST.relative_to(ROOT)) not in names:
        raise SystemExit("zip must include manifest")
    for row in manifest:
        path = ROOT / row["package_path"]
        if row["package_path"] not in names:
            raise SystemExit(f"zip missing {row['package_path']}")
        if row["sha256"] != sha256(path):
            raise SystemExit(f"manifest checksum mismatch: {row['package_path']}")
        require_false(
            row,
            [
                "contains_endpoint_residuals",
                "contains_new_endpoint_scores",
                "contains_fit_statistics",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
            ],
            f"manifest {row['package_path']}",
        )
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("manifest claim boundary mismatch")
    text = DOC.read_text()
    for marker in [
        "not scoring",
        "cross-probe covariance/independence",
        "Covariance-product route",
        "Independence-rationale route",
        CLAIM_BOUNDARY,
    ]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_V1_VALIDATED "
        f"sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
