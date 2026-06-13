#!/usr/bin/env python3
"""Freeze the ACT DR6 units/normalization policy for the path-weight branch."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
CANDIDATE = DERIVED / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_units_normalization_policy_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_units_normalization_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    candidate = read_one(CANDIDATE)
    row = {
        "artifact_id": "ACT_DR6_LENSING_UNITS_NORMALIZATION_POLICY_V1",
        "status": "UNITLESS_PROXY_NORMALIZATION_FROZEN_PHYSICAL_NORMALIZATION_MISSING",
        "current_normalization_rule": candidate["normalization_rule"],
        "normalization_domain": "mask_positive_rows_only",
        "source_rows": candidate["source_rows"],
        "mask_positive_rows": candidate["mask_positive_rows"],
        "mask_zero_rows": candidate["mask_zero_rows"],
        "baseline_center_median": candidate["baseline_center_median"],
        "baseline_scale_mad14826": candidate["baseline_scale_mad14826"],
        "curl_center_median": candidate["curl_center_median"],
        "curl_scale_mad14826": candidate["curl_scale_mad14826"],
        "diff_f150_f090_center_median": candidate["diff_f150_f090_center_median"],
        "diff_f150_f090_scale_mad14826": candidate["diff_f150_f090_scale_mad14826"],
        "current_units_status": "dimensionless_standardized_proxy",
        "physical_units_available": "false",
        "physical_normalization_allowed_now": "false",
        "proxy_normalization_allowed_for_source_diagnostics": "true",
        "required_for_physical_reopen": (
            "source-native convergence-to-path response units or theorem-bounded mapping "
            "from ACT kappa samples to K_path amplitude"
        ),
        "what_this_defines": (
            "the current median/MAD normalization is a deterministic source-side proxy "
            "normalization over mask-positive rows"
        ),
        "what_this_does_not_define": (
            "does not define physical path-weight units; does not define response amplitude; "
            "does not allow endpoint amplitude tuning"
        ),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "endpoint_score,best_fit_amplitude,distance_residuals,fit_statistics,family_winner",
        "claim_boundary": (
            "freezes the unitless proxy normalization and keeps physical normalization as an "
            "open blocker for endpoint or family-verdict use"
        ),
        "verdict": "ACT_REOPEN_05_UNITS_NORMALIZATION_PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN",
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
