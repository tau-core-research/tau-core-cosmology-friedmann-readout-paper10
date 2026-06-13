#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/joint_guarded_replay_run_template_authorization_policy_v1.csv"
TEMPLATE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_summary.csv"
MANIFEST = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1_manifest.csv"
PACKAGE = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip"
SHA = ROOT / "data/derived/joint_guarded_replay_run_template_authorization_package_v1.zip.sha256"
DOC = ROOT / "docs/joint_guarded_replay_run_template_authorization_package_v1.md"
RUN_TEMPLATE_SUMMARY = ROOT / "data/derived/joint_guarded_replay_run_template_v1_summary.csv"
CLAIM_BOUNDARY = "joint_guarded_replay_run_template_authorization_not_execution_not_scoring_not_validation"


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        require(row.get(field) == "false", f"{label}: {field} must be false")


def main() -> None:
    policy = read_rows(POLICY)
    template = read_rows(TEMPLATE)
    summary = read_one(SUMMARY)
    manifest = read_rows(MANIFEST)
    run_summary = read_one(RUN_TEMPLATE_SUMMARY)

    require(PACKAGE.exists(), "missing package zip")
    require(SHA.exists(), "missing package sha sidecar")
    require(summary["status"] == "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED", "bad package status")
    require(summary["zip_sha256"] == sha256(PACKAGE), "zip checksum mismatch")
    require(SHA.read_text().split()[0] == summary["zip_sha256"], "sha sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package must remain uncompleted")
    require(summary["template_authorized_for_later_permission_replay"] == "false", "template cannot be pre-authorized")
    require(summary["separate_execution_step_required"] == "true", "separate execution step must be required")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require_false(
        summary,
        [
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
    require(run_summary["status"] == "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_READY_NOT_EXECUTED", "run template dependency is not ready-not-executed")
    require(len(policy) == 4, "policy must contain four questions")
    require(len(template) == 4, "template must contain four rows")
    require({row["claim_boundary"] for row in policy} == {CLAIM_BOUNDARY}, "policy claim boundary mismatch")
    require({row["claim_boundary"] for row in template} == {CLAIM_BOUNDARY}, "template claim boundary mismatch")
    require({row["review_completed"] for row in template} == {"false"}, "template must be blank")
    require({row["forbidden_inputs_used"] for row in template} == {"false"}, "template forbidden flag mismatch")
    require({row["template_authorized_for_later_permission_replay"] for row in template} == {"false"}, "template authorization flag mismatch")
    require({row["separate_execution_step_required"] for row in template} == {"true"}, "template separate execution flag mismatch")
    for row in template:
        require_false(
            row,
            [
                "direct_execution_allowed",
                "direct_execution_allowed_by_this_package",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
            ],
            f"template {row['question_id']}",
        )

    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    require(str(MANIFEST.relative_to(ROOT)) in names, "zip must include manifest")
    for row in manifest:
        path = ROOT / row["package_path"]
        require(path.exists(), f"manifest path missing: {row['package_path']}")
        require(row["package_path"] in names, f"zip missing {row['package_path']}")
        require(row["sha256"] == sha256(path), f"manifest checksum mismatch: {row['package_path']}")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
        require_false(
            row,
            [
                "contains_endpoint_residuals",
                "contains_new_endpoint_scores",
                "contains_fit_statistics",
                "direct_execution_allowed",
                "endpoint_scoring_allowed",
                "endpoint_validation_claimed",
                "cosmological_validation_claimed",
            ],
            f"manifest {row['package_path']}",
        )

    text = DOC.read_text()
    for marker in [
        "not itself execution",
        "endpoint scoring",
        "cosmological validation",
        "Mandatory controls",
        "Mandatory caveats",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_GUARDED_REPLAY_RUN_TEMPLATE_AUTHORIZATION_PACKAGE_V1_VALIDATED "
        f"sha256={summary['zip_sha256']}"
    )


if __name__ == "__main__":
    main()
