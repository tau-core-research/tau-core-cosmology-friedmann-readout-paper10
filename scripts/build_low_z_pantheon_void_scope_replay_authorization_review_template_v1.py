#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_scope_replay_authorization_review_policy_v1.csv"
SCOPE_SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"
TEMPLATE = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_template_v1_summary.csv"


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
    scope = read_one(SCOPE_SUMMARY)
    if len(policy_rows) != 4:
        raise SystemExit("low-z authorization policy must contain four rows")
    if scope["scope_status"] != "SCOPE_CANDIDATE_FROZEN_NOT_ENDPOINT":
        raise SystemExit("low-z scope candidate must be frozen before authorization template")
    if scope["candidate_endpoint_run_allowed_now"] != "false":
        raise SystemExit("scope candidate must not pre-authorize replay")
    if scope["endpoint_scoring_allowed"] != "false":
        raise SystemExit("scope candidate must not allow endpoint scoring")

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
                "authorization_scope": "single_predeclared_low_z_pantheon_void_replay_permission_only_not_validation",
                "included_rows": scope["included_rows"],
                "z_support_max": scope["z_support_max"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "LOW_Z_PANTHEON_VOID_SCOPE_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "AUTHORIZATION_REVIEW_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "scope_candidate_id": scope["scope_id"],
            "included_rows": scope["included_rows"],
            "z_support_max": scope["z_support_max"],
            "review_completed": "false",
            "endpoint_run_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": "low_z_void_scope_replay_authorization_review_not_validation",
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_LOW_Z_VOID_SCOPE_REPLAY_AUTHORIZATION_REVIEW_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_run_allowed=false"
    )


if __name__ == "__main__":
    main()
