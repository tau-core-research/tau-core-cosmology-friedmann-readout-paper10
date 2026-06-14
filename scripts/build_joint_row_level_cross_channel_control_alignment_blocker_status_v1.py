#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_cross_channel_control_alignment_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_cross_channel_control_alignment_blocker_not_scoring_not_validation"


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
    accepted = present and response["decision"] == "ACCEPT_CROSS_CHANNEL_CONTROL_ALIGNMENT_DESIGN_NOT_VALUES_NOT_RESCORING_NOT_VALIDATION"
    gates = [
        ("CCA_GATE_1_REVIEW_IMPORTED", "SATISFIED" if present else "BLOCKED", str(RESPONSE_SUMMARY.relative_to(ROOT)) if present else "missing response summary"),
        ("CCA_GATE_2_ALIGNMENT_DESIGN", "SATISFIED" if accepted else "BLOCKED", "reviewer accepted design boundary" if accepted else "alignment design not accepted"),
        ("CCA_GATE_3_ALIGNED_CONTROL_VALUES", "OPEN_REQUIRED" if accepted else "BLOCKED", "separate residual-blind aligned-control value package required"),
        ("CCA_GATE_4_T_JOINT_RESCORING", "BLOCKED", "T_joint rescoring remains forbidden until aligned values and lambda policy/value pass separately"),
    ]
    out_rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_BLOCKER_STATUS_V1",
            "gate_id": gate_id,
            "status": status,
            "evidence": evidence,
            "cross_channel_control_alignment_required": str(accepted).lower(),
            "alignment_design_accepted": str(accepted).lower(),
            "aligned_joint_control_values_authorized": "false",
            "lambda_row_numeric_value_authorized": "false",
            "t_joint_rescoring_authorized": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, status, evidence in gates
    ]
    write_csv(OUT, out_rows)
    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_BLOCKER_STATUS_V1",
        "review_response_imported": str(present).lower(),
        "review_decision": response.get("decision", "missing"),
        "cross_channel_control_alignment_required": str(accepted).lower(),
        "alignment_design_accepted": str(accepted).lower(),
        "aligned_joint_control_values_authorized": "false",
        "lambda_row_numeric_value_authorized": "false",
        "t_joint_rescoring_authorized": "false",
        "endpoint_validation_claimed": "false",
        "verdict": (
            "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED"
            if accepted
            else "CROSS_CHANNEL_ALIGNMENT_DESIGN_WAITING_FOR_REVIEW_RESPONSE"
        ),
        "next_required_action": (
            "prepare_separate_residual_blind_aligned_control_value_package"
            if accepted
            else "import_completed_cross_channel_control_alignment_review_response"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level cross-channel control alignment blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** design gate only; no aligned control values; no `lambda_row`; no `T_joint` rescoring.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- review decision: `{summary['review_decision']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "This artifact may not be used as endpoint evidence. It only records whether the",
                "cross-channel alignment design has been reviewed, and whether the next non-scoring",
                "aligned-control value package can be prepared.",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
