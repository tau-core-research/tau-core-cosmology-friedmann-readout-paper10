#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALIGNED_SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_values_v1_summary.csv"
ALIGNED_BLOCKER = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1_summary.csv"
LAMBDA_SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"
NUMERIC_LAMBDA_PACKAGE = ROOT / "data/derived/joint_row_level_numeric_lambda_review_package_v1_summary.csv"
OUT = ROOT / "data/derived/joint_row_level_scoring_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_scoring_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_scoring_readiness_v1.md"
CLAIM_BOUNDARY = "joint_row_level_scoring_readiness_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    return rows[0] if len(rows) == 1 else {}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    aligned = one(ALIGNED_SUMMARY)
    aligned_blocker = one(ALIGNED_BLOCKER)
    lambda_blocker = one(LAMBDA_SUMMARY)
    lambda_package = one(NUMERIC_LAMBDA_PACKAGE)

    aligned_values_ready = (
        aligned.get("verdict") == "ALIGNED_CONTROL_VALUES_COMPUTED_NOT_RESCORING"
        and aligned.get("aligned_control_values_computed") == "true"
    )
    aligned_rescoring_blocked = aligned_blocker.get("t_joint_rescoring_authorized") == "false"
    lambda_ready = (
        lambda_blocker.get("lambda_row_numeric_value_authorized") == "true"
        and lambda_blocker.get("lambda_row_numeric_value") not in {"", None}
    )
    lambda_package_ready = (
        lambda_package.get("status") == "JOINT_ROW_LEVEL_NUMERIC_LAMBDA_REVIEW_PACKAGE_READY_NOT_COMPLETED"
    )

    gates = [
        {
            "readiness_id": "JOINT_ROW_LEVEL_SCORING_READINESS_V1",
            "gate_id": "JRSR_GATE_1_ALIGNED_CONTROL_VALUES",
            "status": "SATISFIED" if aligned_values_ready else "BLOCKED",
            "evidence": str(ALIGNED_SUMMARY.relative_to(ROOT)) if aligned_values_ready else "missing aligned-control value artifact",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "readiness_id": "JOINT_ROW_LEVEL_SCORING_READINESS_V1",
            "gate_id": "JRSR_GATE_2_NUMERIC_LAMBDA",
            "status": "SATISFIED" if lambda_ready else "BLOCKED",
            "evidence": (
                str(LAMBDA_SUMMARY.relative_to(ROOT))
                if lambda_ready
                else (
                    "numeric lambda package ready; completed reviewer response still missing"
                    if lambda_package_ready
                    else "numeric lambda package not ready"
                )
            ),
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "readiness_id": "JOINT_ROW_LEVEL_SCORING_READINESS_V1",
            "gate_id": "JRSR_GATE_3_T_JOINT_RESCORING_AUTHORIZATION",
            "status": "BLOCKED",
            "evidence": "separate post-lambda rescoring authorization required",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "readiness_id": "JOINT_ROW_LEVEL_SCORING_READINESS_V1",
            "gate_id": "JRSR_GATE_4_ENDPOINT_SCORING",
            "status": "BLOCKED",
            "evidence": "endpoint scoring remains forbidden until rescoring gate passes",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, gates)

    verdict = (
        "ROW_LEVEL_SCORING_NOT_READY_NUMERIC_LAMBDA_RESPONSE_MISSING"
        if aligned_values_ready and not lambda_ready
        else "ROW_LEVEL_SCORING_NOT_READY"
    )
    next_action = (
        "send_or_import_completed_numeric_lambda_review_response_before_any_rescoring"
        if aligned_values_ready and not lambda_ready
        else "resolve_blocked_readiness_gates"
    )
    summary = {
        "readiness_id": "JOINT_ROW_LEVEL_SCORING_READINESS_V1",
        "aligned_control_values_ready": str(aligned_values_ready).lower(),
        "aligned_control_rows": aligned.get("aligned_control_rows", ""),
        "P_row_control_mean": aligned.get("P_row_control_mean", ""),
        "aligned_rescoring_blocked": str(aligned_rescoring_blocked).lower(),
        "numeric_lambda_package_ready": str(lambda_package_ready).lower(),
        "numeric_lambda_response_imported": lambda_blocker.get("review_response_imported", "false"),
        "numeric_lambda_ready": str(lambda_ready).lower(),
        "lambda_row_numeric_value": lambda_blocker.get("lambda_row_numeric_value", ""),
        "t_joint_rescoring_authorized": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "verdict": verdict,
        "next_required_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])
    DOC.write_text(
        "\n".join(
            [
                "# Joint row-level scoring readiness v1",
                "",
                "**Doc class:** scoring-readiness ledger.",
                "**Status:** not scoring; not validation.",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`.",
                "",
                "This artifact summarizes the path toward a future row-level penalized",
                "`T_joint` scoring step. It does not compute a new score and does not",
                "authorize endpoint scoring.",
                "",
                f"- aligned control values ready: `{summary['aligned_control_values_ready']}`",
                f"- aligned control rows: `{summary['aligned_control_rows']}`",
                f"- mean aligned control `P_row`: `{summary['P_row_control_mean']}`",
                f"- numeric lambda package ready: `{summary['numeric_lambda_package_ready']}`",
                f"- numeric lambda response imported: `{summary['numeric_lambda_response_imported']}`",
                f"- numeric lambda ready: `{summary['numeric_lambda_ready']}`",
                f"- verdict: `{summary['verdict']}`",
                f"- next action: `{summary['next_required_action']}`",
                "",
                "The current blocker is the missing completed numeric-lambda review",
                "response. Even after that response, a separate rescoring authorization",
                "gate remains required before any penalized `T_joint` result.",
                "",
            ]
        )
    )
    print(f"JOINT_ROW_LEVEL_SCORING_READINESS_V1_BUILT verdict={verdict}")


if __name__ == "__main__":
    main()
