#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv"


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


def main() -> None:
    rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]
    if summary["status"] != "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("unexpected authorization package summary status")
    if not zip_path.exists():
        raise SystemExit("missing authorization package zip")
    if not zip_sha256_path.exists():
        raise SystemExit("missing authorization package checksum sidecar")
    if sha256(zip_path) != summary["zip_sha256"]:
        raise SystemExit("authorization package zip checksum mismatch")
    if zip_sha256_path.read_text().strip() != f"{summary['zip_sha256']}  {zip_path.name}":
        raise SystemExit("authorization package checksum sidecar mismatch")
    if summary["package_file_count"] != "15":
        raise SystemExit("expected 15 files in authorization package")
    for key in [
        "review_completed",
        "endpoint_run_allowed",
        "physical_validation_claimed",
        "contains_endpoint_residuals",
        "contains_endpoint_scores",
        "contains_fit_statistics",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in rows}
    expected.add(str(MANIFEST.relative_to(ROOT)))
    if names != expected:
        raise SystemExit("authorization package contents do not match manifest")
    for row in rows:
        path = ROOT / row["package_path"]
        if not path.exists():
            raise SystemExit(f"missing manifest file: {row['package_path']}")
        if sha256(path) != row["sha256"]:
            raise SystemExit(f"checksum mismatch for {row['package_path']}")
        for key in [
            "contains_endpoint_residuals",
            "contains_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_run_allowed",
            "physical_validation_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"{row['package_path']} must keep {key}=false")
        if row["claim_boundary"] != "combined_multiblock_endpoint_authorization_review_not_validation":
            raise SystemExit("claim boundary mismatch")
    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_PACKAGE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
