#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_replay_execution_authorization_package_v1.zip.sha256"
TEMPLATE = ROOT / "data/derived/joint_guarded_replay_execution_authorization_response_template_v1.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_execution_authorization_not_validation"


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


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    template = read_rows(TEMPLATE)
    require(PACKAGE.exists(), "missing package zip")
    require(SHA.exists(), "missing sha sidecar")
    require(summary["status"] == "JOINT_GUARDED_REPLAY_EXECUTION_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED", "bad status")
    require(summary["zip_sha256"] == sha256(PACKAGE), "zip checksum mismatch")
    require(SHA.read_text().split()[0] == summary["zip_sha256"], "sha sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package must remain uncompleted")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "permission_only_execution_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must be false")
    require(len(template) == 4, "template must contain four rows")
    require({row["review_completed"] for row in template} == {"false"}, "template must be blank")
    require({row["forbidden_inputs_used"] for row in template} == {"false"}, "template forbidden flag mismatch")
    require({row["permission_only_execution_allowed"] for row in template} == {"false"}, "template execution flag mismatch")
    require({row["claim_boundary"] for row in template} == {CLAIM_BOUNDARY}, "template claim boundary mismatch")
    manifest_name = str(MANIFEST.relative_to(ROOT))
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
        require(manifest_name in names, "zip must include manifest")
        require(zf.read(manifest_name) == MANIFEST.read_bytes(), "archived manifest mismatch")
        for row in manifest:
            path = ROOT / row["package_path"]
            require(path.exists(), f"manifest path missing: {row['package_path']}")
            require(row["package_path"] in names, f"zip missing {row['package_path']}")
            require(
                row["sha256"] == sha256_bytes(zf.read(row["package_path"])),
                f"archived checksum mismatch: {row['package_path']}",
            )
            require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
            for field in [
                "contains_endpoint_residuals",
                "contains_new_endpoint_scores",
                "contains_fit_statistics",
                "permission_only_execution_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
                "physical_validation_claimed",
            ]:
                require(row[field] == "false", f"manifest {field} must be false")
    print(
        "JOINT_GUARDED_REPLAY_EXECUTION_AUTHORIZATION_PACKAGE_V1_VALIDATED "
        f"sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
