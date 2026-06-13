#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/pantheon_clock_slope_route_replay_authorization_review_policy_v1.csv"
ROUTE_GATE = ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv"
TEMPLATE = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_response_template_v1.csv"
SUMMARY = ROOT / "data/derived/pantheon_clock_slope_route_replay_authorization_review_template_v1_summary.csv"
CLAIM_BOUNDARY = "clock_slope_route_replay_authorization_review_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy_rows = read_rows(POLICY)
    route = read_one(ROUTE_GATE)
    if len(policy_rows) != 4:
        raise SystemExit("clock_slope authorization policy must contain four rows")
    if route["route_status"] != "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL":
        raise SystemExit("route gate must be blocked-by-global-control before authorization template")
    if route["endpoint_replay_allowed"] != "false" or route["endpoint_validation_claimed"] != "false":
        raise SystemExit("route gate must not pre-authorize replay or validation")
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
                "authorization_scope": "single_permission_only_pantheon_clock_slope_route_replay_candidate_not_validation",
                "route_status": route["route_status"],
                "selected_route_candidate_family": route["selected_route_candidate_family"],
                "local_controls_pass": route["local_controls_pass"],
                "global_controls_pass": route["global_controls_pass"],
                "best_global_control": route["best_global_control"],
                "candidate_delta_chi2_minus_baseline": route["candidate_delta_chi2_minus_baseline"],
                "claim_boundary": row["claim_boundary"],
            }
        )
    write_csv(TEMPLATE, template_rows)
    summary = [
        {
            "policy_id": "PANTHEON_CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_REVIEW_POLICY_V1",
            "status": "CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_TEMPLATE_READY_NOT_COMPLETED",
            "template_path": str(TEMPLATE.relative_to(ROOT)),
            "question_count": str(len(template_rows)),
            "route_status": route["route_status"],
            "selected_route_candidate_family": route["selected_route_candidate_family"],
            "review_completed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_CLOCK_SLOPE_ROUTE_REPLAY_AUTHORIZATION_TEMPLATE_BUILT "
        "review_completed=false endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()
