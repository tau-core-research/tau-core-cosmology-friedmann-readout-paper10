#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_policy_v1.csv"
TEMPLATE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv"
OUT_ZIP = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip"
OUT_ZIP_SHA256 = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1.zip.sha256"
MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv"


PACKAGE_FILES = [
    "REVIEWER_README_KIDS1000_PHOTOZ_HANDOFF.md",
    "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.csv",
    "data/derived/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1_summary.csv",
    "docs/kids1000_cosebis_external_photoz_calibration_reviewer_attestation_template_v1.md",
    "docs/kids1000_cosebis_external_photoz_calibration_external_reviewer_instructions_v1.md",
    "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.csv",
    "data/derived/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1_summary.csv",
    "docs/kids1000_cosebis_external_photoz_calibration_leakage_review_preflight_v1.md",
    "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv",
    "data/derived/kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv",
    "docs/kids1000_cosebis_external_photoz_calibration_source_manifest_v1.md",
    "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_PHOTOZ_CALIBRATION_AANDA.html",
    "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_PHOTOZ_CALIBRATION_ARXIV.html",
    "data/source_manifest/source_page_cache/kids1000_photoz_calibration_v1/KIDS1000_SOM_GOLD_CATALOGUE.html",
    "data/source_manifest/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_policy_v1.csv",
    "docs/kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.md",
    "scripts/validate_kids1000_cosebis_external_photoz_calibration_completed_reviewer_response_v1.py",
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
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_POLICY_FROZEN":
        raise SystemExit("unexpected reviewer handoff package policy status")
    if template_summary["verdict"] != "reviewer_attestation_template_ready_not_completed":
        raise SystemExit("handoff package requires a blank reviewer attestation template")
    if template_summary["review_completed"] != "false":
        raise SystemExit("handoff package must not include a completed review")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("handoff package must not authorize endpoint replay")

    rows = []
    for rel in PACKAGE_FILES:
        path = ROOT / rel
        if not path.exists():
            raise SystemExit(f"missing handoff package file: {rel}")
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
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_BUILT_NOT_COMPLETED",
            "zip_path": str(OUT_ZIP.relative_to(ROOT)),
            "zip_sha256_path": str(OUT_ZIP_SHA256.relative_to(ROOT)),
            "zip_sha256": zip_sha256,
            "package_file_count": str(len(package_rows)),
            "review_completed": "false",
            "independent_reviewer_attestation_complete": "false",
            "r4_leakage_review_complete": "false",
            "h1_independent_evidence_complete": "false",
            "computes_new_scores": "false",
            "contains_endpoint_data": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "reviewer_handoff_package_ready_not_completed",
            "recommended_next_action": "send_zip_to_independent_reviewer_and_validate_completed_response",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
