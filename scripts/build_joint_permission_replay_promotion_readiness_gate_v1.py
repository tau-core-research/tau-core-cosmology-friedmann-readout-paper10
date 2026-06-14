#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLAY_SUMMARY = ROOT / "data/derived/joint_guarded_replay_permission_only_summary_v1.csv"
REPLAY_GRID = ROOT / "data/derived/joint_guarded_replay_permission_only_grid_v1.csv"
COV_SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
CONTROL_SUMMARY = ROOT / "data/derived/joint_matched_control_suite_requirements_gate_v1_summary.csv"
OUT = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_permission_replay_promotion_readiness_gate_v1.md"
CLAIM_BOUNDARY = "joint_permission_replay_promotion_readiness_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
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
    replay = read_one(REPLAY_SUMMARY)
    grid = read_rows(REPLAY_GRID)
    cov = read_one(COV_SUMMARY)
    controls = read_one(CONTROL_SUMMARY)

    if replay["status"] != "JOINT_GUARDED_REPLAY_PERMISSION_ONLY_COMPLETE_NOT_VALIDATION":
        raise SystemExit("joint guarded replay must be complete-not-validation")
    for field in [
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        if replay[field] != "false":
            raise SystemExit(f"unsafe replay field: {field}")
    if len(grid) != int(replay["active_block_count"]):
        raise SystemExit("grid block count mismatch")

    clean_support_blocks = [row for row in grid if row["survives_controls"] == "true"]
    caveated_blocks = [row for row in grid if row["survives_controls"] == "caveated"]
    negative_blocks = [
        row
        for row in grid
        if row["survives_controls"] not in {"true", "caveated"}
    ]

    rows = [
        {
            "criterion_id": "JPRG_01_PERMISSION_REPLAY_COMPLETE",
            "criterion": "A reviewed permission-only guarded replay has run exactly once.",
            "status": "pass",
            "evidence": replay["status"],
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_02_NO_VALIDATION_FLAGS",
            "criterion": "The replay keeps endpoint, cosmological, and physical validation claims false.",
            "status": "pass",
            "evidence": f"endpoint={replay['endpoint_validation_claimed']}; cosmology={replay['cosmological_validation_claimed']}; physical={replay['physical_validation_claimed']}",
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_03_MULTI_BLOCK_SUPPORT",
            "criterion": "All active blocks are positive or caveated-support blocks.",
            "status": "pass" if not negative_blocks else "blocked",
            "evidence": f"active={len(grid)}; clean={len(clean_support_blocks)}; caveated={len(caveated_blocks)}; negative={len(negative_blocks)}",
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_04_CAVEATED_BLOCK_REMAINS",
            "criterion": "Caveated support blocks must not be promoted as clean validation blocks.",
            "status": "blocked" if caveated_blocks else "pass",
            "evidence": ";".join(row["block_id"] for row in caveated_blocks) or "none",
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_05_COVARIANCE_NOT_FULLY_CLOSED",
            "criterion": "A validation-facing joint endpoint requires source-native cross-probe covariance or a stronger reviewed surrogate.",
            "status": "blocked"
            if cov.get("cross_probe_covariance_defined", "false") != "true"
            else "pass",
            "evidence": cov["verdict"],
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_06_CONTROL_SUITE_NOT_IMPLEMENTED",
            "criterion": "Matched controls must be implemented under the same final joint statistic and covariance discipline.",
            "status": "blocked"
            if controls.get("control_suite_implemented_under_joint_statistic", "false") != "true"
            else "pass",
            "evidence": controls["verdict"],
            "hard_blocker_if_failed": "true",
        },
        {
            "criterion_id": "JPRG_07_CLAIM_BOUNDARY",
            "criterion": "This gate records promotion readiness only and makes no validation claim.",
            "status": "pass",
            "evidence": CLAIM_BOUNDARY,
            "hard_blocker_if_failed": "true",
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
    passed = sum(1 for row in rows if row["status"] == "pass")
    blocked = sum(1 for row in rows if row["status"] == "blocked")
    hard_blockers_open = sum(
        1
        for row in rows
        if row["status"] == "blocked" and row["hard_blocker_if_failed"] == "true"
    )
    validation_ready = hard_blockers_open == 0
    verdict = (
        "JOINT_PERMISSION_REPLAY_PROMOTION_READY_FOR_SEPARATE_VALIDATION_PROTOCOL"
        if validation_ready
        else "JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION"
    )
    summary = {
        "gate_id": "JOINT_PERMISSION_REPLAY_PROMOTION_READINESS_GATE_V1",
        "active_block_count": replay["active_block_count"],
        "clean_control_resistant_blocks": str(len(clean_support_blocks)),
        "caveated_support_blocks": str(len(caveated_blocks)),
        "negative_blocks": str(len(negative_blocks)),
        "criteria_total": str(len(rows)),
        "criteria_passed": str(passed),
        "criteria_blocked": str(blocked),
        "hard_blockers_open": str(hard_blockers_open),
        "promotion_ready_for_validation_protocol": str(validation_ready).lower(),
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "next_required_action": "close_caveated_block_covariance_and_same_statistic_control_blockers_before_any_validation_protocol",
        "verdict": verdict,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint permission replay promotion-readiness gate v1",
                "",
                "**Doc class:** post-replay readiness gate",
                "**Status:** not endpoint scoring; not endpoint validation; not cosmological validation",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This gate records what the guarded permission-only joint replay permits",
                "and what it still blocks. It is deliberately conservative: a positive",
                "permission replay can motivate the next validation protocol, but it cannot",
                "itself become validation.",
                "",
                "Summary:",
                "",
                f"- active blocks: `{summary['active_block_count']}`",
                f"- clean control-resistant blocks: `{summary['clean_control_resistant_blocks']}`",
                f"- caveated support blocks: `{summary['caveated_support_blocks']}`",
                f"- hard blockers open: `{summary['hard_blockers_open']}`",
                f"- promotion ready: `{summary['promotion_ready_for_validation_protocol']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the joint replay has a coherent multi-block signal, but",
                "promotion is still blocked by at least one caveated support block, incomplete",
                "cross-probe covariance, and the lack of a fully implemented same-statistic",
                "matched-control suite.",
                "",
            ]
        )
    )
    print(
        "JOINT_PERMISSION_REPLAY_PROMOTION_READINESS_GATE_V1_BUILT "
        f"verdict={verdict} hard_blockers_open={hard_blockers_open}"
    )


if __name__ == "__main__":
    main()
