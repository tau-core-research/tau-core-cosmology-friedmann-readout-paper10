#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip"
ZIP_SHA256 = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_package_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_replay_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    require(summary["status"] == "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["zip_sha256"] == sha256(ZIP_PATH), "zip checksum mismatch")
    require(ZIP_SHA256.read_text().split()[0] == summary["zip_sha256"], "zip sha256 sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package must not be completed")
    require(summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(summary["contains_endpoint_residuals"] == "false", "package must not contain residuals")
    require(summary["contains_endpoint_scores"] == "false", "package must not contain scores")
    require(summary["contains_fit_statistics"] == "false", "package must not contain fit stats")
    require(summary["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = set(zf.namelist())
    for row in manifest:
        require(row["package_path"] in names, f"missing package member {row['package_path']}")
        require(row["sha256"] == sha256(ROOT / row["package_path"]), f"manifest checksum mismatch {row['package_path']}")
        require(row["contains_endpoint_residuals"] == "false", "manifest residual flag must be false")
        require(row["contains_endpoint_scores"] == "false", "manifest score flag must be false")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag must be false")
        require(row["endpoint_replay_allowed"] == "false", "manifest replay flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag must be false")
        require(row["physical_validation_claimed"] == "false", "manifest physical validation flag must be false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
    require(str(MANIFEST.relative_to(ROOT)) in names, "zip must include manifest")
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_PACKAGE_V1_VALIDATED "
        f"zip_sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
