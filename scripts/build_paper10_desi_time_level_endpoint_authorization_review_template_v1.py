#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_authorization_review_policy_v1.csv"
READINESS = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv"
TEMPLATE = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_endpoint_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy_rows = read_rows(POLICY)
    readiness = read_one(READINESS)
    if len(policy_rows) != 5:
        raise SystemExit("DESI time-level authorization policy must contain five rows")
    if readiness["verdict"] != "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing":
        raise SystemExit("readiness gate must be frozen-but-authorization-missing")
    if readiness["desi_dr2_first_cc_matched_endpoint_rows"] != "5":
        raise SystemExit("DESI endpoint scope must remain five CC-matched rows")
    if readiness["desi_time_level_control_family_count"] != "7":
        raise SystemExit("DESI control family count must remain seven")
    if readiness["open_endpoint_blockers"] != "time_level_endpoint_authorization_review_missing":
        raise SystemExit("authorization review must be the active open blocker")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if readiness[field] != "false":
            raise SystemExit(f"readiness {field} must remain false")

    template_rows: list[dict[str, str]] = []
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
                "authorization_scope": "single_permission_only_desi_cc_5row_time_level_replay_not_validation",
                "readiness_verdict": readiness["verdict"],
                "desi_first_endpoint_rows": readiness["desi_dr2_first_cc_matched_endpoint_rows"],
                "desi_control_family_count": readiness["desi_time_level_control_family_count"],
                "desi_control_seed_range": readiness["desi_time_level_control_seed_range"],
                "high_z_policy": "z2p33_excluded_as_holdout_or_future_independent_clock_support",
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "authorization_scope": "single_permission_only_desi_cc_5row_time_level_replay_not_validation",
            "readiness_verdict": readiness["verdict"],
            "desi_first_endpoint_rows": readiness["desi_dr2_first_cc_matched_endpoint_rows"],
            "desi_control_family_count": readiness["desi_time_level_control_family_count"],
            "desi_control_seed_range": readiness["desi_time_level_control_seed_range"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_AUTHORIZATION_TEMPLATE_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
