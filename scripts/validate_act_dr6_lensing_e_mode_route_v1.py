#!/usr/bin/env python3
"""Validate the ACT DR6 source-side E-mode/baseline route."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_e_mode_route_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_e_mode_route_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_E_MODE_ROUTE_V1",
        "status": "E_MODE_ROUTE_DEFINED_SOURCE_SIDE_NOT_PHYSICAL_KERNEL",
        "candidate_variant": "baseline",
        "candidate_variant_role": "recommended_science_variant",
        "baseline_has_kappa_alm_modes": "true",
        "baseline_is_recommended_science_variant": "true",
        "null_control_variants_available": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_02_E_MODE_ROUTE_DEFINED_SOURCE_SIDE_BUT_NOT_PHYSICAL_KERNEL",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    if "recommended science variant" not in row["source_side_route_reason"]:
        raise SystemExit("missing source-side route reason")
    if "does not prove a physical E/B theorem" not in row["what_this_does_not_define"]:
        raise SystemExit("missing theorem-boundary statement")
    if "curl-null policy" not in row["claim_boundary"]:
        raise SystemExit("remaining blocker boundary missing")
    for forbidden in ["distance_residuals", "fit_statistics", "control_performance", "endpoint_score"]:
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
