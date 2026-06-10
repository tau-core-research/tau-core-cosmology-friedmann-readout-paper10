#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_validation_readiness_ledger_policy_v1.csv"
AUTHORIZED = ROOT / "data" / "derived" / "kids1000_cosebis_authorized_endpoint_replay_v1_summary.csv"
DISAMBIGUATION = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv"
HOLDOUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_replay_v1_summary.csv"
BEST_CONTROL = ROOT / "data" / "derived" / "kids1000_cosebis_best_tomographic_control_source_evidence_gate_v1_summary.csv"
PHYSICAL = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_validation_readiness_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_validation_readiness_ledger_v1_summary.csv"


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
    authorized = read_one(AUTHORIZED)
    disambiguation = read_one(DISAMBIGUATION)
    holdout = read_one(HOLDOUT)
    best_control = read_one(BEST_CONTROL)
    physical = read_one(PHYSICAL)

    require(policy["status"] == "VALIDATION_READINESS_LEDGER_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "readiness ledger must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "readiness ledger must not claim validation")
    require(authorized["verdict"] == "authorized_endpoint_replay_low_tail_signal_not_validation", "authorized replay state mismatch")
    require(disambiguation["tomographic_controls_refute_endpoint_signal"] == "false", "tomographic controls must not refute signal")
    require(disambiguation["accepted_physical_alternative_count"] == "0", "no tomographic control may be accepted as physical alternative")
    require(holdout["verdict"] == "holdout_replay_preserves_signal_but_tomographic_control_caveat_remains", "holdout state mismatch")
    require(best_control["verdict"] == "best_holdout_control_is_control_only_not_physical_alternative", "best control state mismatch")
    require(physical["physical_promotion_ready"] == "false", "physical promotion must remain blocked")

    rows = [
        {
            "ledger_id": policy["policy_id"],
            "component_id": "R0_authorized_endpoint_replay",
            "component_status": "LOW_TAIL_SIGNAL_PRESENT_NOT_VALIDATION",
            "evidence_summary": (
                f"delta_chi2={authorized['candidate_delta_chi2_vs_baseline']};"
                f"rank={authorized['candidate_rank_by_chi2']}/{int(authorized['null_control_count']) + 1};"
                f"tail={authorized['plus_one_tail_fraction_chi2']}"
            ),
            "supports_signal_survival": "true",
            "blocks_validation": "false",
            "recommended_next_action": "preserve_as_diagnostic_low_tail_endpoint_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "R1_tomographic_control_disambiguation",
            "component_status": "CONTROLS_BLOCK_VALIDATION_BUT_DO_NOT_REFUTE",
            "evidence_summary": (
                f"better_controls={disambiguation['better_tomographic_control_count']};"
                f"control_only={disambiguation['better_control_only_count']};"
                f"conditional_source_systematic={disambiguation['better_conditional_source_systematic_count']};"
                f"accepted_physical={disambiguation['accepted_physical_alternative_count']}"
            ),
            "supports_signal_survival": "true",
            "blocks_validation": "true",
            "recommended_next_action": "keep_tomographic_control_caveat_explicit",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "R2_source_bin_holdout_replay",
            "component_status": "HOLDS_OUT_DIAGNOSTICALLY_WITH_CAVEAT",
            "evidence_summary": (
                f"improved_folds={holdout['candidate_holdout_improved_fold_count']}/{holdout['fold_count']};"
                f"candidate_total_holdout_delta_chi2={holdout['candidate_total_holdout_delta_chi2_vs_zero']};"
                f"candidate_rank={holdout['candidate_rank_by_total_holdout_delta_chi2']}/"
                f"{holdout['comparison_branch_count']}"
            ),
            "supports_signal_survival": "true",
            "blocks_validation": "true",
            "recommended_next_action": "require_independent_tomographic_or_photoz_holdout_before_validation",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "R3_best_holdout_control_source_evidence",
            "component_status": "BEST_CONTROL_CONTROL_ONLY_NOT_PHYSICAL",
            "evidence_summary": (
                f"target={best_control['target_operator']};"
                f"global_relabel={best_control['target_is_global_source_bin_relabel']};"
                f"independent_source_evidence={best_control['target_has_independent_source_evidence']};"
                f"accepted_physical={best_control['accepted_physical_alternative_count']}"
            ),
            "supports_signal_survival": "true",
            "blocks_validation": "true",
            "recommended_next_action": "do_not_promote_best_control_without_independent_source_evidence",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "ledger_id": policy["policy_id"],
            "component_id": "R4_physical_promotion_blockers",
            "component_status": "PHYSICAL_PROMOTION_BLOCKED",
            "evidence_summary": (
                f"open_blockers={physical['open_blocker_count']};"
                f"diagnostic_ready={physical['diagnostic_endpoint_pipeline_ready']};"
                f"physical_promotion_ready={physical['physical_promotion_ready']}"
            ),
            "supports_signal_survival": "false",
            "blocks_validation": "true",
            "recommended_next_action": "resolve_operator_amplitude_and_normalization_blockers_before_physical_claims",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "VALIDATION_READINESS_LEDGER_BUILT_NOT_VALIDATION",
            "selected_statistic": policy["selected_statistic"],
            "ledger_rows": str(len(rows)),
            "low_tail_endpoint_signal_present": "true",
            "tomographic_controls_refute_endpoint_signal": "false",
            "tomographic_control_concern_reduced": "true",
            "source_bin_holdout_signal_survives": "true",
            "candidate_holdout_improved_fold_count": holdout["candidate_holdout_improved_fold_count"],
            "best_holdout_control_physical_alternative": "false",
            "tomographic_caveat_active": "true",
            "physical_promotion_ready": "false",
            "validation_ready": "false",
            "allowed_current_claim": "diagnostic_low_tail_signal_with_reduced_tomographic_control_concern_not_validation",
            "next_required_gate": "independent_tomographic_or_photoz_holdout_and_physical_promotion_blocker_resolution",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "verdict": "diagnostic_signal_survives_with_reduced_tomographic_concern_but_validation_blocked",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_VALIDATION_READINESS_LEDGER_V1_BUILT "
        f"validation_ready={summary[0]['validation_ready']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()
