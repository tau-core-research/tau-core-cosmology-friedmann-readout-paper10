#!/usr/bin/env python3
"""Freeze the ACT DR6 curl-null policy for the path-weight branch."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
INVENTORY = DERIVED / "act_dr6_lensing_inventory_v1.csv"
CONTROL_DIAGNOSTIC = DERIVED / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_curl_null_policy_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_curl_null_policy_v1_summary.csv"


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
    diagnostic = read_one(CONTROL_DIAGNOSTIC)
    curl_products = [r for r in inventory if r["variant"] == "curl"]
    diff_products = [r for r in inventory if r["variant"] == "diff_f150_f090"]
    curl_available = bool(curl_products)
    curl_is_null = all(r["variant_role"] == "null_control_variant" for r in curl_products)
    diff_available = bool(diff_products)
    curl_dominates = diagnostic["best_control_branch"] == "curl_null"

    row = {
        "artifact_id": "ACT_DR6_LENSING_CURL_NULL_POLICY_V1",
        "status": "CURL_NULL_POLICY_FROZEN_SOURCE_SIDE_NOT_THEOREM",
        "candidate_route": "ACT_DR6_LENSING_E_MODE_ROUTE_V1",
        "curl_variant_available": str(curl_available).lower(),
        "curl_inventory_role": "null_control_variant",
        "curl_role_source": "ACT_DR6 inventory variant_role",
        "curl_is_predeclared_null_control": str(curl_is_null).lower(),
        "frequency_difference_null_available": str(diff_available).lower(),
        "policy_statement": (
            "curl is treated as a source-native null/control branch for the ACT path-weight "
            "candidate; it is not promoted to a positive Tau path channel in this paper"
        ),
        "veto_rule": (
            "if curl_null scores better than the baseline candidate under the frozen replay, "
            "the ACT source basis is control-dominated and cannot support a family verdict"
        ),
        "observed_control_status": "curl_null_best_control" if curl_dominates else "curl_null_not_best_control",
        "controls_better_than_candidate": diagnostic["controls_better_than_candidate"],
        "candidate_delta_chi2_vs_best_control": diagnostic["candidate_delta_chi2_vs_best_control"],
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "curl_as_positive_channel_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "endpoint_score_driven_policy_change,residual_shape,family_winner,posthoc_control_relabeling",
        "claim_boundary": (
            "freezes protocol treatment of curl as a null/control veto branch; does not prove "
            "operator-level curl quotient triviality or physical E/B gauge descent"
        ),
        "verdict": (
            "ACT_REOPEN_03_CURL_NULL_POLICY_FROZEN_AND_CURRENT_BRANCH_VETOED"
            if curl_dominates
            else "ACT_REOPEN_03_CURL_NULL_POLICY_FROZEN_NO_CURRENT_CURL_VETO"
        ),
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
