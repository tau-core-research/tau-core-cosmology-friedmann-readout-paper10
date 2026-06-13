#!/usr/bin/env python3
"""Validate the caveated ACT K_path guarded replay package."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE_ID = "ACT_DR6_LENSING_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_V1"
CLAIM_BOUNDARY = "act_dr6_lensing_caveated_kpath_guarded_replay_package_not_scoring"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_summary.csv"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_guarded_replay_package_v1_manifest.csv"


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


def main() -> None:
    summary = read_one(SUMMARY)
    rows = read_rows(MANIFEST)
    if summary["package_id"] != PACKAGE_ID:
        raise SystemExit("bad package id")
    expected = {
        "status": "GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED",
        "authorization_verdict": "ACT_CAVEATED_KPATH_REPLAY_PACKAGE_PREPARATION_ALLOWED_NOT_SCORING",
        "endpoint_replay_executed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "family_verdict_allowed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "ACT_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_READY_NOT_EXECUTED",
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {summary.get(key)!r}")
    zip_path = ROOT / summary["zip_path"]
    sidecar = ROOT / summary["zip_sha256_path"]
    if not zip_path.exists() or not sidecar.exists():
        raise SystemExit("zip or checksum sidecar missing")
    if sha256(zip_path) != summary["zip_sha256"]:
        raise SystemExit("zip checksum mismatch")
    if sidecar.read_text().strip() != f"{summary['zip_sha256']}  {zip_path.name}":
        raise SystemExit("checksum sidecar mismatch")

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected_names = {row["package_path"] for row in rows}
    expected_names.add(str(MANIFEST.relative_to(ROOT)))
    if names != expected_names:
        raise SystemExit("zip contents do not match manifest")
    for row in rows:
        path = ROOT / row["package_path"]
        if not path.exists():
            raise SystemExit(f"missing package file: {row['package_path']}")
        if sha256(path) != row["sha256"]:
            raise SystemExit(f"checksum mismatch for {row['package_path']}")
        for key in (
            "contains_endpoint_residuals",
            "contains_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_replay_executed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ):
            if row[key] != "false":
                raise SystemExit(f"{row['package_path']} must keep {key}=false")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("manifest claim boundary mismatch")
    print("ACT_CAVEATED_KPATH_GUARDED_REPLAY_PACKAGE_VALIDATED")


if __name__ == "__main__":
    main()
