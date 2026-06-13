#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_post_window_review_source_plan_policy_v1.csv"
DECISION = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1_summary.csv"
NEARMISS = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv"
SCOUT = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv"
PROMOTION = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_post_window_review_source_plan_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_post_window_review_source_plan_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
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


def write_doc(summary: dict[str, str], rows: list[dict[str, str]]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    table = [
        "| Priority | Target | Allowed action | Status |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    row["priority"],
                    row["target_id"],
                    row["allowed_action"],
                    row["target_status"],
                ]
            )
            + " |"
        )
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 post-window-review source plan v1",
                "",
                "**Doc class:** post-review source-side plan",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** source-side only, not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This plan freezes what is allowed after the completed row-2",
                "left-endpoint window review. The review reopens source work in a",
                "caveated way, but it does not release the left endpoint, promote",
                "row 2, or authorize endpoint replay.",
                "",
                "Gate state:",
                "",
                f"- source plan status: `{summary['source_plan_status']}`",
                f"- row2 promotion ready: `{summary['row2_promotion_ready']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                f"- recommended next action: `{summary['recommended_next_action']}`",
                "",
                "Frozen target plan:",
                "",
                *table,
                "",
                "Claim boundary:",
                "",
                "```text",
                summary["claim_boundary"],
                "```",
                "",
                f"Machine verdict: `{summary['verdict']}`.",
                "",
            ]
        )
    )


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must remain false")


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 post-window source-plan claim boundary")
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")

    decision = one_row(DECISION)
    nearmiss = one_row(NEARMISS)
    scout = one_row(SCOUT)
    promotion = one_row(PROMOTION)

    require_false(
        decision,
        [
            "left_endpoint_release_allowed",
            "row2_promotion_ready",
            "shape_route_promotion_allowed",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_validation_claimed",
        ],
        "decision gate",
    )
    require_false(
        nearmiss,
        [
            "left_endpoint_release_allowed",
            "endpoint_pair_independence_satisfied",
            "row2_promotion_ready",
            "shape_route_promotion_allowed",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_validation_claimed",
        ],
        "nearmiss freeze",
    )
    require_false(
        scout,
        [
            "endpoint_pair_independence_satisfied",
            "row2_promotion_ready",
            "shape_route_promotion_allowed",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_validation_claimed",
        ],
        "endpoint-pair scout",
    )
    require_false(
        promotion,
        [
            "endpoint_pair_independence_satisfied",
            "row2_promotion_ready",
            "shape_route_promotion_allowed",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_validation_claimed",
        ],
        "promotion gate",
    )

    source_reopened = decision["gate_status"] == "ROW2_LEFT_SOURCE_REOPEN_CAVEATED_NO_REPLAY"
    strict_left_support = nearmiss["strict_independent_left_support_count"]
    right_strict_support = scout["right_strict_independent_count"]

    if source_reopened:
        source_plan_status = "ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED"
        verdict = "row2_source_reopened_caveated_keep_endpoint_blocked"
        recommended_next = "seek_strict_left_endpoint_or_source_native_shape_support_before_any_promotion_review"
    else:
        source_plan_status = "ROW2_SOURCE_PLAN_BLOCKED_BY_LEFT_WINDOW_DECISION"
        verdict = "row2_source_plan_blocked_no_replay"
        recommended_next = "resolve_left_endpoint_window_decision_before_new_source_targets"

    base = {
        "plan_id": policy["plan_id"],
        "source_plan_status": source_plan_status,
        "strict_left_endpoint_support_count": strict_left_support,
        "right_strict_endpoint_support_count": right_strict_support,
        "left_endpoint_release_allowed": "false",
        "row2_promotion_ready": "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            **base,
            "priority": "P0",
            "target_id": "ROW2_LEFT_STRICT_ENDPOINT_SUPPORT",
            "target_status": "open",
            "allowed_action": "find_independent_clock_or_source_native_shape_support_inside_strict_left_window",
            "forbidden_action": "do_not_use_endpoint_residual_or_shape_score_to_select_source",
            "evidence_requirement": "independent_source_with_abs_delta_z_le_0p05_or_reviewer_accepted_source_native_equivalent",
        },
        {
            **base,
            "priority": "P0",
            "target_id": "ROW2_SOURCE_NATIVE_SHAPE_SUPPORT",
            "target_status": "open",
            "allowed_action": "seek_source_native_shape_or_clock_support_for_row2_interval",
            "forbidden_action": "do_not_relabel_row2_or_tune_kernel_from_endpoint_performance",
            "evidence_requirement": "source_native_support_for_0p934_to_1p321_interval_independent_of_endpoint_scores",
        },
        {
            **base,
            "priority": "P2",
            "target_id": "ROW2_RIGHT_ENDPOINT_CONTEXT",
            "target_status": "context_present_not_sufficient",
            "allowed_action": "retain_right_endpoint_context_as_supporting_context_only",
            "forbidden_action": "do_not_promote_row2_from_right_endpoint_context_alone",
            "evidence_requirement": "right_endpoint_context_already_has_strict_support_but_left_endpoint_remains_unreleased",
        },
    ]
    write_csv(OUT, rows)
    summary = {
        **base,
        "status": "DESI_SHAPE_ROW2_POST_WINDOW_REVIEW_SOURCE_PLAN_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "source_reopen_caveated": "true" if source_reopened else "false",
        "source_target_count": str(len(rows)),
        "p0_source_target_count": str(sum(1 for row in rows if row["priority"] == "P0")),
        "verdict": verdict,
        "recommended_next_action": recommended_next,
    }
    write_csv(SUMMARY, [summary])
    write_doc(summary, rows)
    print(f"PAPER10_DESI_SHAPE_ROW2_POST_WINDOW_REVIEW_SOURCE_PLAN_BUILT status={source_plan_status}")


if __name__ == "__main__":
    main()
