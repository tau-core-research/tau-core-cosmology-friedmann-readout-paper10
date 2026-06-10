#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_manifest.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_sky_z_replay_authorization_review_package_v1_summary.csv"
)
PACKAGE_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_SKY_Z_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "v2_sky_z_replay_authorization_review_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]
    require(summary["package_id"] == PACKAGE_ID, "bad package id")
    require(summary["status"] == "V2_SKY_Z_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["verdict"] == "sky_z_replay_authorization_package_ready_not_completed", "bad verdict")
    require(summary["followup_family"] == "W_path_x_sky_z", "bad followup family")
    require(zip_path.exists(), "missing sky-z authorization zip")
    require(zip_sha256_path.exists(), "missing checksum sidecar")
    require(sha256(zip_path) == summary["zip_sha256"], "zip checksum mismatch")
    require(zip_sha256_path.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}", "checksum sidecar mismatch")
    require(int(summary["package_file_count"]) == len(rows) + 1, "package file count mismatch")
    for key in [
        "review_completed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "contains_endpoint_residuals",
        "contains_endpoint_scores",
        "contains_fit_statistics",
        "physical_lensing_path_weight_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in rows}
    expected.add(str(MANIFEST.relative_to(ROOT)))
    require(names == expected, "zip contents do not match manifest")
    for row in rows:
        path = ROOT / row["package_path"]
        require(path.exists(), f"missing manifest file: {row['package_path']}")
        require(sha256(path) == row["sha256"], f"checksum mismatch for {row['package_path']}")
        require(row["package_id"] == PACKAGE_ID, "manifest package id mismatch")
        for key in [
            "contains_endpoint_residuals",
            "contains_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            require(row[key] == "false", f"{row['package_path']} must keep {key}=false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
    print(
        "PAPER10_V2_SKY_Z_REPLAY_AUTHORIZATION_PACKAGE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
