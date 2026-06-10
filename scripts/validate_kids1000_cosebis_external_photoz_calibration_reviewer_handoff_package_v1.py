#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_policy_v1.csv"
MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_manifest.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_reviewer_handoff_package_v1_summary.csv"


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


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)
    zip_path = ROOT / summary["zip_path"]
    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_POLICY_FROZEN":
        raise SystemExit("unexpected reviewer handoff package policy status")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("unexpected reviewer handoff package summary status")
    if not zip_path.exists():
        raise SystemExit("missing handoff package zip")
    if sha256(zip_path) != summary["zip_sha256"]:
        raise SystemExit("handoff package zip checksum mismatch")
    if summary["package_file_count"] != "16":
        raise SystemExit("expected 16 files in reviewer handoff package")
    for key in [
        "review_completed",
        "independent_reviewer_attestation_complete",
        "r4_leakage_review_complete",
        "h1_independent_evidence_complete",
        "computes_new_scores",
        "contains_endpoint_data",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["verdict"] != "reviewer_handoff_package_ready_not_completed":
        raise SystemExit("unexpected reviewer handoff package verdict")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected = {row["package_path"] for row in rows}
    expected.add(str(MANIFEST.relative_to(ROOT)))
    if names != expected:
        raise SystemExit("handoff package contents do not match manifest")
    for row in rows:
        path = ROOT / row["package_path"]
        if not path.exists():
            raise SystemExit(f"missing manifest file: {row['package_path']}")
        if sha256(path) != row["sha256"]:
            raise SystemExit(f"checksum mismatch for {row['package_path']}")
        if row["contains_endpoint_data"] != "false":
            raise SystemExit("handoff package rows must not contain endpoint data")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("handoff package rows must not authorize replay or validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_REVIEWER_HANDOFF_PACKAGE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
