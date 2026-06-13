#!/usr/bin/env python3
"""Define the ACT DR6 observer/path source object, without scoring it."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
PRODUCT = SOURCE_MANIFEST / "act_dr6_lensing_product_v1.csv"
PILOT = DERIVED / "act_dr6_lensing_low_z_sampling_pilot_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_observer_path_source_object_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_observer_path_source_object_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    product = read_one(PRODUCT)
    pilot = read_one(PILOT)

    row = {
        "artifact_id": "ACT_DR6_LENSING_OBSERVER_PATH_SOURCE_OBJECT_V1",
        "status": "SOURCE_OBJECT_DEFINED_SOURCE_SIDE_NOT_ENDPOINT",
        "provider": product["provider"],
        "source_product": product["product_name"],
        "source_product_sha256": product["sha256"],
        "source_product_type": product["source_product_type"],
        "coordinate_frame": "equatorial_sky_position",
        "source_domain": "low_z_pantheon_sky_positions_with_act_mask_support",
        "source_rows": pilot["source_rows"],
        "active_mask_positive_rows": pilot["mask_positive_count"],
        "inactive_mask_zero_rows": pilot["mask_zero_count"],
        "observable_bundle": "act_dr6_baseline_kappa_alm;act_dr6_curl_null_alm;act_dr6_diff_f150_f090_null_alm;act_dr6_baseline_mask",
        "source_object_definition": (
            "a source-side observer/path lensing environment object consisting of ACT DR6 "
            "convergence reconstruction samples, ACT null-control samples, and ACT mask "
            "coverage sampled at predeclared low-z Pantheon sky positions"
        ),
        "what_it_is_not": (
            "not a metric/lensing path integral; not a physical K_path kernel; not an "
            "endpoint score; not a dark-sector decision object"
        ),
        "allowed_use_before_reopen": (
            "source-side provenance, coverage accounting, null-control definition, "
            "and source-basis freeze inputs"
        ),
        "disallowed_use_before_reopen": (
            "endpoint replay, validation, family verdict, physical lensing path-weight claim, "
            "dark-sector inference"
        ),
        "primary_channel_candidate": "K_path_observer_path_candidate",
        "channel_handoff_status": "candidate_only_requires_separate_channel_handoff_gate",
        "null_control_policy_status": "declared_but_not_theorem_frozen",
        "units_and_normalization_status": "unitless_proxy_only_not_physical_normalization",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "distance_residuals,fit_statistics,family_winner,endpoint_score,control_performance",
        "claim_boundary": (
            "defines the source object needed for ACT_REOPEN_01 only; it does not reopen "
            "ACT replay without the remaining source-basis requirements"
        ),
        "verdict": "ACT_REOPEN_01_SOURCE_OBJECT_DEFINED_BUT_REPLAY_STILL_DISABLED",
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
