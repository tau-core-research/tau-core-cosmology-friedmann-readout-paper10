#!/usr/bin/env python3
"""Validate the ACT DR6 curl-null policy."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_curl_null_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_curl_null_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_CURL_NULL_POLICY_V1",
        "status": "CURL_NULL_POLICY_FROZEN_SOURCE_SIDE_NOT_THEOREM",
        "curl_variant_available": "true",
        "curl_inventory_role": "null_control_variant",
        "curl_is_predeclared_null_control": "true",
        "observed_control_status": "curl_null_best_control",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "curl_as_positive_channel_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_03_CURL_NULL_POLICY_FROZEN_AND_CURRENT_BRANCH_VETOED",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    if "not promoted to a positive Tau path channel" not in row["policy_statement"]:
        raise SystemExit("missing no-positive-channel policy")
    if "cannot support a family verdict" not in row["veto_rule"]:
        raise SystemExit("missing family-veto rule")
    if "does not prove operator-level curl quotient triviality" not in row["claim_boundary"]:
        raise SystemExit("missing theorem-boundary statement")
    if float(row["candidate_delta_chi2_vs_best_control"]) <= 0:
        raise SystemExit("current candidate should lose to best control")


def main() -> None:
    manifest = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    if manifest != summary:
        raise SystemExit("manifest and summary rows differ")
    validate(manifest)


if __name__ == "__main__":
    main()
