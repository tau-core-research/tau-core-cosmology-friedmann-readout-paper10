#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_eligibility_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_eligibility_gate_v1_summary.csv"


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
    ledger = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    if policy["status"] != "LOG_BAND_PRIOR_ELIGIBILITY_GATE_FROZEN":
        raise SystemExit("unexpected eligibility policy status")
    if policy["uses_kids_data_vector_values"] != "false" or policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("eligibility policy must remain data-vector-free and non-scoring")
    if summary["status"] != "LOG_BAND_PRIOR_ELIGIBILITY_GATE_PARTIAL_PASS":
        raise SystemExit("unexpected eligibility summary status")
    if summary["eligibility_verdict"] != "protocol_eligible_for_conditional_envelope_but_not_full_kernel_validated":
        raise SystemExit("unexpected eligibility verdict")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("eligibility gate must not claim validation")
    if len(ledger) != 6 or summary["conditions"] != "6":
        raise SystemExit("eligibility ledger row count mismatch")
    statuses = [row["status"] for row in ledger]
    if statuses.count("OPEN_BLOCKER") != 1:
        raise SystemExit("eligibility gate must preserve one full-kernel blocker")
    if statuses.count("ASSUMPTION_NOT_SOURCE_PROVEN") != 1:
        raise SystemExit("eligibility gate must expose one unproven smoothness assumption")
    if statuses.count("PASS") != 3 or statuses.count("PASS_AS_PROTOCOL_GUARDRAIL") != 1:
        raise SystemExit("unexpected eligibility pass structure")
    if {row["condition_id"] for row in ledger} != {
        "C1_ordered_dimensionless_mode_domain",
        "C2_no_posthoc_mode_cut",
        "C3_source_side_path_mapping_exists",
        "C4_smooth_coherent_path_residual",
        "C5_no_high_frequency_only_source_claim",
        "C6_covariant_or_survey_native_kernel",
    }:
        raise SystemExit("unexpected eligibility condition set")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_LOG_BAND_PRIOR_ELIGIBILITY_GATE_V1_VALIDATED "
        f"verdict={summary['eligibility_verdict']}"
    )


if __name__ == "__main__":
    main()
