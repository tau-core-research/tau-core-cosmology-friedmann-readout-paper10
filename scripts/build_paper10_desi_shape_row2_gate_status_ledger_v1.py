#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_row2_gate_status_ledger_policy_v1.csv"
POST_WINDOW = ROOT / "data/derived/paper10_desi_shape_row2_post_window_review_source_plan_v1_summary.csv"
LEFT_STRICT = ROOT / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv"
SOURCE_NATIVE_SCOUT = ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv"
SOURCE_NATIVE_PACKAGE = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_package_v1_summary.csv"
)
SOURCE_NATIVE_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_review_response_v1_summary.csv"
)
PROMOTION = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
PROMOTION_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_row2_promotion_review_response_v1_summary.csv"
)
REPLAY_AUTH_RESPONSE = (
    ROOT / "data/derived/paper10_desi_shape_row2_replay_authorization_review_response_v1_summary.csv"
)
OUT = ROOT / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_gate_status_ledger_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_gate_status_ledger_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def gate_row(
    gate_id: str,
    status: str,
    artifact: Path,
    blocker: str,
    next_action: str,
    endpoint_replay_allowed: str = "false",
) -> dict[str, str]:
    return {
        "ledger_id": "PAPER10_DESI_SHAPE_ROW2_GATE_STATUS_LEDGER_V1",
        "gate_id": gate_id,
        "status": status,
        "artifact": artifact.relative_to(ROOT).as_posix(),
        "blocker": blocker,
        "next_action": next_action,
        "endpoint_replay_allowed": endpoint_replay_allowed,
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_doc(rows: list[dict[str, str]], summary: dict[str, str]) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    status_lines = [f"- `{row['gate_id']}`: `{row['status']}`" for row in rows]
    DOC.write_text(
        "\n".join(
            [
                "# Paper10 DESI shape row2 gate status ledger v1",
                "",
                "**Doc class:** gate status ledger",
                "**Reader role:** reviewer / reproducibility auditor",
                "**Status:** non-scoring; not validation",
                "**Canonical parent:** Paper10 DESI shape-route replay chain",
                "",
                "This ledger gives the current Row2 gate state without running endpoint",
                "scoring or promoting the shape route.",
                "",
                "Current gates:",
                "",
                *status_lines,
                "",
                "Current interpretation:",
                "",
                f"- overall status: `{summary['status']}`",
                f"- endpoint replay allowed: `{summary['endpoint_replay_allowed']}`",
                f"- recommended next action: `{summary['recommended_next_action']}`",
                "",
                "Claim boundary:",
                "",
                "```text",
                CLAIM_BOUNDARY,
                "```",
                "",
            ]
        )
    )


def main() -> None:
    policy = read_one(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    post_window = read_one(POST_WINDOW)
    left_strict = read_one(LEFT_STRICT)
    source_native_scout = read_one(SOURCE_NATIVE_SCOUT)
    source_native_package = read_one(SOURCE_NATIVE_PACKAGE)
    source_native_response_exists = SOURCE_NATIVE_RESPONSE.exists()
    source_native_response = read_one(SOURCE_NATIVE_RESPONSE) if source_native_response_exists else None
    promotion = read_one(PROMOTION)
    promotion_response_exists = PROMOTION_RESPONSE.exists()
    promotion_response = read_one(PROMOTION_RESPONSE) if promotion_response_exists else None
    replay_auth_response_exists = REPLAY_AUTH_RESPONSE.exists()
    replay_auth_response = read_one(REPLAY_AUTH_RESPONSE) if replay_auth_response_exists else None

    rows = [
        gate_row(
            "G1_POST_WINDOW_SOURCE_PLAN",
            post_window["source_plan_status"],
            POST_WINDOW,
            "left_endpoint_still_not_released"
            if post_window["left_endpoint_release_allowed"] == "false"
            else "none",
            post_window["recommended_next_action"],
        ),
        gate_row(
            "G2_LEFT_STRICT_SUPPORT",
            "BLOCKED_STRICT_LEFT_ENDPOINT_SUPPORT_ABSENT"
            if left_strict["strict_independent_support_count"] == "0"
            else "PASS_STRICT_LEFT_ENDPOINT_SUPPORT_PRESENT",
            LEFT_STRICT,
            "strict_independent_left_support_missing"
            if left_strict["strict_independent_support_count"] == "0"
            else "none",
            left_strict["recommended_next_action"],
        ),
        gate_row(
            "G3_SOURCE_NATIVE_SHAPE_SCOUT",
            "PASS_SOURCE_NATIVE_SHAPE_CONTEXT_PRESENT_NOT_PROMOTION_READY",
            SOURCE_NATIVE_SCOUT,
            "external_source_native_shape_review_required",
            source_native_scout["recommended_next_action"],
        ),
        gate_row(
            "G4_SOURCE_NATIVE_SHAPE_REVIEW_PACKAGE",
            "PASS_PACKAGE_READY_NOT_COMPLETED",
            SOURCE_NATIVE_PACKAGE,
            "completed_source_native_shape_review_response_missing"
            if not source_native_response_exists
            else "none",
            "send_package_to_reviewer_or_import_completed_response"
            if not source_native_response_exists
            else "use_completed_response_in_next_gate",
        ),
        gate_row(
            "G5_SOURCE_NATIVE_SHAPE_COMPLETED_RESPONSE",
            source_native_response["status"] if source_native_response else "BLOCKED_RESPONSE_MISSING",
            SOURCE_NATIVE_RESPONSE,
            "completed_source_native_shape_review_response_missing"
            if not source_native_response
            else (
                "none"
                if source_native_response["row2_source_caveat_reduced"] == "true"
                else "source_native_shape_review_not_accepted"
            ),
            "import_completed_reviewer_response"
            if not source_native_response
            else source_native_response["recommended_next_action"],
        ),
        gate_row(
            "G6_PROMOTION_READINESS",
            promotion["status"],
            PROMOTION,
            "endpoint_pair_independence_blocker_remains"
            if promotion["row2_promotion_ready"] == "false"
            else "none",
            promotion["recommended_next_action"],
        ),
        gate_row(
            "G7_PROMOTION_REVIEW_RESPONSE",
            promotion_response["status"] if promotion_response else "BLOCKED_PROMOTION_REVIEW_RESPONSE_MISSING",
            PROMOTION_RESPONSE,
            "completed_promotion_review_response_missing"
            if not promotion_response
            else (
                "none"
                if promotion_response["separate_replay_authorization_review_allowed"] == "true"
                else "promotion_review_did_not_allow_replay_authorization_handoff"
            ),
            "send_promotion_review_package_or_import_completed_response"
            if not promotion_response
            else promotion_response["recommended_next_action"],
        ),
        gate_row(
            "G8_REPLAY_AUTHORIZATION_RESPONSE",
            replay_auth_response["status"] if replay_auth_response else "BLOCKED_REPLAY_AUTHORIZATION_RESPONSE_MISSING",
            REPLAY_AUTH_RESPONSE,
            "completed_replay_authorization_response_missing"
            if not replay_auth_response
            else (
                "none"
                if replay_auth_response["endpoint_replay_allowed"] == "true"
                else "replay_authorization_not_granted"
            ),
            "send_replay_authorization_package_or_import_completed_response"
            if not replay_auth_response
            else replay_auth_response["recommended_next_action"],
            endpoint_replay_allowed="true"
            if replay_auth_response and replay_auth_response["endpoint_replay_allowed"] == "true"
            else "false",
        ),
    ]
    write_csv(OUT, rows)

    blocked_count = sum("BLOCKED" in row["status"] or "blocker" in row["blocker"] or "missing" in row["blocker"] for row in rows)
    source_native_caveat_reduced = (
        source_native_response["row2_source_caveat_reduced"] if source_native_response else "false"
    )
    separate_replay_authorization_review_allowed = (
        promotion_response["separate_replay_authorization_review_allowed"] if promotion_response else "false"
    )
    replay_permission_allowed = replay_auth_response["endpoint_replay_allowed"] if replay_auth_response else "false"
    if not source_native_response_exists:
        status = "ROW2_ENDPOINT_REPLAY_BLOCKED_SOURCE_NATIVE_REVIEW_PENDING"
        verdict = "row2_waiting_for_source_native_shape_review_no_replay"
        recommended_next_action = "import_completed_source_native_shape_review_response"
        endpoint_replay_allowed = "false"
    elif replay_auth_response and replay_permission_allowed == "true":
        status = "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION"
        verdict = replay_auth_response["verdict"]
        recommended_next_action = replay_auth_response["recommended_next_action"]
        endpoint_replay_allowed = "true"
    elif promotion_response and separate_replay_authorization_review_allowed == "true":
        status = "ROW2_SEPARATE_REPLAY_AUTH_REVIEW_ALLOWED_NOT_REPLAY"
        verdict = "row2_promotion_review_allows_separate_replay_authorization_review_no_replay"
        recommended_next_action = promotion_response["recommended_next_action"]
        endpoint_replay_allowed = "false"
    else:
        status = "ROW2_ENDPOINT_REPLAY_BLOCKED_PROMOTION_NOT_READY"
        verdict = "row2_still_blocked_after_source_native_shape_review_no_replay"
        recommended_next_action = promotion["recommended_next_action"]
        endpoint_replay_allowed = "false"

    summary = {
        "ledger_id": "PAPER10_DESI_SHAPE_ROW2_GATE_STATUS_LEDGER_V1",
        "status": status,
        "gate_count": str(len(rows)),
        "blocked_gate_count": str(blocked_count),
        "source_native_shape_response_exists": str(source_native_response_exists).lower(),
        "source_native_shape_caveat_reduced": source_native_caveat_reduced,
        "promotion_review_response_exists": str(promotion_response_exists).lower(),
        "separate_replay_authorization_review_allowed": separate_replay_authorization_review_allowed,
        "replay_authorization_response_exists": str(replay_auth_response_exists).lower(),
        "left_endpoint_release_allowed": post_window["left_endpoint_release_allowed"],
        "row2_promotion_ready": promotion["row2_promotion_ready"],
        "shape_route_promotion_allowed": promotion["shape_route_promotion_allowed"],
        "endpoint_replay_allowed": endpoint_replay_allowed,
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": verdict,
        "recommended_next_action": recommended_next_action,
    }
    write_csv(SUMMARY, [summary])
    write_doc(rows, summary)
    print(f"PAPER10_DESI_SHAPE_ROW2_GATE_STATUS_LEDGER_BUILT status={summary['status']}")


if __name__ == "__main__":
    main()
