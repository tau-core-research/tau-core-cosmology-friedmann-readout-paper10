#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_validation_permission_replay_authorization_review_response_template_v1.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_validation_permission_replay_authorization_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    summary = one_row(SUMMARY)
    manifest = read_rows(MANIFEST)
    template = read_rows(TEMPLATE)
    require(PACKAGE.exists(), "missing review package zip")
    require(summary["status"] == "DESI_SHAPE_VALIDATION_PERMISSION_REPLAY_AUTHORIZATION_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["zip_sha256"] == sha256(PACKAGE), "zip checksum mismatch")
    require(SHA.read_text().split()[0] == summary["zip_sha256"], "sha sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package must be blank")
    require(summary["route_margin"] == "0.01485705264", "route margin mismatch")
    require(summary["robustness_verdict"] == "positive_but_narrow_margin_and_row_sensitive_not_validation", "robustness caveat mismatch")
    require(summary["narrow_margin_caveat_retained"] == "true", "narrow-margin caveat must be retained")
    require(summary["row_sensitive_caveat_retained"] == "true", "row-sensitive caveat must be retained")
    require(summary["row2_negative_diagnostic_retained"] == "true", "Row2 caveat must be retained")
    require(summary["future_permission_only_replay_preparation_allowed"] == "true", "future replay preparation flag mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "package must not pre-authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(summary["contains_endpoint_residuals"] == "false", "package must not contain endpoint residuals")
    require(summary["contains_new_endpoint_scores"] == "false", "package must not contain new endpoint scores")
    require(summary["contains_fit_statistics"] == "false", "package must not contain fit stats")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len(template) == 4, "template must contain four questions")
    require({row["review_completed"] for row in template} == {"false"}, "template must be uncompleted")
    require({row["forbidden_inputs_used"] for row in template} == {"false"}, "template forbidden flag mismatch")
    require({row["endpoint_replay_allowed"] for row in template} == {"false"}, "template replay flag mismatch")
    require({row["endpoint_validation_claimed"] for row in template} == {"false"}, "template validation flag mismatch")
    require({row["physical_validation_claimed"] for row in template} == {"false"}, "template physical validation flag mismatch")
    require({row["claim_boundary"] for row in template} == {CLAIM_BOUNDARY}, "template claim boundary mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    require(str(MANIFEST.relative_to(ROOT)) in names, "zip must include manifest")
    for row in manifest:
        require(row["package_path"] in names, f"zip missing {row['package_path']}")
        require(row["sha256"] == sha256(ROOT / row["package_path"]), f"manifest checksum mismatch {row['package_path']}")
        require(row["contains_endpoint_residuals"] == "false", "manifest residual flag mismatch")
        require(row["contains_new_endpoint_scores"] == "false", "manifest new-score flag mismatch")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag mismatch")
        require(row["endpoint_replay_allowed"] == "false", "manifest replay flag mismatch")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag mismatch")
        require(row["physical_validation_claimed"] == "false", "manifest physical validation flag mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
    print(f"paper10_desi_shape_validation_permission_replay_authorization_review_package_v1: OK sha256={summary['zip_sha256']}")


if __name__ == "__main__":
    main()
