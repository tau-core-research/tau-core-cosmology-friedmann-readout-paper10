#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_validation_readiness_ledger_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_validation_readiness_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_validation_readiness_ledger_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(policy["status"] == "VALIDATION_READINESS_LEDGER_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "VALIDATION_READINESS_LEDGER_BUILT_NOT_VALIDATION", "unexpected summary status")
    require(summary["ledger_rows"] == "5", "expected five readiness rows")
    require(summary["low_tail_endpoint_signal_present"] == "true", "low-tail signal should be present")
    require(summary["tomographic_controls_refute_endpoint_signal"] == "false", "controls must not refute signal")
    require(summary["tomographic_control_concern_reduced"] == "true", "tomographic concern should be reduced")
    require(summary["source_bin_holdout_signal_survives"] == "true", "source-bin holdout should preserve signal")
    require(summary["candidate_holdout_improved_fold_count"] == "4", "candidate should improve four holdout folds")
    require(summary["best_holdout_control_physical_alternative"] == "false", "best holdout control must not be physical alternative")
    require(summary["tomographic_caveat_active"] == "true", "tomographic caveat must remain active")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation readiness must remain false")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(
        summary["verdict"]
        == "diagnostic_signal_survives_with_reduced_tomographic_concern_but_validation_blocked",
        "unexpected verdict",
    )
    by_component = {row["component_id"]: row for row in rows}
    require(by_component["R0_authorized_endpoint_replay"]["component_status"] == "LOW_TAIL_SIGNAL_PRESENT_NOT_VALIDATION", "R0 mismatch")
    require(
        by_component["R1_tomographic_control_disambiguation"]["component_status"]
        == "CONTROLS_BLOCK_VALIDATION_BUT_DO_NOT_REFUTE",
        "R1 mismatch",
    )
    require(by_component["R2_source_bin_holdout_replay"]["component_status"] == "HOLDS_OUT_DIAGNOSTICALLY_WITH_CAVEAT", "R2 mismatch")
    require(
        by_component["R3_best_holdout_control_source_evidence"]["component_status"]
        == "BEST_CONTROL_CONTROL_ONLY_NOT_PHYSICAL",
        "R3 mismatch",
    )
    require(by_component["R4_physical_promotion_blockers"]["component_status"] == "PHYSICAL_PROMOTION_BLOCKED", "R4 mismatch")
    require(by_component["R4_physical_promotion_blockers"]["supports_signal_survival"] == "false", "R4 must not support signal")
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_VALIDATION_READINESS_LEDGER_V1_VALIDATED "
        f"validation_ready={summary['validation_ready']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
