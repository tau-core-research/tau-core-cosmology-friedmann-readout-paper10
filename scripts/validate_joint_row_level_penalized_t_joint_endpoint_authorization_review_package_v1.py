#!/usr/bin/env python3
"""Validate the consolidated row-level penalized endpoint authorization package."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE_ID = "joint_row_level_penalized_t_joint_endpoint_authorization_review_package_v1"

SUMMARY = DERIVED / f"{PACKAGE_ID}_summary.csv"
MANIFEST = DERIVED / f"{PACKAGE_ID}_manifest.csv"
ZIP = DERIVED / f"{PACKAGE_ID}.zip"
SHA = DERIVED / f"{PACKAGE_ID}.zip.sha256"
LOG = DERIVED / f"{PACKAGE_ID}_validation_log.txt"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    for path in [SUMMARY, MANIFEST, ZIP, SHA]:
        require(path.exists(), f"Missing required artifact: {path}", errors)
    if errors:
        LOG.write_text("\n".join(errors) + "\n", encoding="utf-8")
        raise SystemExit("\n".join(errors))

    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "Summary must contain exactly one row.", errors)
    summary = summary_rows[0] if summary_rows else {}

    for key in [
        "review_completed",
        "penalized_t_joint_ledger_authorized",
        "endpoint_scoring_authorized",
        "endpoint_scoring_run",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
    ]:
        require(summary.get(key) == "false", f"Summary flag {key} must be false.", errors)

    require(
        summary.get("verdict")
        == "CONSOLIDATED_ENDPOINT_AUTHORIZATION_PACKAGE_READY_NOT_COMPLETED_NOT_SCORING",
        "Unexpected summary verdict.",
        errors,
    )

    manifest_rows = read_rows(MANIFEST)
    require(len(manifest_rows) >= 8, "Manifest should include policy/template/summary plus upstream ledgers.", errors)
    for idx, row in enumerate(manifest_rows, start=1):
        require(row.get("contains_endpoint_scores") == "false", f"Manifest row {idx} marks endpoint scores.", errors)
        require(
            row.get("contains_endpoint_residuals") == "false",
            f"Manifest row {idx} marks endpoint residuals.",
            errors,
        )
        require(row.get("contains_fit_statistics") == "false", f"Manifest row {idx} marks fit statistics.", errors)
        path = ROOT / row.get("path", "")
        require(path.exists(), f"Manifest path missing: {path}", errors)
        if path.exists():
            require(row.get("sha256") == sha256(path), f"SHA mismatch for {path}", errors)

    expected_sha = SHA.read_text(encoding="utf-8").split()[0]
    actual_sha = sha256(ZIP)
    require(expected_sha == actual_sha, "Zip SHA sidecar mismatch.", errors)

    with zipfile.ZipFile(ZIP, "r") as archive:
        names = set(archive.namelist())
    for row in manifest_rows:
        require(row.get("path", "") in names, f"Manifest file not present in zip: {row.get('path')}", errors)
    require(f"docs/{PACKAGE_ID}.md" in names, "Reviewer note doc missing from zip.", errors)

    if errors:
        LOG.write_text("FAILED\n" + "\n".join(errors) + "\n", encoding="utf-8")
        raise SystemExit("\n".join(errors))

    LOG.write_text(
        "PASSED\n"
        "Consolidated authorization package is ready, not completed, not scoring, and not validation.\n",
        encoding="utf-8",
    )
    print("PASSED")
    print(ZIP)


if __name__ == "__main__":
    main()
