#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_ZIP = ROOT / "data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.zip"
OUT_SHA = ROOT / "data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_reviewer_handoff_package_v1_summary.csv"
README = ROOT / "data/derived/REVIEWER_README_JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_V1.md"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_closure_review_not_scoring_not_validation"
EXPECTED_STATUS = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEWER_HANDOFF_PACKAGE_READY_NOT_COMPLETED"


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
    if summary["status"] != EXPECTED_STATUS:
        raise SystemExit(f"unexpected handoff status: {summary['status']}")
    if summary["zip_sha256"] != sha256(OUT_ZIP):
        raise SystemExit("handoff zip checksum mismatch")
    if OUT_SHA.read_text().split()[0] != summary["zip_sha256"]:
        raise SystemExit("handoff sha sidecar mismatch")
    if summary["package_file_count"] != str(len(manifest) + 1):
        raise SystemExit("handoff file count mismatch")
    require_false(
        summary,
        [
            "review_completed",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
        ],
        "summary",
    )
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")

    with zipfile.ZipFile(OUT_ZIP) as zf:
        names = set(zf.namelist())
    if str(MANIFEST.relative_to(ROOT)) not in names:
        raise SystemExit("handoff zip missing manifest")
    for row in manifest:
        path = ROOT / row["package_path"]
        if row["package_path"] not in names:
            raise SystemExit(f"handoff zip missing {row['package_path']}")
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

    text = README.read_text()
    compact_text = " ".join(text.split())
    for marker in [
        "You do not need repository access",
        "Forbidden inputs",
        "separate scoring authorization",
        "cross-probe covariance",
    ]:
        if marker not in compact_text:
            raise SystemExit(f"reviewer README missing marker: {marker}")
    print(
        "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEWER_HANDOFF_PACKAGE_V1_VALIDATED "
        f"sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
