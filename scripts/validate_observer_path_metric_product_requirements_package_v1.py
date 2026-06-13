#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/observer_path_metric_product_requirements_review_response_template_v1.csv"
INSTRUCTIONS = ROOT / "docs/observer_path_metric_product_requirements_reviewer_instructions_v1.md"
PACKAGE = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1.zip"
MANIFEST = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1_manifest.csv"
SHA = ROOT / "data/derived/observer_path_metric_product_requirements_package_v1.zip.sha256"
CLAIM_BOUNDARY = "observer_path_metric_product_requirements_not_endpoint_not_validation"
EXPECTED_QUESTIONS = {
    "Q1_product_specificity",
    "Q2_source_alignment",
    "Q3_leakage_barrier",
    "Q4_replay_boundary",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    summary = read_one(SUMMARY)
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("requirements package must not authorize replay")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("requirements package must not claim validation")
    if summary["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("requirements package must not claim physical path weight")
    if summary["metric_path_source_aligned_numeric_count"] != "0":
        raise SystemExit("requirements package should preserve current metric count blocker")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")

    template_rows = read_rows(TEMPLATE)
    if {row["question_id"] for row in template_rows} != EXPECTED_QUESTIONS:
        raise SystemExit("review template question set mismatch")
    for row in template_rows:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit(f"{row['question_id']} must not allow replay")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit(f"{row['question_id']} must not claim validation")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']} claim boundary mismatch")

    manifest_rows = read_rows(MANIFEST)
    if not manifest_rows:
        raise SystemExit("package manifest empty")
    if {row["claim_boundary"] for row in manifest_rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("manifest claim boundary mismatch")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    expected_names = {row["path"] for row in manifest_rows}
    if names != expected_names:
        raise SystemExit("zip contents do not match manifest")
    if not SHA.exists() or PACKAGE.name not in SHA.read_text():
        raise SystemExit("sha file missing package name")
    text = INSTRUCTIONS.read_text()
    for marker in [
        "You do not need repository access",
        "endpoint_replay_allowed=false",
        "ACCEPT_REQUIREMENTS_ONLY",
        CLAIM_BOUNDARY,
    ]:
        if marker not in text:
            raise SystemExit(f"reviewer instructions missing marker: {marker}")

    print(
        "OBSERVER_PATH_METRIC_PRODUCT_REQUIREMENTS_PACKAGE_V1_VALIDATED "
        f"questions={len(template_rows)} metric_count={summary['metric_path_source_aligned_numeric_count']}"
    )


if __name__ == "__main__":
    main()
