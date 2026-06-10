#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv"
OUT_ZIP = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip"
OUT_ZIP_SHA256 = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package.zip.sha256"
MANIFEST = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_manifest.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_package_summary.csv"
PACKAGE_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE"
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"

PACKAGE_FILES = [
    "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization.md",
    "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_policy.csv",
    "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_template.csv",
    "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv",
    "docs/void_source_basis_refinement_v2_observer_orientation_kernel_v2.md",
    "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_manifest.csv",
    "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv",
    "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv",
    "docs/void_source_basis_refinement_v2_sky_z_source_audit_v1.md",
    "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1.csv",
    "data/derived/void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv",
    "data/derived/void_source_basis_refinement_v2_sky_z_authorized_replay_v1_summary.csv",
    "scripts/validate_void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template.py",
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


def manifest_row(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"missing observer-orientation package file: {rel}")
    return {
        "package_id": PACKAGE_ID,
        "package_path": rel,
        "byte_count": str(path.stat().st_size),
        "sha256": sha256(path),
        "contains_endpoint_residuals": "false",
        "contains_endpoint_scores": "false",
        "contains_fit_statistics": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    template_summary = read_one(TEMPLATE_SUMMARY)
    if template_summary["status"] != "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED":
        raise SystemExit("package requires a blank observer-orientation authorization template")
    if template_summary["endpoint_replay_allowed"] != "false" or template_summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("template must not authorize replay or validation")
    rows = [manifest_row(rel) for rel in PACKAGE_FILES]
    write_csv(MANIFEST, rows)
    package_rows = rows + [manifest_row(str(MANIFEST.relative_to(ROOT)))]
    OUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for row in package_rows:
            path = ROOT / row["package_path"]
            info = zipfile.ZipInfo(row["package_path"])
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
    zip_sha = sha256(OUT_ZIP)
    OUT_ZIP_SHA256.write_text(f"{zip_sha}  {OUT_ZIP.name}\n")
    write_csv(
        SUMMARY,
        [
            {
                "package_id": PACKAGE_ID,
                "status": "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED",
                "zip_path": str(OUT_ZIP.relative_to(ROOT)),
                "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
                "zip_sha256": zip_sha,
                "package_file_count": str(len(package_rows)),
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_residuals": "false",
                "contains_endpoint_scores": "false",
                "contains_fit_statistics": "false",
                "physical_lensing_path_weight_claimed": "false",
                "verdict": "observer_orientation_kernel_v2_replay_authorization_package_ready_not_completed",
                "recommended_next_action": "send_zip_to_reviewer_and_validate_completed_authorization_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print("PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTH_PACKAGE_BUILT review_completed=false")


if __name__ == "__main__":
    main()
