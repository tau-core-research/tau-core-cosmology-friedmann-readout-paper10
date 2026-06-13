#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_left_endpoint_window_decision_gate_policy_v1.csv"
PACKAGE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_left_endpoint_window_decision_gate_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_endpoint_window_decision_gate_not_validation"


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


def write_doc(row: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 left-endpoint window decision gate v1",
                "",
                "**Doc class:** source-window decision gate",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** not replay, not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This gate resolves the current status of the row-2 left endpoint",
                "source-window review. It is deliberately non-promotional: it cannot",
                "authorize endpoint replay or validation.",
                "",
                "Current gate state:",
                "",
                f"- gate status: `{row['gate_status']}`",
                f"- review completed: `{row['review_completed']}`",
                f"- source reopen caveated: `{row['source_reopen_caveated']}`",
                f"- row2 promotion ready: `{row['row2_promotion_ready']}`",
                f"- endpoint replay allowed: `{row['endpoint_replay_allowed']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                row["claim_boundary"],
                "```",
                "",
                f"Machine verdict: `{row['verdict']}`.",
                "",
            ]
        )
    )


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad row2 left decision-gate claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    package = one_row(PACKAGE_SUMMARY)
    if package["status"] != "DESI_SHAPE_ROW2_LEFT_ENDPOINT_WINDOW_REVIEW_PACKAGE_BUILT_NOT_COMPLETED":
        raise SystemExit("decision gate expects the row2 left endpoint window review package")
    if package["left_endpoint_release_allowed"] != "false":
        raise SystemExit("package must not release left endpoint")
    if package["row2_promotion_ready"] != "false":
        raise SystemExit("package must not promote row2")

    if RESPONSE_SUMMARY.exists():
        response = one_row(RESPONSE_SUMMARY)
        for field in ["left_endpoint_release_allowed", "row2_promotion_ready", "shape_route_promotion_allowed", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            if response[field] != "false":
                raise SystemExit(f"response summary {field} must remain false")
        source_reopen = response["source_reopen_caveated"] == "true"
        promotion_review_required = response["promotion_review_required_before_endpoint"] == "true"
        if source_reopen and promotion_review_required:
            gate_status = "ROW2_LEFT_SOURCE_REOPEN_CAVEATED_PROMOTION_REVIEW_REQUIRED_NOT_REPLAY"
            verdict = "row2_left_source_reopen_caveated_prepare_promotion_review_only"
            next_action = "prepare_separate_promotion_authorization_package_if_scientifically_warranted"
        elif source_reopen:
            gate_status = "ROW2_LEFT_SOURCE_REOPEN_CAVEATED_NO_REPLAY"
            verdict = "row2_left_source_reopen_caveated_no_replay"
            next_action = "record_caveated_source_reopen_keep_no_replay"
        else:
            gate_status = "ROW2_LEFT_ENDPOINT_WINDOW_BLOCKER_REMAINS_NOT_REPLAY"
            verdict = "row2_left_endpoint_window_blocker_remains_no_replay"
            next_action = "keep_row2_left_endpoint_blocked_or_find_new_source"
        review_completed = "true"
        strict_window_decision = response["strict_window_decision"]
        nearmiss_eligibility = response["nearmiss_eligibility"]
        release_policy = response["release_policy"]
    else:
        gate_status = "ROW2_LEFT_ENDPOINT_WINDOW_REVIEW_PENDING_NOT_REPLAY"
        verdict = "row2_left_endpoint_window_review_pending_no_replay"
        next_action = "wait_for_completed_external_row2_left_endpoint_window_review_response"
        review_completed = "false"
        source_reopen = False
        promotion_review_required = False
        strict_window_decision = "PENDING"
        nearmiss_eligibility = "PENDING"
        release_policy = "PENDING"

    row = {
        "gate_id": policy["gate_id"],
        "gate_status": gate_status,
        "review_package_status": package["status"],
        "review_completed": review_completed,
        "strict_window_decision": strict_window_decision,
        "nearmiss_eligibility": nearmiss_eligibility,
        "release_policy": release_policy,
        "source_reopen_caveated": "true" if source_reopen else "false",
        "promotion_review_required_before_endpoint": "true" if promotion_review_required else "false",
        "left_endpoint_release_allowed": "false",
        "row2_promotion_ready": "false",
        "shape_route_promotion_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
        "recommended_next_action": next_action,
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "gate_id": policy["gate_id"],
                "status": "DESI_SHAPE_ROW2_LEFT_ENDPOINT_WINDOW_DECISION_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION",
                **row,
            }
        ],
    )
    write_doc(row)
    print(f"PAPER10_DESI_SHAPE_ROW2_LEFT_ENDPOINT_WINDOW_DECISION_GATE_BUILT gate_status={gate_status}")


if __name__ == "__main__":
    main()
