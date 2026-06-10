#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_photoz_closure_status_policy_v1.csv"
PHOTOZ = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_closure_ledger_v1_summary.csv"
HOLDOUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv"
BEST_CONTROL = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv"
READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_validation_readiness_ledger_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_photoz_closure_status_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_photoz_closure_status_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    photoz = read_one(PHOTOZ)
    holdout = read_one(HOLDOUT)
    best_control = read_one(BEST_CONTROL)
    readiness = read_one(READINESS)

    require(policy["status"] == "TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "closure status ledger must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "closure status ledger must not claim validation")
    require(photoz["h1_independent_evidence_complete"] == "true", "photo-z H1 source-side evidence must be closed")
    require(photoz["r4_leakage_review_complete"] == "true", "photo-z leakage review must be closed")
    require(photoz["endpoint_validation_claimed"] == "false", "photo-z closure must not claim validation")
    require(holdout["holdout_replay_refutes_endpoint_signal"] == "false", "holdout must not refute the signal")
    require(best_control["best_control_refutes_endpoint_signal"] == "false", "best control must not refute signal")
    require(best_control["best_control_blocks_validation"] == "true", "best control caveat must still block validation")
    require(readiness["validation_ready"] == "false", "validation must remain blocked")
    require(readiness["physical_promotion_ready"] == "false", "physical promotion must remain blocked")

    rows = [
        {
            "ledger_id": policy["policy_id"],
            "component_id": "C0_external_photoz_source_side_closure",
            "component_status": "SOURCE_SIDE_PHOTOZ_CLOSURE_COMPLETE",
            "evidence_summary": (
                f"h1_independent_evidence_complete={photoz['h1_independent_evidence_complete']};"
                f"r4_leakage_review_complete={photoz['r4_leakage_review_complete']};"
                f"endpoint_replay_allowed={photoz['endpoint_replay_allowed']}"
            ),
            "supports_tomographic_caveat_reduction": "true",
            "blocks_validation": "false",
            "recommended_next_action": "use_as_source_side_input_only_not_as_endpoint_validation",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "C1_source_bin_holdout_replay",
            "component_status": "HOLDOUT_SIGNAL_SURVIVES_BUT_CONTROL_REMAINS",
            "evidence_summary": (
                f"improved_folds={holdout['candidate_holdout_improved_fold_count']}/{holdout['fold_count']};"
                f"candidate_rank={holdout['candidate_rank_by_total_holdout_delta_chi2']}/"
                f"{holdout['comparison_branch_count']};"
                f"candidate_beating_control_count={holdout['candidate_beating_control_count']}"
            ),
            "supports_tomographic_caveat_reduction": "true",
            "blocks_validation": "true",
            "recommended_next_action": "keep_holdout_as_diagnostic_until_physical_promotion_blockers_close",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "C2_best_holdout_control_gate",
            "component_status": "BEST_CONTROL_NOT_PHYSICAL_ALTERNATIVE",
            "evidence_summary": (
                f"target={best_control['target_operator']};"
                f"independent_source_evidence={best_control['target_has_independent_source_evidence']};"
                f"accepted_physical={best_control['accepted_physical_alternative_count']}"
            ),
            "supports_tomographic_caveat_reduction": "true",
            "blocks_validation": "true",
            "recommended_next_action": "do_not_promote_control_without_independent_source_evidence",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "C3_validation_readiness",
            "component_status": "VALIDATION_STILL_BLOCKED",
            "evidence_summary": (
                f"validation_ready={readiness['validation_ready']};"
                f"tomographic_caveat_active={readiness['tomographic_caveat_active']};"
                f"physical_promotion_ready={readiness['physical_promotion_ready']}"
            ),
            "supports_tomographic_caveat_reduction": "false",
            "blocks_validation": "true",
            "recommended_next_action": "resolve_physical_promotion_blockers_before_validation_claims",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_BUILT_NOT_VALIDATION",
            "selected_statistic": policy["selected_statistic"],
            "ledger_rows": str(len(rows)),
            "external_photoz_source_side_closed": "true",
            "source_bin_holdout_signal_survives": "true",
            "candidate_holdout_improved_fold_count": holdout["candidate_holdout_improved_fold_count"],
            "best_holdout_control_physical_alternative": "false",
            "tomographic_control_concern_reduced": "true",
            "tomographic_caveat_active": "true",
            "physical_promotion_ready": "false",
            "validation_ready": "false",
            "allowed_current_claim": "source_side_photoz_closed_and_holdout_signal_survives_but_validation_blocked",
            "next_required_gate": "physical_promotion_blocker_resolution_before_validation_claim",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "verdict": "photoz_source_side_closed_tomographic_concern_reduced_but_validation_blocked",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_PHOTOZ_CLOSURE_STATUS_V1_BUILT "
        f"validation_ready={summary[0]['validation_ready']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
