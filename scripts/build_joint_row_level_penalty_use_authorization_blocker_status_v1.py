#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_penalty_use_authorization_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_penalty_use_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_use_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_use_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_use_authorization_blocker_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows(RESPONSE_SUMMARY)
    present = len(rows) == 1
    response = rows[0] if present else {}
    route_allowed = present and response["decision"] == "AUTHORIZE_PENALTY_USE_POLICY_ROUTE_PLANNING_ONLY_NOT_LAMBDA_NOT_RESCORING_NOT_VALIDATION"
    gates = [
        ("PUA_GATE_1_USE_POLICY_REVIEW_IMPORTED", "SATISFIED" if present else "BLOCKED", str(RESPONSE_SUMMARY.relative_to(ROOT)) if present else "missing response summary"),
        ("PUA_GATE_2_CROSS_CHANNEL_CONTROL_ALIGNMENT", "OPEN_REQUIRED" if route_allowed else "BLOCKED", "separate residual-blind cross-channel control alignment package required"),
        ("PUA_GATE_3_RESIDUAL_BLIND_LAMBDA_POLICY", "OPEN_REQUIRED" if route_allowed else "BLOCKED", "separate residual-blind lambda_row policy package required"),
        ("PUA_GATE_4_T_JOINT_RESCORING", "BLOCKED", "T_joint rescoring remains forbidden until gates 2 and 3 are separately accepted"),
    ]
    out_rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_BLOCKER_STATUS_V1",
            "gate_id": gate_id,
            "status": status,
            "evidence": evidence,
            "values_as_precondition_accepted": str(route_allowed).lower(),
            "cross_channel_control_alignment_required": str(route_allowed).lower(),
            "future_lambda_policy_package_allowed": str(route_allowed).lower(),
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, status, evidence in gates
    ]
    write_csv(OUT, out_rows)
    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_BLOCKER_STATUS_V1",
        "review_response_imported": str(present).lower(),
        "review_decision": response.get("decision", "missing"),
        "values_as_precondition_accepted": str(route_allowed).lower(),
        "cross_channel_control_alignment_required": str(route_allowed).lower(),
        "future_lambda_policy_package_allowed": str(route_allowed).lower(),
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "PENALTY_USE_ROUTE_PLANNING_ALLOWED_RESCORING_STILL_BLOCKED"
            if route_allowed
            else "PENALTY_USE_ROUTE_PLANNING_BLOCKED"
        ),
        "next_required_action": (
            "build_cross_channel_control_alignment_package_and_residual_blind_lambda_policy_package"
            if route_allowed
            else "import_completed_penalty_use_authorization_review_response"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level penalty use authorization blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** route planning only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "Open required gates before any penalized joint score:",
                "",
                "1. residual-blind cross-channel control alignment",
                "2. residual-blind `lambda_row` policy",
                "3. separate rescoring authorization after both gates pass",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
