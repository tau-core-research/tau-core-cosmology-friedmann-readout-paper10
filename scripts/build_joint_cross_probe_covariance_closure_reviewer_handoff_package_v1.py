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
PACKAGE_SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv"
PACKAGE_ID = "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEWER_HANDOFF_PACKAGE_V1"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_closure_review_not_scoring_not_validation"

PACKAGE_FILES = [
    "data/derived/REVIEWER_README_JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_V1.md",
    "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip",
    "data/derived/joint_cross_probe_covariance_closure_review_package_v1.zip.sha256",
    "data/derived/joint_cross_probe_covariance_closure_review_package_v1_manifest.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_package_v1_summary.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv",
    "data/derived/joint_cross_probe_covariance_closure_review_response_v1_summary.csv",
    "data/source_manifest/joint_cross_probe_covariance_source_requirements_policy_v1.csv",
    "data/derived/joint_cross_probe_covariance_source_requirements_v1.csv",
    "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv",
    "docs/joint_cross_probe_covariance_source_requirements_v1.md",
    "docs/joint_cross_probe_covariance_closure_review_package_v1.md",
    "scripts/validate_joint_cross_probe_covariance_closure_review_response_v1.py",
    "scripts/import_joint_cross_probe_covariance_closure_review_response_v1.py",
    "scripts/build_joint_cross_probe_covariance_source_requirements_v1.py",
    "scripts/validate_joint_cross_probe_covariance_source_requirements_v1.py",
]


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing handoff file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_new_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    package_summary = read_one(PACKAGE_SUMMARY)
    if package_summary["status"] != "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEW_PACKAGE_READY_NOT_COMPLETED":
        raise SystemExit("cross-probe closure review package is not ready")
    for flag in [
        "review_completed",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        if package_summary[flag] != "false":
            raise SystemExit(f"unsafe package summary flag: {flag}")

    README.write_text(
        "\n".join(
            [
                "# Reviewer handoff: Joint cross-probe covariance closure v1",
                "",
                "You do not need repository access to complete this review.",
                "",
                "## Task",
                "",
                "Review whether Paper10's joint route can close the outstanding",
                "cross-probe covariance / independence blocker across these active blocks:",
                "",
                "- KiDS/COSEBIs low-mode lensing",
                "- observer/path low-z",
                "- DESI shape/readout",
                "",
                "This is a source-side review only. It is not endpoint scoring, not",
                "endpoint validation, and not cosmological validation.",
                "",
                "## Fill this file",
                "",
                "`data/derived/joint_cross_probe_covariance_closure_review_response_template_v1.csv`",
                "",
                "For every row, set `review_completed=true`, provide",
                "`reviewer_id_or_role`, `reviewer_response`, and `reviewer_rationale`.",
                "If you accept either a covariance-product route or an independence route,",
                "also provide `source_reference_or_url`.",
                "",
                "## Forbidden inputs",
                "",
                "Do not use endpoint residuals, new endpoint scores, fit improvements,",
                "posterior chains, or post-score control ranks. Keep",
                "`forbidden_inputs_used=false` unless this rule was violated.",
                "",
                "## Safe outcomes",
                "",
                "The allowed outcomes are:",
                "",
                "1. keep the blocker open;",
                "2. identify a source-native/source-frozen cross-probe covariance product;",
                "3. accept a caveated block-diagonal independence precondition.",
                "",
                "Even outcomes 2 or 3 do not authorize scoring. A separate scoring",
                "authorization package is required later.",
                "",
                "## Current package checksum",
                "",
                f"- review package zip sha256: `{package_summary['zip_sha256']}`",
                "",
            ]
        )
    )

    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    digest = sha256(OUT_ZIP)
    OUT_SHA.write_text(f"{digest}  {OUT_ZIP.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEWER_HANDOFF_PACKAGE_READY_NOT_COMPLETED",
                "zip_path": str(OUT_ZIP.relative_to(ROOT)),
                "zip_sha256_path": str(OUT_SHA.relative_to(ROOT)),
                "zip_sha256": digest,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_new_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "recommended_next_action": "send_handoff_zip_to_external_reviewer_without_repo_access",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print(f"JOINT_CROSS_PROBE_COVARIANCE_CLOSURE_REVIEWER_HANDOFF_PACKAGE_V1_BUILT sha256={digest}")


if __name__ == "__main__":
    main()
