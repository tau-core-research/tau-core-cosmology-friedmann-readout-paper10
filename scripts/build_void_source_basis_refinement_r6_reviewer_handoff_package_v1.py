#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_r6_reviewer_handoff_package_policy_v1.csv"
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_template_v1_summary.csv"
OUT_ZIP = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip"
OUT_ZIP_SHA256 = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1.zip.sha256"
MANIFEST = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_reviewer_handoff_package_v1_summary.csv"

PACKAGE_FILES = [
    "docs/void_source_basis_refinement_r6_external_reviewer_instructions_v1.md",
    "data/derived/void_source_basis_refinement_r6_reviewer_template_v1.csv",
    "data/derived/void_source_basis_refinement_r6_reviewer_template_v1_summary.csv",
    "docs/void_source_basis_refinement_r6_reviewer_template_v1.md",
    "docs/void_source_basis_refinement_r6_reviewer_handoff_package_v1.md",
    "data/source_manifest/void_source_basis_refinement_r6_completed_reviewer_response_policy_v1.csv",
    "scripts/validate_void_source_basis_refinement_r6_completed_reviewer_response_v1.py",
    "docs/void_source_basis_refinement_acquisition_manifest_v1.md",
    "docs/void_source_basis_refinement_r1_r3_source_attachment_v1.md",
    "docs/void_source_basis_refinement_r4_independence_preflight_v1.md",
    "docs/void_source_basis_refinement_r5_control_resistance_preflight_v1.md",
    "data/source_manifest/void_source_basis_refinement_acquisition_manifest_policy_v1.csv",
    "data/derived/void_source_basis_refinement_acquisition_manifest_v1.csv",
    "data/derived/void_source_basis_refinement_acquisition_manifest_v1_summary.csv",
    "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1.csv",
    "data/derived/void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv",
    "data/derived/low_z_pantheon_void_geometry_join_v1.csv",
    "data/derived/low_z_pantheon_los_environment_v1.csv",
    "data/derived/void_source_basis_refinement_r4_independence_preflight_v1.csv",
    "data/derived/void_source_basis_refinement_r4_independence_preflight_v1_summary.csv",
    "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1.csv",
    "data/derived/void_source_basis_refinement_r5_control_vectors_v1.csv",
    "data/derived/void_source_basis_refinement_r5_control_resistance_preflight_v1_summary.csv",
    "data/raw/public_void_catalog/vast_dr7_planck2018/VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt",
    "data/raw/cosmic_web/sdss_dr17_mcpm/slimeMold_galaxy_catalog_v1_0_1.fits",
    "data/source_manifest/source_page_cache/PUBLIC_VOID_CATALOG.html",
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
    policy = read_one(POLICY)
    template_summary = read_one(TEMPLATE_SUMMARY)
    if policy["status"] != "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_POLICY_FROZEN":
        raise SystemExit("unexpected R6 handoff package policy status")
    if template_summary["verdict"] != "r6_reviewer_template_ready_not_completed":
        raise SystemExit("R6 handoff package requires a blank reviewer template")
    if template_summary["review_completed"] != "false":
        raise SystemExit("R6 handoff package must not include a completed review")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("R6 handoff package must not authorize endpoint replay")

    rows = []
    for rel in PACKAGE_FILES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing R6 package file: {rel}")
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "package_path": rel,
                "byte_count": str(path.stat().st_size),
                "sha256": sha256(path),
                "contains_endpoint_data": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )

    write_csv(MANIFEST, rows)
    package_rows = rows + [
        {
            "policy_id": policy["policy_id"],
            "package_path": str(MANIFEST.relative_to(ROOT)),
            "byte_count": str(MANIFEST.stat().st_size),
            "sha256": sha256(MANIFEST),
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    OUT_ZIP.parent.mkdir(parents=True, exist_ok=True)
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
            "policy_id": policy["policy_id"],
            "status": "VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_BUILT_NOT_COMPLETED",
            "zip_path": str(OUT_ZIP.relative_to(ROOT)),
            "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
            "zip_sha256": zip_sha256,
            "package_file_count": str(len(package_rows)),
            "review_completed": "false",
            "independent_reviewer_attestation_complete": "false",
            "leakage_review_complete": "false",
            "source_unique_ready": "false",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "r6_reviewer_handoff_package_ready_not_completed",
            "recommended_next_action": "send_zip_to_independent_reviewer_and_validate_completed_response",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R6_REVIEWER_HANDOFF_PACKAGE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
