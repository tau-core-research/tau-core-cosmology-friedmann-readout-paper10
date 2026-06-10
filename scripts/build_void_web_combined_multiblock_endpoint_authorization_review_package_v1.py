#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv"
OUT_ZIP = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip"
OUT_ZIP_SHA256 = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_package_v1_summary.csv"

PACKAGE_FILES = [
    "REVIEWER_README_VOID_WEB_COMBINED_ENDPOINT_AUTHORIZATION.md",
    "data/source_manifest/void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv",
    "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv",
    "data/derived/void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv",
    "docs/void_web_combined_multiblock_endpoint_authorization_review_v1.md",
    "data/source_manifest/void_web_combined_multiblock_endpoint_protocol_v1.csv",
    "docs/void_web_combined_multiblock_endpoint_protocol_v1.md",
    "data/derived/void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv",
    "docs/void_web_endpoint_readiness_after_flrw_audit_v1.md",
    "data/source_manifest/cosmology_flrw_consistency_channel_audit_v1.csv",
    "docs/cosmology_flrw_consistency_channel_audit_v1.md",
    "data/source_manifest/cosmology_source_grounding_gate_v1.csv",
    "docs/cosmology_source_grounding_gate_v1.md",
    "scripts/validate_void_web_combined_multiblock_endpoint_authorization_review_template_v1.py",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    template_summary = read_one(TEMPLATE_SUMMARY)
    if template_summary["status"] != "AUTHORIZATION_REVIEW_TEMPLATE_READY_NOT_COMPLETED":
        raise SystemExit("authorization package requires a blank template")
    if template_summary["endpoint_run_allowed"] != "false":
        raise SystemExit("authorization package must not pre-authorize endpoint run")
    if template_summary["physical_validation_claimed"] != "false":
        raise SystemExit("authorization package must not claim physical validation")

    rows = []
    for rel in PACKAGE_FILES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing authorization package file: {rel}")
        rows.append(
            {
                "package_id": "VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_PACKAGE_V1",
                "package_path": rel,
                "byte_count": str(path.stat().st_size),
                "sha256": sha256(path),
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "endpoint_run_allowed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": "combined_multiblock_endpoint_authorization_review_not_validation",
            }
        )
    write_csv(MANIFEST, rows)
    package_rows = rows + [
        {
            "package_id": "VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_PACKAGE_V1",
            "package_path": str(MANIFEST.relative_to(ROOT)),
            "byte_count": str(MANIFEST.stat().st_size),
            "sha256": sha256(MANIFEST),
            "contains_endpoint_residuals": "false",
            "contains_endpoint_scores": "false",
            "contains_fit_statistics": "false",
            "endpoint_run_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "combined_multiblock_endpoint_authorization_review_not_validation",
        }
    ]

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    zip_sha256 = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_sha256}  {OUT_ZIP.name}\n")
    summary = [
        {
            "package_id": "VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_PACKAGE_V1",
            "status": "AUTHORIZATION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED",
            "zip_path": str(OUT_ZIP.relative_to(ROOT)),
            "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
            "zip_sha256": zip_sha256,
            "package_file_count": str(len(package_rows)),
            "review_completed": "false",
            "endpoint_run_allowed": "false",
            "physical_validation_claimed": "false",
            "contains_endpoint_residuals": "false",
            "contains_endpoint_scores": "false",
            "contains_fit_statistics": "false",
            "verdict": "authorization_review_package_ready_not_completed",
            "recommended_next_action": "send_zip_to_independent_reviewer_and_validate_completed_response",
            "claim_boundary": "combined_multiblock_endpoint_authorization_review_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_PACKAGE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
