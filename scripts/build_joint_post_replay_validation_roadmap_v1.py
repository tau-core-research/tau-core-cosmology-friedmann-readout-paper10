#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1_summary.csv"
KIDS = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
COV = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
CTRL = ROOT / "data/derived/joint_matched_control_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/joint_post_replay_validation_roadmap_v1.csv"
SUMMARY = ROOT / "data/derived/joint_post_replay_validation_roadmap_v1_summary.csv"
DOC = ROOT / "docs/joint_post_replay_validation_roadmap_v1.md"
CLAIM_BOUNDARY = "joint_post_replay_validation_roadmap_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    readiness = read_one(READINESS)
    kids = read_one(KIDS)
    cov = read_one(COV)
    ctrl = read_one(CTRL)

    if readiness["verdict"] != "JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION":
        raise SystemExit("unexpected readiness verdict")
    if kids["can_promote_kids_block_to_clean_joint_support"] != "false":
        raise SystemExit("KiDS caveat unexpectedly promoted")
    if cov["endpoint_scoring_allowed"] != "false" or ctrl["endpoint_scoring_allowed"] != "false":
        raise SystemExit("upstream plan unexpectedly allows scoring")

    rows = [
        {
            "roadmap_id": "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1",
            "rank": "1",
            "blocker": "kids_caveated_support_block",
            "current_state": "signal_present_but_physical_promotion_open",
            "required_exit": "close_operator_leakage_and_gauge_then_units_null_and_operator_theorem",
            "source_artifact": "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv",
            "can_execute_now": "false",
        },
        {
            "roadmap_id": "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1",
            "rank": "2",
            "blocker": "covariance_or_surrogate_closure",
            "current_state": "block_covariances_available_cross_probe_open",
            "required_exit": "source_native_cross_probe_covariance_or_reviewed_caveated_block_diagonal_surrogate",
            "source_artifact": "data/derived/joint_covariance_resolution_plan_v1_summary.csv",
            "can_execute_now": "false",
        },
        {
            "roadmap_id": "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1",
            "rank": "3",
            "blocker": "same_statistic_matched_controls",
            "current_state": "control_families_frozen_not_implemented",
            "required_exit": "instantiate_single_joint_statistic_and_build_all_control_artifacts",
            "source_artifact": "data/derived/joint_matched_control_resolution_plan_v1_summary.csv",
            "can_execute_now": "false",
        },
        {
            "roadmap_id": "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1",
            "rank": "4",
            "blocker": "separate_validation_protocol_authorization",
            "current_state": "not_prepared",
            "required_exit": "new_external_review_package_after_ranks_1_to_3_are_closed",
            "source_artifact": "future_artifact",
            "can_execute_now": "false",
        },
    ]
    for row in rows:
        row.update(
            {
                "endpoint_scoring_allowed": "false",
                "endpoint_validation_claimed": "false",
                "cosmological_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    summary = {
        "roadmap_id": "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1",
        "active_block_count": readiness["active_block_count"],
        "clean_control_resistant_blocks": readiness["clean_control_resistant_blocks"],
        "caveated_support_blocks": readiness["caveated_support_blocks"],
        "roadmap_steps": str(len(rows)),
        "executable_steps_now": str(sum(1 for row in rows if row["can_execute_now"] == "true")),
        "validation_ready": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "work_rank_1_kids_physical_promotion_or_rank_2_block_diagonal_same_statistic_package_before_any_validation_protocol",
        "verdict": "JOINT_POST_REPLAY_ROADMAP_FROZEN_VALIDATION_NOT_READY",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint post-replay validation roadmap v1",
                "",
                "**Doc class:** post-replay roadmap",
                "**Status:** not endpoint scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This roadmap consolidates the three blocker-resolution plans created after",
                "the guarded permission-only joint replay. It is intentionally non-executable:",
                "it records what must be closed before any validation-facing protocol can be",
                "prepared.",
                "",
                "Current replay status:",
                "",
                f"- active blocks: `{summary['active_block_count']}`",
                f"- clean control-resistant blocks: `{summary['clean_control_resistant_blocks']}`",
                f"- caveated support blocks: `{summary['caveated_support_blocks']}`",
                "",
                "Roadmap:",
                "",
                "1. close the KiDS/COSEBIs physical-promotion proof chain;",
                "2. close covariance via a source-native product or a reviewed caveated",
                "   block-diagonal surrogate;",
                "3. implement all same-statistic matched controls;",
                "4. only then prepare a separate validation-protocol authorization package.",
                "",
                f"Verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )
    print(
        "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()
