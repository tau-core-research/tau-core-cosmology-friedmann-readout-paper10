#!/usr/bin/env python3
"""Validate the caveated ACT K_path replay-authorization review package."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE_ID = "ACT_DR6_LENSING_CAVEATED_KPATH_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_replay_authorization_review_not_validation"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_package_v1_summary.csv"
TEMPLATE = DERIVED / "act_dr6_lensing_caveated_kpath_replay_authorization_review_response_template_v1.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    manifest_rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)
    template_rows = read_rows(TEMPLATE)

    require(summary["package_id"] == PACKAGE_ID, "bad package id")
    require(
        summary["status"] == "CAVEATED_KPATH_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "bad package status",
    )
    require(
        summary["verdict"] == "ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED",
        "bad package verdict",
    )
    require(
        summary["source_design_review_decision"]
        == "ACCEPT_CAVEATED_KPATH_SOURCE_DESIGN_FOR_REVIEW_ONLY",
        "missing source-design acceptance",
    )
    for key in (
        "review_completed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_lensing_path_weight_claimed",
    ):
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(
        summary["future_permission_only_replay_package_authorization_pending"] == "true",
        "future replay-package authorization should be pending",
    )
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")

    zip_path = ROOT / summary["zip_path"]
    sidecar = ROOT / summary["zip_sha256_path"]
    require(zip_path.exists(), "missing zip")
    require(sidecar.exists(), "missing checksum sidecar")
    require(sha256(zip_path) == summary["zip_sha256"], "zip checksum mismatch")
    require(sidecar.read_text().strip() == f"{summary['zip_sha256']}  {zip_path.name}", "sidecar mismatch")
    require(int(summary["package_file_count"]) == len(manifest_rows) + 1, "package file count mismatch")

    with zipfile.ZipFile(zip_path) as zf:
        zip_names = set(zf.namelist())
    expected_names = {row["package_path"] for row in manifest_rows}
    expected_names.add(str(MANIFEST.relative_to(ROOT)))
    require(zip_names == expected_names, "zip contents do not match manifest")

    for row in manifest_rows:
        path = ROOT / row["package_path"]
        require(path.exists(), f"missing package file: {row['package_path']}")
        require(row["package_id"] == PACKAGE_ID, "manifest package id mismatch")
        require(sha256(path) == row["sha256"], f"checksum mismatch for {row['package_path']}")
        for key in (
            "contains_endpoint_residuals",
            "contains_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ):
            require(row[key] == "false", f"{row['package_path']} must keep {key}=false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")

    require(
        {row["question_id"] for row in template_rows}
        == {
            "Q1_source_design_acceptance",
            "Q2_controls_required",
            "Q3_old_branch_quarantine",
            "Q4_forbidden_inputs",
            "Q5_permission_only_replay",
        },
        "unexpected review template questions",
    )
    require(
        all(row["endpoint_replay_allowed"] == "false" for row in template_rows),
        "template must not authorize replay",
    )
    print("ACT_CAVEATED_KPATH_REPLAY_AUTHORIZATION_REVIEW_PACKAGE_VALIDATED")


if __name__ == "__main__":
    main()
