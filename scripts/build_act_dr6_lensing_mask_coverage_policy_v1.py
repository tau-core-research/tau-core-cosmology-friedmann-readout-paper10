#!/usr/bin/env python3
"""Freeze the ACT DR6 mask and coverage policy for the path-weight branch."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
PILOT = DERIVED / "act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv"
CANDIDATE = DERIVED / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_mask_coverage_policy_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_mask_coverage_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    pilot = read_one(PILOT)
    candidate = read_one(CANDIDATE)
    source_rows = int(pilot["source_rows"])
    mask_positive = int(pilot["mask_positive_count"])
    mask_zero = int(pilot["mask_zero_count"])
    active_fraction = mask_positive / source_rows if source_rows else 0.0

    row = {
        "artifact_id": "ACT_DR6_LENSING_MASK_COVERAGE_POLICY_V1",
        "status": "MASK_COVERAGE_POLICY_FROZEN_SOURCE_SIDE_NOT_REPLAY",
        "source_scope": "predeclared_low_z_pantheon_sky_positions",
        "source_rows": str(source_rows),
        "mask_positive_rows": str(mask_positive),
        "mask_zero_rows": str(mask_zero),
        "active_fraction": f"{active_fraction:.12g}",
        "mask_positive_rule": "baseline_mask_nside4096_greater_than_zero",
        "active_row_policy": "use_mask_positive_rows_for_source_side_center_scale_only",
        "outside_mask_policy": "assign_zero_weight_keep_rows_in_scope",
        "row_selection_policy": "no_endpoint_row_drop_or_posthoc_selection",
        "normalization_rule": candidate["normalization_rule"],
        "coverage_claim": "partial_act_coverage_only_not_population_complete_path_kernel",
        "what_this_defines": (
            "coverage accounting and deterministic outside-mask behavior for the ACT source object"
        ),
        "what_this_does_not_define": (
            "does not convert outside-mask rows into missing endpoint data; does not authorize "
            "dropping rows from scoring; does not define physical path weight"
        ),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "distance_residuals,fit_statistics,posthoc_row_selection,endpoint_score,family_winner",
        "claim_boundary": (
            "freezes ACT coverage policy for source-side reopening only; units, channel handoff, "
            "and full control suite remain active blockers"
        ),
        "verdict": "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY_FROZEN_SOURCE_SIDE",
    }

    SOURCE_MANIFEST.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    for path in (OUT, SUMMARY_OUT):
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row))
            writer.writeheader()
            writer.writerow(row)


if __name__ == "__main__":
    main()
