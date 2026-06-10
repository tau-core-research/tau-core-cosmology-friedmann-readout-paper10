#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv"
)
MANIFEST = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_manifest.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1_summary.csv"
)

PACKAGE_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_V1"
EXPECTED_INCLUDED = {
    "docs/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.md",
    "docs/void_source_basis_refinement_v2_projection_morphology_gate_v1.md",
    "data/source_manifest/void_source_basis_refinement_v2_path_partial_scope_reviewer_package_policy_v1.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_reviewer_response_template_v1.csv",
    "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_projection_crossmap_audit.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_policy.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_values_summary.csv",
    "data/derived/void_source_basis_refinement_v2_path_partial_scope_values.csv",
    "scripts/validate_void_source_basis_refinement_v2_path_partial_scope_reviewer_package_v1.py",
}


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
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    rows = read_rows(MANIFEST)
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]

    require(policy["status"] == "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_POLICY_FROZEN", "bad policy status")
    require(policy["review_completed"] == "false", "policy must keep review_completed=false")
    require(policy["current_endpoint_replay_allowed"] == "false", "policy must not authorize endpoint replay")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["package_id"] == PACKAGE_ID, "bad package id")
    require(summary["status"] == "V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["verdict"] == "partial_path_scope_reviewer_package_ready_not_completed", "bad verdict")
    for key in [
        "review_completed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "contains_endpoint_residuals",
        "contains_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(summary["claim_boundary"] == policy["claim_boundary"], "claim boundary mismatch")
    require(zip_path.exists(), "missing reviewer package zip")
    require(zip_sha256_path.exists(), "missing checksum sidecar")
    require(sha256(zip_path) == summary["zip_sha256"], "zip checksum mismatch")
    require(
        zip_sha256_path.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}",
        "checksum sidecar mismatch",
    )
    require(int(summary["package_file_count"]) == len(rows) + 1, "package file count mismatch")

    manifest_paths = {row["package_path"] for row in rows}
    require(EXPECTED_INCLUDED.issubset(manifest_paths), "missing required reviewer package artifacts")
    for row in rows:
        require(row["package_id"] == PACKAGE_ID, "manifest package id mismatch")
        path = ROOT / row["package_path"]
        require(path.exists(), f"missing manifest file: {row['package_path']}")
        require(sha256(path) == row["sha256"], f"checksum mismatch for {row['package_path']}")
        for key in [
            "contains_endpoint_residuals",
            "contains_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[key] == "false", f"manifest row must keep {key}=false")
        require(row["claim_boundary"] == policy["claim_boundary"], "manifest claim boundary mismatch")

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected_zip_names = set(manifest_paths)
    expected_zip_names.add(str(MANIFEST.relative_to(ROOT)))
    require(names == expected_zip_names, "zip contents do not match manifest")
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_REVIEWER_PACKAGE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
