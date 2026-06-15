#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_lambda_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_lambda_blocker_not_rescoring_not_validation"


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
    accepted = present and response["decision"] == "AUTHORIZE_NUMERIC_LAMBDA_RECORD_ONLY_NOT_RESCORING_NOT_VALIDATION"
    gates = [
        ("NL_GATE_1_REVIEW_IMPORTED", "SATISFIED" if present else "BLOCKED", str(RESPONSE_SUMMARY.relative_to(ROOT)) if present else "missing response summary"),
        ("NL_GATE_2_NUMERIC_LAMBDA_RECORD", "SATISFIED" if accepted else "BLOCKED", "reviewer authorized lambda_row=1 record-only" if accepted else "numeric lambda not authorized"),
        ("NL_GATE_3_T_JOINT_RESCORING", "BLOCKED", "T_joint rescoring remains forbidden until aligned controls and separate rescoring authorization pass"),
        ("NL_GATE_4_ENDPOINT_VALIDATION", "BLOCKED", "endpoint validation remains forbidden"),
    ]
    out_rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_BLOCKER_STATUS_V1",
            "gate_id": gate_id,
            "status": status,
            "evidence": evidence,
            "lambda_row_numeric_value_authorized": str(accepted).lower(),
            "lambda_row_numeric_value": "1.0" if accepted else "",
            "t_joint_rescoring_authorized": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, status, evidence in gates
    ]
    write_csv(OUT, out_rows)
    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_BLOCKER_STATUS_V1",
        "review_response_imported": str(present).lower(),
        "review_decision": response.get("decision", "missing"),
        "lambda_row_numeric_value_authorized": str(accepted).lower(),
        "lambda_row_numeric_value": "1.0" if accepted else "",
        "t_joint_rescoring_authorized": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "NUMERIC_LAMBDA_RECORDED_RESCORING_STILL_BLOCKED"
            if accepted
            else "NUMERIC_LAMBDA_WAITING_FOR_REVIEW_RESPONSE"
        ),
        "next_required_action": (
            "prepare_separate_T_joint_rescoring_authorization_after_aligned_values_pass"
            if accepted
            else "import_completed_numeric_lambda_review_response"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric lambda blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** numeric lambda record only; no `T_joint` rescoring.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- lambda row value: `{summary['lambda_row_numeric_value'] or 'unset'}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "This artifact may not be used as endpoint evidence. It only records",
                "whether the dimensionless unit-weight `lambda_row=1` candidate has",
                "been accepted for record. It does not authorize `T_joint` rescoring.",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_LAMBDA_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
