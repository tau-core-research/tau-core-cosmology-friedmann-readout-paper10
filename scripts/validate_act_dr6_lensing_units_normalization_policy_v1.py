#!/usr/bin/env python3
"""Validate the ACT DR6 units/normalization policy."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_units_normalization_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_units_normalization_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_UNITS_NORMALIZATION_POLICY_V1",
        "status": "UNITLESS_PROXY_NORMALIZATION_FROZEN_PHYSICAL_NORMALIZATION_MISSING",
        "current_normalization_rule": "mask_positive_only_median_center_mad_scale_else_zero",
        "normalization_domain": "mask_positive_rows_only",
        "source_rows": "424",
        "mask_positive_rows": "168",
        "mask_zero_rows": "256",
        "current_units_status": "dimensionless_standardized_proxy",
        "physical_units_available": "false",
        "physical_normalization_allowed_now": "false",
        "proxy_normalization_allowed_for_source_diagnostics": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_05_UNITS_NORMALIZATION_PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    if "theorem-bounded mapping" not in row["required_for_physical_reopen"]:
        raise SystemExit("missing theorem-bounded reopen requirement")
    if "does not define physical path-weight units" not in row["what_this_does_not_define"]:
        raise SystemExit("missing physical-units nonclaim")
    if "physical normalization as an open blocker" not in row["claim_boundary"]:
        raise SystemExit("missing blocker boundary")
    for forbidden in ["endpoint_score", "best_fit_amplitude", "distance_residuals"]:
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
