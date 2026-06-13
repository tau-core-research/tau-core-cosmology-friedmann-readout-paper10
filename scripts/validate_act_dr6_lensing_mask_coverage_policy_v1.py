#!/usr/bin/env python3
"""Validate the ACT DR6 mask/coverage policy."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_mask_coverage_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_mask_coverage_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_MASK_COVERAGE_POLICY_V1",
        "status": "MASK_COVERAGE_POLICY_FROZEN_SOURCE_SIDE_NOT_REPLAY",
        "source_rows": "424",
        "mask_positive_rows": "168",
        "mask_zero_rows": "256",
        "mask_positive_rule": "baseline_mask_nside4096_greater_than_zero",
        "outside_mask_policy": "assign_zero_weight_keep_rows_in_scope",
        "row_selection_policy": "no_endpoint_row_drop_or_posthoc_selection",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY_FROZEN_SOURCE_SIDE",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    if abs(float(row["active_fraction"]) - (168 / 424)) > 1e-10:
        raise SystemExit("active fraction mismatch")
    if "does not authorize dropping rows" not in row["what_this_does_not_define"]:
        raise SystemExit("missing no row-drop boundary")
    if "units, channel handoff" not in row["claim_boundary"]:
        raise SystemExit("remaining blocker boundary missing")
    for forbidden in ["posthoc_row_selection", "distance_residuals", "endpoint_score"]:
        if forbidden not in row["forbidden_inputs"].split(","):
            raise SystemExit(f"missing forbidden input {forbidden!r}")


def main() -> None:
    manifest = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    if manifest != summary:
        raise SystemExit("manifest and summary rows differ")
    validate(manifest)


if __name__ == "__main__":
    main()
