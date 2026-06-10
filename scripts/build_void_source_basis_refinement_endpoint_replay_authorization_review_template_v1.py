#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_endpoint_replay_authorization_review_policy_v1.csv"
R6_SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r6_completed_reviewer_response_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "void_source_basis_refinement_endpoint_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_endpoint_replay_authorization_review_template_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy_rows = read_rows(POLICY)
    r6 = read_one(R6_SUMMARY)
    if len(policy_rows) != 4:
        raise SystemExit("refined void authorization policy must contain four rows")
    if r6["leakage_review_complete"] != "true":
        raise SystemExit("refined void authorization requires completed R6 leakage review")
    if r6["source_unique_ready"] != "true":
        raise SystemExit("refined void authorization requires source_unique_ready=true")
    if r6["endpoint_replay_allowed"] != "false":
        raise SystemExit("R6 must not itself authorize endpoint replay")
    if r6["endpoint_validation_claimed"] != "false":
        raise SystemExit("R6 must not claim endpoint validation")

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
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "authorization_scope": "single_predeclared_refined_low_z_void_source_basis_replay_permission_only_not_validation",
                "r6_source_side_verdict": r6["verdict"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_ENDPOINT_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "r6_source_side_verdict": r6["verdict"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": "void_source_basis_refinement_endpoint_replay_authorization_review_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_REFINED_VOID_ENDPOINT_REPLAY_AUTHORIZATION_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
