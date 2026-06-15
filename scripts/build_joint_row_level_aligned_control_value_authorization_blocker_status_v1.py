#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_response_v1_summary.csv"
VALUES_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_values_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_value_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_value_authorization_blocker_not_rescoring_not_validation"


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
    accepted = present and response["decision"] == "AUTHORIZE_ALIGNED_CONTROL_VALUE_COMPUTATION_ONLY_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION"
    value_rows = read_rows(VALUES_SUMMARY)
    values_computed = (
        len(value_rows) == 1
        and value_rows[0].get("verdict") == "ALIGNED_CONTROL_VALUES_COMPUTED_NOT_RESCORING"
        and value_rows[0].get("aligned_control_values_computed") == "true"
    )
    gates = [
        ("ACV_GATE_1_REVIEW_IMPORTED", "SATISFIED" if present else "BLOCKED", str(RESPONSE_SUMMARY.relative_to(ROOT)) if present else "missing response summary"),
        ("ACV_GATE_2_VALUE_COMPUTATION_PERMISSION", "SATISFIED" if accepted else "BLOCKED", "reviewer authorized value-computation-only route" if accepted else "aligned-control value computation not authorized"),
        (
            "ACV_GATE_3_ALIGNED_VALUES",
            "SATISFIED" if values_computed else ("OPEN_REQUIRED" if accepted else "BLOCKED"),
            str(VALUES_SUMMARY.relative_to(ROOT)) if values_computed else "separate guarded non-scoring aligned-control value computation required",
        ),
        ("ACV_GATE_4_T_JOINT_RESCORING", "BLOCKED", "T_joint rescoring remains forbidden until aligned values and numeric lambda pass separately"),
    ]
    out_rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_BLOCKER_STATUS_V1",
            "gate_id": gate_id,
            "status": status,
            "evidence": evidence,
            "aligned_control_value_computation_authorized": str(accepted).lower(),
            "aligned_control_values_computed": str(values_computed).lower(),
            "aligned_joint_control_values_authorized": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, status, evidence in gates
    ]
    write_csv(OUT, out_rows)
    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_BLOCKER_STATUS_V1",
        "review_response_imported": str(present).lower(),
        "review_decision": response.get("decision", "missing"),
        "aligned_control_value_computation_authorized": str(accepted).lower(),
        "aligned_control_values_computed": str(values_computed).lower(),
        "aligned_joint_control_values_authorized": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "ALIGNED_CONTROL_VALUES_COMPUTED_RESCORING_STILL_BLOCKED"
            if values_computed
            else (
                "ALIGNED_CONTROL_VALUE_COMPUTATION_AUTHORIZED_VALUES_STILL_UNCOMPUTED"
                if accepted
                else "ALIGNED_CONTROL_VALUE_AUTHORIZATION_WAITING_FOR_REVIEW_RESPONSE"
            )
        ),
        "next_required_action": (
            "review_aligned_control_values_and_numeric_lambda_before_any_T_joint_rescoring"
            if values_computed
            else (
                "compute_aligned_control_values_in_separate_guarded_non_scoring_artifact"
                if accepted
                else "import_completed_aligned_control_value_authorization_response"
            )
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level aligned-control value authorization blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** aligned-control value gate; no `T_joint` rescoring.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- aligned control values computed: `{summary['aligned_control_values_computed']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "This artifact may not be used as endpoint evidence. It only records",
                "whether a later guarded, non-scoring aligned-control value computation",
                "may be prepared.",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
