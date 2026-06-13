#!/usr/bin/env python3
"""Validate the caveated ACT DR6 K_path source-side design."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "source_manifest" / "act_dr6_lensing_caveated_kpath_source_design_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(DESIGN)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 5:
        raise SystemExit(f"expected five caveated K_path design rows, found {len(rows)}")
    if len(summary_rows) != 1:
        raise SystemExit(f"expected one summary row, found {len(summary_rows)}")

    expected_items = {
        "CKPATH_01_SOURCE_PRODUCT",
        "CKPATH_02_PROXY_MAPPING",
        "CKPATH_03_NULL_QUOTIENT_RULE",
        "CKPATH_04_COVERAGE_SCOPE",
        "CKPATH_05_REPLAY_PRECONDITIONS",
    }
    if {row["design_item_id"] for row in rows} != expected_items:
        raise SystemExit("unexpected caveated K_path design item set")
    if any(row["endpoint_replay_allowed"] != "false" for row in rows):
        raise SystemExit("source design rows must not authorize endpoint replay")
    if any(row["endpoint_validation_claimed"] != "false" for row in rows):
        raise SystemExit("source design rows must not claim validation")
    if any(row["physical_path_weight_claimed"] != "false" for row in rows):
        raise SystemExit("source design rows must not claim physical path-weight derivation")
    if any("endpoint" not in row["forbidden_inputs"] for row in rows):
        raise SystemExit("each design row must include endpoint-side forbidden inputs")

    summary = summary_rows[0]
    expected_summary = {
        "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
        "status": "CAVEATED_KPATH_SOURCE_DESIGN_READY_FOR_EXTERNAL_REVIEW_NOT_REPLAY",
        "closure_verdict": "ACT_REOPEN_CLOSED_CURRENT_BRANCH_QUARANTINED_NOT_VALIDATION",
        "scaffold_verdict": "ACT_NEXT_SOURCE_BASIS_DESIGN_SCAFFOLD_FROZEN_NOT_REPLAY",
        "mapping_status": "dimensionless_shape_proxy_only",
        "physical_lensing_path_weight_claimed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "dark_sector_inference_allowed": "false",
        "external_review_required_before_replay": "true",
        "verdict": "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_READY_NOT_REPLAY",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            raise SystemExit(f"{key}: expected {expected!r}, got {summary.get(key)!r}")
    if "drop_curl_control" not in summary["forbidden_action"]:
        raise SystemExit("summary must forbid dropping the curl control")
    if "does not reopen endpoint scoring" not in summary["claim_boundary"]:
        raise SystemExit("claim boundary must block endpoint scoring")
    if "curl_null" not in summary["control_suite_required"]:
        raise SystemExit("control suite must retain curl_null")


if __name__ == "__main__":
    main()
