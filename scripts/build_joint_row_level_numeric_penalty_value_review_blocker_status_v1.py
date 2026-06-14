#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_value_review_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_value_review_blocker_not_rescoring_not_validation"


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
    response_rows = read_rows(RESPONSE_SUMMARY)
    response_present = len(response_rows) == 1
    response = response_rows[0] if response_present else {}
    values_accepted = response_present and response["numeric_penalty_values_accepted"] == "true"

    rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_BLOCKER_STATUS_V1",
            "gate_id": "NPV_GATE_1_VALUE_REVIEW_IMPORTED",
            "status": "SATISFIED" if response_present else "BLOCKED",
            "evidence": str(RESPONSE_SUMMARY.relative_to(ROOT)) if response_present else "missing response summary",
            "numeric_penalty_values_accepted": str(values_accepted).lower(),
            "cross_channel_control_alignment_authorized": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_BLOCKER_STATUS_V1",
            "gate_id": "NPV_GATE_2_NEXT_USE_BLOCKED",
            "status": "BLOCKED",
            "evidence": "accepted numeric values still require a separate lambda_row or rescoring authorization before use",
            "numeric_penalty_values_accepted": str(values_accepted).lower(),
            "cross_channel_control_alignment_authorized": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_BLOCKER_STATUS_V1",
        "review_response_imported": str(response_present).lower(),
        "review_decision": response.get("decision", "missing"),
        "numeric_penalty_values_accepted": str(values_accepted).lower(),
        "cross_channel_control_alignment_authorized": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "NUMERIC_PENALTY_VALUES_ACCEPTED_FOR_RECORD_ONLY_NEXT_USE_BLOCKED"
            if values_accepted
            else "NUMERIC_PENALTY_VALUES_NOT_ACCEPTED_OR_REVIEW_MISSING"
        ),
        "next_required_action": (
            "separate_lambda_or_rescoring_authorization_required_before_any_penalty_use"
            if values_accepted
            else "import_completed_numeric_penalty_value_review_response"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty value review blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** accepted numeric values for record only; not `lambda_row`; not `T_joint` rescoring; not endpoint validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- numeric penalty values accepted: `{summary['numeric_penalty_values_accepted']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
