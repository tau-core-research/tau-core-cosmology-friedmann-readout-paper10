#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_r6_reviewer_handoff_package_policy_v1.csv"
MANIFEST = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv"


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
    rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)
    zip_path = ROOT / summary["zip_path"]
    zip_sha256_path = ROOT / summary["zip_sha256_path"]
    require(policy["status"] == "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_POLICY_FROZEN", "bad policy")
    require(summary["status"] == "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_BUILT_NOT_COMPLETED", "bad summary status")
    require(zip_path.exists(), "missing R6 handoff zip")
    require(zip_sha256_path.exists(), "missing R6 handoff checksum sidecar")
    require(sha256(zip_path) == summary["zip_sha256"], "zip checksum mismatch")
    require(zip_sha256_path.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}", "checksum sidecar mismatch")
    require(int(summary["package_file_count"]) == len(rows) + 1, "package file count mismatch")
    for key in [
        "review_completed",
        "independent_reviewer_attestation_complete",
        "leakage_review_complete",
        "source_unique_ready",
        "computes_new_scores",
        "contains_endpoint_data",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(summary["verdict"] == "r6_reviewer_handoff_package_ready_not_completed", "unexpected verdict")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in rows}
    expected.add(str(MANIFEST.relative_to(ROOT)))
    require(names == expected, "zip contents do not match manifest")
    for row in rows:
        path = ROOT / row["package_path"]
        require(path.exists(), f"missing manifest file: {row['package_path']}")
        require(sha256(path) == row["sha256"], f"checksum mismatch for {row['package_path']}")
        require(row["contains_endpoint_data"] == "false", "manifest rows must not contain endpoint data")
        require(row["endpoint_replay_allowed"] == "false", "manifest rows must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "manifest rows must not claim validation")
        require(row["claim_boundary"] == policy["claim_boundary"], "claim boundary mismatch")
    require(summary["claim_boundary"] == policy["claim_boundary"], "summary claim boundary mismatch")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
