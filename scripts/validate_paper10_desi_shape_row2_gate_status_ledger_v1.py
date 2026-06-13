#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_gate_status_ledger_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_gate_status_ledger_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_gate_status_ledger_not_scoring_not_validation"
EXPECTED_GATES = {
    "G1_POST_WINDOW_SOURCE_PLAN",
    "G2_LEFT_STRICT_SUPPORT",
    "G3_SOURCE_NATIVE_SHAPE_SCOUT",
    "G4_SOURCE_NATIVE_SHAPE_REVIEW_PACKAGE",
    "G5_SOURCE_NATIVE_SHAPE_COMPLETED_RESPONSE",
    "G6_PROMOTION_READINESS",
    "G7_PROMOTION_REVIEW_RESPONSE",
    "G8_REPLAY_AUTHORIZATION_RESPONSE",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 8, "expected eight Row2 gates")
    require({row["gate_id"] for row in rows} == EXPECTED_GATES, "gate set mismatch")
    for row in rows:
        if row["gate_id"] == "G8_REPLAY_AUTHORIZATION_RESPONSE":
            require(
                row["endpoint_replay_allowed"] in {"false", "true"},
                "G8 replay flag must be boolean",
            )
        else:
            require(row["endpoint_replay_allowed"] == "false", "only G8 may authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "ledger rows must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "ledger rows must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(summary["gate_count"] == "8", "bad gate count")
    require(summary["row2_promotion_ready"] == "false", "Row2 must remain non-promotion-ready")
    require(summary["shape_route_promotion_allowed"] == "false", "shape route promotion must remain false")
    require(summary["endpoint_replay_allowed"] in {"false", "true"}, "summary replay flag must be boolean")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["status"]
        in {
            "ROW2_ENDPOINT_REPLAY_BLOCKED_SOURCE_NATIVE_REVIEW_PENDING",
            "ROW2_ENDPOINT_REPLAY_BLOCKED_PROMOTION_NOT_READY",
            "ROW2_SEPARATE_REPLAY_AUTH_REVIEW_ALLOWED_NOT_REPLAY",
            "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION",
        },
        "unexpected summary status",
    )
    if summary["source_native_shape_response_exists"] == "false":
        g5 = next(row for row in rows if row["gate_id"] == "G5_SOURCE_NATIVE_SHAPE_COMPLETED_RESPONSE")
        require(g5["status"] == "BLOCKED_RESPONSE_MISSING", "missing response should block G5")
        require(
            summary["recommended_next_action"] == "import_completed_source_native_shape_review_response",
            "missing response should recommend response import",
        )
    if summary["status"] == "ROW2_SEPARATE_REPLAY_AUTH_REVIEW_ALLOWED_NOT_REPLAY":
        g7 = next(row for row in rows if row["gate_id"] == "G7_PROMOTION_REVIEW_RESPONSE")
        require(
            summary["separate_replay_authorization_review_allowed"] == "true",
            "separate replay-authorization review flag must be true for this status",
        )
        require(
            g7["status"]
            == "DESI_SHAPE_ROW2_PROMOTION_REVIEW_ACCEPTED_SEPARATE_REPLAY_AUTH_REVIEW_NOT_REPLAY",
            "G7 must contain the accepted separate-review promotion response",
        )
        require(
            summary["recommended_next_action"]
            == "build_separate_row2_replay_authorization_package_no_direct_replay",
            "separate-review status should recommend building the authorization package",
        )
    if summary["status"] == "ROW2_PERMISSION_ONLY_REPLAY_AUTHORIZED_NOT_VALIDATION":
        g8 = next(row for row in rows if row["gate_id"] == "G8_REPLAY_AUTHORIZATION_RESPONSE")
        require(summary["endpoint_replay_allowed"] == "true", "permission-only status should allow replay")
        require(g8["endpoint_replay_allowed"] == "true", "G8 should carry the replay permission")
        require(
            g8["status"] == "DESI_SHAPE_ROW2_REPLAY_AUTHORIZATION_ACCEPTED_PERMISSION_ONLY_NOT_VALIDATION",
            "G8 must contain accepted Row2 replay authorization",
        )
        require(
            summary["verdict"] == "GO_DESI_SHAPE_ROW2_REPLAY_PERMISSION_ONLY",
            "permission-only status should preserve reviewer verdict",
        )
    require(DOC.exists() and DOC.stat().st_size > 0, "missing Row2 gate ledger doc")
    print(f"PAPER10_DESI_SHAPE_ROW2_GATE_STATUS_LEDGER_VALIDATED status={summary['status']}")


if __name__ == "__main__":
    main()
