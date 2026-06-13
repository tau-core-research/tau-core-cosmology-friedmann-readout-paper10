#!/usr/bin/env python3
"""Validate the Paper11-style control-veto gate for ACT path-weight replay."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv"


def main() -> None:
    with SUMMARY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {SUMMARY}, found {len(rows)}")
    row = rows[0]
    required = {
        "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_PAPER11_CONTROL_VETO_GATE_V1",
        "status": "PAPER11_STYLE_CONTROL_VETO_GATE_BUILT_NOT_VALIDATION",
        "best_control_branch": "curl_null",
        "family_survives_controls": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "m0_or_m1_source_structure_claim_allowed": "false",
        "m2_dark_sector_inference_allowed": "false",
        "verdict": "PAPER11_CONTROL_VETO_ACT_PATH_WEIGHT_NOT_FAMILY_VERDICT_ELIGIBLE",
    }
    for key, expected in required.items():
        actual = row.get(key)
        if actual != expected:
            raise SystemExit(f"{key}: expected {expected!r}, got {actual!r}")
    if int(row["controls_better_than_candidate"]) <= 0:
        raise SystemExit("control veto requires at least one control better than candidate")
    if float(row["candidate_delta_chi2_vs_baseline"]) >= 0:
        raise SystemExit("candidate should still record weak improvement over baseline")
    if float(row["candidate_delta_chi2_vs_best_control"]) <= 0:
        raise SystemExit("candidate should lose to best control")
    if "does not by itself favor" not in row["paper11_control_veto_interpretation"]:
        raise SystemExit("missing dark-sector non-inference statement")


if __name__ == "__main__":
    main()
