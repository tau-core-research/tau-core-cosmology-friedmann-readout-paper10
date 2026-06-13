#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_permission_replay_authorization_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/joint_guarded_permission_replay_authorization_response_template_v1.csv"
DOC = ROOT / "docs/joint_guarded_permission_replay_authorization_package_v1.md"
CLAIM_BOUNDARY = "joint_guarded_permission_replay_authorization_not_scoring_not_validation"


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
    if summary["status"] != "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED":
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
            "guarded_replay_package_authorized",
            "direct_execution_allowed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
        ],
        "summary",
    )
    if summary["separate_run_template_required"] != "true":
        raise SystemExit("separate run template must be required")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if len(template) != 4:
        raise SystemExit("template must contain four rows")
    for row in template:
        require_false(
            row,
            [
                "review_completed",
                "forbidden_inputs_used",
                "guarded_replay_package_authorized",
                "direct_execution_allowed",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
            ],
            f"template {row['question_id']}",
        )
        if row["separate_run_template_required"] != "true":
            raise SystemExit("template must require a separate run template")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("template claim boundary mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    if str(MANIFEST.relative_to(ROOT)) not in names:
        raise SystemExit("zip missing manifest")
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
    for marker in ["not scoring", "guarded", "same block-diagonal statistic", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_GUARDED_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_V1_VALIDATED "
        f"sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
