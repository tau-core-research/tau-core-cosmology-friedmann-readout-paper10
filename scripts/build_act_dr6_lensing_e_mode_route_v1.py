#!/usr/bin/env python3
"""Define the source-side ACT DR6 E-mode/baseline candidate route."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
INVENTORY = DERIVED / "act_dr6_lensing_inventory_v1.csv"
SOURCE_OBJECT = SOURCE_MANIFEST / "act_dr6_lensing_observer_path_source_object_v1.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_e_mode_route_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_e_mode_route_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    inventory = read_rows(INVENTORY)
    source_object = read_one(SOURCE_OBJECT)
    baseline_products = [r for r in inventory if r["variant"] == "baseline"]
    curl_products = [r for r in inventory if r["variant"] == "curl"]
    diff_products = [r for r in inventory if r["variant"] == "diff_f150_f090"]
    baseline_has_kappa = any(r["product_type"] == "kappa_alm_modes" for r in baseline_products)
    baseline_is_recommended = all(r["variant_role"] == "recommended_science_variant" for r in baseline_products)
    nulls_available = bool(curl_products and diff_products)

    row = {
        "artifact_id": "ACT_DR6_LENSING_E_MODE_ROUTE_V1",
        "status": "E_MODE_ROUTE_DEFINED_SOURCE_SIDE_NOT_PHYSICAL_KERNEL",
        "source_object": source_object["artifact_id"],
        "candidate_variant": "baseline",
        "candidate_variant_role": "recommended_science_variant",
        "candidate_observable": "baseline_kappa_alm_modes_sampled_as_convergence_reconstruction",
        "source_side_route_reason": (
            "the ACT DR6 inventory labels baseline as the recommended science variant and "
            "provides baseline kappa alm modes plus baseline mask support"
        ),
        "e_mode_interpretation_level": "source_product_label_and_convergence_route_only",
        "baseline_has_kappa_alm_modes": str(baseline_has_kappa).lower(),
        "baseline_products_count": str(len(baseline_products)),
        "baseline_is_recommended_science_variant": str(baseline_is_recommended).lower(),
        "null_control_variants_available": str(nulls_available).lower(),
        "required_null_controls": "curl;diff_f150_f090;diff_f150_f090_tonly",
        "what_this_defines": "source-side candidate route from ACT baseline convergence reconstruction to a possible K_path input",
        "what_this_does_not_define": (
            "does not prove a physical E/B theorem; does not prove gauge descent; "
            "does not define metric/lensing path integral units; does not authorize replay"
        ),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "distance_residuals,fit_statistics,control_performance,family_winner,endpoint_score",
        "claim_boundary": (
            "satisfies ACT_REOPEN_02 only at source-route level; curl-null policy, "
            "normalization, channel handoff, and control suite remain active blockers"
        ),
        "verdict": "ACT_REOPEN_02_E_MODE_ROUTE_DEFINED_SOURCE_SIDE_BUT_NOT_PHYSICAL_KERNEL",
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
