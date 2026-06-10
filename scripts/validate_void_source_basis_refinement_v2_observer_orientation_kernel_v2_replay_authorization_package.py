#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_manifest.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv"
PACKAGE_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE"
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one(path: Path) -> dict[str, str]:
    r = rows(path)
    if len(r) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return r[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(c: bool, m: str) -> None:
    if not c:
        raise SystemExit(m)


def main() -> None:
    manifest = rows(MANIFEST)
    summary = one(SUMMARY)
    zip_path = ROOT / summary["zip_path"]
    sidecar = ROOT / summary["zip_sha256_path"]
    require(summary["package_id"] == PACKAGE_ID, "bad package id")
    require(summary["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(zip_path.exists(), "missing package zip")
    require(sidecar.exists(), "missing package sha sidecar")
    require(sha256(zip_path) == summary["zip_sha256"], "zip checksum mismatch")
    require(sidecar.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}", "sidecar mismatch")
    require(int(summary["package_file_count"]) == len(manifest) + 1, "package file count mismatch")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {r["package_path"] for r in manifest}
    expected.add(str(MANIFEST.relative_to(ROOT)))
    require(names == expected, "zip contents mismatch")
    for key in ["review_completed", "endpoint_replay_allowed", "endpoint_validation_claimed", "contains_endpoint_scores", "contains_fit_statistics", "physical_lensing_path_weight_claimed"]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for r in manifest:
        path = ROOT / r["package_path"]
        require(path.exists(), f"missing manifest file {r['package_path']}")
        require(sha256(path) == r["sha256"], f"checksum mismatch {r['package_path']}")
        require(r["package_id"] == PACKAGE_ID, "manifest package id mismatch")
        require(r["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        for key in ["contains_endpoint_residuals", "contains_endpoint_scores", "contains_fit_statistics", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_lensing_path_weight_claimed"]:
            require(r[key] == "false", f"{r['package_path']} must keep {key}=false")
    print("PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTH_PACKAGE_VALIDATED review_completed=false")


if __name__ == "__main__":
    main()
