#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_policy_v1.csv"
W_TIME_SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_candidate_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_replay_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_replay_authorization_review_not_validation"


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
    w_time = read_one(W_TIME_SUMMARY)
    if len(policy_rows) != 4:
        raise SystemExit("W_time authorization policy must contain four rows")
    if w_time["verdict"] != "w_time_uncertainty_basis_candidate_frozen_not_endpoint_authorized":
        raise SystemExit("W_time basis candidate must be frozen before authorization template")
    if w_time["endpoint_replay_allowed"] != "false":
        raise SystemExit("W_time basis candidate must not pre-authorize replay")
    if w_time["endpoint_validation_claimed"] != "false":
        raise SystemExit("W_time basis candidate must not claim validation")

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
                "physical_validation_claimed": "false",
                "authorization_scope": "single_permission_only_low_z_W_time_uncertainty_basis_replay_not_validation",
                "source_side_basis_verdict": w_time["verdict"],
                "basis_rows": w_time["rows"],
                "W_time_min": w_time["W_time_min"],
                "W_time_max": w_time["W_time_max"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "LOW_Z_PANTHEON_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "source_side_basis_verdict": w_time["verdict"],
            "basis_rows": w_time["rows"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_W_TIME_UNCERTAINTY_BASIS_REPLAY_AUTHORIZATION_TEMPLATE_V1_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
