#!/usr/bin/env python3
"""Validate the ACT caveated K_path source-design review package."""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
PACKAGE = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1.zip"
MANIFEST = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1_manifest.csv"
SUMMARY = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_package_v1_summary.csv"
TEMPLATE = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_review_response_template_v1.csv"


REQUIRED_IN_ZIP = {
    "data/source_manifest/act_dr6_lensing_caveated_kpath_source_design_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv",
    "data/source_manifest/act_dr6_lensing_next_source_basis_design_scaffold_v1.csv",
    "data/derived/act_dr6_lensing_reopen_closure_ledger_v1_summary.csv",
    "data/derived/act_dr6_lensing_path_weight_authorized_replay_v1_summary.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_response_template_v1.csv",
    "data/derived/act_dr6_lensing_caveated_kpath_source_design_review_instructions_v1.md",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if not PACKAGE.exists():
        raise SystemExit("review package zip missing")
    with zipfile.ZipFile(PACKAGE) as zf:
        names = set(zf.namelist())
    missing = REQUIRED_IN_ZIP - names
    if missing:
        raise SystemExit(f"review package missing files: {sorted(missing)}")

    manifest_rows = read_rows(MANIFEST)
    summary_rows = read_rows(SUMMARY)
    template_rows = read_rows(TEMPLATE)
    if len(manifest_rows) < len(REQUIRED_IN_ZIP):
        raise SystemExit("manifest has too few rows")
    if len(summary_rows) != 1:
        raise SystemExit("expected one package summary row")
    if {row["review_item"] for row in template_rows} != {
        "source_product_status",
        "proxy_mapping_status",
        "null_control_status",
        "leakage_status",
        "overall_verdict",
    }:
        raise SystemExit("unexpected response template rows")

    summary = summary_rows[0]
    expected = {
        "package_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_V1",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "verdict": "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_PACKAGE_READY",
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {summary.get(key)!r}")
    if "not_replay_authorization" not in summary["claim_boundary"]:
        raise SystemExit("claim boundary must say not replay authorization")


if __name__ == "__main__":
    main()
