#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_policy.csv"
KERNEL_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv"
TEMPLATE = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_response_template.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_observer_orientation_kernel_v2_replay_authorization_template_summary.csv"
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_replay_authorization_not_validation"
AUTH_SCOPE = "single_permission_only_12_row_observer_orientation_kernel_v2_replay_not_validation"


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
    kernel = read_one(KERNEL_SUMMARY)
    if len(policy_rows) != 4:
        raise SystemExit("observer-orientation authorization policy must contain four rows")
    if kernel["status"] != "OBSERVER_ORIENTATION_KERNEL_V2_BUILT_NOT_SCORING":
        raise SystemExit("observer-orientation V2 kernel must be built before authorization")
    if kernel["endpoint_replay_allowed"] != "false" or kernel["endpoint_validation_claimed"] != "false":
        raise SystemExit("kernel must not self-authorize replay or validation")
    rows = []
    for row in policy_rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['question_id']}: claim boundary mismatch")
        rows.append(
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
                "authorization_scope": AUTH_SCOPE,
                "primary_kernel": kernel["primary_kernel"],
                "reference_kernel": kernel["reference_kernel"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(TEMPLATE, rows)
    write_csv(
        SUMMARY,
        [
            {
                "policy_id": "VOID_SOURCE_BASIS_REFINEMENT_V2_OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_POLICY",
                "status": "OBSERVER_ORIENTATION_KERNEL_V2_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
                "template_path": str(TEMPLATE.relative_to(ROOT)),
                "question_count": str(len(rows)),
                "primary_kernel": kernel["primary_kernel"],
                "review_completed": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print("PAPER10_OBSERVER_ORIENTATION_KERNEL_V2_AUTH_TEMPLATE_BUILT review_completed=false")


if __name__ == "__main__":
    main()
