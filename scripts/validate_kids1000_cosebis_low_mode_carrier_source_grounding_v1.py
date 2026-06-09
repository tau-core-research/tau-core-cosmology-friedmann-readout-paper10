#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_low_mode_carrier_source_grounding_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_carrier_source_grounding_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_low_mode_carrier_source_grounding_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    if policy["status"] != "LOW_MODE_CARRIER_SOURCE_GROUNDING_POLICY_FROZEN":
        raise SystemExit("unexpected low-mode source-grounding policy status")
    if policy["uses_kids_data_vector_values_for_grounding"] != "false":
        raise SystemExit("policy must not use KiDS data-vector values for grounding")
    if policy["allows_endpoint_validation_claim"] != "false":
        raise SystemExit("policy must forbid endpoint validation claims")
    if summary["status"] != "LOW_MODE_CARRIER_SOURCE_GROUNDING_PARTIAL_COMPLETE":
        raise SystemExit("unexpected low-mode source-grounding summary status")
    if summary["source_grounding_verdict"] != "partial_protocol_grounding_with_open_first_principles_derivation_blocker":
        raise SystemExit("unexpected source-grounding verdict")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("source-grounding summary must not claim validation")
    if summary["uses_kids_data_vector_values_for_grounding"] != "false":
        raise SystemExit("source-grounding summary must not use scoring data for grounding")
    if len(rows) != 6 or summary["ledger_rows"] != "6":
        raise SystemExit("source-grounding ledger row count mismatch")
    statuses = [row["criterion_status"] for row in rows]
    if statuses.count("OPEN_BLOCKER") != 1:
        raise SystemExit("source-grounding ledger must preserve one open derivation blocker")
    if statuses.count("SUPPORTING_DIAGNOSTIC") != 2:
        raise SystemExit("source-grounding ledger must distinguish post-score diagnostics")
    if statuses.count("PASS") != 2 or statuses.count("PARTIAL_PASS") != 1:
        raise SystemExit("unexpected source-grounding pass structure")
    required_criteria = {
        "source_independence",
        "coherent_path_readout_prior",
        "no_posthoc_mode_cut",
        "diagnostic_consistency_with_mode_localization",
        "mode_shape_stress_support",
        "missing_first_principles_mode_kernel_derivation",
    }
    if {row["criterion_id"] for row in rows} != required_criteria:
        raise SystemExit("unexpected source-grounding criteria")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_LOW_MODE_CARRIER_SOURCE_GROUNDING_V1_VALIDATED "
        f"verdict={summary['source_grounding_verdict']}"
    )


if __name__ == "__main__":
    main()
