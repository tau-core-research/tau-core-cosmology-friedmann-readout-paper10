#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_lambda_policy_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_lambda_policy_blocker_not_numeric_not_scoring_not_validation"


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
    accepted = present and response["decision"] == "ACCEPT_LAMBDA_POLICY_BOUNDARY_NOT_NUMERIC_NOT_RESCORING_NOT_VALIDATION"
    gates = [
        ("LP_GATE_1_REVIEW_IMPORTED", "SATISFIED" if present else "BLOCKED", str(RESPONSE_SUMMARY.relative_to(ROOT)) if present else "missing response summary"),
        ("LP_GATE_2_POLICY_BOUNDARY", "SATISFIED" if accepted else "BLOCKED", "reviewer accepted policy boundary" if accepted else "lambda policy not accepted"),
        ("LP_GATE_3_NUMERIC_LAMBDA_VALUE", "OPEN_REQUIRED" if accepted else "BLOCKED", "separate residual-blind numeric lambda package required"),
        ("LP_GATE_4_T_JOINT_RESCORING", "BLOCKED", "T_joint rescoring remains forbidden until numeric lambda and aligned controls pass separately"),
    ]
    out_rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_LAMBDA_POLICY_BLOCKER_STATUS_V1",
            "gate_id": gate_id,
            "status": status,
            "evidence": evidence,
            "lambda_row_policy_accepted": str(accepted).lower(),
            "lambda_row_dimensionless_required": str(accepted).lower(),
            "future_numeric_lambda_package_allowed": str(accepted).lower(),
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, status, evidence in gates
    ]
    write_csv(OUT, out_rows)
    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_LAMBDA_POLICY_BLOCKER_STATUS_V1",
        "review_response_imported": str(present).lower(),
        "review_decision": response.get("decision", "missing"),
        "lambda_row_policy_accepted": str(accepted).lower(),
        "lambda_row_dimensionless_required": str(accepted).lower(),
        "future_numeric_lambda_package_allowed": str(accepted).lower(),
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED"
            if accepted
            else "LAMBDA_POLICY_WAITING_FOR_REVIEW_RESPONSE"
        ),
        "next_required_action": (
            "prepare_separate_residual_blind_numeric_lambda_package"
            if accepted
            else "import_completed_lambda_policy_review_response"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level lambda policy blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** policy gate only; no numeric `lambda_row`; no `T_joint` rescoring.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "This artifact may not be used as endpoint evidence. It only records whether the",
                "dimensionless, residual-blind lambda policy has been reviewed, and whether the",
                "next non-scoring numeric-lambda package can be prepared.",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_LAMBDA_POLICY_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
