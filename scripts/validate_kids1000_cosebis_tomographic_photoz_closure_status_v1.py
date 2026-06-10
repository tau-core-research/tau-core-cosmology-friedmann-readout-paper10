#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_photoz_closure_status_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_photoz_closure_status_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_photoz_closure_status_v1_summary.csv"


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
    require(policy["status"] == "TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "policy must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_BUILT_NOT_VALIDATION", "unexpected status")
    require(summary["ledger_rows"] == "4", "expected four ledger rows")
    require(summary["external_photoz_source_side_closed"] == "true", "photo-z source-side closure should be complete")
    require(summary["source_bin_holdout_signal_survives"] == "true", "source-bin holdout signal should survive")
    require(summary["candidate_holdout_improved_fold_count"] == "4", "candidate should improve four folds")
    require(summary["best_holdout_control_physical_alternative"] == "false", "best control must not be physical")
    require(summary["tomographic_control_concern_reduced"] == "true", "tomographic concern should be reduced")
    require(summary["tomographic_caveat_active"] == "true", "tomographic caveat must remain active")
    require(summary["physical_promotion_ready"] == "false", "physical promotion must remain blocked")
    require(summary["validation_ready"] == "false", "validation must remain blocked")
    require(summary["computes_new_scores"] == "false", "summary must not compute scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(
        summary["verdict"] == "photoz_source_side_closed_tomographic_concern_reduced_but_validation_blocked",
        "unexpected verdict",
    )
    by_component = {row["component_id"]: row for row in rows}
    require(
        by_component["C0_external_photoz_source_side_closure"]["component_status"]
        == "SOURCE_SIDE_PHOTOZ_CLOSURE_COMPLETE",
        "C0 mismatch",
    )
    require(
        by_component["C1_source_bin_holdout_replay"]["component_status"]
        == "HOLDOUT_SIGNAL_SURVIVES_BUT_CONTROL_REMAINS",
        "C1 mismatch",
    )
    require(
        by_component["C2_best_holdout_control_gate"]["component_status"] == "BEST_CONTROL_NOT_PHYSICAL_ALTERNATIVE",
        "C2 mismatch",
    )
    require(by_component["C3_validation_readiness"]["component_status"] == "VALIDATION_STILL_BLOCKED", "C3 mismatch")
    require(by_component["C3_validation_readiness"]["blocks_validation"] == "true", "C3 must block validation")
    require({row["claim_boundary"] for row in rows} == {policy["claim_boundary"]}, "claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_V1_VALIDATED "
        f"validation_ready={summary['validation_ready']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
