#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_post_window_review_source_plan_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_post_window_review_source_plan_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_post_window_review_source_plan_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    false_fields = [
        "left_endpoint_release_allowed",
        "row2_promotion_ready",
        "shape_route_promotion_allowed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
    ]
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(summary, false_fields, "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if summary["status"] != "DESI_SHAPE_ROW2_POST_WINDOW_REVIEW_SOURCE_PLAN_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if summary["source_plan_status"] != "ROW2_SOURCE_REOPENED_CAVEATED_LEFT_ENDPOINT_STILL_NOT_RELEASED":
        raise SystemExit("unexpected source-plan status")
    if summary["source_reopen_caveated"] != "true":
        raise SystemExit("source reopen must be caveated true")
    if summary["strict_left_endpoint_support_count"] != "0":
        raise SystemExit("left endpoint must remain without strict support")
    if summary["p0_source_target_count"] != "2":
        raise SystemExit("expected exactly two P0 source targets")
    target_ids = {row["target_id"] for row in rows}
    required_targets = {
        "ROW2_LEFT_STRICT_ENDPOINT_SUPPORT",
        "ROW2_SOURCE_NATIVE_SHAPE_SUPPORT",
        "ROW2_RIGHT_ENDPOINT_CONTEXT",
    }
    if target_ids != required_targets:
        raise SystemExit("unexpected row2 source target set")
    for row in rows:
        require_false(row, false_fields, f"row {row['target_id']}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['target_id']}")
        if "endpoint" in row["forbidden_action"] and "do_not" not in row["forbidden_action"]:
            raise SystemExit(f"forbidden action must be explicit for {row['target_id']}")
    if not DOC.exists() or DOC.stat().st_size == 0:
        raise SystemExit("missing source-plan documentation")
    print("PAPER10_DESI_SHAPE_ROW2_POST_WINDOW_REVIEW_SOURCE_PLAN_VALIDATED")


if __name__ == "__main__":
    main()
