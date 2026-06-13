#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip"
SHA = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_package_v1.zip.sha256"
MANIFEST = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_package_v1_manifest.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_response_template_v1.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_promotion_review_not_replay_not_validation"


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
    require(PACKAGE.exists(), "missing promotion review package zip")
    require(summary["status"] == "DESI_SHAPE_ROW2_PROMOTION_REVIEW_PACKAGE_BUILT_NOT_COMPLETED", "bad status")
    require(summary["zip_sha256"] == sha256(PACKAGE), "zip checksum mismatch")
    require(SHA.read_text().split()[0] == summary["zip_sha256"], "sha sidecar mismatch")
    require(summary["package_file_count"] == str(len(manifest) + 1), "package file count mismatch")
    require(summary["review_completed"] == "false", "package must be uncompleted")
    require(summary["moresco_caveat_reduced"] == "true", "Moresco caveat must be reduced")
    require(summary["source_native_shape_caveat_reduced"] == "true", "source-native shape caveat must be reduced")
    require(summary["row2_source_caveat_reduced"] == "true", "combined caveat must be reduced")
    require(summary["endpoint_pair_independence_satisfied"] == "false", "endpoint-pair independence must remain false")
    require(summary["row2_promotion_ready"] == "false", "package must not mark Row2 promotion-ready")
    require(summary["shape_route_promotion_allowed"] == "false", "package must not allow promotion")
    require(summary["endpoint_replay_allowed"] == "false", "package must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "package must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "package must not claim physical validation")
    require(summary["contains_endpoint_residuals"] == "false", "package must not contain residuals")
    require(summary["contains_endpoint_scores"] == "false", "package must not contain scores")
    require(summary["contains_fit_statistics"] == "false", "package must not contain fit stats")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len(template) == 4, "template must contain four questions")
    require({row["review_completed"] for row in template} == {"false"}, "template must be blank")
    require({row["forbidden_inputs_used"] for row in template} == {"false"}, "template forbidden flag mismatch")
    require({row["endpoint_replay_allowed"] for row in template} == {"false"}, "template replay flag mismatch")
    require({row["endpoint_validation_claimed"] for row in template} == {"false"}, "template validation flag mismatch")
    require({row["physical_validation_claimed"] for row in template} == {"false"}, "template physical validation mismatch")
    require({row["claim_boundary"] for row in template} == {CLAIM_BOUNDARY}, "template claim boundary mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    require(MANIFEST.relative_to(ROOT).as_posix() in names, "zip must include manifest")
    for row in manifest:
        path = ROOT / row["package_path"]
        require(row["package_path"] in names, f"zip missing {row['package_path']}")
        require(row["sha256"] == sha256(path), f"manifest checksum mismatch: {row['package_path']}")
        require(row["contains_endpoint_residuals"] == "false", "manifest residual flag mismatch")
        require(row["contains_endpoint_scores"] == "false", "manifest score flag mismatch")
        require(row["contains_fit_statistics"] == "false", "manifest fit flag mismatch")
        require(row["endpoint_replay_allowed"] == "false", "manifest replay flag mismatch")
        require(row["endpoint_validation_claimed"] == "false", "manifest validation flag mismatch")
        require(row["physical_validation_claimed"] == "false", "manifest physical validation flag mismatch")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "manifest claim boundary mismatch")
    print(f"PAPER10_DESI_SHAPE_ROW2_PROMOTION_REVIEW_PACKAGE_VALIDATED sha256={summary['zip_sha256']}")


if __name__ == "__main__":
    main()
