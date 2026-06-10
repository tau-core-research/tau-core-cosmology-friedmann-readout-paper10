#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_authorization_review_policy_v1.csv"
TEMPLATE = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_authorization_review_template_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy_rows = read_rows(POLICY)
    if len(policy_rows) != 4:
        raise SystemExit("authorization review policy must contain four rows")
    template_rows = []
    for row in policy_rows:
        template_rows.append(
            {
                "policy_id": row["policy_id"],
                "question_id": row["question_id"],
                "question_text": row["question_text"],
                "required_response": row["required_response"],
                "acceptance_condition": row["acceptance_condition"],
                "review_completed": "false",
                "reviewer_id_or_role": "",
                "reviewer_response": "",
                "reviewer_rationale": "",
                "forbidden_inputs_used": "false",
                "endpoint_run_allowed": "false",
                "physical_validation_claimed": "false",
                "authorization_scope": "single_predeclared_combined_void_web_endpoint_run_permission_only_not_validation",
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "AUTHORIZATION_REVIEW_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": "data/derived/void_web_combined_multiblock_endpoint_authorization_review_response_template_v1.csv",
            "question_count": str(len(template_rows)),
            "review_completed": "false",
            "endpoint_run_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "combined_multiblock_endpoint_authorization_review_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_AUTHORIZATION_REVIEW_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_run_allowed=false"
    )


if __name__ == "__main__":
    main()
