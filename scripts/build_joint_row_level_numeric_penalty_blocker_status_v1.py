#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_package_v1_summary.csv"
RESPONSE_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_authorization_review_response_v1_summary.csv"
PROTOCOL_SUMMARY = ROOT / "data/derived/joint_row_level_penalty_protocol_shell_v4_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_blocker_status_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one_required(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    package = read_one_required(PACKAGE_SUMMARY)
    protocol = read_one_required(PROTOCOL_SUMMARY)
    response_rows = read_rows(RESPONSE_SUMMARY)
    response_present = len(response_rows) == 1
    response = response_rows[0] if response_present else {}

    if package["review_completed"] != "false":
        raise SystemExit("package summary should remain not completed")
    if protocol["numeric_t_joint_rescoring_allowed"] != "false":
        raise SystemExit("protocol must not allow rescoring")
    if protocol["penalty_computed"] != "false":
        raise SystemExit("protocol must not compute penalty")

    if response_present:
        numeric_authorized = response["numeric_penalty_computation_authorized"] == "true"
        response_status = response["response_status"]
        response_decision = response["decision"]
    else:
        numeric_authorized = False
        response_status = "missing"
        response_decision = "no_completed_response_imported"

    blocked = not numeric_authorized
    rows = [
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1",
            "gate_id": "RNP_GATE_1_REVIEW_RESPONSE_IMPORTED",
            "status": "SATISFIED" if response_present else "BLOCKED",
            "evidence": str(RESPONSE_SUMMARY.relative_to(ROOT)) if response_present else "no canonical response summary exists",
            "numeric_penalty_computation_allowed": str(numeric_authorized).lower(),
            "lambda_row_numeric_value_allowed": "false",
            "t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1",
            "gate_id": "RNP_GATE_2_NUMERIC_VALUES_ONLY",
            "status": "BLOCKED" if blocked else "READY_FOR_SEPARATE_PACKAGE",
            "evidence": "numeric values require imported reviewer authorization; direct T_joint rescoring remains forbidden",
            "numeric_penalty_computation_allowed": str(numeric_authorized).lower(),
            "lambda_row_numeric_value_allowed": "false",
            "t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1",
            "gate_id": "RNP_GATE_3_RESCORING",
            "status": "BLOCKED",
            "evidence": "this route cannot authorize T_joint rescoring; only a later separate gate could consider it",
            "numeric_penalty_computation_allowed": str(numeric_authorized).lower(),
            "lambda_row_numeric_value_allowed": "false",
            "t_joint_rescoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    summary = {
        "blocker_id": "JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1",
        "review_package_ready": "true",
        "review_response_imported": str(response_present).lower(),
        "review_response_status": response_status,
        "review_decision": response_decision,
        "numeric_penalty_computation_allowed": str(numeric_authorized).lower(),
        "lambda_row_numeric_value_allowed": "false",
        "t_joint_rescoring_allowed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "penalty_values_computed": "false",
        "verdict": (
            "NUMERIC_PENALTY_VALUES_BLOCKED_WAITING_FOR_REVIEW_RESPONSE"
            if blocked
            else "NUMERIC_PENALTY_VALUES_READY_FOR_SEPARATE_PACKAGE_NOT_RESCORING"
        ),
        "next_required_action": (
            "import_completed_reviewer_response_before_numeric_penalty_values"
            if blocked
            else "build_separate_numeric_penalty_value_package_without_lambda_or_rescoring"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level numeric penalty blocker status v1",
                "",
                "**Doc class:** blocker/status artifact.",
                "**Status:** not scoring; not endpoint validation; not cosmological validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact records whether the symbolic row-level penalty route may",
                "advance to numeric penalty-value computation. It never authorizes",
                "`lambda_row`, `T_joint` rescoring, endpoint replay, or validation.",
                "",
                f"- review package ready: `{summary['review_package_ready']}`",
                f"- review response imported: `{summary['review_response_imported']}`",
                f"- numeric penalty computation allowed: `{summary['numeric_penalty_computation_allowed']}`",
                f"- `lambda_row` numeric value allowed: `{summary['lambda_row_numeric_value_allowed']}`",
                f"- `T_joint` rescoring allowed: `{summary['t_joint_rescoring_allowed']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1_BUILT verdict={summary['verdict']}")


if __name__ == "__main__":
    main()
