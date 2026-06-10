#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = (
    ROOT
    / "data"
    / "source_manifest"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_policy_v1.csv"
)
COMPLETED_REVIEW_SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_completed_review_response_v1_summary.csv"
)
TEMPLATE = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_response_template_v1.csv"
)
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_path_partial_scope_replay_authorization_review_template_v1_summary.csv"
)
CLAIM_BOUNDARY = "v2_path_partial_scope_replay_authorization_review_not_validation"


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
    completed = read_one(COMPLETED_REVIEW_SUMMARY)
    if len(policy_rows) != 4:
        raise SystemExit("partial path replay authorization policy must contain four rows")
    if completed["review_completed"] != "true":
        raise SystemExit("partial path replay authorization requires a completed source-side review")
    if completed["final_verdict"] != "ACCEPT_PARTIAL_PATH_CONTROL_AS_CAVEATED_SOURCE_SIDE":
        raise SystemExit("partial path replay authorization requires accepted caveated source-side review")
    if completed["endpoint_replay_allowed"] != "false":
        raise SystemExit("completed source-side review must not itself authorize endpoint replay")
    if completed["endpoint_validation_claimed"] != "false":
        raise SystemExit("completed source-side review must not claim endpoint validation")
    if completed["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("completed source-side review must not claim physical lensing-path weight")
    if (
        completed["future_action_allowed"]
        != "prepare_separate_partial_scope_replay_authorization_package_only"
    ):
        raise SystemExit("completed source-side review must allow only a separate authorization package")

    template_rows = []
    for row in policy_rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']}: claim boundary mismatch")
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
                "physical_lensing_path_weight_claimed": "false",
                "authorization_scope": "single_permission_only_12_row_partial_W_path_replay_not_validation",
                "source_side_review_verdict": completed["verdict"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "source_side_review_verdict": completed["verdict"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_lensing_path_weight_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_REPLAY_AUTHORIZATION_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
